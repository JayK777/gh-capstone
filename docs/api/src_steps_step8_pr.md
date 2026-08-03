# `src.steps.step8_pr`

Step 8 — PR: helpers for branch naming, file collection, and PR body generation.

---

## `make_branch_name(story_id, title)`

Return a git-safe branch name: feature/<story-id>-<slug>.

## `collect_files(docs_root, src_root)`

Collect all files to push to GitHub.
Returns list of (relative_path_str, file_content) tuples.

## `build_pr_body(story, docs_root, files_pushed)`

Construct the full GitHub PR description using the pr-writer skill format.
