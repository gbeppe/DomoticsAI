from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel, Field

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

class CommandStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SIMULATED = "simulated"
    CONFIRMED = "confirmed"
    TIMEOUT = "timeout"
    FAILED = "failed"

class LightDesiredState(str, Enum):
    ON = "ON"
    OFF = "OFF"

class LightCommandRequest(BaseModel):
    desired_state: LightDesiredState
    confirm: bool = False

class CommandEnvelope(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    domain: str = "lights"
    area: str
    device_id: str
    desired_state: LightDesiredState
    created_at: str = Field(default_factory=utc_now_iso)
    expires_in_seconds: int = 15
    source: str = "android"
    mode: str = "simulation"

class CommandReceipt(BaseModel):
    request_id: str
    status: CommandStatus
    message: str
    command_topic: str | None = None
    ack_topic: str | None = None
