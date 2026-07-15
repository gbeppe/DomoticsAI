package it.zara.domoticsai.ui.commands

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CommandStreamClient
import it.zara.domoticsai.data.core.CoreEngineClient
import it.zara.domoticsai.domain.model.CommandsScreenState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.net.ConnectException
import java.net.SocketException
import java.net.SocketTimeoutException

class CommandsViewModel(
    private val client: CoreEngineClient =
        CoreEngineClient(),
    private val streamClient: CommandStreamClient =
        CommandStreamClient(),
    private val baseUrl: String =
        "http://192.168.1.40:8090"
) : ViewModel() {

    private val _state =
        MutableStateFlow(
            CommandsScreenState()
        )

    val state = _state.asStateFlow()

    private var refreshJob: Job? = null
    private var eventRefreshJob: Job? = null

    init {
        refresh()
        startStream()
        startFallbackRefresh()
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
                        client.fetchCommands(
                            baseUrl
                        )
                    }
                }.onSuccess { items ->
                    _state.value =
                        _state.value.copy(
                            loading = false,
                            items = items,
                            error = null
                        )

                }.onFailure { error ->
                    /*
                     * Se anche una normale richiesta HTTP
                     * non raggiunge il Core Engine, lo stream
                     * non può essere considerato sano.
                     *
                     * Lo storico già caricato resta visibile.
                     */
                    _state.value =
                        _state.value.copy(
                            loading = false,
                            connectedToStream = false,
                            error =
                                userMessage(error)
                        )
                }
            }
    }

    private fun scheduleEventRefresh() {
        eventRefreshJob?.cancel()

        eventRefreshJob =
            viewModelScope.launch {
                /*
                 * Un comando genera diverse transizioni
                 * ravvicinate. Le raggruppiamo in un solo
                 * aggiornamento dello storico.
                 */
                delay(300)
                refresh()
            }
    }

    private fun startStream() {
        viewModelScope.launch {
            while (isActive) {
                runCatching {
                    streamClient.connect(
                        baseUrl = baseUrl,

                        onConnected = {
                            _state.value =
                                _state.value.copy(
                                    connectedToStream = true,
                                    error = null
                                )
                        },

                        onDisconnected = {
                            _state.value =
                                _state.value.copy(
                                    connectedToStream = false
                                )
                        },

                        onEvent = {
                            scheduleEventRefresh()
                        }
                    )

                }.onFailure {
                    /*
                     * La riconnessione SSE è automatica.
                     * Non cancelliamo né nascondiamo
                     * lo storico dei comandi.
                     */
                    _state.value =
                        _state.value.copy(
                            connectedToStream = false
                        )
                }

                if (isActive) {
                    delay(2_000)
                }
            }
        }
    }

    private fun startFallbackRefresh() {
        viewModelScope.launch {
            while (isActive) {
                delay(10_000)

                /*
                 * Oltre a recuperare eventi eventualmente
                 * persi, questo controllo determina in modo
                 * affidabile se il Core Engine è raggiungibile.
                 */
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
                    ?: "Errore di comunicazione con il Core Engine"
        }
}
