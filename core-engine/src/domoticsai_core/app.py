import asyncio
from contextlib import asynccontextmanager
import logging

from fastapi.responses import StreamingResponse

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
from .sqlite_database import SQLiteDatabase
from .command_event_stream import CommandEventStream
from .command_models import LightCommandRequest
from .lights_commands import LightsCommandService

logging.basicConfig(level=logging.INFO)

settings = Settings.from_env()

database = SQLiteDatabase(
    settings.db_path
)

event_store = EventStore(
    database
)

twin_store = DigitalTwinStore(
    event_store
)

hub = WebSocketHub()

command_store = CommandStore(
    database
)
command_event_stream = CommandEventStream()
command_manager = None

def handle_mqtt_message(
    topic: str,
    payload: str,
):
    twin_error = None
    command_error = None

    try:
        twin_store.update_from_mqtt(
            topic,
            payload,
        )
    except Exception as error:
        twin_error = error
        logging.exception(
            "Digital Twin MQTT update failed: "
            "topic=%s",
            topic,
        )

    if command_manager is not None:
        try:
            command_manager.handle_mqtt_message(
                topic,
                payload,
            )
        except Exception as error:
            command_error = error
            logging.exception(
                "Command ACK processing failed: "
                "topic=%s",
                topic,
            )

    if (
        twin_error is not None
        or command_error is not None
    ):
        errors = [
            error
            for error in (
                twin_error,
                command_error,
            )
            if error is not None
        ]

        raise RuntimeError(
            "; ".join(
                f"{type(error).__name__}: {error}"
                for error in errors
            )
        )

mqtt_service = MqttService(
    settings,
    handle_mqtt_message,
)

command_manager = CommandManager(
    command_store,
    mqtt_service,
    simulation_mode=True,
)
command_manager.add_listener(
    command_event_stream.publish_from_thread
)
lights_command_service = LightsCommandService(
    mqtt_service,
    simulation_mode=True,
)

twin_store.add_listener(hub.publish_from_thread)


@asynccontextmanager
async def lifespan(app):
    hub.bind_loop(asyncio.get_running_loop())
    command_event_stream.bind_loop(asyncio.get_running_loop())
    mqtt_service.start()
    yield
    command_manager.stop()
    mqtt_service.stop()
    database.close()


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



@app.get("/api/v1/commands/stream")
async def stream_commands():
    queue = await command_event_stream.subscribe()

    async def generate():
        try:
            yield "event: ready\ndata: {}\n\n"

            while True:
                try:
                    event = await asyncio.wait_for(
                        queue.get(),
                        timeout=20,
                    )

                    yield command_event_stream.encode_sse(
                        event
                    )

                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"

        finally:
            await command_event_stream.unsubscribe(
                queue
            )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )

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
