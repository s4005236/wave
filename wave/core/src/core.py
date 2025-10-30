import json
import logging
from time import sleep
from wave.constants.api_config import IP_API_BASE_URL
from wave.models.dataclasses.gesture import Gesture
from wave.models.enums.bodyparts import Fingers
from wave.models.enums.gesture_types import GestureTypes

import requests
import yaml
from pydantic import BaseModel
from requests import Response

log = logging.getLogger(__name__)


class RequestModelGesture(BaseModel):
    """A request model representing a gesture."""

    gesture: Gesture


class Core:
    """
    The core module of this project.
    Handles the config and communication between the other modules.
    """

    def __init__(self, config_file: str = "config.yml"):
        self.gestures: list[Gesture] = []
        self._gesture_ids: list = []

        print("Loading config...")
        self.reload_config(file=config_file)

    def reload_config(self, file: str = "config.yml") -> None:
        """Reloads the config using the given config file"""
        with open(file, encoding="utf-8") as config_file:
            raw_config: dict = yaml.safe_load(config_file)

        for gesture in raw_config["gestures"]:
            gesture_id: str = gesture["id"].lower()
            if gesture_id in self._gesture_ids:
                log.warning("%s already existing; ignoring", gesture_id)
                continue
            else:
                self._gesture_ids.append(gesture_id)
                self.gestures.append(
                    Gesture(
                        gesture_id,
                        gesture["name"],
                        type=GestureTypes(gesture["type"].lower()),
                        power=int(gesture["power"]),
                        events=gesture["events"],
                        components=[
                            Fingers(finger.lower())
                            for finger in gesture["components"]
                        ],
                    )
                )

    def main(self) -> None:
        """
        Makes a connection to the IP and DM and sends the relevant data.
        It also starts the run loop.
        """

        response: Response = requests.get(f"{IP_API_BASE_URL}", timeout=30)

        if response.status_code != 200:
            raise ConnectionError(
                f"Could not connect to Image Processor API. Status code: {response.status_code}"
            )

        request_model_gesture_list: list[RequestModelGesture] = [
            RequestModelGesture(gesture=gesture) for gesture in self.gestures
        ]
        data_dict: dict[RequestModelGesture] = [
            request_model_gesture.model_dump()
            for request_model_gesture in request_model_gesture_list
        ]

        response = requests.post(
            f"{IP_API_BASE_URL}/connect", json=data_dict, timeout=10
        )

        print(f"Response: {response.json().get('message', '')}")

        while True:
            pass


core = Core()
