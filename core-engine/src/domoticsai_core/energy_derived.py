from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import TwinValue

DEADBAND_W = 20.0

@dataclass(frozen=True)
class EnergyRaw:
    solar_power_w: float | None
    home_load_w: float | None
    grid_power_w: float | None
    battery_power_w: float | None
    powerwall_soc_pct: float | None

def _number(domain: dict[str, TwinValue], entity: str) -> float | None:
    item = domain.get(entity)
    if item is None or isinstance(item.value, bool):
        return None
    if isinstance(item.value, (int, float)):
        return float(item.value)
    if isinstance(item.value, str):
        try:
            return float(item.value)
        except ValueError:
            return None
    return None

def read_energy_raw(domain: dict[str, TwinValue]) -> EnergyRaw:
    return EnergyRaw(
        solar_power_w=_number(domain, "solar_power_w"),
        home_load_w=_number(domain, "home_load_w"),
        grid_power_w=_number(domain, "grid_power_w"),
        battery_power_w=_number(domain, "battery_power_w"),
        powerwall_soc_pct=_number(domain, "powerwall_soc_pct"),
    )

def direction(value, positive, negative):
    if value is None:
        return "unknown"
    if value > DEADBAND_W:
        return positive
    if value < -DEADBAND_W:
        return negative
    return "idle"

def calculate_energy_derived(raw: EnergyRaw) -> dict[str, Any]:
    grid_direction = direction(
        raw.grid_power_w,
        "importing",
        "exporting",
    )
    battery_direction = direction(
        raw.battery_power_w,
        "discharging",
        "charging",
    )

    solar = max(raw.solar_power_w or 0.0, 0.0)
    load = max(raw.home_load_w or 0.0, 0.0)

    grid_import_w = (
        max(raw.grid_power_w or 0.0, 0.0)
        if raw.grid_power_w is not None else None
    )
    grid_export_w = (
        max(-(raw.grid_power_w or 0.0), 0.0)
        if raw.grid_power_w is not None else None
    )
    battery_discharge_w = (
        max(raw.battery_power_w or 0.0, 0.0)
        if raw.battery_power_w is not None else None
    )
    battery_charge_w = (
        max(-(raw.battery_power_w or 0.0), 0.0)
        if raw.battery_power_w is not None else None
    )

    self_consumption_pct = None
    if solar > DEADBAND_W:
        self_consumption_pct = min(
            max((solar - (grid_export_w or 0.0)) / solar * 100.0, 0.0),
            100.0,
        )

    self_sufficiency_pct = None
    if load > DEADBAND_W:
        self_sufficiency_pct = min(
            max((load - (grid_import_w or 0.0)) / load * 100.0, 0.0),
            100.0,
        )

    balance_error_w = None
    if all(v is not None for v in (
        raw.solar_power_w,
        raw.home_load_w,
        raw.grid_power_w,
        raw.battery_power_w,
    )):
        balance_error_w = (
            raw.solar_power_w
            + raw.grid_power_w
            + raw.battery_power_w
            - raw.home_load_w
        )

    if (
        solar > DEADBAND_W
        and battery_direction == "charging"
        and grid_direction == "exporting"
    ):
        mode = "solar_charging_and_exporting"
    elif solar > DEADBAND_W and battery_direction == "charging":
        mode = "solar_charging_battery"
    elif solar > DEADBAND_W and grid_direction == "exporting":
        mode = "solar_exporting"
    elif battery_direction == "discharging" and grid_direction != "importing":
        mode = "battery_supplying_home"
    elif grid_direction == "importing":
        mode = "grid_supplying_home"
    elif solar > DEADBAND_W:
        mode = "solar_supplying_home"
    else:
        mode = "idle"

    return {
        "grid_direction": grid_direction,
        "battery_direction": battery_direction,
        "grid_import_w": grid_import_w,
        "grid_export_w": grid_export_w,
        "battery_charge_w": battery_charge_w,
        "battery_discharge_w": battery_discharge_w,
        "self_consumption_pct": self_consumption_pct,
        "self_sufficiency_pct": self_sufficiency_pct,
        "balance_error_w": balance_error_w,
        "operating_mode": mode,
        "is_grid_importing": grid_direction == "importing",
        "is_grid_exporting": grid_direction == "exporting",
        "is_battery_charging": battery_direction == "charging",
        "is_battery_discharging": battery_direction == "discharging",
    }
