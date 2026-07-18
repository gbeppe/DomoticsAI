# Digital Twin Registry Evolution

- **Status:** Active
- **Owner:** Registry / Architecture
- **Version:** 1.0
- **Related ADR:** ADR-018

## Change workflow

1. Identify the logical concept before the physical implementation.
2. Choose a stable `domain.entity_id.property` identity.
3. Define canonical type and capabilities.
4. Define the public interface.
5. Add physical or legacy bindings.
6. Add deterministic transformations.
7. Select lifecycle status.
8. Increment the appropriate version.
9. Run validation and tests.
10. Review dependent documentation and consumers.
11. Commit Registry, tests and documentation together.

## Compatibility

A physical binding change that preserves logical meaning must not change the
logical ID. A logical ID or public-topic change is a compatibility event and may
require an ADR, migration period and `interface_version` increment.

## Deprecation

Before removing a deprecated entity, search Core Engine, Gateway, Android,
Node-RED flows, MQTT documentation, automations and AI configurations. Keep the
entry until migration obligations are closed.

## Secrets

Do not commit passwords, tokens or private keys. Keep secrets in environment
variables or files excluded from version control.

## Required checks

```bash
python3 tools/validate_registry.py \
  config/registry/digital-twin-registry.yaml

python3 core-engine/tests/registry/test_registry_sdk.py
```

Run the complete relevant test suites in the environment where project
dependencies are installed.
