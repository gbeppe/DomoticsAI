from __future__ import annotations

from typing import Any
from uuid import NAMESPACE_URL, uuid5

from .base import DecisionRule
from ..models import (
    DecisionKind,
    HouseDecision,
)


def _context_active(
    contexts: dict[str, dict],
    name: str,
) -> bool:
    context = contexts.get(name)

    if not isinstance(context, dict):
        return False

    return bool(
        context.get("active", False)
    )


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


class CheckLightsAfterSleepModeRule(
    DecisionRule
):
    """
    Verifica la coerenza tra modalità notte
    confermata e stato osservato delle luci.

    Non invia comandi: genera soltanto un avviso.
    """

    rule_id = "check_lights_after_sleep_mode"

    def evaluate(
        self,
        contexts: dict[str, dict],
        facts: dict[str, dict],
    ) -> list[HouseDecision]:
        sleep_mode_active = _context_active(
            contexts,
            "SLEEP_MODE_ACTIVE",
        )

        lights_on = _fact_value(
            facts,
            "lights.count_on",
            0,
        )

        unknown_count = _fact_value(
            facts,
            "lights.unknown_count",
            0,
        )

        all_available = bool(
            _fact_value(
                facts,
                "lights.all_available",
                False,
            )
        )

        try:
            lights_on = int(lights_on)
        except (TypeError, ValueError):
            lights_on = 0

        try:
            unknown_count = int(
                unknown_count
            )
        except (TypeError, ValueError):
            unknown_count = 0

        if (
            not sleep_mode_active
            or lights_on <= 0
        ):
            return []

        decision_id = str(
            uuid5(
                NAMESPACE_URL,
                (
                    "domoticsai:"
                    f"{self.rule_id}"
                ),
            )
        )

        confidence = (
            1.0
            if all_available
            and unknown_count == 0
            else 0.8
        )

        return [
            HouseDecision(
                decision_id=decision_id,
                rule_id=self.rule_id,
                kind=DecisionKind.WARNING,
                action=(
                    "CHECK_LIGHTS_AFTER_SLEEP_MODE"
                ),
                title=(
                    "Luci ancora accese in "
                    "modalità notte"
                ),
                description=(
                    "La modalità notte risulta attiva, "
                    "ma una o più luci risultano ancora "
                    "accese. Verificare che lo scenario "
                    "sia stato applicato completamente."
                ),
                priority=90,
                confidence=confidence,
                context_names=[
                    "SLEEP_MODE_ACTIVE",
                ],
                reason=[
                    (
                        "context."
                        "SLEEP_MODE_ACTIVE active"
                    ),
                    (
                        "lights.count_on="
                        f"{lights_on}"
                    ),
                    (
                        "lights.unknown_count="
                        f"{unknown_count}"
                    ),
                    (
                        "lights.all_available="
                        f"{all_available}"
                    ),
                ],
                data={
                    "executionAllowed": False,
                    "requiresConfirmation": True,
                    "suggestedAction": (
                        "REVIEW_ACTIVE_LIGHTS"
                    ),
                    "lightsOn": lights_on,
                    "unknownLights": (
                        unknown_count
                    ),
                },
            )
        ]
