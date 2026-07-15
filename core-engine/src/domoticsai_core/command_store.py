from __future__ import annotations

import json

from .command_manager_models import (
    CommandEvent,
    CommandRecord,
    CommandSource,
    CommandState,
)
from .sqlite_database import SQLiteDatabase


class CommandStore:
    def __init__(
        self,
        database: SQLiteDatabase,
    ) -> None:
        self._database = database
        self._initialize()

    def _initialize(self) -> None:
        with self._database.transaction() as connection:
            connection.execute(
                """
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
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS command_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details_json TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_commands_state
                ON commands(state)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_command_events_command
                ON command_events(command_id, id)
                """
            )

    def save(
        self,
        command: CommandRecord,
    ) -> None:
        self._database.execute(
            """
            INSERT INTO commands (
                command_id,
                domain,
                action,
                target,
                parameters_json,
                source,
                state,
                created_at,
                updated_at,
                expires_at,
                correlation_id,
                command_topic,
                ack_topic,
                error,
                mode
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ON CONFLICT(command_id) DO UPDATE SET
                domain = excluded.domain,
                action = excluded.action,
                target = excluded.target,
                parameters_json = excluded.parameters_json,
                source = excluded.source,
                state = excluded.state,
                updated_at = excluded.updated_at,
                expires_at = excluded.expires_at,
                correlation_id = excluded.correlation_id,
                command_topic = excluded.command_topic,
                ack_topic = excluded.ack_topic,
                error = excluded.error,
                mode = excluded.mode
            """,
            (
                command.command_id,
                command.domain,
                command.action,
                command.target,
                json.dumps(
                    command.parameters,
                    ensure_ascii=False,
                ),
                command.source.value,
                command.state.value,
                command.created_at,
                command.updated_at,
                command.expires_at,
                command.correlation_id,
                command.command_topic,
                command.ack_topic,
                command.error,
                command.mode,
            ),
        )

    def append_event(
        self,
        event: CommandEvent,
    ) -> None:
        self._database.execute(
            """
            INSERT INTO command_events (
                command_id,
                state,
                timestamp,
                message,
                details_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.command_id,
                event.state.value,
                event.timestamp,
                event.message,
                json.dumps(
                    event.details,
                    ensure_ascii=False,
                ),
            ),
        )

    def get(
        self,
        command_id: str,
    ) -> CommandRecord | None:
        row = self._database.fetchone(
            """
            SELECT *
            FROM commands
            WHERE command_id = ?
            """,
            (command_id,),
        )

        if row is None:
            return None

        return self._row_to_command(row)

    def list_recent(
        self,
        limit: int = 100,
    ) -> list[CommandRecord]:
        safe_limit = max(
            1,
            min(limit, 1000),
        )

        rows = self._database.fetchall(
            """
            SELECT *
            FROM commands
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (safe_limit,),
        )

        return [
            self._row_to_command(row)
            for row in rows
        ]

    def list_non_terminal(
        self,
    ) -> list[CommandRecord]:
        terminal_states = (
            CommandState.SIMULATED.value,
            CommandState.CONFIRMED.value,
            CommandState.REJECTED.value,
            CommandState.TIMEOUT.value,
            CommandState.FAILED.value,
        )

        placeholders = ",".join(
            "?"
            for _ in terminal_states
        )

        rows = self._database.fetchall(
            f"""
            SELECT *
            FROM commands
            WHERE state NOT IN ({placeholders})
            """,
            terminal_states,
        )

        return [
            self._row_to_command(row)
            for row in rows
        ]

    def events(
        self,
        command_id: str,
    ) -> list[CommandEvent]:
        rows = self._database.fetchall(
            """
            SELECT *
            FROM command_events
            WHERE command_id = ?
            ORDER BY id
            """,
            (command_id,),
        )

        return [
            CommandEvent(
                command_id=row["command_id"],
                state=CommandState(
                    row["state"]
                ),
                timestamp=row["timestamp"],
                message=row["message"],
                details=json.loads(
                    row["details_json"]
                ),
            )
            for row in rows
        ]

    @staticmethod
    def _row_to_command(
        row,
    ) -> CommandRecord:
        return CommandRecord(
            command_id=row["command_id"],
            domain=row["domain"],
            action=row["action"],
            target=row["target"],
            parameters=json.loads(
                row["parameters_json"]
            ),
            source=CommandSource(
                row["source"]
            ),
            state=CommandState(
                row["state"]
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            expires_at=row["expires_at"],
            correlation_id=row["correlation_id"],
            command_topic=row["command_topic"],
            ack_topic=row["ack_topic"],
            error=row["error"],
            mode=row["mode"],
        )
