import json
from pathlib import Path
import sqlite3
import threading
from .models import EventRecord

class EventStore:
    def __init__(self, db_path: str):
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        with self._connect() as c:
            c.execute('''
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
            ''')

    def _connect(self):
        c = sqlite3.connect(self._path)
        c.row_factory = sqlite3.Row
        return c

    def append(self, **kwargs):
        with self._lock, self._connect() as c:
            c.execute('''
                INSERT INTO mqtt_events (
                    received_at, topic, domain, entity,
                    payload, parsed_value, quality
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                kwargs["received_at"],
                kwargs["topic"],
                kwargs["domain"],
                kwargs["entity"],
                kwargs["payload"],
                json.dumps(kwargs["parsed_value"], ensure_ascii=False),
                kwargs.get("quality"),
            ))

    def recent(self, limit=100):
        limit = max(1, min(limit, 1000))
        with self._lock, self._connect() as c:
            rows = c.execute('''
                SELECT * FROM mqtt_events
                ORDER BY id DESC LIMIT ?
            ''', (limit,)).fetchall()
        result = []
        for row in rows:
            try:
                parsed = json.loads(row["parsed_value"])
            except Exception:
                parsed = row["parsed_value"]
            result.append(EventRecord(
                id=row["id"],
                received_at=row["received_at"],
                topic=row["topic"],
                domain=row["domain"],
                entity=row["entity"],
                payload=row["payload"],
                parsed_value=parsed,
                quality=row["quality"],
            ))
        return result
