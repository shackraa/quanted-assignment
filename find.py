"""Thin wrapper so `python find.py` keeps working.

The real implementation lives in src/quanted_pipeline/find.py. `quanted_pipeline`
is installed in editable mode via `uv sync` (see pyproject.toml), so this is a
normal import -- no sys.path manipulation needed.
"""

from __future__ import annotations

from quanted_pipeline.find import main

if __name__ == "__main__":
    main()
