# MUDHOUND - Design Document

## Overview

MudHound is a terminal-based batch URL extraction tool that combines powerful search capabilities with an elegant animated interface. The system follows a modular layered architecture with five distinct layers: Presentation (UI rendering and animation), Interaction (user input components), Command (CLI commands), Core (business logic), and Adapter (search engine integrations).

The application emphasizes visual polish through a sophisticated animation system featuring rainbow color cycling, ANSI art banners, and responsive terminal components. All UI elements adapt dynamically to terminal dimensions and support multiple themes and color schemes.

## Architecture

### Layer Stack

The system is organized into five architectural layers:

**Presentation Layer**: Handles all terminal rendering, including the UIRenderer for output, FrameEngine for borders, ThemeEngine for colors, LayoutManager for responsive sizing, and AnimationEngine for animated graphics.

**Interaction Layer**: Provides user input components including Prompts for text entry, Menus for navigation, Validators for input checking, and Confirmations for destructive actions.

**Command Layer**: Implements CLI commands (search, config, export, history) with extensibility for future plugins.

**Core Layer**: Contains business logic including SearchEngine for orchestration, ResultStore for persistence, Logging for diagnostics, and ConfigManager for settings.

**Adapter Layer**: Provides pluggable search engine integrations with DuckDuckGo as the primary implementation and extensibility for Google, Bing, and custom adapters.

### Directory Structure

```
mudhound/
├── cli/              # Command layer (Typer app, commands, callbacks)
├── ui/               # Presentation layer (renderer, frames, layout, theme, animation/, components/)
├── core/             # Core layer (engine, result, store, config, exceptions)
├── adapters/         # Adapter layer (base, duckduckgo, registry)
├── assets/           # Static and animated ANSI art files
├── logging/          # Logging subsystem (handler, formatter, levels)
├── utils/            # Utilities (terminal, text, validators)
└── data/             # Default configuration and themes
```

## Components and Interfaces

### Animation System

**AnimationEngine**: Central controller that coordinates frame loading, timing, and rendering. Manages pause/resume during terminal resize events.

**TimingEngine**: Controls frame timing with configurable FPS (default 10) and easing functions (linear, ease-in, ease-out, ease-in-out, bounce). Calculates current frame index based on elapsed time.

**AnimationRenderer**: Handles terminal-specific rendering with cursor management. Clears previous frames by moving cursor up and clearing lines, then renders new frame.

**AssetManager**: Loads and caches ANSI frame files from disk. Parses frame metadata headers and provides fallback to static assets when animated frames are unavailable.

**ColorScheme**: Enum defining available schemes (rainbow, dark-rainbow, light-rainbow, white, theme). Each scheme maps to specific ANSI 256 color palettes.

### UI Framework

**LayoutManager**: Manages terminal dimensions with minimum 60 columns × 10 rows. Polls terminal size on each render, triggers re-renders on resize, and pauses animations during resize operations.

**FrameEngine**: Renders ASCII borders using configurable character sets (double, single, bold, rounded, ascii). Supports headers, footers, dividers, and content padding.

**ThemeEngine**: Resolves semantic color names (success, error, warning, info) to terminal escape codes. Loads theme definitions from TOML files with fallback chain.

**UIRenderer**: Core rendering engine that outputs formatted content to terminal. Applies themes, manages frames, and coordinates with animation system.

### UI Components

**Banner**: Animated ASCII art header with configurable styles (animated, static, minimal, none). Supports all color schemes with horizontal color cycling at configured FPS.

**Logo**: Compact animated logo for inline display, headers, footers, or floating positions.

**Menu**: Interactive selection component with arrow key navigation, number key direct selection, and ESC to cancel.

**Prompt**: Input component with variants (text, number, choice, path, confirm) and validation support (range, pattern, length, enum, custom).

**Table**: Data display with auto-sizing columns, URL truncation, keyboard navigation (j/k), and inline filtering (/).

**Progress**: Progress indicators with variants (bar, spinner, counter, transfer, rainbow). Shows percentage, elapsed time, and real-time updates.

**Status**: Log message display with timestamps, level-based glyphs ([+], [*], [~], [!]), and color coding.

**Confirmation**: Destructive action prompts with variants (yesno, yesno_yes, destructive, timed). Defaults to NO for safety.

### Search System

**SearchAdapter (ABC)**: Abstract base defining interface for search engines. Requires name, display_name, search (generator), validate_options, and optional on_rate_limit methods.

**DuckDuckGoAdapter**: Concrete implementation using duckduckgo-search library. Supports max_results, region, safesearch, and time_limit options. Yields SearchResult objects with url, title, snippet, source, rank.

**AdapterRegistry**: Discovers and manages adapters from built-in modules, plugin packages (mudhound_adapter_*), and user directories (~/.mudhound/adapters/).

**SearchEngine**: Orchestrates search operations, manages sessions, handles errors, and coordinates with result store.

**ResultStore**: Persists search sessions to SQLite database. Stores query, results, timestamps, status, and error information.

### Configuration System

**ConfigManager**: Loads configuration from priority chain: CLI override → environment variable → current directory → XDG standard → legacy location → internal defaults. Parses TOML format with validation.

**Configuration Schema**: Sections for general settings, UI preferences, animation options, search defaults, export settings, logging configuration, and adapter-specific options.

## Data Models

### Core Models

**SearchResult**: Individual result with url, title, snippet, source, rank, and metadata dict.

**SearchOptions**: Configuration with max_results (default 50), region (default "wt-wt"), safesearch (default "moderate"), and optional time_limit.

**SearchQuery**: Request representation with id, query string, engine name, options, created_at timestamp, and status enum.

**SearchSession**: Complete session with query, results list, started_at, completed_at, optional error, and computed duration/result_count properties.

**SearchStatus**: Enum with states PENDING, RUNNING, COMPLETE, FAILED, CANCELLED.

### Storage Schema

```
~/.mudhound/
├── config.toml              # User configuration
├── history.db               # SQLite: search history
├── cache/                   # Temporary result cache
│   └── <session_id>.json
├── exports/                 # Default export location
└── logs/
    ├── mudhound.log
    └── mudhound.log.1       # Rotated logs
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Terminal UI Framework Properties

Property 1: Terminal resize triggers re-render
*For any* terminal resize event, all visible components should be re-rendered with dimensions recalculated to match the new terminal size.
**Validates: Requirements 1.1**

Property 2: Content width calculation correctness
*For any* terminal width, the calculated content width should equal terminal width minus frame borders minus padding (term_width - 4 for double borders with standard padding).
**Validates: Requirements 1.2**

Property 3: Theme application to frames
*For any* frame and any active theme, rendering the frame should apply the theme's color palette to all frame elements.
**Validates: Requirements 1.4**

### Animation System Properties

Property 4: Asset loading on first access
*For any* valid color scheme, requesting banner or logo frames should load the corresponding ANSI files from the assets directory on first access.
**Validates: Requirements 2.1**

Property 5: Frame rate timing accuracy
*For any* configured frame rate, the animation engine should render frames at approximately that rate (within 10% tolerance).
**Validates: Requirements 2.2**

Property 6: Color scheme application
*For any* color scheme selection, all animation frames should have the scheme's color transformations applied consistently.
**Validates: Requirements 2.3**

Property 7: Animation pause and resume on resize
*For any* terminal resize event during animation, the animation should pause, allow re-render, and resume playback without frame loss.
**Validates: Requirements 2.5**

Property 8: Infinite loop with zero duration
*For any* animation with duration set to zero, the animation should continue looping until explicitly stopped.
**Validates: Requirements 2.7**

### Asset Management Properties

Property 9: Asset caching behavior
*For any* asset loaded from disk, subsequent accesses to the same asset should return the cached version without additional disk I/O.
**Validates: Requirements 3.2**

Property 10: ANSI metadata stripping
*For any* ANSI frame file with metadata header, parsing should strip all lines before the "---" separator.
**Validates: Requirements 3.3**

Property 11: Fallback asset provision
*For any* requested asset that does not exist, the asset manager should provide a static fallback asset instead of failing.
**Validates: Requirements 3.4**

### Search Adapter Properties

Property 12: Adapter interface compliance
*For any* search adapter implementation, it should implement all required methods: name, display_name, search, and validate_options.
**Validates: Requirements 4.1**

Property 13: Generator-based search results
*For any* search execution, the adapter should yield results as a generator (not return a list).
**Validates: Requirements 4.2**

Property 14: Validation error list return
*For any* search options validation, the adapter should return a list of error messages (empty list if valid).
**Validates: Requirements 4.3**

Property 15: Rate limit handling
*For any* rate limit detection, the adapter should invoke on_rate_limit and return a numeric wait duration in seconds.
**Validates: Requirements 4.4**

Property 16: Max results enforcement
*For any* max_results value specified, the DuckDuckGo adapter should return at most that number of results.
**Validates: Requirements 5.2**

Property 17: Search result structure completeness
*For any* search result yielded by the DuckDuckGo adapter, it should contain all required fields: url, title, snippet, source, and rank.
**Validates: Requirements 5.4**

### Command Layer Properties

Property 18: Search command initiation
*For any* query string provided to "mh search", the command should initiate a search with that exact query.
**Validates: Requirements 6.1**

Property 19: Quiet mode output suppression
*For any* search executed with quiet mode enabled, no UI output should be produced (only result data).
**Validates: Requirements 6.3**

Property 20: Output file writing
*For any* valid output path specified, search results should be written to that file path.
**Validates: Requirements 6.4**

### Configuration Properties

Property 21: Config file priority chain
*For any* set of configuration files present, the configuration manager should load from the first file found in priority order (CLI override → env var → current dir → XDG → legacy → defaults).
**Validates: Requirements 7.1**

Property 22: TOML parsing success
*For any* valid TOML configuration file, the configuration manager should parse it without errors.
**Validates: Requirements 7.2**

Property 23: Config set-get round trip
*For any* key-value pair, setting a config value then getting it should return the same value.
**Validates: Requirements 7.3**

Property 24: Config key retrieval
*For any* configuration key that exists, getting the key should return its current value.
**Validates: Requirements 7.4**

### Result Storage Properties

Property 25: Search session persistence
*For any* completed search, the result store should persist the SearchSession to the history database.
**Validates: Requirements 8.1**

Property 26: Session data completeness
*For any* stored search session, it should contain all required fields: query, results, timestamps, status, and error (if applicable).
**Validates: Requirements 8.2**

Property 27: History retrieval by ID
*For any* valid search ID, executing "mh history show <id>" should retrieve and display the full results for that search.
**Validates: Requirements 8.4**

Property 28: History replay parameter preservation
*For any* search ID, replaying the search should use the exact same parameters (query, engine, options) as the original search.
**Validates: Requirements 8.5**

### Export Properties

Property 29: JSON export round trip
*For any* search results, exporting to JSON then parsing the JSON should produce equivalent result data.
**Validates: Requirements 9.1**

Property 30: CSV export round trip
*For any* search results, exporting to CSV then parsing the CSV should produce equivalent result data.
**Validates: Requirements 9.2**

Property 31: URLs export format
*For any* search results, exporting with format "urls" should produce one URL per line with no additional formatting.
**Validates: Requirements 9.4**

### UI Component Properties

Property 32: Banner color cycling rate
*For any* configured frame rate, the animated banner should cycle colors at that rate.
**Validates: Requirements 10.3**

Property 33: Banner responsive scaling
*For any* terminal width less than the banner width, the banner should scale down gracefully without breaking layout.
**Validates: Requirements 10.5**

Property 34: Menu option numbering
*For any* menu displayed, all options should be numbered sequentially and a cursor indicator should be visible.
**Validates: Requirements 11.1**

Property 35: Prompt text and cursor display
*For any* prompt displayed, both the prompt text and input cursor should be visible.
**Validates: Requirements 12.1**

Property 36: Validation error feedback
*For any* invalid input to a prompt, an error message should be displayed and re-entry should be allowed.
**Validates: Requirements 12.3**

Property 37: Validation rule application
*For any* validation rule (range, pattern, length, enum, custom), the prompt should correctly apply the rule to input.
**Validates: Requirements 12.5**

Property 38: Table column rendering
*For any* search results displayed in a table, columns for rank, URL, and source should all be rendered.
**Validates: Requirements 13.1**

Property 39: Table column auto-sizing
*For any* content and terminal dimensions, table columns should be sized to fit within the terminal width.
**Validates: Requirements 13.2**

Property 40: URL truncation with ellipsis
*For any* URL exceeding the column width, the table should truncate it and append ellipsis.
**Validates: Requirements 13.3**

Property 41: Progress percentage display
*For any* progress value between 0 and 100, the progress bar should display the correct percentage.
**Validates: Requirements 14.1**

Property 42: Progress counter updates
*For any* new result received during search, the progress component should increment the result count.
**Validates: Requirements 14.3**

Property 43: Elapsed time display
*For any* elapsed time during an operation, the progress component should display it in the footer.
**Validates: Requirements 14.4**

### Logging Properties

Property 44: Log message formatting
*For any* log message emitted, it should be displayed with a timestamp and the level-appropriate glyph ([+], [*], [~], [!], etc.).
**Validates: Requirements 15.1**

Property 45: Log level color coding
*For any* log level, the status component should apply the correct color (success=green, error=red, warning=yellow, info=blue).
**Validates: Requirements 15.2**

Property 46: File logging persistence
*For any* log entry when file logging is enabled, the entry should be written to the configured log file path.
**Validates: Requirements 15.4**

Property 47: Log file rotation
*For any* log file exceeding the maximum size, the logging system should rotate the file and maintain the configured backup count.
**Validates: Requirements 15.5**

### Confirmation Properties

Property 48: Destructive action confirmation display
*For any* destructive action requested, a confirmation prompt with YES/NO options should be displayed.
**Validates: Requirements 16.1**

Property 49: Destructive variant word confirmation
*For any* confirmation with destructive variant, typing a confirmation word should be required to proceed.
**Validates: Requirements 16.3**

Property 50: Timed confirmation auto-cancel
*For any* confirmation with timed variant, the prompt should auto-cancel after the configured timeout.
**Validates: Requirements 16.4**

Property 51: Destructive action default NO
*For any* destructive action confirmation (unless yesno_yes variant), the default selection should be NO.
**Validates: Requirements 16.5**

### Theme Properties

Property 52: Theme TOML loading
*For any* valid theme TOML file in the themes directory, the theme engine should load it successfully.
**Validates: Requirements 17.1**

Property 53: Semantic color resolution
*For any* semantic color name (success, error, warning, info), the theme engine should resolve it to a valid terminal escape code.
**Validates: Requirements 17.2**

Property 54: Theme application to components
*For any* component requesting a style and any active theme, the theme's color palette should be applied to the component.
**Validates: Requirements 17.3**

Property 55: Animation scheme override
*For any* theme with animation color scheme override configured, the override should be applied instead of the default scheme.
**Validates: Requirements 17.4**

Property 56: Theme fallback behavior
*For any* requested theme that does not exist, the theme engine should fall back to the default theme.
**Validates: Requirements 17.5**

### Error Handling Properties

Property 57: Error message formatting
*For any* error that occurs, the error handler should display a formatted message with error type and description.
**Validates: Requirements 18.1**

Property 58: Common error suggestions
*For any* common error scenario (network timeout, file not found, etc.), the error handler should provide actionable suggestions.
**Validates: Requirements 18.2**

Property 59: Verbose mode stack traces
*For any* error when verbose mode is enabled, the error handler should include stack traces and detailed diagnostics.
**Validates: Requirements 18.3**

Property 60: Error type classification
*For any* error, the error handler should correctly classify it as ConfigError, AdapterError, NetworkError, ValidationError, ExportError, or AnimationError.
**Validates: Requirements 18.4**

Property 61: Rate limit error retry display
*For any* RateLimitError, the error handler should display the retry_after duration and suggest waiting.
**Validates: Requirements 18.5**

### Interactive Mode Properties

Property 62: Interactive session state preservation
*For any* sequence of operations in interactive mode, session state should be maintained across all operations.
**Validates: Requirements 19.2**

Property 63: Search completion navigation
*For any* search that completes in interactive mode, results should be displayed and the main menu should be redisplayed.
**Validates: Requirements 19.3**

### CLI Properties

Property 64: Invalid argument handling
*For any* invalid command-line arguments provided, the CLI should display usage information and exit with non-zero status.
**Validates: Requirements 20.3**

Property 65: Stdin query reading
*For any* input provided via stdin when --stdin flag is used, the CLI should read it as the search query.
**Validates: Requirements 20.5**

## Error Handling

### Exception Hierarchy

All MudHound errors inherit from `MudHoundError` base exception:

- **ConfigError**: Configuration file parsing, validation, or access errors
- **AdapterError**: Base for search adapter errors
  - **AdapterNotFoundError**: Requested adapter not registered
  - **RateLimitError**: Rate limit exceeded (includes retry_after duration)
  - **NetworkError**: Network connectivity or timeout issues
- **ValidationError**: Input validation failures (includes field and message)
- **ExportError**: Export operation failures (file I/O, format errors)
- **AnimationError**: Animation system errors (asset loading, rendering)

### Error Display Strategy

Errors are displayed in framed boxes with:
- Error type and description
- Contextual suggestions for resolution
- Optional verbose details (stack traces) with -v flag
- Appropriate glyph and color coding

### Recovery Mechanisms

- **Network errors**: Automatic retry with exponential backoff (configurable retry_count and retry_delay)
- **Rate limits**: Respect retry_after duration from adapter
- **Config errors**: Fall back to defaults, warn user
- **Asset errors**: Fall back to static assets
- **Validation errors**: Allow re-entry with error feedback

## Testing Strategy

### Property-Based Testing

The project uses **Hypothesis** for Python as the property-based testing library. Each correctness property will be implemented as a property-based test with minimum 100 iterations.

Property-based tests will:
- Generate random valid inputs (terminal sizes, queries, configurations, etc.)
- Verify universal properties hold across all generated inputs
- Use appropriate strategies for each data type (integers for dimensions, strings for queries, enums for color schemes)
- Be tagged with comments referencing the design document property number

Example property test structure:
```python
from hypothesis import given, strategies as st

@given(
    terminal_width=st.integers(min_value=60, max_value=300),
    border_width=st.just(4)
)
def test_content_width_calculation(terminal_width, border_width):
    """
    Feature: mudhound-full-implementation, Property 2: Content width calculation correctness
    """
    layout_manager = LayoutManager()
    layout_manager._cached_size = (terminal_width, 24)
    
    content_width = layout_manager.get_content_width()
    
    assert content_width == terminal_width - border_width
```

### Unit Testing

Unit tests complement property tests by covering:
- Specific examples of correct behavior (e.g., specific border sets render correctly)
- Edge cases identified in requirements (e.g., minimum terminal dimensions)
- Integration points between components
- Error conditions and exception handling

Unit tests will use **pytest** framework with fixtures for common test data.

### Test Organization

```
tests/
├── unit/
│   ├── test_ui_framework.py
│   ├── test_animation.py
│   ├── test_adapters.py
│   ├── test_config.py
│   └── test_export.py
├── property/
│   ├── test_ui_properties.py
│   ├── test_animation_properties.py
│   ├── test_adapter_properties.py
│   ├── test_config_properties.py
│   └── test_export_properties.py
└── fixtures/
    ├── sample_configs.py
    ├── sample_results.py
    └── mock_adapters.py
```

### Testing Configuration

- Property tests: 100 iterations minimum per test
- Coverage target: 80% code coverage
- CI/CD: Run all tests on every commit
- Performance tests: Verify animation frame rates, search response times

## Implementation Notes

### Critical Path

1. **Foundation**: UI framework and layout management must be solid before building components
2. **Animation**: Asset management and timing engine are prerequisites for animated components
3. **Search**: Adapter interface must be stable before implementing DuckDuckGo adapter
4. **Integration**: CLI commands tie everything together and should be implemented last

### Performance Considerations

- **Asset caching**: Load ANSI frames once, cache in memory
- **Lazy loading**: Load assets only when needed (e.g., don't load all color schemes upfront)
- **Generator-based search**: Stream results to avoid memory overhead
- **Animation optimization**: Pre-render frames, use efficient cursor management

### Platform Compatibility

- **Windows**: Use colorama for ANSI support, handle different line endings
- **Linux/Mac**: Native ANSI support, standard terminal behavior
- **Terminal emulators**: Test with common emulators (Windows Terminal, iTerm2, GNOME Terminal)

### Dependencies Rationale

- **Typer**: Modern CLI framework with excellent type hints and automatic help generation
- **Rich**: Terminal rendering utilities for colors, tables, progress bars
- **duckduckgo-search**: No API key required, good rate limits
- **httpx**: Modern async HTTP client for future extensibility
- **Pydantic**: Data validation with excellent error messages
- **tomli/tomli-w**: Standard TOML parsing for Python <3.11 compatibility
- **Hypothesis**: Industry-standard property-based testing library

## Future Extensibility

### Plugin Architecture

The adapter registry pattern enables:
- Third-party search engine adapters
- Custom export formats
- Theme packages
- Command extensions

### Configuration Extensibility

TOML configuration supports:
- Per-adapter settings
- Custom color schemes
- User-defined validators
- Hook system for automation

### API Considerations

While MudHound is primarily a CLI tool, the core layer is designed to be importable:
```python
from mudhound.core import SearchEngine
from mudhound.adapters import DuckDuckGoAdapter

engine = SearchEngine(adapter=DuckDuckGoAdapter())
results = list(engine.search("python libraries", max_results=10))
```

This enables:
- Integration into other Python projects
- Programmatic search automation
- Custom UI implementations
