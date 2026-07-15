package it.zara.domoticsai.ui.context

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.HouseContextItem
import it.zara.domoticsai.domain.model.HouseContextsUiState

@Composable
fun HouseStatusCard(
    state: HouseContextsUiState,
    onRefresh: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement =
                Arrangement.spacedBy(12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment =
                    Alignment.CenterVertically
            ) {
                Column(
                    modifier = Modifier.weight(1f)
                ) {
                    Text(
                        text = "Stato della casa",
                        style =
                            MaterialTheme.typography.titleLarge,
                        fontWeight =
                            FontWeight.SemiBold
                    )

                    Text(
                        text =
                            "Contesti attivi rilevati da DomoticsAI",
                        style =
                            MaterialTheme.typography.bodySmall
                    )
                }

                IconButton(
                    onClick = onRefresh
                ) {
                    Icon(
                        imageVector =
                            Icons.Default.Refresh,
                        contentDescription =
                            "Aggiorna stato casa"
                    )
                }
            }

            if (state.loading) {
                LinearProgressIndicator(
                    modifier = Modifier.fillMaxWidth()
                )
            }

            state.error?.let { error ->
                Card(
                    colors =
                        CardDefaults.cardColors(
                            containerColor =
                                MaterialTheme.colorScheme
                                    .errorContainer
                        )
                ) {
                    Text(
                        text = error,
                        modifier =
                            Modifier.padding(12.dp),
                        color =
                            MaterialTheme.colorScheme
                                .onErrorContainer
                    )
                }
            }

            if (
                !state.loading
                && state.items.isEmpty()
            ) {
                Text(
                    text =
                        "Stato casa normale. "
                            + "Nessun contesto speciale attivo.",
                    style =
                        MaterialTheme.typography.bodyMedium
                )
            }

            state.items
                .take(MAX_VISIBLE_CONTEXTS)
                .forEach { context ->
                    HouseContextRow(
                        context = context
                    )
                }

            if (
                state.items.size
                > MAX_VISIBLE_CONTEXTS
            ) {
                Text(
                    text =
                        "Altri "
                            + (
                                state.items.size
                                    - MAX_VISIBLE_CONTEXTS
                                )
                            + " contesti attivi",
                    style =
                        MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}

@Composable
private fun HouseContextRow(
    context: HouseContextItem
) {
    Card(
        colors =
            CardDefaults.cardColors(
                containerColor =
                    contextContainerColor(
                        context.category
                    )
            )
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            verticalArrangement =
                Arrangement.spacedBy(4.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment =
                    Alignment.CenterVertically
            ) {
                Text(
                    text = contextTitle(
                        context.name
                    ),
                    modifier =
                        Modifier.weight(1f),
                    style =
                        MaterialTheme.typography.titleMedium,
                    fontWeight =
                        FontWeight.SemiBold
                )

                Text(
                    text =
                        "Priorità ${context.priority}",
                    style =
                        MaterialTheme.typography.labelSmall
                )
            }

            Text(
                text = contextDescription(
                    context
                ),
                style =
                    MaterialTheme.typography.bodyMedium
            )

            if (
                context.confidence < 1.0
            ) {
                Text(
                    text =
                        "Confidenza: "
                            + "%.0f%%".format(
                                context.confidence
                                    * 100.0
                            ),
                    style =
                        MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}

@Composable
private fun contextContainerColor(
    category: String
) =
    when (
        category.lowercase()
    ) {
        "scene" ->
            MaterialTheme.colorScheme
                .tertiaryContainer

        "energy" ->
            MaterialTheme.colorScheme
                .secondaryContainer

        "pool" ->
            MaterialTheme.colorScheme
                .primaryContainer

        "lighting" ->
            MaterialTheme.colorScheme
                .surfaceVariant

        else ->
            MaterialTheme.colorScheme
                .surfaceVariant
    }

private fun contextTitle(
    name: String
): String =
    when (name) {
        "SOLAR_SURPLUS" ->
            "Surplus fotovoltaico"

        "GRID_IMPORT" ->
            "Prelievo dalla rete"

        "BATTERY_CHARGING" ->
            "Batteria in carica"

        "ALL_LIGHTS_OFF" ->
            "Tutte le luci spente"

        "POOL_RUNNING" ->
            "Piscina in funzione"

        "POOL_LIGHTING" ->
            "Illuminazione piscina attiva"

        "TV_MODE_ACTIVE" ->
            "Modalità TV attiva"

        "SLEEP_MODE_ACTIVE" ->
            "Modalità notte attiva"

        "HOUSE_NORMAL" ->
            "Stato casa normale"

        else ->
            name
                .lowercase()
                .replace("_", " ")
                .replaceFirstChar {
                    it.uppercase()
                }
    }

private fun contextDescription(
    context: HouseContextItem
): String =
    when (context.name) {
        "SOLAR_SURPLUS" ->
            "La produzione fotovoltaica supera il fabbisogno della casa."

        "GRID_IMPORT" ->
            "La casa sta prelevando energia dalla rete."

        "BATTERY_CHARGING" ->
            "La batteria domestica è in fase di carica."

        "ALL_LIGHTS_OFF" ->
            "Non risultano luci accese."

        "POOL_RUNNING" -> {
            val filtering =
                context.data[
                    "filteringState"
                ]

            if (
                filtering == "active"
            ) {
                "La filtrazione della piscina è attiva."
            } else {
                "Uno o più impianti della piscina sono in funzione."
            }
        }

        "POOL_LIGHTING" ->
            "Le luci della piscina sono accese."

        "TV_MODE_ACTIVE" ->
            "È attiva la configurazione luminosa per la visione TV."

        "SLEEP_MODE_ACTIVE" ->
            "È attiva la configurazione prevista per la notte."

        "HOUSE_NORMAL" ->
            "La casa non presenta condizioni speciali."

        else ->
            context.reasons
                .firstOrNull()
                ?: "Contesto rilevato dal sistema."
    }

private const val MAX_VISIBLE_CONTEXTS = 6
