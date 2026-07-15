from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

MANIFEST_OUTPUT = (
    ROOT / "docs" / "PROJECT_MANIFEST.md"
)

INDEX_OUTPUT = (
    ROOT / "docs" / "PROJECT_INDEX.md"
)


DEPENDENCY_OUTPUT = (
    ROOT / "docs" / "DEPENDENCY_INVENTORY.md"
)

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


SENSITIVE_SUFFIXES = (
    ".db",
    ".db-shm",
    ".db-wal",
    ".pid",
    ".log",
    ".backup",
)


INDEXED_ROOTS = {
    "android",
    "core-engine",
    "docs",
    "gateway",
    "scripts",
    "tools",
}


DEPENDENCY_FILE_NAMES = {
    "pyproject.toml",
    "requirements.txt",
    "build.gradle.kts",
    "settings.gradle.kts",
    "libs.versions.toml",
    "package.json",
}
