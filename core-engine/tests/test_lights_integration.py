from pathlib import Path

from domoticsai_core.digital_twin import DigitalTwinStore
from domoticsai_core.event_store import EventStore


def test_lights_derived_is_created_and_restored(
    tmp_path: Path,
):
    db_path = tmp_path / "lights.db"

    first = DigitalTwinStore(
        EventStore(str(db_path))
    )

    first.update_from_mqtt(
        "domoticsai/v1/state/lights/internal/sala",
        '{"value":"ON","quality":"good"}',
    )

    first.update_from_mqtt(
        "domoticsai/v1/state/lights/pool/pompaPiscina",
        '{"value":"ON","quality":"good"}',
    )

    derived = first.domain("lights_derived")

    assert derived is not None
    assert derived["lights_on_total"].value == 1
    assert derived["relays_on_total"].value == 1
    assert derived["internal_on"].value == 1
    assert derived["pool_on"].value == 1

    restored = DigitalTwinStore(
        EventStore(str(db_path))
    )

    restored_derived = restored.domain(
        "lights_derived"
    )

    assert restored_derived is not None
    assert (
        restored_derived["lights_on_total"].value
        == 1
    )
