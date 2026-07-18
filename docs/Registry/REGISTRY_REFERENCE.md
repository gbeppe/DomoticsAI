# Digital Twin Registry Reference

- **Status:** Active
- **Owner:** Registry
- **Version:** 1.0
- **Authoritative data:** `config/registry/digital-twin-registry.yaml`

## Root sections

### `registry`

Registry metadata: `name`, `version`, `generated`, `interface_version`.

### `brokers`

Named broker endpoints referenced by bindings. Credentials and secrets must be
provided outside the Registry.

### Domain trees

Every non-reserved root section represents a domain tree. A node containing an
`id` is treated as an entity-property declaration.

## Entity fields

| Field | Meaning |
|---|---|
| `id` | Stable fully qualified logical identifier |
| `domain` | Functional domain |
| `entity_id` | Logical entity name |
| `property` | Property represented by this declaration |
| `description` | Human-readable meaning |
| `status` | Lifecycle and migration status |
| `source_type` | Nature of the value or actuator |
| `location` | Stable location metadata |
| `display` | Shared presentation metadata |
| `group` | Logical grouping |
| `state_update` | How initial and ongoing state is obtained |
| `behavior` | Confirmation and optimistic-update behavior |
| `capabilities` | Read, write and history capabilities |
| `interface` | Public DomoticsAI topics and value schema |
| `mqtt` | QoS and retain behavior |
| `transform` | Logical-to-physical payload mapping |
| `legacy` | Physical or pre-existing system bindings |

## Interface section

`state_topic`, `command_topic`, `ack_topic` and `schema.type` define the public
logical interface. A writable capability requires a valid command route; a
readable capability normally requires a valid state route.

## MQTT section

`qos`, `retain_state` and `retain_command` define delivery behavior. Commands
should normally not be retained.

## Legacy binding

Named endpoints such as `source` and `confirmation` reference a broker name and
a physical topic. Additional fields may define device identity, initial-value
strategy and confirmation timeout.

## Transformation rules

`transform.command` maps canonical command values to physical payloads.
`transform.state` maps physical payloads to canonical values. Mappings must be
deterministic; unknown values must not be silently guessed.
