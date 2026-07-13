import asyncio
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from .config import Settings
from .digital_twin import DigitalTwinStore
from .event_store import EventStore
from .mqtt_service import MqttService
from .websocket_hub import WebSocketHub

logging.basicConfig(level=logging.INFO)

settings = Settings.from_env()
event_store = EventStore(settings.db_path)
twin_store = DigitalTwinStore(event_store)
hub = WebSocketHub()
mqtt_service = MqttService(settings, twin_store.update_from_mqtt)
twin_store.add_listener(hub.publish_from_thread)

@asynccontextmanager
async def lifespan(app):
    hub.bind_loop(asyncio.get_running_loop())
    mqtt_service.start()
    yield
    mqtt_service.stop()

app = FastAPI(
    title="DomoticsAI Core Engine",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "mqttConnected": mqtt_service.connected,
        "mqttBroker": f"{settings.mqtt_host}:{settings.mqtt_port}",
        "mqttTopic": settings.mqtt_topic,
        "digitalTwinUpdatedAt": twin_store.snapshot().updated_at,
    }

@app.get("/api/v1/twin")
def get_twin():
    return twin_store.snapshot()

@app.get("/api/v1/twin/{domain_name}")
def get_domain(domain_name: str):
    domain = twin_store.domain(domain_name)
    if domain is None:
        raise HTTPException(404, f"Domain not found: {domain_name}")
    return {"domain": domain_name, "entities": domain}

@app.get("/api/v1/events")
def get_events(limit: int = Query(100, ge=1, le=1000)):
    return {"items": event_store.recent(limit), "limit": limit}

@app.websocket("/ws/twin")
async def ws_twin(websocket: WebSocket):
    await hub.connect(websocket)
    try:
        await websocket.send_json({
            "type": "twin_snapshot",
            "data": twin_store.snapshot().model_dump(),
        })
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await hub.disconnect(websocket)
    except Exception:
        await hub.disconnect(websocket)
