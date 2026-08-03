"""
orchestrator.py
~~~~~~~~~~~~~~~
Main SDLC Pipeline Orchestrator.

Drives the full 8-step lifecycle from a JIRA story to a GitHub PR.
Each step can also be run independently via the run_step() method.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from src.pipeline.doc_generator import sync_docs
from src.pipeline.github_client import GitHubClient, PullRequest
from src.pipeline.jira_client import JiraClient, JiraStory
from src.pipeline.utils import ensure_dir, read_doc, write_doc
from src.steps import (
    step1_requirements,
    step2_architecture,
    step3_design_review,
    step4_impl_plan,
    step5_implementation,
    step6_review,
    step7_verify,
    step8_pr,
)

__all__ = ["PipelineConfig", "SDLCOrchestrator"]

log = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Runtime configuration for the SDLC pipeline."""

    jira_story_id: str
    repo_root: Path = Path(".")
    docs_root: Path = field(default_factory=lambda: Path("docs"))
    src_root: Path = field(default_factory=lambda: Path("src"))
    tests_root: Path = field(default_factory=lambda: Path("tests"))
    base_branch: str = "main"
    dry_run: bool = False           # If True, skip GitHub API calls
    interactive: bool = True        # If True, pause at human-in-the-loop gates


class SDLCOrchestrator:
    """Drives the 8-step Agentic SDLC pipeline end-to-end."""

    STEPS: list[str] = [
        "requirements",
        "architecture",
        "design_review",
        "impl_plan",
        "implementation",
        "review",
        "verify",
        "pr",
    ]

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self._jira = JiraClient()
        self._github: GitHubClient | None = None if config.dry_run else GitHubClient()
        self.story: JiraStory | None = None
        self.pr_url: str | None = None

    # ── public API ────────────────────────────────────────────────────────────

    def run_all(self) -> str:
        """Execute all 8 steps in order. Returns the PR URL."""
        log.info("🚀 Starting SDLC pipeline for story: %s", self.config.jira_story_id)
        ensure_dir(self.config.docs_root)

        for step_name in self.STEPS:
            self.run_step(step_name)

        assert self.pr_url is not None
        log.info("✅ Pipeline complete. PR: %s", self.pr_url)
        return self.pr_url

    def run_step(self, step_name: str) -> None:
        """Run a single named step."""
        if step_name not in self.STEPS:
            raise ValueError(f"Unknown step: {step_name}. Valid: {self.STEPS}")

        handler: Callable[..., None] = getattr(self, f"_run_{step_name}")
        log.info("▶ Step: %s", step_name)
        handler()
        log.info("✔ Step complete: %s", step_name)

    # ── step handlers ─────────────────────────────────────────────────────────

    def _run_requirements(self) -> None:
        self.story = self._jira.get_story(self.config.jira_story_id)
        content = step1_requirements.generate(self.story)
        write_doc(self.config.docs_root, "requirements.md", content)

    def _run_architecture(self) -> None:
        reqs = read_doc(self.config.docs_root, "requirements.md")
        content = step2_architecture.generate(reqs)
        write_doc(self.config.docs_root, "architecture.md", content)

    def _run_design_review(self) -> None:
        arch = read_doc(self.config.docs_root, "architecture.md")
        reqs = read_doc(self.config.docs_root, "requirements.md")
        content = step3_design_review.generate(arch, reqs)
        write_doc(self.config.docs_root, "design-review.md", content)

    def _run_impl_plan(self) -> None:
        arch = read_doc(self.config.docs_root, "architecture.md")
        review = read_doc(self.config.docs_root, "design-review.md")
        content = step4_impl_plan.generate(arch, review)
        write_doc(self.config.docs_root, "impl-plan.md", content)

    def _run_implementation(self) -> None:
        plan = read_doc(self.config.docs_root, "impl-plan.md")
        written = sync_docs(self.config.src_root, self.config.docs_root)
        step5_implementation.record(plan, written)

    def _run_review(self) -> None:
        step6_review.run(self.config.src_root, self.config.docs_root)

    def _run_verify(self) -> None:
        report = step7_verify.run(self.config.tests_root)
        review_doc = read_doc(self.config.docs_root, "design-review.md")
        updated = step7_verify.append_report(review_doc, report)
        write_doc(self.config.docs_root, "design-review.md", updated)

    def _run_pr(self) -> None:
        if self.config.dry_run:
            self.pr_url = "https://github.com/example/repo/pull/0 (dry-run)"
            return

        assert self._github is not None
        if self.story is None:
            self.story = self._jira.get_story(self.config.jira_story_id)

        branch_name = step8_pr.make_branch_name(self.config.jira_story_id, self.story.title)
        base_branch, base_sha = self._github.get_default_branch()
        self._github.create_branch(branch_name, base_sha)

        files_to_push = step8_pr.collect_files(self.config.docs_root, self.config.src_root)
        for file_path, content in files_to_push:
            self._github.push_file(
                branch=branch_name,
                file_path=file_path,
                content=content,
                message=f"feat({self.config.jira_story_id}): add SDLC artefacts and implementation",
            )

        pr_body = step8_pr.build_pr_body(
            story=self.story,
            docs_root=self.config.docs_root,
            files_pushed=list(files_to_push),
        )
        pr_title = f"[{self.config.jira_story_id}] {self.story.title}"
        pr: PullRequest = self._github.create_pull_request(
            title=pr_title,
            body=pr_body,
            head_branch=branch_name,
            base_branch=base_branch,
        )
        self.pr_url = pr.url
