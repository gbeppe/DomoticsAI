"""Execution modes supported by the DomoticsAI Governance Toolkit."""

from enum import Enum


class ExecutionMode(str, Enum):
    """Define how a governance tool is executed."""

    GENERATE = "generate"
    CHECK = "check"
    CI = "ci"

    @classmethod
    def from_value(cls, value: str) -> "ExecutionMode":
        """Create an execution mode from a normalized string value."""
        return cls(value.strip().lower())
