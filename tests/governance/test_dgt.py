from pathlib import Path

import pytest

import tools.governance.governance as governance
from tools.governance.common.models import Inventory, Issue
from tools.governance.execution import ExecutionMode, ExecutionPolicy
from tools.governance.governance import main
from tools.governance.repository_census.classification import category, domain
def test_category_and_domain():
 c={'classification':{'generated_markers':['.egg-info/'],'runtime_markers':['.logs/']}}
 assert category(Path('docs/README.md'),c)=='Documentation'
 d={'domains':{'default':'Repository','path_rules':[{'domain':'Android','prefixes':['app']}]}}
 assert domain(Path('app/src/Main.kt'),d)=='Android'
def test_cli(tmp_path,capsys):
 assert main(['version'])==0
 assert '0.2.0' in capsys.readouterr().out
 (tmp_path/'README.md').write_text('# Demo\nEnough\nLines\nFor\nThe\nRule\nHere\nNow\n')
 assert main(['--repo',str(tmp_path),'doctor'])==0
 assert main(['--repo',str(tmp_path),'census'])==0
 assert (tmp_path/'docs/Governance/Repository_Census.md').exists()
 assert (tmp_path/'docs/Governance/repository-census.json').exists()

@pytest.mark.parametrize(
    ("arguments", "expected_mode"),
    [
        ([], ExecutionMode.GENERATE),
        (["--mode", "generate"], ExecutionMode.GENERATE),
        (["--mode", "check"], ExecutionMode.CHECK),
        (["--mode", "ci"], ExecutionMode.CI),
    ],
)
def test_cli_builds_context_with_execution_policy(
    tmp_path,
    monkeypatch,
    arguments,
    expected_mode,
):
    captured = {}
    original_build_context = governance.build_context

    def capture_build_context(
        repo,
        cfg,
        execution_mode,
        execution_policy,
    ):
        captured["execution_mode"] = execution_mode
        captured["execution_policy"] = execution_policy
        return original_build_context(
            repo,
            cfg,
            execution_mode,
            execution_policy,
        )

    monkeypatch.setattr(
        governance,
        "build_context",
        capture_build_context,
    )

    assert main(
        [
            "--repo",
            str(tmp_path),
            *arguments,
            "plugins",
        ]
    ) == 0

    assert captured["execution_mode"] is expected_mode
    assert captured["execution_policy"] == ExecutionPolicy.from_mode(
        expected_mode
    )


@pytest.mark.parametrize(
    ("mode", "reports_expected"),
    [
        ("generate", True),
        ("check", False),
        ("ci", False),
    ],
)
def test_census_report_generation_follows_execution_policy(
    tmp_path,
    capsys,
    mode,
    reports_expected,
):
    (tmp_path / "README.md").write_text(
        "# Demo\nEnough\nLines\nFor\nThe\nRule\nHere\nNow\n"
    )

    exit_code = main(
        [
            "--repo",
            str(tmp_path),
            "--mode",
            mode,
            "census",
        ]
    )

    output = capsys.readouterr().out
    markdown_path = (
        tmp_path
        / "docs"
        / "Governance"
        / "Repository_Census.md"
    )
    json_path = (
        tmp_path
        / "docs"
        / "Governance"
        / "repository-census.json"
    )

    assert exit_code == 0
    assert markdown_path.exists() is reports_expected
    assert json_path.exists() is reports_expected

    if reports_expected:
        assert "markdown:" in output
        assert "json:" in output
    else:
        assert "markdown:" not in output
        assert "json:" not in output


def inventory_with_severity(severity: str) -> Inventory:
    issue = Issue(
        rule_id="DGT-TEST-001",
        severity=severity,
        message="Synthetic test finding",
        path="README.md",
    )

    return Inventory(
        root=".",
        files=[],
        issues=[issue],
        statistics={
            "file_count": 0,
            "total_size_bytes": 0,
            "text_file_count": 0,
            "categories": {},
            "domains": {},
            "severities": {
                severity: 1,
            },
            "finding_count": 1,
        },
    )

@pytest.mark.parametrize(
    ("mode", "expected_exit_code"),
    [
        ("generate", 0),
        ("check", 3),
        ("ci", 3),
    ],
)
def test_census_default_threshold_follows_execution_policy(
    tmp_path,
    monkeypatch,
    mode,
    expected_exit_code,
):
    monkeypatch.setattr(
        governance,
        "run_census",
        lambda ctx: inventory_with_severity("LOW"),
    )

    assert main(
        [
            "--repo",
            str(tmp_path),
            "--mode",
            mode,
            "census",
        ]
    ) == expected_exit_code


@pytest.mark.parametrize(
    ("threshold", "severity", "expected_exit_code"),
    [
        ("none", "HIGH", 0),
        ("medium", "LOW", 0),
        ("medium", "MEDIUM", 3),
        ("medium", "HIGH", 3),
        ("high", "LOW", 0),
        ("high", "MEDIUM", 0),
        ("high", "HIGH", 3),
    ],
)
def test_census_fail_on_overrides_execution_policy(
    tmp_path,
    monkeypatch,
    threshold,
    severity,
    expected_exit_code,
):
    monkeypatch.setattr(
        governance,
        "run_census",
        lambda ctx: inventory_with_severity(severity),
    )

    assert main(
        [
            "--repo",
            str(tmp_path),
            "--mode",
            "check",
            "census",
            "--fail-on",
            threshold,
        ]
    ) == expected_exit_code
