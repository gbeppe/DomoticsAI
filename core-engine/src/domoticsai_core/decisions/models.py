from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


class DecisionKind(str, Enum):
    RECOMMENDATION = "recommendation"
    WARNING = "warning"
    INFORMATION = "information"


class DecisionStatus(str, Enum):
    ACTIVE = "active"
    DISMISSED = "dismissed"
    EXPIRED = "expired"


class HouseDecision(BaseModel):
    decision_id: str
    rule_id: str
    kind: DecisionKind
    status: DecisionStatus = (
        DecisionStatus.ACTIVE
    )

    action: str
    title: str
    description: str

    priority: int = Field(
        ge=0,
        le=100,
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    reason: list[str] = Field(
        default_factory=list
    )

    context_names: list[str] = Field(
        default_factory=list
    )

    data: dict[str, Any] = Field(
        default_factory=dict
    )

    created_at: str = Field(
        default_factory=utc_now_iso
    )

    source: str = "house-decision-engine"
