# Dashboard to Android — UI Migration Matrix

| Node-RED widget | Android target | Note |
|---|---|---|
| `ui_gauge` | radial gauge / progress indicator | usare unità e range tipizzati |
| `ui_chart` | chart interattivo | zoom, tooltip, intervalli temporali |
| `ui_switch` | Material Switch | stato richiesto vs confermato |
| `ui_slider` | Slider / discrete slider | validazione range |
| `ui_numeric` | Stepper / numeric field | min/max e unità |
| `ui_dropdown` | Exposed dropdown menu | valori da schema |
| `ui_button` | Filled/Tonal button | conferma per azioni critiche |
| `ui_text` | KPI card / status row | timestamp e qualità dato |
| `ui_template` | componente Compose dedicato | evitare HTML embedded |

## Principio

Ogni controllo Android deve essere collegato a un `ViewModel`, non direttamente al client MQTT.

```text
Compose UI
  -> ViewModel
  -> Use Case
  -> Repository
  -> MQTT Gateway
```
