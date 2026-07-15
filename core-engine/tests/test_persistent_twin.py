from pathlib import Path

from domoticsai_core.digital_twin import DigitalTwinStore
from domoticsai_core.event_store import EventStore
from domoticsai_core.sqlite_database import SQLiteDatabase


def test_twin_is_restored_after_restart(tmp_path: Path):
    db_path = tmp_path / "core-engine.db"

    first_store = EventStore(
        SQLiteDatabase(
            str(db_path)
        )
    )
    first_twin = DigitalTwinStore(first_store)

    accepted = first_twin.update_from_mqtt(
        "domoticsai/v1/state/energy/solar_power_w",
        '{"value":2450,"unit":"W","quality":"good","source":"legacy"}',
    )

    assert accepted is True
    assert (
        first_twin.snapshot()
        .domains["energy"]["solar_power_w"]
        .value
        == 2450
    )

    second_store = EventStore(
        SQLiteDatabase(
            str(db_path)
        )
    )
    restored_twin = DigitalTwinStore(second_store)
    restored = restored_twin.snapshot()

    assert restored.domains["energy"]["solar_power_w"].value == 2450
    assert restored.domains["energy"]["solar_power_w"].unit == "W"
    assert restored.domains["energy"]["solar_power_w"].quality == "good"
    assert restored.domains["energy"]["solar_power_w"].source == "legacy"


def test_latest_value_replaces_previous_value(tmp_path: Path):
    db_path = tmp_path / "core-engine.db"
    event_store = EventStore(
        SQLiteDatabase(
            str(db_path)
        )
    )
    twin = DigitalTwinStore(event_store)

    twin.update_from_mqtt(
        "domoticsai/v1/state/energy/home_load_w",
        '{"value":400,"unit":"W","quality":"good"}',
    )
    twin.update_from_mqtt(
        "domoticsai/v1/state/energy/home_load_w",
        '{"value":525,"unit":"W","quality":"good"}',
    )

    restored = DigitalTwinStore(EventStore(
        SQLiteDatabase(
            str(db_path)
        )
    )).snapshot()

    assert restored.domains["energy"]["home_load_w"].value == 525
