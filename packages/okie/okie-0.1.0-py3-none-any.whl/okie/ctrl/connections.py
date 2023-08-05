from typing import Optional, Deque, Set, Any
from contextlib import asynccontextmanager
import asyncio
from collections import deque

from ..typedefs import AsyncioStreamType

DEFAULT_SSL_HANDSHAKE_TIMEOUT = 60
DEFAULT_HTTPS_PORT = 443
DEFAULT_HTTP_PORT = 80


async def close_stream(stream: AsyncioStreamType):
    _, w = stream
    w.close()
    await w.wait_closed()


class ConnectionController:
    def __init__(self, ssl_handshake_timeout: Optional[float] = None):
        self._connections_deque: Deque[Optional[AsyncioStreamType]] = deque()
        self._busy_connections: Set[Optional[AsyncioStreamType]] = set()
        self._semaphore = asyncio.Semaphore()
        self._closed = False
        self._ssl_hshk_timeout = ssl_handshake_timeout or DEFAULT_SSL_HANDSHAKE_TIMEOUT

    @asynccontextmanager
    async def make_connection(
        self,
        destination_host: bytes,
        destination_port: Optional[int],
        ssl: Any,
        ssl_handshake_timeout: Optional[float] = None,
    ) -> AsyncioStreamType:
        await self._semaphore.acquire()
        stream = self._connections_deque.popleft() if self._connections_deque else None
        self._busy_connections.add(stream)

        if stream is None:
            if destination_port is None:
                destination_port = DEFAULT_HTTPS_PORT if ssl else DEFAULT_HTTP_PORT

            stream = await asyncio.open_connection(
                host=destination_host.decode(),
                port=destination_port,
                ssl=ssl,
                ssl_handshake_timeout=(
                    ssl_handshake_timeout or self._ssl_hshk_timeout
                ) if ssl else None,
            )

        try:
            yield stream
        finally:
            self._connections_deque.append(stream)
            self._busy_connections.discard(stream)
            self._semaphore.release()

    async def close_all(self):
        if self._closed:
            return

        self._closed = True
        await asyncio.wait(
            (
                close_stream(rw)
                for rw in (
                    *self._connections_deque,
                    *self._busy_connections
                ) if rw
            )
        )

        self._connections_deque = deque([None] * len(self._connections_deque))
        self._busy_connections.clear()
