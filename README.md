# quanted-case

## At a glance

This project discovers popular GitHub repos in the AI-agent ecosystem, downloads their
READMEs, and turns them into a Markdown wiki an internal agent could read as a knowledge
layer.

```
find.py -> manifest.json -> download.py -> raw/ -> [skill: vault-builder] -> wiki/
```

- **`find.py`** — discovers candidate repos via GitHub topic search, writes/updates
  `manifest.json`.
- **`manifest.json`** — the human-editable list of what gets ingested.
- **`download.py`** — fetches missing READMEs into `raw/`, incrementally.
- **`vault-builder` skill** — summarizes `raw/` content and writes the pages in `wiki/`.

`find.py` and `download.py` make no LLM calls — all summarization and understanding
happens in the `vault-builder` skill.

## Quick Start

```bash
uv sync && cp .env.example .env   # then set GITHUB_TOKEN in .env
python find.py && python download.py
claude   # then: "Build the wiki using the vault-builder skill."
```

## Discovery approach and filters

`find.py` queries GitHub's `search/repositories` endpoint once per topic, across six
topics chosen to cover the ecosystem's main angles:

- `ai-agents`
- `llm-agent`
- `agent-framework`
- `multi-agent-systems`
- `agent-memory`
- `ai-agent-framework`

How results are merged:

- Each topic search requests up to 30 results, sorted by star count descending.
- Results across all six topics are merged into one dict keyed by `full_name`.
- If a repo appears under multiple topics, the highest observed star count wins.
- The merged set is then sorted by stars descending.

`NEW_REPO_CAP` (20) is a **target for the total number of active entries in the
manifest** — not a per-run cap on new repos.

How `merge_manifest()` decides what to add:

- It counts existing entries with `status: "active"`.
- If that count is already at or above the target, no new repos are added this run.
- Otherwise, discovered repos not already in the manifest (active or excluded) backfill
  the remaining slots, ranked by star count, until the target is reached or discovered
  candidates run out.

Excluding a repo effectively opens a slot for the next-best candidate on a later
`find.py` run.

GitHub topic search alone isn't perfectly clean:

- Some results come back with implausible star counts (consistent with star
  manipulation).
- Some are only tangentially related despite carrying an `ai-agents`-adjacent topic tag.

`find.py` does not filter these automatically — that's a deliberate design choice.
Instead:

- `manifest.json` supports a `status` field (`"active"` or `"excluded"`) plus an
  optional `excluded_reason`.
- A human reviewing the discovered set sets an entry's status directly in the file.
- Once an entry is `"excluded"`, `find.py` treats it as frozen — never re-added, never
  overwritten, and it doesn't count toward the active target, even if it resurfaces in
  a later topic search.

In this project, four entries currently carry `status: "excluded"` after manual review
— two for implausible star counts, two for being off-topic despite matching the search
topics. The manifest has 21 active / 4 excluded / 25 total entries as a result.

## Manifest + incremental download

`manifest.json` is a flat JSON list of objects. Each entry has:

- `full_name`, `html_url`, `description`, `stargazers_count`, `topics`, `status`
- `excluded_reason` (present only when excluded)

It's meant to be opened and hand-edited directly — add an entry GitHub search would
never surface, delete one outright, or flip a `status` field. Both `download.py` and the
`vault-builder` skill respect manual edits:

- `download.py` treats an entry as eligible for download unless its `status` is exactly
  `"excluded"` — entries with `status: "active"` or no `status` field at all (e.g. a
  manually added entry) are both eligible.
- For each eligible entry it derives a filesystem-safe filename from `full_name`
  (`owner/repo` → `owner__repo.md`) and checks whether that file already exists in
  `raw/`. If it does, the entry is skipped without any network call. This is what makes
  repeated runs cheap: re-running `download.py` after `find.py` backfills a few new
  entries only fetches those new entries, not the whole set again.
- A 404 from the README endpoint (repo has no README) is caught, logged as a warning,
  and skipped without aborting the rest of the run.
- `download.py` prints a three-way summary at the end: downloaded / skipped (already
  present) / excluded (by status).

## The vault-builder skill

`vault-builder` is a single skill (`.claude/skills/vault-builder/SKILL.md`) with one
frontmatter definition and one shared procedure covering both modes — there's no
separate create/update skill.

**Mode decision:**

- `wiki/` empty, or the user explicitly asks to build from scratch → create mode.
- `wiki/` already has pages, or the user explicitly asks to update → update mode.
- If ambiguous, the skill defaults to update, since it's the non-destructive choice.

**Mapping raw files to manifest entries:** each `raw/` filename (`owner__repo.md`) is
turned back into a `full_name` by replacing the first `__` with `/` and stripping `.md`,
then looked up in `manifest.json`.

- A `raw/` file with no matching manifest entry is skipped and noted as an issue, not
  guessed at.
- An excluded entry found in `raw/` is also skipped defensively (in practice this
  shouldn't happen, since `download.py` never fetches excluded repos).

**What create mode does:** processes every raw/manifest pair, writing one
`wiki/<slug>.md` page per repo — what the project is, what problem it solves, key
features/use cases drawn from the actual README content (summarized, not pasted), and a
link back to the repo. Then it writes `wiki/index.md` from scratch, grouping pages by
category when a natural grouping falls out of the topics.

**What update mode does:** only processes `raw/` files that don't yet have a
corresponding `wiki/<slug>.md`; existing pages are never rewritten or touched. It then
updates `wiki/index.md` by inserting entries for the new pages only, without altering
the wording, links, or ordering of what's already there.

**Cross-linking:** pages use Obsidian `[[wikilink]]` syntax, added only where there's a
genuine relationship (competing frameworks, complementary tools, same category) — not
forced onto every page.

**Session logging (mandatory, both modes):** after finishing, the skill appends an
entry to `session-notes.md` at the project root, recording:

- date
- mode
- the triggering prompt
- a summary of what was processed/created
- any issues or corrections encountered

This file is append-only; the skill is instructed to never overwrite or delete a prior
entry.

## Setup & running it

**Prerequisites:**

- Python 3.11+ and [uv](https://docs.astral.sh/uv/)
- A GitHub personal access token (optional but recommended — `find.py` and
  `download.py` both work unauthenticated, just at GitHub's lower unauthenticated rate
  limit, with a warning printed to say so)
- Claude Code, to run the `vault-builder` skill

**Setup:**

```bash
# 1. Install dependencies (creates .venv/, resolves from uv.lock)
uv sync

# 2. Set up your token
cp .env.example .env
# then edit .env and set GITHUB_TOKEN=<your token>
```

**Running the full pipeline:**

```bash
# 1. Discover repos and write/update manifest.json
uv run python find.py

# (optional) review manifest.json by hand here — flip any entry's
# status to "excluded" and add an excluded_reason if it doesn't belong

# 2. Download READMEs for every active, not-yet-downloaded entry
uv run python download.py

# 3. Build (or update) the wiki — inside Claude Code, in this project directory
claude
> Build the wiki from scratch using the vault-builder skill.
```

The incremental loop is: re-run `find.py`, then `download.py`, then ask Claude Code to
update the wiki.

- `find.py` backfills active slots up to the ~20 target.
- `download.py` only fetches the new entries.
- The `vault-builder` skill only writes pages for repos that don't already have one.

## How Claude Code was used

[`CLAUDE.md`](CLAUDE.md) was written first, before any code. It encodes the pipeline
shape and hard constraints:

- No LLM code in `find.py`/`download.py`.
- Understanding lives only in the skill layer.
- One skill, two modes.
- The manifest is the human-editable source of truth.
- `session-notes.md` logging is append-only.

Each script and the skill were built from targeted, fully-specified prompts — e.g.
`find.py`'s spec named the exact endpoint, the topic list, and the dedup/sort/merge
rules up front.

Each piece was tested against the real GitHub API immediately after being written:

- `find.py`'s first run produced a real, live-data `manifest.json`.
- `download.py` was run twice back-to-back to confirm incremental skip behavior (second
  run: 0 downloaded, all skipped).

When the cap logic in `merge_manifest()` was rewritten to target a total active count
instead of a flat per-run limit, it was sanity-checked with an isolated test: an
excluded repo resurfacing with a wildly different star count. Result: excluded entries
stay completely frozen, active entries still refresh.

Manual review caught what automated logic wasn't asked to catch. The first live
`find.py` run surfaced:

- Implausible star counts (`affaan-m/ECC` at 225,282 stars, `NousResearch/hermes-agent`
  at 208,142).
- At least one topically mismatched result.

The fix was architectural, not a filtering heuristic: the `status`/`excluded_reason`
field on manifest entries, keeping that judgment call a manual, auditable curation step.

`session-notes.md` reflects the same distinction:

- First entry (2026-07-03, `create` mode): the initial wiki build — 20 repos processed,
  pages listed by category, zero unmatched files.
- Second entry: a correction to the `daytonaio/daytona` page's wording. It had been
  described as "archived," which overstated the README — development moved to a
  private codebase, but the repo isn't GitHub-archived. Logged explicitly as a manual
  correction, not a new skill run.

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for what I'd do with more time.
