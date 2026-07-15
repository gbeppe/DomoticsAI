from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .config import ROOT


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def _repository_section(
    data: dict[str, Any],
) -> list[str]:
    git = data["git"]

    clean_label = (
        "sì"
        if git["clean"]
        else "no"
    )

    return [
        "## Repository",
        "",
        f"- Branch: `{git['branch']}`",
        f"- Commit: `{git['commit']}`",
        f"- Working tree pulita: "
        f"`{clean_label}`",
        f"- File modificati: "
        f"`{git['modified']}`",
        f"- File aggiunti: "
        f"`{git['added']}`",
        f"- File eliminati: "
        f"`{git['deleted']}`",
        f"- File rinominati: "
        f"`{git['renamed']}`",
        f"- File non tracciati: "
        f"`{git['untracked']}`",
        "",
    ]


def _overview_section() -> list[str]:
    return [
        "## Visione del progetto",
        "",
        "DomoticsAI è un assistente domestico "
        "locale e self-hosted. Normalizza i dati "
        "della casa, costruisce un Digital Twin, "
        "interpreta lo stato osservato e produce "
        "contesti e suggerimenti consultivi per "
        "l’app Android.",
        "",
        "Il sistema deve continuare a funzionare "
        "senza servizi cloud obbligatori, licenze "
        "commerciali o abbonamenti.",
        "",
    ]


def _principles_section() -> list[str]:
    return [
        "## Principi e vincoli",
        "",
        "- **Local-first:** server su Raspberry Pi "
        "e client su smartphone Android.",
        "- **Offline-capable:** le funzioni "
        "domotiche principali non dipendono da "
        "Internet.",
        "- **Open stack:** nessuna licenza a "
        "pagamento o abbonamento obbligatorio.",
        "- **Self-hosted:** dati, log, storico e "
        "configurazioni restano nella rete locale.",
        "- **Safety boundary:** il Decision Engine "
        "produce suggerimenti, ma non esegue "
        "automaticamente comandi.",
        "- **Explainability:** facts, contesti e "
        "decisioni includono motivazioni.",
        "- **Production isolation:** il Node-RED "
        "attuale resta invariato fino alla "
        "migrazione finale.",
        "",
    ]


def _architecture_section() -> list[str]:
    return [
        "## Architettura generale",
        "",
        "```mermaid",
        "flowchart TD",
        "    DEV[Dispositivi e impianti]",
        "    PROD[Node-RED produzione]",
        "    MQTT[Broker MQTT]",
        "    GW[Gateway Node-RED]",
        "    MAP[Topic Mapper]",
        "    TWIN[Digital Twin persistente]",
        "    DERIVED[Derived Domains]",
        "    KNOW[House Knowledge Engine]",
        "    CONTEXT[House Context Engine]",
        "    DECISION[Decision Engine]",
        "    HOME[Unified Home Snapshot]",
        "    API[REST / SSE / WebSocket API]",
        "    ANDROID[App Android]",
        "",
        "    DEV --> PROD",
        "    PROD --> MQTT",
        "    MQTT --> GW",
        "    GW --> MQTT",
        "    MQTT --> MAP",
        "    MAP --> TWIN",
        "    TWIN --> DERIVED",
        "    DERIVED --> KNOW",
        "    KNOW --> CONTEXT",
        "    CONTEXT --> DECISION",
        "    DECISION --> HOME",
        "    HOME --> API",
        "    API --> ANDROID",
        "    MQTT --> ANDROID",
        "```",
        "",
    ]


def _knowledge_pipeline_section() -> list[str]:
    return [
        "## Pipeline cognitiva",
        "",
        "| Livello | Input | Output | Responsabilità |",
        "|---|---|---|---|",
        "| Digital Twin | MQTT normalizzato | Entità osservate | Rappresentare lo stato reale |",
        "| Derived Domains | Entità osservate | Valori calcolati | Normalizzare e aggregare |",
        "| Knowledge Engine | Twin e derived | Knowledge Facts | Interpretare il significato |",
        "| Context Engine | Facts | House Contexts | Sintetizzare il contesto globale |",
        "| Decision Engine | Facts e contesti | Decisioni consultive | Produrre avvisi e raccomandazioni |",
        "| Home Snapshot | Contesti e decisioni | Snapshot coerente | Alimentare la Home Android |",
        "",
    ]


def _runtime_section() -> list[str]:
    return [
        "## Componenti runtime",
        "",
        "| Componente | Runtime previsto | Ruolo |",
        "|---|---|---|",
        "| Node-RED produzione | Raspberry Pi | Logica e integrazione impianti esistenti |",
        "| Mosquitto | Raspberry Pi | Trasporto MQTT locale |",
        "| Gateway Node-RED | Raspberry Pi | Normalizzazione e bridge MQTT |",
        "| Core Engine | Raspberry Pi | Twin, conoscenza, decisioni e API |",
        "| SQLite | Raspberry Pi | Persistenza locale |",
        "| App DomoticsAI | Smartphone Android | Interfaccia e controllo utente |",
        "",
    ]


def _core_components_section() -> list[str]:
    return [
        "## Core Engine",
        "",
        "### Digital Twin",
        "",
        "Memorizza lo stato osservato dei domini "
        "della casa e lo rende persistente.",
        "",
        "### Derived Domains",
        "",
        "Calcolano stati energetici e aggregazioni "
        "delle luci senza introdurre interpretazioni "
        "probabilistiche.",
        "",
        "### House Knowledge Engine",
        "",
        "Produce facts deterministici e spiegabili "
        "tramite reasoner indipendenti per energia, "
        "luci, piscina e scenari.",
        "",
        "### House Context Engine",
        "",
        "Combina i facts in contesti globali quali "
        "`SOLAR_SURPLUS`, `POOL_RUNNING` e "
        "`SLEEP_MODE_ACTIVE`.",
        "",
        "### Decision Engine",
        "",
        "Produce avvisi e raccomandazioni. "
        "L’esecuzione automatica resta disabilitata.",
        "",
        "### Command Manager",
        "",
        "Gestisce validazione, pubblicazione MQTT, "
        "ACK, timeout, persistenza e storico dei "
        "comandi.",
        "",
        "### Unified Home Snapshot",
        "",
        "L’endpoint `/api/v1/home` restituisce "
        "contesti e decisioni costruiti dallo stesso "
        "snapshot del dominio `knowledge`.",
        "",
    ]


def _android_section() -> list[str]:
    return [
        "## Applicazione Android",
        "",
        "La Home Android presenta tre livelli:",
        "",
        "1. stato di connessione e freschezza;",
        "2. contesti attivi della casa;",
        "3. suggerimenti prodotti dal Decision Engine.",
        "",
        "Il client utilizza uno snapshot unificato "
        "tramite `HomeIntelligenceViewModel`, "
        "mantenendo MQTT come fallback per i dati "
        "operativi.",
        "",
    ]


def _api_section(
    data: dict[str, Any],
) -> list[str]:
    lines = [
        "## API Core Engine",
        "",
        "| Metodo | Endpoint | Handler |",
        "|---|---|---|",
    ]

    for route in data["routes"]:
        lines.append(
            f"| `{route['method']}` "
            f"| `{route['path']}` "
            f"| `{route['function']}` |"
        )

    lines.extend(
        [
            "",
            "L’inventario tecnico completo è "
            "disponibile in "
            "[`PROJECT_INDEX.md`](PROJECT_INDEX.md).",
            "",
        ]
    )

    return lines


def _quality_section(
    data: dict[str, Any],
) -> list[str]:
    return [
        "## Qualità e test",
        "",
        f"- Test rilevati: "
        f"`{len(data['test_files'])}` file.",
        f"- Endpoint FastAPI rilevati: "
        f"`{len(data['routes'])}`.",
        f"- Topic MQTT rilevati nel codice e nella "
        f"documentazione: "
        f"`{len(data['topics'])}`.",
        f"- File sorgente e documentali indicizzati: "
        f"`{len(data['files'])}`.",
        "",
    ]


def _documents_section() -> list[str]:
    return [
        "## Documenti di riferimento",
        "",
        "- [`Architecture/SYSTEM_ARCHITECTURE.md`](Architecture/SYSTEM_ARCHITECTURE.md)",
        "- [`Architecture/CORE_ENGINE_ARCHITECTURE.md`](Architecture/CORE_ENGINE_ARCHITECTURE.md)",
        "- [`Architecture/COMMAND_MANAGER_V1.md`](Architecture/COMMAND_MANAGER_V1.md)",
        "- [`Architecture/PERSISTENT_DIGITAL_TWIN.md`](Architecture/PERSISTENT_DIGITAL_TWIN.md)",
        "- [`AI/AI_ARCHITECTURE.md`](AI/AI_ARCHITECTURE.md)",
        "- [`MQTT/MQTT_TOPICS.md`](MQTT/MQTT_TOPICS.md)",
        "- [`Android/ANDROID_REQUIREMENTS.md`](Android/ANDROID_REQUIREMENTS.md)",
        "- [`Roadmap/ROADMAP_V0_1.md`](Roadmap/ROADMAP_V0_1.md)",
        "",
    ]


def render_manifest(
    data: dict[str, Any],
) -> str:
    lines = [
        "# DomoticsAI — Project Manifest v2",
        "",
        f"Generato automaticamente: "
        f"`{utc_now_iso()}`",
        "",
        "> Il Manifest descrive l’architettura e i "
        "principi del progetto. L’inventario completo "
        "è in `PROJECT_INDEX.md`.",
        "",
    ]

    sections = (
        _overview_section(),
        _repository_section(data),
        _principles_section(),
        _architecture_section(),
        _knowledge_pipeline_section(),
        _runtime_section(),
        _core_components_section(),
        _android_section(),
        _api_section(data),
        _quality_section(data),
        _documents_section(),
    )

    for section in sections:
        lines.extend(section)

    lines.extend(
        [
            "## Generazione",
            "",
            "```bash",
            "./scripts/update-project-manifest.sh",
            "```",
            "",
            "I documenti generati sono:",
            "",
            "- `docs/PROJECT_MANIFEST.md`",
            "- `docs/PROJECT_INDEX.md`",
            "",
        ]
    )

    return "\n".join(lines)
