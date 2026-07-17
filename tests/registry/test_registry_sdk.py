#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core_engine.registry import RegistryError, load_registry

def main() -> int:
    try:
        registry = load_registry(PROJECT_ROOT / "config/registry/digital-twin-registry.yaml")
    except RegistryError as exc:
        print(f"REGISTRY SDK FAILED: {exc}", file=sys.stderr)
        return 1

    if len(registry) == 0:
        print("REGISTRY SDK FAILED: nessuna entità", file=sys.stderr)
        return 1

    for entity in registry:
        if registry.require(entity.id) is not entity:
            print(f"REGISTRY SDK FAILED: indice ID incoerente per {entity.id}", file=sys.stderr)
            return 1
        if entity.state_topic and registry.by_state_topic(entity.state_topic) is not entity:
            print(f"REGISTRY SDK FAILED: state topic incoerente per {entity.id}", file=sys.stderr)
            return 1
        if entity.command_topic and registry.by_command_topic(entity.command_topic) is not entity:
            print(f"REGISTRY SDK FAILED: command topic incoerente per {entity.id}", file=sys.stderr)
            return 1
        if entity.ack_topic and registry.by_ack_topic(entity.ack_topic) is not entity:
            print(f"REGISTRY SDK FAILED: ack topic incoerente per {entity.id}", file=sys.stderr)
            return 1

    print(json.dumps(registry.summary(), ensure_ascii=False, indent=2))
    print("REGISTRY SDK OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
