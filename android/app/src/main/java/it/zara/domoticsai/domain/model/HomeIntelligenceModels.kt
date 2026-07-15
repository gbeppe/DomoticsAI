package it.zara.domoticsai.domain.model

data class HomeIntelligenceSummary(
    val activeContexts: Int = 0,
    val activeDecisions: Int = 0,
    val warnings: Int = 0,
    val recommendations: Int = 0,
    val information: Int = 0
)

data class HomeIntelligenceSnapshot(
    val generatedAt: String?,
    val knowledgeUpdatedAt: String?,
    val contexts: List<HouseContextItem>,
    val decisions: List<HouseDecisionItem>,
    val summary: HomeIntelligenceSummary,
    val executionEnabled: Boolean
)

data class HomeIntelligenceUiState(
    val loading: Boolean = false,
    val contexts: List<HouseContextItem> = emptyList(),
    val decisions: List<HouseDecisionItem> = emptyList(),
    val summary: HomeIntelligenceSummary =
        HomeIntelligenceSummary(),
    val executionEnabled: Boolean = false,
    val generatedAt: String? = null,
    val knowledgeUpdatedAt: String? = null,
    val lastSuccessfulUpdateEpochMs: Long? = null,
    val error: String? = null
)
