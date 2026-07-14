package it.zara.domoticsai.ui.lights

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

class LightsViewModel(
    private val repository: CoreEngineRepository,
    private val baseUrl: String =
        "http://192.168.1.40:8090"
) : ViewModel() {

    val state = repository.lightsState

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
}
