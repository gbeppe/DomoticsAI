#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERRORE: PyYAML non installato. Installa con: python3 -m pip install --user PyYAML", file=sys.stderr)
    raise SystemExit(2)

DEFAULT_REGISTRY = Path("config/registry/digital-twin-registry.yaml")
RESERVED_ROOT_KEYS = {"registry", "brokers"}
ALLOWED_STATUS = {"active", "legacy", "planned", "deprecated", "experimental"}
ALLOWED_SOURCE_TYPES = {
    "physical_sensor", "physical_actuator", "external_system", "calculated",
    "derived", "configuration", "manual_command",
}
ALLOWED_STATE_UPDATE_MODES = {"retained", "subscribe", "poll", "none"}
ALLOWED_SCHEMA_TYPES = {"boolean", "integer", "decimal", "number", "string", "object", "array"}
TOPIC_RE = re.compile(r"^[^\s#+]+(?:/[^\s#+]+)*$")
ENTITY_ID_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+){2,}$")

@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    entity_id: str | None
    path: str
    message: str

class Validator:
    def __init__(self, document: dict[str, Any]) -> None:
        self.document = document
        self.findings: list[Finding] = []
        self.entities: list[tuple[str, dict[str, Any]]] = []
        self.brokers: dict[str, Any] = {}

    def error(self, code: str, path: str, message: str, entity_id: str | None = None) -> None:
        self.findings.append(Finding("ERROR", code, entity_id, path, message))

    def warning(self, code: str, path: str, message: str, entity_id: str | None = None) -> None:
        self.findings.append(Finding("WARNING", code, entity_id, path, message))

    def run(self) -> None:
        self._validate_root()
        self._collect_entities()
        self._validate_entities()
        self._validate_uniqueness()

    def _validate_root(self) -> None:
        registry = self.document.get("registry")
        if not isinstance(registry, dict):
            self.error("REGISTRY_METADATA_MISSING", "registry", "Sezione registry assente o non valida.")
        else:
            for key in ("name", "version", "interface_version"):
                if key not in registry:
                    self.error("REGISTRY_METADATA_FIELD_MISSING", f"registry.{key}", f"Campo obbligatorio mancante: {key}.")

        brokers = self.document.get("brokers")
        if not isinstance(brokers, dict) or not brokers:
            self.error("BROKERS_MISSING", "brokers", "Sezione brokers assente o vuota.")
            return
        self.brokers = brokers
        for name, broker in brokers.items():
            path = f"brokers.{name}"
            if not isinstance(broker, dict):
                self.error("BROKER_INVALID", path, "Definizione broker non valida.")
                continue
            if not isinstance(broker.get("host"), str) or not broker["host"].strip():
                self.error("BROKER_HOST_INVALID", f"{path}.host", "Host broker mancante o non valido.")
            port = broker.get("port")
            if not isinstance(port, int) or not (1 <= port <= 65535):
                self.error("BROKER_PORT_INVALID", f"{path}.port", "Porta broker fuori intervallo 1..65535.")

    def _collect_entities(self) -> None:
        for domain, node in self.document.items():
            if domain in RESERVED_ROOT_KEYS:
                continue
            if not isinstance(node, dict):
                self.error("DOMAIN_INVALID", domain, "Il dominio deve essere una mappa YAML.")
                continue
            self._walk(domain, node)
        if not self.entities:
            self.error("NO_ENTITIES", "", "Nessuna entità trovata nel registry.")

    def _walk(self, path: str, node: Any) -> None:
        if not isinstance(node, dict):
            return
        if "id" in node:
            self.entities.append((path, node))
            return
        for key, child in node.items():
            self._walk(f"{path}.{key}", child)

    def _validate_entities(self) -> None:
        for path, entity in self.entities:
            entity_id = entity.get("id") if isinstance(entity.get("id"), str) else None
            self._validate_identity(path, entity, entity_id)
            self._validate_status(path, entity, entity_id)
            self._validate_capabilities(path, entity, entity_id)
            self._validate_interface(path, entity, entity_id)
            self._validate_mqtt(path, entity, entity_id)
            self._validate_behavior(path, entity, entity_id)
            self._validate_legacy(path, entity, entity_id)
            self._validate_transform(path, entity, entity_id)

    def _validate_identity(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        for field in ("id", "domain", "entity_id", "property"):
            value = entity.get(field)
            if not isinstance(value, str) or not value:
                self.error("IDENTITY_FIELD_MISSING", f"{path}.{field}", f"Campo identità mancante o non valido: {field}.", entity_id)
        if entity_id:
            if not ENTITY_ID_RE.fullmatch(entity_id):
                self.error("ENTITY_ID_FORMAT", f"{path}.id", "L'id deve usare minuscole, numeri, underscore e almeno tre segmenti.", entity_id)
            expected = ".".join(str(entity.get(key, "")) for key in ("domain", "entity_id", "property"))
            if entity_id != expected:
                self.error("ENTITY_ID_INCONSISTENT", f"{path}.id", f"Id non coerente; atteso '{expected}'.", entity_id)
            if path != entity_id:
                self.warning("YAML_PATH_DIFFERS_FROM_ID", path, f"Percorso YAML '{path}' diverso dall'id '{entity_id}'.", entity_id)

    def _validate_status(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        if entity.get("status") not in ALLOWED_STATUS:
            self.error("STATUS_INVALID", f"{path}.status", f"Valore non ammesso: {entity.get('status')!r}.", entity_id)
        if entity.get("source_type") not in ALLOWED_SOURCE_TYPES:
            self.error("SOURCE_TYPE_INVALID", f"{path}.source_type", f"Valore non ammesso: {entity.get('source_type')!r}.", entity_id)
        state_update = entity.get("state_update")
        if not isinstance(state_update, dict):
            self.error("STATE_UPDATE_MISSING", f"{path}.state_update", "Sezione state_update assente.", entity_id)
        elif state_update.get("mode") not in ALLOWED_STATE_UPDATE_MODES:
            self.error("STATE_UPDATE_MODE_INVALID", f"{path}.state_update.mode", f"Modalità non ammessa: {state_update.get('mode')!r}.", entity_id)

    def _validate_capabilities(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        capabilities = entity.get("capabilities")
        if not isinstance(capabilities, dict):
            self.error("CAPABILITIES_MISSING", f"{path}.capabilities", "Sezione capabilities assente.", entity_id)
            return
        for field in ("readable", "writable", "historized"):
            if not isinstance(capabilities.get(field), bool):
                self.error("CAPABILITY_INVALID", f"{path}.capabilities.{field}", f"{field} deve essere boolean.", entity_id)

    def _validate_interface(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        interface = entity.get("interface")
        capabilities = entity.get("capabilities", {})
        if not isinstance(interface, dict):
            self.error("INTERFACE_MISSING", f"{path}.interface", "Sezione interface assente.", entity_id)
            return
        readable = capabilities.get("readable") is True
        writable = capabilities.get("writable") is True
        state_topic = interface.get("state_topic")
        command_topic = interface.get("command_topic")
        ack_topic = interface.get("ack_topic")
        if readable and not state_topic:
            self.error("STATE_TOPIC_REQUIRED", f"{path}.interface.state_topic", "Entità leggibile senza state_topic.", entity_id)
        if not readable and state_topic:
            self.warning("STATE_TOPIC_UNUSED", f"{path}.interface.state_topic", "state_topic presente per entità non leggibile.", entity_id)
        if writable and not command_topic:
            self.error("COMMAND_TOPIC_REQUIRED", f"{path}.interface.command_topic", "Entità scrivibile senza command_topic.", entity_id)
        if not writable and command_topic:
            self.error("COMMAND_TOPIC_FOR_READ_ONLY", f"{path}.interface.command_topic", "command_topic presente per entità non scrivibile.", entity_id)
        for name, topic in (("state_topic", state_topic), ("command_topic", command_topic), ("ack_topic", ack_topic)):
            if topic is not None:
                self._validate_interface_topic(f"{path}.interface.{name}", topic, name, entity_id)
        behavior = entity.get("behavior", {})
        if behavior.get("requires_confirmation") is True and writable and not ack_topic:
            self.error("ACK_TOPIC_REQUIRED", f"{path}.interface.ack_topic", "Conferma richiesta ma ack_topic assente.", entity_id)
        schema = interface.get("schema")
        if not isinstance(schema, dict):
            self.error("SCHEMA_MISSING", f"{path}.interface.schema", "Schema payload assente.", entity_id)
            return
        schema_type = schema.get("type")
        if schema_type not in ALLOWED_SCHEMA_TYPES:
            self.error("SCHEMA_TYPE_INVALID", f"{path}.interface.schema.type", f"Tipo schema non ammesso: {schema_type!r}.", entity_id)
        minimum, maximum = schema.get("minimum"), schema.get("maximum")
        if minimum is not None and maximum is not None:
            if not isinstance(minimum, (int, float)) or not isinstance(maximum, (int, float)):
                self.error("SCHEMA_RANGE_INVALID", f"{path}.interface.schema", "minimum e maximum devono essere numerici.", entity_id)
            elif minimum > maximum:
                self.error("SCHEMA_RANGE_REVERSED", f"{path}.interface.schema", "minimum è maggiore di maximum.", entity_id)
        enum = schema.get("enum")
        if enum is not None and (not isinstance(enum, list) or not enum):
            self.error("SCHEMA_ENUM_INVALID", f"{path}.interface.schema.enum", "enum deve essere una lista non vuota.", entity_id)
        pattern = schema.get("pattern")
        if pattern is not None:
            try:
                re.compile(pattern)
            except (TypeError, re.error) as exc:
                self.error("SCHEMA_PATTERN_INVALID", f"{path}.interface.schema.pattern", f"Pattern non valido: {exc}.", entity_id)

    def _validate_interface_topic(self, path: str, topic: Any, kind: str, entity_id: str | None) -> None:
        if not isinstance(topic, str) or not topic:
            self.error("TOPIC_INVALID", path, "Topic assente o non stringa.", entity_id)
            return
        if not TOPIC_RE.fullmatch(topic):
            self.error("TOPIC_FORMAT_INVALID", path, f"Topic MQTT non valido: {topic!r}.", entity_id)
        if not topic.startswith("zara/interface/"):
            self.error("INTERFACE_NAMESPACE_INVALID", path, "Il topic pubblico deve iniziare con 'zara/interface/'.", entity_id)
        suffix = {"state_topic": "/stat", "command_topic": "/cmd"}.get(kind)
        if suffix and not topic.endswith(suffix):
            self.error("INTERFACE_TOPIC_SUFFIX_INVALID", path, f"{kind} deve terminare con '{suffix}'.", entity_id)

    def _validate_mqtt(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        mqtt = entity.get("mqtt")
        if not isinstance(mqtt, dict):
            self.error("MQTT_MISSING", f"{path}.mqtt", "Sezione mqtt assente.", entity_id)
            return
        if mqtt.get("qos") not in (0, 1, 2):
            self.error("MQTT_QOS_INVALID", f"{path}.mqtt.qos", "QoS deve essere 0, 1 o 2.", entity_id)
        for field in ("retain_state", "retain_command"):
            if not isinstance(mqtt.get(field), bool):
                self.error("MQTT_RETAIN_INVALID", f"{path}.mqtt.{field}", f"{field} deve essere boolean.", entity_id)
        if mqtt.get("retain_command") is True:
            self.error("RETAINED_COMMAND_FORBIDDEN", f"{path}.mqtt.retain_command", "I comandi non devono essere retained.", entity_id)
        if entity.get("capabilities", {}).get("readable") is False and mqtt.get("retain_state") is True:
            self.warning("RETAIN_STATE_ON_COMMAND_ONLY", f"{path}.mqtt.retain_state", "retain_state=true su entità command-only.", entity_id)

    def _validate_behavior(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        behavior = entity.get("behavior")
        if not isinstance(behavior, dict):
            self.error("BEHAVIOR_MISSING", f"{path}.behavior", "Sezione behavior assente.", entity_id)
            return
        for field in ("optimistic_update", "requires_confirmation"):
            if not isinstance(behavior.get(field), bool):
                self.error("BEHAVIOR_FIELD_INVALID", f"{path}.behavior.{field}", f"{field} deve essere boolean.", entity_id)

    def _validate_legacy(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        legacy = entity.get("legacy")
        if entity.get("status") == "legacy" and not isinstance(legacy, dict):
            self.error("LEGACY_MAPPING_REQUIRED", f"{path}.legacy", "Entità legacy senza mapping legacy.", entity_id)
            return
        if legacy is None:
            return
        if not isinstance(legacy, dict):
            self.error("LEGACY_INVALID", f"{path}.legacy", "Sezione legacy non valida.", entity_id)
            return
        for section_name in ("source", "confirmation"):
            section = legacy.get(section_name)
            if section is None:
                continue
            if not isinstance(section, dict):
                self.error("LEGACY_ENDPOINT_INVALID", f"{path}.legacy.{section_name}", "Endpoint legacy non valido.", entity_id)
                continue
            broker = section.get("broker")
            topic = section.get("topic")
            if broker not in self.brokers:
                self.error("UNKNOWN_BROKER", f"{path}.legacy.{section_name}.broker", f"Broker sconosciuto: {broker!r}.", entity_id)
            if not isinstance(topic, str) or not topic:
                self.error("LEGACY_TOPIC_INVALID", f"{path}.legacy.{section_name}.topic", "Topic legacy assente o non valido.", entity_id)
            elif any(ch.isspace() for ch in topic):
                self.error("LEGACY_TOPIC_INVALID", f"{path}.legacy.{section_name}.topic", "Il topic legacy contiene spazi.", entity_id)
        behavior = entity.get("behavior", {})
        capabilities = entity.get("capabilities", {})
        if capabilities.get("writable") is True and behavior.get("requires_confirmation") is True and legacy.get("confirmation") is None:
            self.error("LEGACY_CONFIRMATION_REQUIRED", f"{path}.legacy.confirmation", "Entità scrivibile con conferma richiesta ma senza endpoint legacy di conferma.", entity_id)
        timeout = legacy.get("confirmation_timeout_ms")
        if timeout is not None and (not isinstance(timeout, int) or timeout <= 0):
            self.error("CONFIRMATION_TIMEOUT_INVALID", f"{path}.legacy.confirmation_timeout_ms", "Il timeout deve essere un intero positivo.", entity_id)

    def _validate_transform(self, path: str, entity: dict[str, Any], entity_id: str | None) -> None:
        transform = entity.get("transform")
        if transform is None:
            return
        if not isinstance(transform, dict):
            self.error("TRANSFORM_INVALID", f"{path}.transform", "transform deve essere null oppure una mappa.", entity_id)
            return
        for direction in ("command", "state"):
            mapping = transform.get(direction)
            if mapping is not None and not isinstance(mapping, dict):
                self.error("TRANSFORM_MAPPING_INVALID", f"{path}.transform.{direction}", "La trasformazione deve essere una mappa.", entity_id)

    def _validate_uniqueness(self) -> None:
        ids: dict[str, list[str]] = {}
        topics: dict[str, list[tuple[str, str]]] = {}
        for path, entity in self.entities:
            entity_id = entity.get("id")
            if isinstance(entity_id, str):
                ids.setdefault(entity_id, []).append(path)
            interface = entity.get("interface", {})
            if isinstance(interface, dict):
                for field in ("state_topic", "command_topic"):
                    topic = interface.get(field)
                    if isinstance(topic, str):
                        topics.setdefault(topic, []).append((entity_id or path, field))
        for entity_id, paths in ids.items():
            if len(paths) > 1:
                self.error("DUPLICATE_ENTITY_ID", ", ".join(paths), f"Id duplicato: {entity_id}.", entity_id)
        for topic, usages in topics.items():
            if len(usages) > 1:
                details = ", ".join(f"{eid}:{field}" for eid, field in usages)
                self.error("DUPLICATE_INTERFACE_TOPIC", topic, f"Topic pubblico duplicato: {details}.")

def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERRORE: impossibile leggere {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except yaml.YAMLError as exc:
        print(f"ERRORE YAML in {path}:\n{exc}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(data, dict):
        print("ERRORE: la radice YAML deve essere una mappa.", file=sys.stderr)
        raise SystemExit(1)
    return data

def main() -> int:
    parser = argparse.ArgumentParser(description="Valida il Digital Twin Registry DomoticsAI.")
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()

    document = load_yaml(args.registry)
    validator = Validator(document)
    validator.run()
    errors = [f for f in validator.findings if f.severity == "ERROR"]
    warnings = [f for f in validator.findings if f.severity == "WARNING"]
    metadata = document.get("registry", {})

    print("=" * 72)
    print("DOMOTICSAI DIGITAL TWIN REGISTRY VALIDATOR")
    print("=" * 72)
    print(f"File               : {args.registry}")
    print(f"Registry           : {metadata.get('name', '—')}")
    print(f"Versione           : {metadata.get('version', '—')}")
    print(f"Interface version  : {metadata.get('interface_version', '—')}")
    print(f"Broker             : {len(validator.brokers)}")
    print(f"Entità             : {len(validator.entities)}")
    print(f"Errori             : {len(errors)}")
    print(f"Warning            : {len(warnings)}")

    for finding in validator.findings:
        print()
        entity = f" | {finding.entity_id}" if finding.entity_id else ""
        print(f"[{finding.severity}] {finding.code}{entity}")
        print(f"  Percorso: {finding.path or '<root>'}")
        print(f"  {finding.message}")

    valid = not errors
    print()
    print("REGISTRY VALIDO" if valid else "VALIDAZIONE FALLITA")

    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "valid": valid,
            "registry": str(args.registry),
            "metadata": metadata,
            "brokers": len(validator.brokers),
            "entities": len(validator.entities),
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [asdict(item) for item in validator.findings],
        }
        args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Report JSON        : {args.report_json}")

    return 0 if valid else 1

if __name__ == "__main__":
    raise SystemExit(main())
