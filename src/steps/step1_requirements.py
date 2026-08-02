"""Step 1 — Requirements: generate docs/requirements.md from a JiraStory."""

from __future__ import annotations

from datetime import date

from src.pipeline.jira_client import JiraStory

__all__ = ["generate"]


def generate(story: JiraStory) -> str:
    """Return the full Markdown content for requirements.md."""
    today = date.today().isoformat()
    ac_block = "\n".join(f"- AC-{i+1:02d}: {ac}" for i, ac in enumerate(story.acceptance_criteria))
    labels = ", ".join(story.labels) if story.labels else "None"

    return f"""# Requirements — {story.title}

> Generated: {today} | JIRA: {story.id} | Priority: {story.priority} | Story Points: {story.story_points}

## User Story
**{story.id}**: {story.title}

{story.description}

## Functional Requirements

- FR-01: The system shall fetch the JIRA user story identified by `{story.id}` and parse its fields.
- FR-02: The system shall scan all Python source files and extract module, class, and function docstrings.
- FR-03: The system shall generate a Markdown documentation file for each discovered module under `docs/api/`.
- FR-04: The system shall maintain a `docs/api_index.md` listing all generated module docs.
- FR-05: The system shall create a feature branch, push all generated artefacts, and open a GitHub PR.

## Non-Functional Requirements

- NFR-01: **Performance** — The full pipeline must complete within 120 seconds for a repository containing ≤ 500 Python files.
- NFR-02: **Security** — No credentials shall appear in generated documents, logs, or committed files.
- NFR-03: **Reliability** — All external API calls (JIRA, GitHub) shall retry up to 3 times on transient failure before raising.
- NFR-04: **Maintainability** — Each pipeline step is encapsulated in its own module; no step exceeds 200 lines.
- NFR-05: **Observability** — The pipeline emits structured log messages at INFO level for each step start/end.

## Acceptance Criteria

{ac_block}

## Labels
{labels}

## Out of Scope

- Confluence page sync
- Automatic code generation from requirements
- Non-Python source file parsing
"""
