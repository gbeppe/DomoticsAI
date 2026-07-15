package it.zara.domoticsai.ui.intelligence

import androidx.compose.material3.AssistChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.LaunchedEffect
import it.zara.domoticsai.domain.model.HomeIntelligenceFreshness
import it.zara.domoticsai.domain.model.HomeIntelligenceUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive

@Composable
fun HomeIntelligenceStatus(
    state: HomeIntelligenceUiState
) {
    var nowEpochMs by remember {
        mutableLongStateOf(
            System.currentTimeMillis()
        )
    }

    LaunchedEffect(Unit) {
        while (isActive) {
            delay(5_000)
            nowEpochMs =
                System.currentTimeMillis()
        }
    }

    val freshness =
        state.freshness(nowEpochMs)

    val label =
        when (freshness) {
            HomeIntelligenceFreshness.CURRENT ->
                "Assistente domestico aggiornato"

            HomeIntelligenceFreshness.STALE ->
                "Ultimo stato disponibile"

            HomeIntelligenceFreshness.UNAVAILABLE ->
                if (state.loading) {
                    "Assistente domestico in aggiornamento"
                } else {
                    "Assistente domestico non disponibile"
                }
        }

    AssistChip(
        onClick = {},
        label = {
            Text(label)
        }
    )

    if (
        freshness
        == HomeIntelligenceFreshness.STALE
        && state.error != null
    ) {
        Text(
            text =
                "I dati mostrati potrebbero "
                    + "non rappresentare lo stato attuale.",
            style =
                MaterialTheme.typography.bodySmall,
            color =
                MaterialTheme.colorScheme.error
        )
    }
}
