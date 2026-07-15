#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import ast
import json
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "PROJECT_MANIFEST.md"

EXCLUDED_PARTS = {
    ".git",
    ".gradle",
    ".idea",
    ".logs",
    ".pytest_cache",
    ".run",
    ".venv",
    "__pycache__",
    "build",
    "node_modules",
}

SOURCE_SUFFIXES = {
    ".py",
    ".kt",
    ".kts",
    ".json",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".sh",
}

SENSITIVE_NAMES = {
    ".env",
    "local.properties",
    "gradle.properties",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_allowed(path: Path) -> bool:
    relative = path.relative_to(ROOT)

    if any(
        part in EXCLUDED_PARTS
        for part in relative.parts
    ):
        return False

    if path.name in SENSITIVE_NAMES:
        return False

    if path.name.endswith(
        (
            ".db",
            ".db-shm",
            ".db-wal",
            ".pid",
            ".log",
            ".backup",
        )
    ):
        return False

    return (
        path.is_file()
        and path.suffix in SOURCE_SUFFIXES
    )


def project_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if is_allowed(path)
    )


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        return result.stdout.strip()
    except Exception:
        return "non disponibile"


def tree_lines(
    files: list[Path],
) -> list[str]:
    allowed_roots = {
        "android",
        "core-engine",
        "docs",
        "gateway",
        "scripts",
    }

    result = []

    for path in files:
        relative = path.relative_to(ROOT)

        if (
            relative.parts
            and relative.parts[0]
            in allowed_roots
        ):
            result.append(str(relative))

    return result


def python_symbols(
    path: Path,
) -> dict[str, list[str]]:
    result = {
        "classes": [],
        "functions": [],
    }

    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        return result

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)
        elif isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            result["functions"].append(
                node.name
            )

    return result


def kotlin_symbols(
    text: str,
) -> dict[str, list[str]]:
    return {
        "classes": sorted(
            set(
                re.findall(
                    r"\b(?:data\s+)?class\s+"
                    r"([A-Za-z_]\w*)",
                    text,
                )
            )
        ),
        "objects": sorted(
            set(
                re.findall(
                    r"\bobject\s+"
                    r"([A-Za-z_]\w*)",
                    text,
                )
            )
        ),
        "functions": sorted(
            set(
                re.findall(
                    r"\bfun\s+"
                    r"([A-Za-z_]\w*)\s*\(",
                    text,
                )
            )
        ),
    }


def fastapi_routes(
    files: list[Path],
) -> list[tuple[str, str, str]]:
    pattern = re.compile(
        r'@app\.(get|post|put|patch|delete)'
        r'\(\s*["\']([^"\']+)["\']'
        r'\s*\)\s*'
        r'(?:async\s+)?def\s+([A-Za-z_]\w*)',
        re.MULTILINE,
    )

    routes = []

    for path in files:
        if path.suffix != ".py":
            continue

        try:
            text = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            continue

        for method, route, function in (
            pattern.findall(text)
        ):
            routes.append(
                (
                    method.upper(),
                    route,
                    function,
                )
            )

    return sorted(
        routes,
        key=lambda item: (
            item[1],
            item[0],
        ),
    )


def mqtt_topics(
    files: list[Path],
) -> list[str]:
    patterns = (
        re.compile(
            r'["\']'
            r'(domoticsai/[^"\']+)'
            r'["\']'
        ),
        re.compile(
            r'["\']'
            r'(zara/[^"\']+)'
            r'["\']'
        ),
    )

    topics = set()

    for path in files:
        if path.suffix not in {
            ".py",
            ".kt",
            ".json",
            ".md",
        }:
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            continue

        for pattern in patterns:
            for match in pattern.findall(text):
                value = match.strip()

                if len(value) <= 180:
                    topics.add(value)

    return sorted(topics)


def dependency_files(
    files: list[Path],
) -> list[Path]:
    names = {
        "pyproject.toml",
        "requirements.txt",
        "build.gradle.kts",
        "settings.gradle.kts",
        "package.json",
    }

    return [
        path
        for path in files
        if path.name in names
    ]


def main() -> int:
    files = project_files()
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        "# DomoticsAI — Project Manifest",
        "",
        f"Generato automaticamente: `{utc_now_iso()}`",
        "",
        "> Non modificare manualmente questo file. "
        "Rigenerarlo con "
        "`python3 scripts/generate-project-manifest.py`.",
        "",
        "## Repository",
        "",
        f"- Branch: `{git_output('branch', '--show-current')}`",
        f"- Commit: `{git_output('rev-parse', '--short', 'HEAD')}`",
        f"- Stato: `{git_output('status', '--short') or 'clean'}`",
        "",
        "## Architettura generale",
        "",
        "```text",
        "Android App",
        "  ↓ REST / MQTT / SSE",
        "Core Engine",
        "  ├── Digital Twin",
        "  ├── Derived domains",
        "  ├── House Knowledge Engine",
        "  ├── House Context Engine",
        "  ├── Command Manager",
        "  └── SQLite persistence",
        "  ↓ MQTT",
        "Gateway Node-RED",
        "  ↓",
        "Dispositivi e Node-RED di produzione",
        "```",
        "",
        "## Struttura file",
        "",
        "```text",
    ]

    lines.extend(tree_lines(files))
    lines.extend(
        [
            "```",
            "",
            "## Endpoint Core Engine",
            "",
            "| Metodo | Endpoint | Funzione |",
            "|---|---|---|",
        ]
    )

    routes = fastapi_routes(files)

    for method, route, function in routes:
        lines.append(
            f"| `{method}` | `{route}` | "
            f"`{function}` |"
        )

    lines.extend(
        [
            "",
            "## Moduli Python",
            "",
        ]
    )

    for path in files:
        if path.suffix != ".py":
            continue

        symbols = python_symbols(path)

        if not any(symbols.values()):
            continue

        relative = path.relative_to(ROOT)
        lines.append(f"### `{relative}`")
        lines.append("")

        if symbols["classes"]:
            lines.append(
                "- Classi: "
                + ", ".join(
                    f"`{name}`"
                    for name in symbols[
                        "classes"
                    ]
                )
            )

        if symbols["functions"]:
            lines.append(
                "- Funzioni: "
                + ", ".join(
                    f"`{name}`"
                    for name in symbols[
                        "functions"
                    ]
                )
            )

        lines.append("")

    lines.extend(
        [
            "## Moduli Kotlin / Android",
            "",
        ]
    )

    for path in files:
        if path.suffix not in {
            ".kt",
            ".kts",
        }:
            continue

        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        symbols = kotlin_symbols(text)

        if not any(symbols.values()):
            continue

        relative = path.relative_to(ROOT)
        lines.append(f"### `{relative}`")
        lines.append("")

        for category in (
            "classes",
            "objects",
            "functions",
        ):
            values = symbols[category]

            if values:
                lines.append(
                    f"- {category.capitalize()}: "
                    + ", ".join(
                        f"`{name}`"
                        for name in values
                    )
                )

        lines.append("")

    lines.extend(
        [
            "## Topic MQTT rilevati",
            "",
        ]
    )

    topics = mqtt_topics(files)

    if topics:
        for topic in topics:
            lines.append(f"- `{topic}`")
    else:
        lines.append("- Nessun topic rilevato.")

    lines.extend(
        [
            "",
            "## File delle dipendenze",
            "",
        ]
    )

    for path in dependency_files(files):
        lines.append(
            f"- `{path.relative_to(ROOT)}`"
        )

    lines.extend(
        [
            "",
            "## Test",
            "",
        ]
    )

    test_files = [
        path
        for path in files
        if (
            path.name.startswith("test_")
            or "/test/" in str(path)
            or "/tests/" in str(path)
        )
    ]

    for path in test_files:
        lines.append(
            f"- `{path.relative_to(ROOT)}`"
        )

    lines.extend(
        [
            "",
            "## Vincoli architetturali",
            "",
            "- Funzionamento locale su Raspberry Pi.",
            "- Client Android su smartphone.",
            "- Nessun cloud obbligatorio.",
            "- Nessun abbonamento obbligatorio.",
            "- Nessuna dipendenza con licenza commerciale obbligatoria.",
            "- Preferenza per licenze MIT, BSD e Apache-2.0.",
            "- SQLite locale con WAL e connessione centralizzata.",
            "- Node-RED di produzione invariato fino alla migrazione finale.",
            "",
        ]
    )

    OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"OK: manifest generato in {OUTPUT}"
    )
    print(f"File indicizzati: {len(files)}")
    print(f"Endpoint rilevati: {len(routes)}")
    print(f"Topic MQTT rilevati: {len(topics)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
