from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import re
import tomllib

from .config import ROOT


@dataclass(frozen=True)
class DependencyRecord:
    ecosystem: str
    name: str
    version: str
    scope: str
    source_file: str

    license: str = "DA_VERIFICARE"
    cost_model: str = "DA_VERIFICARE"
    cloud_required: str = "DA_VERIFICARE"
    raspberry_pi: str = "DA_VERIFICARE"

    def sort_key(
        self,
    ) -> tuple[str, str, str]:
        return (
            self.ecosystem.lower(),
            self.name.lower(),
            self.scope.lower(),
        )


def _relative(
    path: Path,
) -> str:
    """
    Restituisce il percorso relativo al repository.

    Se il file non appartiene al repository
    (ad esempio durante i test con tmp_path),
    restituisce semplicemente il nome del file.
    """
    try:
        return str(
            path.relative_to(ROOT)
        )
    except ValueError:
        return path.name


def _split_python_requirement(
    requirement: str,
) -> tuple[str, str]:
    text = requirement.strip()

    # Rimuove environment marker.
    text = text.split(";", 1)[0].strip()

    # Rimuove eventuali extras dal nome,
    # conservando il vincolo di versione.
    match = re.match(
        r"""
        ^
        (?P<name>[A-Za-z0-9_.-]+)
        (?:\[[^\]]+\])?
        (?P<version>.*)
        $
        """,
        text,
        flags=re.VERBOSE,
    )

    if match is None:
        return text, ""

    return (
        match.group("name"),
        match.group("version").strip(),
    )


def collect_python_dependencies(
    path: Path | None = None,
) -> list[DependencyRecord]:
    pyproject = (
        path
        if path is not None
        else ROOT / "core-engine" / "pyproject.toml"
    )

    if not pyproject.exists():
        return []

    data = tomllib.loads(
        pyproject.read_text(
            encoding="utf-8"
        )
    )

    project = data.get(
        "project",
        {},
    )

    result: list[DependencyRecord] = []

    for requirement in project.get(
        "dependencies",
        [],
    ):
        name, version = (
            _split_python_requirement(
                str(requirement)
            )
        )

        result.append(
            DependencyRecord(
                ecosystem="Python",
                name=name,
                version=version or "non vincolata",
                scope="runtime",
                source_file=_relative(
                    pyproject
                ),
            )
        )

    optional = project.get(
        "optional-dependencies",
        {},
    )

    if isinstance(optional, dict):
        for group, requirements in (
            optional.items()
        ):
            for requirement in requirements:
                name, version = (
                    _split_python_requirement(
                        str(requirement)
                    )
                )

                result.append(
                    DependencyRecord(
                        ecosystem="Python",
                        name=name,
                        version=(
                            version
                            or "non vincolata"
                        ),
                        scope=f"optional:{group}",
                        source_file=_relative(
                            pyproject
                        ),
                    )
                )

    return sorted(
        set(result),
        key=DependencyRecord.sort_key,
    )


GRADLE_DEPENDENCY_PATTERN = re.compile(
    r"""
    (?P<scope>
        implementation
        |api
        |compileOnly
        |runtimeOnly
        |testImplementation
        |androidTestImplementation
        |debugImplementation
        |kapt
        |ksp
    )
    \s*\(
    \s*["']
    (?P<coordinate>[^"']+)
    ["']
    \s*\)
    """,
    flags=re.VERBOSE,
)


GRADLE_CATALOG_PATTERN = re.compile(
    r"""
    (?P<scope>
        implementation
        |api
        |compileOnly
        |runtimeOnly
        |testImplementation
        |androidTestImplementation
        |debugImplementation
        |kapt
        |ksp
    )
    \s*\(
    \s*(?P<coordinate>libs\.[A-Za-z0-9_.-]+)
    \s*\)
    """,
    flags=re.VERBOSE,
)


def _gradle_coordinate(
    coordinate: str,
) -> tuple[str, str]:
    parts = coordinate.split(":")

    if len(parts) >= 3:
        return (
            ":".join(parts[:2]),
            ":".join(parts[2:]),
        )

    return coordinate, "catalogo o versione implicita"


def collect_gradle_dependencies(
    paths: list[Path] | None = None,
) -> list[DependencyRecord]:
    gradle_files = (
        paths
        if paths is not None
        else sorted(
            (
                ROOT / "android"
            ).rglob("build.gradle.kts")
        )
    )

    result: list[DependencyRecord] = []

    for path in gradle_files:
        if not path.exists():
            continue

        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        for match in (
            GRADLE_DEPENDENCY_PATTERN.finditer(
                text
            )
        ):
            name, version = (
                _gradle_coordinate(
                    match.group(
                        "coordinate"
                    )
                )
            )

            result.append(
                DependencyRecord(
                    ecosystem="Android/Gradle",
                    name=name,
                    version=version,
                    scope=match.group("scope"),
                    source_file=_relative(path),
                )
            )

        for match in (
            GRADLE_CATALOG_PATTERN.finditer(
                text
            )
        ):
            result.append(
                DependencyRecord(
                    ecosystem="Android/Gradle",
                    name=match.group(
                        "coordinate"
                    ),
                    version=(
                        "risolta dal catalogo Gradle"
                    ),
                    scope=match.group("scope"),
                    source_file=_relative(path),
                )
            )

    return sorted(
        set(result),
        key=DependencyRecord.sort_key,
    )


def _npm_section_scope(
    section: str,
) -> str:
    return {
        "dependencies": "runtime",
        "devDependencies": "development",
        "optionalDependencies": "optional",
        "peerDependencies": "peer",
    }.get(
        section,
        section,
    )


def collect_npm_dependencies(
    path: Path | None = None,
) -> list[DependencyRecord]:
    package_json = (
        path
        if path is not None
        else ROOT / "gateway" / "package.json"
    )

    if not package_json.exists():
        return []

    data: dict[str, Any] = json.loads(
        package_json.read_text(
            encoding="utf-8"
        )
    )

    result: list[DependencyRecord] = []

    for section in (
        "dependencies",
        "devDependencies",
        "optionalDependencies",
        "peerDependencies",
    ):
        dependencies = data.get(
            section,
            {},
        )

        if not isinstance(
            dependencies,
            dict,
        ):
            continue

        for name, version in (
            dependencies.items()
        ):
            result.append(
                DependencyRecord(
                    ecosystem="Node.js/npm",
                    name=str(name),
                    version=str(version),
                    scope=_npm_section_scope(
                        section
                    ),
                    source_file=_relative(
                        package_json
                    ),
                )
            )

    return sorted(
        set(result),
        key=DependencyRecord.sort_key,
    )


def collect_all_dependencies(
) -> list[DependencyRecord]:
    records = [
        *collect_python_dependencies(),
        *collect_gradle_dependencies(),
        *collect_npm_dependencies(),
    ]

    return sorted(
        set(records),
        key=DependencyRecord.sort_key,
    )
