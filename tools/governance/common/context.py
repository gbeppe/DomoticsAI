from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.governance.execution import ExecutionMode


@dataclass(frozen=True)
class ExecutionContext:
 repository_root:Path; package_root:Path; configuration:dict[str,Any]; execution_mode:ExecutionMode=ExecutionMode.GENERATE


def build_context(repo,cfg): return ExecutionContext(repo,Path(__file__).resolve().parents[1],cfg)
