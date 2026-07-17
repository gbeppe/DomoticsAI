from pathlib import Path

DEFAULT_REGISTRY_PATH = Path("config/registry/digital-twin-registry.yaml")
RESERVED_ROOT_KEYS = {"registry", "brokers"}
LEGACY_ENDPOINT_KEYS = ("source", "confirmation", "command")
