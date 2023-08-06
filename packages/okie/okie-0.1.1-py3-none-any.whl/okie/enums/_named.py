import enum


class NamedEnum(enum.Enum):
    """
    NamedEnum overrides _generate_next_value_ of Enum to name values as they are when auto() is used
    """

    def _generate_next_value_(name, start, count, last_values):
        return name


named = enum.auto
