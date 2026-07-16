package it.zara.domoticsai.domain.model


data class ClimateNumberMetric(
    val value: Double? = null,
    val unit: String? = null,
    val quality: String? = null,
    val source: String? = null,
    val timestamp: String? = null,
    val available: Boolean = false
)


data class ClimateTextMetric(
    val value: String? = null,
    val unit: String? = null,
    val quality: String? = null,
    val source: String? = null,
    val timestamp: String? = null,
    val available: Boolean = false
)


data class ClimateBooleanMetric(
    val value: Boolean? = null,
    val unit: String? = null,
    val quality: String? = null,
    val source: String? = null,
    val timestamp: String? = null,
    val available: Boolean = false
)


data class ClimateRoomState(
    val temperature: ClimateNumberMetric =
        ClimateNumberMetric(),
    val humidity: ClimateNumberMetric =
        ClimateNumberMetric(),
    val humidex: ClimateNumberMetric =
        ClimateNumberMetric()
)


data class ClimateOutdoorState(
    val temperature: ClimateNumberMetric =
        ClimateNumberMetric(),
    val humidity: ClimateNumberMetric =
        ClimateNumberMetric()
)


data class ClimateEnvironmentState(
    val living: ClimateRoomState =
        ClimateRoomState(),
    val bedroom: ClimateRoomState =
        ClimateRoomState(),
    val outdoor: ClimateOutdoorState =
        ClimateOutdoorState()
)


data class ClimateThermostatState(
    val livingTargetTemperature:
        ClimateNumberMetric =
            ClimateNumberMetric()
)


data class ClimateVentilationState(
    val speed: ClimateNumberMetric =
        ClimateNumberMetric()
)


data class ClimateThermalState(
    val dhwBufferTemperature:
        ClimateNumberMetric =
            ClimateNumberMetric(),
    val bufferLowerTemperature:
        ClimateNumberMetric =
            ClimateNumberMetric(),
    val bufferUpperTemperature:
        ClimateNumberMetric =
            ClimateNumberMetric()
)


data class ClimateFireplaceState(
    val mode: ClimateTextMetric =
        ClimateTextMetric(),
    val powered: ClimateBooleanMetric =
        ClimateBooleanMetric(),
    val powerLevel: ClimateNumberMetric =
        ClimateNumberMetric()
)


data class ClimateDashboardState(
    val loading: Boolean = false,
    val environment: ClimateEnvironmentState =
        ClimateEnvironmentState(),
    val thermostat: ClimateThermostatState =
        ClimateThermostatState(),
    val ventilation: ClimateVentilationState =
        ClimateVentilationState(),
    val thermal: ClimateThermalState =
        ClimateThermalState(),
    val fireplace: ClimateFireplaceState =
        ClimateFireplaceState(),
    val completeSnapshotJson: String? = null,
    val updatedAt: String? = null,
    val complete: Boolean = false,
    val error: String? = null
) {
    fun hasAnyValue(): Boolean =
        environment.living.temperature.available ||
            environment.living.humidity.available ||
            environment.living.humidex.available ||
            environment.bedroom.temperature.available ||
            environment.bedroom.humidity.available ||
            environment.bedroom.humidex.available ||
            environment.outdoor.temperature.available ||
            environment.outdoor.humidity.available ||
            thermostat.livingTargetTemperature.available ||
            ventilation.speed.available ||
            thermal.dhwBufferTemperature.available ||
            thermal.bufferLowerTemperature.available ||
            thermal.bufferUpperTemperature.available ||
            fireplace.mode.available ||
            fireplace.powered.available ||
            fireplace.powerLevel.available
}
