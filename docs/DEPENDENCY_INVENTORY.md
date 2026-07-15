# DomoticsAI — Dependency Inventory

Generato automaticamente: `2026-07-15T23:48:51.524529+00:00`

> Questo documento censisce le dipendenze dichiarate nel repository. I campi relativi a licenza, costi, cloud e Raspberry Pi devono essere verificati prima di essere considerati definitivi.

## Politica del progetto

- Nessuna licenza commerciale obbligatoria.
- Nessun abbonamento obbligatorio.
- Nessun cloud obbligatorio.
- Esecuzione server prevista su Raspberry Pi.
- Client previsto su smartphone Android.
- Preferenza per MIT, BSD, Apache-2.0, MPL-2.0 e altre licenze open source compatibili con il progetto.

## Riepilogo

- Dipendenze dichiarate: `20`
- Python: `6`
- Android/Gradle: `13`
- Node.js/npm: `1`

## Inventario

| Ecosistema | Dipendenza | Versione/vincolo | Ambito | File sorgente | Licenza | Costi | Cloud obbligatorio | Raspberry Pi |
|---|---|---|---|---|---|---|---|---|
| Android/Gradle | `androidx.activity:activity-compose` | `1.10.1` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.foundation:foundation` | `catalogo o versione implicita` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.material3:material3` | `catalogo o versione implicita` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.material:material-icons-extended` | `catalogo o versione implicita` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.ui:ui` | `catalogo o versione implicita` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.ui:ui-test-manifest` | `catalogo o versione implicita` | debugImplementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.ui:ui-tooling` | `catalogo o versione implicita` | debugImplementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.compose.ui:ui-tooling-preview` | `catalogo o versione implicita` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.datastore:datastore-preferences` | `1.2.1` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.lifecycle:lifecycle-runtime-compose` | `2.9.0` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `androidx.lifecycle:lifecycle-viewmodel-compose` | `2.9.0` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `com.hivemq:hivemq-mqtt-client` | `1.3.3` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Android/Gradle | `org.jetbrains.kotlinx:kotlinx-coroutines-android` | `1.10.2` | implementation | `android/app/build.gradle.kts` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Node.js/npm | `node-red` | `^4.0.0` | runtime | `gateway/package.json` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Python | `fastapi` | `>=0.115,<1` | runtime | `core-engine/pyproject.toml` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Python | `httpx` | `>=0.28,<1` | optional:dev | `core-engine/pyproject.toml` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Python | `paho-mqtt` | `>=2.1,<3` | runtime | `core-engine/pyproject.toml` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Python | `pydantic` | `>=2.10,<3` | runtime | `core-engine/pyproject.toml` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Python | `pytest` | `>=8,<9` | optional:dev | `core-engine/pyproject.toml` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |
| Python | `uvicorn` | `>=0.34,<1` | runtime | `core-engine/pyproject.toml` | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE | DA_VERIFICARE |

## Metodo di verifica previsto

Nella fase successiva ogni dipendenza sarà verificata usando, in ordine:

1. metadati ufficiali del pacchetto;
2. repository ufficiale del progetto;
3. file `LICENSE` o documentazione ufficiale;
4. compatibilità architetturale ARM64/ARMv7;
5. eventuali dipendenze da servizi cloud;
6. eventuali componenti premium o funzioni con abbonamento.

Un pacchetto non verrà classificato come compatibile finché la verifica non sarà supportata da una fonte attendibile.
