from domoticsai_core.command_request import CommandRequest


def test_command_request_defaults():

    request = CommandRequest(
        entity_id="lights.living.power",
        action="set",
    )

    assert request.entity_id == "lights.living.power"

    assert request.action == "set"

    assert request.parameters == {}

    assert request.source == "core"


def test_command_request_parameters():

    request = CommandRequest(
        entity_id="climate.living",
        action="set_temperature",
        parameters={
            "temperature": 22.5,
            "mode": "heat",
        },
        source="android",
    )

    assert request.parameters["temperature"] == 22.5

    assert request.parameters["mode"] == "heat"

    assert request.source == "android"
