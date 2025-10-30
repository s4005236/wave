from wave.core.src.core import Core


def start():
    """
    Entry point for the application.
    Usually called through a poetry script command.
    """
    print("Starting WAVE...")
    Core.start(Core)
