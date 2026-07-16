#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import sys


ROOT = Path(__file__).resolve().parents[2]

FLOW_PATH = (
    ROOT
    / "gateway"
    / "flows.json"
)

MAPPING_PATH = (
    ROOT
    / "config"
    / "mqtt"
    / "climate-shadow-mapping-v1.json"
)

INPUT_ID = "climateshadowinputv012"
FUNCTION_ID = "climateshadowmapv012"
OUTPUT_ID = "climateshadowoutputv012"


def now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).strftime("%Y%m%d-%H%M%S")


def load_json(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def build_function_code(
    *,
    source_base: str,
    target_base: str,
    rules: dict,
) -> str:
    rules_json = json.dumps(
        rules,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    return f'''const sourceBase = {json.dumps(source_base)};
const targetBase = {json.dumps(target_base)};
const rules = {rules_json};

const prefix = sourceBase + "/";

if (!msg.topic.startsWith(prefix)) {{
    return null;
}}

const relative = msg.topic.slice(prefix.length);

if (
    relative.endsWith("/set") ||
    relative.includes("/set/")
) {{
    return null;
}}

const rule = rules[relative];

if (!rule) {{
    return null;
}}

const rawPayload = msg.payload;
let value;

if (rule.type === "number") {{
    value = Number(rawPayload);

    if (!Number.isFinite(value)) {{
        node.warn(
            `Invalid numeric Climate payload: ${{msg.topic}}`
        );
        return null;
    }}
}} else if (rule.type === "boolean") {{
    const normalized =
        String(rawPayload)
            .trim()
            .toUpperCase();

    if (
        ["TRUE", "ON", "1"]
            .includes(normalized)
    ) {{
        value = true;
    }} else if (
        ["FALSE", "OFF", "0"]
            .includes(normalized)
    ) {{
        value = false;
    }} else {{
        node.warn(
            `Invalid boolean Climate payload: ${{msg.topic}}`
        );
        return null;
    }}
}} else if (
    rule.type === "json_object"
) {{
    try {{
        value =
            typeof rawPayload === "object"
                ? rawPayload
                : JSON.parse(
                    String(rawPayload)
                );
    }} catch (error) {{
        node.warn(
            `Invalid JSON Climate payload: ${{msg.topic}}`
        );
        return null;
    }}

    if (
        value === null ||
        Array.isArray(value) ||
        typeof value !== "object"
    ) {{
        return null;
    }}
}} else {{
    value = String(rawPayload);
}}

const sourceTopic = msg.topic;

msg.topic =
    `${{targetBase}}/${{rule.target}}`;

msg.payload = JSON.stringify({{
    value: value,
    unit: rule.unit,
    quality: "good",
    source:
        "production_application_contract",
    sourceTopic: sourceTopic,
    ts: new Date().toISOString(),
    ingestionMode:
        rule.ingestionMode,
    sourceRole:
        rule.sourceRole,
    contractVersion:
        "climate-mapping-v1"
}});

msg.qos = 1;
msg.retain = true;

return msg;'''


def main() -> int:
    flows = load_json(
        FLOW_PATH
    )

    mapping = load_json(
        MAPPING_PATH
    )

    if not isinstance(
        flows,
        list,
    ):
        print(
            "ERRORE: flows.json non contiene "
            "una lista.",
            file=sys.stderr,
        )
        return 1

    production_broker = next(
        (
            node
            for node in flows
            if (
                node.get("type")
                == "mqtt-broker"
                and node.get("broker")
                == "192.168.1.20"
            )
        ),
        None,
    )

    local_broker = next(
        (
            node
            for node in flows
            if (
                node.get("type")
                == "mqtt-broker"
                and node.get("broker")
                == "127.0.0.1"
                and str(
                    node.get("port")
                )
                == "1883"
            )
        ),
        None,
    )

    lights_input = next(
        (
            node
            for node in flows
            if node.get("name")
            == "Production Lights State"
        ),
        None,
    )

    if production_broker is None:
        print(
            "ERRORE: broker produzione "
            "192.168.1.20 non trovato.",
            file=sys.stderr,
        )
        return 1

    if local_broker is None:
        print(
            "ERRORE: broker locale "
            "127.0.0.1:1883 non trovato.",
            file=sys.stderr,
        )
        return 1

    if lights_input is None:
        print(
            "ERRORE: nodo Production Lights "
            "State non trovato.",
            file=sys.stderr,
        )
        return 1

    tab_id = lights_input.get("z")

    if not tab_id:
        print(
            "ERRORE: tab Gateway non risolta.",
            file=sys.stderr,
        )
        return 1

    source_base = (
        mapping["sourceBaseTopic"]
        .strip()
        .strip("/")
    )

    target_base = (
        mapping["targetBaseTopic"]
        .strip()
        .strip("/")
    )

    rules = {
        rule["source"]: {
            "target": rule["target"],
            "type": rule["type"],
            "unit": rule.get("unit"),
            "sourceRole": rule.get(
                "sourceRole",
                "supplemental",
            ),
            "ingestionMode": rule.get(
                "ingestionMode",
                "primary",
            ),
        }
        for rule in mapping["rules"]
    }

    function_code = (
        build_function_code(
            source_base=source_base,
            target_base=target_base,
            rules=rules,
        )
    )

    nodes_by_id = {
        str(node.get("id")): node
        for node in flows
    }

    input_node = nodes_by_id.get(
        INPUT_ID
    )

    function_node = nodes_by_id.get(
        FUNCTION_ID
    )

    output_node = nodes_by_id.get(
        OUTPUT_ID
    )

    backup = FLOW_PATH.with_name(
        ".flows.json.before-climate-v012-"
        f"{now_iso()}"
    )

    shutil.copy2(
        FLOW_PATH,
        backup,
    )

    if input_node is None:
        input_node = {
            "id": INPUT_ID,
            "type": "mqtt in",
            "z": tab_id,
            "name": (
                "Production Climate "
                "Shadow Read Only"
            ),
            "topic": (
                f"{source_base}/#"
            ),
            "qos": "1",
            "datatype": "auto-detect",
            "broker":
                production_broker["id"],
            "nl": False,
            "rap": True,
            "rh": 0,
            "inputs": 0,
            "x": 230,
            "y": 1540,
            "wires": [
                [FUNCTION_ID]
            ],
        }

        flows.append(
            input_node
        )
    else:
        input_node.update(
            {
                "topic":
                    f"{source_base}/#",
                "broker":
                    production_broker["id"],
                "wires":
                    [[FUNCTION_ID]],
            }
        )

    if function_node is None:
        function_node = {
            "id": FUNCTION_ID,
            "type": "function",
            "z": tab_id,
            "name": (
                "Map Production "
                "Climate Shadow"
            ),
            "func": function_code,
            "outputs": 1,
            "timeout": 0,
            "noerr": 0,
            "initialize": "",
            "finalize": "",
            "libs": [],
            "x": 570,
            "y": 1540,
            "wires": [
                [OUTPUT_ID]
            ],
        }

        flows.append(
            function_node
        )
    else:
        function_node.update(
            {
                "func": function_code,
                "wires":
                    [[OUTPUT_ID]],
            }
        )

    if output_node is None:
        output_node = {
            "id": OUTPUT_ID,
            "type": "mqtt out",
            "z": tab_id,
            "name":
                "Publish Climate Shadow",
            "topic": "",
            "qos": "",
            "retain": "",
            "respTopic": "",
            "contentType": "",
            "userProps": "",
            "correl": "",
            "expiry": "",
            "broker":
                local_broker["id"],
            "x": 890,
            "y": 1540,
            "wires": [],
        }

        flows.append(
            output_node
        )
    else:
        output_node.update(
            {
                "broker":
                    local_broker["id"],
            }
        )

    FLOW_PATH.write_text(
        json.dumps(
            flows,
            indent=4,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "OK: Climate shadow ingestion "
        "installata o aggiornata."
    )
    print("Backup:", backup)
    print("Regole:", len(rules))
    print(
        "Input:",
        f"{source_base}/#",
    )
    print(
        "Output:",
        f"{target_base}/...",
    )
    print(
        "Nessun output verso "
        "il broker reale."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
