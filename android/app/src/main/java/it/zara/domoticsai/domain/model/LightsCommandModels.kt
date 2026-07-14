package it.zara.domoticsai.domain.model

enum class UiCommandState {
    IDLE,
    SENDING,
    WAITING_CONFIRMATION,
    SIMULATED,
    CONFIRMED,
    REJECTED,
    TIMEOUT,
    FAILED
}

data class DeviceCommandUiState(
    val commandId: String? = null,
    val desiredState: LightState? = null,
    val state: UiCommandState = UiCommandState.IDLE,
    val message: String? = null
)

data class CommandReceiptDto(
    val commandId: String,
    val state: UiCommandState,
    val message: String? = null
)
