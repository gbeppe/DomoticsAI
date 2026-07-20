from dataclasses import FrozenInstanceError

import pytest

from tools.governance.execution import FindingPolicy, FindingThreshold


def test_finding_threshold_values_are_stable() -> None:
    assert FindingThreshold.NONE.value == "none"
    assert FindingThreshold.LOW.value == "low"
    assert FindingThreshold.MEDIUM.value == "medium"
    assert FindingThreshold.HIGH.value == "high"


@pytest.mark.parametrize(
    "threshold",
    [
        FindingThreshold.NONE,
        FindingThreshold.LOW,
        FindingThreshold.MEDIUM,
        FindingThreshold.HIGH,
    ],
)
def test_finding_policy_describes_threshold(
    threshold: FindingThreshold,
) -> None:
    policy = FindingPolicy(threshold=threshold)

    assert policy.threshold is threshold


def test_finding_policy_is_immutable() -> None:
    policy = FindingPolicy(threshold=FindingThreshold.NONE)

    with pytest.raises(FrozenInstanceError):
        policy.threshold = FindingThreshold.LOW
