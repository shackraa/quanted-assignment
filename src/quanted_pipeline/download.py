"""Download READMEs for eligible repos listed in manifest.json into raw/.

Reads manifest.json (the human-curated source of truth), skips entries whose
status is exactly "excluded", and incrementally fetches READMEs for every
other eligible repo via the GitHub REST API. Already-downloaded READMEs are
never re-fetched. Contains no LLM SDKs, clients, or API calls — only the
GitHub REST API and the filesystem.

Invoked via the root-level wrapper:
    python download.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from .common import MANIFEST_PATH, PROJECT_ROOT, STATUS_EXCLUDED, _base_headers, load_manifest

GITHUB_API_URL = "https://api.github.com"
RAW_DIR = PROJECT_ROOT / "raw"


def build_headers(token: str | None) -> dict[str, str]:
    """Build GitHub API request headers for fetching raw README content."""
    return {"Accept": "application/vnd.github.raw+json", **_base_headers(token)}


def is_eligible(entry: dict[str, Any]) -> bool:
    """An entry is eligible for download unless its status is exactly "excluded".

    Entries with status "active", or with no status field at all (e.g. added
    by hand), are both eligible.
    """
    return entry.get("status") != STATUS_EXCLUDED


def safe_filename(full_name: str) -> str:
    """Derive a filesystem-safe .md filename from a repo's full_name."""
    return full_name.replace("/", "__") + ".md"


def fetch_readme(full_name: str, headers: dict[str, str]) -> str | None:
    """Fetch a repo's README as raw Markdown text via the GitHub REST API.

    Returns None (after printing a warning) if the repo has no README (404)
    or the request otherwise fails.
    """
    url = f"{GITHUB_API_URL}/repos/{full_name}/readme"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 404:
        print(f"Warning: no README found for '{full_name}' (404), skipping.")
        return None
    if response.status_code != 200:
        print(
            f"Warning: failed to fetch README for '{full_name}' "
            f"({response.status_code}): {response.text[:200]}"
        )
        return None
    return response.text


def download_readmes(
    manifest: list[dict[str, Any]],
    headers: dict[str, str],
    raw_dir: Path,
) -> tuple[int, int, int]:
    """Download READMEs for eligible, not-yet-downloaded manifest entries.

    Skips entries whose file already exists in raw_dir (incremental behavior)
    and entries with status "excluded". Returns a
    (downloaded, skipped, excluded) count tuple.
    """
    raw_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    excluded = 0

    for entry in manifest:
        full_name = entry["full_name"]

        if not is_eligible(entry):
            excluded += 1
            continue

        dest = raw_dir / safe_filename(full_name)
        if dest.exists():
            skipped += 1
            continue

        readme = fetch_readme(full_name, headers)
        if readme is None:
            continue

        dest.write_text(readme, encoding="utf-8")
        downloaded += 1
        print(f"Downloaded {full_name} -> {dest.name}")

    return downloaded, skipped, excluded


def main() -> None:
    """Incrementally download READMEs for eligible manifest entries into raw/."""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not set; using unauthenticated requests (lower rate limit).")

    headers = build_headers(token)
    manifest = load_manifest(MANIFEST_PATH)
    downloaded, skipped, excluded = download_readmes(manifest, headers, RAW_DIR)

    print(
        f"Done. {downloaded} downloaded, {skipped} skipped (already present), "
        f"{excluded} excluded (by status)."
    )


if __name__ == "__main__":
    main()
