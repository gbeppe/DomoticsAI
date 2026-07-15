import json

from domoticsai_core.command_manager import (
    CommandManager,
)
from domoticsai_core.command_manager_models import (
    CommandSource,
    CreateCommandRequest,
)
from domoticsai_core.command_store import (
    CommandStore,
)
from domoticsai_core.sqlite_database import (
    SQLiteDatabase,
)


class FakePublisher:
    def __init__(self):
        self.messages = []

    def publish_command(
        self,
        topic,
        payload,
        *,
        qos,
        retain,
    ):
        self.messages.append({
            "topic": topic,
            "payload": payload,
            "qos": qos,
            "retain": retain,
        })


def test_accepts_known_scene(
    tmp_path,
):
    database = SQLiteDatabase(
        str(tmp_path / "scenes.db")
    )

    try:
        publisher = FakePublisher()

        manager = CommandManager(
            CommandStore(database),
            publisher,
            simulation_mode=True,
        )

        command = manager.create(
            CreateCommandRequest(
                domain="scenes",
                action="activate",
                target="TV_MODE",
                parameters={},
                source=CommandSource.ANDROID,
                timeout_seconds=15,
            )
        )

        assert (
            command.command_topic
            == (
                "domoticsai/v1/cmd/"
                "scenes/TV_MODE"
            )
        )

        assert (
            command.ack_topic
            == (
                "domoticsai/v1/ack/"
                f"scenes/TV_MODE/"
                f"{command.command_id}"
            )
        )

        assert len(publisher.messages) == 1

        payload = json.loads(
            publisher.messages[0]["payload"]
        )

        assert payload["domain"] == "scenes"
        assert payload["action"] == "activate"
        assert payload["scene_id"] == "TV_MODE"

        manager.stop()

    finally:
        database.close()


def test_rejects_unknown_scene(
    tmp_path,
):
    database = SQLiteDatabase(
        str(tmp_path / "scenes.db")
    )

    try:
        manager = CommandManager(
            CommandStore(database),
            FakePublisher(),
            simulation_mode=True,
        )

        command = manager.create(
            CreateCommandRequest(
                domain="scenes",
                action="activate",
                target="NOT_A_SCENE",
                parameters={},
                source=CommandSource.ANDROID,
                timeout_seconds=15,
            )
        )

        assert (
            command.state.value
            == "rejected"
        )

        assert (
            command.error
            == "Unknown scene: NOT_A_SCENE"
        )

        manager.stop()

    finally:
        database.close()


def test_rejects_wrong_scene_action(
    tmp_path,
):
    database = SQLiteDatabase(
        str(tmp_path / "scenes.db")
    )

    try:
        manager = CommandManager(
            CommandStore(database),
            FakePublisher(),
            simulation_mode=True,
        )

        command = manager.create(
            CreateCommandRequest(
                domain="scenes",
                action="set_state",
                target="ALL_OFF",
                parameters={},
                source=CommandSource.ANDROID,
                timeout_seconds=15,
            )
        )

        assert (
            command.state.value
            == "rejected"
        )

        manager.stop()

    finally:
        database.close()
