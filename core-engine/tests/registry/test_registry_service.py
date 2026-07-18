from pathlib import Path

import pytest

from domoticsai_core.registry import RegistryLookupError, RegistryService


ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = ROOT / "config/registry/digital-twin-registry.yaml"


@pytest.fixture(scope="module")
def service() -> RegistryService:
    return RegistryService.from_file(REGISTRY_PATH)


def test_service_loads_registry(service):
    assert service.summary()["entities"] > 0
    assert service.version is not None
    assert service.interface_version is not None


def test_entity_lookup_and_topics(service):
    entity = service.require_entity("lights.living.power")
    topics = service.get_topics(entity.id)
    assert topics.state == entity.state_topic
    assert topics.command == entity.command_topic
    assert topics.ack == entity.ack_topic
    assert service.require_command_topic(entity.id) == entity.command_topic


def test_missing_entity_raises(service):
    with pytest.raises(RegistryLookupError):
        service.require_entity("missing.entity.property")


def test_queries_are_deterministic(service):
    entities = service.find_entities(domain="lights", writable=True)
    assert entities
    assert all(item.domain == "lights" and item.writable for item in entities)
    assert list(entities) == sorted(entities, key=lambda item: item.id)


def test_broker_filter(service):
    assert service.find_entities(broker="home")


def test_reverse_resolution(service):
    entity = service.require_entity("lights.living.power")
    assert service.resolve_state_topic(entity.state_topic) is entity
    assert service.resolve_command_topic(entity.command_topic) is entity
