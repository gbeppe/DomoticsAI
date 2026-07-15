from copy import deepcopy
from datetime import datetime, timezone
import inspect
import json
import threading

from .energy_derived import (
    calculate_energy_derived,
    read_energy_raw,
)
from .lights_derived import calculate_lights_derived
from .knowledge.knowledge_engine import (
    HouseKnowledgeEngine,
)
from .knowledge.scene_state import (
    SceneStateTracker,
)
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
        self._knowledge_engine = HouseKnowledgeEngine()
        self._scene_state_tracker = SceneStateTracker()
        self._restored_entities = 0

        self._restore_from_database()
        self._recalculate_energy_derived(
            notify=False,
            persist=True,
        )
        self._recalculate_lights_derived(
            notify=False,
            persist=True,
        )
        self._recalculate_knowledge(
            notify=False,
            persist=True,
        )

    @property
    def restored_entities(self):
        return self._restored_entities

    def _restore_from_database(self):
        restored = self._event_store.load_twin_state()

        if not restored:
            return

        newest_timestamp = None
        entity_count = 0

        with self._lock:
            for domain_name, entities in restored.items():
                target = self._twin.domains.setdefault(
                    domain_name,
                    {},
                )

                for entity_name, value in entities.items():
                    target[entity_name] = value
                    entity_count += 1

                    if (
                        newest_timestamp is None
                        or value.timestamp > newest_timestamp
                    ):
                        newest_timestamp = value.timestamp

            if newest_timestamp is not None:
                self._twin.updated_at = newest_timestamp

            self._restored_entities = entity_count

    def _persist_twin_value(
        self,
        *,
        domain: str,
        entity: str,
        value: TwinValue,
        updated_at: str,
    ):
        method = self._event_store.upsert_twin_value
        parameters = inspect.signature(method).parameters

        kwargs = {
            "domain": domain,
            "entity": entity,
            "value": value,
        }

        if "updated_at" in parameters:
            kwargs["updated_at"] = updated_at

        method(**kwargs)

    def handle_scene_command_event(
        self,
        event: dict,
    ) -> None:
        self._scene_state_tracker.handle_command_event(
            event
        )

        self._recalculate_knowledge(
            notify=True,
            persist=True,
        )

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
            self._twin.domains.setdefault(
                address.domain,
                {},
            )[address.entity] = value

            self._twin.updated_at = received_at
            listeners = list(self._listeners)

        self._persist_twin_value(
            domain=address.domain,
            entity=address.entity,
            value=value,
            updated_at=received_at,
        )

        self._event_store.append(
            received_at=received_at,
            topic=topic,
            domain=address.domain,
            entity=address.entity,
            payload=payload_text,
            parsed_value=value.value,
            quality=value.quality,
        )

        if address.domain == "energy":
            self._recalculate_energy_derived(
                notify=True,
                persist=True,
            )

        if address.domain == "lights":
            self._recalculate_lights_derived(
                notify=True,
                persist=True,
            )

        if address.domain in {
            "energy",
            "lights",
        }:
            self._recalculate_knowledge(
                notify=True,
                persist=True,
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

    def _recalculate_knowledge(
        self,
        *,
        notify: bool,
        persist: bool,
    ):
        with self._lock:
            source_domains = {
                name: dict(values)
                for name, values
                in self._twin.domains.items()
                if name != "knowledge"
            }

        facts = self._knowledge_engine.evaluate(
            source_domains,
            scene_state=(
                self._scene_state_tracker.snapshot()
            ),
        )

        if not facts:
            return

        self._store_derived_domain(
            domain_name="knowledge",
            values=facts,
            notify=notify,
            persist=persist,
        )

    def _recalculate_energy_derived(
        self,
        *,
        notify: bool,
        persist: bool,
    ):
        with self._lock:
            energy = self._twin.domains.get("energy")

            if not energy:
                return

            derived_values = calculate_energy_derived(
                read_energy_raw(energy)
            )

        self._store_derived_domain(
            domain_name="energy_derived",
            values=derived_values,
            notify=notify,
            persist=persist,
        )

    def _recalculate_lights_derived(
        self,
        *,
        notify: bool,
        persist: bool,
    ):
        with self._lock:
            lights = self._twin.domains.get("lights")

            if not lights:
                return

            derived_values = calculate_lights_derived(lights)

        self._store_derived_domain(
            domain_name="lights_derived",
            values=derived_values,
            notify=notify,
            persist=persist,
        )

    def _store_derived_domain(
        self,
        *,
        domain_name: str,
        values: dict,
        notify: bool,
        persist: bool,
    ):
        timestamp = utc_now_iso()

        with self._lock:
            target = self._twin.domains.setdefault(
                domain_name,
                {},
            )
            listeners = list(self._listeners)

        for entity, raw_value in values.items():
            twin_value = TwinValue(
                value=raw_value,
                unit=self._derived_unit(entity),
                quality="calculated",
                source="core-engine",
                timestamp=timestamp,
                topic=f"internal://{domain_name}/{entity}",
            )

            with self._lock:
                target[entity] = twin_value
                self._twin.updated_at = timestamp

            if persist:
                self._persist_twin_value(
                    domain=domain_name,
                    entity=entity,
                    value=twin_value,
                    updated_at=timestamp,
                )

            if notify:
                event = {
                    "type": "twin_update",
                    "domain": domain_name,
                    "entity": entity,
                    "data": twin_value.model_dump(),
                    "updatedAt": timestamp,
                }

                for listener in listeners:
                    try:
                        listener(event)
                    except Exception:
                        pass

    @staticmethod
    def _derived_unit(entity):
        if entity.endswith("_w"):
            return "W"

        if entity.endswith("_pct"):
            return "%"

        return None

    def snapshot(self):
        with self._lock:
            return self._twin.model_copy(deep=True)

    def domain(self, name):
        with self._lock:
            value = self._twin.domains.get(name)

            return (
                deepcopy(value)
                if value is not None
                else None
            )

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
