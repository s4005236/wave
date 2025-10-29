from wave.enums.bodyparts import Fingers
from wave.enums.gesture_types import GestureTypes

from fastapi import FastAPI
from pydantic import BaseModel

api = FastAPI()


class RequestModelGesture(BaseModel):
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
    # pylint: disable=E0211, E0213
    async def root():
        """
        A simple root endpoint that returns a hello world message.
        """
        return {"message": "Welcome to the Image Processor API"}

    @api.post("/connect")
    # pylint: disable=E0213
    async def connect(gesture_list: list[RequestModelGesture]):
        """
        Connect endpoint. Receives all necessary data from core. Starts the image processing.
        """

        print(gesture_list)

        return {"status": 200, "message": "Connected successfully"}

    @api.post("/disconnect")
    # pylint: disable=E0213
    async def disconnect():
        """
        Disconnect endpoint. Stops the image processing.
        """
        # TODO disconnect logic
        pass
