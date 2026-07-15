from pathlib import Path

from scripts.project_manifest.dependencies import (
    collect_gradle_dependencies,
    collect_npm_dependencies,
    collect_python_dependencies,
)


def test_collects_python_dependencies(
    tmp_path: Path,
):
    path = tmp_path / "pyproject.toml"

    path.write_text(
        """
[project]
name = "test"
dependencies = [
    "fastapi>=1.0",
    "pydantic[dotenv]==2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
]
""".strip(),
        encoding="utf-8",
    )

    records = (
        collect_python_dependencies(
            path
        )
    )

    values = {
        (
            item.name,
            item.version,
            item.scope,
        )
        for item in records
    }

    assert (
        "fastapi",
        ">=1.0",
        "runtime",
    ) in values

    assert (
        "pydantic",
        "==2.0",
        "runtime",
    ) in values

    assert (
        "pytest",
        ">=8",
        "optional:dev",
    ) in values


def test_collects_gradle_dependencies(
    tmp_path: Path,
):
    path = tmp_path / "build.gradle.kts"

    path.write_text(
        """
dependencies {
    implementation(
        "androidx.core:core-ktx:1.0.0"
    )
    testImplementation(
        "junit:junit:4.13.2"
    )
    implementation(libs.androidx.lifecycle)
}
""".strip(),
        encoding="utf-8",
    )

    records = (
        collect_gradle_dependencies(
            [path]
        )
    )

    names = {
        item.name
        for item in records
    }

    assert (
        "androidx.core:core-ktx"
        in names
    )

    assert "junit:junit" in names

    assert (
        "libs.androidx.lifecycle"
        in names
    )


def test_collects_npm_dependencies(
    tmp_path: Path,
):
    path = tmp_path / "package.json"

    path.write_text(
        """
{
  "dependencies": {
    "node-red": "^4.0.0"
  },
  "devDependencies": {
    "eslint": "^9.0.0"
  }
}
""".strip(),
        encoding="utf-8",
    )

    records = (
        collect_npm_dependencies(
            path
        )
    )

    values = {
        (
            item.name,
            item.version,
            item.scope,
        )
        for item in records
    }

    assert (
        "node-red",
        "^4.0.0",
        "runtime",
    ) in values

    assert (
        "eslint",
        "^9.0.0",
        "development",
    ) in values
