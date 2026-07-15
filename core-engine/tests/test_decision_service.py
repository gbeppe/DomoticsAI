from domoticsai_core.decisions.decision_service import (
    HouseDecisionService,
    active_context_map_from_domain,
    knowledge_facts_from_domain,
)
from domoticsai_core.models import TwinValue


def knowledge_fact(
    name: str,
    value,
) -> TwinValue:
    return TwinValue(
        value={
            "name": name,
            "category": (
                name.split(".", 1)[0]
            ),
            "value": value,
            "confidence": 1.0,
            "reason": ["test fact"],
            "observed_at": (
                "2026-07-15T16:00:00+00:00"
            ),
            "source": (
                "house-knowledge-engine"
            ),
        },
        quality="calculated",
        source="core-engine",
        topic=f"internal://knowledge/{name}",
    )


def house_context(
    name: str,
    *,
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
                "reason": ["test context"],
                "data": {},
                "observed_at": (
                    "2026-07-15T16:00:00+00:00"
                ),
                "source": (
                    "house-context-engine"
                ),
            },
            "confidence": 1.0,
            "reason": ["test context"],
            "observed_at": (
                "2026-07-15T16:00:00+00:00"
            ),
            "source": (
                "house-context-engine"
            ),
        },
        quality="calculated",
        source="core-engine",
        topic=(
            "internal://knowledge/"
            f"context.{name}"
        ),
    )


def test_extracts_facts_without_contexts():
    domain = {
        "energy.exporting":
            knowledge_fact(
                "energy.exporting",
                True,
            ),
        "pool.system_running":
            knowledge_fact(
                "pool.system_running",
                False,
            ),
        "context.SOLAR_SURPLUS":
            house_context(
                "SOLAR_SURPLUS",
                priority=70,
                category="energy",
            ),
    }

    facts = knowledge_facts_from_domain(
        domain
    )

    assert set(facts) == {
        "energy.exporting",
        "pool.system_running",
    }

    assert (
        facts["energy.exporting"]["value"]
        is True
    )


def test_extracts_only_active_contexts():
    domain = {
        "context.SOLAR_SURPLUS":
            house_context(
                "SOLAR_SURPLUS",
                priority=70,
                category="energy",
            ),
        "context.POOL_RUNNING":
            house_context(
                "POOL_RUNNING",
                priority=45,
                category="pool",
                active=False,
            ),
    }

    contexts = (
        active_context_map_from_domain(
            domain
        )
    )

    assert set(contexts) == {
        "SOLAR_SURPLUS"
    }


def test_real_knowledge_generates_decision():
    domain = {
        "energy.exporting":
            knowledge_fact(
                "energy.exporting",
                True,
            ),
        "pool.system_running":
            knowledge_fact(
                "pool.system_running",
                False,
            ),
        "context.SOLAR_SURPLUS":
            house_context(
                "SOLAR_SURPLUS",
                priority=70,
                category="energy",
            ),
    }

    decisions = (
        HouseDecisionService().evaluate(
            domain
        )
    )

    assert len(decisions) == 1

    assert (
        decisions[0].action
        == "START_POOL_FILTERING"
    )


def test_pool_running_suppresses_decision():
    domain = {
        "context.SOLAR_SURPLUS":
            house_context(
                "SOLAR_SURPLUS",
                priority=70,
                category="energy",
            ),
        "context.POOL_RUNNING":
            house_context(
                "POOL_RUNNING",
                priority=45,
                category="pool",
            ),
    }

    decisions = (
        HouseDecisionService().evaluate(
            domain
        )
    )

    assert decisions == []
