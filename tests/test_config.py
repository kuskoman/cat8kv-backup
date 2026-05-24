import pytest

from cat8kv.config import load_config, load_git_config


def test_load_config_raises_without_host(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEVICE_HOST", raising=False)
    monkeypatch.setenv("DEVICE_PASSWORD", "secret")
    with pytest.raises(ValueError, match="DEVICE_HOST"):
        load_config()


def test_load_config_raises_without_password(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEVICE_HOST", "10.0.0.1")
    monkeypatch.delenv("DEVICE_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="DEVICE_PASSWORD"):
        load_config()


def test_load_config_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEVICE_HOST", "10.0.0.1")
    monkeypatch.setenv("DEVICE_PASSWORD", "secret")
    monkeypatch.delenv("DEVICE_USERNAME", raising=False)
    monkeypatch.delenv("DEVICE_PORT", raising=False)
    config = load_config()
    assert config.host == "10.0.0.1"
    assert config.username == "developer"
    assert config.port == 443
