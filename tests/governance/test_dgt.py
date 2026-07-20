from pathlib import Path

import pytest

import tools.governance.governance as governance
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
