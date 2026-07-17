from __future__ import annotations
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

from .constants import DEFAULT_REGISTRY_PATH, LEGACY_ENDPOINT_KEYS, RESERVED_ROOT_KEYS
from .exceptions import RegistryLookupError, RegistryValidationError
from .loader import load_yaml_document
from .models import Broker, Entity

class Registry:
    def __init__(self, document: Mapping[str, Any], source_path: Path | None = None) -> None:
        self._document = document
        self._source_path = source_path

        metadata = document.get("registry", {})
        brokers_data = document.get("brokers", {})
        if not isinstance(metadata, Mapping):
            raise RegistryValidationError("La sezione 'registry' non è una mappa.")
        if not isinstance(brokers_data, Mapping):
            raise RegistryValidationError("La sezione 'brokers' non è una mappa.")

        self._metadata = metadata
        self._brokers = self._build_brokers(brokers_data)
        self._entities = tuple(self._collect_entities())
        if not self._entities:
            raise RegistryValidationError("Il registry non contiene entità.")

        self._by_id = {}
        self._by_state_topic = {}
        self._by_command_topic = {}
        self._by_ack_topic = {}
        self._by_legacy_topic = {}
        self._by_domain = {}
        self._build_indexes()

    @classmethod
    def load(cls, path: str | Path = DEFAULT_REGISTRY_PATH) -> "Registry":
        document, source_path = load_yaml_document(path)
        return cls(document, source_path)

    @property
    def source_path(self):
        return self._source_path

    @property
    def metadata(self):
        return self._metadata

    @property
    def version(self):
        value = self._metadata.get("version")
        return str(value) if value is not None else None

    @property
    def interface_version(self):
        value = self._metadata.get("interface_version")
        return str(value) if value is not None else None

    @property
    def entities(self):
        return self._entities

    @property
    def brokers(self):
        return MappingProxyType(self._brokers)

    def __len__(self):
        return len(self._entities)

    def __iter__(self) -> Iterator[Entity]:
        return iter(self._entities)

    def get(self, entity_id: str):
        return self._by_id.get(entity_id)

    def require(self, entity_id: str) -> Entity:
        entity = self.get(entity_id)
        if entity is None:
            raise RegistryLookupError(f"Entità non trovata: {entity_id}")
        return entity

    def broker(self, name: str) -> Broker:
        broker = self._brokers.get(name)
        if broker is None:
            raise RegistryLookupError(f"Broker non trovato: {name}")
        return broker

    def by_state_topic(self, topic: str):
        return self._by_state_topic.get(topic)

    def by_command_topic(self, topic: str):
        return self._by_command_topic.get(topic)

    def by_ack_topic(self, topic: str):
        return self._by_ack_topic.get(topic)

    def by_legacy_topic(self, topic: str):
        return tuple(self._by_legacy_topic.get(topic, ()))

    def by_domain(self, domain: str):
        return tuple(self._by_domain.get(domain, ()))

    def readable_entities(self):
        return tuple(e for e in self._entities if e.readable)

    def writable_entities(self):
        return tuple(e for e in self._entities if e.writable)

    def historized_entities(self):
        return tuple(e for e in self._entities if e.historized)

    def active_entities(self):
        return tuple(e for e in self._entities if e.status == "active")

    def summary(self):
        return {
            "name": self._metadata.get("name"),
            "version": self.version,
            "interface_version": self.interface_version,
            "source_path": str(self._source_path) if self._source_path else None,
            "brokers": len(self._brokers),
            "entities": len(self._entities),
            "domains": sorted(self._by_domain),
            "readable": len(self.readable_entities()),
            "writable": len(self.writable_entities()),
            "historized": len(self.historized_entities()),
            "active": len(self.active_entities()),
        }

    def _build_brokers(self, data):
        result = {}
        for name, broker_data in data.items():
            if not isinstance(broker_data, Mapping):
                raise RegistryValidationError(f"Broker '{name}' non valido.")
            result[str(name)] = Broker(str(name), broker_data)
        return result

    def _collect_entities(self) -> Iterable[Entity]:
        for root_key, node in self._document.items():
            if root_key in RESERVED_ROOT_KEYS:
                continue
            if isinstance(node, Mapping):
                yield from self._walk(str(root_key), node)

    def _walk(self, path: str, node: Mapping[str, Any]):
        if "id" in node:
            required = ("id", "domain", "entity_id", "property")
            missing = [f for f in required if not isinstance(node.get(f), str) or not str(node.get(f)).strip()]
            if missing:
                raise RegistryValidationError(
                    f"Entità non valida in '{path}'; campi mancanti: {', '.join(missing)}"
                )
            yield Entity(path, node)
            return

        for key, child in node.items():
            if isinstance(child, Mapping):
                yield from self._walk(f"{path}.{key}", child)

    def _build_indexes(self):
        for entity in self._entities:
            self._insert_unique(self._by_id, entity.id, entity, "entity id")
            self._insert_unique(self._by_state_topic, entity.state_topic, entity, "state topic")
            self._insert_unique(self._by_command_topic, entity.command_topic, entity, "command topic")
            self._insert_unique(self._by_ack_topic, entity.ack_topic, entity, "ack topic")
            self._by_domain.setdefault(entity.domain, []).append(entity)

            for endpoint_name in LEGACY_ENDPOINT_KEYS:
                endpoint = entity.legacy.get(endpoint_name)
                if isinstance(endpoint, Mapping):
                    topic = endpoint.get("topic")
                    if isinstance(topic, str) and topic:
                        self._by_legacy_topic.setdefault(topic, []).append(entity)

        for values in self._by_domain.values():
            values.sort(key=lambda item: item.id)

    @staticmethod
    def _insert_unique(index, key, entity, label):
        if not key:
            return
        existing = index.get(key)
        if existing is not None:
            raise RegistryValidationError(
                f"{label} duplicato '{key}' per '{existing.id}' e '{entity.id}'."
            )
        index[key] = entity

def load_registry(path: str | Path = DEFAULT_REGISTRY_PATH) -> Registry:
    return Registry.load(path)
