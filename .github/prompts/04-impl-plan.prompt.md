---
mode: ask
description: "Step 4 – Create dependency-ordered implementation plan"
---

# SDLC Step 4 — Implementation Planning

You are a technical lead.

## Your Task
Read `docs/architecture.md` and `docs/design-review.md`, then produce `docs/impl-plan.md`.

## Rules
- Tasks must be ordered by **dependency** (no task starts before its blocker finishes).
- Each task gets a unique ID (TASK-001, TASK-002 …).
- Estimate effort in **story points** (1 / 2 / 3 / 5 / 8).
- Flag **blocked** tasks explicitly.

## Output Format for `docs/impl-plan.md`
```markdown
# Implementation Plan

## Summary
Total tasks: N | Total story points: SP

## Task List
| ID | Title | Depends On | Points | Blocked? |
|----|-------|-----------|--------|----------|

## Task Details

### TASK-001 — <title>
**Description**: ...  
**Files to create/modify**: ...  
**Acceptance**: ...
```
