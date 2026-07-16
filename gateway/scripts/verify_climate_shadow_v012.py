#!/usr/bin/env python3

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
FLOW_PATH = ROOT / "gateway" / "flows.json"


def main() -> int:
    flows = json.loads(
        FLOW_PATH.read_text(encoding="utf-8")
    )

    brokers = {
        str(node.get("id")): node
        for node in flows
        if node.get("type") == "mqtt-broker"
    }

    input_node = next(
        (
            node
            for node in flows
            if node.get("name")
            == "Production Climate Shadow Read Only"
        ),
        None,
    )

    mapper = next(
        (
            node
            for node in flows
            if node.get("name")
            == "Map Production Climate Shadow"
        ),
        None,
    )

    output_node = next(
        (
            node
            for node in flows
            if node.get("name")
            == "Publish Climate Shadow"
        ),
        None,
    )

    errors = []

    if input_node is None:
        errors.append(
            "input Climate shadow assente"
        )
    else:
        broker = brokers.get(
            str(input_node.get("broker")),
            {},
        )

        if broker.get("broker") != "192.168.1.20":
            errors.append(
                "input non collegato al broker reale"
            )

        if input_node.get("topic") != (
            "zara/android/domotica/#"
        ):
            errors.append(
                "topic input inatteso"
            )

    if mapper is None:
        errors.append(
            "mapper Climate shadow assente"
        )
    else:
        code = mapper.get("func", "")

        required_guards = [
            'relative.endsWith("/set")',
            'relative.includes("/set/")',
            "if (!rule)",
            'ingestionMode: "shadow"',
        ]

        for guard in required_guards:
            if guard not in code:
                errors.append(
                    f"guardia mancante: {guard}"
                )

    if output_node is None:
        errors.append(
            "output Climate shadow assente"
        )
    else:
        broker = brokers.get(
            str(output_node.get("broker")),
            {},
        )

        if not (
            broker.get("broker") == "127.0.0.1"
            and str(broker.get("port")) == "1883"
        ):
            errors.append(
                "output Climate non collegato "
                "al broker locale"
            )

    production_broker_ids = {
        str(node.get("id"))
        for node in flows
        if (
            node.get("type") == "mqtt-broker"
            and node.get("broker")
            == "192.168.1.20"
        )
    }

    dangerous_outputs = [
        node
        for node in flows
        if (
            node.get("type") == "mqtt out"
            and str(node.get("broker"))
            in production_broker_ids
        )
    ]

    if dangerous_outputs:
        errors.append(
            "esistono mqtt out verso "
            "192.168.1.20"
        )

    if errors:
        for error in errors:
            print(
                "ERRORE:",
                error,
                file=sys.stderr,
            )

        return 1

    print(
        "OK: Climate shadow read-only verificato."
    )
    print(
        "Nessun MQTT output verso 192.168.1.20."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
