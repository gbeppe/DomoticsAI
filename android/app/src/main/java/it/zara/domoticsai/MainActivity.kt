package it.zara.domoticsai




import it.zara.domoticsai.ui.intelligence.HomeIntelligenceViewModel
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Storage
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import it.zara.domoticsai.domain.model.ConnectionSettings
import it.zara.domoticsai.ui.commands.*
import it.zara.domoticsai.ui.diagnostics.*
import it.zara.domoticsai.ui.energy.*
import it.zara.domoticsai.ui.home.*
import it.zara.domoticsai.ui.lights.*
import it.zara.domoticsai.ui.logs.LogsScreen
import it.zara.domoticsai.ui.settings.SettingsScreen
import it.zara.domoticsai.ui.theme.DomoticsAiTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val container =
            (application as DomoticsAiApplication).container

        setContent {
            DomoticsAiTheme {
                val settings by
                    container.settingsRepository
                        .settings
                        .collectAsState(
                            initial = ConnectionSettings()
                        )

                val logs by
                    container.domoticsRepository
                        .logs
                        .collectAsState()

                val scope = rememberCoroutineScope()

                var destination by remember {
                    mutableStateOf(Destination.HOME)
                }

                val homeViewModel: HomeViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                HomeViewModel(
                                    repository =
                                        container.domoticsRepository,
                                    credentialStore =
                                        container.credentialStore,
                                    coreEngineRepository =
                                        container.coreEngineRepository
                                )
                            }
                    )

                val energyViewModel: EnergyViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                EnergyViewModel(
                                    coreRepository =
                                        container.coreEngineRepository,
                                    domoticsRepository =
                                        container.domoticsRepository
                                )
                            }
                    )

                val lightsViewModel: LightsViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                LightsViewModel(
                                    repository =
                                        container.coreEngineRepository
                                )
                            }
                    )

                val commandsViewModel:
                    CommandsViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                CommandsViewModel()
                            }
                    )
                val homeIntelligenceViewModel:
                    HomeIntelligenceViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                HomeIntelligenceViewModel()
                            }
                    )

                val diagnosticsViewModel:
                    DiagnosticsViewModel =
                    viewModel(
                        factory =
                            SimpleViewModelFactory {
                                DiagnosticsViewModel(
                                    repository =
                                        container.coreEngineRepository
                                )
                            }
                    )

                val energyState by
                    energyViewModel.state.collectAsState()

                val lightsState by
                    lightsViewModel.state.collectAsState()

                val lightCommands by
                    lightsViewModel.commands.collectAsState()

                val commandsState by
                    commandsViewModel.state.collectAsState()
                val homeIntelligenceState by
                    homeIntelligenceViewModel.state
                        .collectAsState()

                val diagnosticsState by
                    diagnosticsViewModel.state.collectAsState()

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
                                                Destination.ENERGY ->
                                                    Icons.Default.Bolt
                                                Destination.LIGHTS ->
                                                    Icons.Default.Lightbulb
                                                Destination.COMMANDS ->
                                                    Icons.Default.History
                                                Destination.LOGS ->
                                                    Icons.Default.List
                                                Destination.CORE ->
                                                    Icons.Default.Storage
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
                            Destination.HOME ->
                                HomeScreen(
                                    viewModel =
                                        homeViewModel,
                                    settings =
                                        settings,
                                    intelligenceState =
                                        homeIntelligenceState,
                                    onIntelligenceRefresh =
                                        homeIntelligenceViewModel::refresh
                                )

                            Destination.ENERGY ->
                                EnergyScreen(
                                    state = energyState,
                                    onRefresh =
                                        energyViewModel::refresh
                                )

                            Destination.LIGHTS ->
                                LightsScreen(
                                    state = lightsState,
                                    commandStates =
                                        lightCommands,
                                    onRefresh =
                                        lightsViewModel::refresh,
                                    onToggleSimulation =
                                        lightsViewModel::simulateToggle,
                                    onClearCommand =
                                        lightsViewModel::clearCommand
                                )

                            Destination.COMMANDS ->
                                CommandsScreen(
                                    state = commandsState,
                                    onRefresh =
                                        commandsViewModel::refresh
                                )

                            Destination.LOGS ->
                                LogsScreen(logs)

                            Destination.CORE ->
                                DiagnosticsScreen(
                                    state = diagnosticsState,
                                    baseUrl =
                                        "http://192.168.1.40:8090",
                                    onRefresh = {
                                        diagnosticsViewModel.refresh(
                                            "http://192.168.1.40:8090"
                                        )
                                    }
                                )

                            Destination.SETTINGS ->
                                SettingsScreen(
                                    initial = settings,
                                    initialCredentials =
                                        container.credentialStore.load()
                                ) {
                                        newSettings,
                                        credentials ->

                                    container.credentialStore
                                        .save(credentials)

                                    scope.launch {
                                        container.settingsRepository
                                            .save(newSettings)
                                    }
                                }
                        }
                    }
                }
            }
        }
    }
}

private enum class Destination(
    val label: String
) {
    HOME("Home"),
    ENERGY("Energia"),
    LIGHTS("Luci"),
    COMMANDS("Comandi"),
    LOGS("Log"),
    CORE("Core"),
    SETTINGS("Impostazioni")
}
