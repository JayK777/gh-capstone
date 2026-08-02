"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def _set_required_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure all required env vars are present for every test."""
    monkeypatch.setenv("JIRA_BASE_URL", "https://example.atlassian.net")
    monkeypatch.setenv("JIRA_EMAIL", "test@example.com")
    monkeypatch.setenv("JIRA_API_TOKEN", "fake-token")
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_faketoken1234567890123456789012345678")
    monkeypatch.setenv("GITHUB_OWNER", "test-owner")
    monkeypatch.setenv("GITHUB_REPO", "test-repo")


@pytest.fixture()
def tmp_docs(tmp_path: Path) -> Path:
    """Return a temporary docs/ directory."""
    docs = tmp_path / "docs"
    docs.mkdir()
    return docs


@pytest.fixture()
def tmp_src(tmp_path: Path) -> Path:
    """Return a temporary src/ directory with a sample Python module."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "sample.py").write_text(
        '''"""Sample module for testing DocGenerator."""

def hello(name: str) -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"
''',
        encoding="utf-8",
    )
    return src


@pytest.fixture()
def sample_jira_raw() -> dict:
    """A minimal raw JIRA issue dict."""
    return {
        "key": "DOCS-42",
        "fields": {
            "summary": "Automate documentation sync",
            "description": {
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Given a source file When docs run Then docs/api/ is updated."}
                        ],
                    }
                ],
            },
            "priority": {"name": "High"},
            "story_points": 5,
            "labels": ["automation", "docs"],
        },
    }
