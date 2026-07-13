#!/usr/bin/env python3
"""Estrae inventari di base da un export JSON di Node-RED.

Uso:
    python3 tools/extract_nodered_inventory.py flows.json output_dir
"""
from pathlib import Path
import sys, json, csv, re
from collections import Counter, defaultdict

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: extract_nodered_inventory.py INPUT.json OUTPUT_DIR")
    source = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    nodes = json.loads(source.read_text(encoding="utf-8"))
    tabs = {n["id"]: n.get("label") or n.get("name") or n["id"]
            for n in nodes if n.get("type") == "tab"}
    brokers = {n["id"]: n for n in nodes if n.get("type") == "mqtt-broker"}

    rows = []
    for n in nodes:
        if n.get("type") not in ("mqtt in", "mqtt out"):
            continue
        broker = brokers.get(n.get("broker"), {})
        rows.append({
            "node_id": n.get("id", ""),
            "direction": "SUBSCRIBE" if n.get("type") == "mqtt in" else "PUBLISH",
            "flow": tabs.get(n.get("z"), n.get("z", "")),
            "node_name": n.get("name", ""),
            "topic": n.get("topic", ""),
            "dynamic_topic": "yes" if n.get("type") == "mqtt out" and not n.get("topic") else "no",
            "qos": n.get("qos", ""),
            "retain": n.get("retain", ""),
            "broker_name": broker.get("name", ""),
            "broker_host": broker.get("broker", ""),
            "broker_port": broker.get("port", ""),
        })
    with (out / "mqtt_nodes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"Nodi: {len(nodes)}")
    print(f"Flow: {len(tabs)}")
    print(f"MQTT nodes: {len(rows)}")
    print(f"Creato: {out / 'mqtt_nodes.csv'}")

if __name__ == "__main__":
    main()
