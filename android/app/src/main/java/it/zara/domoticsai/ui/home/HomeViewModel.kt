package it.zara.domoticsai.ui.home

import androidx.lifecycle.ViewModel
import it.zara.domoticsai.data.mqtt.DomoticsRepository
import it.zara.domoticsai.domain.model.ConnectionSettings
import kotlinx.coroutines.flow.StateFlow

class HomeViewModel(private val repository: DomoticsRepository) : ViewModel() {
    val homeState = repository.homeState
    val connectionState = repository.connectionState

    fun connect(settings: ConnectionSettings) = repository.connect(settings)
    fun disconnect() = repository.disconnect()
}
