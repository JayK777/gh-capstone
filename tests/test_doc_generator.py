"""Tests for src/pipeline/doc_generator.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.pipeline.doc_generator import (
    DocEntry,
    render_module_doc,
    scan_source_tree,
    sync_docs,
)


def test_ac_05_scan_finds_docstrings(tmp_src: Path) -> None:
    """AC-05: scan_source_tree extracts docstrings from .py files."""
    entries = scan_source_tree(tmp_src)
    names = {e.name for e in entries}
    assert "sample" in names or any("sample" in e.module for e in entries)


def test_render_module_doc_no_entries() -> None:
    md = render_module_doc([], "some.module")
    assert "No documentation found" in md


def test_render_module_doc_with_entries() -> None:
    entry = DocEntry("my.module", "function", "greet", "Return a greeting.", 5, "greet(name)")
    md = render_module_doc([entry], "my.module")
    assert "greet" in md
    assert "Return a greeting." in md


def test_ac_05_sync_docs_writes_api_index(tmp_src: Path, tmp_docs: Path) -> None:
    """AC-05: sync_docs writes api_index.md."""
    written = sync_docs(tmp_src, tmp_docs)
    paths = [str(p) for p in written]
    assert any("api_index.md" in p for p in paths)


def test_syntax_error_skipped(tmp_path: Path, tmp_docs: Path) -> None:
    """DocGenerator skips files with SyntaxErrors instead of crashing."""
    bad_src = tmp_path / "bad_src"
    bad_src.mkdir()
    (bad_src / "broken.py").write_text("def (: pass", encoding="utf-8")
    entries = scan_source_tree(bad_src)
    assert entries == []  # nothing extracted — no crash
