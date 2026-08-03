# `src.pipeline.doc_generator`

doc_generator.py
~~~~~~~~~~~~~~~~
Core use-case engine: "Automated Documentation Sync".

Scans Python source files for module/class/function docstrings and
generates/updates Markdown documentation under the docs/ folder.

---

## class `DocEntry`

Represents a single documented symbol extracted from source.

## `scan_source_tree(src_root)`

Walk src_root and return DocEntry objects for all documented symbols.

## `render_module_doc(entries, module_name)`

Render a Markdown string documenting a single module.

## `sync_docs(src_root, docs_root)`

Scan src_root for docstrings and write/update Markdown files under docs_root/api/.
Returns a list of Paths that were written.
