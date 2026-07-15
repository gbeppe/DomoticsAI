from __future__ import annotations

from ..models import TwinValue
from .facts import KnowledgeFact
from .reasoners.energy_reasoner import (
    EnergyReasoner,
)


class HouseKnowledgeEngine:
    def __init__(self) -> None:
        self._reasoners = [
            EnergyReasoner(),
        ]

    def evaluate(
        self,
        domains: dict[
            str,
            dict[str, TwinValue],
        ],
    ) -> dict[str, dict]:
        facts: dict[str, dict] = {}

        for reasoner in self._reasoners:
            reasoned_facts = reasoner.reason(
                domains
            )

            for fact in reasoned_facts:
                facts[fact.name] = (
                    fact.model_dump()
                )

        return facts
