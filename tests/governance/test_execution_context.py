from pathlib import Path

from tools.governance.common.context import ExecutionContext, build_context
from tools.governance.execution import ExecutionMode, ExecutionPolicy


def test_execution_context_defaults_to_generate(tmp_path: Path) -> None:
    context = ExecutionContext(
        repository_root=tmp_path,
        package_root=tmp_path,
        configuration={},
    )

    assert context.execution_mode is ExecutionMode.GENERATE
    assert context.execution_policy is None


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


def test_build_context_resolves_policy_from_execution_mode(
    tmp_path: Path,
) -> None:
    context = build_context(
        tmp_path,
        {},
        ExecutionMode.CHECK,
    )

    assert context.execution_mode is ExecutionMode.CHECK
    assert context.execution_policy == ExecutionPolicy.from_mode(
        ExecutionMode.CHECK
    )


def test_build_context_accepts_explicit_execution_policy(
    tmp_path: Path,
) -> None:
    policy = ExecutionPolicy.from_mode(ExecutionMode.CI)

    context = build_context(
        tmp_path,
        {},
        ExecutionMode.CI,
        policy,
    )

    assert context.execution_policy is policy
