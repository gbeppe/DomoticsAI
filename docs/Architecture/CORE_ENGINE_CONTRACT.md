# DomoticsAI Core Engine Contract
Version: 1.0

Status: Approved

---

# 1. Purpose

DomoticsAI is a logical home automation engine.

Its purpose is to represent the house independently from the physical infrastructure and provide a single logical interface for:

- Android Dashboard
- AI Assistant
- Automation Scheduler
- REST APIs
- Future MCP services
- Any future client

The Core Engine SHALL NOT depend on any specific home automation protocol.

---

# 2. Architectural Principles

## Principle 1

Architecture SHALL evolve only to solve:

- architectural errors
- coupling problems
- scalability limitations
- functional limitations

Architecture SHALL NOT evolve only because a solution appears cleaner or more elegant.

---

## Principle 2

Every architectural decision SHALL consider the dual nature of DomoticsAI.

DomoticsAI is simultaneously:

- an operational dashboard
- an intelligent home management system

Both interfaces SHALL use exactly the same logical Core Engine.

No duplicated command pipelines are allowed.

---

# 3. System Vision

The house is represented as a Digital Twin.

The Core Engine manipulates the Digital Twin.

Physical devices are external implementations.

The Core Engine reasons about:

- entities
- state
- capabilities
- commands
- events

The Core Engine never reasons about:

- MQTT topics
- Zigbee
- KNX
- ESPHome
- Shelly
- Modbus
- Matter
- proprietary APIs

---

# 4. Responsibilities

## Dashboard

Responsible for:

- visualization
- manual interaction

Not responsible for:

- automation logic
- routing
- protocol knowledge

---

## AI

Responsible for:

- natural language
- reasoning
- notifications
- recommendations

Not responsible for:

- MQTT
- Gateway
- transport

AI generates logical requests only.

---

## Core Engine

Responsible for:

- business logic
- validation
- Digital Twin
- command lifecycle

Never responsible for:

- protocol translation
- physical devices

---

## Registry

Authoritative description of the house.

Contains:

- entities
- capabilities
- readable/writable flags
- metadata
- bindings

Registry never contains runtime state.

---

## Digital Twin

Authoritative runtime state.

Contains only current state.

Never contains configuration.

---

## Gateway

Infrastructure Adapter.

Responsible for:

- protocol translation
- MQTT adaptation
- physical bindings

Gateway is the only component allowed to know device protocols.

---

## MQTT Service

Transport layer only.

Responsible only for:

- publish
- subscribe

Contains no business logic.

---

# 5. Logical Contracts

## Entity

Every controllable object SHALL have one immutable Entity ID.

Example:

lights.living.power

Entity IDs never change because of hardware replacement.

---

## State

Runtime information only.

Maintained exclusively by the Digital Twin.

---

## Capability

Describes what an entity can do.

Examples:

readable

writable

supports_brightness

supports_color

supports_temperature

---

## Intent

A logical action requested by any client.

Represented by:

CommandRequest

---

## Route

Logical routing information.

Represented by:

CommandRoute

---

## Binding

Translation between logical entities and physical devices.

Owned by the Gateway.

---

# 6. Official Command Pipeline

Dashboard
        │
AI
        │
Automation
        │
REST
        ▼
CommandRequest
        │
        ▼
CommandManager
        │
        ▼
CommandRouter
        │
        ▼
CommandRoute
        │
        ▼
MQTT Service
        │
        ▼
Logical MQTT Topics
(domoticsai/v1/...)
        │
        ▼
Gateway
        │
        ▼
Physical Binding
        │
        ▼
Device

---

# 7. Official State Pipeline

Device
        │
        ▼
Gateway
        │
        ▼
MQTT
        │
        ▼
TopicMapper
        │
        ▼
Registry
        │
        ▼
Digital Twin
        │
        ├────────► Dashboard
        │
        └────────► AI

---

# 8. Ownership Matrix

| Concept | Owner |
|---------|-------|
| Entity IDs | Registry |
| Runtime State | Digital Twin |
| Capabilities | Registry |
| Intent | CommandRequest |
| Validation | CommandManager |
| Routing | CommandRouter |
| Transport | MQTT Service |
| Protocol Translation | Gateway |
| Device Protocols | Gateway |

---

# 9. Evolution Rules

Every new domain SHALL follow exactly the same architecture.

Examples:

Lights

Climate

Energy

Security

Cameras

Audio

Garden

Irrigation

EV Charging

Future AI services

No domain-specific shortcuts are allowed.

---

# 10. Future Vision

Every interaction with the house SHALL eventually become a CommandRequest.

Examples:

Dashboard button

Voice assistant

AI reasoning

Automation

Scheduled action

REST API

Future MCP API

All of them SHALL produce the same logical request.

---

# 11. Stability Policy

This document is normative.

Implementation SHALL adapt to this contract.

The contract SHALL change only when a demonstrable architectural limitation exists.

---

END OF DOCUMENT
