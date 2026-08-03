"""JIRA client: fetch and parse user stories via JIRA REST API v2."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import httpx

from src.pipeline.utils import get_env

__all__ = ["JiraClient", "JiraStory"]


@dataclass
class JiraStory:
    """Parsed representation of a JIRA user story."""

    id: str
    title: str
    description: str
    acceptance_criteria: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    priority: str = "Medium"
    story_points: int | None = None
    status: str = "Open"


class JiraClient:
    """Wrapper around the JIRA REST API v2 for fetching user stories."""

    # Common custom field names used for story points across JIRA instances
    _SP_FIELDS = ("story_points", "customfield_10016", "customfield_10028")

    def __init__(self) -> None:
        self._base_url = get_env("JIRA_BASE_URL").rstrip("/")
        self._email = get_env("JIRA_EMAIL")
        self._token = get_env("JIRA_API_TOKEN")
        self._client = httpx.Client(
            auth=(self._email, self._token),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            timeout=30.0,
        )

    # ── public API ────────────────────────────────────────────────────────────

    def get_story(self, issue_key: str) -> JiraStory:
        """Fetch a JIRA issue and return a JiraStory."""
        data = self._get(f"/rest/api/2/issue/{issue_key}")
        return self._parse(data)

    # ── internal helpers ──────────────────────────────────────────────────────

    def _get(self, path: str) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()

    def _parse(self, data: dict[str, Any]) -> JiraStory:
        fields: dict[str, Any] = data.get("fields", {})
        key: str = data["key"]
        title: str = fields.get("summary", "")
        raw_desc: str = _coerce_description(fields.get("description") or "")

        # Parse acceptance criteria section from description
        ac = _extract_acceptance_criteria(raw_desc)

        # Story points — check known custom field names
        sp: int | None = None
        for cf in self._SP_FIELDS:
            val = fields.get(cf)
            if val is not None:
                try:
                    sp = int(val)
                except (TypeError, ValueError):
                    pass
                break

        priority_obj = fields.get("priority") or {}
        priority: str = priority_obj.get("name", "Medium") if isinstance(priority_obj, dict) else "Medium"

        status_obj = fields.get("status") or {}
        status: str = status_obj.get("name", "Open") if isinstance(status_obj, dict) else "Open"

        labels: list[str] = fields.get("labels") or []

        return JiraStory(
            id=key,
            title=title,
            description=raw_desc,
            acceptance_criteria=ac,
            labels=labels,
            priority=priority,
            story_points=sp,
            status=status,
        )


# ── description helpers ───────────────────────────────────────────────────────

def _coerce_description(raw: Any) -> str:
    """Return description as plain text, handling both string (wiki) and ADF (dict) formats."""
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, dict):
        # ADF (Atlassian Document Format) — extract plain text recursively
        return _adf_to_text(raw).strip()
    return ""


def _adf_to_text(node: dict[str, Any]) -> str:
    """Recursively extract plain text from an ADF node."""
    node_type = node.get("type", "")
    texts: list[str] = []

    if node_type == "text":
        return node.get("text", "")

    for child in node.get("content", []):
        texts.append(_adf_to_text(child))

    sep = "\n" if node_type in ("paragraph", "bulletList", "orderedList", "listItem", "doc") else ""
    return sep.join(texts)


def _extract_acceptance_criteria(description: str) -> list[str]:
    """
    Pull acceptance criteria bullets from the description.
    Handles both wiki markup (*Acceptance Criteria*) and plain headers (## Acceptance Criteria).
    Falls back to an empty list if no section is found.
    """
    # Look for an "Acceptance Criteria" section header (case-insensitive)
    section_pattern = re.compile(
        r"(?:^\*?acceptance criteria\*?|^#+\s*acceptance criteria)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = section_pattern.search(description)
    if not match:
        return []

    section_text = description[match.end():]

    # Collect bullet lines until the next section header or end
    criteria: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        # Stop at the next section header
        if re.match(r"^(\*[A-Z]|\#{1,3}\s+[A-Z])", stripped):
            break
        # Capture bullet items (-, *, #)
        bullet = re.match(r"^[-*#]\s+(.+)", stripped)
        if bullet:
            criteria.append(bullet.group(1).strip())

    return criteria
