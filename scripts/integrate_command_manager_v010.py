#!/usr/bin/env python3
from pathlib import Path
import sys

APP = Path(
    '/home/giuseppe/AndroidStudioProjects/DomoticsAI/'
    'core-engine/src/domoticsai_core/app.py'
)

def main():
    text = APP.read_text(encoding='utf-8')

    marker = 'from .websocket_hub import WebSocketHub\n'
    imports = (
        'from .command_manager import CommandManager\n'
        'from .command_manager_models import CreateCommandRequest\n'
        'from .command_store import CommandStore\n'
    )
    if imports not in text:
        if marker not in text:
            raise RuntimeError('Import marker non trovato')
        text = text.replace(marker, marker + imports, 1)

    old = '''mqtt_service = MqttService(
    settings,
    twin_store.update_from_mqtt,
)
'''
    new = '''command_store = CommandStore(settings.db_path)
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
'''
    if new not in text:
        if old not in text:
            raise RuntimeError('Blocco mqtt_service non trovato')
        text = text.replace(old, new, 1)

    old_shutdown = '    yield\n    mqtt_service.stop()\n'
    new_shutdown = '    yield\n    command_manager.stop()\n    mqtt_service.stop()\n'
    if new_shutdown not in text:
        if old_shutdown not in text:
            raise RuntimeError('Blocco lifespan non trovato')
        text = text.replace(old_shutdown, new_shutdown, 1)

    endpoint = '''

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
'''
    anchor = '\n@app.get("/api/v1/events")'
    if endpoint.strip() not in text:
        if anchor not in text:
            raise RuntimeError('Anchor events non trovato')
        text = text.replace(anchor, endpoint + anchor, 1)

    APP.write_text(text, encoding='utf-8')
    print('OK: Command Manager integrato in app.py')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'ERRORE: {error}', file=sys.stderr)
        raise
