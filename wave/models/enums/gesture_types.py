from enum import StrEnum, auto


class GestureTypes(StrEnum):
    """
    Enum defining all types of gestures which can be detected.
    """

    STILL = auto()
    TRACK = auto()
