from pathlib import Path

from tools.governance.common.context import ExecutionContext
from tools.governance.execution import ExecutionMode


def test_execution_context_defaults_to_generate(tmp_path: Path) -> None:
    context = ExecutionContext(
        repository_root=tmp_path,
        package_root=tmp_path,
        configuration={},
    )

    assert context.execution_mode is ExecutionMode.GENERATE


def test_execution_context_accepts_explicit_execution_mode(
    tmp_path: Path,
) -> None:
    context = ExecutionContext(
        repository_root=tmp_path,
        package_root=tmp_path,
        configuration={},
        execution_mode=ExecutionMode.CHECK,
    )

    assert context.execution_mode is ExecutionMode.CHECK
