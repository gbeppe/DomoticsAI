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
