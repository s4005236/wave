from wave.models.dataclasses.gesture import Gesture


class GestureStore:
    """
    Store for gestures received from the core module.
    """

    def __init__(self):
        self.gestures: list[Gesture] = []

    def store_gestures(self, gesture_list: list[Gesture]) -> None:
        """
        Takes a list of gestures and stores them in the store.
        """
        self.gestures = self.gestures + gesture_list
        print(f"Successfully stored {len(self.gestures)} gesture(s).")

    def get_gestures(self) -> list[Gesture] | None:
        """
        Retrieves all stored gestures. If no gestures are stored, returns None.
        """
        if len(self.gestures) > 0:
            return self.gestures
        return None

    def get_gesture_by_id(self, gesture_id: str) -> Gesture | None:
        """
        Retrieves a gesture by its id.
        """
        # TODO: Implement retrieval logic
        print(f"get gesture with id {gesture_id}, not yet implemented.")
        return None

    def clear_gestures(self) -> None:
        """
        Clears all stored gestures.
        """
        self.gestures = []
        print("Successfully cleaned all stored gestures.")


gesture_store = GestureStore()
