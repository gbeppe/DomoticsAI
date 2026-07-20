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


def test_exit_policy_is_immutable() -> None:
    policy = ExitPolicy(strategy=ExitCodeStrategy.SUCCESS)

    with pytest.raises(FrozenInstanceError):
        policy.strategy = ExitCodeStrategy.FAIL_ON_FINDINGS
