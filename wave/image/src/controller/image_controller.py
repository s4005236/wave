import asyncio
import logging
import threading
from collections.abc import AsyncIterable, Iterable
from wave.image.src.image_processing.image_processor import ImageProcessor
from wave.image.src.stores.core_store import core_store
from wave.image.src.stores.gesture_store import gesture_store
from wave.models.dataclasses.gesture import Gesture

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

log = logging.getLogger(__name__)

api = FastAPI(
    title="Image Processor API",
    description="API for the Image Processor module of the Wave project.",
    version="0.0.1",
)


class RequestModelGesture(BaseModel):
    """A request model wrapping a gesture. Used for Rest API calls."""

    gesture: Gesture


class ImageController:
    """
    Main api endpoint controller for the image processor module.
    """

    def __init__(self):
        pass

    @api.get("/")
    # pylint: disable=E0213
    async def root():
        """
        A simple root endpoint that returns a welcome message.
        """
        return {"message": "Welcome to the Image Processor API"}

    @api.post("/connect")
    # pylint: disable=E0213
    async def connect(request_model_gesture_list: list[RequestModelGesture]):
        """
        Connect endpoint. Receives all necessary data from core. Starts the image processing.
        """

        if not isinstance(request_model_gesture_list, Iterable):
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error: Provided list of gestures is not an instance of iterable.",
            )

        gesture_list: list[Gesture] = [
            request_gesture.gesture
            # pylint: disable=E1133, check above that list isinstance Iterable
            for request_gesture in request_model_gesture_list
        ]

        try:
            gesture_store.store_gestures(gesture_list)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal Server Error: {str(e)}"
            ) from e

        print("Starting Image Processor API...")
        thread = threading.Thread(target=ImageProcessor().process, daemon=True)
        thread.start()

        core_store.register_core_connected()

        return {
            "status": 200,
            "message": "Successfully connected. All Gestures stored correctly.",
        }

    @api.post("/disconnect")
    # pylint: disable=E0213
    async def disconnect():
        """
        Disconnect endpoint. Stops the image processing.
        """
        # TODO disconnect logic
        pass
