from datetime import datetime, timedelta, timezone
import json
import threading
from .command_manager_models import (
    CommandEvent, CommandRecord, CommandState,
    CreateCommandRequest, TERMINAL_STATES, utc_now_iso,
)
from .lights_derived import ACTIVE_DEVICES

class CommandManager:
    def __init__(self, store, publisher, *, simulation_mode=True, timeout_scan_seconds=1.0):
        self._store = store
        self._publisher = publisher
        self._simulation_mode = simulation_mode
        self._timeout_scan_seconds = timeout_scan_seconds
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._timeout_loop,
            name='command-timeout-monitor',
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=2)

    def create(self, request: CreateCommandRequest):
        now = datetime.now(timezone.utc)
        command = CommandRecord(
            domain=request.domain,
            action=request.action,
            target=request.target,
            parameters=request.parameters,
            source=request.source,
            correlation_id=request.correlation_id,
            expires_at=(now + timedelta(seconds=request.timeout_seconds)).isoformat(),
            mode='simulation' if self._simulation_mode else 'active',
        )
        self._transition(command, CommandState.CREATED, 'Command created')
        error = self._validate(command)
        if error:
            command.error = error
            self._transition(command, CommandState.REJECTED, error)
            return command
        self._transition(command, CommandState.VALIDATED, 'Command validated')
        command.command_topic, command.ack_topic = self._build_topics(command)
        self._transition(command, CommandState.QUEUED, 'Command queued')
        try:
            self._publisher.publish_command(
                command.command_topic,
                self._payload(command),
                qos=1,
                retain=False,
            )
        except Exception as exc:
            command.error = str(exc)
            self._transition(
                command, CommandState.FAILED,
                'Command publish failed', {'error': str(exc)},
            )
            return command
        self._transition(command, CommandState.SENT, 'Command published')
        self._transition(
            command, CommandState.WAITING_CONFIRMATION,
            'Waiting for acknowledgement',
        )
        return command

    def get(self, command_id):
        return self._store.get(command_id)

    def recent(self, limit=100):
        return self._store.list_recent(limit)

    def events(self, command_id):
        return self._store.events(command_id)

    def handle_mqtt_message(self, topic, payload):
        if not topic.startswith('domoticsai/v1/ack/'):
            return False
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return False
        command_id = data.get('requestId') or data.get('request_id')
        if not command_id:
            return False
        command = self._store.get(command_id)
        if command is None or command.state in TERMINAL_STATES:
            return False
        status = str(data.get('status', '')).lower()
        if status == 'simulated':
            self._transition(
                command, CommandState.SIMULATED,
                data.get('message', 'Command simulated'), data,
            )
            return True
        if status == 'confirmed':
            self._transition(
                command, CommandState.CONFIRMED,
                data.get('message', 'Command confirmed'), data,
            )
            return True
        if status in {'failed', 'rejected'}:
            command.error = data.get('message', status)
            self._transition(
                command,
                CommandState.FAILED if status == 'failed' else CommandState.REJECTED,
                command.error,
                data,
            )
            return True
        return False

    def _validate(self, command):
        if command.domain != 'lights':
            return f'Unsupported domain: {command.domain}'
        if command.action != 'set_state':
            return f'Unsupported lights action: {command.action}'
        if command.target not in ACTIVE_DEVICES:
            return f'Unknown or inactive target: {command.target}'
        desired = str(command.parameters.get('state', '')).upper()
        if desired not in {'ON', 'OFF'}:
            return 'parameters.state must be ON or OFF'
        command.parameters['state'] = desired
        return None

    @staticmethod
    def _build_topics(command):
        area, device_id = command.target.split('/', 1)
        return (
            f'domoticsai/v1/cmd/lights/{area}/{device_id}',
            f'domoticsai/v1/ack/lights/{area}/{device_id}/{command.command_id}',
        )

    @staticmethod
    def _payload(command):
        area, device_id = command.target.split('/', 1)
        return json.dumps({
            'request_id': command.command_id,
            'domain': command.domain,
            'action': command.action,
            'area': area,
            'device_id': device_id,
            'desired_state': command.parameters['state'],
            'created_at': command.created_at,
            'expires_at': command.expires_at,
            'source': command.source.value,
            'mode': command.mode,
        }, ensure_ascii=False)

    def _transition(self, command, state, message, details=None):
        command.state = state
        command.updated_at = utc_now_iso()
        self._store.save(command)
        self._store.append_event(CommandEvent(
            command_id=command.command_id,
            state=state,
            message=message,
            details=details or {},
        ))

    def _timeout_loop(self):
        while not self._stop.wait(self._timeout_scan_seconds):
            now = datetime.now(timezone.utc)
            for command in self._store.list_non_terminal():
                try:
                    expires_at = datetime.fromisoformat(command.expires_at)
                except ValueError:
                    continue
                if expires_at <= now:
                    command.error = 'Command timed out'
                    self._transition(
                        command, CommandState.TIMEOUT,
                        'Command timed out',
                    )
