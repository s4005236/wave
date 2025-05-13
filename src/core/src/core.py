import yaml
import logging
from src.core.src.gesture import Gesture
from src.enums.gesture_types import GestureTypes
from src.enums.bodyparts import Fingers

log = logging.getLogger(__name__)


class Core:
    """
    The core module of this project.
    Handles the config and communication between the other modules.
    """

    def __init__(self, config_file: str = "config.yml"):
        self.gestures: list[Gesture] = []
        self._gesture_ids: list = []

        self.reload_config(file=config_file)

    def reload_config(self, file: str = "config.yml") -> None:
        """Reloads the config using the given config file"""
        with open(file) as config_file:
            raw_config: dict = yaml.safe_load(config_file)

        for gesture in raw_config["gestures"]:
            gesture_id: str = gesture["id"].lower()
            if gesture_id in self._gesture_ids:
                log.warning(f"{gesture_id} already existing; ignoring")
                continue
            else:
                self._gesture_ids.append(gesture_id)
                self.gestures.append(Gesture(
                    gesture_id, gesture["name"],
                    type=GestureTypes(gesture["type"].lower()),
                    power=int(gesture["power"]),
                    events=gesture["events"],
                    components=[Fingers(finger.lower())
                                for finger in gesture["components"]]
                )
                )

    def start(self) -> None:
        # This currently is only a stub to mark what is to come
        # TODO This function should make a connection to the IP and DM and send the relevant data
        # It also starts a run loop
        pass


if __name__ == "__main__":
    core = Core()
    print(core.gestures)
