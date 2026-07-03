# Session Notes

## 2026-07-03 — create

**Prompt:** "Build the wiki from scratch using the vault-builder skill."

**Summary:** `wiki/` was empty, so this ran in create mode. Processed all 20 READMEs in `raw/`, cross-referenced against `manifest.json` by full_name. All 20 had a matching active entry (0 unmatched, 0 excluded entries found present in `raw/` — consistent with `download.py` never fetching excluded repos). Created 20 per-repo pages plus `wiki/index.md`, grouped into 6 categories inferred from repo topics/content: Frameworks (6), Orchestration & Agent Harnesses (4), Memory (2), Skills & Plugins (3), Agent Tooling & Infrastructure (3), Learning Resources (2). Added judicious `[[wikilinks]]` between related pages (e.g. memory pages cross-link, orchestration harnesses cross-link, competing multi-agent frameworks cross-link) — not on every page uniformly.

**Issues/corrections:** None. One note: `daytonaio/daytona`'s README states the repo is now archived/maintenance-only (core dev moved to a private codebase as of June 2026) — flagged in its wiki page since that materially affects whether it's still a good reference. `microsoft/autogen`'s README similarly flags maintenance mode in favor of Microsoft Agent Framework — also carried into its page.

## 2026-07-03 — correction (manual, not a skill run)

**Prompt:** "correct the status note [on daytonaio__daytona.md]... it's not 'archived'" / follow-up: "fix the one-liner for daytonaio/daytona [in index.md]... append a new short entry documenting this correction."

**Summary:** Manual correction, not a create/update run of the vault-builder skill. The earlier create-mode entry above (and the wiki text it produced) described `daytonaio/daytona` as "archived." That was inaccurate: the repo is not GitHub-archived/read-only — it remains open. The accurate statement, per the project's own README, is that Daytona's core development moved to a private codebase as of June 2026 and the public repo will receive no further updates, fixes, or releases, but it is not archived.

**Files fixed:** `wiki/daytonaio__daytona.md` (Overview section wording) and `wiki/index.md` (the daytonaio/daytona one-liner under "Agent Tooling & Infrastructure").

## 2026-07-03 — update

**Prompt:** "Update the wiki with the new repo using the vault-builder skill."

**Summary:** `wiki/` already had 20 pages, so this ran in update mode. `raw/` had one file with no corresponding wiki page: `letta-ai__letta.md`, matching the manually-added `letta-ai/letta` manifest entry (status `active`). Created `wiki/letta-ai__letta.md` (categorized as Memory — a stateful-agent platform built around structured, agent-editable memory blocks). Updated `wiki/index.md` by inserting one new line under the existing "Memory" section; no other section or existing entry was altered. No other `raw/` files were touched or reprocessed.

**Issues/corrections:** None. `letta-ai/letta` was added to `manifest.json` by hand (not via `find.py`) and downloaded via a normal `download.py` run before this skill invocation — both worked as designed for a manually-curated addition.
