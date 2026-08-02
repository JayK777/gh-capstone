"""Step 6 — Code Review: run automated checks and print findings to stdout/log."""

from __future__ import annotations

import logging
import re
from pathlib import Path

__all__ = ["run"]

log = logging.getLogger(__name__)

_SECRET_RE = re.compile(
    r'(?i)(password|passwd|secret|api_key|apikey|token|private_key)\s*=\s*["\'][^"\']{6,}["\']'
)
_BARE_EXCEPT_RE = re.compile(r'^\s*except\s*:\s*$', re.MULTILINE)
_EVAL_RE = re.compile(r'\beval\s*\(')


def run(src_root: Path, docs_root: Path) -> list[str]:
    """
    Scan src_root for common code issues. Returns list of finding strings.
    Also logs each finding at WARNING level.
    """
    findings: list[str] = []

    for py_file in sorted(src_root.rglob("*.py")):
        text = py_file.read_text(encoding="utf-8")
        rel = py_file.relative_to(src_root.parent)

        for i, line in enumerate(text.splitlines(), 1):
            if _SECRET_RE.search(line):
                msg = f"[CRITICAL] {rel}:{i} — possible hardcoded secret"
                findings.append(msg)
                log.warning(msg)

            if _EVAL_RE.search(line):
                msg = f"[HIGH] {rel}:{i} — eval() call detected"
                findings.append(msg)
                log.warning(msg)

        if _BARE_EXCEPT_RE.search(text):
            msg = f"[HIGH] {rel} — bare except: clause found"
            findings.append(msg)
            log.warning(msg)

    if findings:
        log.warning("Code review: %d finding(s) detected.", len(findings))
    else:
        log.info("Code review: no issues found. ✅")

    return findings
