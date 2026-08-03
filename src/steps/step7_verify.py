"""Step 7 — Verify: run pytest and produce a verification report."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

__all__ = ["run", "append_report"]


@dataclass
class TestReport:
    timestamp: str
    total: int
    passed: int
    failed: int
    skipped: int
    coverage: str
    output: str
    success: bool


def run(tests_root: Path) -> TestReport:
    """
    Execute pytest against tests_root and return a TestReport.
    If pytest is not installed or tests_root is empty, returns a safe default.
    """
    timestamp = datetime.now(tz=timezone.utc).isoformat()

    if not tests_root.exists() or not list(tests_root.rglob("test_*.py")):
        return TestReport(
            timestamp=timestamp,
            total=0, passed=0, failed=0, skipped=0,
            coverage="N/A",
            output="No test files found.",
            success=True,
        )

    result = subprocess.run(
        ["python", "-m", "pytest", str(tests_root), "-v",
         "--cov=src", "--cov-report=term-missing", "--tb=short"],
        capture_output=True, text=True
    )
    output = result.stdout + result.stderr
    total, passed, failed, skipped, coverage = _parse_output(output)

    return TestReport(
        timestamp=timestamp,
        total=total, passed=passed, failed=failed, skipped=skipped,
        coverage=coverage,
        output=output[-3000:],  # keep last 3000 chars
        success=(result.returncode == 0),
    )


def append_report(design_review_md: str, report: TestReport) -> str:
    """Append a Verification Report section to design-review.md content."""
    status = "✅ PASSED" if report.success else "❌ FAILED"
    section = f"""

## Verification Report

**Timestamp**: {report.timestamp}
**Status**: {status}

| Total | Passed | Failed | Skipped | Coverage |
|-------|--------|--------|---------|----------|
| {report.total} | {report.passed} | {report.failed} | {report.skipped} | {report.coverage} |

### Test Output (last 3000 chars)
```
{report.output}
```
"""
    return design_review_md + section


# ── private ───────────────────────────────────────────────────────────────────

def _parse_output(output: str) -> tuple[int, int, int, int, str]:
    import re

    total = passed = failed = skipped = 0
    coverage = "N/A"

    summary_match = re.search(
        r'(\d+) passed(?:, (\d+) failed)?(?:, (\d+) skipped)?', output
    )
    if summary_match:
        passed = int(summary_match.group(1))
        failed = int(summary_match.group(2) or 0)
        skipped = int(summary_match.group(3) or 0)
        total = passed + failed + skipped

    cov_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
    if cov_match:
        coverage = cov_match.group(1) + "%"

    return total, passed, failed, skipped, coverage
