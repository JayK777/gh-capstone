# Skill: PR Writer

## Purpose
Produce a complete, informative GitHub Pull Request description that enables reviewers
to quickly understand, test, and merge the change.

## PR Title Format
`[<JIRA-ID>] <imperative-verb> <concise description>`
Example: `[DOCS-42] Add automated documentation sync pipeline`

## Required Sections (never omit any)

### Summary
2-3 sentences answering:
- What was built?
- Why was it built? (link to user story)
- What is the user impact?

### Changes Made
Table with columns: File | Change Type (Added/Modified/Deleted) | Reason

### SDLC Artefacts
Links to all docs produced during this SDLC cycle.

### Test Evidence
- Paste full `pytest` output (truncate to last 50 lines if long)
- State coverage % explicitly

### Known Limitations
- Anything marked "Not Found" during implementation
- Out-of-scope items from `docs/requirements.md`
- Technical debt deliberately deferred

### Reviewer Checklist
A tick-list; reviewers must check every box before approving:
- [ ] Requirements satisfied
- [ ] Architecture followed
- [ ] All tests passing
- [ ] No secrets in diff (`git log --diff-filter=A -p | grep -i 'secret\|password\|token'`)
- [ ] CHANGELOG updated
- [ ] Docs updated

## Style Rules
- Use past tense for "Changes Made" (e.g., "Added", not "Add")
- Keep "Summary" under 100 words
- Every row in "Changes Made" must have a non-empty "Reason"
