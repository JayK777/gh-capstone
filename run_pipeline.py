#!/usr/bin/env python3
"""
run_pipeline.py
~~~~~~~~~~~~~~~
CLI entry point for the Agentic SDLC Pipeline.

Usage:
    python run_pipeline.py --story PROJ-42
    python run_pipeline.py --story PROJ-42 --step requirements
    python run_pipeline.py --story PROJ-42 --dry-run
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from src.pipeline.orchestrator import PipelineConfig, SDLCOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Agentic SDLC Pipeline: JIRA story → GitHub PR"
    )
    parser.add_argument("--story", required=True, help="JIRA issue key (e.g. PROJ-42)")
    parser.add_argument(
        "--step",
        choices=SDLCOrchestrator.STEPS,
        help="Run a single step instead of the full pipeline",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip GitHub API calls; print PR body to stdout instead",
    )
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Target branch for the PR (default: main)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    config = PipelineConfig(
        jira_story_id=args.story,
        repo_root=Path("."),
        docs_root=Path("docs"),
        src_root=Path("src"),
        tests_root=Path("tests"),
        base_branch=args.base_branch,
        dry_run=args.dry_run,
        interactive=False,
    )

    orchestrator = SDLCOrchestrator(config)

    if args.step:
        orchestrator.run_step(args.step)
        print(f"✅ Step '{args.step}' complete.")
    else:
        pr_url = orchestrator.run_all()
        print(f"\n🎉 Pipeline complete!\n📎 Pull Request: {pr_url}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
