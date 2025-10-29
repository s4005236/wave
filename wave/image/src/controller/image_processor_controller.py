from wave.enums.bodyparts import Fingers
from wave.enums.gesture_types import GestureTypes

from fastapi import FastAPI

api = FastAPI()


class RequestModelGesture:
    """A request model representing a gesture."""

    id: str
    type: GestureTypes
    components: list[Fingers]
    event: str


class CoreController:
    """
    Main api endpoint controller for the image processor.
    """

    def __init__(self):
        pass

    @api.get("/")
    async def root(self):
        """
        A simple root endpoint that returns a hello world message.
        """
        return {"message": "Welcome to the Image Processor API"}

    @api.post("/connect")
    async def connect(self, gesture_list: list[RequestModelGesture]):
        """
        Connect endpoint. Receives all necessary data from core. Starts the image processing.
        """

        # TODO write list to store

        return {"status": 200, "message": "Connected successfully"}

    @api.post("/disconnect")
    async def disconnect(self, core_entity: str):
        """
        Disconnect endpoint. Stops the image processing.
        """
        # TODO disconnect logic
        pass
