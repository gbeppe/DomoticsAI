#!/usr/bin/env python3

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

INPUT = (
    ROOT
    / "config"
    / "mqtt"
    / "application-contract-v1.json"
)

OUTPUT = (
    ROOT
    / "docs"
    / "MQTT"
    / "MQTT_APPLICATION_CONTRACT.md"
)


def now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def escape(value: Any) -> str:
    if value is None:
        return "—"

    return (
        str(value)
        .replace("|", r"\|")
        .replace("\n", " ")
    )


def render(
    contract: dict[str, Any],
) -> str:
    base_topic = contract["baseTopic"]
    topics = contract.get("topics", [])
    devices = contract["devices"]["lights"]

    counts = Counter(
        topic.get("domain", "unknown")
        for topic in topics
    )

    lines = [
        "# DomoticsAI — MQTT Application Contract",
        "",
        f"Generato automaticamente: `{now_iso()}`",
        "",
        f"- Schema: `{contract['schemaVersion']}`",
        f"- Versione contratto: "
        f"`{contract['contractVersion']}`",
        f"- Stato: `{contract['status']}`",
        f"- Base topic predefinito: "
        f"`{base_topic['default']}`",
        f"- Base topic configurabile: "
        f"`{base_topic['configurable']}`",
        "",
        "## Vincolo architetturale",
        "",
        "L’applicazione comunica esclusivamente sotto:",
        "",
        "```text",
        "${baseTopic}/...",
        "```",
        "",
        "Non deve accedere direttamente ai namespace "
        "dei dispositivi come `cmnd/`, `stat/`, "
        "`tele/`, `shellies/`, `zigbee2mqtt/`, "
        "`homeassistant/` o `tasmota/`.",
        "",
        "## Flusso",
        "",
        "```mermaid",
        "flowchart LR",
        "    DEV[Dispositivi reali]",
        "    NR[Node-RED produzione]",
        "    API[MQTT Application Contract]",
        "    CORE[DomoticsAI Core Engine]",
        "    APP[App Android]",
        "",
        "    DEV --> NR",
        "    NR -->|zara/android/domotica| API",
        "    API --> CORE",
        "    CORE --> APP",
        "```",
        "",
        "## Riepilogo domini",
        "",
        "| Dominio | Pattern censiti |",
        "|---|---:|",
    ]

    for domain, count in sorted(
        counts.items()
    ):
        lines.append(
            f"| `{domain}` | `{count}` |"
        )

    lines.extend(
        [
            "",
            "## Luci",
            "",
        ]
    )

    for group in (
        "internal",
        "external",
        "pool",
        "historicalInactive",
    ):
        values = devices.get(group, [])

        lines.append(
            f"### `{group}`"
        )
        lines.append("")

        for value in values:
            lines.append(f"- `{value}`")

        lines.append("")

    lines.extend(
        [
            "## Scene",
            "",
        ]
    )

    for scene in contract.get(
        "scenes",
        []
    ):
        lines.append(f"- `{scene}`")

    lines.extend(
        [
            "",
            "## Topic",
            "",
            "| Pattern relativo | Dominio | Entità | "
            "Tipo | Direzione | Payload | Unità | "
            "Required | Retained | Supportato |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
    )

    for topic in topics:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape(topic.get('pattern'))}`",
                    f"`{escape(topic.get('domain'))}`",
                    f"`{escape(topic.get('entity'))}`",
                    escape(topic.get("kind")),
                    escape(topic.get("direction")),
                    escape(topic.get("payloadType")),
                    escape(topic.get("unit")),
                    escape(topic.get("required")),
                    escape(
                        topic.get(
                            "retainedExpected"
                        )
                    ),
                    escape(topic.get("supported")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Note e verifiche pendenti",
            "",
        ]
    )

    pending = []

    for topic in topics:
        notes = topic.get("notes")
        verification = topic.get(
            "verification"
        )
        semantic_status = topic.get(
            "semanticStatus"
        )

        details = [
            value
            for value in (
                notes,
                verification,
                semantic_status,
            )
            if value
        ]

        if details:
            pending.append(
                (
                    topic["pattern"],
                    " ".join(details),
                )
            )

    for pattern, description in pending:
        lines.append(
            f"- `{pattern}` — {description}"
        )

    lines.extend(
        [
            "",
            "## Regole di evoluzione",
            "",
            "1. Il `baseTopic` deve essere configurabile.",
            "2. Android e Core Engine non devono "
            "contenere `zara/android/domotica` "
            "hardcoded nella logica di dominio.",
            "3. I nuovi topic devono essere aggiunti "
            "prima al contratto.",
            "4. I comandi restano disabilitati durante "
            "la fase read-only.",
            "5. Topic omonimi non sono automaticamente "
            "equivalenti.",
            "6. Le rinomine devono mantenere una fase "
            "di compatibilità esplicita.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    contract = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        render(contract),
        encoding="utf-8",
    )

    print(
        "OK: contratto MQTT generato:"
    )
    print(f"  {OUTPUT}")
    print(
        "Topic/pattern:",
        len(contract.get("topics", [])),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
