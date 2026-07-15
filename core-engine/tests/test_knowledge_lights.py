from domoticsai_core.knowledge.reasoners.lights_reasoner import (
    LightsReasoner,
)
from domoticsai_core.models import TwinValue


def twin_value(
    value,
):
    return TwinValue(
        value=value,
        quality="good",
        source="test",
        topic="test://lights",
    )


def facts_by_name(facts):
    return {
        fact.name: fact
        for fact in facts
    }


def test_all_house_lights_off_pool_relays_on():
    domains = {
        "lights": {
            "internal/sala":
                twin_value("OFF"),
            "internal/televisione":
                twin_value("OFF"),
            "external/portico":
                twin_value("OFF"),
            "pool/luciPiscina":
                twin_value("OFF"),
            "pool/luciPedanaPiscina":
                twin_value("OFF"),
            "pool/pompaPiscina":
                twin_value("ON"),
            "pool/skimmerPiscina":
                twin_value("ON"),
        },
        "lights_derived": {
            "lights_on_total":
                twin_value(0),
            "relays_on_total":
                twin_value(2),
            "unknown_total":
                twin_value(0),
            "internal_on":
                twin_value(0),
            "internal_total":
                twin_value(6),
            "external_on":
                twin_value(0),
            "external_total":
                twin_value(1),
            "pool_on":
                twin_value(2),
            "pool_total":
                twin_value(4),
            "any_internal_on":
                twin_value(False),
            "any_external_on":
                twin_value(False),
            "all_available":
                twin_value(True),
        },
    }

    facts = facts_by_name(
        LightsReasoner().reason(
            domains
        )
    )

    assert (
        facts["lights.any_on"].value
        is False
    )

    assert (
        facts["lights.all_off"].value
        is True
    )

    assert (
        facts[
            "lights.pool_lighting_any_on"
        ].value
        is False
    )

    assert (
        facts[
            "lights.pool_lighting_state"
        ].value
        == "off"
    )

    assert (
        facts["lights.relays_on"].value
        == 2
    )


def test_partial_internal_and_pool_lighting():
    domains = {
        "lights": {
            "internal/sala":
                twin_value("ON"),
            "external/portico":
                twin_value("OFF"),
            "pool/luciPiscina":
                twin_value("ON"),
            "pool/luciPedanaPiscina":
                twin_value("OFF"),
        },
        "lights_derived": {
            "lights_on_total":
                twin_value(2),
            "relays_on_total":
                twin_value(0),
            "unknown_total":
                twin_value(0),
            "internal_on":
                twin_value(1),
            "internal_total":
                twin_value(6),
            "external_on":
                twin_value(0),
            "external_total":
                twin_value(1),
            "pool_on":
                twin_value(1),
            "pool_total":
                twin_value(4),
            "any_internal_on":
                twin_value(True),
            "any_external_on":
                twin_value(False),
            "all_available":
                twin_value(True),
        },
    }

    facts = facts_by_name(
        LightsReasoner().reason(
            domains
        )
    )

    assert (
        facts["lights.any_on"].value
        is True
    )

    assert (
        facts["lights.all_off"].value
        is False
    )

    assert (
        facts[
            "lights.internal_state"
        ].value
        == "partial"
    )

    assert (
        facts[
            "lights.pool_lighting_state"
        ].value
        == "partial"
    )

    assert (
        facts[
            "lights.pool_lighting_any_on"
        ].value
        is True
    )


def test_missing_lights_returns_no_facts():
    assert (
        LightsReasoner().reason({})
        == []
    )
