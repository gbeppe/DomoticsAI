from __future__ import annotations

from typing import Any


def active_contexts_from_domain(
    knowledge: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Estrae gli HouseContext dal dominio knowledge.

    Struttura attesa:
    TwinValue.value -> KnowledgeFact.value -> HouseContext.
    """

    result: list[dict[str, Any]] = []

    for entity_name, twin_value in (
        knowledge.items()
    ):
        if not entity_name.startswith(
            "context."
        ):
            continue

        if hasattr(twin_value, "model_dump"):
            twin_data = twin_value.model_dump()
        elif isinstance(twin_value, dict):
            twin_data = twin_value
        else:
            continue

        fact = twin_data.get("value")

        if not isinstance(fact, dict):
            continue

        context = fact.get("value")

        if not isinstance(context, dict):
            continue

        if not bool(
            context.get("active", False)
        ):
            continue

        name = context.get("name")

        if not isinstance(name, str):
            continue

        result.append({
            "name": name,
            "active": True,
            "priority": int(
                context.get(
                    "priority",
                    0,
                )
            ),
            "category": str(
                context.get(
                    "category",
                    "house",
                )
            ),
            "confidence": float(
                context.get(
                    "confidence",
                    1.0,
                )
            ),
            "reason": list(
                context.get(
                    "reason",
                    [],
                )
            ),
            "data": dict(
                context.get(
                    "data",
                    {},
                )
            ),
            "observedAt": context.get(
                "observed_at"
            ),
        })

    result.sort(
        key=lambda item: (
            -item["priority"],
            item["name"],
        )
    )

    return result
