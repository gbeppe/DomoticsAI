from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


class HouseContext(BaseModel):
    name: str
    active: bool
    priority: int = Field(
        ge=0,
        le=100,
    )
    category: str
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    reason: list[str] = Field(
        default_factory=list
    )
    data: dict[str, Any] = Field(
        default_factory=dict
    )
    observed_at: str = Field(
        default_factory=utc_now_iso
    )
    source: str = "house-context-engine"
