#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import uuid

FLOW_FILE = Path(
    "/home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway/flows.json"
)

def new_id():
    return uuid.uuid4().hex[:16]

def main():
    if not FLOW_FILE.exists():
        print(f"File non trovato: {FLOW_FILE}", file=sys.stderr)
        return 1

    nodes = json.loads(FLOW_FILE.read_text(encoding="utf-8"))

    if any(
        n.get("type") == "mqtt in"
        and n.get("name") == "Simulated Lights Commands"
        for n in nodes
    ):
        print("Simulatore già installato.")
        return 0

    local_broker = next(
        (n for n in nodes
         if n.get("type") == "mqtt-broker"
         and n.get("name") == "DomoticsAI Test Broker"),
        None,
    )
    tab = next(
        (n for n in nodes
         if n.get("type") == "tab"
         and n.get("label") == "03 Lights"),
        None,
    )

    if local_broker is None or tab is None:
        print("Broker locale o tab 03 Lights non trovato.", file=sys.stderr)
        return 1

    mqtt_in_id = new_id()
    function_id = new_id()
    mqtt_out_id = new_id()

    function_code = r"""
let command;
try {
    command = JSON.parse(msg.payload);
} catch (error) {
    return null;
}

const match = msg.topic.match(
    /^domoticsai\/v1\/cmd\/lights\/([^/]+)\/([^/]+)$/
);
if (!match) return null;

const area = match[1];
const deviceId = match[2];

if (command.mode !== "simulation") {
    return null;
}

msg.topic =
    `domoticsai/v1/ack/lights/${area}/${deviceId}/${command.request_id}`;

msg.payload = JSON.stringify({
    requestId: command.request_id,
    status: "simulated",
    area: area,
    deviceId: deviceId,
    desiredState: command.desired_state,
    message: "Validated, not sent to production",
    ts: new Date().toISOString()
});

msg.qos = 1;
msg.retain = false;
return msg;
""".strip()

    nodes.extend([
        {
            "id": mqtt_in_id,
            "type": "mqtt in",
            "z": tab["id"],
            "name": "Simulated Lights Commands",
            "topic": "domoticsai/v1/cmd/lights/+/+",
            "qos": "1",
            "datatype": "auto-detect",
            "broker": local_broker["id"],
            "nl": False,
            "rap": True,
            "rh": 0,
            "inputs": 0,
            "x": 190,
            "y": 320,
            "wires": [[function_id]],
        },
        {
            "id": function_id,
            "type": "function",
            "z": tab["id"],
            "name": "Validate and Simulate Light Command",
            "func": function_code,
            "outputs": 1,
            "timeout": 0,
            "noerr": 0,
            "initialize": "",
            "finalize": "",
            "libs": [],
            "x": 510,
            "y": 320,
            "wires": [[mqtt_out_id]],
        },
        {
            "id": mqtt_out_id,
            "type": "mqtt out",
            "z": tab["id"],
            "name": "Publish Simulated Light Ack",
            "topic": "",
            "qos": "",
            "retain": "",
            "respTopic": "",
            "contentType": "",
            "userProps": "",
            "correl": "",
            "expiry": "",
            "broker": local_broker["id"],
            "x": 830,
            "y": 320,
            "wires": [],
        },
    ])

    FLOW_FILE.write_text(
        json.dumps(nodes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("Simulatore comandi luci installato.")
    print("Nessun comando verso produzione.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
