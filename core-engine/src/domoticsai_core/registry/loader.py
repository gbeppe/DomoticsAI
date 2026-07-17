from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any
import yaml

from .constants import DEFAULT_REGISTRY_PATH
from .exceptions import RegistryFileError

def deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): deep_freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(deep_freeze(v) for v in value)
    if isinstance(value, tuple):
        return tuple(deep_freeze(v) for v in value)
    return value

def load_yaml_document(path: str | Path = DEFAULT_REGISTRY_PATH):
    registry_path = Path(path)
    try:
        raw = registry_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RegistryFileError(f"Impossibile leggere il registry '{registry_path}': {exc}") from exc

    try:
        document = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise RegistryFileError(f"YAML non valido nel registry '{registry_path}': {exc}") from exc

    if not isinstance(document, Mapping):
        raise RegistryFileError("La radice YAML del registry deve essere una mappa.")

    return deep_freeze(document), registry_path
