# Changelog

## 0.0.1 - 2026-01-10

> [!IMPORTANT]
> This is the initial release of MudHound. The core search functionality and DuckDuckGo adapter are fully implemented. The implementation includes:
>
> - **Generator-based streaming** for real-time result delivery
> - **Comprehensive error handling** with custom exception types
> - **Retry logic** with exponential backoff for network failures
> - **Extensible adapter system** with plugin support
> - **No API keys required** - uses DuckDuckGo's public search interface

## 0.0.1

> [!IMPORTANT]
> Core Search Functionality - 2026-01-10
> STATUS: **FULLY IMPLEMENTED**

### A) Data Models (`mudhound/core/result.py`)

| Component | Status |
| --------- | ------ |
| `SearchResult` dataclass | ✅ Complete (url, title, snippet, source, rank, metadata) |
| `SearchOptions` dataclass | ✅ Complete (max_results, region, safesearch, time_limit) |
| `SearchStatus` enum | ✅ Complete (PENDING, RUNNING, COMPLETE, FAILED, CANCELLED) |
| `SearchQuery` dataclass | ✅ Complete (id, query, engine, options, created_at, status) |
| `SearchSession` dataclass | ✅ Complete (query, results, started_at, completed_at, error) |

### Search Engine (`mudhound/core/engine.py`)

| Feature | Status |
| ------- | ------ |
| Adapter orchestration | ✅ Complete |
| Progress callbacks | ✅ Complete |
| Session management | ✅ Complete |
| Retry logic with exponential backoff | ✅ Complete |
| Cancellation support (CTRL+C) | ✅ Complete |
| Error handling | ✅ Complete |

### Exception Hierarchy (`mudhound/core/exceptions.py`)

All exceptions implemented: `MudHoundError`, `ConfigError`, `AdapterError`, `AdapterNotFoundError`, `RateLimitError`, `NetworkError`, `ValidationError`, `ExportError`, `AnimationError`

---

### DuckDuckGo Adapter - **FULLY IMPLEMENTED** ✅

### `DuckDuckGoAdapter` (`mudhound/adapters/duckduckgo.py`)

| Feature | Status |
| ------- | ------ |
| `name` / `display_name` properties | ✅ Complete |
| `search()` generator method | ✅ Complete - uses `duckduckgo-search` library |
| `validate_options()` | ✅ Complete |
| Streaming results | ✅ Complete |
| Rate limit detection (`RatelimitException`) | ✅ Complete |
| Network error handling | ✅ Complete |
| Timeout handling | ✅ Complete |
| Domain extraction helper | ✅ Complete |

### Adapter Registry (`mudhound/adapters/registry.py`)

| Feature | Status |
| ------- | ------ |
| Manual registration | ✅ Complete |
| Built-in adapter discovery | ✅ Complete |
| Plugin discovery (`mudhound_adapter_*`) | ✅ Complete |
| User adapter discovery (`~/.mudhound/adapters/`) | ✅ Complete |
| `list_available()` | ✅ Complete |

---

### Summary

The **core search functionality and DuckDuckGo adapter are fully implemented** and production-ready. The implementation includes:

- **Generator-based streaming** for real-time result delivery
- **Comprehensive error handling** with custom exception types
- **Retry logic** with exponential backoff for network failures
- **Extensible adapter system** with plugin support
- **No API keys required** - uses DuckDuckGo's public search interface

## 0.0.2

> [!IMPORTANT]
> CLI Implementation Status - 2026-01-07

### A) Current Commands (Implemented)

| Command | Status | Integration |
| ------- | ------ | ----------- |
| `mh config list` | ✅ Complete | Fully integrated with ConfigManager |
| `mh config get <key>` | ✅ Complete | Fully integrated |
| `mh config set <key> <value>` | ✅ Complete | Fully integrated |
| `mh config reset` | ✅ Complete | Fully integrated |
| `mh config edit` | ✅ Complete | Fully integrated |
| `mh history list` | ✅ Complete | Fully integrated with ResultStore |
| `mh history show <id>` | ✅ Complete | Fully integrated |
| `mh history replay <id>` | ✅ Complete | Fully integrated with SearchEngine |
| `mh history delete <id>` | ✅ Complete | Fully integrated |
| `mh history clear` | ✅ Complete | Fully integrated |
| `mh interactive` | ✅ Complete | Fully integrated |
| `mh version` | ✅ Complete | Fully integrated |
| Global options (`-v`, `-q`, `--no-color`, etc.) | ✅ Complete | Fully integrated |

### B) **MISSING: Primary Search Command** ❌

The **main `mh search <query>` command is NOT implemented**. This is the most critical missing piece.

According to the design document (`Docs/design.md`), the search command should be:

```sh
mh search <query>
    --max, -m           # Maximum results (default: 50)
    --engine, -e        # Search engine adapter (default: duckduckgo)
    --region, -r        # Region code (default: wt-wt)
    --safesearch, -s    # Safe search level (off|moderate|strict)
    --time, -t          # Time filter (d|w|m|y)
    --output, -o        # Output file path
    --format, -f        # Output format (json|csv|txt|urls)
    --quiet, -q         # Suppress UI, output only
    --interactive, -i   # Interactive mode with live filtering
```

**Current workarounds:**

- Search works via `mh interactive` → Search menu
- Search works via `mh history replay <id>` (for re-running past searches)

---

### C) Export Command Status

| Feature | Status |
| ------- | ------ |
| `export_to_json()` function | ✅ Implemented |
| `export_to_csv()` function | ✅ Implemented |
| `export_to_txt()` function | ✅ Implemented |
| `export_to_urls()` function | ✅ Implemented |
| `mh export` command registration | ⚠️ **NOT registered** in main app |

The export module has functions but the `export` Typer app is **not added** to the main CLI (`app.add_typer(export_cmd.app, name="export")` is missing).

---

### D) Summary

| Component | Status |
| --------- | ------ |
| **CLI Framework (Typer)** | ✅ Set up |
| **Global Options** | ✅ Complete |
| **Config Command** | ✅ Complete & Integrated |
| **History Command** | ✅ Complete & Integrated |
| **Interactive Mode** | ✅ Complete & Integrated |
| **Version Command** | ✅ Complete |
| **Search Command** | ❌ **MISSING** |
| **Export Command** | ⚠️ Functions exist but not registered |
| **Input Validation** | ✅ Complete (validation.py) |

### E) Critical Gap

The **primary use case** documented in the README (`mh search "python libraries"`) **does not work** because the search command file doesn't exist and isn't registered. Users can only search through interactive mode currently.
