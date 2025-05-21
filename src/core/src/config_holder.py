"""
The ConfigHolder class is for easier handling and sharing of the config.
"""

import logging
import os
from uuid import UUID
import yaml
from core.src.gesture import Gesture
from enums.gesture_types import GestureTypes
from enums.bodyparts import Fingers
from .components.image_processor import ImageProcessor
from .components.device_manager import DeviceManager

log = logging.getLogger(__name__)


class ConfigHolder:
    """
    This class holds the config and has some functions for easier
    getting and setting.
    """

    def __init__(self, file: str | None = None):
        if file is None:
            self._filename = os.path.join(
                os.path.dirname(__file__), "config.yml"
            )
        else:
            self._filename = file
        self.gestures: dict[UUID, Gesture] = {}
        self._gesture_ids: list = []
        self._image_processors: dict[UUID, ImageProcessor] = {}
        self._device_managers: dict[UUID, DeviceManager] = {}
        self._api_bind_address: str = ""
        self._api_port: int = None

        self._load_config()

    def _load_config(self) -> None:
        """Loads the config"""
        with open(self._filename, encoding="utf-8") as config_file:
            raw_config: dict = yaml.safe_load(config_file)

            self._load_gestures(raw_config)
            self._load_ips(raw_config)
            self._load_dms(raw_config)
            self._load_api_specs(raw_config)

    def _load_gestures(self, raw_config: dict) -> None:
        """Loads the gestures from the given config"""
        for gesture in raw_config["gestures"]:
            gesture_id: str = gesture["id"].lower()
            if gesture_id in self._gesture_ids:
                log.warning("%s already existing; ignoring", gesture_id)
                continue
            self._gesture_ids.append(gesture_id)
            gesture = Gesture(
                gesture_id,
                gesture["name"],
                type=GestureTypes(gesture["type"].lower()),
                power=int(gesture["power"]),
                events=gesture["events"],
                components=[
                    Fingers(finger.lower()) for finger in gesture["components"]
                ],
            )
            self.gestures[gesture.uuid] = gesture

    def _load_ips(self, raw_config: dict):
        """Loads the Image Processors from the given config"""
        for ip in raw_config["image_processors"]:
            processor = ImageProcessor(
                hostname=ip["hostname"], port=int(ip["port"])
            )
            self._image_processors[processor.id] = processor

    def _load_dms(self, raw_config: dict):
        """Loads the Device Managers from the given config"""
        for dm in raw_config["device_managers"]:
            manager = DeviceManager(
                hostname=dm["hostname"], port=int(dm["port"])
            )
            self._device_managers[manager.id] = manager

    def _load_api_specs(self, raw_config: dict):
        """Loads the API specs from config"""
        self._api_bind_address = raw_config["api"]["bind_address"]
        self._api_port = int(raw_config["api"]["port"])

    @property
    def gestures(self) -> list[Gesture]:
        return self.gestures

    @gestures.setter
    def gestures(self, value) -> None:
        self.gestures = value

    @property
    def image_processors(self) -> list[ImageProcessor]:
        return self._image_processors

    @image_processors.setter
    def image_processors(self, value):
        self._image_processors = value

    @property
    def device_managers(self) -> list[ImageProcessor]:
        return self._device_managers

    @device_managers.setter
    def device_managers(self, value):
        self._device_managers = value

    @property
    def api_bind_address(self):
        return self._api_bind_address

    @api_bind_address.setter
    def api_bind_address(self, value):
        self._api_bind_address = value

    @property
    def api_port(self):
        return self._api_port

    @api_port.setter
    def api_port(self, value):
        self._api_port = int(value)
