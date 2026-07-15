from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3
import threading
from typing import Iterator


class SQLiteDatabase:
    """
    Connessione SQLite persistente e serializzata.

    La stessa connessione viene riutilizzata per tutta la vita
    del Core Engine. L'accesso è protetto da RLock perché FastAPI,
    MQTT e il monitor dei timeout operano su thread differenti.
    """

    def __init__(self, db_path: str) -> None:
        configured_path = Path(db_path).expanduser()

        if configured_path.is_absolute():
            resolved_path = configured_path.resolve()
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

        if not resolved_path.parent.is_dir():
            raise RuntimeError(
                "Directory database non valida: "
                f"{resolved_path.parent}"
            )

        self._path = resolved_path
        self._lock = threading.RLock()
        self._closed = False

        self._connection = sqlite3.connect(
            str(self._path),
            timeout=30.0,
            check_same_thread=False,
        )

        self._connection.row_factory = sqlite3.Row

        self._configure()

    @property
    def path(self) -> Path:
        return self._path

    def _configure(self) -> None:
        with self._lock:
            self._connection.execute(
                "PRAGMA foreign_keys = ON"
            )
            self._connection.execute(
                "PRAGMA busy_timeout = 30000"
            )

            journal_mode = self._connection.execute(
                "PRAGMA journal_mode = WAL"
            ).fetchone()

            if (
                journal_mode is None
                or str(journal_mode[0]).lower() != "wal"
            ):
                raise RuntimeError(
                    "Impossibile attivare SQLite WAL"
                )

            self._connection.execute(
                "PRAGMA synchronous = NORMAL"
            )
            self._connection.commit()

    def execute(
        self,
        sql: str,
        parameters: tuple = (),
    ) -> sqlite3.Cursor:
        with self._lock:
            self._ensure_open()

            cursor = self._connection.execute(
                sql,
                parameters,
            )
            self._connection.commit()

            return cursor

    def fetchone(
        self,
        sql: str,
        parameters: tuple = (),
    ) -> sqlite3.Row | None:
        with self._lock:
            self._ensure_open()

            return self._connection.execute(
                sql,
                parameters,
            ).fetchone()

    def fetchall(
        self,
        sql: str,
        parameters: tuple = (),
    ) -> list[sqlite3.Row]:
        with self._lock:
            self._ensure_open()

            return list(
                self._connection.execute(
                    sql,
                    parameters,
                ).fetchall()
            )

    @contextmanager
    def transaction(
        self,
    ) -> Iterator[sqlite3.Connection]:
        with self._lock:
            self._ensure_open()

            try:
                yield self._connection
                self._connection.commit()
            except Exception:
                self._connection.rollback()
                raise

    def health_check(self) -> dict:
        with self._lock:
            self._ensure_open()

            quick_check = self._connection.execute(
                "PRAGMA quick_check"
            ).fetchone()

            return {
                "path": str(self._path),
                "quickCheck": (
                    quick_check[0]
                    if quick_check
                    else "unknown"
                ),
                "journalMode": self._connection.execute(
                    "PRAGMA journal_mode"
                ).fetchone()[0],
            }

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return

            self._connection.commit()
            self._connection.close()
            self._closed = True

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError(
                "Connessione SQLite già chiusa"
            )
