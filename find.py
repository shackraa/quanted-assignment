"""Thin wrapper so `python find.py` keeps working.

The real implementation lives in src/quanted_pipeline/find.py; this wrapper
just puts src/ on sys.path and delegates, so the script stays runnable
standalone without requiring the package to be installed first.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from quanted_pipeline.find import main  # noqa: E402

if __name__ == "__main__":
    main()
