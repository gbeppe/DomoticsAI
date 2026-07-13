package it.zara.domoticsai.ui.settings

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import it.zara.domoticsai.domain.model.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    initial: ConnectionSettings,
    initialCredentials: AppCredentials,
    onSave: (ConnectionSettings, AppCredentials) -> Unit
) {
    var localHost by remember(initial) { mutableStateOf(initial.local.host) }
    var localPort by remember(initial) { mutableStateOf(initial.local.port.toString()) }
    var remoteHost by remember(initial) { mutableStateOf(initial.remote.host) }
    var remotePort by remember(initial) { mutableStateOf(initial.remote.port.toString()) }
    var mode by remember(initial) { mutableStateOf(initial.mode) }

    var localUsername by remember(initialCredentials) {
        mutableStateOf(initialCredentials.local.username)
    }
    var localPassword by remember(initialCredentials) {
        mutableStateOf(initialCredentials.local.password)
    }
    var remoteUsername by remember(initialCredentials) {
        mutableStateOf(initialCredentials.remote.username)
    }
    var remotePassword by remember(initialCredentials) {
        mutableStateOf(initialCredentials.remote.password)
    }

    var savedMessageVisible by remember { mutableStateOf(false) }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Connessioni") }) }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding()
                .navigationBarsPadding()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("Modalità", style = MaterialTheme.typography.titleMedium)

            SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth()) {
                ConnectionMode.entries.forEachIndexed { index, item ->
                    SegmentedButton(
                        selected = mode == item,
                        onClick = { mode = item },
                        shape = SegmentedButtonDefaults.itemShape(
                            index,
                            ConnectionMode.entries.size
                        )
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
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = localPort,
                onValueChange = { localPort = it.filter(Char::isDigit) },
                label = { Text("Porta") },
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = localUsername,
                onValueChange = { localUsername = it },
                label = { Text("Username") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = localPassword,
                onValueChange = { localPassword = it },
                label = { Text("Password") },
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth()
            )

            HorizontalDivider()

            Text(
                "Broker remoto / Tailscale",
                style = MaterialTheme.typography.titleMedium
            )

            OutlinedTextField(
                value = remoteHost,
                onValueChange = { remoteHost = it },
                label = { Text("Host") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = remotePort,
                onValueChange = { remotePort = it.filter(Char::isDigit) },
                label = { Text("Porta") },
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = remoteUsername,
                onValueChange = { remoteUsername = it },
                label = { Text("Username") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = remotePassword,
                onValueChange = { remotePassword = it },
                label = { Text("Password") },
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth()
            )

            Text(
                "Le password vengono cifrate con Android Keystore.",
                style = MaterialTheme.typography.bodySmall
            )

            Button(
                onClick = {
                    onSave(
                        ConnectionSettings(
                            mode = mode,
                            local = BrokerEndpoint(
                                host = localHost.trim(),
                                port = localPort.toIntOrNull() ?: 1884
                            ),
                            remote = BrokerEndpoint(
                                host = remoteHost.trim(),
                                port = remotePort.toIntOrNull() ?: 1884
                            )
                        ),
                        AppCredentials(
                            local = BrokerCredentials(
                                username = localUsername,
                                password = localPassword
                            ),
                            remote = BrokerCredentials(
                                username = remoteUsername,
                                password = remotePassword
                            )
                        )
                    )
                    savedMessageVisible = true
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Salva impostazioni")
            }

            if (savedMessageVisible) {
                Text(
                    text = "Impostazioni salvate",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.primary
                )
            }

            Spacer(Modifier.height(24.dp))
        }
    }
}
