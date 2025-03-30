# config/settings.py

import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

# Environment Variables


class EnvVars(Enum):
    DEBUG = "DEBUG"
    SECRET_KEY = "SECRET_KEY"
    DATABASE_URL = "DATABASE_URL"
    API_KEY = "API_KEY"


# Load environment variables from .env file


def load_env_vars() -> Dict[str, str]:
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            return {
                line.split("=")[0].strip(): line.split("=")[1].strip()
                for line in f.readlines()
            }
    return {}


# Load JSON configuration file


def load_json_config() -> Dict[str, Any]:
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}


# Dataclass for settings


@dataclass
class Settings:
    debug: bool
    secret_key: str
    database_url: str
    api_key: str


# Load settings from environment variables and JSON config


def load_settings() -> Settings:
    env_vars = load_env_vars()
    json_config = load_json_config()

    debug = env_vars.get(EnvVars.DEBUG.value, json_config.get("debug", False))
    secret_key = env_vars.get(
        EnvVars.SECRET_KEY.value, json_config.get("secret_key", "")
    )
    database_url = env_vars.get(
        EnvVars.DATABASE_URL.value, json_config.get("database_url", "")
    )
    api_key = env_vars.get(EnvVars.API_KEY.value, json_config.get("api_key", ""))

    return Settings(debug, secret_key, database_url, api_key)


# Load settings instance
settings = load_settings()

# Expose settings as module-level variables
DEBUG = settings.debug
SECRET_KEY = settings.secret_key
DATABASE_URL = settings.database_url
API_KEY = settings.api_key
