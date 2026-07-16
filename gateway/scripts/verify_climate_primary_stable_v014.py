#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import json
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


EXPECTED_PRIMARY = {
    "env/tempLiving":
        "climate/living_temperature_c",
    "env/humidexLiving":
        "climate/living_humidex",
    "env/humidexBedroom":
        "climate/bedroom_humidex",
    "vmc/speed/state":
        "vmc/speed",
}


def main() -> int:
    flows = json.loads(
        FLOW_PATH.read_text(
            encoding="utf-8"
        )
    )

    mapping = json.loads(
        MAPPING_PATH.read_text(
            encoding="utf-8"
        )
    )

    errors: list[str] = []

    if mapping.get("mode") != (
        "READ_ONLY_PRIMARY"
    ):
        errors.append(
            "modalità mapping diversa da "
            "READ_ONLY_PRIMARY"
        )

    if mapping.get("canaryStatus") != (
        "PASSED"
    ):
        errors.append(
            "canaryStatus diverso da PASSED"
        )

    rules = {
        rule.get("source"): rule
        for rule in mapping.get(
            "rules",
            []
        )
    }

    for source, target in (
        EXPECTED_PRIMARY.items()
    ):
        rule = rules.get(source)

        if rule is None:
            errors.append(
                f"regola primaria assente: {source}"
            )
            continue

        if rule.get("target") != target:
            errors.append(
                f"{source}: target inatteso "
                f"{rule.get('target')}"
            )

        if rule.get("sourceRole") != (
            "primary"
        ):
            errors.append(
                f"{source}: sourceRole non primary"
            )

        if rule.get("ingestionMode") != (
            "primary"
        ):
            errors.append(
                f"{source}: ingestionMode "
                "non primary"
            )

        if rule.get("promotionStatus") != (
            "PRIMARY_STABLE"
        ):
            errors.append(
                f"{source}: promotionStatus "
                "non PRIMARY_STABLE"
            )

    mapper = next(
        (
            node
            for node in flows
            if (
                node.get("type") == "function"
                and node.get("name")
                == "Map Production Climate Shadow"
            )
        ),
        None,
    )

    if mapper is None:
        errors.append(
            "Function Node Climate assente"
        )
    else:
        code = mapper.get("func", "")

        required_fragments = (
            "rule.ingestionMode",
            "rule.sourceRole",
            'contractVersion:',
            '"climate-mapping-v1"',
        )

        for fragment in required_fragments:
            if fragment not in code:
                errors.append(
                    "metadato mapper assente: "
                    f"{fragment}"
                )

    brokers = {
        str(node.get("id")): node
        for node in flows
        if node.get("type") == "mqtt-broker"
    }

    production_ids = {
        broker_id
        for broker_id, broker
        in brokers.items()
        if broker.get("broker")
        == "192.168.1.20"
    }

    dangerous_outputs = [
        node.get("name") or node.get("id")
        for node in flows
        if (
            node.get("type") == "mqtt out"
            and str(node.get("broker"))
            in production_ids
        )
    ]

    if dangerous_outputs:
        errors.append(
            "mqtt out verso produzione: "
            + ", ".join(
                str(item)
                for item in dangerous_outputs
            )
        )

    legacy_targets = (
        "climate_legacy/"
        "living_temperature_c",
        "climate_legacy/"
        "living_humidex",
        "climate_legacy/"
        "bedroom_humidex",
        "vmc_legacy/speed",
    )

    all_function_code = "\n".join(
        node.get("func", "")
        for node in flows
        if node.get("type") == "function"
    )

    for target in legacy_targets:
        if target not in all_function_code:
            errors.append(
                f"fallback legacy assente: {target}"
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
        "OK: sorgente Climate primaria stabile."
    )
    print(
        "Canary: PASSED."
    )
    print(
        "Fallback legacy: presente."
    )
    print(
        "Nessun MQTT output verso "
        "192.168.1.20."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
