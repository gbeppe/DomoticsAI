from pathlib import Path


def category(p: Path, cfg):
    s = p.as_posix().lower()
    n = p.name.lower()
    x = p.suffix.lower()

    if any(m.lower() in s for m in cfg["classification"]["generated_markers"]):
        return "Generated Artifact"

    if any(m.lower() in s for m in cfg["classification"]["runtime_markers"]):
        return "Runtime Artifact"

    if n.startswith("adr-") or "/adr/" in s or "/adrs/" in s:
        return "ADR"

    if x == ".md" or n.startswith("readme"):
        return "Documentation"

    if "test" in p.parts or n.startswith("test_") or n.endswith("_test.py"):
        return "Test"

    if x in {
        ".py", ".kt", ".kts", ".java",
        ".js", ".ts", ".tsx", ".jsx",
        ".c", ".cpp", ".h", ".hpp",
    }:
        return "Source Code"

    if x in {
        ".yaml", ".yml", ".json",
        ".toml", ".ini", ".cfg",
        ".properties", ".xml",
    }:
        return "Configuration"

    if x in {".sh", ".bash", ".zsh", ".ps1"}:
        return "Script"

    if x in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"}:
        return "Asset"

    if x in {".zip", ".tar", ".gz", ".jar", ".apk", ".bin", ".so"}:
        return "Binary"

    return "Other"


def domain(p: Path, cfg):
    s = p.as_posix().lower()

    for rule in cfg["domains"]["path_rules"]:
        for prefix in rule.get("prefixes", []):
            prefix = prefix.lower().rstrip("/")
            if s == prefix or s.startswith(prefix + "/"):
                return rule["domain"]

    return cfg["domains"].get("default", "Repository")
