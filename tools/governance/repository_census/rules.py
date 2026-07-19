from collections import defaultdict
import re
from urllib.parse import unquote

from tools.governance.common.models import Issue


LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def evaluate_rules(ctx, files):
    issues = []
    root = ctx.repository_root
    ignored = set(ctx.configuration["ignore"]["names"])
    minimum = int(
        ctx.configuration["rules"]["thin_document"]["minimum_lines"]
    )

    for directory in sorted(root.iterdir()):
        if (
            directory.is_dir()
            and directory.name not in ignored
            and not directory.name.startswith(".")
            and not any(
                (directory / name).exists()
                for name in ("README.md", "README", "readme.md")
            )
        ):
            issues.append(
                Issue(
                    "DGT-DOC-001",
                    "MEDIUM",
                    "Top-level directory has no README",
                    directory.name,
                )
            )

    for file_entry in files:
        if (
            file_entry.category in {"Documentation", "ADR"}
            and file_entry.line_count is not None
            and file_entry.line_count < minimum
        ):
            issues.append(
                Issue(
                    "DGT-DOC-002",
                    "LOW",
                    f"Document has fewer than {minimum} lines",
                    file_entry.path,
                )
            )

        if file_entry.category == "Other":
            issues.append(
                Issue(
                    "DGT-REP-001",
                    "LOW",
                    "File classified as Other",
                    file_entry.path,
                )
            )

        if file_entry.category in {
            "Generated Artifact",
            "Runtime Artifact",
        }:
            issues.append(
                Issue(
                    "DGT-REP-002",
                    "MEDIUM",
                    f"{file_entry.category} is present in repository scan",
                    file_entry.path,
                )
            )

        if file_entry.extension == ".md":
            path = root / file_entry.path

            for raw in LINK.findall(
                path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            ):
                target_text = raw.strip().split()[0].strip("<>")

                if (
                    not target_text
                    or target_text.startswith(
                        ("http://", "https://", "mailto:", "#")
                    )
                ):
                    continue

                target = (
                    path.parent
                    / unquote(target_text.split("#", 1)[0])
                ).resolve()

                try:
                    target.relative_to(root.resolve())
                except ValueError:
                    continue

                if not target.exists():
                    issues.append(
                        Issue(
                            "DGT-DOC-003",
                            "HIGH",
                            f"Broken Markdown link: {raw}",
                            file_entry.path,
                        )
                    )

    files_by_hash = defaultdict(list)

    for file_entry in files:
        if file_entry.size_bytes:
            files_by_hash[file_entry.sha256].append(
                file_entry.path
            )

    for paths in files_by_hash.values():
        if len(paths) > 1:
            for path in paths:
                issues.append(
                    Issue(
                        "DGT-REP-003",
                        "LOW",
                        "Duplicate file content detected",
                        path,
                        {"duplicates": sorted(paths)},
                    )
                )

    return sorted(
        issues,
        key=lambda issue: (
            issue.severity,
            issue.rule_id,
            issue.path or "",
        ),
    )
