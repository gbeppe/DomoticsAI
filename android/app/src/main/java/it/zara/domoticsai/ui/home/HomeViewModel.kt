package it.zara.domoticsai.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineRepository
import it.zara.domoticsai.data.mqtt.DomoticsRepository
import it.zara.domoticsai.data.settings.SecureCredentialStore
import it.zara.domoticsai.domain.model.ConnectionSettings
import it.zara.domoticsai.domain.model.HomeDataSource
import it.zara.domoticsai.domain.model.HomeUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

class HomeViewModel(
    private val repository: DomoticsRepository,
    private val credentialStore: SecureCredentialStore,
    private val coreEngineRepository: CoreEngineRepository,
    private val coreBaseUrl: String = "http://192.168.1.40:8090"
) : ViewModel() {

    val connectionState = repository.connectionState

    val uiState = combine(
        repository.homeState,
        coreEngineRepository.twinState
    ) { mqttState, coreState ->
        when {
            coreState.available -> {
                HomeUiState(
                    homeState = coreState.homeState,
                    source = HomeDataSource.CORE_ENGINE
                )
            }

            mqttState.lastUpdateEpochMs != null -> {
                HomeUiState(
                    homeState = mqttState,
                    source = HomeDataSource.MQTT
                )
            }

            else -> HomeUiState()
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = HomeUiState()
    )

    init {
        viewModelScope.launch {
            while (isActive) {
                coreEngineRepository.refresh(coreBaseUrl)
                delay(5_000)
            }
        }
    }

    fun connect(settings: ConnectionSettings) {
        val credentials = credentialStore.load()

        repository.connect(
            settings = settings,
            credentials = mapOf(
                "local" to (
                    credentials.local.username to
                        credentials.local.password
                ),
                "remote" to (
                    credentials.remote.username to
                        credentials.remote.password
                )
            )
        )
    }

    fun disconnect() = repository.disconnect()

    fun refreshCore() {
        viewModelScope.launch {
            coreEngineRepository.refresh(coreBaseUrl)
        }
    }
}
