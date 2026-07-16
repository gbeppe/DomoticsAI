#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

PATH = (
    ROOT
    / "config"
    / "mqtt"
    / "application-contract-v1.json"
)


def fail(
    message: str,
) -> None:
    print(
        f"ERRORE: {message}",
        file=sys.stderr,
    )


def main() -> int:
    contract = json.loads(
        PATH.read_text(
            encoding="utf-8"
        )
    )

    errors: list[str] = []

    base_topic = (
        contract
        .get("baseTopic", {})
        .get("default", "")
        .strip()
        .strip("/")
    )

    if not base_topic:
        errors.append(
            "baseTopic.default vuoto"
        )

    if "#" in base_topic or "+" in base_topic:
        errors.append(
            "baseTopic.default contiene wildcard"
        )

    patterns = [
        item.get("pattern", "")
        for item in contract.get(
            "topics",
            []
        )
    ]

    duplicates = sorted(
        {
            pattern
            for pattern in patterns
            if patterns.count(pattern) > 1
        }
    )

    for duplicate in duplicates:
        errors.append(
            f"pattern duplicato: {duplicate}"
        )

    lights = (
        contract
        .get("devices", {})
        .get("lights", {})
    )

    active_groups = (
        "internal",
        "external",
        "pool",
    )

    active_devices: list[str] = []

    for group in active_groups:
        values = lights.get(group, [])

        if len(values) != len(set(values)):
            errors.append(
                f"duplicati nel gruppo {group}"
            )

        active_devices.extend(values)

    active_duplicates = sorted(
        {
            device
            for device in active_devices
            if active_devices.count(device) > 1
        }
    )

    for duplicate in active_duplicates:
        errors.append(
            "dispositivo presente in più gruppi: "
            f"{duplicate}"
        )

    inactive = set(
        lights.get(
            "historicalInactive",
            []
        )
    )

    overlap = sorted(
        inactive.intersection(
            active_devices
        )
    )

    for device in overlap:
        errors.append(
            "dispositivo attivo e storico insieme: "
            f"{device}"
        )

    if errors:
        for error in errors:
            fail(error)

        return 1

    print(
        "OK: contratto MQTT valido."
    )
    print("Base topic:", base_topic)
    print(
        "Pattern:",
        len(patterns),
    )
    print(
        "Dispositivi attivi:",
        len(active_devices),
    )
    print(
        "Dispositivi storici:",
        len(inactive),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
