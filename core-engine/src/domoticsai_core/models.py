from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

class TwinValue(BaseModel):
    value: Any
    unit: str | None = None
    quality: str = "unknown"
    source: str = "mqtt"
    timestamp: str = Field(default_factory=utc_now_iso)
    topic: str

class DigitalTwin(BaseModel):
    version: str = "0.1"
    updated_at: str = Field(default_factory=utc_now_iso)
    domains: dict[str, dict[str, TwinValue]] = Field(default_factory=dict)

class EventRecord(BaseModel):
    id: int | None = None
    received_at: str
    topic: str
    domain: str
    entity: str
    payload: str
    parsed_value: Any | None = None
    quality: str | None = None
