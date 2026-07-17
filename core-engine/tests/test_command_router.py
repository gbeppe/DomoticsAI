import json

import pytest

from domoticsai_core.command_request import (
    CommandRequest,
)
from domoticsai_core.command_router import (
    CommandEntityNotFoundError,
    CommandNotWritableError,
    CommandRouter,
    CommandTopicMissingError,
)


class FakeEntity:
    def __init__(
        self,
        *,
        entity_id="lights.living.power",
        command_topic=(
            "zara/interface/lights/living/power/cmd"
        ),
        ack_topic=(
            "zara/interface/lights/living/power/ack"
        ),
        writable=True,
    ):
        self.id = entity_id
        self.command_topic = command_topic
        self.ack_topic = ack_topic
        self.writable = writable


class FakeRegistry:
    def __init__(self, entities=None):
        self._entities = {
            entity.id: entity
            for entity in (entities or [])
        }

    def by_entity_id(self, entity_id):
        return self._entities.get(entity_id)


def test_router_can_be_created():
    router = CommandRouter(
        FakeRegistry()
    )

    assert router is not None


def test_router_resolves_writable_entity():
    entity = FakeEntity()

    router = CommandRouter(
        FakeRegistry([entity])
    )

    request = CommandRequest(
        entity_id="lights.living.power",
        action="set",
        parameters={
            "value": True,
        },
        source="android",
    )

    route = router.resolve(request)

    assert route.entity_id == entity.id
    assert route.command_topic == entity.command_topic
    assert route.ack_topic == entity.ack_topic
    assert route.qos == 1
    assert route.retain is False

    payload = json.loads(route.payload)

    assert payload == {
        "action": "set",
        "parameters": {
            "value": True,
        },
        "source": "android",
    }


def test_router_rejects_unknown_entity():
    router = CommandRouter(
        FakeRegistry()
    )

    request = CommandRequest(
        entity_id="lights.unknown.power",
        action="set",
    )

    with pytest.raises(
        CommandEntityNotFoundError
    ):
        router.resolve(request)


def test_router_rejects_non_writable_entity():
    entity = FakeEntity(
        writable=False,
    )

    router = CommandRouter(
        FakeRegistry([entity])
    )

    request = CommandRequest(
        entity_id=entity.id,
        action="set",
    )

    with pytest.raises(
        CommandNotWritableError
    ):
        router.resolve(request)


def test_router_rejects_missing_command_topic():
    entity = FakeEntity(
        command_topic=None,
    )

    router = CommandRouter(
        FakeRegistry([entity])
    )

    request = CommandRequest(
        entity_id=entity.id,
        action="set",
    )

    with pytest.raises(
        CommandTopicMissingError
    ):
        router.resolve(request)
