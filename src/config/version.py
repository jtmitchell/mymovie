"""
Current app version.
"""

import tomllib  # built-in from Python 3.11+; use `tomli` for older versions
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _get_version() -> str:
    pyproject = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
    try:
        return data["project"]["version"]
    except Exception:
        return "0.0.0"


try:
    VERSION = version("mymovie")
except PackageNotFoundError:
    VERSION = _get_version()  # Fallback for development mode
