#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


COMMAND_PATTERNS = (
    re.compile(r"/set(?:$|/)"),
    re.compile(r"/cmnd(?:$|/)"),
    re.compile(r"/command(?:$|/)"),
    re.compile(r"/cmd(?:$|/)"),
)

HARDWARE_PREFIXES = (
    "zigbee2mqtt/",
    "shellies/",
    "casa/clima/cmnd/",
    "alexa/",
    "emon/",
)

ALLOWED_OPERATIONAL_TYPES = {
    "mqtt in",
    "function",
    "mqtt out",
    "change",
    "switch",
    "rbe",
    "delay",
    "trigger",
    "debug",
    "link in",
    "link out",
    "link call",
}

CONFIG_TYPES = {
    "mqtt-broker",
    "tls-config",
}

NON_OPERATIONAL_TYPES = {
    "tab",
    "subflow",
    "comment",
    "group",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    node_id: str
    node_type: str
    node_name: str
    message: str


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERRORE: file non trovato: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"ERRORE: JSON non valido in {path}: "
            f"riga {exc.lineno}, colonna {exc.colno}: {exc.msg}"
        )


def node_label(node: dict[str, Any]) -> str:
    return str(
        node.get("name")
        or node.get("label")
        or node.get("id")
        or "<senza nome>"
    )


def is_command_topic(topic: str) -> bool:
    normalized = topic.strip().lower()
    return any(pattern.search(normalized) for pattern in COMMAND_PATTERNS)


def is_hardware_topic(topic: str) -> bool:
    normalized = topic.strip().lower()
    return normalized.startswith(tuple(prefix.lower() for prefix in HARDWARE_PREFIXES))


def extract_destination_topic(function_code: str) -> str | None:
    marker = "const DESTINATION_TOPIC = "
    if marker not in function_code:
        return None

    remainder = function_code.split(marker, 1)[1]
    line = remainder.splitlines()[0].strip()

    if line.endswith(";"):
        line = line[:-1].strip()

    try:
        value = json.loads(line)
    except json.JSONDecodeError:
        return None

    return value if isinstance(value, str) else None


def validate(
    nodes: list[dict[str, Any]],
    canary_base: str,
) -> list[Finding]:
    findings: list[Finding] = []

    if not isinstance(nodes, list):
        return [
            Finding(
                "ERROR",
                "FLOW_NOT_ARRAY",
                "",
                "",
                "",
                "Il flow Node-RED deve essere un array JSON.",
            )
        ]

    tabs = [
        node
        for node in nodes
        if node.get("type") == "tab"
    ]

    if len(tabs) != 1:
        findings.append(
            Finding(
                "ERROR",
                "TAB_COUNT",
                "",
                "tab",
                "",
                f"Attesa una sola tab, trovate {len(tabs)}.",
            )
        )
    elif tabs[0].get("disabled") is not True:
        findings.append(
            Finding(
                "ERROR",
                "TAB_ENABLED",
                str(tabs[0].get("id") or ""),
                "tab",
                node_label(tabs[0]),
                "La tab del bridge v2 deve essere disabilitata.",
            )
        )

    mqtt_brokers = {
        str(node.get("id"))
        for node in nodes
        if node.get("type") == "mqtt-broker"
    }

    node_ids: set[str] = set()

    for node in nodes:
        node_id = str(node.get("id") or "")
        node_type = str(node.get("type") or "")
        name = node_label(node)

        if not node_id:
            findings.append(
                Finding(
                    "ERROR",
                    "MISSING_NODE_ID",
                    "",
                    node_type,
                    name,
                    "Nodo privo di id.",
                )
            )
        elif node_id in node_ids:
            findings.append(
                Finding(
                    "ERROR",
                    "DUPLICATE_NODE_ID",
                    node_id,
                    node_type,
                    name,
                    "ID nodo duplicato.",
                )
            )
        else:
            node_ids.add(node_id)

        if node_type in NON_OPERATIONAL_TYPES or node_type in CONFIG_TYPES:
            continue

        if node_type not in ALLOWED_OPERATIONAL_TYPES:
            findings.append(
                Finding(
                    "ERROR",
                    "UNEXPECTED_NODE_TYPE",
                    node_id,
                    node_type,
                    name,
                    f"Tipo nodo non ammesso nel flow read-only: {node_type}",
                )
            )

        if node.get("d") is not True:
            findings.append(
                Finding(
                    "ERROR",
                    "NODE_ENABLED",
                    node_id,
                    node_type,
                    name,
                    "Nodo operativo non disabilitato.",
                )
            )

        if node_type == "mqtt in":
            topic = str(node.get("topic") or "")

            if not topic:
                findings.append(
                    Finding(
                        "ERROR",
                        "MQTT_IN_EMPTY_TOPIC",
                        node_id,
                        node_type,
                        name,
                        "MQTT IN senza topic.",
                    )
                )

            if is_command_topic(topic):
                findings.append(
                    Finding(
                        "ERROR",
                        "COMMAND_SUBSCRIPTION",
                        node_id,
                        node_type,
                        name,
                        f"Sottoscrizione a topic comando vietata: {topic}",
                    )
                )

            broker_id = str(node.get("broker") or "")
            if not broker_id or broker_id not in mqtt_brokers:
                findings.append(
                    Finding(
                        "ERROR",
                        "INVALID_SOURCE_BROKER",
                        node_id,
                        node_type,
                        name,
                        "MQTT IN riferisce un broker mancante o non valido.",
                    )
                )

        elif node_type == "mqtt out":
            static_topic = str(node.get("topic") or "")
            retain = str(node.get("retain") or "").lower()
            qos = str(node.get("qos") or "")

            if static_topic:
                findings.append(
                    Finding(
                        "ERROR",
                        "STATIC_OUTPUT_TOPIC",
                        node_id,
                        node_type,
                        name,
                        f"MQTT OUT deve usare msg.topic, non topic statico: {static_topic}",
                    )
                )

            if retain not in {"true", "false"}:
                findings.append(
                    Finding(
                        "ERROR",
                        "INVALID_RETAIN",
                        node_id,
                        node_type,
                        name,
                        f"Valore retain non valido: {retain!r}",
                    )
                )

            if qos not in {"0", "1", "2"}:
                findings.append(
                    Finding(
                        "ERROR",
                        "INVALID_QOS",
                        node_id,
                        node_type,
                        name,
                        f"QoS non valido: {qos!r}",
                    )
                )

            broker_id = str(node.get("broker") or "")
            if not broker_id or broker_id not in mqtt_brokers:
                findings.append(
                    Finding(
                        "ERROR",
                        "INVALID_OUTPUT_BROKER",
                        node_id,
                        node_type,
                        name,
                        "MQTT OUT riferisce un broker mancante o non valido.",
                    )
                )

        elif node_type == "function":
            code = str(node.get("func") or "")
            destination = extract_destination_topic(code)

            if destination is None:
                findings.append(
                    Finding(
                        "ERROR",
                        "DESTINATION_NOT_FOUND",
                        node_id,
                        node_type,
                        name,
                        "Impossibile estrarre DESTINATION_TOPIC dal Function node.",
                    )
                )
                continue

            if not destination.startswith(canary_base + "/"):
                findings.append(
                    Finding(
                        "ERROR",
                        "DESTINATION_OUTSIDE_CANARY",
                        node_id,
                        node_type,
                        name,
                        f"Destinazione fuori namespace canary: {destination}",
                    )
                )

            if is_command_topic(destination):
                findings.append(
                    Finding(
                        "ERROR",
                        "COMMAND_PUBLICATION",
                        node_id,
                        node_type,
                        name,
                        f"Destinazione comando vietata: {destination}",
                    )
                )

            if is_hardware_topic(destination):
                findings.append(
                    Finding(
                        "ERROR",
                        "HARDWARE_PUBLICATION",
                        node_id,
                        node_type,
                        name,
                        f"Destinazione hardware vietata: {destination}",
                    )
                )

            if "startsWith(CANARY_BASE + '/')" not in code:
                findings.append(
                    Finding(
                        "ERROR",
                        "MISSING_LOOP_GUARD",
                        node_id,
                        node_type,
                        name,
                        "Protezione anti-loop canary mancante.",
                    )
                )

            if "msg.topic !== SOURCE_TOPIC" not in code:
                findings.append(
                    Finding(
                        "ERROR",
                        "MISSING_SOURCE_GUARD",
                        node_id,
                        node_type,
                        name,
                        "Controllo del topic sorgente mancante.",
                    )
                )

            if "msg.topic = DESTINATION_TOPIC" not in code:
                findings.append(
                    Finding(
                        "ERROR",
                        "MISSING_TOPIC_ASSIGNMENT",
                        node_id,
                        node_type,
                        name,
                        "Assegnazione finale di msg.topic mancante.",
                    )
                )

    mqtt_out_ids = {
        str(node.get("id"))
        for node in nodes
        if node.get("type") == "mqtt out"
    }

    function_nodes = [
        node
        for node in nodes
        if node.get("type") == "function"
    ]

    for node in function_nodes:
        node_id = str(node.get("id") or "")
        wires = node.get("wires") or []

        wired_targets = {
            str(target)
            for output in wires
            if isinstance(output, list)
            for target in output
        }

        if not wired_targets:
            findings.append(
                Finding(
                    "ERROR",
                    "FUNCTION_NOT_WIRED",
                    node_id,
                    "function",
                    node_label(node),
                    "Function node senza uscita collegata.",
                )
            )
        elif not wired_targets.issubset(mqtt_out_ids):
            findings.append(
                Finding(
                    "ERROR",
                    "FUNCTION_WIRED_TO_UNEXPECTED_NODE",
                    node_id,
                    "function",
                    node_label(node),
                    "Function node collegato a nodi diversi da MQTT OUT.",
                )
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validatore statico di sicurezza per il flow Bridge v2 read-only."
    )
    parser.add_argument("flow_json", type=Path)
    parser.add_argument(
        "--canary-base",
        default="zara/android/domotica/v2",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
    )
    args = parser.parse_args()

    nodes = load_json(args.flow_json)
    findings = validate(nodes, args.canary_base.rstrip("/"))

    report = {
        "flow": str(args.flow_json),
        "canaryBase": args.canary_base.rstrip("/"),
        "errors": sum(item.severity == "ERROR" for item in findings),
        "warnings": sum(item.severity == "WARNING" for item in findings),
        "findings": [
            {
                "severity": item.severity,
                "code": item.code,
                "nodeId": item.node_id,
                "nodeType": item.node_type,
                "nodeName": item.node_name,
                "message": item.message,
            }
            for item in findings
        ],
    }

    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if findings:
        print("VALIDAZIONE FALLITA")
        print(f"Errori: {report['errors']}")
        print(f"Warning: {report['warnings']}")
        print()

        for item in findings:
            location = " | ".join(
                part
                for part in (
                    item.node_type,
                    item.node_name,
                    item.node_id,
                )
                if part
            )
            print(
                f"[{item.severity}] {item.code}"
                + (f" | {location}" if location else "")
            )
            print(f"  {item.message}")

        return 1

    print("OK: flow staticamente sicuro.")
    print("Tab disabilitata: sì")
    print("Nodi operativi disabilitati: sì")
    print("Sottoscrizioni comando: 0")
    print("Pubblicazioni comando: 0")
    print("Pubblicazioni hardware: 0")
    print(f"Namespace canary: {args.canary_base.rstrip('/')}/...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
