"""
The core module of WAVE. It handles the IPs and DMs. It exposes an API
for the components and handles the communication between them.
"""

from functools import lru_cache
from fastapi import FastAPI
import uvicorn
from core.src.config_holder import ConfigHolder

api = FastAPI()


@lru_cache
def get_config():
    return ConfigHolder()


if __name__ == "__main__":
    uvicorn.run(api)
