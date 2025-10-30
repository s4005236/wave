import threading
from time import sleep
from wave.core.src.core import Core
from wave.image.src.controller.image_controller import ImageController

import uvicorn


def start() -> None:
    """
    Entry point for the application.
    Usually called through a poetry script command.
    """
    print("Starting Core...")

    print("Starting Core API...")
    core_thread = threading.Thread(target=start_core_api, daemon=True)
    core_thread.start()

    print("Starting Image Processor API...")
    ip_thread = threading.Thread(target=start_image_processor_api, daemon=True)
    ip_thread.start()

    print("Startup complete. Main thread entering main function on Core.")

    Core.main(Core)

    print("Application exited cleanly.")


def start_core_api() -> None:
    """
    Starts the core API.
    """
    uvicorn.run(
        "wave.core.src.controller.core_controller:api",
        host="127.0.0.1",
        port=4710,
    )


def start_image_processor_api() -> None:
    """
    Starts the image processor API.
    """
    uvicorn.run(
        "wave.image.src.controller.image_controller:api",
        host="127.0.0.1",
        port=4711,
    )
