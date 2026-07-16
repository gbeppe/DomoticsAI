#!/usr/bin/env python3

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONTRACT = (
    ROOT
    / "config"
    / "mqtt"
    / "application-contract-v1.json"
)

DEFAULT_OUTPUT = (
    ROOT
    / "docs"
    / "MQTT"
    / "MQTT_CAPTURE_VALIDATION.md"
)


@dataclass(frozen=True)
class CaptureMessage:
    topic: str
    payload: str


@dataclass(frozen=True)
class CompiledPattern:
    pattern: str
    regex: re.Pattern[str]
    topic_definition: dict[str, Any]


class PayloadCompatibility(Enum):
    COMPATIBLE = "compatible"
    LEGACY_COMPATIBLE = "legacy-compatible"
    INCOMPATIBLE = "incompatible"


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def normalize_base_topic(
    value: str,
) -> str:
    return value.strip().strip("/")


def parse_capture_line(
    line: str,
) -> CaptureMessage | None:
    stripped = line.strip()

    if not stripped:
        return None

    parts = stripped.split(
        maxsplit=1
    )

    topic = parts[0]
    payload = (
        parts[1]
        if len(parts) > 1
        else ""
    )

    return CaptureMessage(
        topic=topic,
        payload=payload,
    )


def read_capture(
    path: Path,
) -> list[CaptureMessage]:
    result: list[CaptureMessage] = []

    for line in path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines():
        message = parse_capture_line(
            line
        )

        if message is not None:
            result.append(message)

    return result


def relative_topic(
    full_topic: str,
    base_topic: str,
) -> str | None:
    normalized_base = (
        normalize_base_topic(
            base_topic
        )
    )

    prefix = normalized_base + "/"

    if full_topic == normalized_base:
        return ""

    if not full_topic.startswith(
        prefix
    ):
        return None

    return full_topic[
        len(prefix):
    ]


PLACEHOLDER_PATTERN = re.compile(
    r"\{([A-Za-z_][A-Za-z0-9_]*)\}"
)


def compile_contract_pattern(
    pattern: str,
) -> re.Pattern[str]:
    cursor = 0
    parts = ["^"]

    for match in (
        PLACEHOLDER_PATTERN.finditer(
            pattern
        )
    ):
        parts.append(
            re.escape(
                pattern[
                    cursor:match.start()
                ]
            )
        )

        name = match.group(1)

        parts.append(
            rf"(?P<{name}>[^/]+)"
        )

        cursor = match.end()

    parts.append(
        re.escape(
            pattern[cursor:]
        )
    )

    parts.append("$")

    return re.compile(
        "".join(parts)
    )


def compile_patterns(
    contract: dict[str, Any],
) -> list[CompiledPattern]:
    result: list[CompiledPattern] = []

    for definition in contract.get(
        "topics",
        []
    ):
        pattern = definition.get(
            "pattern",
            ""
        )

        if not pattern:
            continue

        result.append(
            CompiledPattern(
                pattern=pattern,
                regex=compile_contract_pattern(
                    pattern
                ),
                topic_definition=definition,
            )
        )

    # I pattern specifici devono vincere
    # su quelli generici con placeholder.
    result.sort(
        key=lambda item: (
            item.pattern.count("{"),
            -len(item.pattern),
        )
    )

    return result


def match_topic(
    relative: str,
    patterns: list[CompiledPattern],
) -> list[CompiledPattern]:
    return [
        item
        for item in patterns
        if item.regex.fullmatch(
            relative
        )
    ]


def infer_payload_kind(
    payload: str,
) -> str:
    stripped = payload.strip()

    if not stripped:
        return "empty"

    upper = stripped.upper()

    if upper in {
        "ON",
        "OFF",
        "TRUE",
        "FALSE",
    }:
        return "boolean"

    if stripped in {
        "0",
        "1",
    }:
        return "boolean_or_number"

    try:
        float(stripped)
        return "number"
    except ValueError:
        pass

    try:
        parsed = json.loads(
            stripped
        )

        if isinstance(parsed, dict):
            return "json_object"

        if isinstance(parsed, list):
            return "json_array"

        if isinstance(parsed, bool):
            return "boolean"

        if isinstance(
            parsed,
            (int, float),
        ):
            return "number"

    except json.JSONDecodeError:
        pass

    return "string"


def legacy_payload_is_compatible(
    payload: str,
    accepted_formats: list[str] | None,
) -> bool:
    if not accepted_formats:
        return False

    stripped = payload.strip()
    upper = stripped.upper()

    for accepted in accepted_formats:
        if accepted == "boolean":
            if upper in {
                "TRUE",
                "FALSE",
            }:
                return True

        elif accepted == "0_or_1":
            if stripped in {
                "0",
                "1",
            }:
                return True

        elif accepted == "ON_or_OFF":
            if upper in {
                "ON",
                "OFF",
            }:
                return True

    return False


def payload_compatibility(
    expected: str,
    payload: str,
    legacy_formats: list[str] | None = None,
) -> PayloadCompatibility:
    kind = infer_payload_kind(
        payload
    )

    compatible = False

    if expected in {
        "string",
        "scalar",
        "scene_name",
    }:
        compatible = True

    elif expected == "number":
        compatible = kind in {
            "number",
            "boolean_or_number",
        }

    elif expected == "boolean":
        compatible = kind in {
            "boolean",
            "boolean_or_number",
        }

    elif expected == "boolean_on_off":
        compatible = (
            payload.strip().upper()
            in {
                "ON",
                "OFF",
            }
        )

    elif expected == "boolean_set":
        compatible = (
            payload.strip().upper()
            in {
                "0",
                "1",
                "TRUE",
                "FALSE",
            }
        )

    elif expected == "json_object":
        compatible = (
            kind == "json_object"
        )

    else:
        # Tipo non ancora modellato:
        # non lo consideriamo errore.
        compatible = True

    if compatible:
        return (
            PayloadCompatibility
                .COMPATIBLE
        )

    if legacy_payload_is_compatible(
        payload,
        legacy_formats,
    ):
        return (
            PayloadCompatibility
                .LEGACY_COMPATIBLE
        )

    return (
        PayloadCompatibility
            .INCOMPATIBLE
    )


def payload_is_compatible(
    expected: str,
    payload: str,
) -> bool:
    return (
        payload_compatibility(
            expected,
            payload,
        )
        != PayloadCompatibility.INCOMPATIBLE
    )


def markdown_escape(
    value: Any,
) -> str:
    if value is None:
        return "—"

    return (
        str(value)
        .replace("|", r"\|")
        .replace("\n", " ")
    )


def pattern_specificity(
    item: CompiledPattern,
) -> tuple[int, int]:
    """
    Un numero inferiore di placeholder indica
    un pattern più specifico.

    A parità di placeholder, il pattern più lungo
    è considerato più specifico.
    """
    return (
        item.pattern.count("{"),
        -len(item.pattern),
    )


def matches_are_ambiguous(
    matches: list[CompiledPattern],
) -> bool:
    if len(matches) < 2:
        return False

    return (
        pattern_specificity(matches[0])
        == pattern_specificity(matches[1])
    )


def validate_capture(
    *,
    capture_path: Path,
    contract_path: Path,
) -> dict[str, Any]:
    contract = json.loads(
        contract_path.read_text(
            encoding="utf-8"
        )
    )

    base_topic = normalize_base_topic(
        contract["baseTopic"]["default"]
    )

    messages = read_capture(
        capture_path
    )

    patterns = compile_patterns(
        contract
    )

    outside_namespace: Counter[str] = (
        Counter()
    )

    unmatched: Counter[str] = Counter()
    ambiguous: Counter[str] = Counter()
    matched_topics: Counter[str] = Counter()
    matched_patterns: Counter[str] = (
        Counter()
    )
    payload_kinds: dict[
        str,
        Counter[str],
    ] = defaultdict(Counter)

    legacy_compatible_payloads: dict[
        str,
        Counter[str],
    ] = defaultdict(Counter)

    incompatible_payloads: dict[
        str,
        Counter[str],
    ] = defaultdict(Counter)

    topic_to_pattern: dict[
        str,
        str,
    ] = {}

    topic_definitions: dict[
        str,
        dict[str, Any],
    ] = {}

    for message in messages:
        relative = relative_topic(
            message.topic,
            base_topic,
        )

        if relative is None:
            outside_namespace[
                message.topic
            ] += 1
            continue

        matches = match_topic(
            relative,
            patterns,
        )

        if not matches:
            unmatched[
                relative
            ] += 1
            continue

        if matches_are_ambiguous(
            matches
        ):
            ambiguous[
                relative
            ] += 1

        selected = matches[0]

        matched_topics[
            relative
        ] += 1

        matched_patterns[
            selected.pattern
        ] += 1

        topic_to_pattern[
            relative
        ] = selected.pattern

        topic_definitions[
            relative
        ] = (
            selected.topic_definition
        )

        payload_kind = infer_payload_kind(
            message.payload
        )

        payload_kinds[
            relative
        ][payload_kind] += 1

        expected_type = (
            selected.topic_definition.get(
                "payloadType",
                "",
            )
        )

        compatibility = payload_compatibility(
            expected_type,
            message.payload,
            selected.topic_definition.get(
                "legacyPayloadsTemporarilyAccepted"
            ),
        )

        if (
            compatibility
            == PayloadCompatibility.LEGACY_COMPATIBLE
        ):
            legacy_compatible_payloads[
                relative
            ][
                message.payload[:120]
            ] += 1

        elif (
            compatibility
            == PayloadCompatibility.INCOMPATIBLE
        ):
            incompatible_payloads[
                relative
            ][
                message.payload[:120]
            ] += 1

    observed_patterns = set(
        matched_patterns
    )

    contract_patterns = {
        item["pattern"]
        for item in contract.get(
            "topics",
            []
        )
        if item.get(
            "direction"
        ) in {
            "broker_to_application",
            "bidirectional_pending",
        }
    }

    unobserved_patterns = sorted(
        contract_patterns
        - observed_patterns
    )

    return {
        "capturePath": str(
            capture_path
        ),
        "contractPath": str(
            contract_path
        ),
        "baseTopic": base_topic,
        "messagesTotal": len(messages),
        "messagesMatched": sum(
            matched_topics.values()
        ),
        "uniqueMatchedTopics": len(
            matched_topics
        ),
        "outsideNamespace": dict(
            outside_namespace
        ),
        "unmatchedTopics": dict(
            unmatched
        ),
        "ambiguousTopics": dict(
            ambiguous
        ),
        "matchedTopics": dict(
            matched_topics
        ),
        "matchedPatterns": dict(
            matched_patterns
        ),
        "payloadKinds": {
            topic: dict(counter)
            for topic, counter
            in payload_kinds.items()
        },
        "legacyCompatiblePayloads": {
            topic: dict(counter)
            for topic, counter
            in legacy_compatible_payloads.items()
        },
        "incompatiblePayloads": {
            topic: dict(counter)
            for topic, counter
            in incompatible_payloads.items()
        },
        "topicToPattern":
            topic_to_pattern,
        "topicDefinitions":
            topic_definitions,
        "unobservedContractPatterns":
            unobserved_patterns,
    }


def render_report(
    result: dict[str, Any],
) -> str:
    unmatched = result[
        "unmatchedTopics"
    ]

    outside = result[
        "outsideNamespace"
    ]

    ambiguous = result[
        "ambiguousTopics"
    ]

    legacy_compatible = result[
        "legacyCompatiblePayloads"
    ]

    incompatible = result[
        "incompatiblePayloads"
    ]

    matched_topics = result[
        "matchedTopics"
    ]

    topic_to_pattern = result[
        "topicToPattern"
    ]

    topic_definitions = result[
        "topicDefinitions"
    ]

    payload_kinds = result[
        "payloadKinds"
    ]

    lines = [
        "# DomoticsAI — MQTT Capture Validation",
        "",
        f"Generato automaticamente: "
        f"`{utc_now_iso()}`",
        "",
        f"- Capture: "
        f"`{result['capturePath']}`",
        f"- Contratto: "
        f"`{result['contractPath']}`",
        f"- Base topic: "
        f"`{result['baseTopic']}`",
        "",
        "## Riepilogo",
        "",
        f"- Messaggi totali: "
        f"`{result['messagesTotal']}`",
        f"- Messaggi coperti dal contratto: "
        f"`{result['messagesMatched']}`",
        f"- Topic unici coperti: "
        f"`{result['uniqueMatchedTopics']}`",
        f"- Topic unici non coperti: "
        f"`{len(unmatched)}`",
        f"- Topic fuori namespace: "
        f"`{len(outside)}`",
        f"- Topic ambigui: "
        f"`{len(ambiguous)}`",
        f"- Messaggi legacy temporaneamente accettati: "
        f"`{sum(sum(values.values()) for values in legacy_compatible.values())}`",
        f"- Topic con payload legacy temporanei: "
        f"`{len(legacy_compatible)}`",
        f"- Topic con payload incompatibili: "
        f"`{len(incompatible)}`",
        "",
        "## Topic coperti",
        "",
        "| Topic relativo | Pattern | Dominio | "
        "Entità | Messaggi | Payload osservati |",
        "|---|---|---|---|---:|---|",
    ]

    for topic in sorted(
        matched_topics
    ):
        pattern = topic_to_pattern[
            topic
        ]

        definition = topic_definitions[
            topic
        ]

        kinds = ", ".join(
            f"{name}: {count}"
            for name, count
            in sorted(
                payload_kinds[
                    topic
                ].items()
            )
        )

        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(topic)}`",
                    f"`{markdown_escape(pattern)}`",
                    f"`{markdown_escape(definition.get('domain'))}`",
                    f"`{markdown_escape(definition.get('entity'))}`",
                    str(
                        matched_topics[
                            topic
                        ]
                    ),
                    markdown_escape(kinds),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Topic non coperti",
            "",
        ]
    )

    if unmatched:
        for topic, count in sorted(
            unmatched.items()
        ):
            lines.append(
                f"- `{topic}` — "
                f"`{count}` messaggi"
            )
    else:
        lines.append(
            "- Nessun topic osservato "
            "rimasto fuori contratto."
        )

    lines.extend(
        [
            "",
            "## Pattern del contratto non osservati",
            "",
        ]
    )

    unobserved = result[
        "unobservedContractPatterns"
    ]

    if unobserved:
        for pattern in unobserved:
            lines.append(
                f"- `{pattern}`"
            )
    else:
        lines.append(
            "- Tutti i pattern di lettura "
            "sono stati osservati."
        )

    lines.extend(
        [
            "",
            "## Payload legacy temporaneamente accettati",
            "",
        ]
    )

    if legacy_compatible:
        for topic, values in sorted(
            legacy_compatible.items()
        ):
            lines.append(
                f"### `{topic}`"
            )
            lines.append("")

            for payload, count in sorted(
                values.items()
            ):
                lines.append(
                    f"- `{markdown_escape(payload)}` "
                    f"— `{count}` occorrenze"
                )

            lines.append("")
    else:
        lines.append(
            "- Nessun payload legacy osservato."
        )

    lines.extend(
        [
            "",
            "## Payload incompatibili",
            "",
        ]
    )

    if incompatible:
        for topic, values in sorted(
            incompatible.items()
        ):
            lines.append(
                f"### `{topic}`"
            )
            lines.append("")

            for payload, count in (
                sorted(values.items())
            ):
                lines.append(
                    f"- `{markdown_escape(payload)}` "
                    f"— `{count}` occorrenze"
                )

            lines.append("")
    else:
        lines.append(
            "- Nessuna incompatibilità "
            "rilevata."
        )

    lines.extend(
        [
            "",
            "## Topic ambigui",
            "",
        ]
    )

    if ambiguous:
        for topic, count in sorted(
            ambiguous.items()
        ):
            lines.append(
                f"- `{topic}` — "
                f"`{count}` messaggi"
            )
    else:
        lines.append(
            "- Nessuna corrispondenza ambigua."
        )

    lines.extend(
        [
            "",
            "## Topic fuori namespace",
            "",
        ]
    )

    if outside:
        for topic, count in sorted(
            outside.items()
        ):
            lines.append(
                f"- `{topic}` — "
                f"`{count}` messaggi"
            )
    else:
        lines.append(
            "- Nessun topic fuori dal base topic."
        )

    lines.extend(
        [
            "",
            "## Interpretazione",
            "",
            "- Un topic coperto può essere usato "
            "nelle successive fasi read-only.",
            "- Un topic non coperto deve essere "
            "analizzato prima di essere importato.",
            "- Un pattern non osservato non è "
            "necessariamente errato: può trattarsi "
            "di un comando o di uno stato raro.",
            "- Nessun risultato di questo report "
            "abilita automaticamente la scrittura.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Valida un capture MQTT contro "
            "il contratto applicativo DomoticsAI."
        )
    )

    parser.add_argument(
        "capture",
        type=Path,
        help="Percorso del capture MQTT",
    )

    parser.add_argument(
        "--contract",
        type=Path,
        default=DEFAULT_CONTRACT,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Restituisce errore se esistono "
            "topic fuori contratto, ambigui o "
            "payload incompatibili."
        ),
    )

    args = parser.parse_args()

    if not args.capture.exists():
        print(
            "ERRORE: capture non trovato: "
            f"{args.capture}",
            file=sys.stderr,
        )
        return 2

    result = validate_capture(
        capture_path=args.capture,
        contract_path=args.contract,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        render_report(result),
        encoding="utf-8",
    )

    print(
        "OK: validazione capture completata."
    )
    print(
        "Messaggi:",
        result["messagesTotal"],
    )
    print(
        "Coperti:",
        result["messagesMatched"],
    )
    print(
        "Topic unici coperti:",
        result["uniqueMatchedTopics"],
    )
    print(
        "Topic non coperti:",
        len(result["unmatchedTopics"]),
    )
    print(
        "Topic ambigui:",
        len(result["ambiguousTopics"]),
    )
    print(
        "Payload legacy temporanei:",
        sum(
            sum(values.values())
            for values in result[
                "legacyCompatiblePayloads"
            ].values()
        ),
    )
    print(
        "Payload incompatibili:",
        len(
            result[
                "incompatiblePayloads"
            ]
        ),
    )
    print(
        "Report:",
        args.output,
    )

    if args.strict and (
        result["outsideNamespace"]
        or result["unmatchedTopics"]
        or result["ambiguousTopics"]
        or result[
            "incompatiblePayloads"
        ]
    ):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
