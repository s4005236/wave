from dataclasses import dataclass  # , field

# from uuid import UUID, uuid4


@dataclass
class Event:
    """A base class representing a gesture."""

    id: str
    name: str
    device_id: str
    aspect: str
    modifier: str
    # TODO uuid: UUID = field(default_factory=uuid4)
