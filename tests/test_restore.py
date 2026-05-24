import copy
from unittest.mock import MagicMock, call, patch

import pytest

from cat8kv.client import RestconfClient
from cat8kv.config import DeviceConfig

ORIGINAL_CONFIG = {
    "Cisco-IOS-XE-native:native": {
        "hostname": "cat8000v",
        "interface": {
            "GigabitEthernet": [
                {"name": "1", "description": "WAN"},
                {"name": "2", "description": "LAN"},
            ]
        },
    }
}

TEST_HOSTNAME = "cat8000v-test-backup"
TEST_DESCRIPTION_SUFFIX = "-CHANGED"


@pytest.fixture
def config() -> DeviceConfig:
    return DeviceConfig(
        host="10.10.20.48",
        username="developer",
        password="C1sco12345",
    )


@pytest.fixture
def client(config: DeviceConfig) -> RestconfClient:
    with patch("cat8kv.client.requests.Session"):
        return RestconfClient(config)


def test_restore_flow(client: RestconfClient) -> None:
    changed_config = copy.deepcopy(ORIGINAL_CONFIG)
    changed_config["Cisco-IOS-XE-native:native"]["hostname"] = TEST_HOSTNAME
    for iface in changed_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]:
        iface["description"] = iface["description"] + TEST_DESCRIPTION_SUFFIX

    client.get_config = MagicMock(side_effect=[
        copy.deepcopy(ORIGINAL_CONFIG),  # Step 1: backup
        copy.deepcopy(changed_config),   # Step 3: verify change
        copy.deepcopy(ORIGINAL_CONFIG),  # Step 5: verify restore
    ])
    client.restore_config = MagicMock()

    original_config = client.get_config()
    assert original_config["Cisco-IOS-XE-native:native"]["hostname"] == "cat8000v"

    new_config = copy.deepcopy(original_config)
    new_config["Cisco-IOS-XE-native:native"]["hostname"] = TEST_HOSTNAME
    for iface in new_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]:
        iface["description"] = iface["description"] + TEST_DESCRIPTION_SUFFIX
    client.restore_config(new_config)

    current_config = client.get_config()
    assert current_config["Cisco-IOS-XE-native:native"]["hostname"] == TEST_HOSTNAME
    for iface in current_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]:
        assert iface["description"].endswith(TEST_DESCRIPTION_SUFFIX)

    client.restore_config(original_config)

    restored_config = client.get_config()
    assert restored_config == ORIGINAL_CONFIG


    assert client.get_config.call_count == 3
    assert client.restore_config.call_count == 2
    client.restore_config.assert_has_calls([
        call(new_config),
        call(original_config),
    ])
