#!/usr/bin/env python3

from pathlib import Path
import json
import uuid


ROOT = Path(
    "/home/giuseppe/AndroidStudioProjects/"
    "DomoticsAI/gateway"
)

FLOW_PATH = ROOT / "flows.json"


def node_id() -> str:
    return uuid.uuid4().hex[:16]


def main() -> int:
    flows = json.loads(
        FLOW_PATH.read_text(
            encoding="utf-8"
        )
    )

    existing = {
        node.get("name")
        for node in flows
    }

    names = {
        "DomoticsAI Scenes Command In",
        "DomoticsAI Scenes Command Simulator",
        "DomoticsAI Scenes ACK Out",
    }

    if names.issubset(existing):
        print(
            "Simulatore scenari già presente."
        )
        return 0

    tab_id = None

    for node in flows:
        if (
            node.get("type") == "tab"
            and "DomoticsAI" in (
                node.get("label") or ""
            )
        ):
            tab_id = node["id"]
            break

    if tab_id is None:
        for node in flows:
            if node.get("type") == "tab":
                tab_id = node["id"]
                break

    if tab_id is None:
        raise RuntimeError(
            "Nessun tab Node-RED trovato"
        )

    mqtt_broker_id = None

    for node in flows:
        if node.get("type") in {
            "mqtt in",
            "mqtt out",
        }:
            mqtt_broker_id = node.get("broker")

            if mqtt_broker_id:
                break

    if mqtt_broker_id is None:
        raise RuntimeError(
            "Configurazione broker MQTT "
            "non trovata"
        )

    mqtt_in_id = node_id()
    function_id = node_id()
    mqtt_out_id = node_id()

    mqtt_in = {
        "id": mqtt_in_id,
        "type": "mqtt in",
        "z": tab_id,
        "name": (
            "DomoticsAI Scenes Command In"
        ),
        "topic": (
            "domoticsai/v1/cmd/scenes/+"
        ),
        "qos": "1",
        "datatype": "auto-detect",
        "broker": mqtt_broker_id,
        "nl": False,
        "rap": True,
        "rh": 0,
        "inputs": 0,
        "x": 230,
        "y": 760,
        "wires": [[function_id]],
    }

    function_code = r'''
const parts = msg.topic.split("/");
const sceneId = parts[parts.length - 1];

let data = msg.payload;

if (typeof data === "string") {
    try {
        data = JSON.parse(data);
    } catch (error) {
        data = {};
    }
}

const requestId =
    data.request_id || data.requestId;

if (!requestId) {
    node.warn(
        "Scene command without request_id"
    );
    return null;
}

msg.topic =
    "domoticsai/v1/ack/scenes/" +
    sceneId + "/" + requestId;

msg.payload = JSON.stringify({
    requestId: requestId,
    status: "simulated",
    message:
        "Scene command simulated",
    sceneId: sceneId
});

msg.qos = 1;
msg.retain = false;

return msg;
'''.strip()

    function_node = {
        "id": function_id,
        "type": "function",
        "z": tab_id,
        "name": (
            "DomoticsAI Scenes "
            "Command Simulator"
        ),
        "func": function_code,
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 560,
        "y": 760,
        "wires": [[mqtt_out_id]],
    }

    mqtt_out = {
        "id": mqtt_out_id,
        "type": "mqtt out",
        "z": tab_id,
        "name": (
            "DomoticsAI Scenes ACK Out"
        ),
        "topic": "",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": mqtt_broker_id,
        "x": 860,
        "y": 760,
        "wires": [],
    }

    flows.extend([
        mqtt_in,
        function_node,
        mqtt_out,
    ])

    FLOW_PATH.write_text(
        json.dumps(
            flows,
            ensure_ascii=False,
            indent=4,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "OK: simulatore comandi "
        "scenari aggiunto."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
