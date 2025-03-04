# Terminology
Below is an overview of the terms used in this project.

## Architecture
The architecture of the project. It describes which service sends data to another. The teams or tasks for this project are split into seperated by these components. See the components below.  
![Architecture Diagram](media/architecture.svg "Architecture")

## Image Processor
The image processor (IP) is responsible for processing the raw image data of a camera. It should detect the gestures sent to it on connection by the core. See the [gestures section](GESTURES.md) for more information on this process. It will then send the detected gestures back to the core.  
It is one of the core modules.

## Core / CPU
The core (or central processing unit / CPU) is responsible of parsing the config, user values (trough UI), and receiving and sending the gestures to and from the IP. It is responsible for future features like "Do not disturb" or authentication. It also technically enables to have more than one IP, altough that's currently out of the scope of the project.  
It is one of the core modules.

## Device Manager
The device manager is responsible for the communication between the device modules and the core. It will send the available devices to and receive instructions from the core.  
It is one of the core modules.

## Device Modules
Device modules are modular controllers for devices. They need to publish their devices to the device manager and can register events, therefore receiving the event when it occurs. In the end they are responsible for controlling the devices. A little example:  
You can have a module which controls two lights without dimming. It registers for the events `light_on` and `light_off`. It will then receive this event if it is triggered and meant for its devices. In parallel there can be a module for your heater, which registers the events `heater_on`, `heater_off`, `temperature_down`, `temperature_up`.  
This goes on for any device you can and want to control using the system.  
Device modules are useful for keeping the device-specifics out of the control logic and give users the possibility to add their own devices, as this project can never implement all devices existent. It also prevents the changing of core modules for new devices.

## Core modules
Core modules are the CPU, IP and Device Manager. They do the core logic of the project. They will only be changed after a good amount of review. They are meant to be able to run on different devices. 