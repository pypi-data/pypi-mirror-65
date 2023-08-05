# noimport from src.types


class header_key(str):
    """
    Headers keys are always lower-case in okie
    """

    def __new__(cls, key: str):
        return str.__new__(cls, key).lower()

