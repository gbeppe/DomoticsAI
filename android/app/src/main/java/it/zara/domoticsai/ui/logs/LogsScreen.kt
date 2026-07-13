package it.zara.domoticsai.ui.logs

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.LogEntry
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LogsScreen(logs: List<LogEntry>) {
    val formatter = remember { SimpleDateFormat("HH:mm:ss", Locale.ITALY) }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Log MQTT") }) }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(12.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(logs) { entry ->
                Card {
                    Column(Modifier.padding(12.dp)) {
                        Text(
                            "${formatter.format(Date(entry.timestampEpochMs))}  ${entry.direction}",
                            style = MaterialTheme.typography.labelMedium
                        )
                        Text(entry.topic, style = MaterialTheme.typography.titleSmall)
                        Text(entry.payload, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
}
