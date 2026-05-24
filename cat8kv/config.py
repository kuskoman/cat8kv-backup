from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class DeviceConfig:
    host: str
    username: str
    password: str
    port: int = 443


def load_config() -> DeviceConfig:
    host = os.getenv("DEVICE_HOST")
    username = os.getenv("DEVICE_USERNAME", "developer")
    password = os.getenv("DEVICE_PASSWORD")
    port = int(os.getenv("DEVICE_PORT", "443"))

    if not host:
        raise ValueError("DEVICE_HOST nie jest ustawiony w .env")
    if not password:
        raise ValueError("DEVICE_PASSWORD nie jest ustawiony w .env")

    return DeviceConfig(
        host=host,
        username=username,
        password=password,
        port=port,
    )
