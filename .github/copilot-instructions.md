# GitHub Copilot Instructions — Agentic SDLC Pipeline

## Project Purpose
This repository implements an **Agentic SDLC Pipeline** that turns a JIRA User Story into a
production-ready GitHub PR by driving every phase of the software delivery lifecycle through
GitHub Copilot Agents, Prompts, Instructions, Skills, and Hooks.

## Repo Layout
```
src/pipeline/     – SDLC orchestrator and integrations (JIRA, GitHub)
src/steps/        – One module per SDLC step (steps 1-8)
.github/prompts/  – Reusable prompt files for each SDLC step
.github/agents/   – Custom agent-mode definitions
.github/skills/   – Domain-skill SKILL.md files
hooks/            – Git hooks (pre-commit, post-commit)
docs/             – SDLC artefacts (requirements, architecture, design-review, impl-plan)
tests/            – Pytest suite
```

## Copilot Behaviour Rules
1. **Always follow SDLC order** — never jump ahead of the current step.
2. **Preserve existing docs** — append/update, never overwrite without reading first.
3. **Security first** — never echo secrets, tokens, or passwords; validate all external inputs.
4. **Minimal footprint** — only write code directly requested or architecturally necessary.
5. **Deterministic outputs** — generated artefact filenames are fixed; do not invent new ones.

## Technology Stack
- **Language**: Python 3.11+
- **JIRA client**: `jira` (PyPI) or REST API via `httpx`
- **GitHub client**: PyGithub (`github`)
- **AI/LLM orchestration**: prompt files + agent mode (no external LLM dependency at runtime)
- **Testing**: `pytest` + `pytest-cov`
- **Config**: `.env` (loaded via `python-dotenv`); never commit real secrets

## Coding Conventions
- All functions have a single, clearly named responsibility.
- Module-level `__all__` lists exported symbols.
- No bare `except:` clauses; catch the narrowest exception possible.
- Use `pathlib.Path` for all file I/O.
- Environment variables are the ONLY accepted source of credentials.
