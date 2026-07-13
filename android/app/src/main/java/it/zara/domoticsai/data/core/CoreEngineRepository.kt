package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CoreDiagnosticsState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.withContext

class CoreEngineRepository(
    private val client: CoreEngineClient = CoreEngineClient()
) {
    private val _state = MutableStateFlow(CoreDiagnosticsState())
    val state = _state.asStateFlow()

    suspend fun refresh(baseUrl: String) {
        _state.value = _state.value.copy(loading = true, error = null)

        runCatching {
            withContext(Dispatchers.IO) {
                client.fetchHealth(baseUrl) to client.fetchTwin(baseUrl)
            }
        }.onSuccess { (health, twin) ->
            _state.value = CoreDiagnosticsState(
                health = health,
                twinJson = twin
            )
        }.onFailure {
            _state.value = _state.value.copy(
                loading = false,
                error = it.message ?: it.javaClass.simpleName
            )
        }
    }
}
