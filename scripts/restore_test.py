#!/usr/bin/env python3
import copy

from cat8kv.client import RestconfClient
from cat8kv.config import load_config

TEST_HOSTNAME = "cat8000v-test-backup"
TEST_DESCRIPTION_SUFFIX = "-CHANGED"


def main() -> None:
    config = load_config()
    client = RestconfClient(config)

    print("=== Restore Test ===\n")

    print("[1] Backing up configuration...")
    original_config = client.get_config()
    original_hostname = original_config["Cisco-IOS-XE-native:native"]["hostname"]
    gi_list = original_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]
    print(f"    Hostname: {original_hostname}")
    for iface in gi_list:
        print(f"    GigabitEthernet{iface['name']}: {iface.get('description', '(no description)')}")

    print(f"\n[2] Applying changes...")
    changed_config = copy.deepcopy(original_config)
    changed_config["Cisco-IOS-XE-native:native"]["hostname"] = TEST_HOSTNAME
    for iface in changed_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]:
        iface["description"] = iface.get("description", "") + TEST_DESCRIPTION_SUFFIX
    client.restore_config(changed_config)
    print(f"    Hostname -> {TEST_HOSTNAME}")
    for iface in changed_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]:
        print(f"    GigabitEthernet{iface['name']} -> {iface['description']}")

    print("\n[3] Verifying changes...")
    current_config = client.get_config()
    assert current_config["Cisco-IOS-XE-native:native"]["hostname"] == TEST_HOSTNAME, (
        f"Expected {TEST_HOSTNAME}, got {current_config['Cisco-IOS-XE-native:native']['hostname']}"
    )
    for iface in current_config["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]:
        assert iface.get("description", "").endswith(TEST_DESCRIPTION_SUFFIX), (
            f"Interface {iface['name']} description not changed: {iface.get('description')}"
        )
    print("    [OK] All changes verified")

    print("\n[4] Restoring original configuration...")
    client.restore_config(original_config)

    print("\n[5] Verifying restore...")
    restored_config = client.get_config()
    assert restored_config == original_config, "Restored config does not match original"
    print(f"    [OK] Hostname restored to: {restored_config['Cisco-IOS-XE-native:native']['hostname']}")
    print("    [OK] Full configuration matches original")

    print("\n=== All steps passed ===")


if __name__ == "__main__":
    main()
