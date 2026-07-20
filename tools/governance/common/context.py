from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.governance.execution import ExecutionMode, ExecutionPolicy


@dataclass(frozen=True)
class ExecutionContext:
    repository_root: Path
    package_root: Path
    configuration: dict[str, Any]
    execution_mode: ExecutionMode = ExecutionMode.GENERATE
    execution_policy: ExecutionPolicy | None = None


def build_context(
    repo,
    cfg,
    execution_mode=ExecutionMode.GENERATE,
    execution_policy=None,
):
    resolved_policy = (
        execution_policy
        if execution_policy is not None
        else ExecutionPolicy.from_mode(execution_mode)
    )

    return ExecutionContext(
        repository_root=repo,
        package_root=Path(__file__).resolve().parents[1],
        configuration=cfg,
        execution_mode=execution_mode,
        execution_policy=resolved_policy,
    )
