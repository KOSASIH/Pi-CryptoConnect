# utils/helpers.py
import base64
import hashlib
import json
import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


def get_env_variable(name: str, default: Optional[Any] = None) -> Any:
    value = os.getenv(name)
    if value is None:
        return default
    return value


def load_json_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)


def save_json_file(data: Dict[str, Any], file_path: str):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def generate_random_string(length: int = 32) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(
        characters[
            int(hashlib.sha256(str(time.time()).encode()).hexdigest()[:length], 16)
        ]
        for _ in range(length)
    )


def generate_password_hash(password: str) -> str:
    salt = base64.b64encode(os.urandom(32)).decode()
    return f"{hashlib.sha256(salt.encode() + password.encode()).hexdigest()}.{salt}"


def verify_password_hash(password_hash: str, password: str) -> bool:
    salt, hash_value = password_hash.split(".")
    return hash_value == hashlib.sha256(salt.encode() + password.encode()).hexdigest()


def generate_token(expiration_time: int = 3600) -> str:
    return base64.b64encode(
        f"{datetime.utcnow().isoformat()}.{datetime.utcnow() + timedelta(seconds=expiration_time)}".encode()
    ).decode()


def validate_token(token: str) -> bool:
    try:
        token_data = base64.b64decode(token).decode().split(".")
        token_created = datetime.fromisoformat(token_data[0])
        token_expiration = datetime.fromisoformat(token_data[1])
        if token_expiration < datetime.utcnow():
            return False
        return True
    except Exception:
        return False
