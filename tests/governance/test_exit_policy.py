from dataclasses import FrozenInstanceError

import pytest

from tools.governance.execution import ExitCodeStrategy, ExitPolicy


def test_exit_code_strategy_values_are_stable() -> None:
    assert ExitCodeStrategy.SUCCESS.value == "success"
    assert ExitCodeStrategy.FAIL_ON_FINDINGS.value == "fail_on_findings"


def test_exit_policy_describes_success_strategy() -> None:
    policy = ExitPolicy(strategy=ExitCodeStrategy.SUCCESS)

    assert policy.strategy is ExitCodeStrategy.SUCCESS


def test_exit_policy_describes_fail_on_findings_strategy() -> None:
    policy = ExitPolicy(strategy=ExitCodeStrategy.FAIL_ON_FINDINGS)

    assert policy.strategy is ExitCodeStrategy.FAIL_ON_FINDINGS


def test_success_strategy_always_returns_zero() -> None:
    policy = ExitPolicy(strategy=ExitCodeStrategy.SUCCESS)

    assert policy.exit_code(has_findings=False) == 0
    assert policy.exit_code(has_findings=True) == 0


def test_fail_on_findings_strategy_returns_zero_without_findings() -> None:
    policy = ExitPolicy(
        strategy=ExitCodeStrategy.FAIL_ON_FINDINGS,
    )

    assert policy.exit_code(has_findings=False) == 0


def test_fail_on_findings_strategy_returns_three_with_findings() -> None:
    policy = ExitPolicy(
        strategy=ExitCodeStrategy.FAIL_ON_FINDINGS,
    )

    assert policy.exit_code(has_findings=True) == 3



def test_exit_policy_is_immutable() -> None:
    policy = ExitPolicy(strategy=ExitCodeStrategy.SUCCESS)

    with pytest.raises(FrozenInstanceError):
        policy.strategy = ExitCodeStrategy.FAIL_ON_FINDINGS
