from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
import ast
import re
import subprocess

from .config import (
    DEPENDENCY_FILE_NAMES,
    EXCLUDED_PARTS,
    INDEXED_ROOTS,
    ROOT,
    SENSITIVE_NAMES,
    SENSITIVE_SUFFIXES,
    SOURCE_SUFFIXES,
)


def is_allowed(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False

    if any(
        part in EXCLUDED_PARTS
        for part in relative.parts
    ):
        return False

    if path.name in SENSITIVE_NAMES:
        return False

    if path.name.endswith(
        SENSITIVE_SUFFIXES
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


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def indexed_files(
    files: list[Path],
) -> list[Path]:
    result: list[Path] = []

    for path in files:
        relative = path.relative_to(ROOT)

        if (
            relative.parts
            and relative.parts[0]
            in INDEXED_ROOTS
        ):
            result.append(path)

    return result


def run_git(*args: str) -> str:
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
        return ""


def git_summary() -> dict[str, Any]:
    status = run_git(
        "status",
        "--porcelain",
    )

    counters = Counter()

    for line in status.splitlines():
        if not line:
            continue

        code = line[:2]

        if "?" in code:
            counters["untracked"] += 1

        if "M" in code:
            counters["modified"] += 1

        if "A" in code:
            counters["added"] += 1

        if "D" in code:
            counters["deleted"] += 1

        if "R" in code:
            counters["renamed"] += 1

    dirty_count = sum(counters.values())

    return {
        "branch": (
            run_git(
                "branch",
                "--show-current",
            )
            or "non disponibile"
        ),
        "commit": (
            run_git(
                "rev-parse",
                "--short",
                "HEAD",
            )
            or "non disponibile"
        ),
        "clean": dirty_count == 0,
        "modified": counters["modified"],
        "added": counters["added"],
        "deleted": counters["deleted"],
        "renamed": counters["renamed"],
        "untracked": counters["untracked"],
    }


def python_symbols(
    path: Path,
) -> dict[str, list[str]]:
    result = {
        "classes": [],
        "functions": [],
    }

    try:
        tree = ast.parse(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return result

    for node in tree.body:
        if isinstance(
            node,
            ast.ClassDef,
        ):
            result["classes"].append(
                node.name
            )

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
    path: Path,
) -> dict[str, list[str]]:
    try:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return {
            "classes": [],
            "objects": [],
            "functions": [],
        }

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
) -> list[dict[str, str]]:
    pattern = re.compile(
        r'@app\.(get|post|put|patch|delete)'
        r'\(\s*["\']([^"\']+)["\']'
        r'\s*\)\s*'
        r'(?:async\s+)?def\s+'
        r'([A-Za-z_]\w*)',
        re.MULTILINE,
    )

    routes: set[
        tuple[str, str, str]
    ] = set()

    for path in files:
        if path.suffix != ".py":
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            continue

        for method, route, function in (
            pattern.findall(text)
        ):
            routes.add(
                (
                    method.upper(),
                    route,
                    function,
                )
            )

    return [
        {
            "method": method,
            "path": route,
            "function": function,
        }
        for method, route, function
        in sorted(
            routes,
            key=lambda item: (
                item[1],
                item[0],
                item[2],
            ),
        )
    ]


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

    topics: set[str] = set()

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
            for match in pattern.findall(
                text
            ):
                value = match.strip()

                if len(value) <= 180:
                    topics.add(value)

    return sorted(topics)


def dependency_files(
    files: list[Path],
) -> list[Path]:
    return sorted(
        path
        for path in files
        if path.name
        in DEPENDENCY_FILE_NAMES
    )


def test_files(
    files: list[Path],
) -> list[Path]:
    return sorted(
        path
        for path in files
        if (
            path.name.startswith(
                "test_"
            )
            or "/test/" in str(path)
            or "/tests/" in str(path)
        )
    )


def documentation_files(
    files: list[Path],
) -> list[Path]:
    return sorted(
        path
        for path in files
        if (
            path.relative_to(ROOT).parts
            and path.relative_to(ROOT)
                .parts[0]
            == "docs"
        )
    )


def source_statistics(
    files: list[Path],
) -> dict[str, int]:
    result = Counter()

    for path in files:
        result[
            path.suffix.lstrip(".")
            or "other"
        ] += 1

    return dict(
        sorted(result.items())
    )


def collect_project() -> dict[str, Any]:
    files = project_files()

    return {
        "files": files,
        "indexed_files": indexed_files(
            files
        ),
        "git": git_summary(),
        "routes": fastapi_routes(
            files
        ),
        "topics": mqtt_topics(
            files
        ),
        "dependency_files":
            dependency_files(files),
        "test_files": test_files(
            files
        ),
        "documentation_files":
            documentation_files(files),
        "statistics":
            source_statistics(files),
    }
