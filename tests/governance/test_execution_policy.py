from dataclasses import FrozenInstanceError

import pytest

from tools.governance.execution import (
    ExecutionMode,
    ExecutionPolicy,
    ExitCodeStrategy,
    ExitPolicy,
    FindingPolicy,
    FindingThreshold,
)


@pytest.mark.parametrize(
    ("mode", "expected_policy"),
    [
        (
            ExecutionMode.GENERATE,
            ExecutionPolicy(
                generate_reports=True,
                finding_policy=FindingPolicy(
                    threshold=FindingThreshold.NONE,
                ),
                verbose_output=False,
                exit_policy=ExitPolicy(
                    strategy=ExitCodeStrategy.SUCCESS,
                ),
            ),
        ),
        (
            ExecutionMode.CHECK,
            ExecutionPolicy(
                generate_reports=False,
                finding_policy=FindingPolicy(
                    threshold=FindingThreshold.LOW,
                ),
                verbose_output=False,
                exit_policy=ExitPolicy(
                    strategy=ExitCodeStrategy.FAIL_ON_FINDINGS,
                ),
            ),
        ),
        (
            ExecutionMode.CI,
            ExecutionPolicy(
                generate_reports=False,
                finding_policy=FindingPolicy(
                    threshold=FindingThreshold.LOW,
                ),
                verbose_output=True,
                exit_policy=ExitPolicy(
                    strategy=ExitCodeStrategy.FAIL_ON_FINDINGS,
                ),
            ),
        ),
    ],
)
def test_execution_policy_from_mode(
    mode: ExecutionMode,
    expected_policy: ExecutionPolicy,
) -> None:
    assert ExecutionPolicy.from_mode(mode) == expected_policy


def test_execution_policy_is_immutable() -> None:
    policy = ExecutionPolicy.from_mode(ExecutionMode.GENERATE)

    with pytest.raises(FrozenInstanceError):
        policy.generate_reports = False
