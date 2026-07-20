from dataclasses import FrozenInstanceError

import pytest

from tools.governance.execution import ExecutionMode, ExecutionPolicy


@pytest.mark.parametrize(
    ("mode", "expected_policy"),
    [
        (
            ExecutionMode.GENERATE,
            ExecutionPolicy(
                generate_reports=True,
                fail_on_findings=False,
                verbose_output=False,
            ),
        ),
        (
            ExecutionMode.CHECK,
            ExecutionPolicy(
                generate_reports=False,
                fail_on_findings=True,
                verbose_output=False,
            ),
        ),
        (
            ExecutionMode.CI,
            ExecutionPolicy(
                generate_reports=False,
                fail_on_findings=True,
                verbose_output=True,
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
