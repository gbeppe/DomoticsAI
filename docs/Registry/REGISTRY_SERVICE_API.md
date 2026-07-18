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
