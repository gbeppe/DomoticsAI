#!/usr/bin/env python3
from pathlib import Path
import json

FLOW_FILE = Path("/home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway/flows.json")
EXPECTED = {
    "tavolinoLettura", "libreria", "sala", "televisione",
    "lavanderia", "ingressoServizio", "portico",
    "luciPiscina", "luciPedanaPiscina",
    "skimmerPiscina", "pompaPiscina",
}
FORBIDDEN = {"lampadaHifi", "cucina", "esterno"}

nodes = json.loads(FLOW_FILE.read_text(encoding="utf-8"))
normalize = next((n for n in nodes if n.get("type") == "function" and n.get("name") == "Normalize Active Lights"), None)
if normalize is None:
    raise SystemExit("ERRORE: Normalize Active Lights non trovato")

code = normalize.get("func", "")
missing = sorted(d for d in EXPECTED if d not in code)
forbidden = sorted(d for d in FORBIDDEN if d in code)

broker_by_id = {n.get("id"): n for n in nodes if n.get("type") == "mqtt-broker"}
bad_outputs = []
for node in nodes:
    if node.get("type") == "mqtt out":
        broker = broker_by_id.get(node.get("broker"), {})
        if broker.get("broker") in {"192.168.1.20", "192.168.1.15"}:
            bad_outputs.append(node.get("name", node.get("id")))

errors = []
if missing:
    errors.append("Dispositivi mancanti: " + ", ".join(missing))
if forbidden:
    errors.append("Dispositivi obsoleti presenti: " + ", ".join(forbidden))
if bad_outputs:
    errors.append("Output verso produzione: " + ", ".join(bad_outputs))

if errors:
    for e in errors:
        print("ERRORE:", e)
    raise SystemExit(1)

print("OK: dispositivi attivi presenti.")
print("OK: dispositivi obsoleti esclusi.")
print("OK: nessun MQTT output verso produzione.")
