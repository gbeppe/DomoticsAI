from importlib.util import (
    module_from_spec,
    spec_from_file_location,
)
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[2]

SCRIPT = (
    ROOT
    / "scripts"
    / "validate-mqtt-capture.py"
)


def load_module():
    import sys

    module_name = (
        "mqtt_capture_validation"
    )

    spec = spec_from_file_location(
        module_name,
        SCRIPT,
    )

    assert spec is not None
    assert spec.loader is not None

    module = module_from_spec(
        spec
    )

    sys.modules[
        module_name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


validation = load_module()


def contract(
    tmp_path: Path,
) -> Path:
    path = (
        tmp_path
        / "contract.json"
    )

    path.write_text(
        json.dumps(
            {
                "baseTopic": {
                    "default":
                        "zara/android/domotica"
                },
                "topics": [
                    {
                        "pattern":
                            "light/{device}/state",
                        "domain": "lights",
                        "entity": "{device}",
                        "direction":
                            "broker_to_application",
                        "payloadType":
                            "boolean_on_off"
                    },
                    {
                        "pattern":
                            "energy/production",
                        "domain": "energy",
                        "entity":
                            "solar_production",
                        "direction":
                            "broker_to_application",
                        "payloadType":
                            "number"
                    },
                    {
                        "pattern":
                            "casa/clima/stato_completo",
                        "domain": "climate",
                        "entity":
                            "complete_snapshot",
                        "direction":
                            "broker_to_application",
                        "payloadType":
                            "json_object"
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    return path


def capture_file(
    tmp_path: Path,
    content: str,
) -> Path:
    path = tmp_path / "capture.log"

    path.write_text(
        content.strip(),
        encoding="utf-8",
    )

    return path


def test_matches_placeholder_topic(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            """
zara/android/domotica/light/sala/state ON
zara/android/domotica/light/portico/state OFF
""",
        ),
        contract_path=contract(
            tmp_path
        ),
    )

    assert (
        result["messagesMatched"]
        == 2
    )

    assert (
        result["unmatchedTopics"]
        == {}
    )

    assert (
        result["topicToPattern"][
            "light/sala/state"
        ]
        == "light/{device}/state"
    )


def test_detects_unmatched_topic(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            """
zara/android/domotica/new/domain/value 12
""",
        ),
        contract_path=contract(
            tmp_path
        ),
    )

    assert (
        result["unmatchedTopics"]
        == {
            "new/domain/value": 1
        }
    )


def test_detects_outside_namespace(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            """
shellies/device/power 100
""",
        ),
        contract_path=contract(
            tmp_path
        ),
    )

    assert (
        result["outsideNamespace"]
        == {
            "shellies/device/power": 1
        }
    )


def test_validates_payload_type(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            """
zara/android/domotica/light/sala/state INVALID
""",
        ),
        contract_path=contract(
            tmp_path
        ),
    )

    assert (
        "light/sala/state"
        in result[
            "incompatiblePayloads"
        ]
    )


def test_accepts_json_snapshot(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            """
zara/android/domotica/casa/clima/stato_completo {"season":"SUMMER"}
""",
        ),
        contract_path=contract(
            tmp_path
        ),
    )

    assert (
        result["incompatiblePayloads"]
        == {}
    )


def test_specific_pattern_precedes_generic():
    patterns = (
        validation.compile_patterns(
            {
                "topics": [
                    {
                        "pattern":
                            "system/{name}/state"
                    },
                    {
                        "pattern":
                            "system/ac_auto/state"
                    }
                ]
            }
        )
    )

    matches = validation.match_topic(
        "system/ac_auto/state",
        patterns,
    )

    assert (
        matches[0].pattern
        == "system/ac_auto/state"
    )


def test_specific_and_generic_match_is_not_ambiguous(
    tmp_path: Path,
):
    contract_path = (
        tmp_path / "contract-overlap.json"
    )

    contract_path.write_text(
        json.dumps(
            {
                "baseTopic": {
                    "default":
                        "zara/android/domotica"
                },
                "topics": [
                    {
                        "pattern":
                            "system/ac_auto/state",
                        "domain": "system",
                        "entity":
                            "system_ac_auto",
                        "direction":
                            "broker_to_application",
                        "payloadType":
                            "boolean"
                    },
                    {
                        "pattern":
                            "system/{name}/state",
                        "domain": "system",
                        "entity": "{name}",
                        "direction":
                            "broker_to_application",
                        "payloadType":
                            "scalar"
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            """
zara/android/domotica/system/ac_auto/state 1
""",
        ),
        contract_path=contract_path,
    )

    assert (
        result["ambiguousTopics"]
        == {}
    )

    assert (
        result["topicToPattern"][
            "system/ac_auto/state"
        ]
        == "system/ac_auto/state"
    )

def system_contract(
    tmp_path: Path,
) -> Path:
    path = (
        tmp_path
        / "system-contract.json"
    )

    path.write_text(
        json.dumps(
            {
                "baseTopic": {
                    "default":
                        "zara/android/domotica"
                },
                "topics": [
                    {
                        "pattern":
                            "system/set",
                        "domain":
                            "system",
                        "entity":
                            "automatic_climate_management",
                        "direction":
                            "application_to_broker",
                        "payloadType":
                            "json_object",
                        "legacyPayloadsTemporarilyAccepted": [
                            "boolean",
                            "0_or_1",
                            "ON_or_OFF",
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    return path


def test_system_set_accepts_json_payload(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            (
                "zara/android/domotica/system/set "
                "{\"automaticClimate\":true,"
                "\"origin\":\"android\"}"
            ),
        ),
        contract_path=system_contract(
            tmp_path
        ),
    )

    assert (
        result["incompatiblePayloads"]
        == {}
    )

    assert (
        result["legacyCompatiblePayloads"]
        == {}
    )

def test_system_set_accepts_legacy_payloads_temporarily(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            chr(10).join(
                [
                    (
                        "zara/android/domotica/"
                        "system/set 1"
                    ),
                    (
                        "zara/android/domotica/"
                        "system/set ON"
                    ),
                    (
                        "zara/android/domotica/"
                        "system/set true"
                    ),
                ]
            ),
        ),
        contract_path=system_contract(
            tmp_path
        ),
    )

    assert (
        result["incompatiblePayloads"]
        == {}
    )

    assert (
        result["legacyCompatiblePayloads"]
        == {
            "system/set": {
                "1": 1,
                "ON": 1,
                "true": 1,
            }
        }
    )


def test_system_set_rejects_invalid_payload(
    tmp_path: Path,
):
    result = validation.validate_capture(
        capture_path=capture_file(
            tmp_path,
            (
                "zara/android/domotica/"
                "system/set INVALID"
            ),
        ),
        contract_path=system_contract(
            tmp_path
        ),
    )

    assert (
        result["legacyCompatiblePayloads"]
        == {}
    )

    assert (
        result["incompatiblePayloads"]
        == {
            "system/set": {
                "INVALID": 1,
            }
        }
    )

