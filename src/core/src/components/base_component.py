"""
The base component is the base for all components with some basic
information
"""

import uuid


class BaseComponent:
    """Represents the base for a component with some basic information."""

    def __init__(self, hostname: str, port: int):
        self._hostname = hostname
        self._port = port
        self._uuid = uuid.uuid4()

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self._port

    @property
    def id(self):
        return self._uuid
