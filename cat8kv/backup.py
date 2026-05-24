import json
from pathlib import Path

BACKUPS_DIR = Path("backups")


def save(hostname: str, config: dict, interfaces: dict) -> Path:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    (BACKUPS_DIR / "hostname.json").write_text(json.dumps({"hostname": hostname}, indent=2))
    (BACKUPS_DIR / "interfaces.json").write_text(json.dumps(interfaces, indent=2))
    (BACKUPS_DIR / "config.json").write_text(json.dumps(config, indent=2))

    return BACKUPS_DIR


def load(directory: Path) -> tuple[dict, dict, str]:
    for name in ("config.json", "interfaces.json", "hostname.json"):
        if not (directory / name).exists():
            raise FileNotFoundError(f"{name} not found in: {directory}")

    config = json.loads((directory / "config.json").read_text())
    interfaces = json.loads((directory / "interfaces.json").read_text())
    hostname = json.loads((directory / "hostname.json").read_text())["hostname"]

    return config, interfaces, hostname
