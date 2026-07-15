from domoticsai_core.decisions.decision_engine import (
    HouseDecisionEngine,
)
from domoticsai_core.decisions.models import (
    DecisionKind,
)


def context(
    name: str,
    active: bool = True,
):
    return {
        "name": name,
        "active": active,
    }


def fact(value):
    return {
        "value": value,
    }


def sleep_warning(
    decisions,
):
    return [
        decision
        for decision in decisions
        if decision.rule_id
        == "check_lights_after_sleep_mode"
    ]


def test_warns_when_sleep_mode_and_lights_on():
    contexts = {
        "SLEEP_MODE_ACTIVE":
            context("SLEEP_MODE_ACTIVE"),
    }

    facts = {
        "lights.count_on":
            fact(2),
        "lights.unknown_count":
            fact(0),
        "lights.all_available":
            fact(True),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts=facts,
        )
    )

    matching = sleep_warning(decisions)

    assert len(matching) == 1

    decision = matching[0]

    assert (
        decision.kind
        == DecisionKind.WARNING
    )

    assert (
        decision.action
        == "CHECK_LIGHTS_AFTER_SLEEP_MODE"
    )

    assert decision.priority == 90
    assert decision.confidence == 1.0

    assert (
        decision.data["lightsOn"]
        == 2
    )

    assert (
        decision.data[
            "executionAllowed"
        ]
        is False
    )


def test_no_warning_when_all_lights_off():
    contexts = {
        "SLEEP_MODE_ACTIVE":
            context("SLEEP_MODE_ACTIVE"),
    }

    facts = {
        "lights.count_on":
            fact(0),
        "lights.unknown_count":
            fact(0),
        "lights.all_available":
            fact(True),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts=facts,
        )
    )

    assert sleep_warning(decisions) == []


def test_no_warning_without_sleep_mode():
    contexts = {}

    facts = {
        "lights.count_on":
            fact(3),
        "lights.unknown_count":
            fact(0),
        "lights.all_available":
            fact(True),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts=facts,
        )
    )

    assert sleep_warning(decisions) == []


def test_lower_confidence_with_unknown_lights():
    contexts = {
        "SLEEP_MODE_ACTIVE":
            context("SLEEP_MODE_ACTIVE"),
    }

    facts = {
        "lights.count_on":
            fact(1),
        "lights.unknown_count":
            fact(2),
        "lights.all_available":
            fact(False),
    }

    decisions = (
        HouseDecisionEngine().evaluate(
            contexts=contexts,
            facts=facts,
        )
    )

    decision = sleep_warning(
        decisions
    )[0]

    assert decision.confidence == 0.8

    assert (
        decision.data[
            "unknownLights"
        ]
        == 2
    )


def test_sleep_warning_id_is_stable():
    engine = HouseDecisionEngine()

    contexts = {
        "SLEEP_MODE_ACTIVE":
            context("SLEEP_MODE_ACTIVE"),
    }

    facts = {
        "lights.count_on":
            fact(1),
        "lights.unknown_count":
            fact(0),
        "lights.all_available":
            fact(True),
    }

    first = engine.evaluate(
        contexts=contexts,
        facts=facts,
    )

    second = engine.evaluate(
        contexts=contexts,
        facts=facts,
    )

    first_warning = sleep_warning(
        first
    )[0]

    second_warning = sleep_warning(
        second
    )[0]

    assert (
        first_warning.decision_id
        == second_warning.decision_id
    )
