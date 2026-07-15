from __future__ import annotations

from typing import Any
from uuid import NAMESPACE_URL, uuid5

from .base import DecisionRule
from ..models import (
    DecisionKind,
    HouseDecision,
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


class GridImportWhilePoolRunningRule(
    DecisionRule
):
    """
    Segnala che la piscina è in funzione mentre
    la casa sta prelevando energia dalla rete.

    La regola non ordina lo spegnimento:
    produce soltanto un avviso consultivo.
    """

    rule_id = (
        "grid_import_while_pool_running"
    )

    def evaluate(
        self,
        contexts: dict[str, dict],
        facts: dict[str, dict],
    ) -> list[HouseDecision]:
        importing = bool(
            _fact_value(
                facts,
                "energy.importing",
                False,
            )
        )

        pool_running = bool(
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

        if (
            not importing
            or not pool_running
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
                kind=DecisionKind.WARNING,
                action=(
                    "REVIEW_POOL_FILTERING"
                ),
                title=(
                    "Piscina attiva durante "
                    "il prelievo dalla rete"
                ),
                description=(
                    "La piscina risulta in funzione "
                    "mentre la casa sta importando "
                    "energia dalla rete. Valutare "
                    "se rinviare la filtrazione."
                ),
                priority=70,
                confidence=1.0,
                context_names=[
                    "GRID_IMPORT",
                    "POOL_RUNNING",
                ],
                reason=[
                    "energy.importing=True",
                    "pool.system_running=True",
                    (
                        "pool.filtering_state="
                        f"{filtering_state}"
                    ),
                ],
                data={
                    "executionAllowed": False,
                    "requiresConfirmation": True,
                    "suggestedAction": (
                        "STOP_POOL_FILTERING"
                    ),
                    "filteringState": (
                        filtering_state
                    ),
                },
            )
        ]
