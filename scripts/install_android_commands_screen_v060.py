#!/usr/bin/env python3
from pathlib import Path
import sys

BASE = Path('/home/giuseppe/AndroidStudioProjects/DomoticsAI/android/app/src/main/java/it/zara/domoticsai')

FILES = {
'domain/model/CommandHistoryModels.kt': r'''package it.zara.domoticsai.domain.model

data class CommandHistoryItem(
    val commandId: String,
    val domain: String,
    val action: String,
    val target: String,
    val source: String,
    val state: UiCommandState,
    val createdAt: String,
    val updatedAt: String,
    val mode: String,
    val error: String? = null
)

data class CommandsScreenState(
    val loading: Boolean = false,
    val items: List<CommandHistoryItem> = emptyList(),
    val error: String? = null
)
''',
'data/core/CommandJson.kt': r'''package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CommandHistoryItem
import it.zara.domoticsai.domain.model.UiCommandState
import org.json.JSONObject

object CommandJson {
    fun nullableString(obj: JSONObject, name: String): String? {
        if (!obj.has(name) || obj.isNull(name)) return null
        return obj.optString(name).takeIf {
            it.isNotBlank() && !it.equals("null", ignoreCase = true)
        }
    }

    fun parseState(value: String): UiCommandState =
        when (value.lowercase()) {
            "created", "validated", "queued", "sent" ->
                UiCommandState.SENDING
            "waiting_confirmation" -> UiCommandState.WAITING_CONFIRMATION
            "simulated" -> UiCommandState.SIMULATED
            "confirmed" -> UiCommandState.CONFIRMED
            "rejected" -> UiCommandState.REJECTED
            "timeout" -> UiCommandState.TIMEOUT
            "failed" -> UiCommandState.FAILED
            else -> UiCommandState.IDLE
        }

    fun parseHistoryItem(obj: JSONObject) = CommandHistoryItem(
        commandId = obj.optString("command_id"),
        domain = obj.optString("domain"),
        action = obj.optString("action"),
        target = obj.optString("target"),
        source = obj.optString("source"),
        state = parseState(obj.optString("state")),
        createdAt = obj.optString("created_at"),
        updatedAt = obj.optString("updated_at"),
        mode = obj.optString("mode"),
        error = nullableString(obj, "error")
    )
}
''',
'ui/commands/CommandsViewModel.kt': r'''package it.zara.domoticsai.ui.commands

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
''',
'ui/commands/CommandsScreen.kt': r'''package it.zara.domoticsai.ui.commands

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CommandsScreen(
    state: CommandsScreenState,
    onRefresh: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Comandi") },
                actions = {
                    IconButton(onClick = onRefresh) {
                        Icon(Icons.Default.Refresh, contentDescription = "Aggiorna")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                AssistChip(onClick = {}, label = { Text("Registro operativo") })
            }

            if (state.loading) {
                item { LinearProgressIndicator(Modifier.fillMaxWidth()) }
            }

            state.error?.let { error ->
                item {
                    Card(
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.errorContainer
                        )
                    ) {
                        Text(error, Modifier.padding(16.dp))
                    }
                }
            }

            if (!state.loading && state.items.isEmpty()) {
                item { Text("Nessun comando registrato") }
            }

            items(state.items, key = { it.commandId }) { command ->
                Card(shape = RoundedCornerShape(20.dp)) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Text(
                            command.target.substringAfter("/"),
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold
                        )
                        Text("${command.domain} · ${command.action}")
                        Text(stateLabel(command.state), fontWeight = FontWeight.Bold)
                        Text(
                            "Sorgente: ${command.source} · ${command.mode}",
                            style = MaterialTheme.typography.bodySmall
                        )
                        Text(
                            "ID: ${command.commandId.take(12)}…",
                            style = MaterialTheme.typography.bodySmall
                        )
                        command.error?.let {
                            Text(it, color = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            }
        }
    }
}

private fun stateLabel(state: UiCommandState): String = when (state) {
    UiCommandState.IDLE -> "Creato"
    UiCommandState.SENDING -> "In elaborazione"
    UiCommandState.WAITING_CONFIRMATION -> "In attesa di conferma"
    UiCommandState.SIMULATED -> "Simulazione completata"
    UiCommandState.CONFIRMED -> "Confermato"
    UiCommandState.REJECTED -> "Rifiutato"
    UiCommandState.TIMEOUT -> "Timeout"
    UiCommandState.FAILED -> "Errore"
}
'''
}


def write_files():
    for rel, content in FILES.items():
        path = BASE / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')


def patch_client():
    path = BASE / 'data/core/CoreEngineClient.kt'
    text = path.read_text(encoding='utf-8')
    imp = 'import it.zara.domoticsai.domain.model.CommandHistoryItem\n'
    marker = 'import it.zara.domoticsai.domain.model.CommandReceiptDto\n'
    if imp not in text:
        if marker not in text:
            raise RuntimeError('Import CommandReceiptDto non trovato')
        text = text.replace(marker, marker + imp, 1)

    if 'fun fetchCommands(' not in text:
        marker = '    private fun parseCommandState('
        if marker not in text:
            raise RuntimeError('parseCommandState non trovato')
        method = '''    fun fetchCommands(
        baseUrl: String
    ): List<CommandHistoryItem> {
        val root = JSONObject(
            requestJson(
                "${baseUrl.trimEnd('/')}/api/v1/commands"
            )
        )
        val items = root.optJSONArray("items")
            ?: return emptyList()

        return buildList {
            for (index in 0 until items.length()) {
                val item = items.optJSONObject(index)
                    ?: continue
                add(CommandJson.parseHistoryItem(item))
            }
        }
    }

'''
        text = text.replace(marker, method + marker, 1)
    path.write_text(text, encoding='utf-8')


def patch_main():
    path = BASE / 'MainActivity.kt'
    text = path.read_text(encoding='utf-8')

    if 'import androidx.compose.material.icons.filled.History\n' not in text:
        marker = 'import androidx.compose.material.icons.filled.Home\n'
        text = text.replace(marker, marker + 'import androidx.compose.material.icons.filled.History\n', 1)

    if 'import it.zara.domoticsai.ui.commands.*\n' not in text:
        marker = 'import it.zara.domoticsai.ui.diagnostics.*\n'
        text = text.replace(marker, 'import it.zara.domoticsai.ui.commands.*\n' + marker, 1)

    if 'val commandsViewModel:' not in text:
        marker = '                val diagnosticsViewModel:\n'
        block = '''                val commandsViewModel:
                    CommandsViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                CommandsViewModel()
                            }
                    )

'''
        if marker not in text:
            raise RuntimeError('DiagnosticsViewModel non trovato')
        text = text.replace(marker, block + marker, 1)

    if 'val commandsState by' not in text:
        marker = '                val diagnosticsState by\n'
        block = '''                val commandsState by
                    commandsViewModel.state.collectAsState()

'''
        if marker not in text:
            raise RuntimeError('diagnosticsState non trovato')
        text = text.replace(marker, block + marker, 1)

    if 'COMMANDS("Comandi")' not in text:
        text = text.replace(
            '    LIGHTS("Luci"),\n    LOGS("Log"),',
            '    LIGHTS("Luci"),\n    COMMANDS("Comandi"),\n    LOGS("Log"),',
            1,
        )

    if 'Destination.COMMANDS ->' not in text:
        text = text.replace(
            '                                                Destination.LOGS ->\n                                                    Icons.Default.List',
            '                                                Destination.COMMANDS ->\n                                                    Icons.Default.History\n                                                Destination.LOGS ->\n                                                    Icons.Default.List',
            1,
        )
        marker = '                            Destination.LOGS ->\n'
        block = '''                            Destination.COMMANDS ->
                                CommandsScreen(
                                    state = commandsState,
                                    onRefresh = commandsViewModel::refresh
                                )

'''
        if marker not in text:
            raise RuntimeError('Destination.LOGS non trovato')
        text = text.replace(marker, block + marker, 1)

    path.write_text(text, encoding='utf-8')


def main():
    write_files()
    patch_client()
    patch_main()
    print('OK: schermata Comandi installata.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'ERRORE: {error}', file=sys.stderr)
        raise
