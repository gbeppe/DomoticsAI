from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .collectors import (
    kotlin_symbols,
    python_symbols,
    relative_path,
)


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def _file_index(
    files: list[Path],
) -> list[str]:
    lines = [
        "## File indicizzati",
        "",
        "```text",
    ]

    lines.extend(
        relative_path(path)
        for path in files
    )

    lines.extend(
        [
            "```",
            "",
        ]
    )

    return lines


def _python_index(
    files: list[Path],
) -> list[str]:
    lines = [
        "## Moduli Python",
        "",
    ]

    for path in files:
        if path.suffix != ".py":
            continue

        symbols = python_symbols(path)

        if not any(symbols.values()):
            continue

        lines.extend(
            [
                f"### `{relative_path(path)}`",
                "",
            ]
        )

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

    return lines


def _kotlin_index(
    files: list[Path],
) -> list[str]:
    lines = [
        "## Moduli Kotlin / Android",
        "",
    ]

    for path in files:
        if path.suffix not in {
            ".kt",
            ".kts",
        }:
            continue

        symbols = kotlin_symbols(path)

        if not any(symbols.values()):
            continue

        lines.extend(
            [
                f"### `{relative_path(path)}`",
                "",
            ]
        )

        labels = {
            "classes": "Classi",
            "objects": "Object",
            "functions": "Funzioni",
        }

        for key, label in labels.items():
            values = symbols[key]

            if values:
                lines.append(
                    f"- {label}: "
                    + ", ".join(
                        f"`{value}`"
                        for value in values
                    )
                )

        lines.append("")

    return lines


def _routes_index(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## Endpoint FastAPI",
        "",
        "| Metodo | Endpoint | Handler |",
        "|---|---|---|",
    ]

    for route in data["routes"]:
        lines.append(
            f"| `{route['method']}` "
            f"| `{route['path']}` "
            f"| `{route['function']}` |"
        )

    lines.append("")

    return lines


def _topics_index(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## Topic MQTT rilevati",
        "",
    ]

    for topic in data["topics"]:
        lines.append(
            f"- `{topic}`"
        )

    if not data["topics"]:
        lines.append(
            "- Nessun topic rilevato."
        )

    lines.append("")

    return lines


def _dependencies_index(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## File delle dipendenze",
        "",
    ]

    for path in data[
        "dependency_files"
    ]:
        lines.append(
            f"- `{relative_path(path)}`"
        )

    lines.append("")

    return lines


def _tests_index(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## Test",
        "",
    ]

    for path in data["test_files"]:
        lines.append(
            f"- `{relative_path(path)}`"
        )

    lines.append("")

    return lines


def _documentation_index(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## Documentazione",
        "",
    ]

    for path in data[
        "documentation_files"
    ]:
        if path.name in {
            "PROJECT_MANIFEST.md",
            "PROJECT_INDEX.md",
        }:
            continue

        lines.append(
            f"- `{relative_path(path)}`"
        )

    lines.append("")

    return lines


def _statistics(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## Statistiche",
        "",
        "| Estensione | File |",
        "|---|---:|",
    ]

    for suffix, count in (
        data["statistics"].items()
    ):
        lines.append(
            f"| `{suffix}` | `{count}` |"
        )

    lines.extend(
        [
            "",
            f"- Totale file indicizzati: "
            f"`{len(data['files'])}`",
            f"- Endpoint: "
            f"`{len(data['routes'])}`",
            f"- Topic MQTT: "
            f"`{len(data['topics'])}`",
            f"- File di test: "
            f"`{len(data['test_files'])}`",
            "",
        ]
    )

    return lines


def render_index(
    data: dict[str, Any],
) -> str:
    lines = [
        "# DomoticsAI — Project Index",
        "",
        f"Generato automaticamente: "
        f"`{utc_now_iso()}`",
        "",
        "> Indice tecnico completo del repository. "
        "Per la visione architetturale consultare "
        "`PROJECT_MANIFEST.md`.",
        "",
    ]

    sections = (
        _statistics(data),
        _routes_index(data),
        _python_index(
            data["indexed_files"]
        ),
        _kotlin_index(
            data["indexed_files"]
        ),
        _topics_index(data),
        _dependencies_index(data),
        _tests_index(data),
        _documentation_index(data),
        _file_index(
            data["indexed_files"]
        ),
    )

    for section in sections:
        lines.extend(section)

    return "\n".join(lines)
