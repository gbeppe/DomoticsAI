#!/usr/bin/env bash
set -euo pipefail

cd "${1:-.}"

PKG="core-engine/src/domoticsai_core/registry"
TESTDIR="core-engine/tests/registry"
REGISTRY="config/registry/digital-twin-registry.yaml"

for f in "$REGISTRY" "$PKG/__init__.py" "$PKG/registry.py" "$PKG/models.py" "$PKG/exceptions.py"; do
  [[ -f "$f" ]] || { echo "ERRORE: manca $f" >&2; exit 1; }
done

TARGETS=(
  "$PKG/service.py"
  "$PKG/query.py"
  "$TESTDIR/test_registry_service.py"
  "docs/ADR/ADR-019-registry-service-api.md"
  "docs/Registry/REGISTRY_SERVICE_API.md"
)

for f in "${TARGETS[@]}"; do
  [[ ! -e "$f" ]] || { echo "ERRORE: $f esiste già; nessuna modifica eseguita." >&2; exit 1; }
done

mkdir -p "$TESTDIR" docs/ADR docs/Registry

cat > "$PKG/query.py" <<'PY'
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
PY

cat > "$PKG/service.py" <<'PY'
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
PY

cat > "$TESTDIR/test_registry_service.py" <<'PY'
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
PY

cat > docs/ADR/ADR-019-registry-service-api.md <<'MD'
# ADR-019 — Registry Service API

- **Status:** Accepted
- **Date:** 2026-07-18
- **Owners:** Architecture, Core Engine
- **Decision scope:** Consumers of the Digital Twin Registry

## Context

ADR-018 established `config/registry/digital-twin-registry.yaml` as the
authoritative declaration of entities, capabilities, interfaces and physical
bindings.

Direct YAML consumption by multiple components would make the serialization
format an accidental public contract and permit incompatible lookup semantics.

## Decision

The public in-process contract is `RegistryService`.

Consumers obtain Registry information through service methods instead of
navigating YAML or depending on private indexes.

The initial API includes entity and broker lookup, canonical topic lookup,
reverse topic resolution, capability lookup, deterministic queries and Registry
metadata.

The YAML remains the authoritative persisted representation, but it is not the
consumer API.

## Boundaries

`RegistryService` is read-only, loads one Registry snapshot, exposes no secrets,
publishes no MQTT and executes no business logic.

A future HTTP or MQTT projection may wrap the same semantic contract.

## Compatibility

Breaking changes to public methods, parameters, return semantics or errors
require an ADR and API-version change.

## Consequences

- Core Engine gains a stable abstraction over Registry storage.
- YAML structure may evolve behind the service boundary.
- Direct YAML access outside Registry tooling becomes architectural debt.
- Existing consumers are migrated gradually, not rewritten by this ADR.

## Related

- ADR-018 — Digital Twin Registry as Single Source of Truth
- `docs/Registry/REGISTRY_SERVICE_API.md`
MD

cat > docs/Registry/REGISTRY_SERVICE_API.md <<'MD'
# Registry Service API 1.0

- **Status:** Active
- **Owner:** Core Engine / Registry
- **Related ADR:** ADR-019
- **Implementation:** `core-engine/src/domoticsai_core/registry/service.py`

## Purpose

`RegistryService` is the stable, read-only API used to query declarative system
knowledge. It hides YAML traversal and Registry index implementation.

## Construction

```python
from domoticsai_core.registry import RegistryService

registry = RegistryService.from_file(
    "config/registry/digital-twin-registry.yaml"
)
```

Use one instance per process.

## Main methods

```python
registry.get_entity(entity_id)
registry.require_entity(entity_id)
registry.get_capabilities(entity_id)
registry.get_topics(entity_id)
registry.get_state_topic(entity_id)
registry.get_command_topic(entity_id)
registry.require_command_topic(entity_id)
registry.get_ack_topic(entity_id)
registry.get_broker(name)
registry.require_broker(name)
```

## Queries

```python
registry.find_entities(
    domain="lights",
    writable=True,
    broker="home",
)
```

Filters use AND semantics and results are sorted by logical ID.

Supported filters: `domain`, `status`, `readable`, `writable`, `historized`,
`entity_id`, `property_name`, `broker`.

## Reverse resolution

```python
registry.resolve_state_topic(topic)
registry.resolve_command_topic(topic)
registry.resolve_ack_topic(topic)
registry.resolve_legacy_topic(topic)
```

## Non-goals for 1.0

No mutation, live reload, network transport, graph relations, authorization or
secret management.
MD

python3 - <<'PY'
from pathlib import Path

path = Path("core-engine/src/domoticsai_core/registry/__init__.py")
text = path.read_text(encoding="utf-8")
line = "from .service import RegistryService, RegistryTopics"
if line not in text:
    text = text.rstrip() + "\n\n# Public Registry Service API (ADR-019)\n" + line + "\n"
    path.write_text(text, encoding="utf-8")
PY

echo "Sprint 12.9 installato."
echo "Nessuna modifica a app.py, command_manager.py, Android, Gateway o Registry YAML."
