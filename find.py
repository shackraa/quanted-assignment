"""Discover popular GitHub repos in the AI-agent ecosystem and write manifest.json.

Queries the GitHub REST API's search/repositories endpoint across a handful of
topics covering agent frameworks, agent memory, agent skills/plugins, and agent
orchestration, then merges the results into manifest.json. Contains no LLM SDKs,
clients, or API calls — only the GitHub REST API and the filesystem.

Run standalone:
    python find.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
MANIFEST_PATH = Path(__file__).resolve().parent / "manifest.json"

# Target number of ACTIVE entries to maintain in the manifest overall (not a
# per-run limit on new repos). If the manifest already has this many active
# entries, no new repos are added. Otherwise new repos backfill the remaining
# slots — e.g. slots vacated by excluded entries get filled by the
# next-best discovered candidates.
NEW_REPO_CAP = 20

# Number of results to request per topic search (raw candidates before merging).
RESULTS_PER_TOPIC = 30

# Topics covering the AI-agent ecosystem: frameworks, memory, skills/plugins,
# and orchestration.
TOPICS: list[str] = [
    "ai-agents",
    "llm-agent",
    "agent-framework",
    "multi-agent-systems",
    "agent-memory",
    "ai-agent-framework",
]

# Manifest entry status values. "excluded" is set by a human reviewer and is
# never re-added, overwritten, or removed by this script — it persists until a
# human manually changes it back.
STATUS_ACTIVE = "active"
STATUS_EXCLUDED = "excluded"


def build_headers(token: str | None) -> dict[str, str]:
    """Build GitHub API request headers, adding a bearer token if one is available."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def search_topic(topic: str, headers: dict[str, str]) -> list[dict[str, Any]]:
    """Query the GitHub search/repositories endpoint for a single topic.

    Returns the raw list of repo objects from the API, sorted by stars descending.
    Returns an empty list (with a warning) if the request fails.
    """
    params = {
        "q": f"topic:{topic}",
        "sort": "stars",
        "order": "desc",
        "per_page": RESULTS_PER_TOPIC,
    }
    response = requests.get(GITHUB_SEARCH_URL, headers=headers, params=params, timeout=30)
    if response.status_code != 200:
        print(
            f"Warning: search for topic '{topic}' failed "
            f"({response.status_code}): {response.text[:200]}"
        )
        return []
    return response.json().get("items", [])


def to_entry(repo: dict[str, Any]) -> dict[str, Any]:
    """Convert a raw GitHub API repo object into a manifest entry."""
    return {
        "full_name": repo["full_name"],
        "html_url": repo["html_url"],
        "description": repo.get("description"),
        "stargazers_count": repo.get("stargazers_count", 0),
        "topics": repo.get("topics", []),
    }


def discover_repos(headers: dict[str, str]) -> list[dict[str, Any]]:
    """Search all configured topics and return merged, de-duplicated entries.

    De-duplication is by full_name; results are sorted by star count descending.
    """
    merged: dict[str, dict[str, Any]] = {}
    for topic in TOPICS:
        for repo in search_topic(topic, headers):
            entry = to_entry(repo)
            full_name = entry["full_name"]
            existing = merged.get(full_name)
            if existing is None or entry["stargazers_count"] > existing["stargazers_count"]:
                merged[full_name] = entry
    return sorted(merged.values(), key=lambda e: e["stargazers_count"], reverse=True)


def load_manifest(path: Path) -> list[dict[str, Any]]:
    """Load the existing manifest.json, or return an empty list if it doesn't exist."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def merge_manifest(
    existing: list[dict[str, Any]],
    discovered: list[dict[str, Any]],
    cap: int,
) -> list[dict[str, Any]]:
    """Merge newly discovered repos into the existing manifest.

    `cap` is a target for the total number of ACTIVE entries in the manifest,
    not a per-run limit on how many new repos may be added:

    - Existing entries (including manually added/edited ones) are never removed,
      even if they don't appear in this run's discovered results.
    - Entries with status "excluded" are frozen: they are never re-added,
      overwritten, or have any field (including `stargazers_count`) refreshed
      when they resurface in search results, and they don't count toward the
      active target. They stay excluded until a human manually edits their
      status back in manifest.json.
    - Non-excluded existing entries only have their `stargazers_count` refreshed
      when the repo re-appears in this run's results; every other field is left
      untouched so manual edits survive.
    - If the manifest already has `cap` or more active entries, no new repos
      are added this run.
    - Otherwise, discovered repos whose full_name isn't already present in the
      manifest at all (active or excluded — never duplicate either) are added
      with status "active", ranked by star count, backfilling the remaining
      slots (e.g. ones vacated by excluded entries) until the active count
      reaches `cap` or discovered candidates run out.
    """
    existing_by_name = {entry["full_name"]: entry for entry in existing}
    discovered_by_name = {entry["full_name"]: entry for entry in discovered}

    merged: list[dict[str, Any]] = []
    for entry in existing:
        entry = dict(entry)
        entry.setdefault("status", STATUS_ACTIVE)
        if entry["status"] != STATUS_EXCLUDED:
            rediscovered = discovered_by_name.get(entry["full_name"])
            if rediscovered is not None:
                entry["stargazers_count"] = rediscovered["stargazers_count"]
        merged.append(entry)

    active_count = sum(1 for entry in merged if entry["status"] == STATUS_ACTIVE)
    slots_remaining = max(0, cap - active_count)

    if slots_remaining > 0:
        new_repos = [
            {**entry, "status": STATUS_ACTIVE}
            for entry in discovered
            if entry["full_name"] not in existing_by_name
        ]
        new_repos_sorted = sorted(new_repos, key=lambda e: e["stargazers_count"], reverse=True)
        merged.extend(new_repos_sorted[:slots_remaining])

    return merged


def write_manifest(path: Path, manifest: list[dict[str, Any]]) -> None:
    """Write the manifest to disk as stable, pretty-printed JSON."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    """Discover AI-agent ecosystem repos and update manifest.json."""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not set; using unauthenticated requests (lower rate limit).")

    headers = build_headers(token)
    discovered = discover_repos(headers)
    existing = load_manifest(MANIFEST_PATH)
    manifest = merge_manifest(existing, discovered, NEW_REPO_CAP)
    write_manifest(MANIFEST_PATH, manifest)

    new_count = len(manifest) - len(existing)
    print(f"Discovered {len(discovered)} unique repos across {len(TOPICS)} topics.")
    print(f"Manifest now has {len(manifest)} entries ({new_count} newly added this run).")


if __name__ == "__main__":
    main()
