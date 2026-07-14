import asyncio
from contextlib import asynccontextmanager
import logging

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
)

from .config import Settings
from .digital_twin import DigitalTwinStore
from .event_store import EventStore
from .mqtt_service import MqttService
from .websocket_hub import WebSocketHub
from .command_manager import CommandManager
from .command_manager_models import CreateCommandRequest
from .command_store import CommandStore
from .command_models import LightCommandRequest
from .lights_commands import LightsCommandService

logging.basicConfig(level=logging.INFO)

settings = Settings.from_env()
event_store = EventStore(settings.db_path)
twin_store = DigitalTwinStore(event_store)
hub = WebSocketHub()

command_store = CommandStore(settings.db_path)
command_manager = None

def handle_mqtt_message(topic: str, payload: str):
    twin_store.update_from_mqtt(topic, payload)
    if command_manager is not None:
        command_manager.handle_mqtt_message(topic, payload)

mqtt_service = MqttService(
    settings,
    handle_mqtt_message,
)

command_manager = CommandManager(
    command_store,
    mqtt_service,
    simulation_mode=True,
)
lights_command_service = LightsCommandService(
    mqtt_service,
    simulation_mode=True,
)

twin_store.add_listener(hub.publish_from_thread)


@asynccontextmanager
async def lifespan(app):
    hub.bind_loop(asyncio.get_running_loop())
    mqtt_service.start()
    yield
    command_manager.stop()
    mqtt_service.stop()


app = FastAPI(
    title="DomoticsAI Core Engine",
    version="0.4.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    snapshot = twin_store.snapshot()
    entity_count = sum(
        len(domain)
        for domain in snapshot.domains.values()
    )

    return {
        "status": "ok",
        "version": "0.4.0",
        "mqttConnected": mqtt_service.connected,
        "mqttBroker": (
            f"{settings.mqtt_host}:{settings.mqtt_port}"
        ),
        "mqttTopic": settings.mqtt_topic,
        "digitalTwinUpdatedAt": snapshot.updated_at,
        "digitalTwinDomains": len(snapshot.domains),
        "digitalTwinEntities": entity_count,
        "persistentTwin": True,
        "derivedEnergy": (
            "energy_derived" in snapshot.domains
        ),
        "derivedLights": (
            "lights_derived" in snapshot.domains
        ),
    }


@app.get("/api/v1/twin")
def get_twin():
    return twin_store.snapshot()


@app.get("/api/v1/twin/{domain_name}")
def get_domain(domain_name: str):
    domain = twin_store.domain(domain_name)

    if domain is None:
        raise HTTPException(
            404,
            f"Domain not found: {domain_name}",
        )

    return {
        "domain": domain_name,
        "entities": domain,
    }


@app.get("/api/v1/energy")
def get_energy_view():
    return {
        "raw": twin_store.domain("energy") or {},
        "derived": (
            twin_store.domain("energy_derived")
            or {}
        ),
    }


@app.get("/api/v1/lights")
def get_lights_view():
    return {
        "raw": twin_store.domain("lights") or {},
        "derived": (
            twin_store.domain("lights_derived")
            or {}
        ),
    }


@app.post("/api/v1/commands/lights/{area}/{device_id}")
def command_light(
    area: str,
    device_id: str,
    request: LightCommandRequest,
):
    return lights_command_service.submit(
        area=area,
        device_id=device_id,
        request=request,
    )



@app.post("/api/v1/commands")
def create_command(request: CreateCommandRequest):
    return command_manager.create(request)


@app.get("/api/v1/commands")
def list_commands(limit: int = Query(100, ge=1, le=1000)):
    return {"items": command_manager.recent(limit)}


@app.get("/api/v1/commands/{command_id}")
def get_command(command_id: str):
    command = command_manager.get(command_id)
    if command is None:
        raise HTTPException(404, "Command not found")
    return {
        "command": command,
        "events": command_manager.events(command_id),
    }

@app.get("/api/v1/events")
def get_events(
    limit: int = Query(
        100,
        ge=1,
        le=1000,
    )
):
    return {
        "items": event_store.recent(limit),
        "limit": limit,
    }


@app.websocket("/ws/twin")
async def ws_twin(websocket: WebSocket):
    await hub.connect(websocket)

    try:
        await websocket.send_json(
            {
                "type": "twin_snapshot",
                "data": (
                    twin_store
                    .snapshot()
                    .model_dump()
                ),
            }
        )

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await hub.disconnect(websocket)

    except Exception:
        await hub.disconnect(websocket)
