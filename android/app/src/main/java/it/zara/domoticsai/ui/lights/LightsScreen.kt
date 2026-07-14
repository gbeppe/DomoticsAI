package it.zara.domoticsai.ui.lights

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ElectricalServices
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LightsScreen(
    state: LightsDashboardState,
    commandStates: Map<String, DeviceCommandUiState>,
    onRefresh: () -> Unit,
    onToggleSimulation: (LightDevice) -> Unit,
    onClearCommand: (LightDevice) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Luci") },
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
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement =
                Arrangement.spacedBy(12.dp)
        ) {
            item {
                AssistChip(
                    onClick = {},
                    label = {
                        Text(
                            "Modalità comandi: simulazione"
                        )
                    }
                )
            }

            if (state.loading) {
                item {
                    LinearProgressIndicator(
                        Modifier.fillMaxWidth()
                    )
                }
            }

            state.error?.let { error ->
                item {
                    Card(
                        colors = CardDefaults.cardColors(
                            containerColor =
                                MaterialTheme.colorScheme
                                    .errorContainer
                        )
                    ) {
                        Text(
                            error,
                            Modifier.padding(16.dp)
                        )
                    }
                }
            }

            item {
                SummaryCard(state.summary)
            }

            LightArea.entries.forEach { area ->
                val devices =
                    state.devices.filter {
                        it.area == area
                    }

                item {
                    Text(
                        areaTitle(area),
                        style =
                            MaterialTheme.typography
                                .titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                }

                items(
                    items = devices,
                    key = {
                        "${it.area.name}-${it.id}"
                    }
                ) { device ->
                    val key =
                        "${device.area.name}/${device.id}"

                    DeviceCard(
                        device = device,
                        commandState =
                            commandStates[key],
                        onToggleSimulation = {
                            onToggleSimulation(device)
                        },
                        onClearCommand = {
                            onClearCommand(device)
                        }
                    )
                }
            }

            item {
                Text(
                    "Scenari",
                    style =
                        MaterialTheme.typography
                            .titleLarge,
                    fontWeight = FontWeight.Bold
                )
            }

            item {
                ScenesReadOnlyCard()
            }
        }
    }
}

@Composable
private fun SummaryCard(
    summary: LightsSummary
) {
    Card(shape = RoundedCornerShape(24.dp)) {
        Column(
            Modifier.padding(18.dp),
            verticalArrangement =
                Arrangement.spacedBy(8.dp)
        ) {
            Text(
                "Riepilogo",
                style =
                    MaterialTheme.typography.titleMedium
            )
            Text(
                "Luci accese: ${summary.lightsOnTotal}",
                style =
                    MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Text(
                "Relè attivi: ${summary.relaysOnTotal}"
            )
            Text(
                "Interno ${summary.internalOn}/${summary.internalTotal} · " +
                    "Esterno ${summary.externalOn}/${summary.externalTotal} · " +
                    "Piscina ${summary.poolOn}/${summary.poolTotal}"
            )
        }
    }
}

@Composable
private fun DeviceCard(
    device: LightDevice,
    commandState: DeviceCommandUiState?,
    onToggleSimulation: () -> Unit,
    onClearCommand: () -> Unit
) {
    val pending =
        commandState?.state in setOf(
            UiCommandState.SENDING,
            UiCommandState.WAITING_CONFIRMATION
        )

    Card(shape = RoundedCornerShape(20.dp)) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement =
                Arrangement.spacedBy(10.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment =
                    Alignment.CenterVertically
            ) {
                Icon(
                    imageVector =
                        if (
                            device.type ==
                            LightDeviceType.RELAY
                        ) {
                            Icons.Default
                                .ElectricalServices
                        } else {
                            Icons.Default.Lightbulb
                        },
                    contentDescription = device.label
                )

                Spacer(Modifier.width(14.dp))

                Column(
                    modifier = Modifier.weight(1f)
                ) {
                    Text(
                        device.label,
                        style =
                            MaterialTheme.typography
                                .titleMedium,
                        fontWeight =
                            FontWeight.SemiBold
                    )
                    Text(
                        when (device.type) {
                            LightDeviceType.LIGHT ->
                                "Luce"
                            LightDeviceType.RELAY ->
                                "Relè"
                        },
                        style =
                            MaterialTheme.typography
                                .bodySmall
                    )
                }

                AssistChip(
                    onClick = {},
                    label = {
                        Text(
                            when {
                                !device.available ->
                                    "Non disponibile"
                                device.state == LightState.ON ->
                                    "ON"
                                device.state == LightState.OFF ->
                                    "OFF"
                                else ->
                                    "?"
                            }
                        )
                    }
                )
            }

            Button(
                onClick = onToggleSimulation,
                enabled =
                    device.available &&
                        !pending,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    if (device.state == LightState.ON) {
                        "Simula spegnimento"
                    } else {
                        "Simula accensione"
                    }
                )
            }

            commandState?.let {
                CommandStatusCard(
                    state = it,
                    onClear = onClearCommand
                )
            }
        }
    }
}

@Composable
private fun CommandStatusCard(
    state: DeviceCommandUiState,
    onClear: () -> Unit
) {
    val label = when (state.state) {
        UiCommandState.IDLE ->
            "Pronto"
        UiCommandState.SENDING ->
            "Invio…"
        UiCommandState.WAITING_CONFIRMATION ->
            "In attesa di ACK…"
        UiCommandState.SIMULATED ->
            "Comando simulato"
        UiCommandState.CONFIRMED ->
            "Comando confermato"
        UiCommandState.REJECTED ->
            "Comando rifiutato"
        UiCommandState.TIMEOUT ->
            "Timeout"
        UiCommandState.FAILED ->
            "Errore"
    }

    Surface(
        shape = RoundedCornerShape(16.dp),
        tonalElevation = 2.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment =
                Alignment.CenterVertically
        ) {
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    label,
                    fontWeight = FontWeight.SemiBold
                )
                state.desiredState?.let {
                    Text(
                        "Richiesto: ${it.name}",
                        style =
                            MaterialTheme.typography
                                .bodySmall
                    )
                }
                state.message?.let {
                    Text(
                        it,
                        style =
                            MaterialTheme.typography
                                .bodySmall
                    )
                }
            }

            if (
                state.state !in setOf(
                    UiCommandState.SENDING,
                    UiCommandState.WAITING_CONFIRMATION
                )
            ) {
                TextButton(onClick = onClear) {
                    Text("Chiudi")
                }
            }
        }
    }
}

@Composable
private fun ScenesReadOnlyCard() {
    Card(shape = RoundedCornerShape(20.dp)) {
        Column(
            Modifier.padding(16.dp),
            verticalArrangement =
                Arrangement.spacedBy(8.dp)
        ) {
            Text("ALL_ON · ALL_OFF")
            Text("TV_MODE · SLEEP_MODE")
            Text(
                "Gli scenari saranno collegati al Command Manager nel prossimo incremento.",
                style =
                    MaterialTheme.typography.bodySmall
            )
        }
    }
}

private fun areaTitle(
    area: LightArea
): String =
    when (area) {
        LightArea.INTERNAL -> "Interno"
        LightArea.EXTERNAL -> "Esterno"
        LightArea.POOL -> "Piscina"
    }
