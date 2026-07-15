from domoticsai_core.decisions.decision_engine import (
    HouseDecisionEngine,
)
from domoticsai_core.decisions.models import (
    DecisionKind,
)


def fact(value):
    return {
        "value": value,
    }


def test_warns_when_grid_import_and_pool_running():
    facts = {
        "energy.importing":
            fact(True),
        "pool.system_running":
            fact(True),
        "pool.filtering_state":
            fact("active"),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts={},
            facts=facts,
        )
    )

    matching = [
        decision
        for decision in decisions
        if decision.rule_id
        == (
            "grid_import_while_"
            "pool_running"
        )
    ]

    assert len(matching) == 1

    decision = matching[0]

    assert (
        decision.kind
        == DecisionKind.WARNING
    )

    assert (
        decision.action
        == "REVIEW_POOL_FILTERING"
    )

    assert decision.priority == 70

    assert (
        decision.data[
            "executionAllowed"
        ]
        is False
    )

    assert (
        decision.data[
            "suggestedAction"
        ]
        == "STOP_POOL_FILTERING"
    )


def test_no_warning_without_grid_import():
    facts = {
        "energy.importing":
            fact(False),
        "pool.system_running":
            fact(True),
        "pool.filtering_state":
            fact("active"),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts={},
            facts=facts,
        )
    )

    assert all(
        decision.rule_id
        != (
            "grid_import_while_"
            "pool_running"
        )
        for decision in decisions
    )


def test_no_warning_when_pool_is_off():
    facts = {
        "energy.importing":
            fact(True),
        "pool.system_running":
            fact(False),
        "pool.filtering_state":
            fact("off"),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts={},
            facts=facts,
        )
    )

    assert all(
        decision.rule_id
        != (
            "grid_import_while_"
            "pool_running"
        )
        for decision in decisions
    )


def test_grid_pool_decision_id_is_stable():
    engine = HouseDecisionEngine()

    facts = {
        "energy.importing":
            fact(True),
        "pool.system_running":
            fact(True),
        "pool.filtering_state":
            fact("active"),
    }

    first = engine.evaluate(
        contexts={},
        facts=facts,
    )

    second = engine.evaluate(
        contexts={},
        facts=facts,
    )

    first_warning = next(
        decision
        for decision in first
        if decision.rule_id
        == (
            "grid_import_while_"
            "pool_running"
        )
    )

    second_warning = next(
        decision
        for decision in second
        if decision.rule_id
        == (
            "grid_import_while_"
            "pool_running"
        )
    )

    assert (
        first_warning.decision_id
        == second_warning.decision_id
    )


def test_solar_pool_and_grid_pool_are_independent():
    engine = HouseDecisionEngine()

    contexts = {
        "SOLAR_SURPLUS": {
            "name": "SOLAR_SURPLUS",
            "active": True,
        }
    }

    facts = {
        "energy.importing":
            fact(False),
        "pool.system_running":
            fact(False),
        "pool.filtering_state":
            fact("off"),
    }

    decisions = engine.evaluate(
        contexts=contexts,
        facts=facts,
    )

    assert [
        decision.action
        for decision in decisions
    ] == [
        "START_POOL_FILTERING"
    ]
