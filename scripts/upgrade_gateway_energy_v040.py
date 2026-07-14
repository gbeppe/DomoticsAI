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
        and n.get("name") == "Legacy Grid Power"
        for n in nodes
    ):
        print("Upgrade energia già applicato.")
        return 0

    energy_tab = next(
        (n for n in nodes
         if n.get("type") == "tab"
         and n.get("label") == "02 Energy"),
        None,
    )
    local_broker = next(
        (n for n in nodes
         if n.get("type") == "mqtt-broker"
         and n.get("name") == "DomoticsAI Test Broker"),
        None,
    )
    source_broker = next(
        (n for n in nodes
         if n.get("type") == "mqtt-broker"
         and n.get("broker") == "192.168.1.15"),
        None,
    )

    if not energy_tab or not local_broker or not source_broker:
        print(
            "Tab Energy o broker richiesti non trovati.",
            file=sys.stderr,
        )
        return 1

    mqtt_in_id = new_id()
    function_id = new_id()
    mqtt_out_id = new_id()

    function_code = """
const config = global.get("domoticsai_config") || {
    baseTopic: "domoticsai/v1"
};

const gridPowerW = Number(msg.payload);

if (!Number.isFinite(gridPowerW)) {
    return null;
}

const timestamp = new Date().toISOString();

const gridMessage = {
    topic: `${config.baseTopic}/state/energy/grid_power_w`,
    payload: JSON.stringify({
        value: Math.abs(gridPowerW) < 20 ? 0 : gridPowerW,
        unit: "W",
        ts: timestamp,
        quality: "good",
        source: "legacy",
        semantics: "positive_import_negative_export"
    }),
    qos: 1,
    retain: true
};

const solarPowerW = Number(
    flow.get("energy_solar_power_w")
);
const homeLoadW = Number(
    flow.get("energy_home_load_w")
);

let batteryMessage = null;

if (
    Number.isFinite(solarPowerW) &&
    Number.isFinite(homeLoadW)
) {
    const batteryPowerW =
        homeLoadW - solarPowerW - gridPowerW;

    batteryMessage = {
        topic: `${config.baseTopic}/state/energy/battery_power_w`,
        payload: JSON.stringify({
            value: Math.abs(batteryPowerW) < 20
                ? 0
                : batteryPowerW,
            unit: "W",
            ts: timestamp,
            quality: "calculated",
            source: "gateway",
            semantics: "positive_discharge_negative_charge"
        }),
        qos: 1,
        retain: true
    };
}

return [gridMessage, batteryMessage];
""".strip()

    nodes.extend([
        {
            "id": mqtt_in_id,
            "type": "mqtt in",
            "z": energy_tab["id"],
            "name": "Legacy Grid Power",
            "topic": "TeslaPowerwall/site_instant_power",
            "qos": "1",
            "datatype": "auto-detect",
            "broker": source_broker["id"],
            "nl": False,
            "rap": True,
            "rh": 0,
            "inputs": 0,
            "x": 180,
            "y": 340,
            "wires": [[function_id]],
        },
        {
            "id": function_id,
            "type": "function",
            "z": energy_tab["id"],
            "name": "Normalize Grid and Battery Power",
            "func": function_code,
            "outputs": 2,
            "timeout": 0,
            "noerr": 0,
            "initialize": "",
            "finalize": "",
            "libs": [],
            "x": 500,
            "y": 340,
            "wires": [[mqtt_out_id], [mqtt_out_id]],
        },
        {
            "id": mqtt_out_id,
            "type": "mqtt out",
            "z": energy_tab["id"],
            "name": "Publish Grid and Battery Power",
            "topic": "",
            "qos": "",
            "retain": "",
            "respTopic": "",
            "contentType": "",
            "userProps": "",
            "correl": "",
            "expiry": "",
            "broker": local_broker["id"],
            "x": 820,
            "y": 340,
            "wires": [],
        },
    ])

    for node in nodes:
        if node.get("type") != "function":
            continue

        if node.get("name") == "Normalize Solar Power":
            marker = 'flow.set("energy_solar_power_w", value);'
            if marker not in node.get("func", ""):
                node["func"] = node["func"].replace(
                    'const unit = "W";',
                    'const unit = "W";\n'
                    'flow.set("energy_solar_power_w", value);',
                )

        if node.get("name") == "Normalize Home Load":
            marker = 'flow.set("energy_home_load_w", value);'
            if marker not in node.get("func", ""):
                node["func"] = node["func"].replace(
                    'const unit = "W";',
                    'const unit = "W";\n'
                    'flow.set("energy_home_load_w", value);',
                )

    FLOW_FILE.write_text(
        json.dumps(nodes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Upgrade energia v0.4.0 applicato.")
    print("Rete: positivo=import, negativo=export.")
    print("Batteria: positivo=scarica, negativo=carica.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
