from copy import deepcopy
from datetime import datetime, timezone
import json
import threading
from .models import DigitalTwin, TwinValue
from .topic_mapper import map_state_topic

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

class DigitalTwinStore:
    def __init__(self, event_store):
        self._event_store = event_store
        self._lock = threading.RLock()
        self._twin = DigitalTwin()
        self._listeners = []

    def add_listener(self, listener):
        with self._lock:
            self._listeners.append(listener)

    def update_from_mqtt(self, topic, payload_text):
        address = map_state_topic(topic)
        if address is None:
            return False

        received_at = utc_now_iso()
        parsed = self._parse_payload(payload_text)

        value = TwinValue(
            value=parsed["value"],
            unit=parsed.get("unit"),
            quality=parsed.get("quality", "unknown"),
            source=parsed.get("source", "mqtt"),
            timestamp=parsed.get("ts", received_at),
            topic=topic,
        )

        with self._lock:
            self._twin.domains.setdefault(address.domain, {})[address.entity] = value
            self._twin.updated_at = received_at
            listeners = list(self._listeners)

        self._event_store.append(
            received_at=received_at,
            topic=topic,
            domain=address.domain,
            entity=address.entity,
            payload=payload_text,
            parsed_value=value.value,
            quality=value.quality,
        )

        event = {
            "type": "twin_update",
            "domain": address.domain,
            "entity": address.entity,
            "data": value.model_dump(),
            "updatedAt": received_at,
        }
        for listener in listeners:
            try:
                listener(event)
            except Exception:
                pass
        return True

    def snapshot(self):
        with self._lock:
            return self._twin.model_copy(deep=True)

    def domain(self, name):
        with self._lock:
            value = self._twin.domains.get(name)
            return deepcopy(value) if value is not None else None

    @staticmethod
    def _parse_payload(payload_text):
        text = payload_text.strip()
        if text.startswith("{"):
            try:
                obj = json.loads(text)
                if "value" in obj:
                    return obj
            except json.JSONDecodeError:
                pass
        try:
            return {"value": float(text)}
        except ValueError:
            return {"value": payload_text}
