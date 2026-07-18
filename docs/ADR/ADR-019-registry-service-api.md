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
