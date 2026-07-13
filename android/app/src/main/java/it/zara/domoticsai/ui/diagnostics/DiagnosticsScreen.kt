package it.zara.domoticsai.ui.diagnostics

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.CoreDiagnosticsState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DiagnosticsScreen(
    state: CoreDiagnosticsState,
    baseUrl: String,
    onRefresh: () -> Unit
) {
    LaunchedEffect(Unit) { onRefresh() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Core Engine") },
                actions = {
                    IconButton(onClick = onRefresh) {
                        Icon(Icons.Default.Refresh, contentDescription = "Aggiorna")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            Modifier.fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(baseUrl, style = MaterialTheme.typography.bodySmall)

            if (state.loading) {
                LinearProgressIndicator(Modifier.fillMaxWidth())
            }

            state.error?.let {
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer
                    )
                ) {
                    Text(
                        it,
                        Modifier.padding(16.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer
                    )
                }
            }

            state.health?.let { health ->
                Card {
                    Column(
                        Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Text("Health", style = MaterialTheme.typography.titleMedium)
                        Text("Stato: ${health.status}")
                        Text("MQTT connesso: ${health.mqttConnected}")
                        Text("Broker: ${health.mqttBroker}")
                        Text("Topic: ${health.mqttTopic}")
                        Text("Twin aggiornato: ${health.digitalTwinUpdatedAt}")
                    }
                }
            }

            if (state.twinJson.isNotBlank()) {
                Text("Digital Twin", style = MaterialTheme.typography.titleMedium)
                Card {
                    Box(
                        Modifier.fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                            .padding(12.dp)
                    ) {
                        Text(
                            state.twinJson,
                            fontFamily = FontFamily.Monospace,
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }
            }
        }
    }
}
