# Skill: System Architect

## Purpose
Design a well-structured, secure, and scalable architecture from `docs/requirements.md`.

## Architecture Principles
1. **Separation of Concerns** — pipeline, integrations, and domain logic are separate modules.
2. **Dependency Inversion** — high-level orchestration depends on abstractions, not concretions.
3. **Fail Fast** — validate inputs at system boundaries; surface errors early.
4. **Least Privilege** — each component only receives the secrets/permissions it needs.

## Mandatory Diagram Types
| Diagram | Mermaid type | When Required |
|---------|-------------|---------------|
| Component | `graph TD` | Always |
| Data Flow | `sequenceDiagram` | When >2 systems interact |
| State Machine | `stateDiagram-v2` | When complex workflow states exist |
| ER Diagram | `erDiagram` | When persistent data models are involved |

## Technology Selection Criteria
- Prefer stdlib over third-party where functionality is equivalent.
- Third-party libraries must have >1 M monthly PyPI downloads or a well-known sponsor.
- All async I/O uses `asyncio` + `httpx.AsyncClient`.

## Security Checklist
- [ ] Authentication method documented for each external API call
- [ ] Input sanitisation at every public function boundary
- [ ] Secrets loaded from env vars only
- [ ] No sensitive data in log output
