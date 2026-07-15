package it.zara.domoticsai.ui.decisions

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.AssistChip
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
import it.zara.domoticsai.domain.model.HouseDecisionItem
import it.zara.domoticsai.domain.model.HouseDecisionKind
import it.zara.domoticsai.domain.model.HouseDecisionsUiState

@Composable
fun DecisionsCard(
    state: HouseDecisionsUiState,
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
                        text = "Suggerimenti",
                        style =
                            MaterialTheme.typography.titleLarge,
                        fontWeight =
                            FontWeight.SemiBold
                    )

                    Text(
                        text =
                            "Analisi consultiva dello stato della casa",
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
                            "Aggiorna suggerimenti"
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
                                .onErrorContainer,
                        style =
                            MaterialTheme.typography.bodyMedium
                    )
                }
            }

            if (
                !state.loading
                && state.items.isEmpty()
            ) {
                Text(
                    text =
                        "Nessun suggerimento attivo. "
                            + "Lo stato della casa non "
                            + "richiede attenzione.",
                    style =
                        MaterialTheme.typography.bodyMedium
                )
            }

            state.items
                .take(MAX_VISIBLE_DECISIONS)
                .forEach { decision ->
                    DecisionItem(
                        decision = decision
                    )
                }

            if (
                state.items.size
                > MAX_VISIBLE_DECISIONS
            ) {
                Text(
                    text =
                        "Altri "
                            + (
                                state.items.size
                                    - MAX_VISIBLE_DECISIONS
                                )
                            + " suggerimenti disponibili",
                    style =
                        MaterialTheme.typography.bodySmall
                )
            }

            AssistChip(
                onClick = {},
                label = {
                    Text(
                        if (
                            state.executionEnabled
                        ) {
                            "Esecuzione automatica abilitata"
                        } else {
                            "Solo consultazione"
                        }
                    )
                }
            )
        }
    }
}

@Composable
private fun DecisionItem(
    decision: HouseDecisionItem
) {
    val containerColor =
        when (decision.kind) {
            HouseDecisionKind.WARNING ->
                MaterialTheme.colorScheme
                    .errorContainer

            HouseDecisionKind.RECOMMENDATION ->
                MaterialTheme.colorScheme
                    .secondaryContainer

            HouseDecisionKind.INFORMATION,
            HouseDecisionKind.UNKNOWN ->
                MaterialTheme.colorScheme
                    .surfaceVariant
        }

    val contentColor =
        when (decision.kind) {
            HouseDecisionKind.WARNING ->
                MaterialTheme.colorScheme
                    .onErrorContainer

            HouseDecisionKind.RECOMMENDATION ->
                MaterialTheme.colorScheme
                    .onSecondaryContainer

            HouseDecisionKind.INFORMATION,
            HouseDecisionKind.UNKNOWN ->
                MaterialTheme.colorScheme
                    .onSurfaceVariant
        }

    Card(
        colors =
            CardDefaults.cardColors(
                containerColor = containerColor,
                contentColor = contentColor
            )
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement =
                Arrangement.spacedBy(5.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment =
                    Alignment.CenterVertically
            ) {
                Text(
                    text = kindLabel(
                        decision.kind
                    ),
                    style =
                        MaterialTheme.typography.labelMedium,
                    fontWeight =
                        FontWeight.Bold,
                    modifier =
                        Modifier.weight(1f)
                )

                Text(
                    text =
                        "Priorità ${decision.priority}",
                    style =
                        MaterialTheme.typography.labelSmall
                )
            }

            Text(
                text = decision.title,
                style =
                    MaterialTheme.typography.titleMedium,
                fontWeight =
                    FontWeight.SemiBold
            )

            if (
                decision.description.isNotBlank()
            ) {
                Text(
                    text = decision.description,
                    style =
                        MaterialTheme.typography.bodyMedium
                )
            }

            if (
                decision.confidence < 1.0
            ) {
                Spacer(
                    modifier = Modifier.height(2.dp)
                )

                Text(
                    text =
                        "Confidenza: "
                            + "%.0f%%".format(
                                decision.confidence
                                    * 100.0
                            ),
                    style =
                        MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}

private fun kindLabel(
    kind: HouseDecisionKind
): String =
    when (kind) {
        HouseDecisionKind.WARNING ->
            "Avviso"

        HouseDecisionKind.RECOMMENDATION ->
            "Raccomandazione"

        HouseDecisionKind.INFORMATION ->
            "Informazione"

        HouseDecisionKind.UNKNOWN ->
            "Suggerimento"
    }

private const val MAX_VISIBLE_DECISIONS = 3
