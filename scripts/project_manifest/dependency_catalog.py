from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MatchKind(str, Enum):
    EXACT = "exact"
    PREFIX = "prefix"


@dataclass(frozen=True)
class DependencyPolicy:
    ecosystem: str
    pattern: str
    match_kind: MatchKind

    license: str
    cost_model: str
    cloud_required: str
    raspberry_pi: str

    verification_status: str
    verified_at: str
    official_source: str
    notes: str = ""

    def matches(
        self,
        ecosystem: str,
        name: str,
    ) -> bool:
        if (
            ecosystem.lower()
            != self.ecosystem.lower()
        ):
            return False

        candidate = name.lower()
        pattern = self.pattern.lower()

        if (
            self.match_kind
            == MatchKind.EXACT
        ):
            return candidate == pattern

        return candidate.startswith(
            pattern
        )


VERIFIED_AT = "2026-07-16"


CATALOG: tuple[
    DependencyPolicy,
    ...
] = (
    DependencyPolicy(
        ecosystem="Python",
        pattern="fastapi",
        match_kind=MatchKind.EXACT,
        license="MIT",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; verifica runtime finale richiesta"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/fastapi/fastapi/"
            "blob/master/LICENSE"
        ),
    ),
    DependencyPolicy(
        ecosystem="Python",
        pattern="uvicorn",
        match_kind=MatchKind.EXACT,
        license="BSD-3-Clause",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; verifica runtime finale richiesta"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/encode/uvicorn/"
            "blob/master/LICENSE.md"
        ),
        notes=(
            "Gli extra standard possono installare "
            "dipendenze native opzionali."
        ),
    ),
    DependencyPolicy(
        ecosystem="Python",
        pattern="paho-mqtt",
        match_kind=MatchKind.EXACT,
        license="EPL-2.0 OR EDL-1.0",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; client Python multipiattaforma"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/eclipse-paho/"
            "paho.mqtt.python/blob/master/"
            "LICENSE.txt"
        ),
        notes=(
            "Progetto Eclipse con doppia licenza."
        ),
    ),
    DependencyPolicy(
        ecosystem="Python",
        pattern="pydantic",
        match_kind=MatchKind.EXACT,
        license="MIT",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; verificare wheel ARM della "
            "versione risolta"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/pydantic/"
            "pydantic/blob/main/LICENSE"
        ),
    ),
    DependencyPolicy(
        ecosystem="Python",
        pattern="pytest",
        match_kind=MatchKind.EXACT,
        license="MIT",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; dipendenza di sviluppo"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/pytest-dev/"
            "pytest"
        ),
    ),
    DependencyPolicy(
        ecosystem="Python",
        pattern="httpx",
        match_kind=MatchKind.EXACT,
        license="BSD-3-Clause",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; dipendenza di sviluppo"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/encode/httpx/"
            "blob/master/LICENSE.md"
        ),
    ),

    # Famiglia AndroidX, inclusa Jetpack Compose.
    DependencyPolicy(
        ecosystem="Android/Gradle",
        pattern="androidx.",
        match_kind=MatchKind.PREFIX,
        license="Apache-2.0",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Non applicabile: libreria client Android"
        ),
        verification_status="VERIFICATA_FAMIGLIA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://android.googlesource.com/"
            "platform/frameworks/support/"
        ),
        notes=(
            "Regola applicata agli artifact "
            "ufficiali AndroidX."
        ),
    ),
    DependencyPolicy(
        ecosystem="Android/Gradle",
        pattern=(
            "org.jetbrains.kotlinx:"
            "kotlinx-coroutines"
        ),
        match_kind=MatchKind.PREFIX,
        license="Apache-2.0",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Non applicabile: libreria client Android"
        ),
        verification_status="VERIFICATA_FAMIGLIA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/Kotlin/"
            "kotlinx.coroutines/blob/master/"
            "LICENSE.txt"
        ),
    ),
    DependencyPolicy(
        ecosystem="Android/Gradle",
        pattern="org.eclipse.paho:",
        match_kind=MatchKind.PREFIX,
        license="EPL-2.0 OR EDL-1.0",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Non applicabile: libreria client Android"
        ),
        verification_status="VERIFICATA_FAMIGLIA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/eclipse-paho/"
            "paho.mqtt.android/blob/master/"
            "LICENSE"
        ),
    ),
    DependencyPolicy(
        ecosystem="Android/Gradle",
        pattern="com.hivemq:",
        match_kind=MatchKind.PREFIX,
        license="Apache-2.0",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Non applicabile: libreria client Android"
        ),
        verification_status="VERIFICATA_FAMIGLIA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/hivemq/"
            "hivemq-mqtt-client/blob/master/"
            "LICENSE"
        ),
    ),

    # Gateway Node-RED.
    DependencyPolicy(
        ecosystem="Node.js/npm",
        pattern="node-red",
        match_kind=MatchKind.EXACT,
        license="Apache-2.0",
        cost_model="Gratuito / open source",
        cloud_required="No",
        raspberry_pi=(
            "Sì; verifica runtime finale richiesta"
        ),
        verification_status="VERIFICATA",
        verified_at=VERIFIED_AT,
        official_source=(
            "https://github.com/node-red/"
            "node-red/blob/main/LICENSE"
        ),
    ),
)


def find_dependency_policy(
    ecosystem: str,
    name: str,
) -> DependencyPolicy | None:
    exact_matches = [
        policy
        for policy in CATALOG
        if (
            policy.match_kind
            == MatchKind.EXACT
            and policy.matches(
                ecosystem,
                name,
            )
        )
    ]

    if exact_matches:
        return exact_matches[0]

    prefix_matches = [
        policy
        for policy in CATALOG
        if (
            policy.match_kind
            == MatchKind.PREFIX
            and policy.matches(
                ecosystem,
                name,
            )
        )
    ]

    if not prefix_matches:
        return None

    # Vince il prefisso più specifico.
    return max(
        prefix_matches,
        key=lambda policy:
            len(policy.pattern),
    )
