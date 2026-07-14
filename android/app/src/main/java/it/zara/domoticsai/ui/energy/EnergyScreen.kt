package it.zara.domoticsai.ui.energy

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.BatteryChargingFull
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Power
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.EnergyDashboardState
import it.zara.domoticsai.domain.model.EnergyDataSource
import kotlin.math.abs

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EnergyScreen(
    state: EnergyDashboardState,
    onRefresh: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Energia") },
                actions = {
                    IconButton(onClick = onRefresh) {
                        Icon(
                            Icons.Default.Refresh,
                            contentDescription = "Aggiorna"
                        )
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(4.dp)
            ) {
                if (
                    state.loading &&
                    state.source == EnergyDataSource.NONE
                ) {
                    LinearProgressIndicator(
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }

            AssistChip(
                onClick = {},
                label = {
                    Text(
                        when (state.source) {
                            EnergyDataSource.CORE_ENGINE ->
                                "Dati: Core Engine"
                            EnergyDataSource.MQTT_FALLBACK ->
                                "Dati: MQTT fallback"
                            EnergyDataSource.NONE ->
                                "Dati non disponibili"
                        }
                    )
                }
            )

            if (
                state.source == EnergyDataSource.NONE &&
                state.error != null
            ) {
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor =
                            MaterialTheme.colorScheme.errorContainer
                    )
                ) {
                    Text(
                        state.error,
                        Modifier.padding(16.dp)
                    )
                }
            }

            OperatingModeCard(
                mode = state.derived.operatingMode,
                source = state.source
            )

            EnergyFlowCard(state)

            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                PercentageCard(
                    title = "Autoconsumo",
                    value = state.derived.selfConsumptionPct,
                    modifier = Modifier.weight(1f)
                )

                PercentageCard(
                    title = "Autosufficienza",
                    value = state.derived.selfSufficiencyPct,
                    modifier = Modifier.weight(1f)
                )
            }

            BatteryCard(state)
            BalanceCard(
                errorW = state.derived.balanceErrorW,
                source = state.source
            )
        }
    }
}

@Composable
private fun OperatingModeCard(
    mode: String,
    source: EnergyDataSource
) {
    val label =
        if (source == EnergyDataSource.MQTT_FALLBACK) {
            "Dati grezzi disponibili; analisi avanzata sospesa"
        } else {
            when (mode) {
                "solar_charging_and_exporting" ->
                    "FV alimenta casa, carica batteria ed esporta"
                "solar_charging_battery" ->
                    "FV alimenta casa e carica batteria"
                "solar_exporting" ->
                    "FV alimenta casa ed esporta"
                "battery_supplying_home" ->
                    "Powerwall alimenta la casa"
                "grid_supplying_home" ->
                    "Rete alimenta la casa"
                "solar_supplying_home" ->
                    "Fotovoltaico alimenta la casa"
                "idle" ->
                    "Sistema energetico in equilibrio"
                else ->
                    "Stato energetico in aggiornamento"
            }
        }

    Card(shape = RoundedCornerShape(24.dp)) {
        Column(Modifier.padding(18.dp)) {
            Text(
                "Stato attuale",
                style = MaterialTheme.typography.titleMedium
            )
            Spacer(Modifier.height(6.dp))
            Text(
                label,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
private fun EnergyFlowCard(state: EnergyDashboardState) {
    val primary = MaterialTheme.colorScheme.primary
    val outline =
        MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)

    Card(shape = RoundedCornerShape(28.dp)) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(340.dp)
                .padding(16.dp)
        ) {
            Canvas(Modifier.fillMaxSize()) {
                val center = Offset(
                    size.width / 2f,
                    size.height / 2f
                )

                drawLine(
                    color = outline,
                    start = Offset(
                        size.width / 2f,
                        size.height * 0.20f
                    ),
                    end = center,
                    strokeWidth = 7f,
                    cap = StrokeCap.Round
                )

                drawLine(
                    color = outline,
                    start = center,
                    end = Offset(
                        size.width * 0.22f,
                        size.height * 0.80f
                    ),
                    strokeWidth = 7f,
                    cap = StrokeCap.Round
                )

                drawLine(
                    color = outline,
                    start = center,
                    end = Offset(
                        size.width * 0.78f,
                        size.height * 0.80f
                    ),
                    strokeWidth = 7f,
                    cap = StrokeCap.Round
                )

                drawCircle(
                    color = primary,
                    radius = 11f,
                    center = center
                )
            }

            FlowNode(
                title = "Fotovoltaico",
                value = state.raw.solarPowerW,
                icon = Icons.Default.WbSunny,
                modifier = Modifier.align(Alignment.TopCenter)
            )

            FlowNode(
                title = "Casa",
                value = state.raw.homeLoadW,
                icon = Icons.Default.Home,
                modifier = Modifier.align(Alignment.Center)
            )

            FlowNode(
                title = "Powerwall",
                value = state.raw.batteryPowerW,
                subtitle = directionLabel(
                    explicit = state.derived.batteryDirection,
                    rawValue = state.raw.batteryPowerW,
                    positive = "Scarica",
                    negative = "Carica"
                ),
                icon = Icons.Default.BatteryChargingFull,
                modifier = Modifier.align(Alignment.BottomStart)
            )

            FlowNode(
                title = "Rete",
                value = state.raw.gridPowerW,
                subtitle = directionLabel(
                    explicit = state.derived.gridDirection,
                    rawValue = state.raw.gridPowerW,
                    positive = "Import",
                    negative = "Export"
                ),
                icon = Icons.Default.Power,
                modifier = Modifier.align(Alignment.BottomEnd)
            )
        }
    }
}

private fun directionLabel(
    explicit: String,
    rawValue: Double?,
    positive: String,
    negative: String
): String =
    when {
        explicit == "importing" -> "Import"
        explicit == "exporting" -> "Export"
        explicit == "charging" -> "Carica"
        explicit == "discharging" -> "Scarica"
        explicit == "idle" -> "Neutro"
        rawValue == null -> "—"
        rawValue > 20 -> positive
        rawValue < -20 -> negative
        else -> "Neutro"
    }

@Composable
private fun FlowNode(
    title: String,
    value: Double?,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    modifier: Modifier = Modifier,
    subtitle: String? = null
) {
    Surface(
        modifier = modifier.width(132.dp),
        shape = RoundedCornerShape(20.dp),
        tonalElevation = 6.dp
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(icon, contentDescription = title)
            Spacer(Modifier.height(5.dp))
            Text(
                title,
                style = MaterialTheme.typography.labelLarge
            )
            Text(
                formatPower(value),
                fontWeight = FontWeight.Bold
            )
            subtitle?.let {
                Text(
                    it,
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}

@Composable
private fun PercentageCard(
    title: String,
    value: Double?,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(22.dp)
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(
                title,
                style = MaterialTheme.typography.titleMedium
            )
            Spacer(Modifier.height(8.dp))
            Text(
                value?.let { "%.1f%%".format(it) } ?: "—",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
private fun BatteryCard(state: EnergyDashboardState) {
    Card(shape = RoundedCornerShape(24.dp)) {
        Column(Modifier.padding(18.dp)) {
            Text(
                "Powerwall",
                style = MaterialTheme.typography.titleMedium
            )
            Spacer(Modifier.height(8.dp))
            Text(
                state.raw.powerwallSocPct
                    ?.let { "%.1f%%".format(it) }
                    ?: "—",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(Modifier.height(10.dp))
            LinearProgressIndicator(
                progress = {
                    ((state.raw.powerwallSocPct ?: 0.0) / 100.0)
                        .toFloat()
                        .coerceIn(0f, 1f)
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(12.dp),
                strokeCap = StrokeCap.Round
            )
        }
    }
}

@Composable
private fun BalanceCard(
    errorW: Double?,
    source: EnergyDataSource
) {
    Card(shape = RoundedCornerShape(22.dp)) {
        Column(Modifier.padding(16.dp)) {
            Text(
                "Coerenza telemetria",
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                if (source == EnergyDataSource.MQTT_FALLBACK) {
                    "Verifica disponibile con Core Engine"
                } else {
                    val ok =
                        errorW != null &&
                            abs(errorW) <= 150.0

                    when {
                        errorW == null ->
                            "Bilancio non disponibile"
                        ok ->
                            "Bilancio coerente"
                        else ->
                            "Scostamento ${"%.0f".format(abs(errorW))} W"
                    }
                }
            )
        }
    }
}

private fun formatPower(value: Double?): String =
    when {
        value == null -> "—"
        abs(value) >= 1000 ->
            "%.2f kW".format(value / 1000.0)
        else ->
            "%.0f W".format(value)
    }
