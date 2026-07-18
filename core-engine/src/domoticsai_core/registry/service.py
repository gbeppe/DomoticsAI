"""Stable public query API for the DomoticsAI Digital Twin Registry."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .constants import DEFAULT_REGISTRY_PATH
from .exceptions import RegistryLookupError
from .models import Broker, Entity
from .query import RegistryQuery
from .registry import Registry, load_registry


@dataclass(frozen=True)
class RegistryTopics:
    state: str | None
    command: str | None
    ack: str | None


class RegistryService:
    """Read-only façade that is the public Registry contract."""

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    @classmethod
    def from_file(
        cls,
        path: str | Path = DEFAULT_REGISTRY_PATH,
    ) -> "RegistryService":
        return cls(load_registry(path))

    @property
    def version(self) -> str | None:
        return self._registry.version

    @property
    def interface_version(self) -> str | None:
        return self._registry.interface_version

    @property
    def source_path(self) -> Path | None:
        return self._registry.source_path

    def summary(self) -> Mapping[str, Any]:
        return self._registry.summary()

    def get_entity(self, entity_id: str) -> Entity | None:
        return self._registry.get(entity_id)

    def require_entity(self, entity_id: str) -> Entity:
        return self._registry.require(entity_id)

    def get_broker(self, name: str) -> Broker | None:
        return self._registry.brokers.get(name)

    def require_broker(self, name: str) -> Broker:
        return self._registry.broker(name)

    def get_topics(self, entity_id: str) -> RegistryTopics:
        entity = self.require_entity(entity_id)
        return RegistryTopics(
            state=entity.state_topic,
            command=entity.command_topic,
            ack=entity.ack_topic,
        )

    def get_state_topic(self, entity_id: str) -> str | None:
        return self.require_entity(entity_id).state_topic

    def get_command_topic(self, entity_id: str) -> str | None:
        return self.require_entity(entity_id).command_topic

    def require_command_topic(self, entity_id: str) -> str:
        topic = self.get_command_topic(entity_id)
        if topic is None:
            raise RegistryLookupError(f"Entità senza command topic: {entity_id}")
        return topic

    def get_ack_topic(self, entity_id: str) -> str | None:
        return self.require_entity(entity_id).ack_topic

    def get_capabilities(self, entity_id: str) -> Mapping[str, Any]:
        return self.require_entity(entity_id).capabilities

    def find_entities(
        self,
        *,
        domain: str | None = None,
        status: str | None = None,
        readable: bool | None = None,
        writable: bool | None = None,
        historized: bool | None = None,
        entity_id: str | None = None,
        property_name: str | None = None,
        broker: str | None = None,
    ) -> tuple[Entity, ...]:
        return RegistryQuery(
            domain=domain,
            status=status,
            readable=readable,
            writable=writable,
            historized=historized,
            entity_id=entity_id,
            property_name=property_name,
            broker=broker,
        ).apply(self._registry.entities)

    def resolve_state_topic(self, topic: str) -> Entity | None:
        return self._registry.by_state_topic(topic)

    def resolve_command_topic(self, topic: str) -> Entity | None:
        return self._registry.by_command_topic(topic)

    def resolve_ack_topic(self, topic: str) -> Entity | None:
        return self._registry.by_ack_topic(topic)

    def resolve_legacy_topic(self, topic: str) -> tuple[Entity, ...]:
        return self._registry.by_legacy_topic(topic)
