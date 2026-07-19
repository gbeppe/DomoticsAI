"""Repository Census pipeline stages."""

from collections import Counter
from tools.governance.common.filesystem import (
    is_text,
    iter_files,
    lines,
    sha256_file,
)
from tools.governance.common.models import (
    CensusState,
    FileEntry,
    Inventory,
)
from .classification import category, domain
from .rules import evaluate_rules


class ScanStage:
    """Populate the Census state with the repository file inventory."""

    def process(self, state: CensusState) -> CensusState:
        files = []

        ignored_names = set(
            state.ctx.configuration["ignore"]["names"]
        )

        for path in iter_files(
            state.ctx.repository_root,
            ignored_names,
        ):
            relative = path.relative_to(
                state.ctx.repository_root
            )

            files.append(
                FileEntry(
                    path=relative.as_posix(),
                    size_bytes=path.stat().st_size,
                    sha256=sha256_file(path),
                    extension=path.suffix.lower(),
                    category=category(
                        relative,
                        state.ctx.configuration,
                    ),
                    domain=domain(
                        relative,
                        state.ctx.configuration,
                    ),
                    is_text=is_text(path),
                    line_count=lines(path),
                )
            )

        state.files = files
        return state

class RuleStage:
    """Evaluate repository governance rules."""

    def process(self, state: CensusState) -> CensusState:
        state.issues = evaluate_rules(
            state.ctx,
            state.files,
        )
        return state

class StatisticsStage:
    """Calculate Repository Census statistics."""

    def process(self, state: CensusState) -> CensusState:
        state.statistics = {
            "file_count": len(state.files),
            "total_size_bytes": sum(
                file_entry.size_bytes
                for file_entry in state.files
            ),
            "text_file_count": sum(
                file_entry.is_text
                for file_entry in state.files
            ),
            "categories": dict(
                sorted(
                    Counter(
                        file_entry.category
                        for file_entry in state.files
                    ).items()
                )
            ),
            "domains": dict(
                sorted(
                    Counter(
                        file_entry.domain
                        for file_entry in state.files
                    ).items()
                )
            ),
            "severities": dict(
                sorted(
                    Counter(
                        issue.severity
                        for issue in state.issues
                    ).items()
                )
            ),
            "finding_count": len(state.issues),
        }

        return state


class InventoryStage:
    """Build the final Repository Census inventory."""

    def process(self, state: CensusState) -> CensusState:
        state.inventory = Inventory(
            str(state.ctx.repository_root),
            state.files,
            state.issues,
            state.statistics,
        )

        return state
