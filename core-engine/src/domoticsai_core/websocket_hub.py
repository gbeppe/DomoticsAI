import asyncio

class WebSocketHub:
    def __init__(self):
        self._clients = set()
        self._lock = asyncio.Lock()
        self._loop = None

    def bind_loop(self, loop):
        self._loop = loop

    async def connect(self, websocket):
        await websocket.accept()
        async with self._lock:
            self._clients.add(websocket)

    async def disconnect(self, websocket):
        async with self._lock:
            self._clients.discard(websocket)

    def publish_from_thread(self, message):
        if self._loop is not None:
            asyncio.run_coroutine_threadsafe(self.broadcast(message), self._loop)

    async def broadcast(self, message):
        async with self._lock:
            clients = list(self._clients)
        dead = []
        for client in clients:
            try:
                await client.send_json(message)
            except Exception:
                dead.append(client)
        if dead:
            async with self._lock:
                for client in dead:
                    self._clients.discard(client)
