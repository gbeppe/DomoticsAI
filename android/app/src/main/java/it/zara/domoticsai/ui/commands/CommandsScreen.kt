package it.zara.domoticsai.ui.commands

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
                AssistChip(
                    onClick = {},
                    label = {
                        Text(
                            if (
                                state.connectedToStream
                            ) {
                                "Aggiornamenti realtime attivi"
                            } else {
                                "Stream in riconnessione"
                            }
                        )
                    }
                )
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
