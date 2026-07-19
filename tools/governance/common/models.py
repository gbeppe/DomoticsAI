from dataclasses import asdict, dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .context import ExecutionContext


@dataclass(frozen=True)
class FileEntry:
    path: str
    size_bytes: int
    sha256: str
    extension: str
    category: str
    domain: str
    is_text: bool
    line_count: int | None = None


@dataclass(frozen=True)
class Issue:
    rule_id: str
    severity: str
    message: str
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Inventory:
    root: str
    files: list[FileEntry]
    issues: list[Issue]
    statistics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CensusState:
    """Mutable state shared by Repository Census pipeline stages."""

    ctx: "ExecutionContext"
    files: list[FileEntry] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)
    inventory: Inventory | None = None


@dataclass
class CommandResult:
    ok: bool
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    exit_code: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
