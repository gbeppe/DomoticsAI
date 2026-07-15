from domoticsai_core.knowledge.context_engine import (
    HouseContextEngine,
)


def fact(value):
    return {
        "value": value,
    }


def test_solar_surplus_and_pool_running():
    facts = {
        "energy.exporting":
            fact(True),
        "energy.primary_source":
            fact("solar"),
        "energy.importing":
            fact(False),
        "energy.battery_charging":
            fact(False),
        "lights.all_off":
            fact(True),
        "pool.system_running":
            fact(True),
        "pool.filtering_state":
            fact("active"),
        "pool.lighting_on":
            fact(False),
        "pool.lighting_state":
            fact("off"),
        "scenes.confirmed_mode":
            fact(None),
        "scenes.command_state":
            fact(None),
    }

    contexts = (
        HouseContextEngine().evaluate(
            facts
        )
    )

    assert "SOLAR_SURPLUS" in contexts
    assert "POOL_RUNNING" in contexts
    assert "ALL_LIGHTS_OFF" in contexts
    assert "GRID_IMPORT" not in contexts


def test_sleep_mode_has_highest_priority():
    facts = {
        "energy.exporting":
            fact(False),
        "energy.primary_source":
            fact("grid"),
        "energy.importing":
            fact(True),
        "energy.battery_charging":
            fact(False),
        "lights.all_off":
            fact(True),
        "pool.system_running":
            fact(False),
        "pool.filtering_state":
            fact("off"),
        "pool.lighting_on":
            fact(False),
        "pool.lighting_state":
            fact("off"),
        "scenes.confirmed_mode":
            fact("sleep"),
        "scenes.command_state":
            fact("confirmed"),
    }

    contexts = (
        HouseContextEngine().evaluate(
            facts
        )
    )

    names = list(contexts)

    assert names[0] == "SLEEP_MODE_ACTIVE"
    assert "GRID_IMPORT" in contexts
    assert "ALL_LIGHTS_OFF" in contexts


def test_normal_context_when_nothing_active():
    facts = {
        "energy.exporting":
            fact(False),
        "energy.primary_source":
            fact("none"),
        "energy.importing":
            fact(False),
        "energy.battery_charging":
            fact(False),
        "lights.all_off":
            fact(False),
        "pool.system_running":
            fact(False),
        "pool.filtering_state":
            fact("off"),
        "pool.lighting_on":
            fact(False),
        "pool.lighting_state":
            fact("off"),
        "scenes.confirmed_mode":
            fact(None),
        "scenes.command_state":
            fact(None),
    }

    contexts = (
        HouseContextEngine().evaluate(
            facts
        )
    )

    assert list(contexts) == [
        "HOUSE_NORMAL"
    ]


def test_tv_mode_context():
    facts = {
        "energy.exporting":
            fact(False),
        "energy.primary_source":
            fact("grid"),
        "energy.importing":
            fact(False),
        "energy.battery_charging":
            fact(False),
        "lights.all_off":
            fact(False),
        "pool.system_running":
            fact(False),
        "pool.filtering_state":
            fact("off"),
        "pool.lighting_on":
            fact(False),
        "pool.lighting_state":
            fact("off"),
        "scenes.confirmed_mode":
            fact("tv"),
        "scenes.command_state":
            fact("simulated"),
    }

    contexts = (
        HouseContextEngine().evaluate(
            facts
        )
    )

    assert "TV_MODE_ACTIVE" in contexts
