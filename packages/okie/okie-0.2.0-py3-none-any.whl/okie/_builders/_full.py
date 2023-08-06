from typing import Optional

from .base import OkieRequestPart
from ..types import Headers
from .utils import encode_headers


HTTP_USER_AGENT = "okie/0.x"


class HTTPRequestFull:
    """
    Dynamic HttpRequestFull builds a plain http request. Part of non-public API.
    """

    def __init__(
        self,
        method: str,
        host: bytes,
        path: bytes,
        sub_builder: Optional[OkieRequestPart],
        headers: Optional[Headers] = None,
    ):
        self.host = host
        self.method = method
        self.path = path
        self.headers_data = headers
        self.sub_data = sub_builder

    @property
    def begin(self) -> bytes:
        return b"%b %b HTTP/1.1" % (self.method.encode(), self.path)

    @property
    def headers(self) -> bytes:
        headers = Headers((
            ("host", self.host.decode()),
            ("user-agent", HTTP_USER_AGENT),
        ))

        headers = headers.get_merged(self.headers_data)
        out = encode_headers(headers) + b"\r\n"

        sub_builder = self.sub_data
        if sub_builder is not None and sub_builder.body:
            out += encode_headers(
                Headers((
                    ("content-length", str(sub_builder.content_length)),
                    ("content-type", sub_builder.content_type),
                ))
            ) + b"\r\n"

        return out

    @property
    def body(self) -> bytes:
        if self.sub_data is not None and self.sub_data.body:
            return self.sub_data.body
        return b""

    @property
    def full(self):
        return b"\r\n".join((
            self.begin,
            self.headers,
            self.body,
        )) + b"\r\n"
