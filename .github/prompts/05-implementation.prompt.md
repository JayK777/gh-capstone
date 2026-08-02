---
mode: agent
description: "Step 5 – Implement the feature described in impl-plan.md"
---

# SDLC Step 5 — Implementation

You are a senior Python developer. Implement **every TASK** listed in `docs/impl-plan.md`
in dependency order. For each task:

1. Read the relevant requirements from `docs/requirements.md`.
2. Write idiomatic Python 3.11+ code.
3. Add a module docstring and type hints.
4. Write a corresponding test in `tests/` before or alongside the implementation.
5. Mark the task complete by appending `[x]` to its row in `docs/impl-plan.md`.

## Hard Rules
- Credentials come **only** from environment variables — never hardcode secrets.
- All file I/O uses `pathlib.Path`.
- All HTTP calls use `httpx` with explicit timeouts.
- Raise specific, documented exceptions; never `raise Exception("...")`.
- Keep functions ≤ 30 lines; extract helpers if needed.

## Copilot Features to Use
- Use `#copilot:generate` inline comments to trigger code generation.
- Reference `docs/architecture.md` to understand component boundaries.
