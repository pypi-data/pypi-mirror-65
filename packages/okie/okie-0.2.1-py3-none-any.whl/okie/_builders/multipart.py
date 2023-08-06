from .utils import encode_headers
from ..types import Headers

from .form_data import FormDataBuilder


def make_binary_field(
    *,
    field_name: str,
    boundary: bytes,
    headers: Headers,
    binary: bytes,
    filename: str,
    content_type: str,
) -> bytes:
    return (
        b"--%b\r\n"
        b"content-disposition:"
        b" form-data;"
        b' name="%b";'
        b' filename="%b"'
        b"\r\n"
        b"content-type: %b"
        b"\r\n"
        b"%b"
        b"\r\n\r\n"
        b"%b"
        b"\r\n" % (
            boundary,
            field_name.encode(),
            (filename or field_name).encode(),
            content_type.encode(),
            encode_headers(headers),
            binary,
        )
    )


class MultipartBuilder(FormDataBuilder):
    """
    Similar to FormDataBuilder differs in specifying `content-type` and `filename`
    attributes to okie-generated `content-disposition` header.

    !!! todo "implement multipart subtypes"
    """

    def add_binary_data(
        self,
        field_name: str,
        headers: Headers,
        binary: bytes,
        filename: str,
        content_type: str,
    ):
        """
        Add partial binary field to intermediate.

        ##### Parameters
        - field_name: `str` - *field name*
        - headers: `okie.types.Headers` - *headers for field*
        - binary: `str` - *file's binary*
        - filename: `str` - *name of posting file*
        - content_type: `str` - *file mime-type*

        """
        self.intermediate.append(
            make_binary_field(
                field_name=field_name,
                boundary=self.boundary,
                headers=headers,
                binary=binary,
                filename=filename,
                content_type=content_type,
            )
        )


__all__ = ["MultipartBuilder"]
