#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

SAFE_STATUSES = {
    "CURRENT_APP_NAMESPACE",
    "LEGACY_MAP",
    "READ_ONLY_PRIMARY",
    "KEEP_AS_STATE",
    "PHYSICAL_TOPIC",
}
READ_ONLY_ROLES = {"READ_ONLY", "STATE"}

COMMAND_SEGMENTS = {
    "set",
    "cmd",
    "cmnd",
    "command",
}


def is_command_topic(topic: str) -> bool:
    segments = {
        segment.lower()
        for segment in topic.strip("/").split("/")
        if segment
    }

    return bool(
        segments & COMMAND_SEGMENTS
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mapping_csv", type=Path)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("config/nodered/bridge-v2-readonly-plan.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("docs/NodeRED/BRIDGE_V2_READONLY_PLAN.md"),
    )
    args = parser.parse_args()

    rows = load_rows(args.mapping_csv)
    subscriptions = []
    excluded = []

    for row in rows:
        role = row["role"]
        status = row["migration_status"]
        source_topic = row["current_topic"]
        suffix = row["proposed_suffix"]

        safe = (
            role in READ_ONLY_ROLES
            and status in SAFE_STATUSES
            and source_topic
            and source_topic not in {"<dinamico>", "zara/android/domotica"}
            and not is_command_topic(source_topic)
            and suffix
        )

        if safe:
            subscriptions.append(
                {
                    "domain": row["domain"],
                    "sourceTopic": source_topic,
                    "sourceBroker": (
                        f"{row['broker_host']}:{row['broker_port']}"
                        if row["broker_host"]
                        else None
                    ),
                    "destinationSuffix": suffix,
                    "destinationTopicTemplate": f"${{canaryBaseTopic}}/{suffix}",
                    "payload": row["proposed_payload"],
                    "retain": row["proposed_retain"],
                    "occurrences": int(row["occurrences"]),
                    "nodes": row["node_names"],
                    "status": status,
                }
            )
        else:
            excluded.append(
                {
                    "domain": row["domain"],
                    "role": role,
                    "topic": source_topic,
                    "status": status,
                }
            )

    dedup = {}
    for item in subscriptions:
        key = (item["sourceTopic"], item["destinationTopicTemplate"])
        if key not in dedup:
            dedup[key] = item
        else:
            dedup[key]["occurrences"] += item["occurrences"]

    subscriptions = sorted(
        dedup.values(),
        key=lambda item: (
            item["domain"],
            item["sourceTopic"],
            item["destinationTopicTemplate"],
        ),
    )

    plan = {
        "version": "1.0.0-draft",
        "mode": "READ_ONLY_CANARY",
        "productionBaseTopic": "zara/android/domotica",
        "canaryBaseTopic": "zara/android/domotica/v2",
        "sourceBrokers": {
            "domotics": {"host": "192.168.1.20", "port": 1883},
            "telemetry": {"host": "192.168.1.15", "port": 1883},
        },
        "safety": {
            "hardwareCommandsEnabled": False,
            "subscribeToCanaryCommands": False,
            "publishOnlyUnderCanaryBaseTopic": True,
            "allowDynamicPublishTopics": False,
            "allowRetainedStates": True,
            "allowRetainedCommands": False,
        },
        "subscriptions": subscriptions,
        "excluded": excluded,
    }

    by_domain = defaultdict(list)
    for item in subscriptions:
        by_domain[item["domain"]].append(item)

    lines = [
        "# DomoticsAI — Piano Bridge v2 read-only",
        "",
        f"- Modalità: `{plan['mode']}`",
        f"- Base topic produzione: `{plan['productionBaseTopic']}`",
        f"- Base topic canary: `{plan['canaryBaseTopic']}`",
        f"- Sottoscrizioni read-only: `{len(subscriptions)}`",
        f"- Elementi esclusi: `{len(excluded)}`",
        "",
        "## Regole di sicurezza",
        "",
        "- Nessun comando hardware.",
        "- Nessuna sottoscrizione ai topic di comando del namespace canary.",
        "- Pubblicazioni consentite soltanto sotto `zara/android/domotica/v2/...`.",
        "- Stati read-only retained consentiti.",
        "- Comandi retained vietati.",
        "- Topic dinamici esclusi dal primo canary.",
        "",
    ]

    for domain in sorted(by_domain):
        lines.extend(
            [
                f"## {domain.upper()}",
                "",
                "| Sorgente | Broker | Destinazione canary | Payload | Retain |",
                "|---|---|---|---|---|",
            ]
        )
        for item in by_domain[domain]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{item['sourceTopic']}`",
                        f"`{item['sourceBroker'] or 'n/d'}`",
                        f"`{item['destinationTopicTemplate']}`",
                        item["payload"],
                        item["retain"],
                    ]
                )
                + " |"
            )
        lines.append("")

    counts = Counter(item["status"] for item in excluded)
    lines.extend(["## Esclusioni", ""])
    for status, count in sorted(counts.items()):
        lines.append(f"- `{status}`: `{count}`")

    lines.extend(
        [
            "",
            "## Criterio di promozione",
            "",
            "Il bridge può passare da `READ_ONLY_CANARY` a `READ_ONLY_PRIMARY` soltanto dopo:",
            "",
            "1. almeno 24 ore senza loop MQTT;",
            "2. nessuna pubblicazione fuori dal namespace canary;",
            "3. confronto positivo dei valori con il bridge storico;",
            "4. assenza di errori di payload;",
            "5. conferma manuale per ogni dominio.",
            "",
        ]
    )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)

    args.output_json.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print("OK: piano bridge v2 read-only generato.")
    print("Sottoscrizioni:", len(subscriptions))
    print("Esclusioni:", len(excluded))
    print("JSON:", args.output_json)
    print("Markdown:", args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
