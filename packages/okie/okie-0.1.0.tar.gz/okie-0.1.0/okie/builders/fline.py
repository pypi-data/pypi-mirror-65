from typing import Optional

from .base import OkieRequestPart


class SupervisorBuilder:
    """
    Sets:
        content-type
        content-length
        host

    It's upper to child(sub) builder to set upper separators.
    """

    def __init__(self, method: str, host: bytes, path: bytes, sub_builder: Optional[OkieRequestPart]):
        body = b"%b %b HTTP/1.1\r\nhost: %b\r\n" % (method.encode(), path, host)

        # todo: add custom headers feature

        if sub_builder is not None and sub_builder.body:
            body += (
                b"content-length: %d\r\n" 
                b"content-type: %b\r\n"
                b"\r\n"
                b"%b"
                b"\r\n" % (
                    sub_builder.content_length,
                    sub_builder.content_type.encode(),
                    sub_builder.body,
                )
            )

        self.body = body + b"\r\n"
