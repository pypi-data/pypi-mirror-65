from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class OkieRequestPart(Generic[T]):
    body: bytes = b""
    intermediate: Optional[T] = None

    @property
    def content_type(self) -> str:
        return "*/*"

    @property
    def content_length(self) -> int:
        return len(self.body)

    def build(self):
        pass

    def clean(self):
        self.body = b""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.build()
