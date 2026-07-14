from pathlib import Path

from domoticsai_core.command_manager_models import (
    CommandRecord,
    CommandSource,
    CommandState,
)
from domoticsai_core.command_store import CommandStore


def test_rows_are_accessible_by_column_name(
    tmp_path: Path,
):
    store = CommandStore(
        str(tmp_path / "commands.db")
    )

    command = CommandRecord(
        command_id="test-command",
        domain="lights",
        action="set_state",
        target="internal/sala",
        parameters={"state": "ON"},
        source=CommandSource.ANDROID,
        state=CommandState.CREATED,
        created_at="2026-07-15T00:00:00+00:00",
        updated_at="2026-07-15T00:00:00+00:00",
        expires_at="2026-07-15T00:00:15+00:00",
        mode="simulation",
    )

    store.save(command)

    items = store.list_recent(10)

    assert len(items) == 1
    assert items[0].command_id == "test-command"
    assert items[0].target == "internal/sala"
