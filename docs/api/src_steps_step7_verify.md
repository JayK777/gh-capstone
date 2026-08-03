# `src.steps.step7_verify`

Step 7 — Verify: run pytest and produce a verification report.

---

## class `TestReport`

## `run(tests_root)`

Execute pytest against tests_root and return a TestReport.
If pytest is not installed or tests_root is empty, returns a safe default.

## `append_report(design_review_md, report)`

Append a Verification Report section to design-review.md content.
