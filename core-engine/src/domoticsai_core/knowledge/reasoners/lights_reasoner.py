from __future__ import annotations

from typing import Any

from ...models import TwinValue
from ..facts import KnowledgeFact


def _value(
    domain: dict[str, TwinValue],
    entity: str,
    default: Any = None,
) -> Any:
    item = domain.get(entity)

    if item is None:
        return default

    return item.value


def _boolean(
    domain: dict[str, TwinValue],
    entity: str,
    default: bool = False,
) -> bool:
    value = _value(
        domain,
        entity,
        default,
    )

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        return (
            value.strip().lower()
            in {
                "true",
                "1",
                "yes",
                "on",
            }
        )

    return default


def _integer(
    domain: dict[str, TwinValue],
    entity: str,
    default: int = 0,
) -> int:
    value = _value(
        domain,
        entity,
        default,
    )

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, (int, float)):
        return int(value)

    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return default

    return default


class LightsReasoner:
    """
    Interpreta lights e lights_derived.

    I relè della piscina restano separati dalle luci:
    pompa e skimmer non contribuiscono a lights.count_on.
    """

    category = "lights"

    def reason(
        self,
        domains: dict[
            str,
            dict[str, TwinValue],
        ],
    ) -> list[KnowledgeFact]:
        lights = domains.get(
            "lights",
            {},
        )

        derived = domains.get(
            "lights_derived",
            {},
        )

        if not lights and not derived:
            return []

        lights_on_total = _integer(
            derived,
            "lights_on_total",
        )

        relays_on_total = _integer(
            derived,
            "relays_on_total",
        )

        unknown_total = _integer(
            derived,
            "unknown_total",
        )

        internal_on = _integer(
            derived,
            "internal_on",
        )

        internal_total = _integer(
            derived,
            "internal_total",
        )

        external_on = _integer(
            derived,
            "external_on",
        )

        external_total = _integer(
            derived,
            "external_total",
        )

        pool_on = _integer(
            derived,
            "pool_on",
        )

        pool_total = _integer(
            derived,
            "pool_total",
        )

        any_internal_on = _boolean(
            derived,
            "any_internal_on",
        )

        any_external_on = _boolean(
            derived,
            "any_external_on",
        )

        all_available = _boolean(
            derived,
            "all_available",
        )

        pool_lights_on = self._pool_lights_on(
            lights
        )

        facts = [
            KnowledgeFact(
                name="lights.any_on",
                category=self.category,
                value=lights_on_total > 0,
                reason=[
                    (
                        "lights_derived."
                        "lights_on_total="
                        f"{lights_on_total}"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.all_off",
                category=self.category,
                value=(
                    lights_on_total == 0
                    and unknown_total == 0
                ),
                reason=[
                    (
                        "lights_on_total="
                        f"{lights_on_total}"
                    ),
                    (
                        "unknown_total="
                        f"{unknown_total}"
                    ),
                ],
            ),
            KnowledgeFact(
                name="lights.count_on",
                category=self.category,
                value=lights_on_total,
                reason=[
                    (
                        "lights_derived."
                        "lights_on_total"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.relays_on",
                category=self.category,
                value=relays_on_total,
                reason=[
                    (
                        "lights_derived."
                        "relays_on_total"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.unknown_count",
                category=self.category,
                value=unknown_total,
                reason=[
                    (
                        "lights_derived."
                        "unknown_total"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.all_available",
                category=self.category,
                value=all_available,
                reason=[
                    (
                        "lights_derived."
                        "all_available="
                        f"{all_available}"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.internal_any_on",
                category=self.category,
                value=any_internal_on,
                reason=[
                    (
                        "lights_derived."
                        "internal_on="
                        f"{internal_on}"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.external_any_on",
                category=self.category,
                value=any_external_on,
                reason=[
                    (
                        "lights_derived."
                        "external_on="
                        f"{external_on}"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.pool_lighting_any_on",
                category=self.category,
                value=pool_lights_on > 0,
                reason=[
                    (
                        "observed pool light "
                        "devices on="
                        f"{pool_lights_on}"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.internal_state",
                category=self.category,
                value=self._area_state(
                    internal_on,
                    internal_total,
                    unknown_total,
                ),
                reason=[
                    (
                        "internal_on="
                        f"{internal_on}"
                    ),
                    (
                        "internal_total="
                        f"{internal_total}"
                    ),
                ],
            ),
            KnowledgeFact(
                name="lights.external_state",
                category=self.category,
                value=self._area_state(
                    external_on,
                    external_total,
                    unknown_total,
                ),
                reason=[
                    (
                        "external_on="
                        f"{external_on}"
                    ),
                    (
                        "external_total="
                        f"{external_total}"
                    ),
                ],
            ),
            KnowledgeFact(
                name="lights.pool_lighting_state",
                category=self.category,
                value=self._pool_lighting_state(
                    lights
                ),
                reason=[
                    (
                        "observed pool/luciPiscina "
                        "and pool/luciPedanaPiscina"
                    )
                ],
            ),
            KnowledgeFact(
                name="lights.area_summary",
                category=self.category,
                value={
                    "internal": {
                        "on": internal_on,
                        "total": internal_total,
                    },
                    "external": {
                        "on": external_on,
                        "total": external_total,
                    },
                    "pool_all_devices": {
                        "on": pool_on,
                        "total": pool_total,
                    },
                    "pool_lights_on": (
                        pool_lights_on
                    ),
                },
                reason=[
                    "lights_derived area counters"
                ],
            ),
        ]

        return facts

    @staticmethod
    def _normalized_state(
        item: TwinValue | None,
    ) -> str:
        if item is None:
            return "UNKNOWN"

        value = item.value

        if isinstance(value, bool):
            return (
                "ON"
                if value
                else "OFF"
            )

        if isinstance(value, (int, float)):
            return (
                "ON"
                if value != 0
                else "OFF"
            )

        text = str(value).strip().upper()

        if text in {
            "ON",
            "1",
            "TRUE",
        }:
            return "ON"

        if text in {
            "OFF",
            "0",
            "FALSE",
        }:
            return "OFF"

        return "UNKNOWN"

    def _pool_lights_on(
        self,
        lights: dict[str, TwinValue],
    ) -> int:
        pool_light_ids = (
            "pool/luciPiscina",
            "pool/luciPedanaPiscina",
        )

        return sum(
            1
            for entity_id in pool_light_ids
            if self._normalized_state(
                lights.get(entity_id)
            )
            == "ON"
        )

    def _pool_lighting_state(
        self,
        lights: dict[str, TwinValue],
    ) -> str:
        states = [
            self._normalized_state(
                lights.get(entity_id)
            )
            for entity_id in (
                "pool/luciPiscina",
                "pool/luciPedanaPiscina",
            )
        ]

        if "UNKNOWN" in states:
            return "unknown"

        on_count = states.count("ON")

        if on_count == 0:
            return "off"

        if on_count == len(states):
            return "all_on"

        return "partial"

    @staticmethod
    def _area_state(
        on_count: int,
        total_count: int,
        unknown_total: int,
    ) -> str:
        if total_count <= 0:
            return "unavailable"

        if unknown_total > 0:
            return "partially_unknown"

        if on_count == 0:
            return "all_off"

        if on_count == total_count:
            return "all_on"

        return "partial"
