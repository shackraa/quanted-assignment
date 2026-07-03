---
name: vault-builder
description: Build or update the Obsidian-style Markdown wiki in wiki/ from the READMEs in raw/ and their metadata in manifest.json. Trigger this skill whenever the user asks to build, create, generate, regenerate, or update the wiki/vault/knowledge-base from downloaded repo data — e.g. "build the wiki", "create the vault", "update the wiki with the new repos", "regenerate the knowledge base". This is the only place in the project where summarizing/understanding of README content happens; find.py and download.py never do this work.
---

# vault-builder

Turn the raw READMEs in `raw/` and their metadata in `manifest.json` into an
Obsidian-vault-style Markdown wiki under `wiki/`. All judgment — reading a
README, deciding what matters, writing prose, choosing cross-links — happens
here, in this skill, by you. Nothing upstream (`find.py`, `download.py`) does
any of this; they only move data.

This is a single skill with two modes, **create** and **update**. Don't treat
them as separate skills or duplicate logic — decide the mode first, then run
one shared procedure that branches only where the modes genuinely differ.

## 1. Decide the mode

- **create** — `wiki/` is empty (no `.md` files other than a possible stray
  `index.md`), OR the user explicitly asked to build/regenerate the vault
  from scratch.
- **update** — `wiki/` already contains repo pages, OR the user explicitly
  asked to update/refresh the wiki with newly downloaded repos.

If it's ambiguous (e.g. `wiki/` has pages but the user's phrasing is vague),
default to **update** — it's the non-destructive choice, since update mode
never touches existing pages.

## 2. Build the set of repos to process

1. List every file in `raw/`. Each filename is a slug of the form
   `owner__repo.md` (produced by `download.py`'s `safe_filename`). Recover
   the manifest `full_name` by replacing the first `__` with `/` and
   stripping the `.md` extension (e.g. `firecrawl__firecrawl.md` →
   `firecrawl/firecrawl`).
2. Load `manifest.json` and look up each recovered `full_name`.
   - If no matching entry exists, skip that file, and note it as an issue
     in the session-notes entry (see step 6) — don't guess at metadata.
   - If the matching entry has `"status": "excluded"`, skip it. (In
     practice `download.py` never fetches excluded repos, so this
     shouldn't happen, but skip defensively rather than assume.)
3. From the remaining raw/manifest pairs, narrow to the repos this run
   should actually produce pages for:
   - **create mode:** all of them.
   - **update mode:** only those whose slug has no corresponding file
     already in `wiki/` (i.e. `wiki/<slug>.md` doesn't exist yet). Existing
     wiki pages are never rewritten, regenerated, or otherwise touched —
     don't open them except to read titles/links for index purposes.

## 3. Write one page per repo: `wiki/<slug>.md`

Use the same slug as the raw filename (`owner__repo.md`), so pages map
1:1 back to `raw/` and `manifest.json` entries.

Read the actual README content plus the manifest entry's `description`,
`stargazers_count`, `topics`, and `html_url` for context, then write a page
that covers, in your own words (don't just paste the README):

- **What the project is** — a clear, short framing of what it does.
- **What problem it solves / what it's good for** — the use case, not just
  a feature list.
- **Key features or use cases** — pulled from the README, summarized, not
  copied verbatim at length.
- **A link back to the repo** — the `html_url` from the manifest.

A reasonable structure (adapt as the content calls for it — don't force a
rigid template onto a page where it doesn't fit):

```markdown
# <repo name>

**GitHub:** <html_url>
**Stars:** <stargazers_count>
**Topics:** <topics, e.g. as tags or a comma-separated list>

## Overview
...

## Key Features / Use Cases
...

## Related
- [[other-slug]] — one line on why it's related
```

Add `[[wikilink]]`-style links to other pages only where there's a genuine
relationship (same category, competing approaches, complementary tools,
one builds on the other). Don't force a "Related" section onto every page
if nothing is actually related — a page with no meaningful cross-links can
just omit that section.

## 4. Write or update `wiki/index.md`

- **create mode:** write `wiki/index.md` from scratch, linking to every
  page you just generated. Group by category if a natural grouping falls
  out of the topics (e.g. Frameworks, Memory, Skills/Plugins,
  Orchestration, Other) — otherwise a flat alphabetical list of
  `[[wikilinks]]` with a one-line description each is fine. Prefer
  whichever reads more usefully given what actually got discovered; don't
  invent categories that only have one member.
- **update mode:** read the existing `wiki/index.md` and add entries for
  the newly created pages only, in a way consistent with its existing
  structure (same grouping scheme, same list style). Do not alter the
  wording, links, or ordering of entries already present — only insert the
  new ones.

## 5. Output constraints

- Plain Markdown only. No vector store, no database, no embeddings, no
  JSON/YAML sidecar files, no other formats — just `.md` files under
  `wiki/`.
- Every page and the index must be valid, readable Markdown on its own
  (someone should be able to open any single file in Obsidian or a plain
  text editor and have it make sense).

## 6. Log the run in `session-notes.md`

This step is mandatory in **both** modes, every time this skill runs. Append
(never overwrite or delete prior entries) a new entry to `session-notes.md`
at the project root, creating the file with a top-level `# Session Notes`
heading if it doesn't exist yet. Each entry must include:

- **Date** — today's date.
- **Mode** — `create` or `update`.
- **Prompt** — the user's prompt that triggered this run, verbatim or
  close to it.
- **Summary** — how many repos were processed, which pages were created
  (list the slugs), and whether the index was written fresh or updated.
- **Issues/corrections** — anything notable: a `raw/` file with no matching
  manifest entry, an excluded entry found in `raw/` unexpectedly, a README
  that was too sparse/short to summarize meaningfully (and how you handled
  it), or any other judgment call worth recording for future runs.

A suggested entry format:

```markdown
## 2026-07-03 — update

**Prompt:** "update the wiki with the new repos"

**Summary:** Processed 3 new repos (foo__bar, baz__qux, a__b). Created
wiki/foo__bar.md, wiki/baz__qux.md, wiki/a__b.md. Updated wiki/index.md
to add entries under "Frameworks" and "Memory".

**Issues:** raw/orphan__repo.md had no matching manifest.json entry —
skipped, not written to the wiki.
```
