#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

DEFAULT_FLOW = Path(
    "/home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway/flows.json"
)

KEYWORDS = (
    "light", "lights", "luce", "luci", "lamp", "lampada",
    "pool", "piscina", "garden", "giardino", "external",
    "esterno", "internal", "interno", "scene", "scenario",
    "scena", "relay", "rele", "relè",
)

INTERESTING_TYPES = {
    "mqtt in", "mqtt out", "function", "change", "switch",
    "inject", "trigger", "link in", "link out", "subflow",
    "ui_switch", "ui_button", "ui_dropdown", "ui_template",
    "api-call-service", "server-state-changed",
}


def normalize(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def searchable_text(node: dict[str, Any]) -> str:
    fields = (
        "name", "label", "topic", "func", "rules", "property",
        "payload", "service", "entityid", "entityId",
        "domain", "action", "title", "group",
    )
    return " ".join(normalize(node.get(field)) for field in fields).lower()


def is_relevant(node: dict[str, Any]) -> bool:
    text = searchable_text(node)
    return any(keyword in text for keyword in KEYWORDS)


def connected_ids(node: dict[str, Any]) -> list[str]:
    result: list[str] = []
    wires = node.get("wires", [])
    if isinstance(wires, list):
        for output in wires:
            if isinstance(output, list):
                result.extend(str(item) for item in output)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reverse engineering luci e scenari dai flow Node-RED."
    )
    parser.add_argument("--flow", type=Path, default=DEFAULT_FLOW)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "/home/giuseppe/AndroidStudioProjects/DomoticsAI/"
            "docs/reverse-engineering/lights"
        ),
    )
    args = parser.parse_args()

    if not args.flow.exists():
        raise SystemExit(f"File non trovato: {args.flow}")

    nodes = json.loads(args.flow.read_text(encoding="utf-8"))
    by_id = {
        str(node.get("id")): node
        for node in nodes
        if isinstance(node, dict) and node.get("id")
    }
    tabs = {
        str(node.get("id")): node.get("label", node.get("name", ""))
        for node in nodes
        if node.get("type") == "tab"
    }

    relevant_ids: set[str] = {
        str(node["id"])
        for node in nodes
        if isinstance(node, dict)
        and node.get("id")
        and is_relevant(node)
    }

    for node in nodes:
        node_id = str(node.get("id", ""))
        outputs = set(connected_ids(node))
        if node_id in relevant_ids:
            relevant_ids.update(outputs)
        elif outputs & relevant_ids:
            relevant_ids.add(node_id)

    records: list[dict[str, Any]] = []
    topics: list[dict[str, str]] = []

    for node_id in sorted(relevant_ids):
        node = by_id.get(node_id)
        if not node:
            continue

        node_type = normalize(node.get("type"))
        if node_type not in INTERESTING_TYPES and not is_relevant(node):
            continue

        tab_id = normalize(node.get("z"))
        record = {
            "id": node_id,
            "tab": normalize(tabs.get(tab_id, tab_id)),
            "type": node_type,
            "name": normalize(node.get("name") or node.get("label")),
            "topic": normalize(node.get("topic")),
            "broker_id": normalize(node.get("broker")),
            "payload": normalize(node.get("payload")),
            "outputs_to": ", ".join(connected_ids(node)),
            "relevant_text": searchable_text(node)[:500],
        }
        records.append(record)

        topic = record["topic"].strip()
        if topic:
            topics.append({
                "node_id": node_id,
                "tab": record["tab"],
                "node_type": node_type,
                "node_name": record["name"],
                "direction": (
                    "input" if node_type == "mqtt in"
                    else "output" if node_type == "mqtt out"
                    else "reference"
                ),
                "topic": topic,
            })

    args.output.mkdir(parents=True, exist_ok=True)

    (args.output / "lights-nodes.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (args.output / "lights-topics.json").write_text(
        json.dumps(topics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    node_fields = [
        "id", "tab", "type", "name", "topic", "broker_id",
        "payload", "outputs_to", "relevant_text",
    ]
    with (args.output / "lights-nodes.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=node_fields)
        writer.writeheader()
        writer.writerows(records)

    topic_fields = [
        "node_id", "tab", "node_type", "node_name",
        "direction", "topic",
    ]
    with (args.output / "lights-topics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=topic_fields)
        writer.writeheader()
        writer.writerows(topics)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in topics:
        grouped[item["tab"] or "Senza tab"].append(item)

    md = [
        "# Reverse engineering — Luci e scenari",
        "",
        f"Flow analizzato: `{args.flow}`",
        "",
        f"Nodi rilevanti: **{len(records)}**",
        f"Topic espliciti rilevati: **{len(topics)}**",
        "",
        "## Topic MQTT e riferimenti",
        "",
    ]

    if topics:
        for tab, items in sorted(grouped.items()):
            md.extend([f"### {tab}", ""])
            for item in items:
                md.append(
                    f"- `{item['topic']}` — {item['direction']} — "
                    f"{item['node_name'] or item['node_type']} "
                    f"(`{item['node_id']}`)"
                )
            md.append("")
    else:
        md.append("Nessun topic esplicito rilevato automaticamente.")
        md.append("")

    md.extend([
        "## Classificazione da completare",
        "",
        "| ID logico | Nome UI | Area | Tipo | Topic stato | Topic comando | Dimmer | Note |",
        "|---|---|---|---|---|---|---|---|",
        "| | | interno/esterno/piscina | luce/scenario/gruppo | | | sì/no | |",
        "",
        "## Domande funzionali",
        "",
        "- Lo stato pubblicato rappresenta il comando o la conferma reale?",
        "- Esistono luci dimmerabili o RGB?",
        "- Quali scenari sono mutuamente esclusivi?",
        "- Gli scenari modificano anche clima, piscina o ingressi?",
        "- Quali comandi richiedono conferma o timeout?",
        "- Esistono automazioni orarie o crepuscolari?",
        "",
    ])

    (args.output / "LIGHTS_REVERSE_ENGINEERING.md").write_text(
        "\n".join(md),
        encoding="utf-8",
    )

    print(f"OK: report creato in {args.output}")
    print(f"Nodi rilevanti: {len(records)}")
    print(f"Topic espliciti: {len(topics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
