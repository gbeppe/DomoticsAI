package it.zara.domoticsai.domain.model

data class CoreHealth(
    val status: String = "unknown",
    val mqttConnected: Boolean = false,
    val mqttBroker: String = "",
    val mqttTopic: String = "",
    val digitalTwinUpdatedAt: String = ""
)

data class CoreDiagnosticsState(
    val loading: Boolean = false,
    val health: CoreHealth? = null,
    val twinJson: String = "",
    val error: String? = null
)

data class CoreTwinState(
    val homeState: HomeState = HomeState(),
    val available: Boolean = false,
    val fetchedAtEpochMs: Long? = null,
    val error: String? = null
)

enum class HomeDataSource {
    CORE_ENGINE,
    MQTT,
    NONE
}

data class HomeUiState(
    val homeState: HomeState = HomeState(),
    val source: HomeDataSource = HomeDataSource.NONE
)
