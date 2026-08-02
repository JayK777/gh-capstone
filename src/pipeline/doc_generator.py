"""
doc_generator.py
~~~~~~~~~~~~~~~~
Core use-case engine: "Automated Documentation Sync".

Scans Python source files for module/class/function docstrings and
generates/updates Markdown documentation under the docs/ folder.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["DocEntry", "scan_source_tree", "render_module_doc", "sync_docs"]


@dataclass
class DocEntry:
    """Represents a single documented symbol extracted from source."""

    module: str
    kind: str          # "module" | "class" | "function"
    name: str
    docstring: str
    lineno: int
    signature: str = ""
    children: list["DocEntry"] = field(default_factory=list)


# ── extraction ────────────────────────────────────────────────────────────────

def scan_source_tree(src_root: Path) -> list[DocEntry]:
    """Walk src_root and return DocEntry objects for all documented symbols."""
    entries: list[DocEntry] = []
    for py_file in sorted(src_root.rglob("*.py")):
        if py_file.name.startswith("_"):
            continue
        entries.extend(_parse_file(py_file, src_root))
    return entries


def _parse_file(path: Path, src_root: Path) -> list[DocEntry]:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []

    module_name = _path_to_module(path, src_root)
    entries: list[DocEntry] = []

    module_doc = ast.get_docstring(tree) or ""
    if module_doc:
        entries.append(DocEntry(module_name, "module", module_name, module_doc, 1))

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            entry = DocEntry(module_name, "class", node.name, doc, node.lineno)
            # Collect methods
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    method_doc = ast.get_docstring(item) or ""
                    sig = _build_signature(item)
                    entry.children.append(
                        DocEntry(module_name, "function", item.name, method_doc, item.lineno, sig)
                    )
            entries.append(entry)

        elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            parent = _get_parent_class(tree, node)
            if parent is None:  # top-level function only
                doc = ast.get_docstring(node) or ""
                sig = _build_signature(node)
                entries.append(DocEntry(module_name, "function", node.name, doc, node.lineno, sig))

    return entries


def _path_to_module(path: Path, src_root: Path) -> str:
    rel = path.relative_to(src_root.parent)
    return str(rel.with_suffix("")).replace("\\", ".").replace("/", ".")


def _build_signature(node: ast.FunctionDef) -> str:
    args = [a.arg for a in node.args.args]
    return f"{node.name}({', '.join(args)})"


def _get_parent_class(tree: ast.AST, func: ast.FunctionDef) -> ast.ClassDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if item is func:
                    return node
    return None


# ── rendering ─────────────────────────────────────────────────────────────────

def render_module_doc(entries: list[DocEntry], module_name: str) -> str:
    """Render a Markdown string documenting a single module."""
    module_entries = [e for e in entries if e.module == module_name]
    if not module_entries:
        return f"# {module_name}\n\n*No documentation found.*\n"

    lines: list[str] = [f"# `{module_name}`\n"]

    for entry in module_entries:
        if entry.kind == "module":
            lines.append(f"{entry.docstring}\n\n---\n")
        elif entry.kind == "class":
            lines.append(f"## class `{entry.name}`\n")
            if entry.docstring:
                lines.append(f"{entry.docstring}\n")
            for child in entry.children:
                lines.append(f"### `{child.signature or child.name}`\n")
                if child.docstring:
                    lines.append(f"{child.docstring}\n")
        elif entry.kind == "function":
            lines.append(f"## `{entry.signature or entry.name}`\n")
            if entry.docstring:
                lines.append(f"{entry.docstring}\n")

    return "\n".join(lines)


# ── sync ──────────────────────────────────────────────────────────────────────

def sync_docs(src_root: Path, docs_root: Path) -> list[Path]:
    """
    Scan src_root for docstrings and write/update Markdown files under docs_root/api/.
    Returns a list of Paths that were written.
    """
    api_dir = docs_root / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    entries = scan_source_tree(src_root)
    modules = {e.module for e in entries}

    written: list[Path] = []
    for module in sorted(modules):
        content = render_module_doc(entries, module)
        slug = module.replace(".", "_")
        out_path = api_dir / f"{slug}.md"
        out_path.write_text(content, encoding="utf-8")
        written.append(out_path)

    # Write an index
    index_lines = ["# API Documentation Index\n"]
    for module in sorted(modules):
        slug = module.replace(".", "_")
        index_lines.append(f"- [{module}](api/{slug}.md)")
    index_path = docs_root / "api_index.md"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    written.append(index_path)

    return written
