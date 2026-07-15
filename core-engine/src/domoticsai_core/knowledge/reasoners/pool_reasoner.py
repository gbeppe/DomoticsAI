from __future__ import annotations

from ...models import TwinValue
from ..facts import KnowledgeFact


POOL_PUMP = "pool/pompaPiscina"
POOL_SKIMMER = "pool/skimmerPiscina"
POOL_LIGHT = "pool/luciPiscina"
POOL_DECK_LIGHT = "pool/luciPedanaPiscina"


def _normalized_state(
    item: TwinValue | None,
) -> str:
    if item is None:
        return "UNKNOWN"

    value = item.value

    if isinstance(value, bool):
        return "ON" if value else "OFF"

    if isinstance(value, (int, float)):
        return "ON" if value != 0 else "OFF"

    text = str(value).strip().upper()

    if text in {"ON", "1", "TRUE"}:
        return "ON"

    if text in {"OFF", "0", "FALSE"}:
        return "OFF"

    return "UNKNOWN"


class PoolReasoner:
    """
    Interpreta il sottosistema piscina.

    La filtrazione è considerata pienamente attiva soltanto
    quando pompa e skimmer risultano entrambi ON.
    """

    category = "pool"

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

        if not lights:
            return []

        pump_state = _normalized_state(
            lights.get(POOL_PUMP)
        )

        skimmer_state = _normalized_state(
            lights.get(POOL_SKIMMER)
        )

        pool_light_state = _normalized_state(
            lights.get(POOL_LIGHT)
        )

        deck_light_state = _normalized_state(
            lights.get(POOL_DECK_LIGHT)
        )

        filtering_state = self._filtering_state(
            pump_state,
            skimmer_state,
        )

        lighting_state = self._lighting_state(
            pool_light_state,
            deck_light_state,
        )

        all_available = all(
            state != "UNKNOWN"
            for state in (
                pump_state,
                skimmer_state,
                pool_light_state,
                deck_light_state,
            )
        )

        return [
            KnowledgeFact(
                name="pool.pump_on",
                category=self.category,
                value=pump_state == "ON",
                reason=[
                    f"{POOL_PUMP}={pump_state}"
                ],
            ),
            KnowledgeFact(
                name="pool.skimmer_on",
                category=self.category,
                value=skimmer_state == "ON",
                reason=[
                    f"{POOL_SKIMMER}={skimmer_state}"
                ],
            ),
            KnowledgeFact(
                name="pool.filtering_active",
                category=self.category,
                value=filtering_state == "active",
                reason=[
                    f"pump={pump_state}",
                    f"skimmer={skimmer_state}",
                ],
            ),
            KnowledgeFact(
                name="pool.filtering_state",
                category=self.category,
                value=filtering_state,
                reason=[
                    f"pump={pump_state}",
                    f"skimmer={skimmer_state}",
                ],
            ),
            KnowledgeFact(
                name="pool.lighting_on",
                category=self.category,
                value=lighting_state in {
                    "partial",
                    "all_on",
                },
                reason=[
                    f"{POOL_LIGHT}={pool_light_state}",
                    (
                        f"{POOL_DECK_LIGHT}="
                        f"{deck_light_state}"
                    ),
                ],
            ),
            KnowledgeFact(
                name="pool.lighting_state",
                category=self.category,
                value=lighting_state,
                reason=[
                    f"{POOL_LIGHT}={pool_light_state}",
                    (
                        f"{POOL_DECK_LIGHT}="
                        f"{deck_light_state}"
                    ),
                ],
            ),
            KnowledgeFact(
                name="pool.system_running",
                category=self.category,
                value=(
                    pump_state == "ON"
                    or skimmer_state == "ON"
                ),
                reason=[
                    f"pump={pump_state}",
                    f"skimmer={skimmer_state}",
                ],
            ),
            KnowledgeFact(
                name="pool.all_available",
                category=self.category,
                value=all_available,
                reason=[
                    (
                        "pump, skimmer and pool lights "
                        "have known state"
                    )
                ],
            ),
            KnowledgeFact(
                name="pool.operating_mode",
                category=self.category,
                value=self._operating_mode(
                    filtering_state,
                    lighting_state,
                ),
                reason=[
                    (
                        "derived from filtering_state="
                        f"{filtering_state}"
                    ),
                    (
                        "derived from lighting_state="
                        f"{lighting_state}"
                    ),
                ],
            ),
        ]

    @staticmethod
    def _filtering_state(
        pump_state: str,
        skimmer_state: str,
    ) -> str:
        if "UNKNOWN" in {
            pump_state,
            skimmer_state,
        }:
            return "unknown"

        if (
            pump_state == "ON"
            and skimmer_state == "ON"
        ):
            return "active"

        if (
            pump_state == "OFF"
            and skimmer_state == "OFF"
        ):
            return "off"

        return "partial"

    @staticmethod
    def _lighting_state(
        pool_light_state: str,
        deck_light_state: str,
    ) -> str:
        states = (
            pool_light_state,
            deck_light_state,
        )

        if "UNKNOWN" in states:
            return "unknown"

        on_count = states.count("ON")

        if on_count == 0:
            return "off"

        if on_count == len(states):
            return "all_on"

        return "partial"

    @staticmethod
    def _operating_mode(
        filtering_state: str,
        lighting_state: str,
    ) -> str:
        filtering_active = (
            filtering_state == "active"
        )

        lighting_active = (
            lighting_state
            in {
                "partial",
                "all_on",
            }
        )

        if filtering_active and lighting_active:
            return "filtering_and_lighting"

        if filtering_active:
            return "filtering"

        if lighting_active:
            return "lighting"

        if (
            filtering_state == "unknown"
            or lighting_state == "unknown"
        ):
            return "unknown"

        if filtering_state == "partial":
            return "partial_filtering"

        return "idle"
