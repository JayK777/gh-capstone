"""Integration test for the full SDLC Orchestrator in dry_run mode."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.pipeline.orchestrator import PipelineConfig, SDLCOrchestrator


def _make_fake_story() -> MagicMock:
    story = MagicMock()
    story.id = "DOCS-42"
    story.title = "Automate documentation sync"
    story.description = "Given a source file When run Then docs updated."
    story.acceptance_criteria = ["Given a source file When run Then docs updated."]
    story.story_points = 5
    story.priority = "P1"
    story.labels = ["docs"]
    return story


def test_dry_run_pipeline(tmp_path: Path) -> None:
    """AC-07: dry_run=True completes without making any GitHub API calls."""
    docs = tmp_path / "docs"
    src = tmp_path / "src"
    tests = tmp_path / "tests"
    for d in (docs, src, tests):
        d.mkdir()

    # Add a sample source file so sync_docs has something to scan
    (src / "sample.py").write_text('"""Sample."""\n\ndef hello() -> str:\n    """Hi."""\n    return "hi"\n')

    config = PipelineConfig(
        jira_story_id="DOCS-42",
        repo_root=tmp_path,
        docs_root=docs,
        src_root=src,
        tests_root=tests,
        dry_run=True,
        interactive=False,
    )

    with patch("src.pipeline.orchestrator.JiraClient") as mock_jira_cls:
        mock_jira = MagicMock()
        mock_jira.get_story.return_value = _make_fake_story()
        mock_jira_cls.return_value = mock_jira

        orch = SDLCOrchestrator(config)
        pr_url = orch.run_all()

    assert "dry-run" in pr_url
    # Verify SDLC artefacts were written
    assert (docs / "requirements.md").exists()
    assert (docs / "architecture.md").exists()
    assert (docs / "design-review.md").exists()
    assert (docs / "impl-plan.md").exists()
    assert (docs / "api_index.md").exists()


def test_run_step_invalid_name(tmp_path: Path) -> None:
    config = PipelineConfig(jira_story_id="X-1", repo_root=tmp_path, dry_run=True)
    orch = SDLCOrchestrator(config)
    with pytest.raises(ValueError, match="Unknown step"):
        orch.run_step("nonexistent_step")
