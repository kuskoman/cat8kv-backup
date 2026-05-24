#!/usr/bin/env python3
import json
import urllib3
from pathlib import Path

import requests

from cat8kv.client import ENDPOINTS
from cat8kv.config import load_config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FIXTURES_DIR = Path("tests/fixtures")

HEADERS = {"Accept": "application/yang-data+json"}


def fetch(session: requests.Session, base_url: str, endpoint: str) -> dict:
    url = f"{base_url}{endpoint}"
    print(f"  GET {url}")
    response = session.get(url, headers=HEADERS, verify=False, timeout=30)
    response.raise_for_status()
    return response.json()


def save_fixture(name: str, data: dict) -> None:
    path = FIXTURES_DIR / f"{name}.json"
    path.write_text(json.dumps(data, indent=2))
    print(f"  [OK] Saved: {path}")


def main() -> None:
    print("=== Fetching fixtures ===\n")
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

    config = load_config()
    base_url = f"https://{config.host}:{config.port}"

    session = requests.Session()
    session.auth = (config.username, config.password)

    for name, endpoint in ENDPOINTS.items():
        print(f"[->] {name}")
        try:
            data = fetch(session, base_url, endpoint)
            save_fixture(name, data)
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] {e}")
        print()

    print("=== Done ===")


if __name__ == "__main__":
    main()
