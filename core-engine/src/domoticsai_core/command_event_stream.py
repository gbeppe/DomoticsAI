from __future__ import annotations

import asyncio
import json
import threading
from typing import Any


class CommandEventStream:
    def __init__(self) -> None:
        self._loop: asyncio.AbstractEventLoop | None = None
        self._lock = threading.RLock()
        self._subscribers: set[asyncio.Queue] = set()

    def bind_loop(
        self,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self._loop = loop

    async def subscribe(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)

        with self._lock:
            self._subscribers.add(queue)

        return queue

    async def unsubscribe(
        self,
        queue: asyncio.Queue,
    ) -> None:
        with self._lock:
            self._subscribers.discard(queue)

    def publish_from_thread(
        self,
        event: dict[str, Any],
    ) -> None:
        loop = self._loop

        if loop is None or loop.is_closed():
            return

        loop.call_soon_threadsafe(
            self._publish_now,
            event,
        )

    def _publish_now(
        self,
        event: dict[str, Any],
    ) -> None:
        with self._lock:
            subscribers = list(self._subscribers)

        for queue in subscribers:
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass

            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass

    @staticmethod
    def encode_sse(
        event: dict[str, Any],
    ) -> str:
        payload = json.dumps(
            event,
            ensure_ascii=False,
        )

        return (
            "event: command\n"
            f"data: {payload}\n\n"
        )
