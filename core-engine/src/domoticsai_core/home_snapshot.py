from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .decisions.decision_service import (
    HouseDecisionService,
)
from .knowledge.context_api import (
    active_contexts_from_domain,
)


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def _as_dict(
    value: Any,
) -> dict[str, Any] | None:
    if hasattr(value, "model_dump"):
        result = value.model_dump()

        if isinstance(result, dict):
            return result

        return None

    if isinstance(value, dict):
        return value

    return None


def latest_knowledge_timestamp(
    knowledge: dict[str, Any],
) -> str | None:
    """
    Restituisce il timestamp più recente fra i TwinValue
    presenti nel dominio knowledge.
    """

    timestamps: list[str] = []

    for wrapped in knowledge.values():
        data = _as_dict(wrapped)

        if data is None:
            continue

        timestamp = data.get("timestamp")

        if (
            isinstance(timestamp, str)
            and timestamp
        ):
            timestamps.append(timestamp)

    if not timestamps:
        return None

    # I timestamp ISO UTC generati dal Core Engine
    # sono confrontabili lessicograficamente.
    return max(timestamps)


class HouseHomeSnapshotService:
    """
    Costruisce la risposta destinata alla Home Android.

    Contesti e decisioni vengono ricavati dalla stessa
    copia del dominio knowledge.
    """

    def __init__(
        self,
        decision_service: (
            HouseDecisionService | None
        ) = None,
    ) -> None:
        self._decision_service = (
            decision_service
            if decision_service is not None
            else HouseDecisionService()
        )

    def build(
        self,
        knowledge: dict[str, Any],
    ) -> dict[str, Any]:
        contexts = (
            active_contexts_from_domain(
                knowledge
            )
        )

        decisions = (
            self._decision_service.evaluate(
                knowledge
            )
        )

        serialized_decisions = [
            decision.model_dump(
                mode="json"
            )
            for decision in decisions
        ]

        warnings = sum(
            1
            for decision
            in serialized_decisions
            if decision.get("kind")
            == "warning"
        )

        recommendations = sum(
            1
            for decision
            in serialized_decisions
            if decision.get("kind")
            == "recommendation"
        )

        information = sum(
            1
            for decision
            in serialized_decisions
            if decision.get("kind")
            == "information"
        )

        return {
            "generatedAt": utc_now_iso(),
            "knowledgeUpdatedAt": (
                latest_knowledge_timestamp(
                    knowledge
                )
            ),
            "contexts": contexts,
            "decisions": serialized_decisions,
            "summary": {
                "activeContexts": len(
                    contexts
                ),
                "activeDecisions": len(
                    serialized_decisions
                ),
                "warnings": warnings,
                "recommendations": (
                    recommendations
                ),
                "information": information,
            },
            "executionEnabled": False,
        }
