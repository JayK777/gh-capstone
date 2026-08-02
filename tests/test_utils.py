"""Tests for src/pipeline/utils.py."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from src.pipeline.utils import ensure_dir, get_env, read_doc, write_doc


def test_get_env_returns_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_VAR", "hello")
    assert get_env("TEST_VAR") == "hello"


def test_get_env_raises_on_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MISSING_VAR", raising=False)
    with pytest.raises(EnvironmentError, match="MISSING_VAR"):
        get_env("MISSING_VAR")


def test_ensure_dir_creates_nested(tmp_path: Path) -> None:
    nested = tmp_path / "a" / "b" / "c"
    result = ensure_dir(nested)
    assert result.is_dir()


def test_write_and_read_doc(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    write_doc(docs, "test.md", "# Hello")
    content = read_doc(docs, "test.md")
    assert content == "# Hello"


def test_read_doc_raises_on_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="no_such_file.md"):
        read_doc(tmp_path, "no_such_file.md")
