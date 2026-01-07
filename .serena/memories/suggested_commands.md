# Suggested Commands for MudHound

## Setup
```bash
uv venv && .venv\Scripts\activate && uv sync   # Windows
```

## Running
```bash
mh search "query"        # CLI search
mh interactive           # Menu-driven interface
```

## Testing
```bash
pytest                           # All tests with coverage
pytest tests/unit/               # Unit tests only
pytest tests/property/           # Property-based tests (Hypothesis)
pytest tests/unit/test_config.py # Single file
pytest -k "test_name"            # Single test by name
```

## Code Quality
```bash
black mudhound/          # Format code
ruff check mudhound/     # Lint
ruff check --fix mudhound/  # Auto-fix lint issues
mypy mudhound/           # Type check
```

## Windows System Commands
- `dir` instead of `ls`
- `type` instead of `cat`
- `findstr` instead of `grep`
- PowerShell: `Get-ChildItem -Recurse` for find
