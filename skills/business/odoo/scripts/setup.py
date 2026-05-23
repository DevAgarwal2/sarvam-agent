#!/usr/bin/env python3
"""
Odoo credential setup for Hermes skills.
Stores Odoo connection details in ~/.hermes/odoo_config.json.
The agent drives this non-interactively via CLI flags.

Commands:
    --check                   Verify credentials exist and connection works
    --store URL DB USER PASS  Save credentials to config file
    --clear                   Remove stored credentials

Usage by the agent:
    Step 0: python setup.py --check
    Step 1: Ask user for Odoo URL, database name, username, password
    Step 2: python setup.py --store <url> <db> <user> <pass>
    Step 3: python setup.py --check
"""
import argparse
import json
import sys
from pathlib import Path
from _hermes_home import get_hermes_home, display_hermes_home

CONFIG_FILE = "odoo_config.json"


def config_path() -> Path:
    return get_hermes_home() / CONFIG_FILE


def load_config():
    cp = config_path()
    if not cp.exists():
        return None
    try:
        return json.loads(cp.read_text())
    except (json.JSONDecodeError, IOError):
        return None


def save_config(url: str, db: str, user: str, password: str):
    hermes = get_hermes_home()
    hermes.mkdir(parents=True, exist_ok=True)
    config = {
        "url": url.rstrip("/"),
        "db": db,
        "user": user,
        "password": password,
    }
    config_path().write_text(json.dumps(config, indent=2))
    print(f"SAVED: {display_hermes_home()}/{CONFIG_FILE}")


def check_auth() -> bool:
    """Validate that config exists and the Odoo connection works."""
    config = load_config()
    if not config:
        print("NOT_CONFIGURED")
        sys.exit(1)

    print(f"URL: {config['url']}")
    print(f"DB:  {config['db']}")
    print(f"USER: {config['user']}")

    try:
        import urllib.request
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [config["db"], config["user"], config["password"], {}]
            },
            "id": 1,
        }
        req = urllib.request.Request(
            f"{config['url']}/jsonrpc",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        if data.get("result") and isinstance(data["result"], int):
            uid = data["result"]
            print(f"AUTHENTICATED (uid={uid})")
            return True
        else:
            print("AUTH_FAILED: " + str(data.get("error", "unknown error")))
            sys.exit(1)
    except Exception as e:
        print(f"CONNECTION_FAILED: {e}")
        sys.exit(1)


def clear_config():
    cp = config_path()
    if cp.exists():
        cp.unlink()
        print(f"REMOVED: {display_hermes_home()}/{CONFIG_FILE}")
    else:
        print("NOT_FOUND: no config to remove")


def main():
    parser = argparse.ArgumentParser(description="Odoo credential setup for Hermes")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Verify credentials and connection")
    group.add_argument("--store", nargs=4, metavar=("URL", "DB", "USER", "PASS"),
                       help="Save credentials (URL DB USER PASSWORD)")
    group.add_argument("--clear", action="store_true", help="Remove stored credentials")
    args = parser.parse_args()

    if args.check:
        check_auth()
    elif args.store:
        save_config(*args.store)
    elif args.clear:
        clear_config()


if __name__ == "__main__":
    main()
