# quanted-case

An "agentic company" knowledge pipeline: discover popular GitHub repos in the AI-agent
ecosystem, download their READMEs, and turn them into an Obsidian-style Markdown wiki
that an internal agent could read as a knowledge layer.

## 1. Overview

```
find.py -> manifest.json -> download.py -> raw/ -> [skill: vault-builder] -> wiki/
```

- **`find.py`** searches the GitHub REST API for candidate repos and writes/updates
  `manifest.json`.
- **`manifest.json`** is the human-editable source of truth for what gets ingested.
- **`download.py`** reads `manifest.json` and incrementally fetches missing READMEs into
  `raw/`.
- **The `vault-builder` skill** (`.claude/skills/vault-builder/SKILL.md`) reads `raw/` and
  `manifest.json`, does all the summarizing/understanding, and writes the Markdown wiki
  into `wiki/`.

The two Python scripts only talk to the GitHub REST API and the filesystem — no LLM
SDKs, clients, or API calls anywhere in `find.py` or `download.py`. Every bit of
"understanding" (what a project is, what it's good for, how pages relate to each other)
happens exclusively in the skill layer, per the constraints in [`CLAUDE.md`](CLAUDE.md).

## 2. Discovery approach and filters

`find.py` queries GitHub's `search/repositories` endpoint once per topic, across six
topics chosen to cover the ecosystem's main angles:

- `ai-agents`
- `llm-agent`
- `agent-framework`
- `multi-agent-systems`
- `agent-memory`
- `ai-agent-framework`

Each topic search asks for up to 30 results sorted by star count descending. Results
across all six topics are merged into one dict keyed by `full_name` — if the same repo
shows up under multiple topics, the highest observed star count wins — then the merged
set is sorted by stars descending.

`NEW_REPO_CAP` (20) is a **target for the total number of active entries in the
manifest**, not a per-run cap on new repos. `merge_manifest()` counts how many entries in
the existing manifest already have `status: "active"`; if that count is already at or
above the target, no new repos are added that run. Otherwise, discovered repos not
already present in the manifest (by `full_name`, whether currently active or excluded)
backfill the remaining slots, ranked by star count, until the active count reaches the
target or discovered candidates run out. This means excluding a repo effectively opens a
slot for the next-best candidate on a later `find.py` run.

Discovery from GitHub's topic search alone isn't perfectly clean — some results come back
with implausible star counts (consistent with star manipulation) or are only tangentially
related despite carrying an `ai-agents`-adjacent topic tag. `find.py` does not try to
filter these automatically; that's a deliberate design choice. `manifest.json` supports a
`status` field (`"active"` or `"excluded"`) plus an optional `excluded_reason`, and a
human reviewing the discovered set sets an entry's status directly in the file. Once an
entry is `"excluded"`, `find.py` treats it as frozen: it's never re-added, never
overwritten, and doesn't count toward the active target, even if it resurfaces in a later
topic search. In this project, four entries currently carry `status: "excluded"` after
manual review — two for implausible star counts, two for being off-topic despite matching
the search topics — and the manifest has 20 active / 4 excluded / 24 total entries as a
result.

## 3. Manifest + incremental download

`manifest.json` is a flat JSON list of objects, each with `full_name`, `html_url`,
`description`, `stargazers_count`, `topics`, and `status` (plus `excluded_reason` when
excluded). It's meant to be opened and hand-edited directly — someone can add an entry
GitHub search would never surface, delete one outright, or flip a `status` field, and both
`download.py` and the `vault-builder` skill respect that:

- `download.py` treats an entry as eligible for download unless its `status` is exactly
  `"excluded"` — entries with `status: "active"` or with no `status` field at all (e.g. a
  manually added entry) are both eligible.
- For each eligible entry it derives a filesystem-safe filename from `full_name`
  (`owner/repo` → `owner__repo.md`) and checks whether that file already exists in `raw/`.
  If it does, the entry is skipped without any network call. Only entries missing a file
  trigger a GitHub API request. This is what makes repeated runs cheap: re-running
  `download.py` after `find.py` backfills a few new entries only fetches those new
  entries, not the whole set again.
- A 404 from the README endpoint (repo has no README) is caught, logged as a warning, and
  skipped without aborting the rest of the run.
- `download.py` prints a three-way summary at the end: downloaded / skipped (already
  present) / excluded (by status).

## 4. The vault-builder skill

`vault-builder` is a single skill (`.claude/skills/vault-builder/SKILL.md`) with one
frontmatter definition and one shared procedure covering both modes — there's no separate
create/update skill.

**Mode decision:** `wiki/` empty (or the user explicitly asks to build from scratch) →
create mode; `wiki/` already has pages (or the user explicitly asks to update) → update
mode. If ambiguous, the skill defaults to update, since it's the non-destructive choice.

**Mapping raw files to manifest entries:** each `raw/` filename (`owner__repo.md`) is
turned back into a `full_name` by replacing the first `__` with `/` and stripping `.md`,
then looked up in `manifest.json`. A `raw/` file with no matching manifest entry is
skipped and noted as an issue rather than guessed at; an excluded entry found in `raw/` is
also skipped defensively (in practice this shouldn't happen, since `download.py` never
fetches excluded repos).

**What create mode does:** processes every raw/manifest pair, writing one
`wiki/<slug>.md` page per repo — covering what the project is, what problem it solves,
key features/use cases drawn from the actual README content (summarized, not pasted), and
a link back to the repo — then writes `wiki/index.md` from scratch, grouping pages by
category when a natural grouping falls out of the topics.

**What update mode does:** only processes `raw/` files that don't yet have a
corresponding `wiki/<slug>.md`; existing pages are never rewritten or touched. It then
updates `wiki/index.md` by inserting entries for the new pages only, without altering the
wording, links, or ordering of what's already there.

**Cross-linking:** pages use Obsidian `[[wikilink]]` syntax, added only where there's a
genuine relationship (competing frameworks, complementary tools, same category) — not
forced onto every page.

**Session logging (mandatory, both modes):** after finishing, the skill appends an entry
to `session-notes.md` at the project root — date, mode, the triggering prompt, a summary
of what was processed/created, and any issues or corrections encountered. This file is
append-only; the skill is instructed to never overwrite or delete a prior entry.

## 5. Setup & running it

**Prerequisites:**
- Python 3.11+
- A GitHub personal access token (optional but recommended — `find.py` and `download.py`
  both work unauthenticated, just at GitHub's lower unauthenticated rate limit, with a
  warning printed to say so)
- Claude Code, to run the `vault-builder` skill

**Setup:**

```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Set up your token
cp .env.example .env
# then edit .env and set GITHUB_TOKEN=<your token>
```

**Running the full pipeline:**

```bash
# 1. Discover repos and write/update manifest.json
python find.py

# (optional) review manifest.json by hand here — flip any entry's
# status to "excluded" and add an excluded_reason if it doesn't belong

# 2. Download READMEs for every active, not-yet-downloaded entry
python download.py

# 3. Build (or update) the wiki — inside Claude Code, in this project directory
claude
> Build the wiki from scratch using the vault-builder skill.
```

Re-running `find.py` followed by `download.py` and then asking Claude Code to update the
wiki is the incremental loop: `find.py` backfills active slots up to the ~20 target,
`download.py` only fetches the new entries, and the `vault-builder` skill only writes
pages for repos that don't already have one.

## 6. How Claude Code was used

The project was built by writing [`CLAUDE.md`](CLAUDE.md) first, before any code — it
encodes the pipeline shape and the hard constraints (no LLM code in `find.py`/
`download.py`, understanding lives only in the skill layer, one skill with two modes, the
manifest as human-editable source of truth, the append-only `session-notes.md` logging
rule) so every later prompt could be checked against a written contract instead of
re-litigating the rules each time.

Each script and the skill were then built from targeted, fully-specified prompts rather
than one broad "build the pipeline" ask — e.g. `find.py`'s spec named the exact endpoint,
the topic list, the dedup/sort/merge rules, and how existing vs. new entries should be
treated, before any code was written. Each piece was tested against the real GitHub API
immediately after being written, not mocked: `find.py`'s first run produced a real,
live-data `manifest.json`; `download.py` was run twice back-to-back specifically to prove
the incremental skip behavior (second run: 0 downloaded, all skipped) rather than taking
the "incremental" claim on faith.

When the cap logic in `merge_manifest()` was rewritten to target a total active count
instead of a flat per-run limit, the new function was sanity-checked with an isolated
test (simulating an excluded repo resurfacing with a wildly different star count) before
being trusted against the live API — confirming excluded entries stay completely frozen
while active entries still refresh.

Manual review caught things automated logic wasn't asked to catch: the first live
`find.py` run surfaced entries with implausible star counts (`affaan-m/ECC` at 225,282
stars, `NousResearch/hermes-agent` at 208,142 — both far outside what's plausible for
those repos) and at least one topically mismatched result. Rather than adding automated
anomaly filtering to `find.py`, the fix was architectural: a `status`/`excluded_reason`
field on manifest entries, so that judgment call stays a manual, auditable curation step
instead of a hardcoded blocklist or heuristic buried in the script.

`session-notes.md` captures this same distinction directly. Its first entry (2026-07-03,
`create` mode) logs the initial wiki build: 20 repos processed, pages listed by category,
zero unmatched files. A second entry, logged after the fact, documents a correction to
wording on the `daytonaio/daytona` page (it had been described as "archived," which
overstated what the repo's own README actually says — development moved to a private
codebase, but the repo isn't GitHub-archived) — explicitly marked as a manual correction
rather than a new skill run, so the log distinguishes actual skill executions from direct
edits.

## 7. What I'd improve with more time

- **Retry/backoff for GitHub API rate limits in `find.py`.** Right now a failed topic
  search (including a rate-limit response) is caught, logged as a warning, and skipped —
  the run continues with whatever topics succeeded, but a transient rate limit silently
  shrinks that run's discovered set instead of waiting and retrying.
- **A more robust `raw/` filename → manifest `full_name` mapping.** The current approach
  (`download.py`'s `safe_filename` joins `owner/repo` with `__`; the skill reverses it by
  splitting on the first `__`) works, but it's inferred from string structure rather than
  stored explicitly. It would be more robust for the skill to iterate `manifest.json`
  entries directly and check for the corresponding `raw/<safe_filename>` file, rather than
  reverse-parsing filenames back into `full_name`s.
- **Explicit UTF-8 decoding in `download.py`.** `fetch_readme()` currently returns
  `response.text`, which relies on `requests`' guessed encoding. Several READMEs in this
  set contain non-ASCII content (e.g. `666ghj/MiroFish`'s Chinese-language sections,
  emoji-heavy headers across many repos), and `requests`' encoding guess isn't always
  right for that. Decoding `response.content` as UTF-8 explicitly would be more reliable
  than trusting the guess.
- **Pagination for topic searches.** `find.py` requests one page of 30 results per topic;
  a topic with a deep pool of relevant repos beyond the top 30 by stars is invisible to
  discovery. This wasn't a real problem for the topics chosen here, but it would matter
  more with narrower or newer topics.
