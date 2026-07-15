from __future__ import annotations

from uuid import uuid5, NAMESPACE_URL

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


class StartPoolOnSolarSurplusRule(
    DecisionRule
):
    rule_id = "start_pool_on_solar_surplus"

    def evaluate(
        self,
        contexts: dict[str, dict],
        facts: dict[str, dict],
    ) -> list[HouseDecision]:
        solar_surplus = _context_active(
            contexts,
            "SOLAR_SURPLUS",
        )

        pool_running = _context_active(
            contexts,
            "POOL_RUNNING",
        )

        if (
            not solar_surplus
            or pool_running
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

        return [
            HouseDecision(
                decision_id=decision_id,
                rule_id=self.rule_id,
                kind=(
                    DecisionKind.RECOMMENDATION
                ),
                action=(
                    "START_POOL_FILTERING"
                ),
                title=(
                    "Avviare la filtrazione "
                    "della piscina"
                ),
                description=(
                    "È disponibile surplus "
                    "fotovoltaico e la piscina "
                    "non risulta in funzione."
                ),
                priority=80,
                confidence=1.0,
                context_names=[
                    "SOLAR_SURPLUS",
                ],
                reason=[
                    (
                        "context."
                        "SOLAR_SURPLUS active"
                    ),
                    (
                        "context."
                        "POOL_RUNNING inactive"
                    ),
                ],
                data={
                    "executionAllowed": False,
                    "requiresConfirmation": True,
                },
            )
        ]
