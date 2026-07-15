from domoticsai_core.home_snapshot import (
    HouseHomeSnapshotService,
    latest_knowledge_timestamp,
)
from domoticsai_core.models import TwinValue


def knowledge_fact(
    name: str,
    value,
    timestamp: str,
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
            "observed_at": timestamp,
            "source": (
                "house-knowledge-engine"
            ),
        },
        quality="calculated",
        source="core-engine",
        timestamp=timestamp,
        topic=f"internal://knowledge/{name}",
    )


def house_context(
    name: str,
    *,
    priority: int,
    category: str,
    timestamp: str,
) -> TwinValue:
    return TwinValue(
        value={
            "name": f"context.{name}",
            "category": "context",
            "value": {
                "name": name,
                "active": True,
                "priority": priority,
                "category": category,
                "confidence": 1.0,
                "reason": ["test context"],
                "data": {},
                "observed_at": timestamp,
                "source": (
                    "house-context-engine"
                ),
            },
            "confidence": 1.0,
            "reason": ["test context"],
            "observed_at": timestamp,
            "source": (
                "house-context-engine"
            ),
        },
        quality="calculated",
        source="core-engine",
        timestamp=timestamp,
        topic=(
            "internal://knowledge/"
            f"context.{name}"
        ),
    )


def test_builds_contexts_and_decisions_from_same_domain():
    timestamp = (
        "2026-07-15T20:00:00+00:00"
    )

    knowledge = {
        "energy.exporting":
            knowledge_fact(
                "energy.exporting",
                True,
                timestamp,
            ),
        "pool.system_running":
            knowledge_fact(
                "pool.system_running",
                False,
                timestamp,
            ),
        "context.SOLAR_SURPLUS":
            house_context(
                "SOLAR_SURPLUS",
                priority=70,
                category="energy",
                timestamp=timestamp,
            ),
    }

    snapshot = (
        HouseHomeSnapshotService().build(
            knowledge
        )
    )

    assert (
        snapshot["knowledgeUpdatedAt"]
        == timestamp
    )

    assert [
        item["name"]
        for item in snapshot["contexts"]
    ] == [
        "SOLAR_SURPLUS"
    ]

    assert [
        item["action"]
        for item in snapshot["decisions"]
    ] == [
        "START_POOL_FILTERING"
    ]

    assert (
        snapshot["summary"][
            "activeContexts"
        ]
        == 1
    )

    assert (
        snapshot["summary"][
            "activeDecisions"
        ]
        == 1
    )

    assert (
        snapshot["summary"][
            "recommendations"
        ]
        == 1
    )

    assert (
        snapshot["executionEnabled"]
        is False
    )


def test_empty_knowledge_returns_empty_snapshot():
    snapshot = (
        HouseHomeSnapshotService().build(
            {}
        )
    )

    assert snapshot["contexts"] == []
    assert snapshot["decisions"] == []

    assert (
        snapshot["summary"][
            "activeContexts"
        ]
        == 0
    )

    assert (
        snapshot["summary"][
            "activeDecisions"
        ]
        == 0
    )

    assert (
        snapshot["knowledgeUpdatedAt"]
        is None
    )


def test_latest_timestamp_is_selected():
    knowledge = {
        "first": knowledge_fact(
            "energy.importing",
            False,
            "2026-07-15T20:00:00+00:00",
        ),
        "second": knowledge_fact(
            "lights.all_off",
            True,
            "2026-07-15T20:01:00+00:00",
        ),
    }

    assert latest_knowledge_timestamp(
        knowledge
    ) == "2026-07-15T20:01:00+00:00"
