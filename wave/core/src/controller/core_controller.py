from wave.models.dataclasses.gesture import Gesture
from wave.models.enums.gesture_types import GestureTypes

from fastapi import FastAPI
from pydantic import BaseModel

api = FastAPI(
    title="Core API",
    description="API for the Core module of the Wave project.",
    version="0.0.1",
)


class RequestModelGesture(BaseModel):
    """A request model representing a gesture."""

    gesture: Gesture


class CoreController:
    """
    Main api endpoint controller for the core module.
    """

    def __init__(self):
        pass

    @api.get("/")
    # pylint: disable=E0211, E0213
    async def root():
        """
        A simple root endpoint that returns a welcome message.
        """
        return {"message": "Welcome to the Image Processor API"}
