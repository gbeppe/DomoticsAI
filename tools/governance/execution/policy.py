"""Execution policies supported by the DomoticsAI Governance Toolkit."""

from dataclasses import dataclass

from .exit_policy import ExitCodeStrategy, ExitPolicy
from .finding_policy import FindingPolicy, FindingThreshold
from .mode import ExecutionMode


@dataclass(frozen=True)
class ExecutionPolicy:
    """Describe the behavior associated with an execution mode."""

    generate_reports: bool
    finding_policy: FindingPolicy
    verbose_output: bool
    exit_policy: ExitPolicy

    @classmethod
    def from_mode(cls, mode: ExecutionMode) -> "ExecutionPolicy":
        """Create the execution policy associated with an execution mode."""
        policies = {
            ExecutionMode.GENERATE: cls(
                generate_reports=True,
                finding_policy=FindingPolicy(
                    threshold=FindingThreshold.NONE,
                ),
                verbose_output=False,
                exit_policy=ExitPolicy(
                    strategy=ExitCodeStrategy.SUCCESS,
                ),
            ),
            ExecutionMode.CHECK: cls(
                generate_reports=False,
                finding_policy=FindingPolicy(
                    threshold=FindingThreshold.LOW,
                ),
                verbose_output=False,
                exit_policy=ExitPolicy(
                    strategy=ExitCodeStrategy.FAIL_ON_FINDINGS,
                ),
            ),
            ExecutionMode.CI: cls(
                generate_reports=False,
                finding_policy=FindingPolicy(
                    threshold=FindingThreshold.LOW,
                ),
                verbose_output=True,
                exit_policy=ExitPolicy(
                    strategy=ExitCodeStrategy.FAIL_ON_FINDINGS,
                ),
            ),
        }

        return policies[mode]
