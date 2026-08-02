---
mode: ask
description: "Step 2 – Design system architecture from requirements.md"
---

# SDLC Step 2 — Architecture Design

You are a principal software architect.

## Your Task
Read `docs/requirements.md` and produce `docs/architecture.md`.

## Deliverables in `docs/architecture.md`
1. **Component Diagram** (Mermaid `graph TD`)
2. **Technology Choices** — justify each choice against the NFRs
3. **Data Flow** (Mermaid `sequenceDiagram`)
4. **Key Design Decisions** — table of decision / rationale / alternatives rejected
5. **Security Boundaries** — where authentication and authorisation occur
6. **Deployment View** — container/cloud topology

## Constraints
- Prefer well-supported, minimal-dependency libraries.
- All external calls must be async-capable.
- No architecture decision should contradict a requirement in `docs/requirements.md`.
