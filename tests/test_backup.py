import json
from pathlib import Path

import pytest

from cat8kv.backup import load, save

CONFIG = {"Cisco-IOS-XE-native:native": {"hostname": "router1"}}
INTERFACES = {"GigabitEthernet": [{"name": "1", "description": "WAN"}]}
HOSTNAME = "router1"


def test_save_creates_all_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    save(HOSTNAME, CONFIG, INTERFACES)
    for name in ("config.json", "interfaces.json", "hostname.json"):
        assert (tmp_path / "backups" / name).exists()


def test_save_and_load_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    save(HOSTNAME, CONFIG, INTERFACES)
    config, interfaces, hostname = load(tmp_path / "backups")
    assert config == CONFIG
    assert interfaces == INTERFACES
    assert hostname == HOSTNAME


def test_load_missing_file_raises(tmp_path: Path) -> None:
    (tmp_path / "config.json").write_text(json.dumps(CONFIG))
    (tmp_path / "interfaces.json").write_text(json.dumps(INTERFACES))
    with pytest.raises(FileNotFoundError, match="hostname.json"):
        load(tmp_path)
