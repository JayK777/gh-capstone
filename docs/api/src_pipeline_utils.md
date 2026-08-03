# `src.pipeline.utils`

Shared utility functions used across pipeline steps.

---

## `get_env(key)`

Return an environment variable value; raise if missing or empty.

## `ensure_dir(path)`

Create directory (and parents) if it doesn't exist; return the path.

## `write_doc(docs_root, filename, content)`

Write content to docs_root/filename, creating dirs as needed.

## `read_doc(docs_root, filename)`

Read and return the text of docs_root/filename.
