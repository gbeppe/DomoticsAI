package it.zara.domoticsai.ui.home

import androidx.lifecycle.ViewModel
import it.zara.domoticsai.data.mqtt.DomoticsRepository
import it.zara.domoticsai.data.settings.SecureCredentialStore
import it.zara.domoticsai.domain.model.ConnectionSettings

class HomeViewModel(
    private val repository: DomoticsRepository,
    private val credentialStore: SecureCredentialStore
) : ViewModel() {
    val homeState = repository.homeState
    val connectionState = repository.connectionState

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
}
