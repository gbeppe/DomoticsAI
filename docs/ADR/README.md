# DomoticsAI — Architecture Decision Records

Gli ADR documentano le decisioni architetturali durature del progetto.

## Decisioni

| ADR | Titolo | Stato |
|---|---|---|
| [ADR-001](ADR-001-separate-gateway.md) | Gateway separato dal Node-RED di produzione | Accepted |
| [ADR-002](ADR-002-mqtt-primary-protocol.md) | MQTT come protocollo primario | Accepted |
| [ADR-003](ADR-003-ai-safety-boundary.md) | Confine di sicurezza dell’AI | Accepted |
| [ADR-004](ADR-004-versioned-mqtt-namespace.md) | Namespace MQTT versionato | Accepted |
| [ADR-005](ADR-005-no-link-nodes-across-projects.md) | Nessun link node fra progetti | Accepted |
| [ADR-006](ADR-006-command-acknowledgement.md) | Conferma dei comandi | Accepted |
| [ADR-007](ADR-007-automatic-endpoint-selection.md) | Selezione automatica degli endpoint | Accepted |
| [ADR-008](ADR-008-core-engine-python-service.md) | Core Engine come servizio Python | Accepted |
| [ADR-009](ADR-009-persistent-digital-twin.md) | Digital Twin persistente | Accepted |
| [ADR-010](ADR-010-derived-state-in-core-engine.md) | Stato derivato nel Core Engine | Accepted |
| [ADR-011](ADR-011-lights-domain-model.md) | Modello del dominio luci | Accepted |
| [ADR-012](ADR-012-general-command-manager.md) | Command Manager generale | Accepted |
| [ADR-013](ADR-013-command-state-contract.md) | Separazione fra comando e stato | Accepted |
| [ADR-014](ADR-014-json-payloads.md) | JSON per i nuovi payload applicativi | Accepted |
| [ADR-015](ADR-015-android-core-gateway-boundary.md) | Android non accede direttamente al broker reale | Accepted |
| [ADR-016](ADR-016-confirmed-ui-state.md) | La UI rappresenta lo stato confermato | Accepted |
| [ADR-017](ADR-017-core-engine-authority.md) | Core Engine come fonte applicativa autorevole | Accepted |
