"""Composable filters used by RegistryService."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from .constants import LEGACY_ENDPOINT_KEYS
from .models import Entity


@dataclass(frozen=True)
class RegistryQuery:
    domain: str | None = None
    status: str | None = None
    readable: bool | None = None
    writable: bool | None = None
    historized: bool | None = None
    entity_id: str | None = None
    property_name: str | None = None
    broker: str | None = None

    def apply(self, entities: Iterable[Entity]) -> tuple[Entity, ...]:
        result = tuple(entity for entity in entities if self._matches(entity))
        return tuple(sorted(result, key=lambda item: item.id))

    def _matches(self, entity: Entity) -> bool:
        if self.domain is not None and entity.domain != self.domain:
            return False
        if self.status is not None and entity.status != self.status:
            return False
        if self.readable is not None and entity.readable is not self.readable:
            return False
        if self.writable is not None and entity.writable is not self.writable:
            return False
        if self.historized is not None and entity.historized is not self.historized:
            return False
        if self.entity_id is not None and entity.entity_id != self.entity_id:
            return False
        if self.property_name is not None and entity.property != self.property_name:
            return False
        if self.broker is not None and not _uses_broker(entity, self.broker):
            return False
        return True


def _uses_broker(entity: Entity, broker_name: str) -> bool:
    for endpoint_name in LEGACY_ENDPOINT_KEYS:
        endpoint = entity.legacy.get(endpoint_name)
        if isinstance(endpoint, Mapping) and endpoint.get("broker") == broker_name:
            return True
    return False
