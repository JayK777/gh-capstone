# Agentic SDLC Pipeline — GitHub Copilot Capstone

> **Input**: A JIRA User Story ID → **Output**: A GitHub Pull Request URL

This project implements a complete, fully agentic Software Delivery Lifecycle (SDLC) pipeline
powered by **GitHub Copilot Agents, Prompts, Instructions, Skills, and Hooks**.

## What It Does

Given a JIRA User Story, the pipeline automatically:

| Step | Action | Artefact |
|------|--------|---------|
| 1 | Elicit requirements | `docs/requirements.md` |
| 2 | Design architecture | `docs/architecture.md` |
| 3 | Conduct design review | `docs/design-review.md` |
| 4 | Create implementation plan | `docs/impl-plan.md` |
| 5 | Implement (doc sync + AST scan) | `docs/api/*.md` |
| 6 | Code review | findings in chat |
| 7 | Verify (run tests) | verification report |
| 8 | Create GitHub PR | PR URL returned |

## GitHub Copilot Features Used

| Feature | Location | Purpose |
|---------|----------|---------|
| **copilot-instructions.md** | `.github/copilot-instructions.md` | Repo-wide AI behaviour rules |
| **Prompts** | `.github/prompts/*.prompt.md` | Reusable step-specific prompts |
| **Instructions** | `.github/instructions/*.instructions.md` | File-scoped writing rules |
| **Skills** | `.github/skills/*/SKILL.md` | Domain knowledge per SDLC role |
| **Agents** | `.github/agents/*.agent.md` | Custom agent-mode definitions |
| **Git Hooks** | `hooks/` | Pre/post commit safety automation |

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/JayK777/gh-capstone.git
cd gh-capstone
pip install -r requirements.txt

# 2. Install git hooks
python hooks/install-hooks.py

# 3. Configure credentials
cp .env.example .env
# Edit .env with your JIRA and GitHub credentials

# 4. Run the full pipeline
python run_pipeline.py --story DOCS-42

# 5. Dry run (no GitHub API calls)
python run_pipeline.py --story DOCS-42 --dry-run

# 6. Run a single step
python run_pipeline.py --story DOCS-42 --step requirements
```

## Using with GitHub Copilot Chat

### Run the full SDLC from chat
Open GitHub Copilot Chat in VS Code and use the **SDLC Orchestrator** agent:

```
@sdlc-orchestrator  JIRA Story: DOCS-42 — As a developer, I want automated doc sync...
```

### Run a single step
```
@requirements-agent analyse story DOCS-42
@architect-agent design
@reviewer-agent review
@pr-agent create DOCS-42
```

### Use a prompt directly
Open `.github/prompts/01-requirements.prompt.md` in Copilot Chat and fill in `{{JIRA_STORY}}`.

## Project Structure

```
gh-capstone/
├── .github/
│   ├── copilot-instructions.md   ← Global Copilot instructions
│   ├── agents/                   ← 5 custom agent definitions
│   ├── instructions/             ← 3 file-scoped instruction files
│   ├── prompts/                  ← 8 SDLC step prompt files
│   ├── skills/                   ← 5 domain skill SKILL.md files
│   └── workflows/                ← GitHub Actions CI/CD
├── .vscode/
│   ├── settings.json             ← VS Code + Copilot settings
│   └── tasks.json                ← Run pipeline, tests via VS Code Tasks
├── hooks/
│   ├── pre-commit                ← Secret & code quality checks
│   ├── post-commit               ← Auto CHANGELOG update
│   └── install-hooks.py          ← One-time setup script
├── src/
│   ├── pipeline/                 ← Core modules (JIRA, GitHub, DocGen, Orchestrator)
│   └── steps/                   ← Step 1-8 artefact generators
├── tests/                        ← Pytest suite (≥80% coverage)
├── docs/                         ← SDLC artefacts (auto-generated)
├── run_pipeline.py               ← CLI entry point
├── requirements.txt
└── .env.example
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JIRA_BASE_URL` | Yes | e.g. `https://your-org.atlassian.net` |
| `JIRA_EMAIL` | Yes | Your Atlassian account email |
| `JIRA_API_TOKEN` | Yes | JIRA API token (not password) |
| `GITHUB_TOKEN` | Yes | GitHub Personal Access Token (repo + PR scope) |
| `GITHUB_OWNER` | Yes | GitHub username or org |
| `GITHUB_REPO` | Yes | Repository name |

## Running Tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

Target: **≥ 80% coverage**, all 24 tests green.

## License

MIT
