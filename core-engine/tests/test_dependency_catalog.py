from scripts.project_manifest.dependencies import (
    DependencyRecord,
    enrich_dependency,
)
from scripts.project_manifest.dependency_catalog import (
    find_dependency_policy,
)


def record(
    ecosystem: str,
    name: str,
) -> DependencyRecord:
    return DependencyRecord(
        ecosystem=ecosystem,
        name=name,
        version="test",
        scope="runtime",
        source_file="test",
    )


def test_exact_python_dependency():
    enriched = enrich_dependency(
        record(
            "Python",
            "fastapi",
        )
    )

    assert enriched.license == "MIT"

    assert (
        enriched.verification_status
        == "VERIFICATA"
    )

    assert (
        enriched.cloud_required
        == "No"
    )


def test_androidx_family():
    enriched = enrich_dependency(
        record(
            "Android/Gradle",
            "androidx.lifecycle:"
            "lifecycle-viewmodel-compose",
        )
    )

    assert (
        enriched.license
        == "Apache-2.0"
    )

    assert (
        enriched.verification_status
        == "VERIFICATA_FAMIGLIA"
    )


def test_most_specific_prefix_wins():
    policy = find_dependency_policy(
        "Android/Gradle",
        "org.jetbrains.kotlinx:"
        "kotlinx-coroutines-android",
    )

    assert policy is not None

    assert (
        policy.license
        == "Apache-2.0"
    )


def test_unknown_dependency_remains_unknown():
    enriched = enrich_dependency(
        record(
            "Node.js/npm",
            "unknown-package",
        )
    )

    assert (
        enriched.license
        == "DA_VERIFICARE"
    )

    assert (
        enriched.verification_status
        == "NON_VERIFICATA"
    )


def test_paho_dual_license():
    enriched = enrich_dependency(
        record(
            "Python",
            "paho-mqtt",
        )
    )

    assert (
        enriched.license
        == "EPL-2.0 OR EDL-1.0"
    )
