# Code Style & Conventions

## Formatting
- Line length: 100 (black/ruff configured)
- Black for formatting
- Ruff for linting

## Type Hints
- Encouraged but not strictly enforced
- Python 3.8+ compatible (use `typing` module imports)
- `no_implicit_optional = true` in mypy

## Imports
- F401 ignored in `__init__.py` for re-exports
- isort via ruff for import ordering

## Error Handling
- Use exception chaining: `raise NewError(...) from original_error`

## Testing
- Unit tests: `tests/unit/`
- Property tests: `tests/property/` (Hypothesis)
- Coverage required via pytest-cov
