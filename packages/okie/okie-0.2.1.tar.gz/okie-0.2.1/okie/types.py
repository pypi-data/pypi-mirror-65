from typing import Iterable, Iterator, Tuple, MutableMapping, Optional, Union


class header_key(str):
    """
    Case-insensitive string.

    Stores keys as always lower-case. Implements case-insensitive equality check:

    ```python
    from okie.types import header_key
    header_key("Accept-Encoding") == "accept-encoding" # True
    ```

    !!! note
        Other operators like: >=,<= , >,< are not implemented.
    """

    def __new__(cls, key: str):
        return str.__new__(cls, key).lower()

    def __eq__(self, other: str):
        """
        Check if the given string is equal to header key. Case-insensitive
        """
        return self == header_key(other)

    def __contains__(self, item: str):
        """
        Checks if given string is substring of header key. Case-insensitive
        """
        return header_key(item) in self

    __le__ = __ge__ = __gt__ = __lt__ = lambda *_: NotImplemented


_Key = Union[str, header_key]


class Headers(MutableMapping[header_key, str]):
    """
    Case-insensitive mutable mapping.
    Provides case-insensitive lookup and querying.

    okie.types.Headers example:
    ```python
    from okie.types import Headers
    h = Headers({"Content-Type": "mpa/mpa"})
    h["connection"] = "keep-alive"
    h["ConNecTIOn"] == h["connection"]  # True
    del h["connEctIon"]
    h["connection"]  # raise KeyError: `connection`
    ```

    !!! note
        Headers are case-insensitive due to http headers spec
        [rfc](https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2)
    """

    def __init__(
        self,
        headers: Optional[Union[MutableMapping[_Key, str], Iterable[Tuple[_Key, str]]]] = None
    ):
        self._data: MutableMapping[header_key, str] = {}
        if headers:
            is_map = isinstance(headers, MutableMapping)
            for key, value in headers if not is_map else headers.items():
                self._data[header_key(key)] = value

    def __setitem__(self, key: _Key, value: str):
        """
        `key` will be eventually transformed to `okie.types.header_key` which is case-insensitive
        """

        self._data[header_key(key)] = value

    def __getitem__(self, item: _Key) -> str:
        """
        Case-insensitive lookup for item(key) in headers
        """

        return self._data[header_key(item)]

    def __delitem__(self, key: _Key):
        """
        Case-insensitive removal of key from headers
        """

        del self._data[header_key(key)]

    def __iter__(self) -> Iterator[header_key]:
        """
        Iterates headers returning its keys
        """

        return self._data.__iter__()

    def __len__(self) -> int:
        """
        Returns the count of keys in headers.
        """

        return self._data.__len__()

    def get_merged(self, headers: Optional['Headers']) -> 'Headers':
        """
        Merges two Headers into a new Headers object with respect non-self headers.
        Never mutates original or non-self headers. If non-self headers are empty,
        new headers will be returned, copying self headers.

        - headers `okie.Headers` *non-self headers, second Headers object to merge with self.*
        ##### Returns
        new merged Headers object
        """

        return Headers({**(headers or {}), **self})


__all__ = ["header_key", "Headers"]
