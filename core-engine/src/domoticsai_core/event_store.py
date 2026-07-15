from __future__ import annotations

import json
from typing import Any

from .models import EventRecord, TwinValue
from .sqlite_database import SQLiteDatabase


class EventStore:
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
                CREATE TABLE IF NOT EXISTS mqtt_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    received_at TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    parsed_value TEXT,
                    quality TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_mqtt_events_received_at
                ON mqtt_events(received_at DESC)
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS twin_state (
                    domain TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    value_json TEXT NOT NULL,
                    unit TEXT,
                    quality TEXT NOT NULL,
                    source TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    PRIMARY KEY (domain, entity)
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_twin_state_timestamp
                ON twin_state(timestamp DESC)
                """
            )

    def append(
        self,
        *,
        received_at: str,
        topic: str,
        domain: str,
        entity: str,
        payload: str,
        parsed_value: Any,
        quality: str | None,
    ) -> None:
        serialized_value = json.dumps(
            parsed_value,
            ensure_ascii=False,
        )

        self._database.execute(
            """
            INSERT INTO mqtt_events (
                received_at,
                topic,
                domain,
                entity,
                payload,
                parsed_value,
                quality
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                received_at,
                topic,
                domain,
                entity,
                payload,
                serialized_value,
                quality,
            ),
        )

    def upsert_twin_value(
        self,
        *,
        domain: str,
        entity: str,
        value: TwinValue,
    ) -> None:
        self._database.execute(
            """
            INSERT INTO twin_state (
                domain,
                entity,
                value_json,
                unit,
                quality,
                source,
                timestamp,
                topic
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(domain, entity) DO UPDATE SET
                value_json = excluded.value_json,
                unit = excluded.unit,
                quality = excluded.quality,
                source = excluded.source,
                timestamp = excluded.timestamp,
                topic = excluded.topic
            """,
            (
                domain,
                entity,
                json.dumps(
                    value.value,
                    ensure_ascii=False,
                ),
                value.unit,
                value.quality,
                value.source,
                value.timestamp,
                value.topic,
            ),
        )

    def load_twin_state(
        self,
    ) -> dict[str, dict[str, TwinValue]]:
        rows = self._database.fetchall(
            """
            SELECT
                domain,
                entity,
                value_json,
                unit,
                quality,
                source,
                timestamp,
                topic
            FROM twin_state
            ORDER BY domain, entity
            """
        )

        result: dict[
            str,
            dict[str, TwinValue],
        ] = {}

        for row in rows:
            try:
                parsed_value = json.loads(
                    row["value_json"]
                )
            except json.JSONDecodeError:
                parsed_value = row["value_json"]

            result.setdefault(
                row["domain"],
                {},
            )[row["entity"]] = TwinValue(
                value=parsed_value,
                unit=row["unit"],
                quality=row["quality"],
                source=row["source"],
                timestamp=row["timestamp"],
                topic=row["topic"],
            )

        return result

    def clear_twin_state(self) -> None:
        self._database.execute(
            "DELETE FROM twin_state"
        )

    def recent(
        self,
        limit: int = 100,
    ) -> list[EventRecord]:
        bounded_limit = max(
            1,
            min(limit, 1000),
        )

        rows = self._database.fetchall(
            """
            SELECT
                id,
                received_at,
                topic,
                domain,
                entity,
                payload,
                parsed_value,
                quality
            FROM mqtt_events
            ORDER BY id DESC
            LIMIT ?
            """,
            (bounded_limit,),
        )

        result: list[EventRecord] = []

        for row in rows:
            parsed_value = None

            if row["parsed_value"] is not None:
                try:
                    parsed_value = json.loads(
                        row["parsed_value"]
                    )
                except json.JSONDecodeError:
                    parsed_value = row[
                        "parsed_value"
                    ]

            result.append(
                EventRecord(
                    id=row["id"],
                    received_at=row[
                        "received_at"
                    ],
                    topic=row["topic"],
                    domain=row["domain"],
                    entity=row["entity"],
                    payload=row["payload"],
                    parsed_value=parsed_value,
                    quality=row["quality"],
                )
            )

        return result
