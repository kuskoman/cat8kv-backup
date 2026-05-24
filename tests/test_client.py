from unittest.mock import MagicMock, patch

import pytest

from cat8kv.client import ENDPOINTS, RestconfClient
from cat8kv.config import DeviceConfig


@pytest.fixture
def client() -> RestconfClient:
    config = DeviceConfig(host="10.0.0.1", username="admin", password="secret", port=443)
    with patch("cat8kv.client.requests.Session"):
        return RestconfClient(config)


def test_url_construction(client: RestconfClient) -> None:
    assert client._url("native") == f"https://10.0.0.1:443{ENDPOINTS['native']}"
    assert client._url("hostname") == f"https://10.0.0.1:443{ENDPOINTS['hostname']}"


def test_get_hostname_parses_response(client: RestconfClient) -> None:
    client.session.get.return_value = MagicMock(
        json=lambda: {"Cisco-IOS-XE-native:hostname": "myrouter"},
        raise_for_status=lambda: None,
    )
    assert client.get_hostname() == "myrouter"


def test_restore_config_calls_put(client: RestconfClient) -> None:
    payload = {"Cisco-IOS-XE-native:native": {"hostname": "r1"}}
    client.session.put.return_value = MagicMock(raise_for_status=lambda: None)
    client.restore_config(payload)
    client.session.put.assert_called_once()
    _, kwargs = client.session.put.call_args
    assert kwargs["json"] == payload
