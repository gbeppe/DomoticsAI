package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CoreDiagnosticsState
import it.zara.domoticsai.domain.model.CoreTwinState
import it.zara.domoticsai.domain.model.EnergyDashboardState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.withContext

class CoreEngineRepository(
    private val client: CoreEngineClient =
        CoreEngineClient()
) {
    private val _state =
        MutableStateFlow(CoreDiagnosticsState())
    val state = _state.asStateFlow()

    private val _twinState =
        MutableStateFlow(CoreTwinState())
    val twinState = _twinState.asStateFlow()

    private val _energyState =
        MutableStateFlow(EnergyDashboardState())
    val energyState = _energyState.asStateFlow()

    suspend fun refresh(baseUrl: String) {
        _state.value =
            _state.value.copy(
                loading = true,
                error = null
            )

        runCatching {
            withContext(Dispatchers.IO) {
                val health =
                    client.fetchHealth(baseUrl)
                val twinJson =
                    client.fetchTwin(baseUrl)
                val parsedHomeState =
                    CoreTwinParser.parse(twinJson)

                Triple(
                    health,
                    twinJson,
                    parsedHomeState
                )
            }
        }.onSuccess {
                (health, twinJson, homeState) ->

            _state.value = CoreDiagnosticsState(
                loading = false,
                health = health,
                twinJson = twinJson,
                error = null
            )

            _twinState.value = CoreTwinState(
                homeState = homeState,
                available =
                    CoreTwinParser.hasAnyValue(homeState),
                fetchedAtEpochMs =
                    System.currentTimeMillis(),
                error = null
            )
        }.onFailure { error ->
            val message =
                error.message
                    ?: error.javaClass.simpleName

            _state.value =
                _state.value.copy(
                    loading = false,
                    error = message
                )

            _twinState.value =
                _twinState.value.copy(
                    available = false,
                    error = message
                )
        }
    }

    suspend fun refreshEnergy(baseUrl: String) {
/*        _energyState.value =
            _energyState.value.copy(
                loading = true,
                error = null
            )
*/
val current = _energyState.value

val hasExistingData =
    current.raw.solarPowerW != null ||
        current.raw.homeLoadW != null ||
        current.raw.gridPowerW != null ||
        current.raw.batteryPowerW != null ||
        current.raw.powerwallSocPct != null

_energyState.value =
    current.copy(
        loading = !hasExistingData,
        error = null
    )

        runCatching {
            withContext(Dispatchers.IO) {
                EnergyParser.parse(
                    client.fetchEnergy(baseUrl)
                )
            }
        }.onSuccess { parsed ->
            _energyState.value =
                parsed.copy(
                    loading = false,
                    error = null
                )
        }.onFailure { error ->
            _energyState.value =
                _energyState.value.copy(
                    loading = false,
                    error =
                        error.message
                            ?: error.javaClass.simpleName
                )
        }
    }
}
