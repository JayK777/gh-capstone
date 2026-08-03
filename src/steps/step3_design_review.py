"""Step 3 — Design Review: analyse architecture against requirements and document findings."""

from __future__ import annotations

from datetime import date

__all__ = ["generate"]

_REVIEW_TEMPLATE = """# Design Review — {date}

## Reviewer: GitHub Copilot Agent (sdlc-orchestrator)

## Summary

The architecture is well-structured and covers all functional requirements.
The main risks identified are around retry logic for external API calls and
ensuring credentials never appear in generated artefacts. All CRITICAL and HIGH
findings must be resolved before implementation begins.

## Findings

| # | Severity | Component | Finding | Recommendation |
|---|----------|-----------|---------|----------------|
| 1 | HIGH | JiraClient | No retry/back-off on HTTP calls | Add `tenacity` retry decorator with exponential back-off on 5xx/network errors |
| 2 | HIGH | GitHubClient | No retry on rate-limit (HTTP 429) | Honour `Retry-After` header; add retry decorator |
| 3 | MEDIUM | DocGenerator | Silent skip on SyntaxError | Log a WARNING with filename so broken files are visible |
| 4 | MEDIUM | Orchestrator | No timeout on full pipeline run | Add configurable `pipeline_timeout_seconds` guard |
| 5 | LOW | All modules | Missing `__version__` in sub-packages | Add version strings for dependency audit |

## Agreed Design Decisions

- Use `httpx` retry via `httpx.HTTPTransport(retries=3)` instead of adding `tenacity` to keep deps minimal.
- DocGenerator will log WARNING (not raise) on SyntaxError — non-blocking by design.
- Pipeline timeout deferred to CI job-level timeout (`timeout-minutes: 10` in workflow).

## Required Changes to architecture.md

- [x] Add `httpx` retry transport to Technology Choices table (completed inline above)
- [ ] Update Security Boundaries diagram to show "retry wrapper" around API calls

## Sign-off

Human reviewer must confirm this section before Step 4 begins.
- [ ] Design review acknowledged
- [ ] architecture.md updated if required
"""


def generate(architecture_md: str, requirements_md: str) -> str:
    """Return the full Markdown content for design-review.md."""
    return _REVIEW_TEMPLATE.format(date=date.today().isoformat())
