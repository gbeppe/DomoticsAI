"""Finding policies supported by the DomoticsAI Governance Toolkit."""

from dataclasses import dataclass
from enum import Enum


class FindingThreshold(str, Enum):
    """Define the minimum finding severity considered significant."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class FindingPolicy:
    """Describe how findings are evaluated by an execution policy."""

    threshold: FindingThreshold
