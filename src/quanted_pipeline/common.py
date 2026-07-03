"""Shared helpers used by both find.py and download.py.

Holds the project-root-relative paths, manifest status constants, manifest
I/O, and the GitHub API header fields common to both scripts (Authorization
and X-GitHub-Api-Version). Each script still builds its own `Accept` header,
since they request different response formats.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = PROJECT_ROOT / "manifest.json"

# Manifest entry status values. "excluded" is set by a human reviewer and is
# never re-added, overwritten, or removed by find.py -- it persists until a
# human manually changes it back. download.py treats it as non-eligible.
STATUS_ACTIVE = "active"
STATUS_EXCLUDED = "excluded"


def _base_headers(token: str | None) -> dict[str, str]:
    """Build the GitHub API headers shared by find.py and download.py.

    Adds the API version header always, and a bearer Authorization header if
    a token is available. Callers add their own `Accept` header on top.
    """
    headers = {"X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_manifest(path: Path) -> list[dict[str, Any]]:
    """Load a manifest JSON file. Returns an empty list if it doesn't exist."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
