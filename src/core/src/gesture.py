from dataclasses import dataclass, field
from uuid import UUID, uuid4
from src.enums.gesture_types import GestureTypes
from src.enums.bodyparts import Fingers


@dataclass
class Gesture():
    """A base class representing a gesture."""
    id: str
    name: str
    type: GestureTypes
    power: int
    events: list[str]
    components: list[Fingers]
    uuid: UUID = field(default_factory=uuid4)

    def is_still(self):
        """Returns `True` if the gesture is of type STILL; `False` otherwise."""
        return self.type == GestureTypes.STILL
