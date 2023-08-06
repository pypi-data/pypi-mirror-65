from typing import List
import uuid

from ..types import Headers

from .base import OkieRequestPart
from .utils import encode_headers


def make_boundary() -> bytes:
    """
    Generate new uuid4 and get its `hex`

    ##### Returns
    boundary in bytes

    """
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
            b'\r\n'
            b"%b"
            b"\r\n" % (
                boundary,
                encode_headers(headers) + b"\r\n",
                name.encode(),
                value
            )
    )


class FormDataBuilder(OkieRequestPart[List[bytes]]):
    """
    FormDataBuilder is superclass for multipart builder, but `okie.MultipartBuilder`
    has `add_binary_data` which is designed for bigger file-binaries.
    """

    def __init__(self):
        self.boundary = make_boundary()
        self.intermediate = []

    @property
    def content_type(self) -> str:
        """
        Get the content of the body.
        """
        return "multipart/form-data; boundary={}".format(self.boundary.decode())

    def add_form_data(
        self,
        name: str,
        value: bytes,
        headers: Headers,
    ):
        """
        ##### Parameters
        - name: `str` - *field name*
        - value: `bytes` - *binary*
        - headers: `okie.types.Headers` - *headers for the part for form-data*

        !!! note "Headers"
            `content-disposition` header is added by the library.

        """
        self.intermediate.append(
            make_form_field(
                name=name,
                value=value,
                headers=headers,
                boundary=self.boundary,
            )
        )

    def build(self):
        self._body = b"".join(
            self.intermediate
        ) + b"--%b--\r\n\r\n" % self.boundary

    def clean(self):
        super().clean()
        self.intermediate.clear()


__all__ = ["FormDataBuilder"]
