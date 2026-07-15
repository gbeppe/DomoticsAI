from domoticsai_core.knowledge.context_api import (
    active_contexts_from_domain,
)
from domoticsai_core.models import TwinValue


def wrapped_context(
    name: str,
    priority: int,
    category: str,
    active: bool = True,
) -> TwinValue:
    return TwinValue(
        value={
            "name": f"context.{name}",
            "category": "context",
            "value": {
                "name": name,
                "active": active,
                "priority": priority,
                "category": category,
                "confidence": 1.0,
                "reason": [
                    f"reason for {name}"
                ],
                "data": {},
                "observed_at": (
                    "2026-07-15T15:00:00+00:00"
                ),
                "source": (
                    "house-context-engine"
                ),
            },
            "confidence": 1.0,
            "reason": [],
            "observed_at": (
                "2026-07-15T15:00:00+00:00"
            ),
            "source": (
                "house-context-engine"
            ),
        },
        quality="calculated",
        source="core-engine",
        topic=f"internal://knowledge/context.{name}",
    )


def test_extracts_and_orders_active_contexts():
    domain = {
        "context.POOL_RUNNING":
            wrapped_context(
                "POOL_RUNNING",
                45,
                "pool",
            ),
        "context.SLEEP_MODE_ACTIVE":
            wrapped_context(
                "SLEEP_MODE_ACTIVE",
                100,
                "scene",
            ),
        "context.SOLAR_SURPLUS":
            wrapped_context(
                "SOLAR_SURPLUS",
                70,
                "energy",
            ),
    }

    contexts = active_contexts_from_domain(
        domain
    )

    assert [
        item["name"]
        for item in contexts
    ] == [
        "SLEEP_MODE_ACTIVE",
        "SOLAR_SURPLUS",
        "POOL_RUNNING",
    ]


def test_ignores_non_context_facts():
    domain = {
        "energy.exporting": TwinValue(
            value={
                "name": "energy.exporting",
                "value": True,
            },
            quality="calculated",
            source="core-engine",
            topic=(
                "internal://knowledge/"
                "energy.exporting"
            ),
        ),
    }

    assert (
        active_contexts_from_domain(
            domain
        )
        == []
    )


def test_ignores_inactive_contexts():
    domain = {
        "context.HOUSE_NORMAL":
            wrapped_context(
                "HOUSE_NORMAL",
                10,
                "house",
                active=False,
            )
    }

    assert (
        active_contexts_from_domain(
            domain
        )
        == []
    )
