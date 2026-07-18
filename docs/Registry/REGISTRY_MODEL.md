# Digital Twin Registry Model

- **Status:** Active
- **Owner:** Architecture / Registry
- **Version:** 1.0
- **Related ADR:** ADR-018

## Purpose

The Digital Twin Registry is the declarative heart of DomoticsAI. It separates
the stable logical model of the house from physical protocols, broker addresses,
legacy topics and device-specific payloads.

## Core concepts

### Logical identity

Each property exposed by the ecosystem has a stable logical identity:

`<domain>.<entity_id>.<property>`

Logical identity is independent of the current hardware and transport.

### Domain, entity and property

A domain groups entities by functional meaning. An entity represents a logical
thing; a property represents one observable or controllable aspect of that thing.

### Capability

Capabilities declare whether a property can be read, written or historized.
Consumers use capabilities instead of inferring behavior from topic names.

### Public interface

The interface section defines the stable DomoticsAI-facing contract. Logical
consumers use this interface and must not depend on legacy physical topics.

### Physical binding

The legacy or adapter binding describes how the current physical system exposes
or accepts data. This layer may change without changing logical identity.

### Transformation

Transformations translate between canonical logical values and protocol-specific
payloads.

### Lifecycle status

Status describes migration and availability state. A deprecated entity is not
silently deleted. Removal requires reference checks and a documented migration
decision.

## Architectural invariants

1. Logical identities are stable and unique.
2. Public interface topics are unique.
3. Domain logic never embeds physical addresses or legacy topics.
4. Physical bindings never redefine logical meaning.
5. Secrets are external to the Registry.
6. Changes are validated before consumers are restarted.
7. A breaking public-interface change increments `interface_version`.
8. The Registry remains usable without a mandatory cloud service.
