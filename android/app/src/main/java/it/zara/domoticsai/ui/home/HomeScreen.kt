package it.zara.domoticsai.ui.home

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Link
import androidx.compose.material.icons.filled.LinkOff
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.ConnectionSettings
import it.zara.domoticsai.domain.model.ConnectionState
import it.zara.domoticsai.domain.model.HomeDataSource
import it.zara.domoticsai.domain.model.HomeIntelligenceUiState
import it.zara.domoticsai.domain.model.HouseDecisionsUiState
import it.zara.domoticsai.domain.model.HouseContextsUiState
import it.zara.domoticsai.ui.components.*
import it.zara.domoticsai.ui.decisions.DecisionsCard
import it.zara.domoticsai.ui.context.HouseStatusCard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    settings: ConnectionSettings,
    intelligenceState: HomeIntelligenceUiState,
    onIntelligenceRefresh: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()
    val connection by viewModel.connectionState.collectAsState()
    val state = uiState.homeState

    val houseContextsState =
        HouseContextsUiState(
            loading =
                intelligenceState.loading,
            items =
                intelligenceState.contexts,
            error =
                intelligenceState.error,
            lastSuccessfulUpdateEpochMs =
                intelligenceState
                    .lastSuccessfulUpdateEpochMs
        )

    val decisionsState =
        HouseDecisionsUiState(
            loading =
                intelligenceState.loading,
            items =
                intelligenceState.decisions,
            executionEnabled =
                intelligenceState.executionEnabled,
            error =
                intelligenceState.error
        )

    LaunchedEffect(settings, connection) {
        if (
            connection == ConnectionState.DISCONNECTED ||
            connection == ConnectionState.ERROR
        ) {
            viewModel.connect(settings)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("DomoticsAI") },
                actions = {
                    IconButton(onClick = viewModel::refreshCore) {
                        Icon(Icons.Default.Refresh, contentDescription = "Aggiorna Digital Twin")
                    }
                    IconButton(
                        onClick = {
                            if (
                                connection == ConnectionState.DISCONNECTED ||
                                connection == ConnectionState.ERROR
                            ) viewModel.connect(settings) else viewModel.disconnect()
                        }
                    ) {
                        Icon(
                            if (
                                connection == ConnectionState.CONNECTED_LOCAL ||
                                connection == ConnectionState.CONNECTED_REMOTE
                            ) Icons.Default.Link else Icons.Default.LinkOff,
                            contentDescription = "Connessione MQTT"
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
            item(span = { GridItemSpan(maxLineSpan) }) {
                AssistChip(
                    onClick = {},
                    label = {
                        Text(
                            when (uiState.source) {
                                HomeDataSource.CORE_ENGINE -> "Dati: Core Engine"
                                HomeDataSource.MQTT -> "Dati: MQTT fallback"
                                HomeDataSource.NONE ->
                                    if (connection == ConnectionState.CONNECTING) {
                                        "Connessione MQTT in corso…"
                                    } else {
                                        "Dati non disponibili"
                                    }
                            }
                        )
                    }
                )
            }

            item(
                span = {
                    GridItemSpan(maxLineSpan)
                }
            ) {
                HouseStatusCard(
                    state = houseContextsState,
                    onRefresh =
                        onIntelligenceRefresh
                )
            }

            item(
                span = {
                    GridItemSpan(maxLineSpan)
                }
            ) {
                DecisionsCard(
                    state = decisionsState,
                    onRefresh =
                        onIntelligenceRefresh
                )
            }

            item { DialCard("Produzione FV", state.energy.solarPowerW, "W", 6000.0) }
            item { DialCard("Consumo casa", state.energy.homeLoadW, "W", 6000.0) }
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
                AssistChip(onClick = {}, label = { Text("MQTT: ${connection.name}") })
            }
        }
    }
}
