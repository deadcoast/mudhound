# Error Log (Temporary)

## 0.0.1

> [!NOTE]
> Below is a json based temporary dump of errors from vscode.
> - The file is a revolving door any and all data should be considered temporary and subject to change
> - Relevant data should be added to the CHANGELOG or VALIDATION files as appropriate

---

- 2026-01-07 (Updated)

## Current State: CLEAN

All linting and type checking passes:

```bash
$ uv run mypy mudhound/
Success: no issues found in 51 source files

$ uv run ruff check mudhound/
All checks passed!

$ uv run pytest tests/
150 passed (unit tests)
108 passed (property tests)
```

### Previous Issues (Resolved in 0.0.2 and 0.0.3)

The following categories of issues were resolved:

1. **Mypy Type Errors** - Fixed type annotations in:
   - `mudhound/adapters/duckduckgo.py` (safesearch arg-type)
   - `mudhound/core/config.py` (assignment type)
   - `mudhound/core/store.py` (no-any-return)
   - `mudhound/__main__.py` (implicit Optional)
   - `mudhound/logging/levels.py` (attr-defined, ignored)
   - `mudhound/ui/glyphs.py` (GLYPHS indexing)
   - `mudhound/ui/components/*.py` (return types, Optional)
   - `mudhound/cli/validation.py` (return type)
   - `demo_files/demo_error_handler.py` (variable reuse)

2. **Ruff B904 (Exception Chaining)** - Added `raise ... from err` throughout:
   - `mudhound/adapters/duckduckgo.py`
   - `mudhound/core/config.py`
   - `mudhound/core/store.py`
   - `mudhound/core/engine.py`
   - `mudhound/assets/manager.py`
   - `mudhound/ui/theme.py`
   - `mudhound/cli/commands/*.py`

3. **Ruff F841/B007 (Unused Variables)** - Fixed in:
   - `mudhound/__main__.py`
   - `mudhound/adapters/registry.py`
   - `mudhound/assets/manager.py`
   - `tests/property/test_logging.py`
   - `tests/property/test_table.py`

4. **Configuration Updates** (0.0.4):
   - `pyproject.toml` - Moved ruff lint settings to `[tool.ruff.lint]` section
   - `tests/property/test_adapters.py` - Renamed `TestAdapter` to `MockAdapter`

---

*Last verified: 2026-01-07*
