from pathlib import Path

from tools.governance.repository_census.stages import (
    InventoryStage,
    RuleStage,
    ScanStage,
    StatisticsStage,
)
from tools.governance.common.context import ExecutionContext
from tools.governance.common.models import CensusState


def build_state(tmp_path: Path) -> CensusState:
    configuration = {
        "ignore": {
            "names": [],
        },
        "classification": {
            "generated_markers": [],
            "runtime_markers": [],
        },
        "domains": {
            "default": "Repository",
            "path_rules": [],
        },
    }

    context = ExecutionContext(
        repository_root=tmp_path,
        package_root=tmp_path,
        configuration=configuration,
    )

    return CensusState(ctx=context)


def test_scan_stage_populates_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Demo\n",
        encoding="utf-8",
    )

    state = build_state(tmp_path)
    result = ScanStage().process(state)

    assert result is state
    assert len(result.files) == 1
    assert result.files[0].path == "README.md"
    assert result.files[0].category == "Documentation"


def test_scan_stage_replaces_existing_files(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        "print('ok')\n",
        encoding="utf-8",
    )

    state = build_state(tmp_path)
    state.files.append(object())  # type: ignore[arg-type]

    result = ScanStage().process(state)

    assert len(result.files) == 1
    assert result.files[0].path == "main.py"
    assert result.files[0].category == "Source Code"

def test_rule_stage_populates_issues(tmp_path: Path) -> None:
    configuration = {
        "ignore": {
            "names": [],
        },
        "classification": {
            "generated_markers": [],
            "runtime_markers": [],
        },
        "domains": {
            "default": "Repository",
            "path_rules": [],
        },
        "rules": {
            "thin_document": {
                "minimum_lines": 3,
            },
        },
    }

    context = ExecutionContext(
        repository_root=tmp_path,
        package_root=tmp_path,
        configuration=configuration,
    )

    (tmp_path / "README.md").write_text(
        "# Demo\n",
        encoding="utf-8",
    )

    state = CensusState(ctx=context)

    ScanStage().process(state)
    result = RuleStage().process(state)

    assert result is state
    assert any(
        issue.rule_id == "DGT-DOC-002"
        for issue in result.issues
    )

def test_statistics_stage_populates_statistics(
    tmp_path: Path,
) -> None:
    state = build_state(tmp_path)

    (tmp_path / "README.md").write_text(
        "# Demo\n",
        encoding="utf-8",
    )

    ScanStage().process(state)
    StatisticsStage().process(state)

    assert state.statistics["file_count"] == 1
    assert state.statistics["text_file_count"] == 1
    assert state.statistics["finding_count"] == 0
    assert state.statistics["categories"] == {
        "Documentation": 1,
    }


def test_inventory_stage_builds_inventory(
    tmp_path: Path,
) -> None:
    state = build_state(tmp_path)

    (tmp_path / "main.py").write_text(
        "print('ok')\n",
        encoding="utf-8",
    )

    ScanStage().process(state)
    StatisticsStage().process(state)
    result = InventoryStage().process(state)

    assert result is state
    assert result.inventory is not None
    assert result.inventory.root == str(tmp_path)
    assert result.inventory.files == result.files
    assert result.inventory.issues == result.issues
    assert result.inventory.statistics == result.statistics
