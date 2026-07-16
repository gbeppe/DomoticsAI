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
import it.zara.domoticsai.domain.model.ClimateDashboardState
import it.zara.domoticsai.domain.model.ConnectionSettings
import it.zara.domoticsai.domain.model.ConnectionState
import it.zara.domoticsai.domain.model.HomeDataSource
import it.zara.domoticsai.domain.model.HomeIntelligenceUiState
import it.zara.domoticsai.domain.model.HouseDecisionsUiState
import it.zara.domoticsai.domain.model.HouseContextsUiState
import it.zara.domoticsai.ui.components.*
import it.zara.domoticsai.ui.decisions.DecisionsCard
import it.zara.domoticsai.ui.context.HouseStatusCard
import it.zara.domoticsai.ui.intelligence.HomeIntelligenceStatus

private fun formatClimateValue(
    value: Double?,
    unit: String? = null,
    decimals: Int = 1
): String {
    if (value == null) {
        return "—"
    }

    val formatted =
        when (decimals) {
            0 -> "%.0f".format(value)
            2 -> "%.2f".format(value)
            else -> "%.1f".format(value)
        }

    return if (unit.isNullOrBlank()) {
        formatted
    } else {
        "$formatted $unit"
    }
}


private fun formatVmcSpeed(
    value: Double?
): String =
    value
        ?.toInt()
        ?.toString()
        ?: "—"


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    settings: ConnectionSettings,
    intelligenceState: HomeIntelligenceUiState,
    climateState: ClimateDashboardState,
    onClimateRefresh: () -> Unit,
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
            error = null,
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
            error = null
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
                Column(
                    verticalArrangement =
                        Arrangement.spacedBy(6.dp)
                ) {
                    HomeIntelligenceStatus(
                        state =
                            intelligenceState
                    )
                }
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
            item(
                span = {
                    GridItemSpan(maxLineSpan)
                }
            ) {
                ElevatedCard(
                    modifier =
                        Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier =
                            Modifier
                                .fillMaxWidth()
                                .padding(
                                    horizontal = 16.dp,
                                    vertical = 10.dp
                                ),
                        horizontalArrangement =
                            Arrangement
                                .SpaceBetween
                    ) {
                        Column {
                            Text(
                                text = "Clima reale",
                                style =
                                    MaterialTheme
                                        .typography
                                        .titleMedium
                            )

                            Text(
                                text =
                                    when {
                                        climateState.loading ->
                                            "Aggiornamento…"

                                        climateState.error != null ->
                                            "Core Engine non raggiungibile"

                                        climateState.complete ->
                                            "Dati completi"

                                        climateState.hasAnyValue() ->
                                            "Dati parziali"

                                        else ->
                                            "Dati non disponibili"
                                    },
                                style =
                                    MaterialTheme
                                        .typography
                                        .bodySmall
                            )
                        }

                        TextButton(
                            onClick =
                                onClimateRefresh
                        ) {
                            Text("Aggiorna")
                        }
                    }
                }
            }

            item {
                val living =
                    climateState
                        .environment
                        .living

                MetricCard(
                    "Living",
                    formatClimateValue(
                        living.temperature.value,
                        living.temperature.unit
                    ),
                    "Umidità ${
                        formatClimateValue(
                            living.humidity.value,
                            living.humidity.unit
                        )
                    } · Humidex ${
                        formatClimateValue(
                            living.humidex.value
                        )
                    }"
                )
            }

            item {
                val bedroom =
                    climateState
                        .environment
                        .bedroom

                MetricCard(
                    "Camera",
                    formatClimateValue(
                        bedroom.temperature.value,
                        bedroom.temperature.unit
                    ),
                    "Umidità ${
                        formatClimateValue(
                            bedroom.humidity.value,
                            bedroom.humidity.unit
                        )
                    } · Humidex ${
                        formatClimateValue(
                            bedroom.humidex.value
                        )
                    }"
                )
            }

            item {
                val outdoor =
                    climateState
                        .environment
                        .outdoor

                MetricCard(
                    "Esterno",
                    formatClimateValue(
                        outdoor.temperature.value,
                        outdoor.temperature.unit
                    ),
                    "Umidità ${
                        formatClimateValue(
                            outdoor.humidity.value,
                            outdoor.humidity.unit
                        )
                    }"
                )
            }

            item {
                MetricCard(
                    "Termostato",
                    formatClimateValue(
                        climateState
                            .thermostat
                            .livingTargetTemperature
                            .value,
                        climateState
                            .thermostat
                            .livingTargetTemperature
                            .unit
                    ),
                    "Target living"
                )
            }

            item {
                MetricCard(
                    "VMC",
                    formatVmcSpeed(
                        climateState
                            .ventilation
                            .speed
                            .value
                    ),
                    "Velocità attuale"
                )
            }
            item(span = { GridItemSpan(maxLineSpan) }) {
                AssistChip(onClick = {}, label = { Text("MQTT: ${connection.name}") })
            }
        }
    }
}
