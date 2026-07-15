from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


class KnowledgeFact(BaseModel):
    """
    Fatto deterministico e spiegabile prodotto
    dall'House Knowledge Engine.
    """

    name: str
    category: str
    value: Any
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    reason: list[str] = Field(
        default_factory=list
    )
    observed_at: str = Field(
        default_factory=utc_now_iso
    )
    source: str = "house-knowledge-engine"
