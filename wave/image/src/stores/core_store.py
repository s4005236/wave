import logging
from enum import StrEnum, auto

log = logging.getLogger(__name__)


class ConnectionStates(StrEnum):
    CONNECTED = auto()
    DISCONNECTED = auto()


class CoreModel:
    """Model storing information about a core entity."""

    id: int | None
    state: ConnectionStates


class CoreStore:
    """
    Class storing information about the connection to core entities.
    """

    def __init__(self):
        self.core_registry_list = list[CoreModel]()

    def get_core_state_by_id(self, core_id: int) -> ConnectionStates:
        """Get the current connection state of a core entity by id."""
        core = next(
            (x for x in self.core_registry_list if x.id == core_id), None
        )
        return core.state

    def register_core_connected(self, core_id: int):
        """Register a core which connected to the image processor."""
        self.core_registry_list.append(
            CoreModel(id=core_id, state=ConnectionStates.CONNECTED)
        )

    def register_core_disconnected(self, core_id: int):
        """Unregister a core which disconnected from the image processor."""
        for obj in self.core_registry_list:
            if obj.id == core_id:
                self.core_registry_list.remove(obj)
