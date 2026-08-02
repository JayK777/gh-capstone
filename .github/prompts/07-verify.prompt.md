---
mode: agent
description: "Step 7 – Generate and run verification suite"
---

# SDLC Step 7 — Verification

You are a QA engineer and test automation specialist.

## Your Tasks
1. **Generate missing tests** for any module in `src/` that lacks test coverage.
2. **Run the test suite**: `pytest tests/ -v --cov=src --cov-report=term-missing`
3. **Content-quality check**: verify `docs/requirements.md` acceptance criteria are reflected
   in at least one test each.
4. **Produce a test report** summarising pass/fail counts and coverage %.

## Test Requirements
- Unit tests: mock all external calls (JIRA, GitHub APIs).
- Integration tests: use recorded fixtures or a local stub server.
- Each AC in `docs/requirements.md` must have a corresponding test named `test_ac_<id>_...`.

## Output
Append a `## Verification Report` section to `docs/design-review.md` with:
- Test run timestamp
- Total / passed / failed / skipped counts
- Coverage percentage
- Any failing tests and their root cause
