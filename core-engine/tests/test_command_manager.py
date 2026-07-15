import json
from pathlib import Path
from domoticsai_core.command_manager import CommandManager
from domoticsai_core.command_manager_models import CommandState, CreateCommandRequest
from domoticsai_core.command_store import CommandStore
from domoticsai_core.sqlite_database import SQLiteDatabase

class FakePublisher:
    def __init__(self):
        self.messages = []
    def publish_command(self, topic, payload, *, qos=1, retain=False):
        self.messages.append({
            'topic': topic, 'payload': payload,
            'qos': qos, 'retain': retain,
        })

def test_command_lifecycle_to_simulated(tmp_path: Path):
    publisher = FakePublisher()
    manager = CommandManager(
        CommandStore(
            SQLiteDatabase(
                str(tmp_path / 'commands.db')
            )
        ),
        publisher,
        simulation_mode=True,
    )
    command = manager.create(CreateCommandRequest(
        domain='lights', action='set_state',
        target='internal/sala', parameters={'state': 'ON'},
    ))
    assert command.state == CommandState.WAITING_CONFIRMATION
    assert publisher.messages[0]['retain'] is False
    manager.handle_mqtt_message(
        command.ack_topic,
        json.dumps({'requestId': command.command_id, 'status': 'simulated'}),
    )
    assert manager.get(command.command_id).state == CommandState.SIMULATED
    manager.stop()

def test_rejects_inactive_target(tmp_path: Path):
    manager = CommandManager(
        CommandStore(
            SQLiteDatabase(
                str(tmp_path / 'commands.db')
            )
        ),
        FakePublisher(),
    )
    command = manager.create(CreateCommandRequest(
        domain='lights', action='set_state',
        target='internal/lampadaHifi', parameters={'state': 'ON'},
    ))
    assert command.state == CommandState.REJECTED
    manager.stop()
