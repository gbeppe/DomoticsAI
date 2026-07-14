from pathlib import Path

from domoticsai_core.digital_twin import DigitalTwinStore
from domoticsai_core.event_store import EventStore


def test_energy_derived_is_created_and_restored(
    tmp_path: Path,
):
    db_path = tmp_path / "energy.db"

    first = DigitalTwinStore(
        EventStore(str(db_path))
    )

    first.update_from_mqtt(
        "domoticsai/v1/state/energy/solar_power_w",
        '{"value":4000,"unit":"W"}',
    )
    first.update_from_mqtt(
        "domoticsai/v1/state/energy/home_load_w",
        '{"value":1500,"unit":"W"}',
    )
    first.update_from_mqtt(
        "domoticsai/v1/state/energy/grid_power_w",
        '{"value":-1500,"unit":"W"}',
    )
    first.update_from_mqtt(
        "domoticsai/v1/state/energy/battery_power_w",
        '{"value":-1000,"unit":"W"}',
    )

    derived = first.domain("energy_derived")

    assert derived is not None
    assert derived["grid_direction"].value == "exporting"
    assert derived["battery_direction"].value == "charging"
    assert derived["balance_error_w"].value == 0

    restored = DigitalTwinStore(
        EventStore(str(db_path))
    )

    restored_derived = restored.domain(
        "energy_derived"
    )

    assert restored_derived is not None
    assert (
        restored_derived["operating_mode"].value
        == "solar_charging_and_exporting"
    )
