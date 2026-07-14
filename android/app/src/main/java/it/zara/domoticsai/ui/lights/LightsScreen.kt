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
    onRefresh: () -> Unit
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
                if (state.loading) {
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

                if (devices.isEmpty()) {
                    item {
                        Text(
                            "Nessun dispositivo disponibile",
                            style =
                                MaterialTheme.typography
                                    .bodyMedium
                        )
                    }
                } else {
                    items(
                        items = devices,
                        key = {
                            "${it.area.name}-${it.id}"
                        }
                    ) { device ->
                        DeviceCard(device)
                    }
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
    Card(
        shape = RoundedCornerShape(24.dp)
    ) {
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

            if (summary.unknownTotal > 0) {
                AssistChip(
                    onClick = {},
                    label = {
                        Text(
                            "Stato sconosciuto: ${summary.unknownTotal}"
                        )
                    }
                )
            }
        }
    }
}

@Composable
private fun DeviceCard(
    device: LightDevice
) {
    Card(
        shape = RoundedCornerShape(20.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
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
                    fontWeight = FontWeight.SemiBold
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

            StatusPill(device)
        }
    }
}

@Composable
private fun StatusPill(
    device: LightDevice
) {
    val label =
        if (!device.available) {
            "Non disponibile"
        } else {
            when (device.state) {
                LightState.ON -> "ON"
                LightState.OFF -> "OFF"
                LightState.UNKNOWN -> "?"
            }
        }

    AssistChip(
        onClick = {},
        label = { Text(label) }
    )
}

@Composable
private fun ScenesReadOnlyCard() {
    Card(
        shape = RoundedCornerShape(20.dp)
    ) {
        Column(
            Modifier.padding(16.dp),
            verticalArrangement =
                Arrangement.spacedBy(8.dp)
        ) {
            Text("ALL_ON · ALL_OFF")
            Text("TV_MODE · SLEEP_MODE")
            Text(
                "I comandi saranno abilitati nella fase successiva.",
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
