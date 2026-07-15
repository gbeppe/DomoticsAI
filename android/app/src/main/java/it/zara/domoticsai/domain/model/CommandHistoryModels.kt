package it.zara.domoticsai.domain.model

data class CommandHistoryItem(
    val commandId: String,
    val domain: String,
    val action: String,
    val target: String,
    val source: String,
    val state: UiCommandState,
    val createdAt: String,
    val updatedAt: String,
    val mode: String,
    val error: String? = null
)

data class CommandsScreenState(
    val loading: Boolean = false,
    val connectedToStream: Boolean = false,
    val items: List<CommandHistoryItem> = emptyList(),
    val error: String? = null
)
