from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class OkieRequestPart(Generic[T]):
    _body: Optional[bytes] = None
    intermediate: Optional[T] = None

    @property
    def content_type(self) -> str:
        """
        Get the content of the body. Default - anything.
        """

        return "*/*"

    @property
    def content_length(self) -> int:
        """
        Get the length of already built data
        """

        return len(self.body)

    @property
    def body(self) -> bytes:
        """
        Get built(request-specific) data.
        """

        return self._body or b""

    def build(self):
        """
        Build body.
        """
        pass

    def clean(self):
        """
        Clean up "buffers"
        """
        self._body = b""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.build()
