from dataclasses import dataclass

import pytest

from domoticsai_core.topic_mapper import (
    configure_registry,
    map_state_topic,
)


@dataclass(frozen=True)
class FakeEntity:
    domain: str
    entity_id: str


class FakeRegistry:
    def __init__(self, mappings=None):
        self._mappings = mappings or {}

    def by_state_topic(self, topic: str):
        return self._mappings.get(topic)


@pytest.fixture(autouse=True)
def reset_topic_mapper_registry():
    """Prevent Registry configuration from leaking between tests."""
    configure_registry(None)
    yield
    configure_registry(None)


def test_maps_energy_topic_with_legacy_parser():
    result = map_state_topic(
        "domoticsai/v1/state/energy/solar_power_w"
    )

    assert result is not None
    assert result.domain == "energy"
    assert result.entity == "solar_power_w"


def test_uses_registry_when_topic_is_registered():
    topic = "custom/registry/state/solar"

    configure_registry(
        FakeRegistry(
            {
                topic: FakeEntity(
                    domain="energy",
                    entity_id="solar_power_w",
                )
            }
        )
    )

    result = map_state_topic(topic)

    assert result is not None
    assert result.domain == "energy"
    assert result.entity == "solar_power_w"


def test_falls_back_to_legacy_parser_on_registry_miss():
    configure_registry(FakeRegistry())

    result = map_state_topic(
        "domoticsai/v1/state/lights/living_room"
    )

    assert result is not None
    assert result.domain == "lights"
    assert result.entity == "living_room"


def test_ignores_invalid_topic_after_registry_miss():
    configure_registry(FakeRegistry())

    assert map_state_topic(
        "domoticsai/v1/log/gateway"
    ) is None
