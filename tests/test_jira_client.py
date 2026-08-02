"""Tests for src/pipeline/jira_client.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.pipeline.jira_client import JiraClient, JiraStory, _extract_ac, _map_priority


# ── JiraStory unit tests ──────────────────────────────────────────────────────

def test_jira_story_parses_fields(sample_jira_raw: dict) -> None:
    story = JiraStory(sample_jira_raw)
    assert story.id == "DOCS-42"
    assert story.title == "Automate documentation sync"
    assert story.priority == "P1"
    assert story.story_points == 5
    assert "automation" in story.labels


def test_jira_story_defaults_on_none() -> None:
    raw = {"key": "X-1", "fields": {"summary": "Test", "description": None, "priority": {"name": "Medium"}}}
    story = JiraStory(raw)
    assert story.description == "No description provided."
    assert story.story_points == 0
    assert story.priority == "P2"


def test_jira_story_to_dict(sample_jira_raw: dict) -> None:
    story = JiraStory(sample_jira_raw)
    d = story.to_dict()
    assert set(d.keys()) == {"id", "title", "description", "acceptance_criteria", "story_points", "priority", "labels"}


# ── AC extraction ─────────────────────────────────────────────────────────────

def test_extract_ac_from_given_when_then() -> None:
    desc = "Some intro.\nGiven a file When run Then docs updated.\nOther text."
    acs = _extract_ac(desc)
    assert any("Given" in ac for ac in acs)


def test_extract_ac_fallback_on_no_gwt() -> None:
    acs = _extract_ac("No criteria here at all.")
    assert len(acs) == 1
    assert "not explicitly defined" in acs[0]


# ── Priority mapping ──────────────────────────────────────────────────────────

def test_map_priority_known() -> None:
    assert _map_priority("High") == "P1"
    assert _map_priority("Highest") == "P0"
    assert _map_priority("Low") == "P3"


def test_map_priority_unknown_defaults_p2() -> None:
    assert _map_priority("SomethingWeird") == "P2"


# ── JiraClient HTTP calls ─────────────────────────────────────────────────────

def test_ac_01_jira_client_get_story_success(sample_jira_raw: dict) -> None:
    """AC-01: get_story returns JiraStory on 200."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = sample_jira_raw
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.return_value = mock_resp
        mock_client_cls.return_value = mock_client

        client = JiraClient()
        story = client.get_story("DOCS-42")

    assert story.id == "DOCS-42"


def test_jira_client_get_story_404() -> None:
    """get_story propagates HTTP errors."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404", request=MagicMock(), response=MagicMock(status_code=404)
    )

    with patch("httpx.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.return_value = mock_resp
        mock_client_cls.return_value = mock_client

        client = JiraClient()
        with pytest.raises(httpx.HTTPStatusError):
            client.get_story("MISSING-999")


def test_jira_client_get_story_validates_empty_key() -> None:
    client = JiraClient()
    with pytest.raises(ValueError, match="non-empty"):
        client.get_story("")
