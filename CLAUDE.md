# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Setup
uv venv && source .venv/bin/activate && uv sync

# Run the CLI
mh search "query"        # or: mudhound search "query"
mh interactive           # menu-driven interface

# Tests
pytest                           # all tests with coverage
pytest tests/unit/               # unit tests only
pytest tests/property/           # property-based tests (hypothesis)
pytest tests/unit/test_config.py # single file
pytest -k "test_name"            # single test by name

# Code quality
black mudhound/          # format
ruff check mudhound/     # lint
mypy mudhound/           # type check
```

## Architecture

MudHound is a terminal-based batch URL extraction tool with animated UI. The codebase follows a layered architecture:

### Layer Structure

- **CLI Layer** (`cli/`): Typer application with commands. Global options (verbose, quiet, theme, config) are passed via `typer.Context.obj`. Entry point is `__main__.py` which initializes logging, discovers adapters, and runs the Typer app.

- **Core Layer** (`core/`): Business logic
  - `engine.py`: `SearchEngine` orchestrates searches with retry logic, progress callbacks, and session management
  - `config.py`: `ConfigManager` with priority chain (CLI > env var > cwd > XDG > legacy > defaults), dot notation access (e.g., `config.get("general.engine")`)
  - `result.py`: Pydantic models for `SearchResult`, `SearchQuery`, `SearchSession`, `SearchOptions`
  - `store.py`: History persistence

- **Adapter Layer** (`adapters/`): Pluggable search engine adapters
  - `base.py`: `SearchAdapter` ABC - implement `name`, `display_name`, `search()` generator, `validate_options()`
  - `registry.py`: `AdapterRegistry` discovers adapters from: built-in modules, `mudhound_adapter_*` packages, `~/.mudhound/adapters/`
  - `duckduckgo.py`: Default implementation

- **UI Layer** (`ui/`): Terminal rendering
  - `renderer.py`: `UIRenderer` handles ANSI sequences, cursor management, output buffering
  - `frames.py`: `FrameRenderer` draws box frames with Unicode borders
  - `theme.py`: `ThemeEngine` applies semantic colors
  - `animation/`: Animation engine with color schemes and timing
  - `components/`: Reusable UI components (banner, menu, progress, table, confirm, error, status)

### Key Patterns

- **Adapter Pattern**: Search engines implement `SearchAdapter`. The `search()` method must be a generator yielding `SearchResult` objects for streaming progress.

- **Registry Discovery**: `AdapterRegistry.discover_all()` auto-discovers adapters at startup. Custom adapters: subclass `SearchAdapter`, place in `~/.mudhound/adapters/` or package as `mudhound_adapter_*`.

- **Configuration Priority**: CLI override > `MUDHOUND_CONFIG` env > `./mudhound.toml` > `~/.config/mudhound/config.toml` > `~/.mudhound/config.toml` > defaults.

- **Theme System**: Themes are TOML files in `data/themes/`. Use semantic names (e.g., "frame_border", "error", "success") with `ThemeEngine.apply()`.

### Testing

- Unit tests in `tests/unit/` for isolated component testing
- Property-based tests in `tests/property/` using Hypothesis for fuzzing inputs
- Use `pytest --cov=mudhound` for coverage (configured in pyproject.toml)

## Code Style

- Line length: 100 (configured in black/ruff)
- Python 3.8+ compatibility required
- Type hints encouraged but not strictly enforced
- Ruff ignores in `__init__.py`: F401 (unused imports for re-exports)
