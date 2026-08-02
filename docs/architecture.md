# Architecture — Automated Documentation Sync Pipeline

> Generated: 2026-08-02

## Overview

The system is a Python 3.11+ CLI/library that orchestrates an 8-step SDLC pipeline.
It integrates with JIRA (story input), scans source code (documentation extraction),
and integrates with GitHub (PR output). All steps are driven by Copilot agents and prompts.

## Component Diagram

```mermaid
graph TD
    CLI[CLI Entry Point<br/>run_pipeline.py] --> ORCH[SDLCOrchestrator]
    ORCH --> JIRA[JiraClient<br/>JIRA REST API v3]
    ORCH --> STEPS[Steps 1-8 Modules]
    STEPS --> DOCGEN[DocGenerator<br/>AST-based scanner]
    STEPS --> GH[GitHubClient<br/>GitHub REST API]
    DOCGEN --> DOCS[(docs/ artefacts)]
    GH --> PR[(GitHub PR)]
    ORCH --> DOCS
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Orchestrator
    participant JIRA
    participant DocGen
    participant GitHub

    User->>CLI: python run_pipeline.py --story PROJ-42
    CLI->>Orchestrator: run_all()
    Orchestrator->>JIRA: get_story("PROJ-42")
    JIRA-->>Orchestrator: JiraStory
    Orchestrator->>Orchestrator: Steps 1-4 (generate docs)
    Orchestrator->>DocGen: sync_docs(src/, docs/)
    DocGen-->>Orchestrator: [list of written Paths]
    Orchestrator->>GitHub: create_branch(feature/PROJ-42-...)
    Orchestrator->>GitHub: push_file() × N
    Orchestrator->>GitHub: create_pull_request(...)
    GitHub-->>Orchestrator: PullRequest(url)
    Orchestrator-->>User: PR URL
```

## Component Responsibilities

| Component | Module | Responsibility |
|-----------|--------|----------------|
| CLI | `run_pipeline.py` | Parse args, build config, invoke orchestrator |
| Orchestrator | `src/pipeline/orchestrator.py` | Sequence steps, manage state |
| JiraClient | `src/pipeline/jira_client.py` | Fetch & parse JIRA stories |
| GitHubClient | `src/pipeline/github_client.py` | Create branches, push files, open PRs |
| DocGenerator | `src/pipeline/doc_generator.py` | AST scan → Markdown |
| Steps 1-8 | `src/steps/step*.py` | Generate each SDLC artefact |
| Hooks | `hooks/` | Pre/post commit safety checks |

## Technology Choices

| Choice | Library | Rationale | NFR |
|--------|---------|-----------|-----|
| HTTP client | `httpx` | Sync + async, explicit timeouts, wide adoption | NFR-01, NFR-03 |
| Config | `python-dotenv` | Zero-dependency env file loading | NFR-02 |
| AST parsing | stdlib `ast` | No extra dependency; stable API | NFR-04 |
| Testing | `pytest` + `pytest-cov` | Industry standard; rich plugin ecosystem | NFR-04 |
| Retry transport | `httpx.HTTPTransport(retries=3)` | Minimal deps; handles transient 5xx | NFR-03 |

## Security Boundaries

```mermaid
graph LR
    ENV[.env file<br/>NOT committed] -->|loaded at startup| APP[Application]
    APP -->|Bearer token| JIRA_API[JIRA API]
    APP -->|Bearer token| GITHUB_API[GitHub API]
    APP -->|write| DOCS_DIR[docs/ directory]
    APP -.->|never logs| SECRETS[Credentials]
    RETRY[Retry wrapper] --> JIRA_API
    RETRY --> GITHUB_API
```

- All credentials loaded exclusively from environment variables.
- No credential is ever written to a generated document or log line.
- JIRA and GitHub clients use HTTPS only.
- Retry wrapper added around all external API calls (addresses design review finding #1).

## Deployment View

```
Developer workstation / CI runner
└── Python 3.11 virtualenv
    ├── run_pipeline.py
    ├── src/
    └── .env  ← gitignored; set in CI as secrets
```

CI: GitHub Actions (`sdlc-pipeline.yml`) — triggered on push to feature branches.
