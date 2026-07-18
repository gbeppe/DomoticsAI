#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

CENSUS="tools/repository_census/census.py"
CONFIG="tools/repository_census/config.json"

if [[ ! -f "$CENSUS" || ! -f "$CONFIG" ]]; then
  echo "Errore: Repository Census v0.1 non trovato."
  exit 1
fi

cp "$CENSUS" "${CENSUS}.backup-v0.1"
cp "$CONFIG" "${CONFIG}.backup-v0.1"

python3 - <<'PY'
from pathlib import Path
import json

config_path = Path("tools/repository_census/config.json")
config = json.loads(config_path.read_text(encoding="utf-8"))

ignored_dirs = set(config.get("ignored_directories", []))
ignored_dirs.update({".captures", ".logs", ".run"})
config["ignored_directories"] = sorted(ignored_dirs)

generated = set(config.get("generated_path_fragments", []))
generated.update({"/.egg-info/", "/egg-info/"})
config["generated_path_fragments"] = sorted(generated)

rules = config.get("domain_rules", [])
new_rules = [
    {"prefix": "Project/", "domain": "Project Governance", "owner": "Architecture"},
    {"prefix": "assets/", "domain": "Assets", "owner": "Design"},
    {"prefix": "design/", "domain": "Design", "owner": "Design"}
]
existing = {r["prefix"] for r in rules}
for rule in reversed(new_rules):
    if rule["prefix"] not in existing:
        rules.insert(0, rule)
config["domain_rules"] = rules

config_path.write_text(
    json.dumps(config, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
PY

python3 - <<'PY'
from pathlib import Path

path = Path("tools/repository_census/census.py")
text = path.read_text(encoding="utf-8")

text = text.replace('VERSION = "0.1.0"', 'VERSION = "0.2.0"')

old = """def classify(path: Path, relative: str) -> str:
    suffix = path.suffix.lower()
    name_lower = path.name.lower()
    parts_lower = {part.lower() for part in path.parts}

    if "test" in parts_lower or "tests" in parts_lower or re.search(
        r"(^test_|_test\\.|test\\.)", name_lower
    ):
        return "Test"
    if relative.startswith("docs/") or suffix in DOCUMENT_EXTENSIONS:
"""
new = """def classify(path: Path, relative: str) -> str:
    suffix = path.suffix.lower()
    name_lower = path.name.lower()
    parts_lower = {part.lower() for part in path.parts}

    if any(part.endswith(".egg-info") for part in path.parts):
        return "Generated Artifact"
    if "test" in parts_lower or "tests" in parts_lower or re.search(
        r"(^test_|_test\\.|test\\.)", name_lower
    ):
        return "Test"
    if relative.startswith("docs/") or suffix in DOCUMENT_EXTENSIONS:
"""
if old not in text:
    raise SystemExit("Patch classify non applicata.")
text = text.replace(old, new)

old = """    for dirname, group in sorted(tracked_dirs.items()):
        if dirname.startswith("."):
            continue
        if not any(
            entry.path == f"{dirname}/README.md"
            or entry.path == f"{dirname}/README.rst"
            for entry in group
        ):
"""
new = """    for dirname, group in sorted(tracked_dirs.items()):
        if dirname.startswith("."):
            continue

        top_path = root / dirname
        if not top_path.is_dir():
            continue

        if not any(
            entry.path == f"{dirname}/README.md"
            or entry.path == f"{dirname}/README.rst"
            for entry in group
        ):
"""
if old not in text:
    raise SystemExit("Patch README rule non applicata.")
text = text.replace(old, new)

old = """    documents = [
        item for item in items
        if item.category in {"Documentation", "ADR"}
    ]
"""
new = """    documents = [
        item for item in items
        if item.category in {"Documentation", "ADR"}
        and not item.generated
    ]
"""
if old not in text:
    raise SystemExit("Patch document statistics non applicata.")
text = text.replace(old, new)

marker = """def pct(part: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{part * 100 / total:.1f}%"
"""
replacement = """def pct(part: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{part * 100 / total:.1f}%"


def repository_health(items: list[Item], issues: list[Issue]) -> dict[str, int]:
    high = sum(1 for issue in issues if issue.severity == "HIGH")
    medium = sum(1 for issue in issues if issue.severity == "MEDIUM")
    unclassified = sum(1 for item in items if item.domain == "Unclassified")
    tests = sum(1 for item in items if item.category == "Test")
    source = sum(1 for item in items if item.category == "Source Code")

    documentation = max(0, round(100 - (high * 8) - (medium * 2) - (unclassified * 2)))
    architecture = max(0, round(100 - (unclassified * 3) - (high * 4)))
    testing = min(100, round((tests / source) * 400) if source else 100)
    governance = round((documentation + architecture + testing) / 3)
    registry = 100 if any(item.domain == "Registry" for item in items) else 0

    return {
        "Architecture": architecture,
        "Documentation": documentation,
        "Registry": registry,
        "Testing": testing,
        "Governance": governance,
    }
"""
if marker not in text:
    raise SystemExit("Patch health helper non applicata.")
text = text.replace(marker, replacement)

old = """    categories = Counter(item.category for item in items)
    domains = Counter(item.domain for item in items)
    statuses = Counter(item.status for item in items)
    actions = Counter(item.action for item in items)
    severities = Counter(issue.severity for issue in issues)
"""
new = """    categories = Counter(item.category for item in items)
    domains = Counter(item.domain for item in items)
    statuses = Counter(item.status for item in items)
    actions = Counter(item.action for item in items)
    severities = Counter(issue.severity for issue in issues)
    health = repository_health(items, issues)
"""
if old not in text:
    raise SystemExit("Patch health summary non applicata.")
text = text.replace(old, new)

old = """        f"- Issues: **{len(issues)}** "
        f"(HIGH {severities['HIGH']}, MEDIUM {severities['MEDIUM']}, LOW {severities['LOW']})",
        "",
        "## Files by category",
"""
new = """        f"- Issues: **{len(issues)}** "
        f"(HIGH {severities['HIGH']}, MEDIUM {severities['MEDIUM']}, LOW {severities['LOW']})",
        "",
        "## Repository Health",
        "",
        "| Area | Score |",
        "|---|---:|",
        *[f"| {name} | {score}% |" for name, score in health.items()],
        "",
        "> Structural governance indicators; they are not code coverage metrics.",
        "",
        "## Files by category",
"""
if old not in text:
    raise SystemExit("Patch Repository Health output non applicata.")
text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
PY

cat > tests/tools/test_repository_census_v0_2.py <<'PY'
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.repository_census.census import analyze, classify, load_config, scan


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "ignored_directories": [".captures", ".logs", ".run"],
                "ignored_files": [],
                "generated_path_fragments": ["/.egg-info/"],
                "domain_rules": [
                    {"prefix": "Project/", "domain": "Project Governance", "owner": "Architecture"},
                    {"prefix": "assets/", "domain": "Assets", "owner": "Design"},
                    {"prefix": "design/", "domain": "Design", "owner": "Design"}
                ]
            }
        ),
        encoding="utf-8",
    )
    return path


def test_egg_info_is_generated_artifact(tmp_path: Path) -> None:
    directory = tmp_path / "pkg.egg-info"
    directory.mkdir()
    file = directory / "top_level.txt"
    file.write_text("pkg\n", encoding="utf-8")
    assert classify(file, "pkg.egg-info/top_level.txt") == "Generated Artifact"


def test_runtime_directories_are_ignored(tmp_path: Path) -> None:
    (tmp_path / ".logs").mkdir()
    (tmp_path / ".logs" / "core.log").write_text("runtime\n", encoding="utf-8")
    assert scan(tmp_path, load_config(_config(tmp_path))) == []


def test_project_assets_design_domains(tmp_path: Path) -> None:
    for dirname in ("Project", "assets", "design"):
        (tmp_path / dirname).mkdir()

    (tmp_path / "Project" / "Roadmap.md").write_text("# Roadmap\n" * 20, encoding="utf-8")
    (tmp_path / "assets" / "README.md").write_text("# Assets\n" * 20, encoding="utf-8")
    (tmp_path / "design" / "README.md").write_text("# Design\n" * 20, encoding="utf-8")

    domains = {
        item.path: item.domain
        for item in scan(tmp_path, load_config(_config(tmp_path)))
    }
    assert domains["Project/Roadmap.md"] == "Project Governance"
    assert domains["assets/README.md"] == "Assets"
    assert domains["design/README.md"] == "Design"


def test_root_file_does_not_trigger_missing_readme(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Root\n" * 20, encoding="utf-8")
    config = load_config(_config(tmp_path))
    items = scan(tmp_path, config)
    issues = analyze(tmp_path, items)
    assert not any(
        issue.rule == "MISSING_TOP_LEVEL_README" and issue.path == "README.md"
        for issue in issues
    )
PY

python3 -m py_compile tools/repository_census/census.py

if command -v pytest >/dev/null 2>&1; then
  pytest -q tests/tools/test_repository_census.py tests/tools/test_repository_census_v0_2.py
else
  echo "pytest non disponibile: test automatici non eseguiti."
fi

./scripts/run-repository-census.sh

echo
echo "Repository Census v0.2 installato."
echo
sed -n '1,120p' docs/Documentation/DOCUMENTATION_CENSUS.md
echo
git status --short -- \
  tools/repository_census \
  tests/tools \
  scripts/run-repository-census.sh \
  docs/Documentation
