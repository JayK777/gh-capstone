---
applyTo: "src/**"
---
# Python Implementation Rules
- Python version: 3.11+
- All public functions must have type hints.
- Use `pathlib.Path` for file operations — never `os.path`.
- Use `httpx` for HTTP calls with explicit `timeout=30` parameter.
- Load secrets exclusively from `os.environ` or `python-dotenv` — never hardcode.
- Maximum function length: 30 lines. Extract helpers beyond that.
- Import order: stdlib → third-party → local (enforced by isort).
- All modules must define `__all__`.
