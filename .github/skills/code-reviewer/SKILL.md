# Skill: Code Reviewer

## Purpose
Review Python source code against the project's coding conventions and the requirements.

## Review Checklist (evaluate each systematically)

### Correctness
- Does the implementation satisfy every FR in `docs/requirements.md`?
- Are all edge cases in the ACs handled?

### Security (OWASP Top 10 focus)
- No secrets in code or logs (A02 Cryptographic Failures)
- No SQL/command injection via string concatenation (A03 Injection)
- Input validated at all public function boundaries (A03)
- Dependencies checked against known CVEs (A06 Vulnerable Components)

### Error Handling
- Every external call (HTTP, file I/O, DB) wrapped in try/except
- Exceptions are specific (not bare `except:`)
- Errors are logged with context before re-raising

### Test Coverage
- Happy path covered
- "Not Found" / 404 / None covered
- Empty collection edge cases covered
- Async code tested with `pytest-asyncio`

### Code Clarity
- Functions ≤ 30 lines
- Names are verbs for functions, nouns for classes
- No magic numbers (use named constants)

### DRY
- No copy-pasted logic blocks
- Shared utilities extracted to `src/pipeline/utils.py`

## Output Format
For each finding:
```
[SEVERITY] file.py:line — description
  Suggestion: ...
```
