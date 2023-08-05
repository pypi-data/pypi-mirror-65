from typing import Optional

from .types import header_key as hk
from .typedefs import Headers


class Response:
    # class-members:
    url: Optional[str]
    body: Optional[bytes]
    headers: Optional[Headers]

    status: Optional[str]
    status_code: Optional[int]
    closed: bool

    _cnt_len = -1

    __slots__ = ("url", "body", "headers", "status", "status_code", "closed")

    def __init__(self):
        for slot in self.__slots__:
            setattr(self, slot, None)

    def __len__(self) -> int:
        if self._cnt_len != -1:
            return self._cnt_len
        return int(self.headers[hk("content-length")])


class HTProtocol:
    """
    Http-Tools-Protocol
    """
    def __init__(self):
        self.response = Response()

    def on_url(self, url: bytes):
        self.response.url = url.decode()

    def on_header(self, name: bytes, value: bytes):
        k, val = hk(name.decode()), value.decode()
        if self.response.headers:
            self.response.headers[k] = val
        else:
            self.response.headers = {k: val}

    def on_body(self, body: bytes):
        self.response.body = body

    def on_message_complete(self):
        self.response.closed = True

    def on_status(self, status: bytes):
        self.response.status = status.decode()

    def put_status_code(self, code: int):
        self.response.status_code = code
