from typing import Optional, Union

import httptools

from .ctrl import asyncio
from ._builders import OkieRequestPart, HTTPRequestFull
from .types import Headers
from .response import HTProtocol, Response
from .enums.http_request import HttpRequestType


class Okie(asyncio.AsyncioConnectionController):
    def __init__(
        self,
        timeout: float,
        ssl_handshake_timeout: Optional[float] = None,
        headers: Optional[Headers] = None,
    ):
        # initialize controllers
        asyncio.AsyncioConnectionController.__init__(
            self, ssl_handshake_timeout=ssl_handshake_timeout
        )

        self.timeout = timeout
        self.default_headers = headers or Headers()

    async def _request(
        self,
        method: Union[str, HttpRequestType],
        url: str,
        data_builder: Optional[OkieRequestPart] = None,
        headers: Optional[Headers] = None,
    ) -> Response:
        url: httptools.parser.URL = httptools.parse_url(url.encode())

        async with self.make_connection(
            url.host,
            url.port,
            url.schema.startswith(b"https") if url.schema else False
        ) as stream:  # type: asyncio.AsyncioStreamType
            r, w = stream
            method = HttpRequestType(method)
            plain_request = HTTPRequestFull(
                method=str(method.value),
                host=url.host,
                path=url.path,
                sub_builder=data_builder,
                headers=self.default_headers.get_merged(headers),
            )
            w.write(plain_request.full)

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
        method: Union[str, HttpRequestType],
        url: str,
        timeout: Optional[float] = None,
        data_builder: Optional[OkieRequestPart] = None,
        headers: Optional[Headers] = None,
    ) -> Response:
        """
        Makes HTTP request within given timeout if succeeds on time returns Response object
        otherwise raises `asyncio.TimeoutError`

        ##### Parameters
        - method `(str, okie.HTTPRequestType)` *HTTP request type*
        - url `str` *resource identifier, if doesn't have schema, will assume non-ssl request*
        - timeout `float` *optional timeout within request should be sent/read. (Task gets cancelled on error)*
        - data_builder `okie._builders.OkieRequestPart` *partial builder object to fill `okie.builders.HTTPFullRequest`*
        - headers `okie.Headers` *headers object, gets merged with self.default_headers into new Headers before request*

        ##### Returns
        - `okie.response.Response`
        """

        return await asyncio.call_with_timeout(
            timeout=timeout or self.timeout, future=self._request(
                method=method, url=url, data_builder=data_builder,
                headers=headers,
            )
        )
