from typing import Optional
import asyncio

import httptools

from .ctrl import connections
from .builders import OkieRequestPart, SupervisorBuilder
from .typedefs import AsyncioStreamType
from .response import HTProtocol, Response


class Okie(connections.ConnectionController):
    def __init__(self, timeout: float, ssl_handshake_timeout: Optional[float] = None):
        # initialize controllers
        connections.ConnectionController.__init__(
            self, ssl_handshake_timeout=ssl_handshake_timeout
        )

        self.timeout = timeout

    async def _request(
        self,
        method: str,
        url: str,
        data_builder: Optional[OkieRequestPart] = None,
    ) -> Response:
        url: httptools.parser.URL = httptools.parse_url(url.encode())

        async with self.make_connection(
            url.host, url.port, url.schema.startswith(b"https")
        ) as stream:  # type: AsyncioStreamType
            r, w = stream
            plain_request = SupervisorBuilder(
                method, url.host, url.path, data_builder,
            )
            w.write(plain_request.body)

            await w.drain()

            pc = HTProtocol()
            parser = httptools.parser.HttpResponseParser(pc)

            # feed headers
            parser.feed_data(await r.readuntil(b"\r\n\r\n"))
            # feed the rest body
            parser.feed_data(await r.readexactly(len(pc.response)))

            return pc.response

    async def request(
        self,
        method: str,
        url: str,
        timeout: Optional[float] = None,
        data_builder: Optional[OkieRequestPart] = None,
    ) -> Response:
        return await asyncio.wait_for(
            timeout=timeout or self.timeout, fut=self._request(
                method=method, url=url, data_builder=data_builder,
            )
        )
