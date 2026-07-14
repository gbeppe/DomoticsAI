package it.zara.domoticsai.ui.lights

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineClient
import it.zara.domoticsai.data.core.CoreEngineRepository
import it.zara.domoticsai.domain.model.DeviceCommandUiState
import it.zara.domoticsai.domain.model.LightDevice
import it.zara.domoticsai.domain.model.LightState
import it.zara.domoticsai.domain.model.UiCommandState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class LightsViewModel(
    private val repository: CoreEngineRepository,
    private val client: CoreEngineClient = CoreEngineClient(),
    private val baseUrl: String =
        "http://192.168.1.40:8090"
) : ViewModel() {

    val state = repository.lightsState

    private val _commands =
        MutableStateFlow<Map<String, DeviceCommandUiState>>(
            emptyMap()
        )
    val commands = _commands.asStateFlow()

    init {
        viewModelScope.launch {
            while (isActive) {
                repository.refreshLights(baseUrl)
                delay(3_000)
            }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            repository.refreshLights(baseUrl)
        }
    }

    fun simulateToggle(device: LightDevice) {
        val desired =
            if (device.state == LightState.ON) {
                LightState.OFF
            } else {
                LightState.ON
            }

        sendCommand(device, desired)
    }

    private fun sendCommand(
        device: LightDevice,
        desiredState: LightState
    ) {
        val key = commandKey(device)

        _commands.value =
            _commands.value + (
                key to DeviceCommandUiState(
                    desiredState = desiredState,
                    state = UiCommandState.SENDING,
                    message = "Invio comando simulato…"
                )
            )

        viewModelScope.launch {
            runCatching {
                withContext(Dispatchers.IO) {
                    client.createLightCommand(
                        baseUrl,
                        device,
                        desiredState
                    )
                }
            }.onSuccess { receipt ->
                updateCommand(
                    key,
                    DeviceCommandUiState(
                        commandId = receipt.commandId,
                        desiredState = desiredState,
                        state = receipt.state,
                        message = receipt.message
                    )
                )

                pollUntilTerminal(
                    key = key,
                    commandId = receipt.commandId,
                    desiredState = desiredState
                )
            }.onFailure { error ->
                updateCommand(
                    key,
                    DeviceCommandUiState(
                        desiredState = desiredState,
                        state = UiCommandState.FAILED,
                        message =
                            error.message
                                ?: "Errore invio comando"
                    )
                )
            }
        }
    }

    private suspend fun pollUntilTerminal(
        key: String,
        commandId: String,
        desiredState: LightState
    ) {
        repeat(20) {
            delay(500)

            val receipt =
                runCatching {
                    withContext(Dispatchers.IO) {
                        client.fetchCommand(
                            baseUrl,
                            commandId
                        )
                    }
                }.getOrElse { error ->
                    updateCommand(
                        key,
                        DeviceCommandUiState(
                            commandId = commandId,
                            desiredState = desiredState,
                            state = UiCommandState.FAILED,
                            message =
                                error.message
                                    ?: "Errore lettura comando"
                        )
                    )
                    return
                }

            updateCommand(
                key,
                DeviceCommandUiState(
                    commandId = commandId,
                    desiredState = desiredState,
                    state = receipt.state,
                    message = receipt.message
                )
            )

            if (
                receipt.state in setOf(
                    UiCommandState.SIMULATED,
                    UiCommandState.CONFIRMED,
                    UiCommandState.REJECTED,
                    UiCommandState.TIMEOUT,
                    UiCommandState.FAILED
                )
            ) {
                return
            }
        }

        updateCommand(
            key,
            DeviceCommandUiState(
                commandId = commandId,
                desiredState = desiredState,
                state = UiCommandState.TIMEOUT,
                message = "Timeout attesa esito"
            )
        )
    }

    fun clearCommand(device: LightDevice) {
        val key = commandKey(device)
        _commands.value =
            _commands.value - key
    }

    private fun updateCommand(
        key: String,
        value: DeviceCommandUiState
    ) {
        _commands.value =
            _commands.value + (key to value)
    }

    private fun commandKey(
        device: LightDevice
    ): String =
        "${device.area.name}/${device.id}"
}
