from domoticsai_core.knowledge.reasoners.energy_reasoner import (
    EnergyReasoner,
)
from domoticsai_core.models import TwinValue


def twin_value(
    value,
    unit=None,
):
    return TwinValue(
        value=value,
        unit=unit,
        quality="good",
        source="test",
        topic="test://energy",
    )


def facts_by_name(facts):
    return {
        fact.name: fact
        for fact in facts
    }


def test_solar_exporting_full_battery():
    domains = {
        "energy": {
            "solar_power_w": twin_value(
                3627,
                "W",
            ),
            "home_load_w": twin_value(
                462,
                "W",
            ),
            "powerwall_soc_pct": twin_value(
                100,
                "%",
            ),
        },
        "energy_derived": {
            "grid_direction": twin_value(
                "exporting"
            ),
            "battery_direction": twin_value(
                "idle"
            ),
            "operating_mode": twin_value(
                "solar_exporting"
            ),
            "self_sufficiency_pct": twin_value(
                100.0,
                "%",
            ),
            "self_consumption_pct": twin_value(
                12.8,
                "%",
            ),
        },
    }

    facts = facts_by_name(
        EnergyReasoner().reason(domains)
    )

    assert facts[
        "energy.exporting"
    ].value is True

    assert facts[
        "energy.importing"
    ].value is False

    assert facts[
        "energy.primary_source"
    ].value == "solar"

    assert facts[
        "energy.solar_production_level"
    ].value == "high"

    assert facts[
        "energy.battery_level"
    ].value == "full"

    assert facts[
        "energy.self_sufficient"
    ].value is True


def test_grid_supplying_home():
    domains = {
        "energy": {
            "solar_power_w": twin_value(
                0,
                "W",
            ),
            "home_load_w": twin_value(
                2200,
                "W",
            ),
            "powerwall_soc_pct": twin_value(
                25,
                "%",
            ),
        },
        "energy_derived": {
            "grid_direction": twin_value(
                "importing"
            ),
            "battery_direction": twin_value(
                "idle"
            ),
            "operating_mode": twin_value(
                "grid_supplying_home"
            ),
            "self_sufficiency_pct": twin_value(
                0.0,
                "%",
            ),
        },
    }

    facts = facts_by_name(
        EnergyReasoner().reason(domains)
    )

    assert facts[
        "energy.importing"
    ].value is True

    assert facts[
        "energy.primary_source"
    ].value == "grid"

    assert facts[
        "energy.battery_level"
    ].value == "low"

    assert facts[
        "energy.self_sufficient"
    ].value is False


def test_missing_energy_returns_no_facts():
    assert (
        EnergyReasoner().reason({})
        == []
    )
