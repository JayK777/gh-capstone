"""JIRA client: fetch and parse user stories via the JIRA REST API v3."""

from __future__ import annotations

import os
from typing import Any

import httpx

from src.pipeline.utils import get_env

__all__ = ["JiraClient", "JiraStory"]

JIRA_API_VERSION = "3"


class JiraStory:
    """Structured representation of a JIRA issue."""

    def __init__(self, raw: dict[str, Any]) -> None:
        fields = raw.get("fields", {})
        self.id: str = raw.get("key", "UNKNOWN")
        self.title: str = fields.get("summary", "No title")
        self.description: str = _extract_description(fields.get("description"))
        self.story_points: int = int(
            fields.get("story_points") or fields.get("customfield_10016") or 0
        )
        self.priority: str = _map_priority(fields.get("priority", {}).get("name", "Medium"))
        self.labels: list[str] = fields.get("labels", [])
        self.acceptance_criteria: list[str] = _extract_ac(self.description)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "acceptance_criteria": self.acceptance_criteria,
            "story_points": self.story_points,
            "priority": self.priority,
            "labels": self.labels,
        }


class JiraClient:
    """Thin wrapper around the JIRA REST API v3."""

    def __init__(self) -> None:
        self._base_url = get_env("JIRA_BASE_URL").rstrip("/")
        self._email = get_env("JIRA_EMAIL")
        self._token = get_env("JIRA_API_TOKEN")

    def get_story(self, issue_key: str) -> JiraStory:
        """Fetch a JIRA issue by key and return a structured JiraStory."""
        if not issue_key or not issue_key.strip():
            raise ValueError("issue_key must be a non-empty string.")
        url = f"{self._base_url}/rest/api/{JIRA_API_VERSION}/issue/{issue_key.strip()}"
        with httpx.Client(timeout=30) as client:
            response = client.get(
                url,
                auth=(self._email, self._token),
                headers={"Accept": "application/json"},
            )
        response.raise_for_status()
        return JiraStory(response.json())

    def search_stories(self, jql: str, max_results: int = 50) -> list[JiraStory]:
        """Search JIRA with a JQL query and return a list of JiraStory objects."""
        if not jql or not jql.strip():
            raise ValueError("jql must be a non-empty string.")
        url = f"{self._base_url}/rest/api/{JIRA_API_VERSION}/search"
        params = {"jql": jql, "maxResults": max_results, "fields": "*all"}
        with httpx.Client(timeout=30) as client:
            response = client.get(
                url,
                params=params,
                auth=(self._email, self._token),
                headers={"Accept": "application/json"},
            )
        response.raise_for_status()
        issues = response.json().get("issues", [])
        return [JiraStory(issue) for issue in issues]


# ── private helpers ──────────────────────────────────────────────────────────

def _extract_description(description: Any) -> str:
    """Extract plain text from an Atlassian Document Format (ADF) description."""
    if description is None:
        return "No description provided."
    if isinstance(description, str):
        return description

    # ADF: walk content tree and concatenate text nodes
    parts: list[str] = []
    _walk_adf(description, parts)
    return " ".join(parts) if parts else "No description provided."


def _walk_adf(node: Any, parts: list[str]) -> None:
    if not isinstance(node, dict):
        return
    if node.get("type") == "text":
        parts.append(node.get("text", ""))
    for child in node.get("content", []):
        _walk_adf(child, parts)


def _map_priority(name: str) -> str:
    mapping = {"Highest": "P0", "High": "P1", "Medium": "P2", "Low": "P3", "Lowest": "P4"}
    return mapping.get(name, "P2")


def _extract_ac(description: str) -> list[str]:
    """Extract Given/When/Then lines from a description string."""
    criteria: list[str] = []
    for line in description.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if lower.startswith("given ") or lower.startswith("when ") or lower.startswith("then "):
            criteria.append(stripped)
    return criteria or ["(Acceptance criteria not explicitly defined — see description.)"]
