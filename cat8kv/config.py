from dataclasses import dataclass
from dataclasses import field
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DeviceConfig:
    host: str
    username: str
    password: str
    port: int = 443


@dataclass
class GitConfig:
    repo_path: Path
    committer_name: str = "cat8kv-backup"
    committer_email: str = "cat8kv-backup@local"


def load_config() -> DeviceConfig:
    host = os.getenv("DEVICE_HOST")
    username = os.getenv("DEVICE_USERNAME", "developer")
    password = os.getenv("DEVICE_PASSWORD")
    port = int(os.getenv("DEVICE_PORT", "443"))

    if not host:
        raise ValueError("DEVICE_HOST is not set in .env")
    if not password:
        raise ValueError("DEVICE_PASSWORD is not set in .env")

    return DeviceConfig(
        host=host,
        username=username,
        password=password,
        port=port,
    )


def load_git_config() -> GitConfig:
    repo_path = os.getenv("GIT_REPO_PATH", "./git-backups")
    committer_name = os.getenv("GIT_COMMITTER_NAME", "cat8kv-backup")
    committer_email = os.getenv("GIT_COMMITTER_EMAIL", "cat8kv-backup@local")

    return GitConfig(
        repo_path=Path(repo_path),
        committer_name=committer_name,
        committer_email=committer_email,
    )
