"""GitHub client: create branches, push files, and open pull requests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from src.pipeline.utils import get_env

__all__ = ["GitHubClient", "PullRequest"]

GITHUB_API = "https://api.github.com"
ACCEPT_JSON = "application/vnd.github+json"
API_VERSION = "2022-11-28"


class PullRequest:
    """Lightweight representation of a GitHub Pull Request."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.number: int = data["number"]
        self.url: str = data["html_url"]
        self.title: str = data["title"]
        self.state: str = data["state"]

    def __str__(self) -> str:
        return f"PR #{self.number}: {self.title} — {self.url}"


class GitHubClient:
    """Wrapper around the GitHub REST API for SDLC pipeline operations."""

    def __init__(self) -> None:
        self._token = get_env("GITHUB_TOKEN")
        self._owner = get_env("GITHUB_OWNER")
        self._repo = get_env("GITHUB_REPO")

    # ── branch ───────────────────────────────────────────────────────────────

    def get_default_branch_sha(self) -> str:
        """Return the HEAD SHA of the repository's default branch."""
        data = self._get(f"/repos/{self._owner}/{self._repo}")
        default_branch = data["default_branch"]
        ref_data = self._get(f"/repos/{self._owner}/{self._repo}/git/ref/heads/{default_branch}")
        return ref_data["object"]["sha"]

    def create_branch(self, branch_name: str, from_sha: str) -> str:
        """Create a new branch and return its name."""
        if not branch_name or not from_sha:
            raise ValueError("branch_name and from_sha are required.")
        self._post(
            f"/repos/{self._owner}/{self._repo}/git/refs",
            {"ref": f"refs/heads/{branch_name}", "sha": from_sha},
        )
        return branch_name

    # ── file push ─────────────────────────────────────────────────────────────

    def push_file(self, branch: str, file_path: str, content: str, message: str) -> None:
        """Create or update a file on the given branch."""
        import base64

        encoded = base64.b64encode(content.encode()).decode()
        url = f"/repos/{self._owner}/{self._repo}/contents/{file_path}"

        # Check if file already exists (need its SHA to update)
        existing_sha: str | None = None
        try:
            existing = self._get(f"{url}?ref={branch}")
            existing_sha = existing.get("sha")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code != 404:
                raise

        payload: dict[str, Any] = {
            "message": message,
            "content": encoded,
            "branch": branch,
        }
        if existing_sha:
            payload["sha"] = existing_sha

        self._put(url, payload)

    # ── pull request ──────────────────────────────────────────────────────────

    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> PullRequest:
        """Open a new pull request and return the PullRequest object."""
        if not title or not head_branch:
            raise ValueError("title and head_branch are required.")
        data = self._post(
            f"/repos/{self._owner}/{self._repo}/pulls",
            {
                "title": title,
                "body": body,
                "head": head_branch,
                "base": base_branch,
                "draft": False,
            },
        )
        return PullRequest(data)

    # ── private HTTP helpers ──────────────────────────────────────────────────

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": ACCEPT_JSON,
            "X-GitHub-Api-Version": API_VERSION,
        }

    def _get(self, path: str) -> dict[str, Any]:
        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{GITHUB_API}{path}", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{GITHUB_API}{path}", json=payload, headers=self._headers()
            )
        resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        with httpx.Client(timeout=30) as client:
            resp = client.put(
                f"{GITHUB_API}{path}", json=payload, headers=self._headers()
            )
        resp.raise_for_status()
        return resp.json()
