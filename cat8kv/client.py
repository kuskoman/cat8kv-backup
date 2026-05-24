import urllib3
import requests

from cat8kv.config import DeviceConfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS_GET = {"Accept": "application/yang-data+json"}
HEADERS_PUT = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

ENDPOINTS = {
    "native": "/restconf/data/Cisco-IOS-XE-native:native",
    "hostname": "/restconf/data/Cisco-IOS-XE-native:native/hostname",
    "interfaces": "/restconf/data/Cisco-IOS-XE-native:native/interface",
}


class RestconfClient:
    def __init__(self, config: DeviceConfig) -> None:
        self.base_url = f"https://{config.host}:{config.port}"
        self.session = requests.Session()
        self.session.auth = (config.username, config.password)
        self.session.verify = False

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{ENDPOINTS[endpoint]}"

    def get(self, endpoint: str) -> dict:
        response = self.session.get(self._url(endpoint), headers=HEADERS_GET, timeout=30)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict) -> None:
        response = self.session.put(self._url(endpoint), headers=HEADERS_PUT, json=data, timeout=30)
        response.raise_for_status()

    def get_config(self) -> dict:
        return self.get("native")

    def get_hostname(self) -> str:
        data = self.get("hostname")
        return data["Cisco-IOS-XE-native:hostname"]

    def set_hostname(self, hostname: str) -> None:
        self.put("hostname", {"Cisco-IOS-XE-native:hostname": hostname})

    def restore_config(self, config: dict) -> None:
        self.put("native", config)

    def restore_interfaces(self, interfaces: dict) -> None:
        self.put("interfaces", interfaces)

    def get_interfaces(self) -> dict:
        return self.get("interfaces")

    def set_interface_description(self, interface_name: str, description: str) -> None:
        endpoint = f"/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={interface_name}"
        url = f"{self.base_url}{endpoint}"
        data = {
            "Cisco-IOS-XE-native:GigabitEthernet": {
                "name": interface_name,
                "description": description,
            }
        }
        response = self.session.patch(url, headers=HEADERS_PUT, json=data, timeout=30)
        response.raise_for_status()
