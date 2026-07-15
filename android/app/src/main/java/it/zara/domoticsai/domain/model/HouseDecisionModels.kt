package it.zara.domoticsai.domain.model

enum class HouseDecisionKind {
    RECOMMENDATION,
    WARNING,
    INFORMATION,
    UNKNOWN
}

data class HouseDecisionItem(
    val decisionId: String,
    val ruleId: String,
    val kind: HouseDecisionKind,
    val action: String,
    val title: String,
    val description: String,
    val priority: Int,
    val confidence: Double,
    val reasons: List<String>,
    val contextNames: List<String>,
    val executionAllowed: Boolean,
    val requiresConfirmation: Boolean,
    val suggestedAction: String?,
    val createdAt: String
)

data class HouseDecisionsResult(
    val decisions: List<HouseDecisionItem>,
    val executionEnabled: Boolean
)

data class HouseDecisionsUiState(
    val loading: Boolean = false,
    val items: List<HouseDecisionItem> = emptyList(),
    val executionEnabled: Boolean = false,
    val error: String? = null
)
