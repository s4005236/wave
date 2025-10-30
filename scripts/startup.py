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
    Core.start(Core)

    print("Starting Core API...")
    core_thread = threading.Thread(target=start_core_api, daemon=True)
    core_thread.start()

    print("Starting Image Processor API...")
    ip_thread = threading.Thread(target=start_image_processor_api, daemon=True)
    ip_thread.start()

    print("Application started successfully.")

    while True:
        pass

    # print("Application exited...")


def start_core_api() -> None:
    """
    Starts the core API.
    """
    # TODO enable
    while True:
        print("Core running...")
        sleep(30)
    # uvicorn.run("wave.core.src.controller.core_controller:api", host="127.0.0.1", port=4711)


def start_image_processor_api() -> None:
    """
    Starts the image processor API.
    """
    uvicorn.run(
        "wave.image.src.controller.image_controller:api",
        host="127.0.0.1",
        port=4712,
    )
