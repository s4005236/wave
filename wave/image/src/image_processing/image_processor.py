from time import sleep
from wave.image.src.stores.gesture_store import gesture_store
from wave.models.dataclasses.gesture import Gesture


class ImageProcessor:
    """
    The image processor module of this project.
    Handles image processing tasks.
    """

    def __init__(self):
        pass

    def process(self):
        """Main image processing function."""

        run_image_processing = True

        while run_image_processing:
            print("Processing image...")

            gestures: list[Gesture] = gesture_store.get_gestures()

            print(f"Detected {len(gestures)} gesture(s).")

            for gesture in gestures or []:
                print(f"Gesture {gesture.id}:")
                print(f"    Name: {gesture.name}")
                print(f"    Components: {gesture.components}")
                print(f"    Events: {gesture.events}")
                print("----------------")

            # TODO put code for image processing here

            # TODO call Core module api with detected gesture

            sleep(60)
