from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.repository_census.census import analyze, load_config, scan

def cfg(tmp_path: Path) -> Path:
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"ignored_directories":["node_modules"],"ignored_files":[],"domain_rules":[["docs/","Documentation","Documentation"],["src/","Core","Core"]]}), encoding="utf-8")
    return p

def test_scan_and_broken_link(tmp_path: Path):
    (tmp_path / "docs").mkdir(); (tmp_path / "src").mkdir()
    (tmp_path / "docs/README.md").write_text("# Test\n\nSee [missing](missing.md). This document is long enough for analysis.", encoding="utf-8")
    (tmp_path / "src/main.py").write_text("print('ok')\n", encoding="utf-8")
    items = scan(tmp_path, load_config(cfg(tmp_path)))
    by = {i.path:i for i in items}
    assert by["docs/README.md"].category == "Documentation"
    assert by["src/main.py"].category == "Source Code"
    assert any(i.rule == "BROKEN_LOCAL_LINK" for i in analyze(tmp_path, items))
