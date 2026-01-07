# MudHound Project Overview

## Purpose
Terminal-based batch URL extraction tool with animated UI for search engine queries.

## Tech Stack
- Python 3.8+
- Typer (CLI framework)
- Rich (terminal rendering)
- Pydantic (data models)
- duckduckgo-search (default adapter)
- httpx (HTTP client)

## Architecture Layers
1. **CLI** (`cli/`): Typer app, entry point `__main__.py`
2. **Core** (`core/`): engine.py, config.py, result.py, store.py
3. **Adapters** (`adapters/`): Pluggable search engines (base.py, registry.py, duckduckgo.py)
4. **UI** (`ui/`): renderer.py, frames.py, theme.py, animation/, components/

## Key Patterns
- Adapter Pattern for search engines
- Registry Discovery for auto-loading adapters
- Configuration Priority Chain: CLI > env > cwd > XDG > legacy > defaults
