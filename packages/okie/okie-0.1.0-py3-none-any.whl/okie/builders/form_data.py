from typing import List
import uuid

from ..typedefs import Headers

from .base import OkieRequestPart
from .utils import encode_headers


def make_boundary():
    return b"%032x" % uuid.uuid4().int


def make_form_field(
    *,
    name: str,
    value: bytes,
    headers: Headers,
    boundary: bytes,
) -> bytes:
    return (
            b"--%b\r\n"
            b'content-disposition: form-data; name="%b"\r\n'
            b'%b'
            b'\r\n\r\n'
            b"%b"
            b"\r\n" % (
                boundary,
                encode_headers(headers),
                name.encode(),
                value
            )
    )


class FormDataBuilder(OkieRequestPart[List[bytes]]):
    def __init__(self):
        self.boundary = make_boundary()
        self.body = b""
        self.intermediate = []

    @property
    def content_type(self) -> str:
        return "multipart/form-data; boundary={}".format(self.boundary.decode())

    def add_form_data(
        self,
        name: str,
        value: bytes,
        headers: Headers,
    ):
        self.intermediate.append(
            make_form_field(
                name=name,
                value=value,
                headers=headers,
                boundary=self.boundary,
            )
        )

    def build(self):
        self.body = b"".join(
            self.intermediate
        ) + b"--%b--\r\n\r\n" % self.boundary

    def clean(self):
        super().clean()
        self.intermediate.clear()


__all__ = ["FormDataBuilder"]
