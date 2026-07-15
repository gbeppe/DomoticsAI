package it.zara.domoticsai.domain.model

data class HouseContextItem(
    val name: String,
    val priority: Int,
    val category: String,
    val confidence: Double,
    val reasons: List<String>,
    val observedAt: String?,
    val data: Map<String, String>
)

data class HouseContextsResult(
    val contexts: List<HouseContextItem>
)

data class HouseContextsUiState(
    val loading: Boolean = false,
    val items: List<HouseContextItem> = emptyList(),
    val error: String? = null,
    val lastSuccessfulUpdateEpochMs: Long? = null
)
