#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-$(pwd)}"
cd "$ROOT"
mkdir -p tools/repository_census tests/tools docs/Documentation scripts

cat > tools/repository_census/config.json <<'JSON'
{
  "ignored_directories": [".git", ".gradle", ".idea", ".pytest_cache", ".venv", "venv", "__pycache__", "build", "dist", "node_modules"],
  "ignored_files": [".DS_Store"],
  "domain_rules": [
    ["core-engine/", "Core Engine", "Core"],
    ["android/", "Android", "Android"],
    ["gateway/", "Gateway", "Gateway"],
    ["nodered/", "Gateway", "Gateway"],
    ["config/registry/", "Registry", "Registry"],
    ["docs/Registry/", "Registry", "Registry"],
    ["docs/ADR/", "Architecture", "Architecture"],
    ["docs/Architecture/", "Architecture", "Architecture"],
    ["docs/AI/", "AI", "AI"],
    ["docs/MQTT/", "Contracts", "Architecture"],
    ["docs/NodeRED/", "Gateway", "Gateway"],
    ["docs/", "Documentation", "Documentation"],
    ["scripts/", "DevOps", "DevOps"],
    ["tools/", "Tooling", "Architecture"],
    ["tests/", "Testing", "QA"],
    ["test/", "Testing", "QA"],
    ["config/", "Configuration", "Architecture"]
  ]
}
JSON

cat > tools/repository_census/census.py <<'PY'
#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
DOC_EXT = {".md", ".rst", ".adoc", ".txt", ".pdf"}
CFG_EXT = {".yaml", ".yml", ".json", ".toml", ".ini", ".conf", ".properties", ".env"}
SRC_EXT = {".py", ".kt", ".kts", ".java", ".js", ".ts", ".tsx", ".jsx", ".c", ".cpp", ".h", ".hpp", ".go", ".rs"}
SCRIPT_EXT = {".sh", ".bash", ".zsh", ".ps1"}

@dataclass(frozen=True)
class Item:
    path: str; category: str; domain: str; owner: str; status: str; action: str
    priority: str; size_bytes: int; modified_utc: str; sha256_12: str

@dataclass(frozen=True)
class Issue:
    severity: str; rule: str; path: str; message: str

def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def ignored(path: Path, root: Path, cfg: dict[str, Any]) -> bool:
    rel = path.relative_to(root)
    return any(p in set(cfg["ignored_directories"]) for p in rel.parts[:-1]) or path.name in set(cfg["ignored_files"])

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:12]

def classify(path: Path, rel: str) -> str:
    s, n = path.suffix.lower(), path.name.lower()
    parts = {p.lower() for p in path.parts}
    if "test" in parts or "tests" in parts or re.search(r"(^test_|_test\.)", n): return "Test"
    if rel.startswith("docs/ADR/") or re.match(r"ADR-\d+", path.name, re.I): return "ADR"
    if rel.startswith("docs/") or s in DOC_EXT: return "Documentation"
    if s in SCRIPT_EXT or os.access(path, os.X_OK): return "Script"
    if s in CFG_EXT or path.name in {"Dockerfile", "Makefile", "settings.gradle", "settings.gradle.kts"}: return "Configuration"
    if s in SRC_EXT: return "Source Code"
    return "Other"

def domain_owner(rel: str, cfg: dict[str, Any]) -> tuple[str, str]:
    for prefix, domain, owner in cfg["domain_rules"]:
        if rel.startswith(prefix): return domain, owner
    return ("Repository", "Architecture") if "/" not in rel else ("Unclassified", "Architecture")

def status_action(path: Path, rel: str, category: str) -> tuple[str, str, str]:
    low = rel.lower(); name = path.name.lower()
    if "/archive/" in f"/{low}/": return "ARCHIVED", "KEEP", "LOW"
    if any(x in name for x in ("deprecated", "obsolete", "legacy")): return "DEPRECATED", "ARCHIVE", "MEDIUM"
    if any(x in name for x in ("draft", "todo", "backlog")): return "DRAFT", "UPDATE", "MEDIUM"
    if category in {"Documentation", "ADR"}:
        if path.stat().st_size == 0: return "DRAFT", "UPDATE", "HIGH"
        if name.startswith("readme"): return "ACTIVE", "KEEP", "HIGH"
        return "ACTIVE", "REVIEW", "MEDIUM"
    return "ACTIVE", "KEEP", "LOW"

def scan(root: Path, cfg: dict[str, Any]) -> list[Item]:
    out = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ignored(path, root, cfg): continue
        rel = path.resolve().relative_to(root.resolve()).as_posix()
        cat = classify(path, rel); domain, owner = domain_owner(rel, cfg)
        status, action, priority = status_action(path, rel, cat)
        st = path.stat()
        out.append(Item(rel, cat, domain, owner, status, action, priority, st.st_size,
                        datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(timespec="seconds"), digest(path)))
    return out

def analyze(root: Path, items: list[Item]) -> list[Issue]:
    issues: list[Issue] = []
    tops = defaultdict(list)
    for i in items:
        tops[i.path.split("/", 1)[0]].append(i)
        if i.domain == "Unclassified": issues.append(Issue("MEDIUM", "UNCLASSIFIED_DOMAIN", i.path, "No domain rule matched."))
        if i.category == "Documentation" and Path(i.path).suffix.lower() in {".md", ".rst", ".adoc", ".txt"}:
            p = root / i.path
            try: text = p.read_text(encoding="utf-8")
            except Exception: continue
            if len(text.strip()) < 80: issues.append(Issue("MEDIUM", "THIN_DOCUMENT", i.path, "Document is very short."))
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://", "mailto:", "#")) or "://" in target: continue
                clean = target.split("#", 1)[0]
                if clean and not (p.parent / clean).exists(): issues.append(Issue("HIGH", "BROKEN_LOCAL_LINK", i.path, f"Missing link target: {target}"))
    for top, group in tops.items():
        if top.startswith("."): continue
        if not any(x.path in {f"{top}/README.md", f"{top}/README.rst"} for x in group):
            issues.append(Issue("LOW", "MISSING_TOP_LEVEL_README", top, "Top-level area has no README."))
    return sorted(issues, key=lambda x: ({"HIGH":0,"MEDIUM":1,"LOW":2}.get(x.severity,9), x.rule, x.path))

def git(root: Path, *args: str) -> str:
    try: return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip() or "unknown"
    except Exception: return "unknown"

def render(root: Path, items: list[Item], issues: list[Issue]) -> str:
    cats, doms, stats, acts = map(Counter, ([i.category for i in items], [i.domain for i in items], [i.status for i in items], [i.action for i in items]))
    sev = Counter(i.severity for i in issues)
    docs = [i for i in items if i.category in {"Documentation", "ADR"}]
    lines = [
        "# DomoticsAI — Repository Census", "", "> Generated automatically by WP1 Repository Census v0.1.", "",
        "## Metadata", "", f"- Generated at: `{now()}`", f"- Git branch: `{git(root, 'branch', '--show-current')}`",
        f"- Git commit: `{git(root, 'rev-parse', '--short', 'HEAD')}`", f"- Files inventoried: **{len(items)}**",
        f"- Documentation files: **{len(docs)}**", f"- Findings: **{len(issues)}** (HIGH {sev['HIGH']}, MEDIUM {sev['MEDIUM']}, LOW {sev['LOW']})", ""
    ]
    for title, counter in (("Files by category", cats), ("Files by domain", doms), ("Status", stats), ("Recommended actions", acts)):
        lines += [f"## {title}", "", "| Value | Count |", "|---|---:|"] + [f"| {k} | {v} |" for k,v in sorted(counter.items())] + [""]
    lines += ["## Findings", "", "| Severity | Rule | Path | Finding |", "|---|---|---|---|"]
    lines += [f"| {x.severity} | `{x.rule}` | `{x.path}` | {x.message.replace('|','/')} |" for x in issues] or ["| — | — | — | No findings |"]
    lines += ["", "## Documentation inventory", "", "| Path | Domain | Owner | Status | Action | Priority | Size | Modified UTC | Manual decision |", "|---|---|---|---|---|---|---:|---|---|"]
    lines += [f"| `{i.path}` | {i.domain} | {i.owner} | {i.status} | {i.action} | {i.priority} | {i.size_bytes} | `{i.modified_utc}` |  |" for i in docs]
    lines += ["", "## Interpretation", "", "Automatic classifications are proposals. No file is moved or deleted by this tool.", ""]
    return "\n".join(lines)

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--root", type=Path, default=Path.cwd()); ap.add_argument("--fail-on-high", action="store_true")
    a = ap.parse_args(); root = a.root.resolve(); cfg = load_config(root / "tools/repository_census/config.json")
    items = scan(root, cfg); issues = analyze(root, items)
    out_md = root / "docs/Documentation/DOCUMENTATION_CENSUS.md"; out_json = root / "docs/Documentation/repository-census.json"
    out_md.write_text(render(root, items, issues), encoding="utf-8")
    out_json.write_text(json.dumps({"schemaVersion":"1", "toolVersion":VERSION, "generatedAt":now(), "items":[asdict(i) for i in items], "issues":[asdict(i) for i in issues]}, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    c = Counter(i.severity for i in issues)
    print(f"Repository Census completato: files={len(items)} HIGH={c['HIGH']} MEDIUM={c['MEDIUM']} LOW={c['LOW']}")
    print("Output: docs/Documentation/DOCUMENTATION_CENSUS.md")
    print("Output: docs/Documentation/repository-census.json")
    return 2 if a.fail_on_high and c["HIGH"] else 0

if __name__ == "__main__": raise SystemExit(main())
PY
chmod +x tools/repository_census/census.py

cat > tools/repository_census/README.md <<'MD'
# Repository Census

Genera l'inventario automatico del repository DomoticsAI e individua anomalie documentali di base.

```bash
./scripts/run-repository-census.sh
```

Output:

- `docs/Documentation/DOCUMENTATION_CENSUS.md`
- `docs/Documentation/repository-census.json`

Lo strumento non modifica, sposta o elimina file.
MD

cat > scripts/run-repository-census.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 tools/repository_census/census.py "$@"
SH
chmod +x scripts/run-repository-census.sh

cat > tests/tools/test_repository_census.py <<'PY'
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
PY

python3 -m py_compile tools/repository_census/census.py
if command -v pytest >/dev/null 2>&1; then pytest -q tests/tools/test_repository_census.py; else echo "pytest non disponibile: test saltati"; fi
./scripts/run-repository-census.sh

echo
echo "WP1 Repository Census v0.1 installato."
git status --short -- tools/repository_census tests/tools/test_repository_census.py scripts/run-repository-census.sh docs/Documentation
