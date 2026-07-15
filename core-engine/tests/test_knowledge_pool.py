from domoticsai_core.knowledge.reasoners.pool_reasoner import (
    PoolReasoner,
)
from domoticsai_core.models import TwinValue


def twin_value(value):
    return TwinValue(
        value=value,
        quality="good",
        source="test",
        topic="test://pool",
    )


def facts_by_name(facts):
    return {
        fact.name: fact
        for fact in facts
    }


def test_filtering_active_lights_off():
    domains = {
        "lights": {
            "pool/pompaPiscina":
                twin_value("ON"),
            "pool/skimmerPiscina":
                twin_value("ON"),
            "pool/luciPiscina":
                twin_value("OFF"),
            "pool/luciPedanaPiscina":
                twin_value("OFF"),
        }
    }

    facts = facts_by_name(
        PoolReasoner().reason(domains)
    )

    assert (
        facts["pool.filtering_active"].value
        is True
    )

    assert (
        facts["pool.filtering_state"].value
        == "active"
    )

    assert (
        facts["pool.lighting_on"].value
        is False
    )

    assert (
        facts["pool.operating_mode"].value
        == "filtering"
    )


def test_partial_filtering_and_partial_lighting():
    domains = {
        "lights": {
            "pool/pompaPiscina":
                twin_value("ON"),
            "pool/skimmerPiscina":
                twin_value("OFF"),
            "pool/luciPiscina":
                twin_value("ON"),
            "pool/luciPedanaPiscina":
                twin_value("OFF"),
        }
    }

    facts = facts_by_name(
        PoolReasoner().reason(domains)
    )

    assert (
        facts["pool.filtering_active"].value
        is False
    )

    assert (
        facts["pool.filtering_state"].value
        == "partial"
    )

    assert (
        facts["pool.lighting_state"].value
        == "partial"
    )

    assert (
        facts["pool.operating_mode"].value
        == "lighting"
    )


def test_filtering_and_lighting():
    domains = {
        "lights": {
            "pool/pompaPiscina":
                twin_value("ON"),
            "pool/skimmerPiscina":
                twin_value("ON"),
            "pool/luciPiscina":
                twin_value("ON"),
            "pool/luciPedanaPiscina":
                twin_value("ON"),
        }
    }

    facts = facts_by_name(
        PoolReasoner().reason(domains)
    )

    assert (
        facts["pool.operating_mode"].value
        == "filtering_and_lighting"
    )


def test_missing_pool_domain_returns_no_facts():
    assert (
        PoolReasoner().reason({})
        == []
    )
