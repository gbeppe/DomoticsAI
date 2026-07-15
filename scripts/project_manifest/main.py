from __future__ import annotations

from .collectors import collect_project
from .config import (
    INDEX_OUTPUT,
    MANIFEST_OUTPUT,
)
from .render_index import render_index
from .render_manifest import render_manifest


def main() -> int:
    data = collect_project()

    MANIFEST_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = render_manifest(data)
    index = render_index(data)

    MANIFEST_OUTPUT.write_text(
        manifest,
        encoding="utf-8",
    )

    INDEX_OUTPUT.write_text(
        index,
        encoding="utf-8",
    )

    print(
        "OK: Project Manifest v2 generato:"
    )
    print(
        f"  {MANIFEST_OUTPUT}"
    )
    print(
        f"  {INDEX_OUTPUT}"
    )
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

    return 0
