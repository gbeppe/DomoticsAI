from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

_EMPTY = MappingProxyType({})

@dataclass(frozen=True)
class Broker:
    name: str
    data: Mapping[str, Any]

    @property
    def host(self) -> str | None:
        value = self.data.get("host")
        return str(value) if value is not None else None

    @property
    def port(self) -> int | None:
        value = self.data.get("port")
        return value if isinstance(value, int) else None

@dataclass(frozen=True)
class Entity:
    path: str
    data: Mapping[str, Any]

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def domain(self) -> str:
        return str(self.data["domain"])

    @property
    def entity_id(self) -> str:
        return str(self.data["entity_id"])

    @property
    def attribute(self) -> str:
        return str(self.data["property"])

    @property
    def status(self) -> str | None:
        value = self.data.get("status")
        return str(value) if value is not None else None

    def _mapping(self, key: str) -> Mapping[str, Any]:
        value = self.data.get(key)
        return value if isinstance(value, Mapping) else _EMPTY

    @property
    def capabilities(self) -> Mapping[str, Any]:
        return self._mapping("capabilities")

    @property
    def interface(self) -> Mapping[str, Any]:
        return self._mapping("interface")

    @property
    def mqtt(self) -> Mapping[str, Any]:
        return self._mapping("mqtt")

    @property
    def behavior(self) -> Mapping[str, Any]:
        return self._mapping("behavior")

    @property
    def legacy(self) -> Mapping[str, Any]:
        return self._mapping("legacy")

    @property
    def transform(self) -> Mapping[str, Any]:
        return self._mapping("transform")

    @property
    def readable(self) -> bool:
        return self.capabilities.get("readable") is True

    @property
    def writable(self) -> bool:
        return self.capabilities.get("writable") is True

    @property
    def historized(self) -> bool:
        return self.capabilities.get("historized") is True

    @property
    def state_topic(self) -> str | None:
        value = self.interface.get("state_topic")
        return str(value) if value else None

    @property
    def command_topic(self) -> str | None:
        value = self.interface.get("command_topic")
        return str(value) if value else None

    @property
    def ack_topic(self) -> str | None:
        value = self.interface.get("ack_topic")
        return str(value) if value else None
