from types import SimpleNamespace

from domoticsai_core.command_manager import (
    CommandManager,
)
from domoticsai_core.command_manager_models import (
    CommandSource,
    CreateCommandRequest,
)


class FakeStore:
    def __init__(self):
        self.commands = {}
        self.command_events = []

    def save(self, command):
        self.commands[
            command.command_id
        ] = command

    def append_event(self, event):
        self.command_events.append(event)

    def get(self, command_id):
        return self.commands.get(
            command_id
        )

    def list_recent(self, limit=100):
        return list(
            self.commands.values()
        )[-limit:]

    def events(self, command_id):
        return [
            event
            for event in self.command_events
            if event.command_id == command_id
        ]

    def list_non_terminal(self):
        return []


class FakePublisher:
    def __init__(self):
        self.publications = []

    def publish_command(
        self,
        topic,
        payload,
        *,
        qos=1,
        retain=False,
    ):
        self.publications.append({
            "topic": topic,
            "payload": payload,
            "qos": qos,
            "retain": retain,
        })


class FakeCommandRouter:
    def __init__(self):
        self.requests = []

    def resolve(self, request):
        self.requests.append(request)

        return SimpleNamespace(
            entity_id=request.entity_id,
            command_topic=(
                "registry/test/command"
            ),
            ack_topic=(
                "registry/test/ack"
            ),
            payload="unused",
            qos=1,
            retain=False,
        )


def test_command_manager_uses_optional_router():
    store = FakeStore()
    publisher = FakePublisher()
    router = FakeCommandRouter()

    manager = CommandManager(
        store,
        publisher,
        command_router=router,
        timeout_scan_seconds=60,
    )

    manager._validate = (
        lambda command: None
    )

    try:
        command = manager.create(
            CreateCommandRequest(
                domain="lights",
                action="set_state",
                target="living/power",
                parameters={
                    "state": "ON",
                },
                source=CommandSource.ANDROID,
            )
        )

    finally:
        manager.stop()

    assert len(router.requests) == 1

    routed_request = router.requests[0]

    assert (
        routed_request.entity_id
        == "lights.living.power"
    )
    assert (
        routed_request.action
        == "set_state"
    )
    assert routed_request.parameters == {
        "state": "ON",
    }
    assert (
        routed_request.source
        == "android"
    )

    assert (
        command.command_topic
        == "registry/test/command"
    )
    assert (
        command.ack_topic
        == "registry/test/ack"
    )

    assert len(
        publisher.publications
    ) == 1

    publication = (
        publisher.publications[0]
    )

    assert (
        publication["topic"]
        == "registry/test/command"
    )
    assert publication["qos"] == 1
    assert (
        publication["retain"]
        is False
    )


def test_command_manager_keeps_legacy_topics_without_router():
    command = SimpleNamespace(
        domain="lights",
        target="living/power",
        command_id="test-command-id",
    )

    command_topic, ack_topic = (
        CommandManager._build_topics(
            command
        )
    )

    assert command_topic == (
        "domoticsai/v1/cmd/"
        "lights/living/power"
    )

    assert ack_topic == (
        "domoticsai/v1/ack/"
        "lights/living/power/"
        "test-command-id"
    )


def test_dashboard_and_ai_sources_share_entity_mapping():
    dashboard_command = (
        SimpleNamespace(
            domain="lights",
            target="living/power",
            source=CommandSource.ANDROID,
        )
    )

    intelligent_command = (
        SimpleNamespace(
            domain="lights",
            target="living/power",
            source=CommandSource.AI,
        )
    )

    assert (
        CommandManager._command_entity_id(
            dashboard_command
        )
        == CommandManager._command_entity_id(
            intelligent_command
        )
        == "lights.living.power"
    )
