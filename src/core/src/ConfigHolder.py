"""
The ConfigHolder class is for easier handling and sharing of the config.
"""

import logging
import yaml
from src.core.src.gesture import Gesture
from src.enums.gesture_types import GestureTypes
from src.enums.bodyparts import Fingers
from .components.ImageProcessor import ImageProcessor
from .components.DeviceManager import DeviceManager

log = logging.getLogger(__name__)


class ConfigHolder:
    """
    This class holds the config and has some functions for easier
    getting and setting.
    """

    def __init__(self, file: str = "config.ini"):
        self._filename = file
        self.gestures: list[Gesture] = []
        self._gesture_ids: list = []
        self._image_processors: list[ImageProcessor] = []
        self._device_managers: list[DeviceManager] = []

        self._load_config()

    def _load_config(self) -> None:
        """Loads the config"""
        with open(self._filename, encoding="utf-8") as config_file:
            raw_config: dict = yaml.safe_load(config_file)

        for gesture in raw_config["gestures"]:
            gesture_id: str = gesture["id"].lower()
            if gesture_id in self._gesture_ids:
                log.warning("%s already existing; ignoring", gesture_id)
                continue
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

    @property
    def gestures(self) -> list[Gesture]:
        return self.gestures

    @gestures.setter
    def gestures(self, value) -> None:
        # pylint: disable=unused-argument
        log.warning("A module tried to overwrite the gestures! Not doing it.")

    @property
    def image_processors(self) -> list[ImageProcessor]:
        return self._image_processors

    @image_processors.setter
    def image_processors(self, value):
        # pylint: disable=unused-argument
        log.warning("A module tried to overwrite the IPs! Not doing it.")

    @property
    def device_managers(self) -> list[ImageProcessor]:
        return self._device_managers

    @device_managers.setter
    def device_managers(self, value):
        # pylint: disable=unused-argument
        log.warning("A module tried to overwrite the DMs! Not doing it.")
