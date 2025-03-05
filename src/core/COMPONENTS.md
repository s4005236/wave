# Components
Below is a small documentation / braindump of the components of the core.

## API
- Fastapi
- For communication with other external components (IP, UI, ...)

## Database Controller
A database controller to have a unified interface for a range of database backends.

## Gesture Handler
A handler that receives gestures from the API and processes them according to the config and defined events. It sends the events to the Device Manager.