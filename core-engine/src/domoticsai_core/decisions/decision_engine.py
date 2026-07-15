from __future__ import annotations

from .models import HouseDecision
from .rules.solar_pool import (
    StartPoolOnSolarSurplusRule,
)


class HouseDecisionEngine:
    def __init__(self) -> None:
        self._rules = [
            StartPoolOnSolarSurplusRule(),
        ]

    def evaluate(
        self,
        contexts: dict[str, dict],
        facts: dict[str, dict],
    ) -> list[HouseDecision]:
        decisions: list[
            HouseDecision
        ] = []

        for rule in self._rules:
            decisions.extend(
                rule.evaluate(
                    contexts,
                    facts,
                )
            )

        decisions.sort(
            key=lambda item: (
                -item.priority,
                item.action,
            )
        )

        return decisions
