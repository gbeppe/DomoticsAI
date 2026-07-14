from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import TwinValue


ACTIVE_DEVICES = {
    "internal/tavolinoLettura": {
        "area": "internal",
        "type": "light",
        "label": "Tavolino lettura",
    },
    "internal/libreria": {
        "area": "internal",
        "type": "light",
        "label": "Libreria",
    },
    "internal/sala": {
        "area": "internal",
        "type": "light",
        "label": "Sala",
    },
    "internal/televisione": {
        "area": "internal",
        "type": "light",
        "label": "Televisione",
    },
    "internal/lavanderia": {
        "area": "internal",
        "type": "light",
        "label": "Lavanderia",
    },
    "internal/ingressoServizio": {
        "area": "internal",
        "type": "light",
        "label": "Ingresso servizio",
    },
    "external/portico": {
        "area": "external",
        "type": "light",
        "label": "Portico",
    },
    "pool/luciPiscina": {
        "area": "pool",
        "type": "light",
        "label": "Luci piscina",
    },
    "pool/luciPedanaPiscina": {
        "area": "pool",
        "type": "light",
        "label": "Luci pedana piscina",
    },
    "pool/skimmerPiscina": {
        "area": "pool",
        "type": "relay",
        "label": "Skimmer piscina",
    },
    "pool/pompaPiscina": {
        "area": "pool",
        "type": "relay",
        "label": "Pompa piscina",
    },
}


def normalize_state(value: Any) -> str:
    if isinstance(value, bool):
        return "ON" if value else "OFF"

    if isinstance(value, (int, float)):
        return "ON" if value != 0 else "OFF"

    text = str(value).strip().upper()

    if text in {"ON", "1", "TRUE"}:
        return "ON"

    if text in {"OFF", "0", "FALSE"}:
        return "OFF"

    return "UNKNOWN"


def calculate_lights_derived(
    lights: dict[str, TwinValue],
) -> dict[str, Any]:
    devices: dict[str, dict[str, Any]] = {}

    area_totals = {
        "internal": {"total": 0, "on": 0},
        "external": {"total": 0, "on": 0},
        "pool": {"total": 0, "on": 0},
    }

    lights_on_total = 0
    relays_on_total = 0
    unknown_total = 0

    for entity_id, metadata in ACTIVE_DEVICES.items():
        item = lights.get(entity_id)
        state = (
            normalize_state(item.value)
            if item is not None
            else "UNKNOWN"
        )

        is_on = state == "ON"
        is_unknown = state == "UNKNOWN"
        device_type = metadata["type"]
        area = metadata["area"]

        area_totals[area]["total"] += 1
        if is_on:
            area_totals[area]["on"] += 1

        if is_unknown:
            unknown_total += 1
        elif is_on and device_type == "light":
            lights_on_total += 1
        elif is_on and device_type == "relay":
            relays_on_total += 1

        devices[entity_id] = {
            "id": entity_id.split("/", 1)[1],
            "area": area,
            "type": device_type,
            "label": metadata["label"],
            "state": state,
            "is_on": is_on,
            "available": item is not None,
            "quality": item.quality if item else "unknown",
            "timestamp": item.timestamp if item else None,
        }

    return {
        "devices": devices,
        "lights_on_total": lights_on_total,
        "relays_on_total": relays_on_total,
        "unknown_total": unknown_total,
        "internal_on": area_totals["internal"]["on"],
        "internal_total": area_totals["internal"]["total"],
        "external_on": area_totals["external"]["on"],
        "external_total": area_totals["external"]["total"],
        "pool_on": area_totals["pool"]["on"],
        "pool_total": area_totals["pool"]["total"],
        "any_internal_on": area_totals["internal"]["on"] > 0,
        "any_external_on": area_totals["external"]["on"] > 0,
        "any_pool_on": area_totals["pool"]["on"] > 0,
        "all_available": unknown_total == 0,
    }
