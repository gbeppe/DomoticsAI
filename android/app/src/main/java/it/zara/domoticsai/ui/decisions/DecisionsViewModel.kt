package it.zara.domoticsai.ui.decisions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineClient
import it.zara.domoticsai.domain.model.HouseDecisionsUiState
import java.net.ConnectException
import java.net.SocketException
import java.net.SocketTimeoutException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class DecisionsViewModel(
    private val client: CoreEngineClient =
        CoreEngineClient(),
    private val baseUrl: String =
        "http://192.168.1.40:8090"
) : ViewModel() {

    private val _state =
        MutableStateFlow(
            HouseDecisionsUiState()
        )

    val state = _state.asStateFlow()

    private var refreshJob: Job? = null

    init {
        refresh()
        startPeriodicRefresh()
    }

    fun refresh() {
        if (refreshJob?.isActive == true) {
            return
        }

        refreshJob =
            viewModelScope.launch {
                val current = _state.value

                _state.value =
                    current.copy(
                        loading =
                            current.items.isEmpty(),
                        error = null
                    )

                runCatching {
                    withContext(
                        Dispatchers.IO
                    ) {
                        client.fetchDecisions(
                            baseUrl
                        )
                    }
                }.onSuccess { result ->
                    _state.value =
                        HouseDecisionsUiState(
                            loading = false,
                            items = result.decisions,
                            executionEnabled =
                                result.executionEnabled,
                            error = null
                        )

                }.onFailure { error ->
                    /*
                     * Manteniamo gli eventuali suggerimenti
                     * già caricati durante un errore temporaneo.
                     */
                    _state.value =
                        _state.value.copy(
                            loading = false,
                            error = userMessage(
                                error
                            )
                        )
                }
            }
    }

    private fun startPeriodicRefresh() {
        viewModelScope.launch {
            while (isActive) {
                delay(10_000)
                refresh()
            }
        }
    }

    private fun userMessage(
        error: Throwable
    ): String =
        when (error) {
            is ConnectException,
            is SocketTimeoutException,
            is SocketException ->
                "Core Engine non raggiungibile"

            else ->
                error.message
                    ?.replace(
                        "/192.168.1.40:8090",
                        "192.168.1.40:8090"
                    )
                    ?.takeIf {
                        it.isNotBlank()
                    }
                    ?: (
                        "Errore nel caricamento "
                        + "dei suggerimenti"
                    )
        }
}
