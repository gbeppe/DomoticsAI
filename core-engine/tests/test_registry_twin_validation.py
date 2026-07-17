from dataclasses import dataclass

import pytest

from domoticsai_core.digital_twin import DigitalTwinStore
from domoticsai_core.topic_mapper import configure_registry


@pytest.fixture(autouse=True)
def reset_topic_mapper_registry():
    configure_registry(None)
    yield
    configure_registry(None)


@dataclass(frozen=True)
class FakeRegistryEntity:
    domain: str
    entity_id: str


class FakeRegistry:
    def __init__(self, mappings=None):
        self._mappings = mappings or {}

    def by_state_topic(self, topic: str):
        return self._mappings.get(topic)


class FakeEventStore:
    def __init__(self):
        self.upserts = []
        self.events = []

    def load_twin_state(self):
        return {}

    def upsert_twin_value(
        self,
        *,
        domain,
        entity,
        value,
        updated_at=None,
    ):
        self.upserts.append(
            {
                "domain": domain,
                "entity": entity,
                "value": value,
                "updated_at": updated_at,
            }
        )

    def append(self, **event):
        self.events.append(event)


def test_accepts_topic_registered_in_registry():
    topic = (
        "domoticsai/v1/state/"
        "energy/solar_power_w"
    )

    registry = FakeRegistry(
        {
            topic: FakeRegistryEntity(
                domain="energy",
                entity_id="solar_power_w",
            )
        }
    )

    configure_registry(registry)

    event_store = FakeEventStore()
    twin = DigitalTwinStore(
        event_store,
        registry=registry,
    )

    initial_events = len(event_store.events)

    accepted = twin.update_from_mqtt(
        topic,
        '{"value": 2500, "unit": "W"}',
    )

    assert accepted is True
    assert len(event_store.events) == initial_events + 1
    assert event_store.events[-1]["domain"] == "energy"
    assert (
        event_store.events[-1]["entity"]
        == "solar_power_w"
    )


def test_rejects_valid_legacy_topic_missing_from_registry():
    registry = FakeRegistry()

    configure_registry(registry)

    event_store = FakeEventStore()
    twin = DigitalTwinStore(
        event_store,
        registry=registry,
    )

    initial_events = len(event_store.events)
    initial_upserts = len(event_store.upserts)

    accepted = twin.update_from_mqtt(
        "domoticsai/v1/state/lights/unknown_light",
        '{"value": true}',
    )

    assert accepted is False
    assert len(event_store.events) == initial_events
    assert len(event_store.upserts) == initial_upserts


def test_preserves_legacy_behavior_without_registry():
    event_store = FakeEventStore()
    twin = DigitalTwinStore(event_store)

    initial_events = len(event_store.events)

    accepted = twin.update_from_mqtt(
        "domoticsai/v1/state/lights/legacy_light",
        '{"value": true}',
    )

    assert accepted is True
    assert len(event_store.events) == initial_events + 1
    assert event_store.events[-1]["domain"] == "lights"
    assert (
        event_store.events[-1]["entity"]
        == "legacy_light"
    )
