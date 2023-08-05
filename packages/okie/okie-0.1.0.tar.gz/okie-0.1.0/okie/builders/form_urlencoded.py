from typing import Dict

from urllib.parse import urlencode

from .base import OkieRequestPart


class FormURLEncodedBuilder(OkieRequestPart[Dict[str, str]]):
    def __init__(self):
        self.body = b""
        self.intermediate = {}

    @property
    def content_type(self) -> str:
        return "application/x-www-form-urlencoded"

    def add_field(
        self, name: str, value: str
    ):
        self.intermediate[name] = value

    def build(self):
        self.body += urlencode(self.intermediate).encode()

    def clean(self):
        super().clean()
        self.intermediate.clear()
