import json
from pathlib import Path

BACKUPS_DIR = Path("backups")


def save(hostname: str, config: dict, interfaces: dict) -> Path:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    (BACKUPS_DIR / "hostname.json").write_text(json.dumps({"hostname": hostname}, indent=2))
    (BACKUPS_DIR / "interfaces.json").write_text(json.dumps(interfaces, indent=2))
    (BACKUPS_DIR / "config.json").write_text(json.dumps(config, indent=2))

    return BACKUPS_DIR


def load(directory: Path) -> dict:
    config_file = directory / "config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"config.json not found in: {directory}")
    return json.loads(config_file.read_text())
