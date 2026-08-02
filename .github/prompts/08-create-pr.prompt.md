---
mode: agent
description: "Step 8 – Create GitHub PR with full agentic SDLC description"
---

# SDLC Step 8 — Create Pull Request

You are the release engineer completing the agentic SDLC cycle.

## Your Tasks
1. Ensure all SDLC artefacts are committed: `requirements.md`, `architecture.md`,
   `design-review.md`, `impl-plan.md`.
2. Create a feature branch named `feature/<jira-story-id>-<slug>` if not already on one.
3. Push the branch and open a PR against `main`.

## Required PR Description Sections
Generate ALL of the following:

```markdown
## Summary
<2-3 sentences: what was built and why>

## Changes Made
| File | Change Type | Reason |
|------|-------------|--------|
...

## SDLC Artefacts
- [requirements.md](docs/requirements.md)
- [architecture.md](docs/architecture.md)
- [design-review.md](docs/design-review.md)
- [impl-plan.md](docs/impl-plan.md)

## Test Evidence
\`\`\`
<paste pytest output>
\`\`\`
Coverage: XX%

## Known Limitations
- ...

## Reviewer Checklist
- [ ] Requirements satisfied (see `docs/requirements.md`)
- [ ] Architecture followed (see `docs/architecture.md`)
- [ ] All tests passing
- [ ] No secrets in diff
- [ ] CHANGELOG updated
- [ ] Docs updated
```

## Inputs
- JIRA Story ID: {{JIRA_STORY_ID}}
- Branch: {{FEATURE_BRANCH}}
