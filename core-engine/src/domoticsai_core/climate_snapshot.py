from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ClimateMetric:
    value: Any
    unit: str | None
    quality: str | None
    source: str | None
    timestamp: str | None
    available: bool


@dataclass(frozen=True)
class ClimateSnapshot:
    living_temperature: ClimateMetric
    living_humidity: ClimateMetric
    living_humidex: ClimateMetric

    bedroom_temperature: ClimateMetric
    bedroom_humidity: ClimateMetric
    bedroom_humidex: ClimateMetric

    outdoor_temperature: ClimateMetric
    outdoor_humidity: ClimateMetric

    living_target_temperature: ClimateMetric
    vmc_speed: ClimateMetric

    dhw_buffer_temperature: ClimateMetric
    buffer_lower_temperature: ClimateMetric
    buffer_upper_temperature: ClimateMetric

    fireplace_mode: ClimateMetric
    fireplace_powered: ClimateMetric
    fireplace_power_level: ClimateMetric

    complete_snapshot: ClimateMetric

    updated_at: str | None
    complete: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": "climate",
            "environment": {
                "living": {
                    "temperature": self._metric(
                        self.living_temperature
                    ),
                    "humidity": self._metric(
                        self.living_humidity
                    ),
                    "humidex": self._metric(
                        self.living_humidex
                    ),
                },
                "bedroom": {
                    "temperature": self._metric(
                        self.bedroom_temperature
                    ),
                    "humidity": self._metric(
                        self.bedroom_humidity
                    ),
                    "humidex": self._metric(
                        self.bedroom_humidex
                    ),
                },
                "outdoor": {
                    "temperature": self._metric(
                        self.outdoor_temperature
                    ),
                    "humidity": self._metric(
                        self.outdoor_humidity
                    ),
                },
            },
            "thermostat": {
                "livingTargetTemperature":
                    self._metric(
                        self.living_target_temperature
                    ),
            },
            "ventilation": {
                "speed": self._metric(
                    self.vmc_speed
                ),
            },
            "thermal": {
                "dhwBufferTemperature":
                    self._metric(
                        self.dhw_buffer_temperature
                    ),
                "bufferLowerTemperature":
                    self._metric(
                        self.buffer_lower_temperature
                    ),
                "bufferUpperTemperature":
                    self._metric(
                        self.buffer_upper_temperature
                    ),
            },
            "fireplace": {
                "mode": self._metric(
                    self.fireplace_mode
                ),
                "powered": self._metric(
                    self.fireplace_powered
                ),
                "powerLevel": self._metric(
                    self.fireplace_power_level
                ),
            },
            "completeSnapshot": self._metric(
                self.complete_snapshot
            ),
            "updatedAt": self.updated_at,
            "complete": self.complete,
        }

    @staticmethod
    def _metric(
        metric: ClimateMetric,
    ) -> dict[str, Any]:
        return {
            "value": metric.value,
            "unit": metric.unit,
            "quality": metric.quality,
            "source": metric.source,
            "timestamp": metric.timestamp,
            "available": metric.available,
        }


def _metric_from_wrapped(
    wrapped,
) -> ClimateMetric:

    if wrapped is None:
        return ClimateMetric(
            value=None,
            unit=None,
            quality=None,
            source=None,
            timestamp=None,
            available=False,
        )

    #
    # Caso 1:
    # dizionario normale
    #
    if isinstance(
        wrapped,
        dict,
    ):
        return ClimateMetric(
            value=wrapped.get("value"),
            unit=wrapped.get("unit"),
            quality=wrapped.get("quality"),
            source=wrapped.get("source"),
            timestamp=wrapped.get("timestamp"),
            available=True,
        )

    #
    # Caso 2:
    # TwinValue (Pydantic)
    #
    return ClimateMetric(
        value=getattr(
            wrapped,
            "value",
            None,
        ),
        unit=getattr(
            wrapped,
            "unit",
            None,
        ),
        quality=getattr(
            wrapped,
            "quality",
            None,
        ),
        source=getattr(
            wrapped,
            "source",
            None,
        ),
        timestamp=getattr(
            wrapped,
            "timestamp",
            None,
        ),
        available=True,
    )


def build_climate_snapshot(
    twin: dict[str, Any],
) -> ClimateSnapshot:
    domains = twin.get(
        "domains",
        {}
    )

    climate = domains.get(
        "climate",
        {}
    )

    vmc = domains.get(
        "vmc",
        {}
    )

    thermal = domains.get(
        "thermal",
        {}
    )

    fireplace = domains.get(
        "fireplace",
        {}
    )

    metrics = {
        "living_temperature":
            _metric_from_wrapped(
                climate.get(
                    "living_temperature_c"
                )
            ),
        "living_humidity":
            _metric_from_wrapped(
                climate.get(
                    "living_humidity_pct"
                )
            ),
        "living_humidex":
            _metric_from_wrapped(
                climate.get(
                    "living_humidex"
                )
            ),
        "bedroom_temperature":
            _metric_from_wrapped(
                climate.get(
                    "bedroom_temperature_c"
                )
            ),
        "bedroom_humidity":
            _metric_from_wrapped(
                climate.get(
                    "bedroom_humidity_pct"
                )
            ),
        "bedroom_humidex":
            _metric_from_wrapped(
                climate.get(
                    "bedroom_humidex"
                )
            ),
        "outdoor_temperature":
            _metric_from_wrapped(
                climate.get(
                    "outdoor_temperature_c"
                )
            ),
        "outdoor_humidity":
            _metric_from_wrapped(
                climate.get(
                    "outdoor_humidity_pct"
                )
            ),
        "living_target_temperature":
            _metric_from_wrapped(
                climate.get(
                    "living_target_temperature_c"
                )
            ),
        "vmc_speed":
            _metric_from_wrapped(
                vmc.get(
                    "speed"
                )
            ),
        "dhw_buffer_temperature":
            _metric_from_wrapped(
                thermal.get(
                    "dhw_buffer_temperature_c"
                )
            ),
        "buffer_lower_temperature":
            _metric_from_wrapped(
                thermal.get(
                    "buffer_lower_temperature_c"
                )
            ),
        "buffer_upper_temperature":
            _metric_from_wrapped(
                thermal.get(
                    "buffer_upper_temperature_c"
                )
            ),
        "fireplace_mode":
            _metric_from_wrapped(
                fireplace.get(
                    "mode"
                )
            ),
        "fireplace_powered":
            _metric_from_wrapped(
                fireplace.get(
                    "powered"
                )
            ),
        "fireplace_power_level":
            _metric_from_wrapped(
                fireplace.get(
                    "power_level"
                )
            ),
        "complete_snapshot":
            _metric_from_wrapped(
                climate.get(
                    "complete_snapshot"
                )
            ),
    }

    timestamps = [
        metric.timestamp
        for metric in metrics.values()
        if metric.timestamp
    ]

    updated_at = (
        max(timestamps)
        if timestamps
        else None
    )

    required = (
        metrics["living_temperature"],
        metrics["living_humidity"],
        metrics["living_humidex"],
        metrics["bedroom_temperature"],
        metrics["bedroom_humidity"],
        metrics["bedroom_humidex"],
        metrics["outdoor_temperature"],
        metrics["outdoor_humidity"],
        metrics["vmc_speed"],
    )

    return ClimateSnapshot(
        **metrics,
        updated_at=updated_at,
        complete=all(
            metric.available
            for metric in required
        ),
    )
