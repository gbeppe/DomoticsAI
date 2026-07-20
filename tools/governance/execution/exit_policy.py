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

    def exit_code(self, has_findings: bool) -> int:
        """Return the process exit code for the execution result."""
        if (
            self.strategy is ExitCodeStrategy.FAIL_ON_FINDINGS
            and has_findings
        ):
            return 3

        return 0
