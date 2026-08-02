"""Step 5 — Implementation: record doc-sync results into the impl-plan."""

from __future__ import annotations

from pathlib import Path

__all__ = ["record"]


def record(impl_plan_md: str, written_paths: list[Path]) -> str:
    """
    Append a completion note to impl-plan_md listing files written by DocGenerator.
    Returns the updated plan text (caller must persist it).
    """
    files_list = "\n".join(f"  - `{p}`" for p in written_paths)
    note = f"""

## Implementation Log — DocGenerator Run

Files written during `sync_docs`:
{files_list}

TASK-005: ✅ complete
TASK-006: ✅ complete
"""
    return impl_plan_md + note
