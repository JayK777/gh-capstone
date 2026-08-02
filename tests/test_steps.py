"""Tests for src/steps/ modules."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.pipeline.jira_client import JiraStory
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


# ── Step 1 ────────────────────────────────────────────────────────────────────

def test_step1_generate(sample_jira_raw: dict) -> None:
    story = JiraStory(sample_jira_raw)
    md = step1_requirements.generate(story)
    assert "## Functional Requirements" in md
    assert "## Acceptance Criteria" in md
    assert story.id in md


# ── Step 2 ────────────────────────────────────────────────────────────────────

def test_step2_generate() -> None:
    md = step2_architecture.generate("some requirements")
    assert "```mermaid" in md
    assert "graph TD" in md


# ── Step 3 ────────────────────────────────────────────────────────────────────

def test_step3_generate() -> None:
    md = step3_design_review.generate("arch text", "reqs text")
    assert "## Findings" in md
    assert "Severity" in md


# ── Step 4 ────────────────────────────────────────────────────────────────────

def test_step4_generate() -> None:
    md = step4_impl_plan.generate("arch text", "review text")
    assert "TASK-001" in md
    assert "## Task List" in md


# ── Step 5 ────────────────────────────────────────────────────────────────────

def test_step5_record(tmp_path: Path) -> None:
    written = [tmp_path / "docs" / "api" / "mod.md"]
    updated = step5_implementation.record("# Plan\n", written)
    assert "Implementation Log" in updated
    assert "mod.md" in updated


# ── Step 6 ────────────────────────────────────────────────────────────────────

def test_step6_run_no_issues(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "clean.py").write_text('"""Clean module."""\n\ndef hello() -> str:\n    """Return hi."""\n    return "hi"\n')
    docs = tmp_path / "docs"
    findings = step6_review.run(src, docs)
    assert findings == []


def test_step6_detects_bare_except(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "bad.py").write_text("try:\n    pass\nexcept:\n    pass\n")
    docs = tmp_path / "docs"
    findings = step6_review.run(src, docs)
    assert any("bare except" in f for f in findings)


# ── Step 7 ────────────────────────────────────────────────────────────────────

def test_step7_run_no_tests(tmp_path: Path) -> None:
    empty_tests = tmp_path / "tests"
    empty_tests.mkdir()
    report = step7_verify.run(empty_tests)
    assert report.total == 0
    assert report.success is True


def test_step7_append_report() -> None:
    from src.steps.step7_verify import TestReport
    report = TestReport("2026-08-02T00:00:00Z", 10, 10, 0, 0, "90%", "all passed", True)
    updated = step7_verify.append_report("# Design Review\n", report)
    assert "Verification Report" in updated
    assert "90%" in updated


# ── Step 8 ────────────────────────────────────────────────────────────────────

def test_step8_make_branch_name() -> None:
    name = step8_pr.make_branch_name("DOCS-42", "Automate docs sync feature")
    assert name.startswith("feature/docs-42-")
    assert " " not in name


def test_step8_build_pr_body(sample_jira_raw: dict, tmp_path: Path) -> None:
    story = JiraStory(sample_jira_raw)
    docs = tmp_path / "docs"
    docs.mkdir()
    body = step8_pr.build_pr_body(story, docs, [("docs/requirements.md", "# Req")])
    assert "## Summary" in body
    assert "## Reviewer Checklist" in body
    assert story.id in body
