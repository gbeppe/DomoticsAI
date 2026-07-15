# DomoticsAI — Project Manifest

Generato automaticamente: `2026-07-15T18:02:37.748903+00:00`

> Non modificare manualmente questo file. Rigenerarlo con `python3 scripts/generate-project-manifest.py`.

## Repository

- Branch: `develop`
- Commit: `6b41d53`
- Stato: `M android/app/src/main/java/it/zara/domoticsai/domain/model/CommandHistoryModels.kt
 M android/app/src/main/java/it/zara/domoticsai/ui/commands/CommandsScreen.kt
 M core-engine/src/domoticsai_core/app.py
 M core-engine/src/domoticsai_core/command_store.py
 M core-engine/src/domoticsai_core/digital_twin.py
 M docs/PROJECT_MANIFEST.md
?? core-engine/src/domoticsai_core/command_event_stream.py
?? core-engine/src/domoticsai_core/decisions/decision_service.py
?? core-engine/src/domoticsai_core/knowledge/reasoners/lights_reasoner.py
?? core-engine/src/domoticsai_core/knowledge/reasoners/scene_reasoner.py
?? core-engine/src/domoticsai_core/knowledge/scene_state.py
?? core-engine/src/domoticsai_core/knowledge/scenes_registry.py
?? core-engine/src/domoticsai_core/sqlite_database.py
?? core-engine/tests/test_decision_service.py
?? core-engine/tests/test_knowledge_lights.py
?? core-engine/tests/test_knowledge_scenes.py
?? scripts/install_android_commands_screen_v060.py`

## Architettura generale

```text
Android App
  ↓ REST / MQTT / SSE
Core Engine
  ├── Digital Twin
  ├── Derived domains
  ├── House Knowledge Engine
  ├── House Context Engine
  ├── Command Manager
  └── SQLite persistence
  ↓ MQTT
Gateway Node-RED
  ↓
Dispositivi e Node-RED di produzione
```

## Struttura file

```text
android/BUILDING.md
android/README.md
android/app/build.gradle.kts
android/app/src/main/java/it/zara/domoticsai/AppContainer.kt
android/app/src/main/java/it/zara/domoticsai/DomoticsAiApplication.kt
android/app/src/main/java/it/zara/domoticsai/MainActivity.kt
android/app/src/main/java/it/zara/domoticsai/SimpleViewModelFactory.kt
android/app/src/main/java/it/zara/domoticsai/data/core/CommandJson.kt
android/app/src/main/java/it/zara/domoticsai/data/core/CommandStreamClient.kt
android/app/src/main/java/it/zara/domoticsai/data/core/CoreEngineClient.kt
android/app/src/main/java/it/zara/domoticsai/data/core/CoreEngineRepository.kt
android/app/src/main/java/it/zara/domoticsai/data/core/CoreTwinParser.kt
android/app/src/main/java/it/zara/domoticsai/data/core/EnergyParser.kt
android/app/src/main/java/it/zara/domoticsai/data/core/LightsParser.kt
android/app/src/main/java/it/zara/domoticsai/data/mqtt/DomoticsRepository.kt
android/app/src/main/java/it/zara/domoticsai/data/mqtt/MqttClientService.kt
android/app/src/main/java/it/zara/domoticsai/data/settings/SecureCredentialStore.kt
android/app/src/main/java/it/zara/domoticsai/data/settings/SettingsRepository.kt
android/app/src/main/java/it/zara/domoticsai/domain/model/CommandHistoryModels.kt
android/app/src/main/java/it/zara/domoticsai/domain/model/CoreModels.kt
android/app/src/main/java/it/zara/domoticsai/domain/model/EnergyModels.kt
android/app/src/main/java/it/zara/domoticsai/domain/model/LightsCommandModels.kt
android/app/src/main/java/it/zara/domoticsai/domain/model/LightsModels.kt
android/app/src/main/java/it/zara/domoticsai/domain/model/Models.kt
android/app/src/main/java/it/zara/domoticsai/ui/commands/CommandsScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/commands/CommandsViewModel.kt
android/app/src/main/java/it/zara/domoticsai/ui/components/DashboardCards.kt
android/app/src/main/java/it/zara/domoticsai/ui/diagnostics/DiagnosticsScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/diagnostics/DiagnosticsViewModel.kt
android/app/src/main/java/it/zara/domoticsai/ui/energy/EnergyScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/energy/EnergyViewModel.kt
android/app/src/main/java/it/zara/domoticsai/ui/home/HomeScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/home/HomeViewModel.kt
android/app/src/main/java/it/zara/domoticsai/ui/lights/LightsScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/lights/LightsViewModel.kt
android/app/src/main/java/it/zara/domoticsai/ui/logs/LogsScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/settings/SettingsScreen.kt
android/app/src/main/java/it/zara/domoticsai/ui/theme/Theme.kt
android/build.gradle.kts
android/settings.gradle.kts
core-engine/README.md
core-engine/docs/ADR/ADR-008-core-engine-python-service.md
core-engine/docs/Architecture/CORE_ENGINE_ARCHITECTURE.md
core-engine/pyproject.toml
core-engine/run.py
core-engine/scripts/core-engine.sh
core-engine/src/domoticsai_core/__init__.py
core-engine/src/domoticsai_core/app.py
core-engine/src/domoticsai_core/command_event_stream.py
core-engine/src/domoticsai_core/command_manager.py
core-engine/src/domoticsai_core/command_manager_models.py
core-engine/src/domoticsai_core/command_models.py
core-engine/src/domoticsai_core/command_store.py
core-engine/src/domoticsai_core/config.py
core-engine/src/domoticsai_core/decisions/__init__.py
core-engine/src/domoticsai_core/decisions/decision_engine.py
core-engine/src/domoticsai_core/decisions/decision_service.py
core-engine/src/domoticsai_core/decisions/models.py
core-engine/src/domoticsai_core/decisions/rules/__init__.py
core-engine/src/domoticsai_core/decisions/rules/base.py
core-engine/src/domoticsai_core/decisions/rules/solar_pool.py
core-engine/src/domoticsai_core/digital_twin.py
core-engine/src/domoticsai_core/energy_derived.py
core-engine/src/domoticsai_core/event_store.py
core-engine/src/domoticsai_core/knowledge/__init__.py
core-engine/src/domoticsai_core/knowledge/context.py
core-engine/src/domoticsai_core/knowledge/context_api.py
core-engine/src/domoticsai_core/knowledge/context_engine.py
core-engine/src/domoticsai_core/knowledge/facts.py
core-engine/src/domoticsai_core/knowledge/knowledge_engine.py
core-engine/src/domoticsai_core/knowledge/reasoners/__init__.py
core-engine/src/domoticsai_core/knowledge/reasoners/energy_reasoner.py
core-engine/src/domoticsai_core/knowledge/reasoners/lights_reasoner.py
core-engine/src/domoticsai_core/knowledge/reasoners/pool_reasoner.py
core-engine/src/domoticsai_core/knowledge/reasoners/scene_reasoner.py
core-engine/src/domoticsai_core/knowledge/scene_state.py
core-engine/src/domoticsai_core/knowledge/scenes_registry.py
core-engine/src/domoticsai_core/lights_commands.py
core-engine/src/domoticsai_core/lights_derived.py
core-engine/src/domoticsai_core/models.py
core-engine/src/domoticsai_core/mqtt_service.py
core-engine/src/domoticsai_core/sqlite_database.py
core-engine/src/domoticsai_core/topic_mapper.py
core-engine/src/domoticsai_core/websocket_hub.py
core-engine/tests/test_command_manager.py
core-engine/tests/test_command_store.py
core-engine/tests/test_context_api.py
core-engine/tests/test_decision_service.py
core-engine/tests/test_decision_solar_pool.py
core-engine/tests/test_energy_derived.py
core-engine/tests/test_energy_integration.py
core-engine/tests/test_house_context.py
core-engine/tests/test_knowledge_energy.py
core-engine/tests/test_knowledge_lights.py
core-engine/tests/test_knowledge_pool.py
core-engine/tests/test_knowledge_scenes.py
core-engine/tests/test_lights_commands.py
core-engine/tests/test_lights_derived.py
core-engine/tests/test_lights_integration.py
core-engine/tests/test_persistent_twin.py
core-engine/tests/test_scene_commands.py
core-engine/tests/test_sqlite_database.py
core-engine/tests/test_topic_mapper.py
docs/ADR/ADR-001-separate-gateway.md
docs/ADR/ADR-002-mqtt-primary-protocol.md
docs/ADR/ADR-003-ai-safety-boundary.md
docs/ADR/ADR-004-versioned-mqtt-namespace.md
docs/ADR/ADR-005-no-link-nodes-across-projects.md
docs/ADR/ADR-006-command-acknowledgement.md
docs/ADR/ADR-007-automatic-endpoint-selection.md
docs/ADR/ADR-008-core-engine-python-service.md
docs/ADR/ADR-009-persistent-digital-twin.md
docs/ADR/ADR-010-derived-state-in-core-engine.md
docs/ADR/ADR-011-lights-domain-model.md
docs/ADR/ADR-012-general-command-manager.md
docs/AI/AI_ARCHITECTURE.md
docs/Android/ANDROID_REQUIREMENTS.md
docs/Architecture/AI_CLIMATE_CONFIGURATION_CONTRACT.md
docs/Architecture/AI_CLIMATE_STATE_MACHINE.md
docs/Architecture/ANDROID_APP_BRIDGE_MIGRATION_MATRIX.md
docs/Architecture/ANDROID_DASHBOARD_COMPONENT_MODEL.md
docs/Architecture/ANDROID_GATEWAY_CONTRACT_V0_1.md
docs/Architecture/COMMANDS_ANDROID_SCREEN_V1.md
docs/Architecture/COMMAND_LIFECYCLE_DRAFT.md
docs/Architecture/COMMAND_MANAGER_V1.md
docs/Architecture/CORE_ENGINE_ARCHITECTURE.md
docs/Architecture/DATA_MODEL_DRAFT.md
docs/Architecture/ENERGY_DERIVED_STATE.md
docs/Architecture/ENERGY_POWER_SEMANTICS.md
docs/Architecture/GATEWAY_MODULES_DRAFT.md
docs/Architecture/GATEWAY_MODULE_SPEC.md
docs/Architecture/GATEWAY_MVP_SCOPE.md
docs/Architecture/LIGHTS_COMMAND_PATH_V1.md
docs/Architecture/LIGHTS_CONTRACT_V1.md
docs/Architecture/LIGHTS_DERIVED_STATE.md
docs/Architecture/LOCAL_REMOTE_CONNECTIVITY.md
docs/Architecture/LOGGING_ARCHITECTURE.md
docs/Architecture/MQTT_GATEWAY_NAMESPACE_DRAFT.md
docs/Architecture/PERSISTENT_DIGITAL_TWIN.md
docs/Architecture/SYSTEM_ARCHITECTURE.md
docs/Architecture/SYSTEM_ARCHITECTURE_V1.md
docs/Architecture.md
docs/Backlog/GATEWAY_MVP_BACKLOG.md
docs/CHANGELOG.md
docs/DevelopmentDiary.md
docs/MQTT/MQTT_REVIEW_CHECKLIST.md
docs/MQTT/MQTT_TOPICS.md
docs/NodeRED/AI_CLIMATE_DUPLICATE_FUNCTIONS.md
docs/NodeRED/AI_CLIMATE_REGRESSION_TEST_PLAN.md
docs/NodeRED/AI_CLIMATE_REVERSE_ENGINEERING.md
docs/NodeRED/ANDROID_APP_BRIDGE_COMPATIBILITY_TEST_PLAN.md
docs/NodeRED/ANDROID_APP_BRIDGE_REVERSE_ENGINEERING.md
docs/NodeRED/ANDROID_APP_BRIDGE_ROUTER_INVENTORY.md
docs/NodeRED/DASHBOARD_ANDROID_APP_REVERSE_ENGINEERING.md
docs/NodeRED/FLOW_ANALYSIS.md
docs/NodeRED/PHASE1_INITIAL_FINDINGS.md
docs/NodeRED/VARIABLES.md
docs/PROJECT_MANIFEST.md
docs/Roadmap/ROADMAP_V0_1.md
docs/TinyCam/TINYCAM.md
docs/UI/ANDROID_NAVIGATION_DRAFT.md
docs/UI/DASHBOARD_ANDROID_ACCEPTANCE_CRITERIA.md
docs/UI/DASHBOARD_TO_ANDROID_MIGRATION_MATRIX.md
docs/reverse-engineering/lights/LIGHTS_REVERSE_ENGINEERING.md
docs/reverse-engineering/lights/lights-nodes.json
docs/reverse-engineering/lights/lights-topics.json
gateway/.config.nodes.json
gateway/.config.projects.json
gateway/.config.runtime.json
gateway/.config.users.json
gateway/LIVE_READ_ONLY_TESTING.md
gateway/README.md
gateway/TESTING.md
gateway/context/42e8d1c3858f48ca/flow.json
gateway/context/global/global.json
gateway/flows.json
gateway/flows_cred.json
gateway/package-lock.json
gateway/package.json
gateway/scripts/upgrade_gateway_lights_command_simulator_v010.py
gateway/scripts/upgrade_gateway_scenes_command_simulator_v011.py
gateway/scripts/verify_read_only.py
scripts/README.md
scripts/analyze_lights_flows.py
scripts/dev-stack.sh
scripts/generate-project-manifest.py
scripts/install_android_commands_screen_v060.py
scripts/integrate_command_manager_v010.py
scripts/run-android.sh
scripts/update-gateway-test-broker.py
scripts/update-project-manifest.sh
scripts/upgrade_gateway_energy_v040.py
scripts/upgrade_gateway_lights_v010.py
scripts/verify_lights_gateway.py
```

## Endpoint Core Engine

| Metodo | Endpoint | Funzione |
|---|---|---|
| `GET` | `/api/v1/commands` | `list_commands` |
| `GET` | `/api/v1/commands` | `list_commands` |
| `POST` | `/api/v1/commands` | `create_command` |
| `POST` | `/api/v1/commands` | `create_command` |
| `POST` | `/api/v1/commands/lights/{area}/{device_id}` | `command_light` |
| `GET` | `/api/v1/commands/stream` | `stream_commands` |
| `GET` | `/api/v1/commands/{command_id}` | `get_command` |
| `GET` | `/api/v1/commands/{command_id}` | `get_command` |
| `GET` | `/api/v1/context` | `get_context` |
| `GET` | `/api/v1/context/active` | `get_active_context` |
| `GET` | `/api/v1/decisions` | `get_decisions` |
| `GET` | `/api/v1/energy` | `get_energy_view` |
| `GET` | `/api/v1/events` | `get_events` |
| `GET` | `/api/v1/knowledge` | `get_knowledge` |
| `GET` | `/api/v1/lights` | `get_lights_view` |
| `GET` | `/api/v1/twin` | `get_twin` |
| `GET` | `/api/v1/twin/{domain_name}` | `get_domain` |
| `GET` | `/health` | `health` |

## Moduli Python

### `core-engine/src/domoticsai_core/app.py`

- Funzioni: `handle_mqtt_message`, `lifespan`, `health`, `get_twin`, `get_domain`, `get_decisions`, `get_active_context`, `get_context`, `get_knowledge`, `get_energy_view`, `get_lights_view`, `command_light`, `create_command`, `list_commands`, `stream_commands`, `get_command`, `get_events`, `ws_twin`

### `core-engine/src/domoticsai_core/command_event_stream.py`

- Classi: `CommandEventStream`

### `core-engine/src/domoticsai_core/command_manager.py`

- Classi: `CommandManager`

### `core-engine/src/domoticsai_core/command_manager_models.py`

- Classi: `CommandState`, `CommandSource`, `CreateCommandRequest`, `CommandRecord`, `CommandEvent`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/command_models.py`

- Classi: `CommandStatus`, `LightDesiredState`, `LightCommandRequest`, `CommandEnvelope`, `CommandReceipt`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/command_store.py`

- Classi: `CommandStore`

### `core-engine/src/domoticsai_core/config.py`

- Classi: `Settings`

### `core-engine/src/domoticsai_core/decisions/decision_engine.py`

- Classi: `HouseDecisionEngine`

### `core-engine/src/domoticsai_core/decisions/decision_service.py`

- Classi: `HouseDecisionService`
- Funzioni: `_as_dict`, `knowledge_facts_from_domain`, `active_context_map_from_domain`

### `core-engine/src/domoticsai_core/decisions/models.py`

- Classi: `DecisionKind`, `DecisionStatus`, `HouseDecision`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/decisions/rules/base.py`

- Classi: `DecisionRule`

### `core-engine/src/domoticsai_core/decisions/rules/solar_pool.py`

- Classi: `StartPoolOnSolarSurplusRule`
- Funzioni: `_context_active`

### `core-engine/src/domoticsai_core/digital_twin.py`

- Classi: `DigitalTwinStore`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/energy_derived.py`

- Classi: `EnergyRaw`
- Funzioni: `_number`, `read_energy_raw`, `direction`, `calculate_energy_derived`

### `core-engine/src/domoticsai_core/event_store.py`

- Classi: `EventStore`

### `core-engine/src/domoticsai_core/knowledge/context.py`

- Classi: `HouseContext`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/knowledge/context_api.py`

- Funzioni: `active_contexts_from_domain`

### `core-engine/src/domoticsai_core/knowledge/context_engine.py`

- Classi: `HouseContextEngine`
- Funzioni: `_fact_value`

### `core-engine/src/domoticsai_core/knowledge/facts.py`

- Classi: `KnowledgeFact`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/knowledge/knowledge_engine.py`

- Classi: `HouseKnowledgeEngine`

### `core-engine/src/domoticsai_core/knowledge/reasoners/energy_reasoner.py`

- Classi: `EnergyReasoner`
- Funzioni: `_value`

### `core-engine/src/domoticsai_core/knowledge/reasoners/lights_reasoner.py`

- Classi: `LightsReasoner`
- Funzioni: `_value`, `_boolean`, `_integer`

### `core-engine/src/domoticsai_core/knowledge/reasoners/pool_reasoner.py`

- Classi: `PoolReasoner`
- Funzioni: `_normalized_state`

### `core-engine/src/domoticsai_core/knowledge/reasoners/scene_reasoner.py`

- Classi: `SceneReasoner`

### `core-engine/src/domoticsai_core/knowledge/scene_state.py`

- Classi: `SceneStateSnapshot`, `SceneStateTracker`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/knowledge/scenes_registry.py`

- Funzioni: `is_known_scene`, `scene_metadata`

### `core-engine/src/domoticsai_core/lights_commands.py`

- Classi: `LightsCommandService`

### `core-engine/src/domoticsai_core/lights_derived.py`

- Funzioni: `normalize_state`, `calculate_lights_derived`

### `core-engine/src/domoticsai_core/models.py`

- Classi: `TwinValue`, `DigitalTwin`, `EventRecord`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/mqtt_service.py`

- Classi: `MqttService`
- Funzioni: `utc_now_iso`

### `core-engine/src/domoticsai_core/sqlite_database.py`

- Classi: `SQLiteDatabase`

### `core-engine/src/domoticsai_core/topic_mapper.py`

- Classi: `TopicAddress`
- Funzioni: `map_state_topic`

### `core-engine/src/domoticsai_core/websocket_hub.py`

- Classi: `WebSocketHub`

### `core-engine/tests/test_command_manager.py`

- Classi: `FakePublisher`
- Funzioni: `test_command_lifecycle_to_simulated`, `test_rejects_inactive_target`

### `core-engine/tests/test_command_store.py`

- Funzioni: `test_rows_are_accessible_by_column_name`

### `core-engine/tests/test_context_api.py`

- Funzioni: `wrapped_context`, `test_extracts_and_orders_active_contexts`, `test_ignores_non_context_facts`, `test_ignores_inactive_contexts`

### `core-engine/tests/test_decision_service.py`

- Funzioni: `knowledge_fact`, `house_context`, `test_extracts_facts_without_contexts`, `test_extracts_only_active_contexts`, `test_real_knowledge_generates_decision`, `test_pool_running_suppresses_decision`

### `core-engine/tests/test_decision_solar_pool.py`

- Funzioni: `context`, `test_recommends_pool_filtering_on_surplus`, `test_does_not_recommend_when_pool_running`, `test_does_not_recommend_without_surplus`, `test_decision_id_is_stable`

### `core-engine/tests/test_energy_derived.py`

- Funzioni: `test_solar_charging_and_exporting`, `test_grid_importing`, `test_balance_error_is_zero`

### `core-engine/tests/test_energy_integration.py`

- Funzioni: `test_energy_derived_is_created_and_restored`

### `core-engine/tests/test_house_context.py`

- Funzioni: `fact`, `test_solar_surplus_and_pool_running`, `test_sleep_mode_has_highest_priority`, `test_normal_context_when_nothing_active`, `test_tv_mode_context`

### `core-engine/tests/test_knowledge_energy.py`

- Funzioni: `twin_value`, `facts_by_name`, `test_solar_exporting_full_battery`, `test_grid_supplying_home`, `test_missing_energy_returns_no_facts`

### `core-engine/tests/test_knowledge_lights.py`

- Funzioni: `twin_value`, `facts_by_name`, `test_all_house_lights_off_pool_relays_on`, `test_partial_internal_and_pool_lighting`, `test_missing_lights_returns_no_facts`

### `core-engine/tests/test_knowledge_pool.py`

- Funzioni: `twin_value`, `facts_by_name`, `test_filtering_active_lights_off`, `test_partial_filtering_and_partial_lighting`, `test_filtering_and_lighting`, `test_missing_pool_domain_returns_no_facts`

### `core-engine/tests/test_knowledge_scenes.py`

- Funzioni: `facts_by_name`, `test_requested_scene_is_pending`, `test_confirmed_scene`, `test_non_scene_command_is_ignored`

### `core-engine/tests/test_lights_commands.py`

- Classi: `FakePublisher`
- Funzioni: `test_accepts_active_light_in_simulation`, `test_rejects_obsolete_device`

### `core-engine/tests/test_lights_derived.py`

- Funzioni: `value`, `test_counts_lights_and_relays`, `test_obsolete_devices_are_not_in_registry`, `test_unknown_devices_are_reported_unavailable`

### `core-engine/tests/test_lights_integration.py`

- Funzioni: `test_lights_derived_is_created_and_restored`

### `core-engine/tests/test_persistent_twin.py`

- Funzioni: `test_twin_is_restored_after_restart`, `test_latest_value_replaces_previous_value`

### `core-engine/tests/test_scene_commands.py`

- Classi: `FakePublisher`
- Funzioni: `test_accepts_known_scene`, `test_rejects_unknown_scene`, `test_rejects_wrong_scene_action`

### `core-engine/tests/test_sqlite_database.py`

- Funzioni: `test_persistent_connection_and_health`, `test_serialized_access_from_threads`

### `core-engine/tests/test_topic_mapper.py`

- Funzioni: `test_maps_energy_topic`, `test_ignores_log_topic`

### `gateway/scripts/upgrade_gateway_lights_command_simulator_v010.py`

- Funzioni: `new_id`, `main`

### `gateway/scripts/upgrade_gateway_scenes_command_simulator_v011.py`

- Funzioni: `node_id`, `main`

### `scripts/analyze_lights_flows.py`

- Funzioni: `normalize`, `searchable_text`, `is_relevant`, `connected_ids`, `main`

### `scripts/generate-project-manifest.py`

- Funzioni: `utc_now_iso`, `is_allowed`, `project_files`, `git_output`, `tree_lines`, `python_symbols`, `kotlin_symbols`, `fastapi_routes`, `mqtt_topics`, `dependency_files`, `main`

### `scripts/install_android_commands_screen_v060.py`

- Funzioni: `write_files`, `patch_client`, `patch_main`, `main`

### `scripts/integrate_command_manager_v010.py`

- Funzioni: `main`

### `scripts/upgrade_gateway_energy_v040.py`

- Funzioni: `new_id`, `main`

### `scripts/upgrade_gateway_lights_v010.py`

- Funzioni: `new_id`, `main`

### `tools/extract_nodered_inventory.py`

- Funzioni: `main`

## Moduli Kotlin / Android

### `android/app/src/main/java/it/zara/domoticsai/AppContainer.kt`

- Classes: `AppContainer`

### `android/app/src/main/java/it/zara/domoticsai/DomoticsAiApplication.kt`

- Classes: `DomoticsAiApplication`
- Functions: `onCreate`

### `android/app/src/main/java/it/zara/domoticsai/MainActivity.kt`

- Classes: `Destination`, `MainActivity`
- Functions: `onCreate`

### `android/app/src/main/java/it/zara/domoticsai/SimpleViewModelFactory.kt`

- Classes: `SimpleViewModelFactory`

### `android/app/src/main/java/it/zara/domoticsai/data/core/CommandJson.kt`

- Objects: `CommandJson`
- Functions: `nullableString`, `parseHistoryItem`, `parseState`

### `android/app/src/main/java/it/zara/domoticsai/data/core/CommandStreamClient.kt`

- Classes: `CommandStreamClient`
- Functions: `connect`

### `android/app/src/main/java/it/zara/domoticsai/data/core/CoreEngineClient.kt`

- Classes: `CoreEngineClient`
- Functions: `createLightCommand`, `fetchCommand`, `fetchCommands`, `fetchEnergy`, `fetchHealth`, `fetchLights`, `fetchTwin`, `parseCommandState`, `requestJson`

### `android/app/src/main/java/it/zara/domoticsai/data/core/CoreEngineRepository.kt`

- Classes: `CoreEngineRepository`
- Functions: `refresh`, `refreshEnergy`, `refreshLights`

### `android/app/src/main/java/it/zara/domoticsai/data/core/CoreTwinParser.kt`

- Objects: `CoreTwinParser`
- Functions: `hasAnyValue`, `parse`, `valueOf`

### `android/app/src/main/java/it/zara/domoticsai/data/core/EnergyParser.kt`

- Objects: `EnergyParser`
- Functions: `parse`, `textOf`, `valueOf`

### `android/app/src/main/java/it/zara/domoticsai/data/core/LightsParser.kt`

- Objects: `LightsParser`
- Functions: `boolValue`, `intValue`, `parse`, `parseArea`, `parseState`, `parseType`

### `android/app/src/main/java/it/zara/domoticsai/data/mqtt/DomoticsRepository.kt`

- Classes: `DomoticsRepository`
- Functions: `connect`, `connectEndpoint`, `connectEndpointAwait`, `consumeMessage`, `disconnect`, `parseValue`

### `android/app/src/main/java/it/zara/domoticsai/data/mqtt/MqttClientService.kt`

- Classes: `MqttClientService`
- Functions: `connect`, `disconnect`, `log`

### `android/app/src/main/java/it/zara/domoticsai/data/settings/SecureCredentialStore.kt`

- Classes: `SecureCredentialStore`
- Functions: `getOrCreateKey`, `load`, `save`

### `android/app/src/main/java/it/zara/domoticsai/data/settings/SettingsRepository.kt`

- Classes: `SettingsRepository`
- Objects: `Keys`
- Functions: `save`

### `android/app/src/main/java/it/zara/domoticsai/domain/model/CommandHistoryModels.kt`

- Classes: `CommandHistoryItem`, `CommandsScreenState`

### `android/app/src/main/java/it/zara/domoticsai/domain/model/CoreModels.kt`

- Classes: `CoreDiagnosticsState`, `CoreHealth`, `CoreTwinState`, `HomeDataSource`, `HomeUiState`

### `android/app/src/main/java/it/zara/domoticsai/domain/model/EnergyModels.kt`

- Classes: `EnergyDashboardState`, `EnergyDataSource`, `EnergyDerivedState`

### `android/app/src/main/java/it/zara/domoticsai/domain/model/LightsCommandModels.kt`

- Classes: `CommandReceiptDto`, `DeviceCommandUiState`, `UiCommandState`

### `android/app/src/main/java/it/zara/domoticsai/domain/model/LightsModels.kt`

- Classes: `LightArea`, `LightDevice`, `LightDeviceType`, `LightState`, `LightsDashboardState`, `LightsSummary`

### `android/app/src/main/java/it/zara/domoticsai/domain/model/Models.kt`

- Classes: `AppCredentials`, `BrokerCredentials`, `BrokerEndpoint`, `ClimateState`, `ConnectionMode`, `ConnectionSettings`, `ConnectionState`, `EnergyState`, `HomeState`, `LogEntry`, `VmcState`

### `android/app/src/main/java/it/zara/domoticsai/ui/commands/CommandsScreen.kt`

- Functions: `CommandsScreen`, `stateLabel`

### `android/app/src/main/java/it/zara/domoticsai/ui/commands/CommandsViewModel.kt`

- Classes: `CommandsViewModel`
- Functions: `refresh`, `scheduleEventRefresh`, `startFallbackRefresh`, `startStream`, `userMessage`

### `android/app/src/main/java/it/zara/domoticsai/ui/components/DashboardCards.kt`

- Functions: `BatteryCard`, `DialCard`, `MetricCard`

### `android/app/src/main/java/it/zara/domoticsai/ui/diagnostics/DiagnosticsScreen.kt`

- Functions: `DiagnosticsScreen`

### `android/app/src/main/java/it/zara/domoticsai/ui/diagnostics/DiagnosticsViewModel.kt`

- Classes: `DiagnosticsViewModel`
- Functions: `refresh`

### `android/app/src/main/java/it/zara/domoticsai/ui/energy/EnergyScreen.kt`

- Functions: `BalanceCard`, `BatteryCard`, `EnergyFlowCard`, `EnergyScreen`, `FlowNode`, `OperatingModeCard`, `PercentageCard`, `directionLabel`, `formatPower`

### `android/app/src/main/java/it/zara/domoticsai/ui/energy/EnergyViewModel.kt`

- Classes: `EnergyViewModel`
- Functions: `refresh`

### `android/app/src/main/java/it/zara/domoticsai/ui/home/HomeScreen.kt`

- Functions: `HomeScreen`

### `android/app/src/main/java/it/zara/domoticsai/ui/home/HomeViewModel.kt`

- Classes: `HomeViewModel`
- Functions: `connect`, `disconnect`, `refreshCore`

### `android/app/src/main/java/it/zara/domoticsai/ui/lights/LightsScreen.kt`

- Functions: `CommandStatusCard`, `DeviceCard`, `LightsScreen`, `ScenesReadOnlyCard`, `SummaryCard`, `areaTitle`

### `android/app/src/main/java/it/zara/domoticsai/ui/lights/LightsViewModel.kt`

- Classes: `LightsViewModel`
- Functions: `clearCommand`, `commandKey`, `pollUntilTerminal`, `refresh`, `sendCommand`, `simulateToggle`, `updateCommand`

### `android/app/src/main/java/it/zara/domoticsai/ui/logs/LogsScreen.kt`

- Functions: `LogsScreen`

### `android/app/src/main/java/it/zara/domoticsai/ui/settings/SettingsScreen.kt`

- Functions: `SettingsScreen`

### `android/app/src/main/java/it/zara/domoticsai/ui/theme/Theme.kt`

- Functions: `DomoticsAiTheme`

## Topic MQTT rilevati

- `domoticsai/v1`
- `domoticsai/v1/#`
- `domoticsai/v1/ack/`
- `domoticsai/v1/ack/lights/{area}/{device_id}/`
- `domoticsai/v1/ack/scenes/`
- `domoticsai/v1/ack/scenes/\`
- `domoticsai/v1/availability/gateway`
- `domoticsai/v1/cmd/`
- `domoticsai/v1/cmd/climate/enabled`
- `domoticsai/v1/cmd/lights`
- `domoticsai/v1/cmd/lights/`
- `domoticsai/v1/cmd/lights/+/+`
- `domoticsai/v1/cmd/lights/internal/sala`
- `domoticsai/v1/cmd/scenes/`
- `domoticsai/v1/cmd/scenes/+`
- `domoticsai/v1/log/gateway`
- `domoticsai/v1/meta/lights/registry`
- `domoticsai/v1/meta/lights/registry\`
- `domoticsai/v1/state/`
- `domoticsai/v1/state/climate/ac_power_w`
- `domoticsai/v1/state/climate/bedroom_humidex`
- `domoticsai/v1/state/climate/living_humidex`
- `domoticsai/v1/state/climate/living_temperature_c`
- `domoticsai/v1/state/energy/battery_power_w`
- `domoticsai/v1/state/energy/grid_power_w`
- `domoticsai/v1/state/energy/home_load_w`
- `domoticsai/v1/state/energy/powerwall_soc_pct`
- `domoticsai/v1/state/energy/solar_power_w`
- `domoticsai/v1/state/lights/internal/sala`
- `domoticsai/v1/state/lights/pool/pompaPiscina`
- `domoticsai/v1/state/vmc/speed`
- `domoticsai/v1\`
- `zara/android/domotica`
- `zara/android/domotica/#`
- `zara/android/domotica/ac_auto/set\`
- `zara/android/domotica/eco_lights/set\`
- `zara/android/domotica/holiday/set`
- `zara/android/domotica/holiday/set false`
- `zara/android/domotica/holiday/set true`
- `zara/android/domotica/holiday/set\`
- `zara/android/domotica/light/+/state`
- `zara/android/domotica/light/sala/set\`
- `zara/android/domotica/pool_lights_auto/set\`
- `zara/android/domotica/scene/set`
- `zara/android/domotica/system/set\`
- `zara/android/domotica/vmc/maxNightSpeed/set\`
- `zara/android/domotica/vmc/speed/state\`
- `zara/android/domotica\`
- `zara/android/domotica\\\`
- `zara/domotics/AC/command`
- `zara/domotics/AC/command\`
- `zara/domotics/ACAuto`
- `zara/domotics/ACAuto\`
- `zara/domotics/BedroomHumidex`
- `zara/domotics/BedroomHumidex\`
- `zara/domotics/HP/abilitata`
- `zara/domotics/HP/solardivertmode`
- `zara/domotics/LivingHumidex`
- `zara/domotics/LivingHumidex\`
- `zara/domotics/SmallBathroomThermostatMaxValue`
- `zara/domotics/SmallBathroomThermostatMinValue`
- `zara/domotics/attivaACS`
- `zara/domotics/attivaACS\`
- `zara/domotics/clima_log_eventi`
- `zara/domotics/controlloAutomaticoPotenzaCaminetto`
- `zara/domotics/floorpumpstate`
- `zara/domotics/lights/bedroomlight`
- `zara/domotics/lights/livinglamp`
- `zara/domotics/lights/livinglamp\`
- `zara/domotics/lights/poolfloor`
- `zara/domotics/lights/poolfloor\`
- `zara/domotics/lights/poollight`
- `zara/domotics/lights/poollight\`
- `zara/domotics/lights/poolpump`
- `zara/domotics/lights/poolpump\`
- `zara/domotics/lights/poolskimmer`
- `zara/domotics/lights/poolskimmer\`
- `zara/domotics/lights/prolunga`
- `zara/domotics/lights/readinglight`
- `zara/domotics/lights/readinglight\`
- `zara/domotics/lights/shelflamp`
- `zara/domotics/lights/shelflamp\`
- `zara/domotics/lights/tvlamp`
- `zara/domotics/lights/tvlamp\`
- `zara/domotics/livingThemostatMaxValue`
- `zara/domotics/livingThemostatMinValue`
- `zara/domotics/luciECO`
- `zara/domotics/luciECO\`
- `zara/domotics/luciPiscinaAuto`
- `zara/domotics/luciPiscinaAuto\`
- `zara/domotics/modalitavacanza`
- `zara/domotics/modalitavacanza\`
- `zara/domotics/palazzetti/#`
- `zara/domotics/palazzetti/\`
- `zara/domotics/palazzetti/acceso`
- `zara/domotics/palazzetti/modalita`
- `zara/domotics/palazzetti/oraavvio`
- `zara/domotics/palazzetti/oraspegnimento`
- `zara/domotics/palazzetti/set/modalita\`
- `zara/domotics/pompapavimento/abilitata`
- `zara/domotics/porch_sensor`
- `zara/domotics/porch_sensor\`
- `zara/domotics/time_range`
- `zara/domotics/time_range\`

## File delle dipendenze

- `android/app/build.gradle.kts`
- `android/build.gradle.kts`
- `android/settings.gradle.kts`
- `core-engine/pyproject.toml`
- `gateway/package.json`

## Test

- `core-engine/tests/test_command_manager.py`
- `core-engine/tests/test_command_store.py`
- `core-engine/tests/test_context_api.py`
- `core-engine/tests/test_decision_service.py`
- `core-engine/tests/test_decision_solar_pool.py`
- `core-engine/tests/test_energy_derived.py`
- `core-engine/tests/test_energy_integration.py`
- `core-engine/tests/test_house_context.py`
- `core-engine/tests/test_knowledge_energy.py`
- `core-engine/tests/test_knowledge_lights.py`
- `core-engine/tests/test_knowledge_pool.py`
- `core-engine/tests/test_knowledge_scenes.py`
- `core-engine/tests/test_lights_commands.py`
- `core-engine/tests/test_lights_derived.py`
- `core-engine/tests/test_lights_integration.py`
- `core-engine/tests/test_persistent_twin.py`
- `core-engine/tests/test_scene_commands.py`
- `core-engine/tests/test_sqlite_database.py`
- `core-engine/tests/test_topic_mapper.py`
- `test/README.md`

## Vincoli architetturali

- Funzionamento locale su Raspberry Pi.
- Client Android su smartphone.
- Nessun cloud obbligatorio.
- Nessun abbonamento obbligatorio.
- Nessuna dipendenza con licenza commerciale obbligatoria.
- Preferenza per licenze MIT, BSD e Apache-2.0.
- SQLite locale con WAL e connessione centralizzata.
- Node-RED di produzione invariato fino alla migrazione finale.
