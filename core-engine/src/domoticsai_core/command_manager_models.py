from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class CommandState(str, Enum):
    CREATED = "created"
    VALIDATED = "validated"
    QUEUED = "queued"
    SENT = "sent"
    WAITING_CONFIRMATION = "waiting_confirmation"
    SIMULATED = "simulated"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    TIMEOUT = "timeout"
    FAILED = "failed"

TERMINAL_STATES = {
    CommandState.SIMULATED,
    CommandState.CONFIRMED,
    CommandState.REJECTED,
    CommandState.TIMEOUT,
    CommandState.FAILED,
}

class CommandSource(str, Enum):
    ANDROID = "android"
    AI = "ai"
    SCHEDULER = "scheduler"
    API = "api"

class CreateCommandRequest(BaseModel):
    domain: str
    action: str
    target: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    source: CommandSource = CommandSource.ANDROID
    timeout_seconds: int = Field(default=15, ge=1, le=300)
    correlation_id: str | None = None

class CommandRecord(BaseModel):
    command_id: str = Field(default_factory=lambda: str(uuid4()))
    domain: str
    action: str
    target: str
    parameters: dict[str, Any]
    source: CommandSource
    state: CommandState = CommandState.CREATED
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)
    expires_at: str
    correlation_id: str | None = None
    command_topic: str | None = None
    ack_topic: str | None = None
    error: str | None = None
    mode: str = "simulation"

class CommandEvent(BaseModel):
    command_id: str
    state: CommandState
    timestamp: str = Field(default_factory=utc_now_iso)
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
