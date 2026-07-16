import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "config"
    / "mqtt"
    / "application-contract-v1.json"
)


def load_contract():
    return json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )


def test_default_base_topic():
    contract = load_contract()

    assert (
        contract["baseTopic"]["default"]
        == "zara/android/domotica"
    )

    assert (
        contract["baseTopic"][
            "configurable"
        ]
        is True
    )


def test_application_is_limited_to_base_topic():
    contract = load_contract()

    assert (
        contract["principles"][
            "applicationUsesOnlyBaseTopic"
        ]
        is True
    )


def test_light_state_and_command_patterns():
    contract = load_contract()

    patterns = {
        item["pattern"]: item
        for item in contract["topics"]
    }

    assert (
        patterns[
            "light/{device}/state"
        ]["direction"]
        == "broker_to_application"
    )

    assert (
        patterns[
            "light/{device}/set"
        ]["direction"]
        == "application_to_broker"
    )

    assert (
        patterns[
            "light/{device}/set"
        ]["activationPhase"]
        == "Sprint 11.3"
    )


def test_inactive_lights_are_not_active():
    contract = load_contract()

    lights = contract["devices"]["lights"]

    active = {
        *lights["internal"],
        *lights["external"],
        *lights["pool"],
    }

    inactive = set(
        lights["historicalInactive"]
    )

    assert active.isdisjoint(inactive)

    assert "cucina" in inactive
    assert "esterno" in inactive


def test_ac_auto_topics_are_distinct():
    contract = load_contract()

    patterns = {
        item["pattern"]: item
        for item in contract["topics"]
    }

    legacy = patterns["ac_auto/set"]
    system = patterns[
        "system/ac_auto/state"
    ]

    assert (
        legacy["entity"]
        != system["entity"]
    )

    assert (
        legacy["semanticStatus"]
        == "distinct_semantics_pending_rename"
    )

    assert (
        system["semanticStatus"]
        == "distinct_semantics_pending_rename"
    )


def test_direct_device_namespaces_forbidden():
    contract = load_contract()

    forbidden = set(
        contract["principles"][
            "directDeviceNamespacesForbidden"
        ]
    )

    assert "cmnd/" in forbidden
    assert "shellies/" in forbidden
    assert "zigbee2mqtt/" in forbidden
