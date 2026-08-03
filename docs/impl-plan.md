# Implementation Plan

> Generated: 2026-08-03

## Summary

Total tasks: 8 | Total story points: 21

## Task List

| ID | Title | Depends On | Points | Blocked? |
|----|-------|-----------|--------|----------|
| TASK-001 | Set up project structure & dependencies | — | 1 | No |
| TASK-002 | Implement `utils.py` shared helpers | TASK-001 | 1 | No |
| TASK-003 | Implement `JiraClient` | TASK-002 | 3 | No |
| TASK-004 | Implement `GitHubClient` | TASK-002 | 3 | No |
| TASK-005 | Implement `DocGenerator` (AST scan → Markdown) | TASK-002 | 5 | No |
| TASK-006 | Implement Steps 1–8 modules | TASK-003, TASK-005 | 5 | Blocked by TASK-003 |
| TASK-007 | Implement `SDLCOrchestrator` | TASK-004, TASK-006 | 2 | Blocked by TASK-006 |
| TASK-008 | Write pytest suite (unit + integration) | TASK-007 | 1 | Blocked by TASK-007 |

## Task Details

### TASK-001 — Set up project structure & dependencies
**Description**: Create `src/`, `tests/`, `docs/`, `hooks/` dirs; write `requirements.txt`, `.env.example`, `README.md`.
**Files**: `requirements.txt`, `.env.example`, `README.md`, directory scaffolding
**Acceptance**: `pip install -r requirements.txt` succeeds with no errors.

### TASK-002 — Implement `utils.py`
**Description**: Write `get_env`, `ensure_dir`, `write_doc`, `read_doc`.
**Files**: `src/pipeline/utils.py`
**Acceptance**: Unit tests pass; `get_env` raises on missing env var.

### TASK-003 — Implement `JiraClient`
**Description**: Fetch JIRA stories via REST API v3; parse ADF descriptions; extract ACs.
**Files**: `src/pipeline/jira_client.py`
**Acceptance**: `get_story` returns a `JiraStory`; mocked HTTP 404 raises `httpx.HTTPStatusError`.

### TASK-004 — Implement `GitHubClient`
**Description**: Create branches, push files, open PRs via GitHub REST API.
**Files**: `src/pipeline/github_client.py`
**Acceptance**: `create_pull_request` returns a `PullRequest` with a valid URL.

### TASK-005 — Implement `DocGenerator`
**Description**: AST-scan Python files; extract docstrings; render Markdown; write `docs/api/`.
**Files**: `src/pipeline/doc_generator.py`
**Acceptance**: `sync_docs` writes one `.md` file per module and an `api_index.md`.

### TASK-006 — Implement Steps 1-8 modules
**Description**: Each `src/steps/step*.py` generates its SDLC artefact.
**Files**: `src/steps/step1_*.py` through `step8_*.py`
**Acceptance**: Each `generate()` or `run()` function returns/writes valid Markdown.

### TASK-007 — Implement `SDLCOrchestrator`
**Description**: Wire all steps; add human-in-the-loop gate stubs; expose `run_all()` and `run_step()`.
**Files**: `src/pipeline/orchestrator.py`
**Acceptance**: `run_all()` completes without error in `dry_run=True` mode.

### TASK-008 — Write pytest suite
**Description**: Unit tests for all modules; integration test for full pipeline in dry_run mode.
**Files**: `tests/`
**Acceptance**: `pytest --cov=src` reports ≥ 80% coverage; all tests green.
