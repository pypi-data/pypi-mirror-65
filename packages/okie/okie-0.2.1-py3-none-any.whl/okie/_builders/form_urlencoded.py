from typing import Dict

from urllib.parse import urlencode

from .base import OkieRequestPart


class FormURLEncodedBuilder(OkieRequestPart[Dict[str, str]]):
    """
    Builder for '%-encoding' body.

    !!! note
        [Discussion-RFC](https://www.ietf.org/rfc/rfc1867.txt)
    """

    def __init__(self):
        self.intermediate = {}

    @property
    def content_type(self) -> str:
        """
        Get the content type for FormURLEncodedBuilder which is application/x-www-form-urlencoded
        """

        return "application/x-www-form-urlencoded"

    def add_field(
        self, name: str, value: str
    ):
        """
        Add new field, (name, value) pair to existing encoded form

        ##### Parameters
        - name: `str` - *key(name) of the field*
        - value: `str` - *value of field as string*
        """

        self.intermediate[name] = value

    def build(self):
        """
        Generate data and add to an existing encoded form
        """

        self._body = self.body + urlencode(self.intermediate).encode()

    def clean(self):
        """
        "Terminate" the current encoded form, and makes it b""
        """

        super().clean()
        self.intermediate.clear()
