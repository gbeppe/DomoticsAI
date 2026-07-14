package it.zara.domoticsai.domain.model

enum class LightDeviceType {
    LIGHT,
    RELAY
}

enum class LightArea {
    INTERNAL,
    EXTERNAL,
    POOL
}

enum class LightState {
    ON,
    OFF,
    UNKNOWN
}

data class LightDevice(
    val id: String,
    val label: String,
    val area: LightArea,
    val type: LightDeviceType,
    val state: LightState,
    val available: Boolean,
    val quality: String = "unknown",
    val timestamp: String? = null
)

data class LightsSummary(
    val lightsOnTotal: Int = 0,
    val relaysOnTotal: Int = 0,
    val unknownTotal: Int = 0,
    val internalOn: Int = 0,
    val internalTotal: Int = 0,
    val externalOn: Int = 0,
    val externalTotal: Int = 0,
    val poolOn: Int = 0,
    val poolTotal: Int = 0,
    val allAvailable: Boolean = false
)

data class LightsDashboardState(
    val loading: Boolean = false,
    val devices: List<LightDevice> = emptyList(),
    val summary: LightsSummary = LightsSummary(),
    val error: String? = null
)
