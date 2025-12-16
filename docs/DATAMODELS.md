# Datamodels

```
Author: Alexander Jahn <s4005236@edu.dhsn.de>
Last updated: 13.11.2025
```

The different modules of the application use different datamodels to fulfill their tasks. In the following, those relations between modules and their data structures are described. The necessary data filling the datamodels is centrally defined in the `config.yaml` file located in the Core module. From there, the data is sent to the other modules.

## Relations: Modules - Datamodel

The following table displays which module needs what type of datamodel.

| Module                | Datamodel             |
|-----------------------|-----------------------|
| Core                  | Events                |
| Image Processor       | Gestures              |
| Device Manager        | Devices               |
| UI                    | Settings              |


- **Gestures** are used by the Image Processor to know, which gestures to detect.
- **Devices** are used by the Device Manager to know, which devices should be available, what aspects and functionality they possess and how those aspects can the modified in a meaningful manner.
- **Events** are used by the Core module as the center piece between _Gestures_ and _Devices_. Events are triggered by detection of a gesture and specify, which aspects of which devices shall be modified in what way.

## Data Model

The following provides a database model kind of overview of the data models defined above.

TODO finish docs

```

Gestures                    Events                  Device
id                          id                      id
list of event_id : int      device : Device         possible properties

```