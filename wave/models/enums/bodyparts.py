from enum import StrEnum, auto


class Fingers(StrEnum):
    """
    Enum defining all bodyparts which can be used to identify a gesture.
    """

    LTHUMB = auto()
    LINDEX = auto()
    LMIDDLE = auto()
    LRING = auto()
    LLITTLE = auto()
    RTHUMB = auto()
    RINDEX = auto()
    RMIDDLE = auto()
    RRING = auto()
    RLITTLE = auto()
