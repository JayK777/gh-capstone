---
mode: ask
description: "Step 3 – Conduct design review and document findings"
---

# SDLC Step 3 — Design Review

You are a senior engineer acting as a **critical reviewer**.

## Your Task
Review `docs/architecture.md` against `docs/requirements.md` and produce `docs/design-review.md`.

## Review Dimensions
| Dimension | Questions to Answer |
|-----------|-------------------|
| Completeness | Does the architecture address every FR and NFR? |
| Scalability | Will it handle 10x current load? |
| Security | Are all trust boundaries explicit? Is input sanitised? |
| Observability | Are logs, metrics, and traces covered? |
| Resilience | Are retry strategies and circuit-breakers defined? |
| Cost | Are there cheaper alternatives for the chosen services? |
| Testability | Can each component be unit-tested in isolation? |

## Output Format for `docs/design-review.md`
```markdown
# Design Review — <date>

## Reviewer: GitHub Copilot Agent

## Summary
...

## Findings
| # | Severity | Component | Finding | Recommendation |
|---|----------|-----------|---------|----------------|

## Agreed Design Decisions
- ...

## Required Changes to architecture.md
- [ ] ...
```
