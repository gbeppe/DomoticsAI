package it.zara.domoticsai.ui.energy

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineRepository
import it.zara.domoticsai.data.mqtt.DomoticsRepository
import it.zara.domoticsai.domain.model.EnergyDashboardState
import it.zara.domoticsai.domain.model.EnergyDataSource
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

class EnergyViewModel(
    private val coreRepository: CoreEngineRepository,
    private val domoticsRepository: DomoticsRepository,
    private val baseUrl: String =
        "http://192.168.1.40:8090"
) : ViewModel() {

    val state = combine(
        coreRepository.energyState,
        domoticsRepository.homeState
    ) { coreState, mqttHomeState ->
        val mqttEnergy = mqttHomeState.energy
        val mqttAvailable =
            mqttEnergy.solarPowerW != null ||
                mqttEnergy.homeLoadW != null ||
                mqttEnergy.gridPowerW != null ||
                mqttEnergy.batteryPowerW != null ||
                mqttEnergy.powerwallSocPct != null

        val coreAvailable =
            coreState.raw.solarPowerW != null ||
                coreState.raw.homeLoadW != null ||
                coreState.raw.gridPowerW != null ||
                coreState.raw.batteryPowerW != null ||
                coreState.raw.powerwallSocPct != null

        when {
            coreState.error == null && coreAvailable ->
                coreState.copy(
                    source = EnergyDataSource.CORE_ENGINE
                )

            mqttAvailable ->
                EnergyDashboardState(
                    loading = false,
                    raw = mqttEnergy,
                    source = EnergyDataSource.MQTT_FALLBACK,
                    error = null
                )

            else ->
                EnergyDashboardState(
                    loading = coreState.loading,
                    source = EnergyDataSource.NONE,
                    error = coreState.error
                )
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = EnergyDashboardState()
    )

    init {
        viewModelScope.launch {
            while (isActive) {
                coreRepository.refreshEnergy(baseUrl)
                delay(3_000)
            }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            coreRepository.refreshEnergy(baseUrl)
        }
    }
}
