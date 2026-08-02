# Skill: Requirements Writer

## Purpose
Transform a structured JIRA story (from the jira-analyst skill) into a complete
`docs/requirements.md` that satisfies the requirements.instructions.md rules.

## Process
1. **Clarify** — list questions Copilot should ask the user before writing (see prompt 01).
2. **Write FR** — one FR per story acceptance criterion; add inferred FRs for implicit behaviour.
3. **Write NFR** — derive from priority, labels (e.g. `security`, `performance`), and ACs.
4. **Write AC** — rewrite each criterion in strict Given/When/Then form.
5. **Out of Scope** — explicitly state what is NOT in this story.

## Quality Gates
- Every FR must be testable (avoid "should be fast" → use "must respond within 500 ms").
- Every AC must map to exactly one FR.
- No requirement contains the word "easy" or "simple" (too vague).

## Template Variables
- `{{STORY_ID}}` — JIRA issue key
- `{{STORY_TITLE}}` — issue summary
- `{{DATE}}` — today's date (ISO 8601)
