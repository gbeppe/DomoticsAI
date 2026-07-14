from .command_models import (
    CommandEnvelope,
    CommandReceipt,
    CommandStatus,
    LightCommandRequest,
)
from .lights_derived import ACTIVE_DEVICES

class LightsCommandService:
    COMMAND_PREFIX = "domoticsai/v1/cmd/lights"

    def __init__(self, publisher, simulation_mode=True):
        self._publisher = publisher
        self._simulation_mode = simulation_mode

    def submit(self, *, area, device_id, request: LightCommandRequest):
        entity = f"{area}/{device_id}"
        metadata = ACTIVE_DEVICES.get(entity)

        if metadata is None:
            return CommandReceipt(
                request_id="",
                status=CommandStatus.REJECTED,
                message=f"Unknown or inactive device: {entity}",
            )

        envelope = CommandEnvelope(
            area=area,
            device_id=device_id,
            desired_state=request.desired_state,
            mode="simulation" if self._simulation_mode else "active",
        )

        command_topic = f"{self.COMMAND_PREFIX}/{area}/{device_id}"
        ack_topic = (
            f"domoticsai/v1/ack/lights/{area}/{device_id}/"
            f"{envelope.request_id}"
        )

        self._publisher.publish_command(
            command_topic,
            envelope.model_dump_json(),
            qos=1,
            retain=False,
        )

        return CommandReceipt(
            request_id=envelope.request_id,
            status=CommandStatus.ACCEPTED,
            message="Command accepted in simulation mode",
            command_topic=command_topic,
            ack_topic=ack_topic,
        )
