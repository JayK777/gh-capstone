# Skill: JIRA Story Analyst

## Purpose
Teach Copilot how to read and decompose a JIRA User Story into structured requirements.

## Input Format (JIRA REST API v3 response or plain text)
A JIRA issue contains:
- `summary` — one-line title
- `description` — Atlassian Document Format (ADF) or plain text
- `acceptance_criteria` — custom field or embedded in description
- `story_points` — custom field (e.g. `story_points`, `customfield_10016`)
- `labels`, `components`, `priority`

## How to Parse
1. Extract `summary` as the story title.
2. Walk `description.content[]` (ADF) and concatenate all `text` nodes.
3. Look for sections headed **Acceptance Criteria**, **AC**, or **Given/When/Then**.
4. If no explicit AC section, infer criteria from the "so that" clause of the story.
5. Map `priority` → NFR severity: `Highest`=P0, `High`=P1, `Medium`=P2, `Low`=P3.

## Output
A structured dict:
```python
{
  "id": "PROJ-123",
  "title": "...",
  "description": "...",
  "acceptance_criteria": ["Given … When … Then …"],
  "story_points": 5,
  "priority": "P1",
  "labels": []
}
```

## Edge Cases
- If `description` is None → set `"description": "No description provided"`.
- If `story_points` is None → set to 0.
- If ADF parsing fails → fall back to raw text via `str(description)`.
