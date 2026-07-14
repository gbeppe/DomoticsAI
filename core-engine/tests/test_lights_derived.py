from domoticsai_core.lights_derived import (
    calculate_lights_derived,
)
from domoticsai_core.models import TwinValue


def value(state: str) -> TwinValue:
    return TwinValue(
        value=state,
        quality="good",
        source="legacy",
        timestamp="2026-07-14T12:00:00+00:00",
        topic="test",
    )


def test_counts_lights_and_relays():
    result = calculate_lights_derived(
        {
            "internal/sala": value("ON"),
            "internal/libreria": value("OFF"),
            "external/portico": value("ON"),
            "pool/luciPiscina": value("ON"),
            "pool/pompaPiscina": value("ON"),
        }
    )

    assert result["lights_on_total"] == 3
    assert result["relays_on_total"] == 1
    assert result["internal_on"] == 1
    assert result["external_on"] == 1
    assert result["pool_on"] == 2


def test_obsolete_devices_are_not_in_registry():
    result = calculate_lights_derived({})

    devices = result["devices"]

    assert "internal/lampadaHifi" not in devices
    assert "internal/cucina" not in devices
    assert "external/esterno" not in devices


def test_unknown_devices_are_reported_unavailable():
    result = calculate_lights_derived({})

    sala = result["devices"]["internal/sala"]

    assert sala["state"] == "UNKNOWN"
    assert sala["available"] is False
    assert result["all_available"] is False
