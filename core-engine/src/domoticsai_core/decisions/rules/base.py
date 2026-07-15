from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import HouseDecision


class DecisionRule(ABC):
    rule_id: str

    @abstractmethod
    def evaluate(
        self,
        contexts: dict[str, dict],
        facts: dict[str, dict],
    ) -> list[HouseDecision]:
        """
        Valuta lo stato corrente e restituisce
        zero o più decisioni.

        Una regola non modifica mai il Digital Twin
        e non invia mai comandi.
        """
        raise NotImplementedError
