# ADR-018 — Digital Twin Registry as Single Source of Truth

- **Status:** Accepted
- **Date:** 2026-07-17
- **Owners:** Architecture, Core Engine, Gateway
- **Decision scope:** Entire DomoticsAI ecosystem

## Context

DomoticsAI contains several consumers and adapters: Android application, AI layer,
Core Engine, Gateway, MQTT brokers, Node-RED flows and physical devices.

Entity identifiers, capabilities, public MQTT interfaces and legacy physical
bindings must not be duplicated independently across those components. Duplication
would allow incompatible names, topics, payload mappings and device status to
diverge over time.

The repository contains the machine-readable registry:

`config/registry/digital-twin-registry.yaml`

The Core Engine already loads this file through its Registry SDK and exposes
registry information in its health state.

## Decision

`config/registry/digital-twin-registry.yaml` is the authoritative, executable
declaration of the DomoticsAI Digital Twin.

It is the single source of truth for:

- logical entity identifiers;
- domains, entities and properties;
- entity lifecycle status;
- capabilities;
- public interface topics;
- MQTT delivery properties;
- payload transformations;
- broker references;
- legacy physical bindings;
- confirmation behavior and timeouts;
- presentation metadata intentionally shared by consumers.

Normative prose documents define the registry's concepts and rules, but they
must not duplicate complete entity or topic inventories.

## Responsibility boundaries

### Core Engine

The Core Engine consumes logical identities and capabilities from the Registry.
It must not embed physical device addresses or legacy topic mappings in domain
logic.

### Gateway

The Gateway consumes interface and legacy bindings from the Registry and
translates between the logical DomoticsAI interface and physical protocols.

### Android and AI

Android and AI consume logical identities, capabilities and supported operations.
They must not depend directly on legacy device bindings.

### Node-RED and physical systems

Legacy systems remain integration targets during migration. Their details belong
in registry bindings and Gateway adapters, not in logical consumers.

## Versioning

- `registry.version` versions registry content.
- `registry.interface_version` versions the public logical interface.
- Backward-incompatible public-interface changes require an interface-version
  increment and a migration plan.
- Entity additions that preserve the interface contract normally require only a
  registry content-version increment.
- Deprecated entities remain explicitly marked until references and migration
  obligations have been verified.

## Validation

Every change to the Registry must pass:

1. YAML parsing;
2. the repository Registry validator;
3. Registry SDK loading tests;
4. uniqueness checks for identifiers and public topics;
5. applicable Core Engine, Gateway and contract tests.

## Consequences

### Positive

- one authoritative declaration;
- reduced configuration drift;
- deterministic discovery and routing;
- reusable validation and tooling;
- safer migration away from legacy bindings;
- future dynamic UI and AI discovery become possible.

### Costs and constraints

- Registry changes become architectural changes and require review;
- consumers must use the Registry SDK or a controlled projection;
- secrets must not be stored in the Registry;
- validation and compatibility rules must be maintained.

## Related documents

- `docs/Architecture/CORE_ENGINE_CONTRACT.md`
- `docs/Registry/REGISTRY_MODEL.md`
- `docs/Registry/REGISTRY_REFERENCE.md`
- `docs/Registry/REGISTRY_EVOLUTION.md`
- `config/registry/README.md`
