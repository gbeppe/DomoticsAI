package it.zara.domoticsai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import it.zara.domoticsai.domain.model.ConnectionSettings
import it.zara.domoticsai.ui.home.*
import it.zara.domoticsai.ui.logs.LogsScreen
import it.zara.domoticsai.ui.settings.SettingsScreen
import it.zara.domoticsai.ui.theme.DomoticsAiTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val container = (application as DomoticsAiApplication).container

        setContent {
            DomoticsAiTheme {
                val settings by container.settingsRepository.settings.collectAsState(
                    initial = ConnectionSettings()
                )
                val logs by container.domoticsRepository.logs.collectAsState()
                val scope = rememberCoroutineScope()
                var destination by remember {
                    mutableStateOf(Destination.HOME)
                }

                val homeViewModel: HomeViewModel = viewModel(
                    factory = SimpleViewModelFactory {
                        HomeViewModel(
                            repository = container.domoticsRepository,
                            credentialStore = container.credentialStore
                        )
                    }
                )

                Scaffold(
                    bottomBar = {
                        NavigationBar {
                            Destination.entries.forEach { item ->
                                NavigationBarItem(
                                    selected = destination == item,
                                    onClick = { destination = item },
                                    icon = {
                                        Icon(
                                            when (item) {
                                                Destination.HOME ->
                                                    Icons.Default.Home
                                                Destination.LOGS ->
                                                    Icons.Default.List
                                                Destination.SETTINGS ->
                                                    Icons.Default.Settings
                                            },
                                            contentDescription = item.label
                                        )
                                    },
                                    label = { Text(item.label) }
                                )
                            }
                        }
                    }
                ) { outerPadding ->
                    Box(
                        Modifier
                            .fillMaxSize()
                            .padding(outerPadding)
                    ) {
                        when (destination) {
                            Destination.HOME -> {
                                HomeScreen(homeViewModel, settings)
                            }

                            Destination.LOGS -> {
                                LogsScreen(logs)
                            }

                            Destination.SETTINGS -> {
                                SettingsScreen(
                                    initial = settings,
                                    initialCredentials =
                                        container.credentialStore.load()
                                ) { newSettings, credentials ->
                                    container.credentialStore.save(credentials)
                                    scope.launch {
                                        container.settingsRepository.save(
                                            newSettings
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

private enum class Destination(val label: String) {
    HOME("Home"),
    LOGS("Log"),
    SETTINGS("Impostazioni")
}
