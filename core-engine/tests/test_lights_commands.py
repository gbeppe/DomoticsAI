from domoticsai_core.command_models import (
    CommandStatus,
    LightCommandRequest,
    LightDesiredState,
)
from domoticsai_core.lights_commands import LightsCommandService

class FakePublisher:
    def __init__(self):
        self.messages = []

    def publish_command(self, topic, payload, *, qos=1, retain=False):
        self.messages.append((topic, payload, qos, retain))

def test_accepts_active_light_in_simulation():
    publisher = FakePublisher()
    service = LightsCommandService(publisher, simulation_mode=True)

    receipt = service.submit(
        area="internal",
        device_id="sala",
        request=LightCommandRequest(
            desired_state=LightDesiredState.ON
        ),
    )

    assert receipt.status == CommandStatus.ACCEPTED
    assert publisher.messages[0][0] == (
        "domoticsai/v1/cmd/lights/internal/sala"
    )
    assert publisher.messages[0][3] is False

def test_rejects_obsolete_device():
    publisher = FakePublisher()
    service = LightsCommandService(publisher)

    receipt = service.submit(
        area="internal",
        device_id="lampadaHifi",
        request=LightCommandRequest(
            desired_state=LightDesiredState.ON
        ),
    )

    assert receipt.status == CommandStatus.REJECTED
    assert publisher.messages == []
