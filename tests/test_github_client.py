"""Tests for src/pipeline/github_client.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.pipeline.github_client import GitHubClient, PullRequest


def _make_mock_client(responses: list[dict]) -> MagicMock:
    """Build a mock httpx.Client context manager returning responses in order."""
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)

    mock_responses = []
    for data in responses:
        resp = MagicMock()
        resp.json.return_value = data
        resp.raise_for_status = MagicMock()
        mock_responses.append(resp)

    mock_client.get.side_effect = mock_responses[:2] if mock_responses else []
    mock_client.post.return_value = mock_responses[-1] if mock_responses else MagicMock()
    mock_client.put.return_value = mock_responses[-1] if mock_responses else MagicMock()
    return mock_client


def test_ac_06_create_pull_request_returns_pr() -> None:
    """AC-06: create_pull_request returns a PullRequest with url."""
    pr_data = {"number": 7, "html_url": "https://github.com/owner/repo/pull/7", "title": "Test PR", "state": "open"}

    with patch("httpx.Client") as mock_client_cls:
        mock_client = _make_mock_client([pr_data])
        mock_client_cls.return_value = mock_client

        gh = GitHubClient()
        pr = gh.create_pull_request("Test PR", "body", "feature/test", "main")

    assert pr.number == 7
    assert "pull/7" in pr.url


def test_pull_request_str() -> None:
    pr = PullRequest({"number": 1, "html_url": "https://github.com/x/y/pull/1", "title": "Hi", "state": "open"})
    assert "PR #1" in str(pr)


def test_create_pull_request_validates_empty_title() -> None:
    gh = GitHubClient()
    with pytest.raises(ValueError, match="title"):
        gh.create_pull_request("", "body", "branch")


def test_missing_env_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(EnvironmentError, match="GITHUB_TOKEN"):
        GitHubClient()
