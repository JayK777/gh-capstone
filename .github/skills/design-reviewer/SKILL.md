# Skill: Design Reviewer

## Purpose
Perform a structured design review of `docs/architecture.md` as a senior engineer.

## Review Framework
Use the **CARS** model per finding:
- **C**omponent — which component has the issue
- **A**ssessment — what exactly is wrong or risky
- **R**ationale — why it matters
- **S**uggestion — concrete fix or alternative

## Severity Levels
| Level | Meaning | Must Fix Before Merge? |
|-------|---------|----------------------|
| CRITICAL | Security hole, data loss risk | Yes |
| HIGH | Missing requirement, scalability blocker | Yes |
| MEDIUM | Technical debt, observability gap | Recommended |
| LOW | Style, naming, minor improvement | Optional |

## Common Architecture Risks to Check
1. Single points of failure with no fallback
2. Synchronous calls in a high-throughput path
3. Mutable shared state across concurrent workers
4. Missing retry/back-off on external API calls
5. No timeout set on HTTP clients
6. Logging sensitive data (passwords, tokens, PII)
7. Overly broad IAM/permission scopes
