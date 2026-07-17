#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TOPIC_LITERAL_RE = re.compile(
    r'(?P<quote>["\'`])(?P<topic>[^"\'`\n]*(?:/|mqtt|TeslaPowerwall|zigbee2mqtt|shellies|emon|alexa|casa|zara)[^"\'`\n]*)\1'
)

APP_TOPIC_RE = re.compile(
    r'\$\{(?:APP_BASE|baseTopic)\}/([^"\'`\s;,)]+)'
)


def load_nodes(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Il file Node-RED deve contenere un array JSON di nodi.")
    return [node for node in data if isinstance(node, dict)]


def bool_text(value: Any) -> str:
    if value in (True, "true", "True", 1, "1"):
        return "true"
    if value in (False, "false", "False", 0, "0"):
        return "false"
    return "" if value is None else str(value)


def node_label(node: dict[str, Any]) -> str:
    return str(node.get("name") or node.get("label") or node.get("id") or "")


def broker_label(
    node: dict[str, Any],
    brokers: dict[str, dict[str, Any]],
) -> tuple[str, str, str]:
    broker = brokers.get(str(node.get("broker")), {})
    return (
        str(broker.get("name") or ""),
        str(broker.get("broker") or ""),
        str(broker.get("port") or ""),
    )


def extract_function_topics(code: str) -> tuple[list[str], list[str]]:
    literals: set[str] = set()
    app_topics: set[str] = set()

    for match in TOPIC_LITERAL_RE.finditer(code or ""):
        topic = match.group("topic").strip()
        if topic and len(topic) <= 240:
            literals.add(topic)

    for match in APP_TOPIC_RE.finditer(code or ""):
        app_topics.add(match.group(1).strip())

    return sorted(literals), sorted(app_topics)


def classify_topic(topic: str) -> str:
    lowered = topic.lower()
    if lowered.endswith("/set") or "/cmnd/" in lowered or "/command" in lowered:
        return "command"
    if lowered.endswith("/state") or "/stat/" in lowered or "stato" in lowered:
        return "state"
    if any(x in lowered for x in ("temperature", "humidity", "humidex", "power", "soe", "sensor")):
        return "telemetry"
    if "history" in lowered:
        return "history"
    if topic:
        return "other"
    return "dynamic"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    def esc(value: str) -> str:
        return value.replace("|", r"\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(esc(str(v)) for v in row) + " |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera inventario CSV e Markdown da un export Node-RED."
    )
    parser.add_argument("flow_json", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/NodeRED"),
    )
    args = parser.parse_args()

    nodes = load_nodes(args.flow_json)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    by_id = {str(node.get("id")): node for node in nodes if node.get("id")}
    tabs = {
        str(node.get("id")): str(node.get("label") or node.get("name") or node.get("id"))
        for node in nodes
        if node.get("type") in {"tab", "subflow"}
    }
    brokers = {
        str(node.get("id")): node
        for node in nodes
        if node.get("type") == "mqtt-broker"
    }

    type_counts = Counter(str(node.get("type") or "") for node in nodes)
    mqtt_nodes = [
        node for node in nodes if node.get("type") in {"mqtt in", "mqtt out"}
    ]
    function_nodes = [node for node in nodes if node.get("type") == "function"]
    link_nodes = [
        node for node in nodes if node.get("type") in {"link in", "link out", "link call"}
    ]

    inventory_rows: list[dict[str, str]] = []
    for node in nodes:
        broker_name, broker_host, broker_port = broker_label(node, brokers)
        inventory_rows.append(
            {
                "id": str(node.get("id") or ""),
                "type": str(node.get("type") or ""),
                "tab": tabs.get(str(node.get("z")), str(node.get("z") or "")),
                "name": node_label(node),
                "disabled": bool_text(node.get("d", False)),
                "topic": str(node.get("topic") or ""),
                "qos": str(node.get("qos") or ""),
                "retain": bool_text(node.get("retain")),
                "broker_name": broker_name,
                "broker_host": broker_host,
                "broker_port": broker_port,
                "outputs": str(node.get("outputs") or ""),
                "wire_targets": ",".join(
                    str(target)
                    for group in node.get("wires", []) or []
                    for target in (group or [])
                ),
            }
        )

    csv_path = output_dir / "ANDROID_APP_BRIDGE_NODE_INVENTORY.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(inventory_rows[0].keys()))
        writer.writeheader()
        writer.writerows(inventory_rows)

    mqtt_rows: list[dict[str, str]] = []
    for node in mqtt_nodes:
        broker_name, broker_host, broker_port = broker_label(node, brokers)
        topic = str(node.get("topic") or "")
        mqtt_rows.append(
            {
                "id": str(node.get("id") or ""),
                "direction": "subscribe" if node.get("type") == "mqtt in" else "publish",
                "name": node_label(node),
                "topic": topic,
                "classification": classify_topic(topic),
                "dynamic_topic": "yes" if not topic else "no",
                "qos": str(node.get("qos") or ""),
                "retain": bool_text(node.get("retain")),
                "disabled": bool_text(node.get("d", False)),
                "broker_name": broker_name,
                "broker_host": broker_host,
                "broker_port": broker_port,
            }
        )

    mqtt_csv = output_dir / "ANDROID_APP_BRIDGE_MQTT_INVENTORY.csv"
    with mqtt_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(mqtt_rows[0].keys()))
        writer.writeheader()
        writer.writerows(mqtt_rows)

    function_topic_rows: list[dict[str, str]] = []
    for node in function_nodes:
        literals, app_topics = extract_function_topics(str(node.get("func") or ""))
        function_topic_rows.append(
            {
                "id": str(node.get("id") or ""),
                "name": node_label(node),
                "tab": tabs.get(str(node.get("z")), str(node.get("z") or "")),
                "literal_topics": " ; ".join(literals),
                "application_suffixes": " ; ".join(app_topics),
                "disabled": bool_text(node.get("d", False)),
            }
        )

    function_csv = output_dir / "ANDROID_APP_BRIDGE_FUNCTION_TOPICS.csv"
    with function_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(function_topic_rows[0].keys()))
        writer.writeheader()
        writer.writerows(function_topic_rows)

    link_rows: list[dict[str, str]] = []
    for node in link_nodes:
        linked_ids = [str(value) for value in (node.get("links") or [])]
        unresolved = [value for value in linked_ids if value not in by_id]
        link_rows.append(
            {
                "id": str(node.get("id") or ""),
                "type": str(node.get("type") or ""),
                "name": node_label(node),
                "tab": tabs.get(str(node.get("z")), str(node.get("z") or "")),
                "linked_ids": ",".join(linked_ids),
                "unresolved_external_ids": ",".join(unresolved),
                "external_dependency": "yes" if unresolved else "no",
            }
        )

    links_csv = output_dir / "ANDROID_APP_BRIDGE_LINK_DEPENDENCIES.csv"
    with links_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(link_rows[0].keys()))
        writer.writeheader()
        writer.writerows(link_rows)

    anomalies: list[str] = []
    for row in mqtt_rows:
        if row["direction"] == "publish" and row["broker_host"] == "192.168.1.20":
            anomalies.append(
                f"MQTT out verso broker reale: {row['name'] or row['id']} "
                f"(topic={row['topic'] or '<dinamico>'}, retain={row['retain']})"
            )
        if row["direction"] == "publish" and row["topic"].endswith("/set") and row["retain"] == "true":
            anomalies.append(
                f"Comando retained: {row['name'] or row['id']} -> {row['topic']}"
            )

    for row in function_topic_rows:
        suffixes = row["application_suffixes"]
        if "system/set" in suffixes and row["name"] == "Outbound Router Settaggi":
            anomalies.append(
                "Outbound Router Settaggi pubblica lo stato su system/set; "
                "nel protocollo v2 deve usare system/state."
            )

    unresolved_links = [row for row in link_rows if row["external_dependency"] == "yes"]
    if unresolved_links:
        anomalies.append(
            f"Dipendenze Link Node esterne all'export: {len(unresolved_links)} nodi."
        )

    broker_rows = []
    for broker_id, broker in sorted(brokers.items()):
        broker_rows.append(
            [
                broker_id,
                str(broker.get("name") or ""),
                str(broker.get("broker") or ""),
                str(broker.get("port") or ""),
                bool_text(broker.get("usetls")),
                str(broker.get("protocolVersion") or ""),
            ]
        )

    mqtt_md_rows = [
        [
            row["direction"],
            row["name"] or row["id"],
            row["topic"] or "<dinamico>",
            row["broker_host"] + ":" + row["broker_port"],
            row["qos"],
            row["retain"],
            row["disabled"],
        ]
        for row in mqtt_rows
    ]

    link_md_rows = [
        [
            row["type"],
            row["name"] or row["id"],
            row["linked_ids"],
            row["unresolved_external_ids"] or "—",
        ]
        for row in link_rows
    ]

    md = [
        "# DomoticsAI — Inventario del bridge Node-RED esistente",
        "",
        f"- File analizzato: `{args.flow_json}`",
        f"- Nodi totali: `{len(nodes)}`",
        f"- Schede/subflow: `{len(tabs)}`",
        f"- Broker MQTT: `{len(brokers)}`",
        f"- MQTT in: `{type_counts.get('mqtt in', 0)}`",
        f"- MQTT out: `{type_counts.get('mqtt out', 0)}`",
        f"- Function Node: `{type_counts.get('function', 0)}`",
        f"- Link Node: `{len(link_nodes)}`",
        "",
        "## Broker",
        "",
        markdown_table(
            ["ID", "Nome", "Host", "Porta", "TLS", "Protocollo"],
            broker_rows,
        ),
        "",
        "## Nodi MQTT",
        "",
        markdown_table(
            ["Direzione", "Nodo", "Topic", "Broker", "QoS", "Retain", "Disabilitato"],
            mqtt_md_rows,
        ),
        "",
        "## Dipendenze Link Node",
        "",
        markdown_table(
            ["Tipo", "Nodo", "ID collegati", "ID esterni/non risolti"],
            link_md_rows,
        ),
        "",
        "## Anomalie e punti da verificare",
        "",
    ]

    if anomalies:
        md.extend(f"- {item}" for item in anomalies)
    else:
        md.append("- Nessuna anomalia automatica rilevata.")

    md.extend(
        [
            "",
            "## File generati",
            "",
            "- `ANDROID_APP_BRIDGE_NODE_INVENTORY.csv`",
            "- `ANDROID_APP_BRIDGE_MQTT_INVENTORY.csv`",
            "- `ANDROID_APP_BRIDGE_FUNCTION_TOPICS.csv`",
            "- `ANDROID_APP_BRIDGE_LINK_DEPENDENCIES.csv`",
            "",
            "## Limiti dell'analisi",
            "",
            "- I topic dinamici costruiti da Function Node sono estratti euristicamente.",
            "- I Link Node con destinazioni esterne richiedono gli export delle schede collegate.",
            "- L'inventario non abilita alcun comando verso gli impianti.",
        ]
    )

    md_path = output_dir / "ANDROID_APP_BRIDGE_INVENTORY.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("OK: inventario generato.")
    print("Nodi totali:", len(nodes))
    print("MQTT in:", type_counts.get("mqtt in", 0))
    print("MQTT out:", type_counts.get("mqtt out", 0))
    print("Function Node:", type_counts.get("function", 0))
    print("Link Node:", len(link_nodes))
    print("Anomalie:", len(anomalies))
    print("Output:", output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
