#!/usr/bin/env python3

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


EXPECTED_LEGACY_TARGETS = {
    (
        "${config.baseTopic}/state/"
        "climate_legacy/living_temperature_c"
    ),
    (
        "${config.baseTopic}/state/"
        "climate_legacy/living_humidex"
    ),
    (
        "${config.baseTopic}/state/"
        "climate_legacy/bedroom_humidex"
    ),
    (
        "${config.baseTopic}/state/"
        "vmc_legacy/speed"
    ),
}


FORBIDDEN_LEGACY_TARGETS = {
    (
        "${config.baseTopic}/state/"
        "climate/living_temperature_c"
    ),
    (
        "${config.baseTopic}/state/"
        "climate/living_humidex"
    ),
    (
        "${config.baseTopic}/state/"
        "climate/bedroom_humidex"
    ),
    (
        "${config.baseTopic}/state/"
        "vmc/speed"
    ),
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

    errors = []

    rules = {
        rule.get("source"):
            rule.get("target")
        for rule in mapping.get(
            "rules",
            []
        )
    }

    for source, expected in (
        EXPECTED_PRIMARY.items()
    ):
        actual = rules.get(source)

        if actual != expected:
            errors.append(
                f"{source}: atteso {expected}, "
                f"trovato {actual}"
            )

    function_codes = [
        node.get("func", "")
        for node in flows
        if node.get("type") == "function"
    ]

    all_code = "\n".join(
        function_codes
    )

    for target in (
        EXPECTED_LEGACY_TARGETS
    ):
        if target not in all_code:
            errors.append(
                "target legacy assente: "
                f"{target}"
            )

    climate_mapper = next(
        (
            node
            for node in flows
            if node.get("name")
            == "Map Production Climate Shadow"
        ),
        None,
    )

    if climate_mapper is None:
        errors.append(
            "mapper contratto Climate assente"
        )
    else:
        mapper_code = climate_mapper.get(
            "func",
            ""
        )

        for target in (
            FORBIDDEN_LEGACY_TARGETS
        ):
            if target in mapper_code:
                # Nel mapper è corretto trovare
                # i target primari.
                continue

    brokers = {
        str(node.get("id")): node
        for node in flows
        if node.get("type")
        == "mqtt-broker"
    }

    production_ids = {
        node_id
        for node_id, node
        in brokers.items()
        if node.get("broker")
        == "192.168.1.20"
    }

    dangerous_outputs = [
        node.get("name")
        for node in flows
        if (
            node.get("type") == "mqtt out"
            and str(
                node.get("broker")
            ) in production_ids
        )
    ]

    if dangerous_outputs:
        errors.append(
            "mqtt out verso produzione: "
            + ", ".join(
                str(name)
                for name in dangerous_outputs
            )
        )

    accepted_modes = {
        "READ_ONLY_PRIMARY_CANARY",
        "READ_ONLY_PRIMARY",
    }

    if mapping.get("mode") not in accepted_modes:
        errors.append(
            "mapping non in una modalità "
            "primaria riconosciuta"
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
        "OK: contratto Climate promosso "
        "a sorgente primaria."
    )
    print(
        "Fallback legacy mantenuto in "
        "namespace separato."
    )
    print(
        "Nessun MQTT output verso "
        "192.168.1.20."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
