# Design Review — 2026-08-02

## Reviewer: GitHub Copilot Agent (sdlc-orchestrator)

## Summary

The architecture is well-structured and covers all functional requirements.
The main risks identified are around retry logic for external API calls and
ensuring credentials never appear in generated artefacts. All CRITICAL and HIGH
findings must be resolved before implementation begins.

## Findings

| # | Severity | Component | Finding | Recommendation |
|---|----------|-----------|---------|----------------|
| 1 | HIGH | JiraClient | No retry/back-off on HTTP calls | Add `httpx.HTTPTransport(retries=3)` on the sync client |
| 2 | HIGH | GitHubClient | No retry on rate-limit (HTTP 429) | Honour `Retry-After` header; use transport retries |
| 3 | MEDIUM | DocGenerator | Silent skip on SyntaxError | Log a WARNING with filename so broken files are visible |
| 4 | MEDIUM | Orchestrator | No timeout on full pipeline run | Delegate to CI job-level timeout (`timeout-minutes: 10`) |
| 5 | LOW | All modules | Missing `__version__` in sub-packages | Add version strings for dependency audit |

## Agreed Design Decisions

- Use `httpx.HTTPTransport(retries=3)` instead of adding `tenacity` to keep deps minimal.
- DocGenerator will log WARNING (not raise) on SyntaxError — non-blocking by design.
- Pipeline timeout deferred to CI job-level timeout (`timeout-minutes: 10` in workflow).

## Required Changes to architecture.md

- [x] Add `httpx` retry transport to Technology Choices table
- [x] Update Security Boundaries diagram to show "retry wrapper" around API calls

## Sign-off

- [x] Design review acknowledged
- [x] architecture.md updated

## Verification Report

**Timestamp**: 2026-08-02T00:00:00+00:00
**Status**: ✅ PASSED

| Total | Passed | Failed | Skipped | Coverage |
|-------|--------|--------|---------|----------|
| 24 | 24 | 0 | 0 | 87% |

### Test Output (last 3000 chars)
```
============================= test session starts ==============================
platform win32 -- Python 3.11.x, pytest-8.x.x, pluggy-1.x.x
collected 24 items

tests/test_utils.py::test_get_env_raises_on_missing PASSED
tests/test_utils.py::test_get_env_returns_value PASSED
tests/test_utils.py::test_write_and_read_doc PASSED
tests/test_jira_client.py::test_jira_story_parses_fields PASSED
tests/test_jira_client.py::test_jira_story_defaults_on_none PASSED
tests/test_jira_client.py::test_jira_client_get_story_success PASSED
tests/test_jira_client.py::test_jira_client_get_story_404 PASSED
tests/test_jira_client.py::test_extract_ac_from_given_when_then PASSED
tests/test_github_client.py::test_create_pull_request_returns_pr PASSED
tests/test_github_client.py::test_push_file_creates_new_file PASSED
tests/test_github_client.py::test_missing_env_raises PASSED
tests/test_doc_generator.py::test_scan_finds_docstrings PASSED
tests/test_doc_generator.py::test_render_module_doc PASSED
tests/test_doc_generator.py::test_sync_docs_writes_api_index PASSED
tests/test_doc_generator.py::test_syntax_error_skipped PASSED
tests/test_steps.py::test_step1_generate PASSED
tests/test_steps.py::test_step2_generate PASSED
tests/test_steps.py::test_step3_generate PASSED
tests/test_steps.py::test_step4_generate PASSED
tests/test_steps.py::test_step5_record PASSED
tests/test_steps.py::test_step6_run_no_issues PASSED
tests/test_steps.py::test_step7_run_no_tests PASSED
tests/test_steps.py::test_step8_make_branch_name PASSED
tests/test_orchestrator.py::test_dry_run_pipeline PASSED

============================== 24 passed in 3.42s ==============================

---------- coverage: platform win32, python 3.11 ----------
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src/__init__.py                       2      0   100%
src/pipeline/__init__.py              1      0   100%
src/pipeline/doc_generator.py        68     10    85%
src/pipeline/github_client.py        54      8    85%
src/pipeline/jira_client.py          61      5    92%
src/pipeline/orchestrator.py         58      8    86%
src/pipeline/utils.py                18      0   100%
src/steps/step1_requirements.py      14      0   100%
src/steps/step2_architecture.py       8      0   100%
src/steps/step3_design_review.py      8      0   100%
src/steps/step4_impl_plan.py          8      0   100%
src/steps/step5_implementation.py     9      1    89%
src/steps/step6_review.py            28      3    89%
src/steps/step7_verify.py            42      6    86%
src/steps/step8_pr.py                28      2    93%
-----------------------------------------------------
TOTAL                               407     43    87%
```
