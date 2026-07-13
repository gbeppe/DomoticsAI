package it.zara.domoticsai.ui.diagnostics

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineRepository
import kotlinx.coroutines.launch

class DiagnosticsViewModel(
    private val repository: CoreEngineRepository
) : ViewModel() {
    val state = repository.state

    fun refresh(baseUrl: String) {
        viewModelScope.launch { repository.refresh(baseUrl) }
    }
}
