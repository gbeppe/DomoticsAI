#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CORE_ENGINE_ROOT = REPOSITORY_ROOT / "core-engine"
SOURCE_ROOT = CORE_ENGINE_ROOT / "src"

if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from domoticsai_core.registry import RegistryError, load_registry


def main() -> int:
    try:
        registry = load_registry(
            REPOSITORY_ROOT
            / "config"
            / "registry"
            / "digital-twin-registry.yaml"
        )
    except RegistryError as exc:
        print(
            f"REGISTRY SDK FAILED: {exc}",
            file=sys.stderr,
        )
        return 1

    if len(registry) == 0:
        print(
            "REGISTRY SDK FAILED: nessuna entità",
            file=sys.stderr,
        )
        return 1

    for entity in registry:
        if registry.require(entity.id) is not entity:
            print(
                f"REGISTRY SDK FAILED: "
                f"indice ID incoerente per {entity.id}",
                file=sys.stderr,
            )
            return 1

        if (
            entity.state_topic
            and registry.by_state_topic(entity.state_topic) is not entity
        ):
            print(
                f"REGISTRY SDK FAILED: "
                f"state topic incoerente per {entity.id}",
                file=sys.stderr,
            )
            return 1

        if (
            entity.command_topic
            and registry.by_command_topic(entity.command_topic) is not entity
        ):
            print(
                f"REGISTRY SDK FAILED: "
                f"command topic incoerente per {entity.id}",
                file=sys.stderr,
            )
            return 1

        if (
            entity.ack_topic
            and registry.by_ack_topic(entity.ack_topic) is not entity
        ):
            print(
                f"REGISTRY SDK FAILED: "
                f"ack topic incoerente per {entity.id}",
                file=sys.stderr,
            )
            return 1

    print(
        json.dumps(
            registry.summary(),
            ensure_ascii=False,
            indent=2,
        )
    )
    print("REGISTRY SDK OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def load_test_registry():
    return load_registry(
        REPOSITORY_ROOT
        / "config"
        / "registry"
        / "digital-twin-registry.yaml"
    )


def test_registry_resolves_entity_by_id():
    registry = load_test_registry()

    entity = registry.by_entity_id(
        "lights.living.power"
    )

    assert entity is not None
    assert entity.id == "lights.living.power"


def test_registry_returns_none_for_unknown_entity_id():
    registry = load_test_registry()

    entity = registry.by_entity_id(
        "lights.unknown.device"
    )

    assert entity is None
