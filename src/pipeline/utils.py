"""Shared utility functions used across pipeline steps."""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["get_env", "ensure_dir", "write_doc", "read_doc"]


def get_env(key: str) -> str:
    """Return an environment variable value; raise if missing or empty."""
    value = os.environ.get(key, "").strip()
    if not value:
        raise EnvironmentError(f"Required environment variable '{key}' is not set.")
    return value


def ensure_dir(path: Path) -> Path:
    """Create directory (and parents) if it doesn't exist; return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_doc(docs_root: Path, filename: str, content: str) -> Path:
    """Write content to docs_root/filename, creating dirs as needed."""
    ensure_dir(docs_root)
    target = docs_root / filename
    target.write_text(content, encoding="utf-8")
    return target


def read_doc(docs_root: Path, filename: str) -> str:
    """Read and return the text of docs_root/filename."""
    target = docs_root / filename
    if not target.exists():
        raise FileNotFoundError(f"SDLC artefact not found: {target}")
    return target.read_text(encoding="utf-8")
