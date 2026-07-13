#!/usr/bin/env python3
from pathlib import Path
import json
import sys

FLOW_FILE = Path(
    "/home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway/flows.json"
)
NEW_HOST = "192.168.1.40"
NEW_PORT = "1883"

if not FLOW_FILE.exists():
    print(f"File non trovato: {FLOW_FILE}", file=sys.stderr)
    sys.exit(1)

nodes = json.loads(FLOW_FILE.read_text(encoding="utf-8"))

matches = [
    node for node in nodes
    if node.get("type") == "mqtt-broker"
    and (
        node.get("name") == "DomoticsAI Test Broker"
        or node.get("broker") == "127.0.0.1"
    )
]

if not matches:
    print("Nessun broker test trovato.", file=sys.stderr)
    sys.exit(1)

for broker in matches:
    broker["broker"] = NEW_HOST
    broker["port"] = NEW_PORT

FLOW_FILE.write_text(
    json.dumps(nodes, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(
    f"OK: aggiornati {len(matches)} broker test a "
    f"{NEW_HOST}:{NEW_PORT}"
)
