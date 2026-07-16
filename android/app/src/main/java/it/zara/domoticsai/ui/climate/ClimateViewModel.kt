package it.zara.domoticsai.ui.climate

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import it.zara.domoticsai.data.core.CoreEngineRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch


class ClimateViewModel(
    private val coreRepository:
        CoreEngineRepository,
    private val baseUrl: String =
        "http://192.168.1.40:8090"
) : ViewModel() {

    val state =
        coreRepository
            .climateState
            .stateIn(
                scope =
                    viewModelScope,
                started =
                    SharingStarted
                        .WhileSubscribed(
                            5_000
                        ),
                initialValue =
                    coreRepository
                        .climateState
                        .value
            )

    init {
        viewModelScope.launch {
            while (isActive) {
                coreRepository
                    .refreshClimate(
                        baseUrl
                    )

                delay(3_000)
            }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            coreRepository
                .refreshClimate(
                    baseUrl
                )
        }
    }
}
