"""Execution policies supported by the DomoticsAI Governance Toolkit."""

from dataclasses import dataclass

from .mode import ExecutionMode


@dataclass(frozen=True)
class ExecutionPolicy:
    """Describe the behavior associated with an execution mode."""

    generate_reports: bool
    fail_on_findings: bool
    verbose_output: bool

    @classmethod
    def from_mode(cls, mode: ExecutionMode) -> "ExecutionPolicy":
        """Create the execution policy associated with an execution mode."""
        policies = {
            ExecutionMode.GENERATE: cls(
                generate_reports=True,
                fail_on_findings=False,
                verbose_output=False,
            ),
            ExecutionMode.CHECK: cls(
                generate_reports=False,
                fail_on_findings=True,
                verbose_output=False,
            ),
            ExecutionMode.CI: cls(
                generate_reports=False,
                fail_on_findings=True,
                verbose_output=True,
            ),
        }

        return policies[mode]
