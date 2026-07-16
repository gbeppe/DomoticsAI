#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
import argparse
import json
import math


PAIRS = {
    "living_temperature_c": (
        "domoticsai/v1/state/climate/"
        "living_temperature_c",
        "domoticsai/v1/state/climate_shadow/"
        "living_temperature_c",
    ),
    "living_humidex": (
        "domoticsai/v1/state/climate/"
        "living_humidex",
        "domoticsai/v1/state/climate_shadow/"
        "living_humidex",
    ),
    "bedroom_humidex": (
        "domoticsai/v1/state/climate/"
        "bedroom_humidex",
        "domoticsai/v1/state/climate_shadow/"
        "bedroom_humidex",
    ),
    "vmc_speed": (
        "domoticsai/v1/state/vmc/speed",
        "domoticsai/v1/state/climate_shadow/"
        "vmc_speed",
    ),
}


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def parse_payload(
    raw: str,
) -> float | None:
    try:
        parsed = json.loads(
            raw
        )
    except json.JSONDecodeError:
        parsed = raw

    if isinstance(
        parsed,
        dict,
    ):
        parsed = parsed.get(
            "value"
        )

    try:
        value = float(parsed)
    except (
        TypeError,
        ValueError,
    ):
        return None

    if not math.isfinite(value):
        return None

    return value


def read_capture(
    path: Path,
) -> dict[str, list[float]]:
    values: dict[
        str,
        list[float],
    ] = defaultdict(list)

    for line in path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines():
        if not line.strip():
            continue

        parts = line.split(
            maxsplit=1
        )

        if len(parts) != 2:
            continue

        topic, payload = parts

        value = parse_payload(
            payload
        )

        if value is not None:
            values[topic].append(
                value
            )

    return values


def render(
    values: dict[str, list[float]],
    capture: Path,
) -> str:
    lines = [
        "# DomoticsAI — Climate Source Comparison",
        "",
        f"Generato: `{utc_now_iso()}`",
        "",
        f"Capture: `{capture}`",
        "",
        "| Grandezza | Campioni legacy | "
        "Media legacy | Campioni contract | "
        "Media contract | Delta medio assoluto |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for name, (
        legacy_topic,
        contract_topic,
    ) in PAIRS.items():
        legacy = values.get(
            legacy_topic,
            [],
        )

        contract = values.get(
            contract_topic,
            [],
        )

        legacy_mean = (
            mean(legacy)
            if legacy
            else None
        )

        contract_mean = (
            mean(contract)
            if contract
            else None
        )

        difference = (
            abs(
                legacy_mean
                - contract_mean
            )
            if (
                legacy_mean is not None
                and contract_mean
                is not None
            )
            else None
        )

        def fmt(value):
            return (
                "—"
                if value is None
                else f"{value:.3f}"
            )

        lines.append(
            f"| `{name}` "
            f"| `{len(legacy)}` "
            f"| `{fmt(legacy_mean)}` "
            f"| `{len(contract)}` "
            f"| `{fmt(contract_mean)}` "
            f"| `{fmt(difference)}` |"
        )

    lines.extend(
        [
            "",
            "## Interpretazione",
            "",
            "- Il confronto usa le medie dei "
            "campioni ricevuti nello stesso intervallo.",
            "- Un delta basso suggerisce che le "
            "sorgenti rappresentino la stessa misura.",
            "- Un delta elevato può indicare sensori, "
            "filtri o timestamp differenti.",
            "- Questo report non promuove "
            "automaticamente alcuna sorgente.",
            "",
        ]
    )

    return "\n".join(
        lines
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "capture",
        type=Path,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "docs/MQTT/"
            "CLIMATE_SOURCE_COMPARISON.md"
        ),
    )

    args = parser.parse_args()

    values = read_capture(
        args.capture
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        render(
            values,
            args.capture,
        ),
        encoding="utf-8",
    )

    print(
        "OK: confronto Climate generato:"
    )
    print(
        args.output
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
