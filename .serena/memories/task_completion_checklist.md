# Task Completion Checklist

Before marking a task complete:

1. **Format**: `black mudhound/`
2. **Lint**: `ruff check mudhound/` (or `ruff check --fix mudhound/`)
3. **Type Check**: `mypy mudhound/`
4. **Test**: `pytest` (all tests pass)

## After Code Changes
- Ensure exception chaining with `from err`
- No unused variables (F841/B007)
- Type annotations consistent with mypy settings
