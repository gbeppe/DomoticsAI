#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def stable_id(*parts: str) -> str:
    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()
    return digest[:16]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def mqtt_broker_node(node_id: str, name: str, host: str, port: int) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": "mqtt-broker",
        "name": name,
        "broker": host,
        "port": str(port),
        "clientid": "",
        "autoConnect": True,
        "usetls": False,
        "protocolVersion": "4",
        "keepalive": "60",
        "cleansession": True,
        "autoUnsubscribe": True,
        "birthTopic": "",
        "birthQos": "0",
        "birthPayload": "",
        "birthMsg": {},
        "closeTopic": "",
        "closeQos": "0",
        "closePayload": "",
        "closeMsg": {},
        "willTopic": "",
        "willQos": "0",
        "willPayload": "",
        "willMsg": {},
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera il flow Node-RED Bridge v2 read-only canary, disabilitato."
    )
    parser.add_argument(
        "plan_json",
        type=Path,
        help="Piano JSON generato da generate_readonly_bridge_plan.py",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("gateway/flows/bridge-v2-readonly-disabled.json"),
    )
    args = parser.parse_args()

    plan = load_json(args.plan_json)

    if plan.get("mode") != "READ_ONLY_CANARY":
        raise SystemExit("ERRORE: il piano non è READ_ONLY_CANARY.")

    safety = plan.get("safety", {})
    required = {
        "hardwareCommandsEnabled": False,
        "subscribeToCanaryCommands": False,
        "publishOnlyUnderCanaryBaseTopic": True,
        "allowDynamicPublishTopics": False,
        "allowRetainedCommands": False,
    }
    for key, expected in required.items():
        if safety.get(key) is not expected:
            raise SystemExit(f"ERRORE: requisito safety non rispettato: {key}")

    canary_base = str(plan["canaryBaseTopic"]).rstrip("/")
    subscriptions = plan.get("subscriptions", [])

    tab_id = stable_id("domoticsai", "bridge-v2-readonly")
    nodes: list[dict[str, Any]] = [
        {
            "id": tab_id,
            "type": "tab",
            "label": "DomoticsAI Production Bridge v2 — READ ONLY CANARY",
            "disabled": True,
            "info": (
                "Flow generato automaticamente.\n"
                "Stato iniziale: DISABLED.\n"
                "Nessun comando hardware.\n"
                f"Output ammesso solo sotto {canary_base}/..."
            ),
            "env": [],
        },
        {
            "id": stable_id(tab_id, "warning"),
            "type": "comment",
            "z": tab_id,
            "name": "⚠ READ-ONLY CANARY — FLOW DISABILITATO",
            "info": (
                "Non abilitare prima della revisione.\n"
                "Questo flow deve soltanto leggere topic sorgente e pubblicare copie normalizzate "
                f"nel namespace {canary_base}/..."
            ),
            "x": 300,
            "y": 40,
            "wires": [],
        },
    ]

    broker_nodes: dict[tuple[str, int], str] = {}

    def broker_id(host: str, port: int, label: str) -> str:
        key = (host, port)
        if key not in broker_nodes:
            node_id = stable_id("broker", host, str(port))
            broker_nodes[key] = node_id
            nodes.append(
                mqtt_broker_node(
                    node_id=node_id,
                    name=label,
                    host=host,
                    port=port,
                )
            )
        return broker_nodes[key]

    output_host = plan["sourceBrokers"]["domotics"]["host"]
    output_port = int(plan["sourceBrokers"]["domotics"]["port"])
    output_broker_id = broker_id(
        output_host,
        output_port,
        "DomoticsAI canary broker",
    )

    x_in = 180
    x_fn = 500
    x_out = 850
    y = 100

    generated_count = 0

    for index, item in enumerate(subscriptions):
        source_topic = str(item["sourceTopic"])
        destination_template = str(item["destinationTopicTemplate"])
        destination_topic = destination_template.replace(
            "${canaryBaseTopic}",
            canary_base,
        )

        if source_topic.endswith("/set") or "/cmnd/" in source_topic or "/command" in source_topic:
            raise SystemExit(f"ERRORE: comando incluso nel piano: {source_topic}")

        if not destination_topic.startswith(canary_base + "/"):
            raise SystemExit(
                f"ERRORE: destinazione fuori namespace canary: {destination_topic}"
            )

        source_broker = item.get("sourceBroker")
        if source_broker:
            host, port_text = source_broker.rsplit(":", 1)
            port = int(port_text)
        else:
            host = output_host
            port = output_port

        source_broker_id = broker_id(
            host,
            port,
            f"Source {host}:{port}",
        )

        domain = str(item.get("domain") or "unclassified")
        node_key = f"{domain}:{source_topic}:{destination_topic}:{index}"
        in_id = stable_id(node_key, "in")
        fn_id = stable_id(node_key, "guard")
        out_id = stable_id(node_key, "out")

        guard_code = (
            "const CANARY_BASE = "
            + json.dumps(canary_base)
            + ";\n"
            + "const SOURCE_TOPIC = "
            + json.dumps(source_topic)
            + ";\n"
            + "const DESTINATION_TOPIC = "
            + json.dumps(destination_topic)
            + ";\n\n"
            + "if (typeof msg.topic !== 'string') {\n"
            + "    node.warn('Topic sorgente mancante');\n"
            + "    return null;\n"
            + "}\n"
            + "if (msg.topic.startsWith(CANARY_BASE + '/')) {\n"
            + "    node.warn('Loop canary bloccato: ' + msg.topic);\n"
            + "    return null;\n"
            + "}\n"
            + "if (msg.topic !== SOURCE_TOPIC) {\n"
            + "    node.warn('Topic inatteso bloccato: ' + msg.topic);\n"
            + "    return null;\n"
            + "}\n"
            + "msg.domoticsai = {\n"
            + "    bridge: 'v2-readonly-canary',\n"
            + "    sourceTopic: SOURCE_TOPIC,\n"
            + "    observedAt: new Date().toISOString()\n"
            + "};\n"
            + "msg.topic = DESTINATION_TOPIC;\n"
            + "return msg;\n"
        )

        nodes.extend(
            [
                {
                    "id": in_id,
                    "type": "mqtt in",
                    "z": tab_id,
                    "name": f"[{domain}] {source_topic}",
                    "topic": source_topic,
                    "qos": "0",
                    "datatype": "auto-detect",
                    "broker": source_broker_id,
                    "nl": False,
                    "rap": True,
                    "rh": 0,
                    "inputs": 0,
                    "x": x_in,
                    "y": y,
                    "wires": [[fn_id]],
                    "d": True,
                },
                {
                    "id": fn_id,
                    "type": "function",
                    "z": tab_id,
                    "name": f"Guard + map → {destination_topic}",
                    "func": guard_code,
                    "outputs": 1,
                    "timeout": 0,
                    "noerr": 0,
                    "initialize": "",
                    "finalize": "",
                    "libs": [],
                    "x": x_fn,
                    "y": y,
                    "wires": [[out_id]],
                    "d": True,
                },
                {
                    "id": out_id,
                    "type": "mqtt out",
                    "z": tab_id,
                    "name": destination_topic,
                    "topic": "",
                    "qos": "0",
                    "retain": "true",
                    "respTopic": "",
                    "contentType": "",
                    "userProps": "",
                    "correl": "",
                    "expiry": "",
                    "broker": output_broker_id,
                    "x": x_out,
                    "y": y,
                    "wires": [],
                    "d": True,
                },
            ]
        )

        generated_count += 1
        y += 60

    metadata = {
        "generator": "generate_readonly_bridge_flow.py",
        "mode": plan["mode"],
        "canaryBaseTopic": canary_base,
        "generatedMappings": generated_count,
        "allOperationalNodesDisabled": True,
        "hardwareCommandsEnabled": False,
    }

    nodes.append(
        {
            "id": stable_id(tab_id, "metadata"),
            "type": "comment",
            "z": tab_id,
            "name": "Generation metadata",
            "info": json.dumps(metadata, indent=2, ensure_ascii=False),
            "x": 250,
            "y": y + 20,
            "wires": [],
        }
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(nodes, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("OK: flow Node-RED read-only canary generato.")
    print("Mapping:", generated_count)
    print("Nodi totali:", len(nodes))
    print("Stato operativo: DISABLED")
    print("Output:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
