<div align="center">
    <img src="./docs/_media/wave_project_avatar.png" width="20%">
    <h1>WAVE</h1>
    <p align="center">
    <strong>Wireless Automation via Engagement</strong>
    </p>
</div>

# About the project

WAVE enables you to control your home without touching any buttons or screens. Use a personalized system of gestures to manage all your smart devices at the wink of your hand.

## Features
The features are split into two categories: Originally planned and finished.  
Due to mistakes in the planning of deadlines, features are highly incomplete. The core functionality of detecting gestures is available, therefore reaching the requirement of the task.  
The documentation is written as if the features would work. Please open an issue or contact the authors if you've got any questions.

### Was planned

- Core module to configure the gestures and other settings
- Device Manager to control arbitrary smart home devices
- A web UI for settings and a log of detected gestures
- Possibly accounts with different, auto-detected persons

### Finished

- Image processor
    - Detecting hand gestures
    - Running on RPI or better hardware
    - Fast and reliable detection
- Data models, definitions and communication protocols
- DevOps features
    - Automatic Docker image builds
    - Code quality checks
    - PR reviews and pipelines
    - Commit checks

## User Guide

For more information on how to use WAVE, please refer to our [User Guide](/docs/User/_USER_GUIDE.md).

# Development and Contributing

## Development Setup & Start
At the project root:

__Step 1:__ Create a virtual environment  `.venv`.

__Step 2:__ Then run:
```
python setup_dev.py
```

__All done setting up!__

__Step 3:__ Start the application by running:
```
poetry run wave
```

Wave is a lightweight gesture-recognition platform for controlling smart home devices. It is designed to run on Raspberry Pi units so devices can be placed easily in rooms, operate wirelessly, and are not tied to a single location. Gesture inputs are translated into control commands for lights, outlets, media, and other home automation endpoints.

## User Guide

For more information on how to use WAVE, please refer to our [User Guide](/docs/User/_USER_GUIDE.md).

## Documentation Ressources
For further technical documentation, please consult the following documents:

- Module Documentation
    - Core Documentation: [open](/docs/Core/_CORE.md)
    - Device Documentation: [open](/docs/Device/_DEVICE.md)
    - Image Processor Documentation: [open](/docs/ImageProcessor/_IMAGE_PROCESSOR.md)
    - WebApp Documentation [open](/docs/WebApp/_WEB_APP.md)

- DevOps Documentation: [open](/docs/DevOps/_DEV_OPS.md)