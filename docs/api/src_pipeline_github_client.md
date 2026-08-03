# `src.pipeline.github_client`

GitHub client: create branches, push files, and open pull requests.

---

## class `PullRequest`

Lightweight representation of a GitHub Pull Request.

## class `GitHubClient`

Wrapper around the GitHub REST API for SDLC pipeline operations.

### `get_default_branch_sha(self)`

Return the HEAD SHA of the repository's default branch.

### `create_branch(self, branch_name, from_sha)`

Create a new branch and return its name.

### `push_file(self, branch, file_path, content, message)`

Create or update a file on the given branch.

### `create_pull_request(self, title, body, head_branch, base_branch)`

Open a new pull request and return the PullRequest object.
