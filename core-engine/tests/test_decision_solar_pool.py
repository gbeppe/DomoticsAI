from domoticsai_core.decisions.decision_engine import (
    HouseDecisionEngine,
)


def context(
    name: str,
    active: bool = True,
):
    return {
        "name": name,
        "active": active,
        "priority": 50,
        "category": "test",
    }


def test_recommends_pool_filtering_on_surplus():
    contexts = {
        "SOLAR_SURPLUS":
            context("SOLAR_SURPLUS"),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts={},
        )
    )

    assert len(decisions) == 1

    decision = decisions[0]

    assert (
        decision.action
        == "START_POOL_FILTERING"
    )

    assert decision.priority == 80

    assert (
        decision.data[
            "executionAllowed"
        ]
        is False
    )

    assert (
        decision.data[
            "requiresConfirmation"
        ]
        is True
    )


def test_does_not_recommend_when_pool_running():
    contexts = {
        "SOLAR_SURPLUS":
            context("SOLAR_SURPLUS"),
        "POOL_RUNNING":
            context("POOL_RUNNING"),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts={},
        )
    )

    assert decisions == []


def test_does_not_recommend_without_surplus():
    contexts = {
        "POOL_RUNNING":
            context(
                "POOL_RUNNING",
                active=False,
            ),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts={},
        )
    )

    assert decisions == []


def test_decision_id_is_stable():
    engine = HouseDecisionEngine()

    first = engine.evaluate(
        contexts={
            "SOLAR_SURPLUS":
                context("SOLAR_SURPLUS"),
        },
        facts={},
    )

    second = engine.evaluate(
        contexts={
            "SOLAR_SURPLUS":
                context("SOLAR_SURPLUS"),
        },
        facts={},
    )

    assert (
        first[0].decision_id
        == second[0].decision_id
    )
