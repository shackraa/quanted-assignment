# What I'd Improve With More Time

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
- **A Karpathy-LLM-Wiki-inspired `lint` mode for the skill**, checking for broken
  `[[wikilinks]]` and index/orphan consistency, is a natural next step once the vault
  grows beyond a couple dozen pages — not implemented now since at this scale manual
  review already covers it.
- **A self-verification step for status-type claims in the skill.** After writing each
  wiki page, the skill would re-check its own status-type claims (archived/deprecated/
  actively maintained/etc.) against the raw README content before finishing. If a claim
  isn't directly supported by the README text, it would flag the page with a
  `needs_review` frontmatter field instead of silently asserting it. The motivating
  example is real: the `daytonaio/daytona` page was written describing the repo as
  "archived," which overstated the README — development had moved to a private
  codebase, but the repo wasn't GitHub-archived — and it was only caught by manual
  review, logged as a correction in `session-notes.md`. A self-check pass would let the
  skill catch this itself instead of relying on a human to notice.
