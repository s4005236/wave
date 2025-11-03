from wave.models.dataclasses.gesture import Gesture
from wave.models.enums.gesture_types import GestureTypes

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

api = FastAPI(
    title="Core API",
    description="API for the Core module of the Wave project.",
    version="0.0.1",
)


class RequestModelGesture(BaseModel):
    """A request model wrapping a gesture. Used for Rest API calls."""

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

    @api.post("/connect")
    # pylint: disable=E0213
    async def connect(request_model_gesture: RequestModelGesture):
        """
        Connect endpoint. Receives a gesture from the Image Processor module. Sends the events of the received gesture to the Device Manager.
        """

        if not isinstance(request_model_gesture, RequestModelGesture):
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error: Provided gesture is not an instance of RequestModelGesture.",
            )

        # pylint: disable=E1101, check that request_model contains member 'gesture'
        if request_model_gesture.gesture is None:
            raise HTTPException(
                status_code=400,
                detail="Bad Request: No valid gesture provided.",
            )
        detected_gesture: Gesture = request_model_gesture.gesture

        if detected_gesture is None:
            raise HTTPException(
                status_code=400,
                detail="Bad Request: Provided gesture is None.",
            )

        print(
            f"Core: Trigger events {detected_gesture.events} for gesture {detected_gesture.name}"
        )

        # TODO send to DM

        return {
            "status": 200,
            "message": "Successfully connected. All Gestures stored correctly.",
        }
