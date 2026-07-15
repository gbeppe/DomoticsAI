from __future__ import annotations

from typing import Any

from .decision_engine import HouseDecisionEngine
from .models import HouseDecision
from ..knowledge.context_api import (
    active_contexts_from_domain,
)


def _as_dict(value: Any) -> dict[str, Any] | None:
    if hasattr(value, "model_dump"):
        result = value.model_dump()
        return result if isinstance(result, dict) else None

    if isinstance(value, dict):
        return value

    return None


def knowledge_facts_from_domain(
    knowledge: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """
    Estrae i KnowledgeFact dal dominio knowledge.

    Ogni entità del dominio è normalmente un TwinValue
    il cui campo value contiene il KnowledgeFact.
    """

    facts: dict[str, dict[str, Any]] = {}

    for entity_name, wrapped in knowledge.items():
        if entity_name.startswith("context."):
            continue

        twin_data = _as_dict(wrapped)

        if twin_data is None:
            continue

        fact = twin_data.get("value")

        if not isinstance(fact, dict):
            continue

        fact_name = fact.get("name")

        if not isinstance(fact_name, str):
            continue

        facts[fact_name] = fact

    return facts


def active_context_map_from_domain(
    knowledge: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """
    Converte la lista ordinata dei contesti attivi
    in una mappa indicizzata per nome.
    """

    return {
        context["name"]: context
        for context in active_contexts_from_domain(
            knowledge
        )
    }


class HouseDecisionService:
    def __init__(
        self,
        engine: HouseDecisionEngine | None = None,
    ) -> None:
        self._engine = (
            engine
            if engine is not None
            else HouseDecisionEngine()
        )

    def evaluate(
        self,
        knowledge: dict[str, Any],
    ) -> list[HouseDecision]:
        facts = knowledge_facts_from_domain(
            knowledge
        )

        contexts = (
            active_context_map_from_domain(
                knowledge
            )
        )

        return self._engine.evaluate(
            contexts=contexts,
            facts=facts,
        )
