from pathlib import Path
import threading

from domoticsai_core.sqlite_database import (
    SQLiteDatabase,
)


def test_persistent_connection_and_health(
    tmp_path: Path,
):
    database = SQLiteDatabase(
        str(tmp_path / "core-engine.db")
    )

    database.execute(
        """
        CREATE TABLE test_values (
            id INTEGER PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    database.execute(
        """
        INSERT INTO test_values(value)
        VALUES (?)
        """,
        ("ok",),
    )

    row = database.fetchone(
        """
        SELECT value
        FROM test_values
        WHERE id = 1
        """
    )

    assert row is not None
    assert row["value"] == "ok"

    health = database.health_check()

    assert health["quickCheck"] == "ok"
    assert health["journalMode"].lower() == "wal"

    database.close()


def test_serialized_access_from_threads(
    tmp_path: Path,
):
    database = SQLiteDatabase(
        str(tmp_path / "threads.db")
    )

    database.execute(
        """
        CREATE TABLE counters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL
        )
        """
    )

    def worker(offset: int):
        for index in range(25):
            database.execute(
                """
                INSERT INTO counters(value)
                VALUES (?)
                """,
                (offset + index,),
            )

    threads = [
        threading.Thread(
            target=worker,
            args=(worker_index * 100,),
        )
        for worker_index in range(4)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    row = database.fetchone(
        "SELECT COUNT(*) AS total FROM counters"
    )

    assert row is not None
    assert row["total"] == 100

    database.close()
