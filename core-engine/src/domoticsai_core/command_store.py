import json
from pathlib import Path
import sqlite3
import threading
from .command_manager_models import CommandEvent, CommandRecord, CommandSource, CommandState

class CommandStore:
    def __init__(self, db_path: str):
        configured_path = Path(db_path).expanduser()

        if configured_path.is_absolute():
            resolved_path = configured_path
        else:
            core_engine_root = (
                Path(__file__).resolve().parents[2]
            )
            resolved_path = (
                core_engine_root / configured_path
            ).resolve()

        resolved_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._path = resolved_path
        self._lock = threading.RLock()
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(
            self._path,
            check_same_thread=False,
        )

        connection.row_factory = sqlite3.Row

        return connection

    def _initialize(self):
        with self._connect() as connection:
            connection.execute('''
                CREATE TABLE IF NOT EXISTS commands (
                    command_id TEXT PRIMARY KEY,
                    domain TEXT NOT NULL,
                    action TEXT NOT NULL,
                    target TEXT NOT NULL,
                    parameters_json TEXT NOT NULL,
                    source TEXT NOT NULL,
                    state TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    correlation_id TEXT,
                    command_topic TEXT,
                    ack_topic TEXT,
                    error TEXT,
                    mode TEXT NOT NULL
                )
            ''')
            connection.execute('''
                CREATE TABLE IF NOT EXISTS command_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details_json TEXT NOT NULL
                )
            ''')

    def save(self, command: CommandRecord):
        with self._lock, self._connect() as connection:
            connection.execute('''
                INSERT INTO commands VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(command_id) DO UPDATE SET
                    state = excluded.state,
                    updated_at = excluded.updated_at,
                    command_topic = excluded.command_topic,
                    ack_topic = excluded.ack_topic,
                    error = excluded.error,
                    mode = excluded.mode
            ''', (
                command.command_id, command.domain, command.action, command.target,
                json.dumps(command.parameters, ensure_ascii=False), command.source.value,
                command.state.value, command.created_at, command.updated_at,
                command.expires_at, command.correlation_id, command.command_topic,
                command.ack_topic, command.error, command.mode,
            ))

    def append_event(self, event: CommandEvent):
        with self._lock, self._connect() as connection:
            connection.execute('''
                INSERT INTO command_events(command_id, state, timestamp, message, details_json)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                event.command_id, event.state.value, event.timestamp,
                event.message, json.dumps(event.details, ensure_ascii=False),
            ))

    def get(self, command_id: str):
        with self._lock, self._connect() as connection:
            row = connection.execute(
                'SELECT * FROM commands WHERE command_id = ?',
                (command_id,),
            ).fetchone()
        return self._row_to_command(row) if row else None

    def list_recent(self, limit: int = 100):
        limit = max(1, min(limit, 1000))
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                'SELECT * FROM commands ORDER BY created_at DESC LIMIT ?',
                (limit,),
            ).fetchall()
        return [self._row_to_command(row) for row in rows]

    def list_non_terminal(self):
        terminal = ('simulated', 'confirmed', 'rejected', 'timeout', 'failed')
        placeholders = ','.join('?' for _ in terminal)
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                f'SELECT * FROM commands WHERE state NOT IN ({placeholders})',
                terminal,
            ).fetchall()
        return [self._row_to_command(row) for row in rows]

    def events(self, command_id: str):
        with self._lock, self._connect() as connection:
            rows = connection.execute('''
                SELECT * FROM command_events
                WHERE command_id = ? ORDER BY id
            ''', (command_id,)).fetchall()
        return [
            CommandEvent(
                command_id=row['command_id'],
                state=CommandState(row['state']),
                timestamp=row['timestamp'],
                message=row['message'],
                details=json.loads(row['details_json']),
            )
            for row in rows
        ]

    @staticmethod
    def _row_to_command(row):
        return CommandRecord(
            command_id=row['command_id'],
            domain=row['domain'],
            action=row['action'],
            target=row['target'],
            parameters=json.loads(row['parameters_json']),
            source=CommandSource(row['source']),
            state=CommandState(row['state']),
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            expires_at=row['expires_at'],
            correlation_id=row['correlation_id'],
            command_topic=row['command_topic'],
            ack_topic=row['ack_topic'],
            error=row['error'],
            mode=row['mode'],
        )
