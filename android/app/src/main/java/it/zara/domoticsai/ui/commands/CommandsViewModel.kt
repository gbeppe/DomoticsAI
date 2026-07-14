package it.zara.domoticsai.ui.commands

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineClient
import it.zara.domoticsai.domain.model.CommandsScreenState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class CommandsViewModel(
    private val client: CoreEngineClient = CoreEngineClient(),
    private val baseUrl: String = "http://192.168.1.40:8090"
) : ViewModel() {
    private val _state = MutableStateFlow(CommandsScreenState())
    val state = _state.asStateFlow()

    init {
        viewModelScope.launch {
            while (isActive) {
                refresh()
                delay(3_000)
            }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            val current = _state.value
            _state.value = current.copy(
                loading = current.items.isEmpty(),
                error = null
            )

            runCatching {
                withContext(Dispatchers.IO) {
                    client.fetchCommands(baseUrl)
                }
            }.onSuccess { items ->
                _state.value = CommandsScreenState(
                    loading = false,
                    items = items
                )
            }.onFailure { error ->
                _state.value = current.copy(
                    loading = false,
                    error = error.message ?: "Errore comandi"
                )
            }
        }
    }
}
