package it.zara.domoticsai.ui.theme

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColors = darkColorScheme(
    primary = Color(0xFF35D6A1),
    secondary = Color(0xFF77D7FF),
    tertiary = Color(0xFFFFC857),
    background = Color(0xFF08110F),
    surface = Color(0xFF101C19),
    surfaceVariant = Color(0xFF182824)
)

@Composable
fun DomoticsAiTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = DarkColors,
        typography = Typography(),
        content = content
    )
}
