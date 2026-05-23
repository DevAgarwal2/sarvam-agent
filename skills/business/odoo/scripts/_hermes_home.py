"""
Resolve HERMES_HOME directory path.
Tries to import from hermes_constants if running inside the Hermes runtime,
otherwise falls back to the HERMES_HOME environment variable or ~/.hermes.
"""
import os
from pathlib import Path


def get_hermes_home() -> Path:
    try:
        from hermes_constants import HERMES_HOME
        return HERMES_HOME
    except ImportError:
        env_home = os.environ.get("HERMES_HOME")
        if env_home:
            return Path(env_home).expanduser().resolve()
        return Path.home() / ".hermes"


def display_hermes_home() -> str:
    home = get_hermes_home()
    try:
        return "~/" + str(home.relative_to(Path.home()))
    except ValueError:
        return str(home)
