"""The 纲目 (Gangmu) AIBOM rule base, as an installable rule pack.

``gangmu aibom`` finds this package through the ``gangmu.rule_packs`` entry point and
reads the ``formats/*.yaml`` and ``runtimes/*.yaml`` in the directory :func:`path` returns. The rules are
data; the code that reads them lives in gangmu.
"""

from pathlib import Path

__version__ = "2026.10.9"


def path() -> Path:
    """The rule directory: the copy inside the wheel, or ``rules/`` in a checkout."""
    packaged = Path(__file__).resolve().parent / "data"
    if packaged.is_dir():
        return packaged
    return Path(__file__).resolve().parents[2] / "rules"
