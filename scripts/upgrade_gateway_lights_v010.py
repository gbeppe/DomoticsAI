#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import uuid

FLOW_FILE = Path("/home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway/flows.json")
SOURCE_BROKER_HOST = "192.168.1.20"
SOURCE_TOPIC = "zara/android/domotica/light/+/state"
LOCAL_BROKER_NAME = "DomoticsAI Test Broker"
TAB_LABEL = "03 Lights"

ACTIVE_DEVICES = {
    "tavolinoLettura": {"area": "internal", "type": "light", "label": "Tavolino lettura"},
    "libreria": {"area": "internal", "type": "light", "label": "Libreria"},
    "sala": {"area": "internal", "type": "light", "label": "Sala"},
    "televisione": {"area": "internal", "type": "light", "label": "Televisione"},
    "lavanderia": {"area": "internal", "type": "light", "label": "Lavanderia"},
    "ingressoServizio": {"area": "internal", "type": "light", "label": "Ingresso servizio"},
    "portico": {"area": "external", "type": "light", "label": "Portico"},
    "luciPiscina": {"area": "pool", "type": "light", "label": "Luci piscina"},
    "luciPedanaPiscina": {"area": "pool", "type": "light", "label": "Luci pedana piscina"},
    "skimmerPiscina": {"area": "pool", "type": "relay", "label": "Skimmer piscina"},
    "pompaPiscina": {"area": "pool", "type": "relay", "label": "Pompa piscina"},
}
SCENES = ["ALL_ON", "ALL_OFF", "TV_MODE", "SLEEP_MODE"]

def new_id():
    return uuid.uuid4().hex[:16]

def main():
    if not FLOW_FILE.exists():
        print(f"File non trovato: {FLOW_FILE}", file=sys.stderr)
        return 1

    nodes = json.loads(FLOW_FILE.read_text(encoding="utf-8"))

    if any(n.get("type") == "mqtt in" and n.get("name") == "Production Lights State" for n in nodes):
        print("Upgrade Lights v0.1.0 già applicato.")
        return 0

    source_broker = next((n for n in nodes if n.get("type") == "mqtt-broker" and n.get("broker") == SOURCE_BROKER_HOST), None)
    local_broker = next((n for n in nodes if n.get("type") == "mqtt-broker" and n.get("name") == LOCAL_BROKER_NAME), None)

    if source_broker is None or local_broker is None:
        print("Broker richiesti non trovati.", file=sys.stderr)
        return 1

    tab = next((n for n in nodes if n.get("type") == "tab" and n.get("label") == TAB_LABEL), None)
    if tab is None:
        tab = {"id": new_id(), "type": "tab", "label": TAB_LABEL, "disabled": False, "info": "Read-only lights adapter", "env": []}
        nodes.append(tab)

    mqtt_in_id = new_id()
    normalize_id = new_id()
    mqtt_out_id = new_id()
    inject_id = new_id()
    registry_id = new_id()
    registry_out_id = new_id()

    devices_js = json.dumps(ACTIVE_DEVICES, ensure_ascii=False)
    registry = json.dumps({
        "version": "1.0",
        "baseTopic": "zara/android/domotica",
        "devices": [{"id": k, **v} for k, v in ACTIVE_DEVICES.items()],
        "scenes": SCENES,
    }, ensure_ascii=False)

    normalize_func = f"""
const devices = {devices_js};
const match = msg.topic.match(/^zara\\/android\\/domotica\\/light\\/([^/]+)\\/state$/);
if (!match) return null;

const deviceId = match[1];
const metadata = devices[deviceId];
if (!metadata) {{
    node.warn(`Ignored inactive or unknown light device: ${{deviceId}}`);
    return null;
}}

const raw = String(msg.payload).trim().toUpperCase();
let state = null;
if (["ON", "1", "TRUE"].includes(raw)) state = "ON";
else if (["OFF", "0", "FALSE"].includes(raw)) state = "OFF";
else return null;

const sourceTopic = msg.topic;
msg.topic = `domoticsai/v1/state/lights/${{metadata.area}}/${{deviceId}}`;
msg.payload = JSON.stringify({{
    value: state,
    state: state,
    area: metadata.area,
    deviceType: metadata.type,
    label: metadata.label,
    quality: "good",
    source: "legacy",
    ts: new Date().toISOString(),
    sourceTopic: sourceTopic
}});
msg.qos = 1;
msg.retain = true;
return msg;
""".strip()

    registry_func = f"""
msg.topic = "domoticsai/v1/meta/lights/registry";
msg.payload = {json.dumps(registry)};
msg.qos = 1;
msg.retain = true;
return msg;
""".strip()

    nodes.extend([
        {"id": mqtt_in_id, "type": "mqtt in", "z": tab["id"], "name": "Production Lights State", "topic": SOURCE_TOPIC, "qos": "1", "datatype": "auto-detect", "broker": source_broker["id"], "nl": False, "rap": True, "rh": 0, "inputs": 0, "x": 180, "y": 120, "wires": [[normalize_id]]},
        {"id": normalize_id, "type": "function", "z": tab["id"], "name": "Normalize Active Lights", "func": normalize_func, "outputs": 1, "timeout": 0, "noerr": 0, "initialize": "", "finalize": "", "libs": [], "x": 470, "y": 120, "wires": [[mqtt_out_id]]},
        {"id": mqtt_out_id, "type": "mqtt out", "z": tab["id"], "name": "Publish Normalized Lights", "topic": "", "qos": "", "retain": "", "respTopic": "", "contentType": "", "userProps": "", "correl": "", "expiry": "", "broker": local_broker["id"], "x": 780, "y": 120, "wires": []},
        {"id": inject_id, "type": "inject", "z": tab["id"], "name": "Publish Lights Registry", "props": [{"p": "payload"}], "repeat": "", "crontab": "", "once": True, "onceDelay": 1, "topic": "", "payload": "", "payloadType": "date", "x": 190, "y": 220, "wires": [[registry_id]]},
        {"id": registry_id, "type": "function", "z": tab["id"], "name": "Build Lights Registry", "func": registry_func, "outputs": 1, "timeout": 0, "noerr": 0, "initialize": "", "finalize": "", "libs": [], "x": 470, "y": 220, "wires": [[registry_out_id]]},
        {"id": registry_out_id, "type": "mqtt out", "z": tab["id"], "name": "Publish Lights Registry", "topic": "", "qos": "", "retain": "", "respTopic": "", "contentType": "", "userProps": "", "correl": "", "expiry": "", "broker": local_broker["id"], "x": 780, "y": 220, "wires": []},
    ])

    FLOW_FILE.write_text(json.dumps(nodes, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Upgrade Lights v0.1.0 applicato.")
    print(f"Dispositivi attivi: {len(ACTIVE_DEVICES)}")
    print("Modalità: read-only")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
