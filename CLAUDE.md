# quanted-case

## Project Overview
This project is a take-home technical case for Quanted: an "agentic company" knowledge
pipeline. It discovers popular GitHub repositories in the AI-agent ecosystem (frameworks,
memory, skills/plugins, orchestration), downloads their READMEs, and generates a Markdown
wiki (Obsidian-vault style) meant to be a knowledge layer an internal agent could read.

## Pipeline

```
find.py -> manifest.json -> download.py -> raw/ -> [skill: vault-builder] -> wiki/
```

- **find.py** — queries the GitHub REST API for candidate repos and writes/updates
  `manifest.json`.
- **manifest.json** — the human-editable source of truth for what gets ingested. Anyone
  can open it and manually add or remove an entry; both `download.py` and the skill must
  respect manual edits.
- **download.py** — reads `manifest.json`, incrementally fetches missing READMEs into
  `raw/`.
- **vault-builder skill** (`.claude/skills/vault-builder/`) — reads `raw/`, does all
  understanding/summarizing, and writes the Markdown wiki into `wiki/`.

## Hard Constraints

1. **No LLM code in Python.** `find.py` and `download.py` must contain **no LLM SDKs,
   clients, or API calls whatsoever** — no Anthropic, OpenAI, LangChain, or any similar
   library/import. They may only talk to the GitHub REST API and the local filesystem.
   `requests` or `httpx` are fine for HTTP.
2. **Understanding lives only in the skill layer.** All summarizing, categorizing, and
   wiki-writing logic lives exclusively under `.claude/skills/`. Python scripts never
   summarize or interpret content — they only fetch and move data.
3. **download.py must be incremental.** Given `manifest.json`, it only fetches READMEs
   for entries it hasn't already downloaded (e.g. by checking what already exists in
   `raw/`). It must never blindly re-download everything on every run.
4. **One skill, two modes.** The wiki is produced by a single skill
   (`vault-builder`) that supports:
   - `create` — build the vault from scratch.
   - `update` — add only newly downloaded repos since the last run.

   Both modes are driven by the same skill definition and shared logic — do not fork
   this into two separate skills.
5. **Wiki is plain Markdown only.** No vector store, no database, no embeddings. Just
   `.md` files (and Obsidian-style `[[wikilinks]]` where useful) under `wiki/`.
6. **Python code must be clean and typed.** Type hints on all function signatures,
   docstrings, sensible module structure, and each script must be runnable independently
   (`python find.py`, `python download.py`) without depending on being imported by
   another script first.
7. **manifest.json is human-editable.** It is the source of truth for ingestion — someone
   must be able to open it, hand-add or hand-remove an entry, and have `download.py` /
   the skill respect that on the next run.

## Session Notes Rule

Every time the `vault-builder` skill runs, in **either mode** (`create` or `update`), it
must append an entry to `session-notes.md` at the project root. Each entry must record:

- **Date** of the run
- **Mode** (`create` or `update`)
- **The user's prompt** that triggered the run
- **A summary** of what was done (repos processed, pages created/updated, etc.)
- **Any issues or corrections** encountered during the run (missing READMEs, malformed
  manifest entries, conflicts with manually-edited wiki content, etc.)

`session-notes.md` is append-only — never overwrite or delete prior entries when adding a
new one.

## Project Structure
- `find.py` — GitHub repo discovery, writes `manifest.json`.
- `manifest.json` — human-editable ingestion list.
- `download.py` — incremental README downloader, writes to `raw/`.
- `raw/` — downloaded README files, one per repo.
- `wiki/` — generated Obsidian-style Markdown vault (output of the skill).
- `.claude/skills/vault-builder/` — the single skill implementing both `create` and
  `update` modes.
- `session-notes.md` — append-only log of every skill run.

## Coding Conventions
- Python 3.11+, standard type hints (`list[str]`, `dict[str, Any]`, etc.), docstrings on
  every public function.
- Prefer `pathlib.Path` over raw string paths.
- Keep `find.py` and `download.py` dependency-light: only `requests`/`httpx` plus
  standard library.
- No hardcoded secrets — GitHub tokens (if used) come from environment variables.
