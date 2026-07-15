from __future__ import annotations

from .collectors import collect_project
from .config import (
    DEPENDENCY_OUTPUT,
    INDEX_OUTPUT,
    MANIFEST_OUTPUT,
)
from .dependencies import (
    collect_all_dependencies,
)
from .render_dependencies import (
    render_dependency_inventory,
)
from .render_index import render_index
from .render_manifest import render_manifest


def main() -> int:
    data = collect_project()
    dependencies = (
        collect_all_dependencies()
    )

    MANIFEST_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    MANIFEST_OUTPUT.write_text(
        render_manifest(data),
        encoding="utf-8",
    )

    INDEX_OUTPUT.write_text(
        render_index(data),
        encoding="utf-8",
    )

    DEPENDENCY_OUTPUT.write_text(
        render_dependency_inventory(
            dependencies
        ),
        encoding="utf-8",
    )

    print(
        "OK: documentazione progetto generata:"
    )

    for path in (
        MANIFEST_OUTPUT,
        INDEX_OUTPUT,
        DEPENDENCY_OUTPUT,
    ):
        print(f"  {path}")

    print()
    print(
        "File indicizzati:",
        len(data["files"]),
    )
    print(
        "Endpoint unici:",
        len(data["routes"]),
    )
    print(
        "Topic MQTT:",
        len(data["topics"]),
    )
    print(
        "Test:",
        len(data["test_files"]),
    )
    print(
        "Dipendenze dichiarate:",
        len(dependencies),
    )

    return 0
