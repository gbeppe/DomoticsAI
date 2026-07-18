# DomoticsAI Registry Documentation

- **Status:** Active
- **Owner:** Architecture / Registry
- **Authoritative executable artifact:** `config/registry/digital-twin-registry.yaml`
- **Related ADR:** `docs/ADR/ADR-018-digital-twin-registry-source-of-truth.md`

## Purpose

This directory documents the concepts, structure and evolution rules of the
DomoticsAI Digital Twin Registry.

The YAML file under `config/registry/` is the authoritative inventory and binding
declaration. Files in this directory explain its semantics and governance; they
must not maintain a competing copy of entity or topic data.

## Reading order

1. `REGISTRY_MODEL.md`
2. `REGISTRY_REFERENCE.md`
3. `REGISTRY_EVOLUTION.md`
4. `config/registry/README.md`
5. `config/registry/digital-twin-registry.yaml`
