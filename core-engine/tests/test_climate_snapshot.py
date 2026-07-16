from domoticsai_core.climate_snapshot import (
    build_climate_snapshot,
)


def wrapped(
    value,
    unit=None,
    timestamp="2026-07-16T10:00:00+00:00",
):
    return {
        "value": value,
        "unit": unit,
        "quality": "good",
        "source": "core-engine",
        "timestamp": timestamp,
    }


def test_builds_complete_climate_snapshot():
    twin = {
        "domains": {
            "climate": {
                "living_temperature_c":
                    wrapped(25.5, "°C"),
                "living_humidity_pct":
                    wrapped(55.0, "%"),
                "living_humidex":
                    wrapped(30.1),
                "bedroom_temperature_c":
                    wrapped(24.1, "°C"),
                "bedroom_humidity_pct":
                    wrapped(53.0, "%"),
                "bedroom_humidex":
                    wrapped(26.4),
                "outdoor_temperature_c":
                    wrapped(28.0, "°C"),
                "outdoor_humidity_pct":
                    wrapped(58.0, "%"),
                "living_target_temperature_c":
                    wrapped(23.0, "°C"),
                "complete_snapshot":
                    wrapped(
                        {"season": "SUMMER"}
                    ),
            },
            "vmc": {
                "speed": wrapped(1, "level"),
            },
            "thermal": {
                "dhw_buffer_temperature_c":
                    wrapped(47.8, "°C"),
                "buffer_lower_temperature_c":
                    wrapped(37.7, "°C"),
                "buffer_upper_temperature_c":
                    wrapped(47.8, "°C"),
            },
            "fireplace": {
                "mode": wrapped("sanitaria"),
                "powered": wrapped(False),
                "power_level":
                    wrapped(2, "level"),
            },
        }
    }

    snapshot = build_climate_snapshot(
        twin
    )

    assert snapshot.complete is True

    result = snapshot.to_dict()

    assert (
        result["environment"]["living"]
        ["temperature"]["value"]
        == 25.5
    )

    assert (
        result["ventilation"]["speed"]
        ["value"]
        == 1
    )

    assert (
        result["fireplace"]["powered"]
        ["value"]
        is False
    )


def test_missing_values_are_unavailable():
    snapshot = build_climate_snapshot(
        {
            "domains": {
                "climate": {
                    "living_temperature_c":
                        wrapped(25.0, "°C")
                }
            }
        }
    )

    assert snapshot.complete is False

    result = snapshot.to_dict()

    assert (
        result["environment"]["living"]
        ["temperature"]["available"]
        is True
    )

    assert (
        result["environment"]["bedroom"]
        ["temperature"]["available"]
        is False
    )


def test_updated_at_uses_latest_metric():
    snapshot = build_climate_snapshot(
        {
            "domains": {
                "climate": {
                    "living_temperature_c":
                        wrapped(
                            25.0,
                            "°C",
                            "2026-07-16T10:00:00+00:00",
                        ),
                    "living_humidity_pct":
                        wrapped(
                            55.0,
                            "%",
                            "2026-07-16T10:02:00+00:00",
                        ),
                }
            }
        }
    )

    assert (
        snapshot.updated_at
        == "2026-07-16T10:02:00+00:00"
    )
