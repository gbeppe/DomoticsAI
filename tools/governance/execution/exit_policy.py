"""Exit policies supported by the DomoticsAI Governance Toolkit."""

from dataclasses import dataclass
from enum import Enum


class ExitCodeStrategy(str, Enum):
    """Define how execution findings affect the process exit code."""

    SUCCESS = "success"
    FAIL_ON_FINDINGS = "fail_on_findings"


@dataclass(frozen=True)
class ExitPolicy:
    """Describe the exit-code strategy for an execution policy."""

    strategy: ExitCodeStrategy
