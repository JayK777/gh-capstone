#!/usr/bin/env python3
"""
install-hooks.py  –  Copy hooks/ into .git/hooks/ and make them executable.
Run once after cloning: python hooks/install-hooks.py
"""

import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HOOKS_SRC = REPO_ROOT / "hooks"
HOOKS_DST = REPO_ROOT / ".git" / "hooks"

HOOK_FILES = ["pre-commit", "post-commit"]


def install() -> None:
    if not HOOKS_DST.exists():
        print("❌ .git/hooks directory not found. Are you in a git repo?")
        sys.exit(1)

    for hook in HOOK_FILES:
        src = HOOKS_SRC / hook
        dst = HOOKS_DST / hook
        shutil.copy2(src, dst)
        dst.chmod(dst.stat().st_mode | 0o111)  # make executable
        print(f"✅ Installed {hook} → {dst}")

    print("\nAll hooks installed successfully.")


if __name__ == "__main__":
    install()
