from __future__ import annotations

from typing import Any

from .context import HouseContext


def _fact_value(
    facts: dict[str, dict],
    name: str,
    default: Any = None,
) -> Any:
    fact = facts.get(name)

    if not isinstance(fact, dict):
        return default

    return fact.get(
        "value",
        default,
    )


class HouseContextEngine:
    """
    Sintetizza i facts deterministici in contesti globali.

    Non legge il Digital Twin grezzo e non genera comandi.
    """

    def evaluate(
        self,
        facts: dict[str, dict],
    ) -> dict[str, dict]:
        contexts = [
            self._solar_surplus(facts),
            self._grid_import(facts),
            self._battery_charging(facts),
            self._all_lights_off(facts),
            self._pool_running(facts),
            self._pool_lighting(facts),
            self._tv_mode(facts),
            self._sleep_mode(facts),
        ]

        active_contexts = [
            context
            for context in contexts
            if context.active
        ]

        if not active_contexts:
            active_contexts.append(
                HouseContext(
                    name="HOUSE_NORMAL",
                    active=True,
                    priority=10,
                    category="house",
                    reason=[
                        (
                            "no higher-priority "
                            "house context is active"
                        )
                    ],
                )
            )

        active_contexts.sort(
            key=lambda item: (
                -item.priority,
                item.name,
            )
        )

        return {
            context.name: context.model_dump()
            for context in active_contexts
        }

    @staticmethod
    def _solar_surplus(
        facts: dict[str, dict],
    ) -> HouseContext:
        exporting = bool(
            _fact_value(
                facts,
                "energy.exporting",
                False,
            )
        )

        source = _fact_value(
            facts,
            "energy.primary_source",
            "unknown",
        )

        return HouseContext(
            name="SOLAR_SURPLUS",
            active=(
                exporting
                and source == "solar"
            ),
            priority=70,
            category="energy",
            reason=[
                f"energy.exporting={exporting}",
                f"energy.primary_source={source}",
            ],
        )

    @staticmethod
    def _grid_import(
        facts: dict[str, dict],
    ) -> HouseContext:
        importing = bool(
            _fact_value(
                facts,
                "energy.importing",
                False,
            )
        )

        return HouseContext(
            name="GRID_IMPORT",
            active=importing,
            priority=60,
            category="energy",
            reason=[
                f"energy.importing={importing}"
            ],
        )

    @staticmethod
    def _battery_charging(
        facts: dict[str, dict],
    ) -> HouseContext:
        charging = bool(
            _fact_value(
                facts,
                "energy.battery_charging",
                False,
            )
        )

        return HouseContext(
            name="BATTERY_CHARGING",
            active=charging,
            priority=50,
            category="energy",
            reason=[
                (
                    "energy.battery_charging="
                    f"{charging}"
                )
            ],
        )

    @staticmethod
    def _all_lights_off(
        facts: dict[str, dict],
    ) -> HouseContext:
        all_off = bool(
            _fact_value(
                facts,
                "lights.all_off",
                False,
            )
        )

        return HouseContext(
            name="ALL_LIGHTS_OFF",
            active=all_off,
            priority=40,
            category="lighting",
            reason=[
                f"lights.all_off={all_off}"
            ],
        )

    @staticmethod
    def _pool_running(
        facts: dict[str, dict],
    ) -> HouseContext:
        running = bool(
            _fact_value(
                facts,
                "pool.system_running",
                False,
            )
        )

        filtering_state = _fact_value(
            facts,
            "pool.filtering_state",
            "unknown",
        )

        return HouseContext(
            name="POOL_RUNNING",
            active=running,
            priority=45,
            category="pool",
            reason=[
                f"pool.system_running={running}",
                (
                    "pool.filtering_state="
                    f"{filtering_state}"
                ),
            ],
            data={
                "filteringState":
                    filtering_state,
            },
        )

    @staticmethod
    def _pool_lighting(
        facts: dict[str, dict],
    ) -> HouseContext:
        lighting = bool(
            _fact_value(
                facts,
                "pool.lighting_on",
                False,
            )
        )

        lighting_state = _fact_value(
            facts,
            "pool.lighting_state",
            "unknown",
        )

        return HouseContext(
            name="POOL_LIGHTING",
            active=lighting,
            priority=35,
            category="pool",
            reason=[
                f"pool.lighting_on={lighting}",
                (
                    "pool.lighting_state="
                    f"{lighting_state}"
                ),
            ],
            data={
                "lightingState":
                    lighting_state,
            },
        )

    @staticmethod
    def _tv_mode(
        facts: dict[str, dict],
    ) -> HouseContext:
        confirmed_mode = _fact_value(
            facts,
            "scenes.confirmed_mode",
        )

        command_state = _fact_value(
            facts,
            "scenes.command_state",
        )

        active = (
            confirmed_mode == "tv"
            and command_state in {
                "confirmed",
                "simulated",
            }
        )

        return HouseContext(
            name="TV_MODE_ACTIVE",
            active=active,
            priority=90,
            category="scene",
            reason=[
                (
                    "scenes.confirmed_mode="
                    f"{confirmed_mode}"
                ),
                (
                    "scenes.command_state="
                    f"{command_state}"
                ),
            ],
        )

    @staticmethod
    def _sleep_mode(
        facts: dict[str, dict],
    ) -> HouseContext:
        confirmed_mode = _fact_value(
            facts,
            "scenes.confirmed_mode",
        )

        command_state = _fact_value(
            facts,
            "scenes.command_state",
        )

        active = (
            confirmed_mode == "sleep"
            and command_state in {
                "confirmed",
                "simulated",
            }
        )

        return HouseContext(
            name="SLEEP_MODE_ACTIVE",
            active=active,
            priority=100,
            category="scene",
            reason=[
                (
                    "scenes.confirmed_mode="
                    f"{confirmed_mode}"
                ),
                (
                    "scenes.command_state="
                    f"{command_state}"
                ),
            ],
        )
