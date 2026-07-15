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


class EnergyReasoner:
    """
    Interpreta i domini energy ed energy_derived.

    Produce esclusivamente fatti deterministici:
    nessuna previsione e nessuna inferenza probabilistica.
    """

    category = "energy"

    def reason(
        self,
        domains: dict[
            str,
            dict[str, TwinValue],
        ],
    ) -> list[KnowledgeFact]:
        energy = domains.get(
            "energy",
            {},
        )

        derived = domains.get(
            "energy_derived",
            {},
        )

        if not energy and not derived:
            return []

        grid_direction = _value(
            derived,
            "grid_direction",
            "unknown",
        )

        battery_direction = _value(
            derived,
            "battery_direction",
            "unknown",
        )

        operating_mode = _value(
            derived,
            "operating_mode",
            "unknown",
        )

        solar_power_w = _value(
            energy,
            "solar_power_w",
        )

        home_load_w = _value(
            energy,
            "home_load_w",
        )

        powerwall_soc_pct = _value(
            energy,
            "powerwall_soc_pct",
        )

        self_sufficiency_pct = _value(
            derived,
            "self_sufficiency_pct",
        )

        self_consumption_pct = _value(
            derived,
            "self_consumption_pct",
        )

        facts = [
            KnowledgeFact(
                name="energy.exporting",
                category=self.category,
                value=(
                    grid_direction
                    == "exporting"
                ),
                reason=[
                    (
                        "energy_derived."
                        "grid_direction="
                        f"{grid_direction}"
                    )
                ],
            ),
            KnowledgeFact(
                name="energy.importing",
                category=self.category,
                value=(
                    grid_direction
                    == "importing"
                ),
                reason=[
                    (
                        "energy_derived."
                        "grid_direction="
                        f"{grid_direction}"
                    )
                ],
            ),
            KnowledgeFact(
                name="energy.battery_charging",
                category=self.category,
                value=(
                    battery_direction
                    == "charging"
                ),
                reason=[
                    (
                        "energy_derived."
                        "battery_direction="
                        f"{battery_direction}"
                    )
                ],
            ),
            KnowledgeFact(
                name="energy.battery_discharging",
                category=self.category,
                value=(
                    battery_direction
                    == "discharging"
                ),
                reason=[
                    (
                        "energy_derived."
                        "battery_direction="
                        f"{battery_direction}"
                    )
                ],
            ),
            KnowledgeFact(
                name="energy.operating_mode",
                category=self.category,
                value=operating_mode,
                reason=[
                    (
                        "energy_derived."
                        "operating_mode="
                        f"{operating_mode}"
                    )
                ],
            ),
            KnowledgeFact(
                name="energy.primary_source",
                category=self.category,
                value=self._primary_source(
                    operating_mode
                ),
                reason=[
                    (
                        "derived from "
                        "energy.operating_mode"
                    )
                ],
            ),
        ]

        if solar_power_w is not None:
            facts.append(
                KnowledgeFact(
                    name=(
                        "energy.solar_production_level"
                    ),
                    category=self.category,
                    value=self._production_level(
                        solar_power_w
                    ),
                    reason=[
                        (
                            "energy.solar_power_w="
                            f"{solar_power_w}"
                        )
                    ],
                )
            )

        if home_load_w is not None:
            facts.append(
                KnowledgeFact(
                    name="energy.home_load_level",
                    category=self.category,
                    value=self._load_level(
                        home_load_w
                    ),
                    reason=[
                        (
                            "energy.home_load_w="
                            f"{home_load_w}"
                        )
                    ],
                )
            )

        if powerwall_soc_pct is not None:
            facts.extend(
                [
                    KnowledgeFact(
                        name=(
                            "energy.battery_soc_pct"
                        ),
                        category=self.category,
                        value=powerwall_soc_pct,
                        reason=[
                            (
                                "energy."
                                "powerwall_soc_pct"
                            )
                        ],
                    ),
                    KnowledgeFact(
                        name=(
                            "energy.battery_level"
                        ),
                        category=self.category,
                        value=self._battery_level(
                            powerwall_soc_pct
                        ),
                        reason=[
                            (
                                "energy."
                                "powerwall_soc_pct="
                                f"{powerwall_soc_pct}"
                            )
                        ],
                    ),
                ]
            )

        if self_sufficiency_pct is not None:
            facts.extend(
                [
                    KnowledgeFact(
                        name=(
                            "energy."
                            "self_sufficiency_pct"
                        ),
                        category=self.category,
                        value=self_sufficiency_pct,
                        reason=[
                            (
                                "energy_derived."
                                "self_sufficiency_pct"
                            )
                        ],
                    ),
                    KnowledgeFact(
                        name=(
                            "energy.self_sufficient"
                        ),
                        category=self.category,
                        value=(
                            self_sufficiency_pct
                            >= 99.0
                        ),
                        reason=[
                            (
                                "self_sufficiency_pct"
                                f"={self_sufficiency_pct}"
                            )
                        ],
                    ),
                ]
            )

        if self_consumption_pct is not None:
            facts.append(
                KnowledgeFact(
                    name=(
                        "energy."
                        "self_consumption_pct"
                    ),
                    category=self.category,
                    value=self_consumption_pct,
                    reason=[
                        (
                            "energy_derived."
                            "self_consumption_pct"
                        )
                    ],
                )
            )

        return facts

    @staticmethod
    def _primary_source(
        operating_mode: str,
    ) -> str:
        if operating_mode.startswith(
            "solar_"
        ):
            return "solar"

        if operating_mode == (
            "battery_supplying_home"
        ):
            return "battery"

        if operating_mode == (
            "grid_supplying_home"
        ):
            return "grid"

        if operating_mode == "idle":
            return "none"

        return "unknown"

    @staticmethod
    def _production_level(
        solar_power_w: float,
    ) -> str:
        if solar_power_w < 20:
            return "none"

        if solar_power_w < 1000:
            return "low"

        if solar_power_w < 3000:
            return "medium"

        return "high"

    @staticmethod
    def _load_level(
        home_load_w: float,
    ) -> str:
        if home_load_w < 300:
            return "very_low"

        if home_load_w < 1000:
            return "low"

        if home_load_w < 3000:
            return "medium"

        if home_load_w < 6000:
            return "high"

        return "very_high"

    @staticmethod
    def _battery_level(
        soc_pct: float,
    ) -> str:
        if soc_pct < 10:
            return "critical"

        if soc_pct < 30:
            return "low"

        if soc_pct < 70:
            return "medium"

        if soc_pct < 95:
            return "high"

        return "full"
