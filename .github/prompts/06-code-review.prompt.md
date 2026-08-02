---
mode: ask
description: "Step 6 – Structured code review against requirements"
---

# SDLC Step 6 — Code Review

You are a senior peer reviewer. Review **all files changed** in the current working branch.

## Review Checklist
| Area | Question |
|------|---------|
| Correctness | Does each component behave as specified in `docs/requirements.md`? |
| Security | Are secrets excluded from output? Is user input validated? |
| Error Handling | Are all API failures, missing files, and empty repos handled gracefully? |
| Test Coverage | Do tests cover happy path AND edge cases (missing fields, 404, empty)? |
| Code Clarity | Are function names self-explanatory? Is logic easy to follow? |
| DRY | Is there duplicated logic that should be refactored into a shared helper? |
| Dependency Safety | Flag any known-vulnerable package versions in `requirements.txt`. |

## Output
Produce a review comment for each finding. End with:
```markdown
## Review Verdict
- [ ] Approved
- [ ] Approved with minor comments
- [ ] Changes requested
```
List any **blocking** issues that must be fixed before merging.
