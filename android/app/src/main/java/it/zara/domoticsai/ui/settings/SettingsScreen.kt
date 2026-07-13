package it.zara.domoticsai.ui.settings

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    initial: ConnectionSettings,
    onSave: (ConnectionSettings) -> Unit
) {
    var localHost by remember(initial) { mutableStateOf(initial.local.host) }
    var localPort by remember(initial) { mutableStateOf(initial.local.port.toString()) }
    var remoteHost by remember(initial) { mutableStateOf(initial.remote.host) }
    var remotePort by remember(initial) { mutableStateOf(initial.remote.port.toString()) }
    var mode by remember(initial) { mutableStateOf(initial.mode) }

    Scaffold(topBar = { TopAppBar(title = { Text("Connessioni") }) }) { padding ->
        Column(
            Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("Modalità", style = MaterialTheme.typography.titleMedium)

            SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth()) {
                ConnectionMode.entries.forEachIndexed { index, item ->
                    SegmentedButton(
                        selected = mode == item,
                        onClick = { mode = item },
                        shape = SegmentedButtonDefaults.itemShape(index, ConnectionMode.entries.size)
                    ) {
                        Text(item.name.replace("_", " "))
                    }
                }
            }

            Text("Broker locale", style = MaterialTheme.typography.titleMedium)

            OutlinedTextField(
                value = localHost,
                onValueChange = { localHost = it },
                label = { Text("Host") },
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = localPort,
                onValueChange = { localPort = it.filter(Char::isDigit) },
                label = { Text("Porta") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                modifier = Modifier.fillMaxWidth()
            )

            Text("Broker remoto / Tailscale", style = MaterialTheme.typography.titleMedium)

            OutlinedTextField(
                value = remoteHost,
                onValueChange = { remoteHost = it },
                label = { Text("Host") },
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = remotePort,
                onValueChange = { remotePort = it.filter(Char::isDigit) },
                label = { Text("Porta") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                modifier = Modifier.fillMaxWidth()
            )

            Text(
                "Le credenziali verranno aggiunte nel prossimo incremento usando Android Keystore.",
                style = MaterialTheme.typography.bodySmall
            )

            Button(
                onClick = {
                    onSave(
                        ConnectionSettings(
                            mode = mode,
                            local = BrokerEndpoint(localHost, localPort.toIntOrNull() ?: 1883),
                            remote = BrokerEndpoint(remoteHost, remotePort.toIntOrNull() ?: 1883)
                        )
                    )
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Salva")
            }
        }
    }
}
