from tools.governance.execution import ExecutionMode

import pytest


def test_values_are_stable():
    assert ExecutionMode.GENERATE.value == "generate"
    assert ExecutionMode.CHECK.value == "check"
    assert ExecutionMode.CI.value == "ci"


def test_parsing():
    assert ExecutionMode.from_value("generate") is ExecutionMode.GENERATE
    assert ExecutionMode.from_value("CHECK") is ExecutionMode.CHECK
    assert ExecutionMode.from_value(" ci ") is ExecutionMode.CI


def test_unknown_mode():
    with pytest.raises(ValueError):
        ExecutionMode.from_value("unknown")
