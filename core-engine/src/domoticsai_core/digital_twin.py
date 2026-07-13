from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import threading
from typing import Any, Callable

from .event_store import EventStore
from .models import DigitalTwin, TwinValue
from .topic_mapper import map_state_topic


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DigitalTwinStore:
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store
        self._lock = threading.RLock()
        self._listeners: list[Callable[[dict[str, Any]], None]] = []

        restored_domains = self._event_store.load_twin_state()
        restored_at = self._latest_timestamp(restored_domains)

        self._twin = DigitalTwin(
            updated_at=restored_at or utc_now_iso(),
            domains=restored_domains,
        )

    def add_listener(self, listener: Callable[[dict[str, Any]], None]) -> None:
        with self._lock:
            self._listeners.append(listener)

    def update_from_mqtt(self, topic: str, payload_text: str) -> bool:
        address = map_state_topic(topic)
        if address is None:
            return False

        received_at = utc_now_iso()
        parsed = self._parse_payload(payload_text)

        twin_value = TwinValue(
            value=parsed["value"],
            unit=parsed.get("unit"),
            quality=parsed.get("quality", "unknown"),
            source=parsed.get("source", "mqtt"),
            timestamp=parsed.get("ts", received_at),
            topic=topic,
        )

        with self._lock:
            domain = self._twin.domains.setdefault(address.domain, {})
            domain[address.entity] = twin_value
            self._twin.updated_at = received_at

        self._event_store.append(
            received_at=received_at,
            topic=topic,
            domain=address.domain,
            entity=address.entity,
            payload=payload_text,
            parsed_value=twin_value.value,
            quality=twin_value.quality,
        )

        self._event_store.upsert_twin_value(
            domain=address.domain,
            entity=address.entity,
            value=twin_value,
        )

        event = {
            "type": "twin_update",
            "domain": address.domain,
            "entity": address.entity,
            "data": twin_value.model_dump(),
            "updatedAt": received_at,
        }

        with self._lock:
            listeners = list(self._listeners)

        for listener in listeners:
            try:
                listener(event)
            except Exception:
                pass

        return True

    def snapshot(self) -> DigitalTwin:
        with self._lock:
            return self._twin.model_copy(deep=True)

    def domain(self, domain_name: str) -> dict[str, TwinValue] | None:
        with self._lock:
            domain = self._twin.domains.get(domain_name)
            return deepcopy(domain) if domain is not None else None

    def reset(self) -> None:
        with self._lock:
            self._twin = DigitalTwin()
        self._event_store.clear_twin_state()

    @staticmethod
    def _parse_payload(payload_text: str) -> dict[str, Any]:
        stripped = payload_text.strip()

        if stripped.startswith("{"):
            try:
                obj = json.loads(stripped)
                if "value" in obj:
                    return obj
            except json.JSONDecodeError:
                pass

        try:
            number = float(stripped)
            return {"value": number}
        except ValueError:
            return {"value": payload_text}

    @staticmethod
    def _latest_timestamp(
        domains: dict[str, dict[str, TwinValue]],
    ) -> str | None:
        timestamps = [
            value.timestamp
            for entities in domains.values()
            for value in entities.values()
            if value.timestamp
        ]
        return max(timestamps) if timestamps else None
