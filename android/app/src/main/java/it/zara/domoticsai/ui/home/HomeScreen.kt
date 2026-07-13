package it.zara.domoticsai.ui.home

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Link
import androidx.compose.material.icons.filled.LinkOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.ConnectionSettings
import it.zara.domoticsai.domain.model.ConnectionState
import it.zara.domoticsai.ui.components.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    settings: ConnectionSettings
) {
    val state by viewModel.homeState.collectAsState()
    val connection by viewModel.connectionState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("DomoticsAI") },
                actions = {
                    IconButton(
                        onClick = {
                            if (connection == ConnectionState.DISCONNECTED ||
                                connection == ConnectionState.ERROR
                            ) viewModel.connect(settings) else viewModel.disconnect()
                        }
                    ) {
                        Icon(
                            if (connection == ConnectionState.CONNECTED_LOCAL ||
                                connection == ConnectionState.CONNECTED_REMOTE
                            ) Icons.Default.Link else Icons.Default.LinkOff,
                            contentDescription = "Connessione"
                        )
                    }
                }
            )
        }
    ) { padding ->
        LazyVerticalGrid(
            columns = GridCells.Adaptive(160.dp),
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                DialCard("Produzione FV", state.energy.solarPowerW, "W", 6000.0)
            }
            item {
                DialCard("Consumo casa", state.energy.homeLoadW, "W", 6000.0)
            }
            item(span = { GridItemSpan(maxLineSpan) }) {
                BatteryCard(state.energy.powerwallSocPct)
            }
            item {
                MetricCard(
                    "Living",
                    state.climate.livingTemperatureC?.let { "%.1f °C".format(it) } ?: "—",
                    "Humidex ${state.climate.livingHumidex?.let { "%.1f".format(it) } ?: "—"}"
                )
            }
            item {
                MetricCard(
                    "Climatizzatore",
                    state.climate.acPowerW?.let { "%.0f W".format(it) } ?: "—",
                    "Assorbimento reale"
                )
            }
            item {
                MetricCard("VMC", state.vmc.speed?.toString() ?: "—", "Velocità attuale")
            }
            item(span = { GridItemSpan(maxLineSpan) }) {
                AssistChip(
                    onClick = {},
                    label = { Text("Connessione: ${connection.name}") }
                )
            }
        }
    }
}
