#!/usr/bin/env python3
from pathlib import Path
import json, sys

flow = Path(__file__).resolve().parents[1] / "flows.json"
nodes = json.loads(flow.read_text(encoding="utf-8"))
brokers = {n["id"]: n for n in nodes if n.get("type") == "mqtt-broker"}

errors = []
for n in nodes:
    if n.get("type") == "mqtt out":
        host = brokers.get(n.get("broker"), {}).get("broker")
        if host in {"192.168.1.20", "192.168.1.15"}:
            errors.append((n.get("name"), host))

if errors:
    print("ERRORE: MQTT output verso broker di produzione:")
    for name, host in errors:
        print(f"- {name}: {host}")
    sys.exit(1)

print("OK: nessun MQTT output punta ai broker di produzione.")
