import threading
from wave.constants.api_config import API_HOST_URL, CORE_API_PORT, IP_API_PORT
from wave.core.src.core import core

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

    core.main()

    print("Application exited.")


def start_core_api() -> None:
    """
    Starts the core API.
    """
    uvicorn.run(
        "wave.core.src.controller.core_controller:api",
        host=API_HOST_URL,
        port=CORE_API_PORT,
    )


def start_image_processor_api() -> None:
    """
    Starts the image processor API.
    """
    uvicorn.run(
        "wave.image.src.controller.image_controller:api",
        host=API_HOST_URL,
        port=IP_API_PORT,
    )
