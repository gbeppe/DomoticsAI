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


PRIMARY_RULES = {
    "env/tempLiving": (
        "climate/living_temperature_c"
    ),
    "env/humidexLiving": (
        "climate/living_humidex"
    ),
    "env/humidexBedroom": (
        "climate/bedroom_humidex"
    ),
    "vmc/speed/state": (
        "vmc/speed"
    ),
}


LEGACY_TOPIC_REPLACEMENTS = {
    (
        "${config.baseTopic}/state/"
        "climate/living_temperature_c"
    ): (
        "${config.baseTopic}/state/"
        "climate_legacy/living_temperature_c"
    ),
    (
        "${config.baseTopic}/state/"
        "climate/living_humidex"
    ): (
        "${config.baseTopic}/state/"
        "climate_legacy/living_humidex"
    ),
    (
        "${config.baseTopic}/state/"
        "climate/bedroom_humidex"
    ): (
        "${config.baseTopic}/state/"
        "climate_legacy/bedroom_humidex"
    ),
    (
        "${config.baseTopic}/state/"
        "vmc/speed"
    ): (
        "${config.baseTopic}/state/"
        "vmc_legacy/speed"
    ),
}


EXPECTED_LEGACY_INPUTS = {
    "Legacy Living Temperature",
    "Legacy Living Humidex",
    "Legacy Bedroom Humidex",
    "Legacy VMC Speed",
}


def timestamp() -> str:
    return datetime.now(
        timezone.utc
    ).strftime("%Y%m%d-%H%M%S")


def load_json(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def main() -> int:
    flows = load_json(
        FLOW_PATH
    )

    mapping = load_json(
        MAPPING_PATH
    )

    if not isinstance(flows, list):
        print(
            "ERRORE: flows.json non contiene "
            "una lista.",
            file=sys.stderr,
        )
        return 1

    rules = mapping.get(
        "rules",
        []
    )

    rules_by_source = {
        rule.get("source"): rule
        for rule in rules
    }

    missing_rules = sorted(
        set(PRIMARY_RULES)
        - set(rules_by_source)
    )

    if missing_rules:
        for source in missing_rules:
            print(
                "ERRORE: regola assente:",
                source,
                file=sys.stderr,
            )

        return 1

    backup = FLOW_PATH.with_name(
        ".flows.json.before-climate-primary-v013-"
        f"{timestamp()}"
    )

    mapping_backup = (
        MAPPING_PATH.with_name(
            ".climate-shadow-mapping-v1.json."
            "before-primary-v013-"
            f"{timestamp()}"
        )
    )

    shutil.copy2(
        FLOW_PATH,
        backup,
    )

    shutil.copy2(
        MAPPING_PATH,
        mapping_backup,
    )

    changed_mapping = 0

    for source, target in (
        PRIMARY_RULES.items()
    ):
        rule = rules_by_source[source]

        if rule.get("target") != target:
            rule["target"] = target
            changed_mapping += 1

        rule["promotionStatus"] = (
            "PRIMARY_CANARY"
        )

    mapping["mode"] = (
        "READ_ONLY_PRIMARY_CANARY"
    )

    mapping["primarySource"] = (
        "production_application_contract"
    )

    mapping["legacyFallbackEnabled"] = True

    mapping["promotedTopics"] = sorted(
        PRIMARY_RULES
    )

    legacy_function_targets = {
        "Normalize Living Temperature": (
            "${config.baseTopic}/state/"
            "climate/living_temperature_c",
            "${config.baseTopic}/state/"
            "climate_legacy/living_temperature_c",
        ),
        "Normalize Living Humidex": (
            "${config.baseTopic}/state/"
            "climate/living_humidex",
            "${config.baseTopic}/state/"
            "climate_legacy/living_humidex",
        ),
        "Normalize Bedroom Humidex": (
            "${config.baseTopic}/state/"
            "climate/bedroom_humidex",
            "${config.baseTopic}/state/"
            "climate_legacy/bedroom_humidex",
        ),
        "Normalize VMC Speed": (
            "${config.baseTopic}/state/"
            "vmc/speed",
            "${config.baseTopic}/state/"
            "vmc_legacy/speed",
        ),
    }

    function_nodes = {
        node.get("name"): node
        for node in flows
        if node.get("type") == "function"
    }

    changed_functions = []

    for name, (
        old_target,
        new_target,
    ) in legacy_function_targets.items():
        node = function_nodes.get(name)

        if node is None:
            print(
                "ERRORE: funzione legacy assente:",
                name,
                file=sys.stderr,
            )
            return 1

        code = node.get(
            "func",
            ""
        )

        if new_target in code:
            # Consente una riesecuzione sicura.
            changed_functions.append(name)
            continue

        if old_target not in code:
            print(
                "ERRORE: target primario non trovato "
                f"nella funzione {name}.",
                file=sys.stderr,
            )
            return 1

        node["func"] = code.replace(
            old_target,
            new_target,
            1,
        )

        changed_functions.append(name)

    missing_inputs = []

    input_names = {
        node.get("name")
        for node in flows
        if node.get("type") == "mqtt in"
    }

    for expected in (
        EXPECTED_LEGACY_INPUTS
    ):
        if expected not in input_names:
            missing_inputs.append(
                expected
            )

    if missing_inputs:
        for name in missing_inputs:
            print(
                "ERRORE: input legacy assente:",
                name,
                file=sys.stderr,
            )

        return 1

    if len(changed_functions) != 4:
        print(
            "ERRORE: attese 4 funzioni legacy "
            "modificate, trovate "
            f"{len(changed_functions)}.",
            file=sys.stderr,
        )

        print(
            "Funzioni:",
            changed_functions,
            file=sys.stderr,
        )

        return 1

    MAPPING_PATH.write_text(
        json.dumps(
            mapping,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
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
        "OK: promozione Climate preparata."
    )
    print(
        "Regole primarie aggiornate:",
        changed_mapping,
    )
    print(
        "Funzioni legacy spostate:",
        len(changed_functions),
    )

    for name in changed_functions:
        print(" -", name)

    print("Backup flow:", backup)
    print(
        "Backup mapping:",
        mapping_backup,
    )
    print()
    print(
        "Il contratto alimenterà climate/* "
        "e vmc/*."
    )
    print(
        "Le vecchie sorgenti alimenteranno "
        "climate_legacy/* e vmc_legacy/*."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
