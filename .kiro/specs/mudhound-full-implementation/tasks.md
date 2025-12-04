# Implementation Plan

- [x] 1. Project scaffolding and core infrastructure





  - Create project directory structure following the design specification
  - Set up pyproject.toml with dependencies (typer, rich, duckduckgo-search, httpx, pydantic, tomli, tomli-w)
  - Create __init__.py files for all packages
  - Set up __main__.py entry point for `python -m mudhound`
  - _Requirements: All_

- [x] 2. Exception hierarchy and error handling





  - Implement core/exceptions.py with MudHoundError base class
  - Create ConfigError, AdapterError, AdapterNotFoundError, RateLimitError, NetworkError, ValidationError, ExportError, AnimationError
  - Add error attributes (retry_after for RateLimitError, field/message for ValidationError)
  - _Requirements: 18.4_

- [x] 3. Data models





  - Implement core/result.py with SearchResult dataclass (url, title, snippet, source, rank, metadata)
  - Create SearchOptions dataclass (max_results, region, safesearch, time_limit)
  - Create SearchStatus enum (PENDING, RUNNING, COMPLETE, FAILED, CANCELLED)
  - Create SearchQuery dataclass (id, query, engine, options, created_at, status)
  - Create SearchSession dataclass (query, results, started_at, completed_at, error) with duration and result_count properties
  - _Requirements: 5.4, 8.2_

- [x] 3.1 Write property test for SearchSession


  - **Property 26: Session data completeness**
  - **Validates: Requirements 8.2**

- [x] 4. Configuration management system





  - Implement core/config.py with ConfigManager class
  - Create config file priority chain logic (CLI → env → current dir → XDG → legacy → defaults)
  - Implement TOML parsing with tomli
  - Create default configuration schema with all sections (general, ui, animation, search, export, logging, adapters)
  - Implement get, set, list operations
  - Add config persistence with tomli-w
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 4.1 Write property test for config priority chain


  - **Property 21: Config file priority chain**
  - **Validates: Requirements 7.1**

- [x] 4.2 Write property test for config round trip


  - **Property 23: Config set-get round trip**
  - **Validates: Requirements 7.3**

- [x] 5. Terminal utilities and layout management





  - Implement utils/terminal.py with terminal size detection
  - Create ui/layout.py with LayoutManager class
  - Implement get_content_width() method with border and padding calculations
  - Add terminal resize detection and callback system
  - Implement minimum dimension enforcement (60x10)
  - Add animation engine pause/resume on resize
  - _Requirements: 1.1, 1.2, 1.5_

- [x] 5.1 Write property test for content width calculation


  - **Property 2: Content width calculation correctness**
  - **Validates: Requirements 1.2**

- [x] 5.2 Write property test for resize handling


  - **Property 1: Terminal resize triggers re-render**
  - **Validates: Requirements 1.1**

- [x] 6. Frame rendering system





  - Implement ui/frames.py with border character sets (double, single, bold, rounded, ascii)
  - Create frame rendering functions (top_border, bottom_border, header_row, footer_row, divider, content_rows)
  - Add frame anatomy support (title, tag, status, pagination)
  - Implement dynamic width adjustment based on terminal size
  - _Requirements: 1.3_

- [x] 7. Theme engine





  - Create ui/theme.py with Theme class
  - Implement TOML theme file loading from data/themes/
  - Create color palette structure (primary, secondary, accent, semantic colors, frame colors, content colors)
  - Implement semantic color name resolution to ANSI escape codes
  - Add theme application to components
  - Create fallback to default theme
  - Implement animation color scheme override support
  - Create default, minimal, and hacker themes
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 7.1 Write property test for theme loading


  - **Property 52: Theme TOML loading**
  - **Validates: Requirements 17.1**



- [x] 7.2 Write property test for color resolution


  - **Property 53: Semantic color resolution**
  - **Validates: Requirements 17.2**

- [x] 7.3 Write property test for theme fallback





  - **Property 56: Theme fallback behavior**
  - **Validates: Requirements 17.5**

- [x] 8. Glyph registry





  - Implement ui/glyphs.py with GLYPHS dictionary
  - Define status indicators ([+], [!], [~], [*], [.], [?])
  - Define progress glyphs (spinner, progress blocks, bullet, arrow, pointer)
  - Define selection glyphs ([x], [ ], (*), ( ), >>>)
  - Define decorative glyphs (divider, ellipsis, check, cross, dot)
  - Define data flow glyphs (input, output, pipe, chain)
  - _Requirements: 15.1_

- [x] 9. Core UI renderer





  - Implement ui/renderer.py with UIRenderer class
  - Create render methods for frames with theme application
  - Add ANSI escape sequence handling
  - Implement cursor management (save, restore, move, clear)
  - Add output buffering for smooth rendering
  - Integrate with LayoutManager for responsive rendering
  - _Requirements: 1.4_

- [x] 9.1 Write property test for theme application


  - **Property 3: Theme application to frames**
  - **Validates: Requirements 1.4**

- [x] 10. Animation timing engine





  - Implement ui/animation/timing.py with TimingEngine class
  - Create easing functions (linear, ease_in, ease_out, ease_in_out, bounce)
  - Implement frame rate control with configurable FPS
  - Add start, stop, pause, resume methods
  - Implement get_current_frame calculation based on elapsed time
  - Add loop control (continuous vs single-pass)
  - _Requirements: 2.2, 2.7_

- [x] 10.1 Write property test for frame rate timing


  - **Property 5: Frame rate timing accuracy**
  - **Validates: Requirements 2.2**

- [x] 10.2 Write property test for infinite loop


  - **Property 8: Infinite loop with zero duration**
  - **Validates: Requirements 2.7**

- [x] 11. Color scheme definitions





  - Implement ui/animation/schemes.py with ColorScheme enum
  - Define RAINBOW_COLORS_256 palette (196, 208, 226, 46, 51, 21, 129, 201)
  - Define DARK_RAINBOW_COLORS_256 palette (88, 130, 136, 22, 23, 18, 54, 90)
  - Define LIGHT_RAINBOW_COLORS_256 palette (210, 216, 228, 120, 123, 111, 183, 219)
  - Define WHITE_COLORS (255)
  - Create generate_rainbow_frame function with color offset algorithm
  - _Requirements: 2.3, 2.4_

- [x] 12. Asset management system





  - Implement assets/manager.py with AssetManager class
  - Create ANSI frame file parser that strips metadata headers
  - Implement frame caching with CACHE dictionary
  - Add get_banner_frames and get_logo_frames methods
  - Implement _load_animated_asset with glob pattern matching
  - Add fallback to static assets when animated frames unavailable
  - Create assets directory structure (animated/rainbow-banner/, animated/rainbow-logo/, static/)
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 12.1 Write property test for asset caching


  - **Property 9: Asset caching behavior**
  - **Validates: Requirements 3.2**

- [x] 12.2 Write property test for metadata stripping


  - **Property 10: ANSI metadata stripping**
  - **Validates: Requirements 3.3**

- [x] 12.3 Write property test for fallback assets


  - **Property 11: Fallback asset provision**
  - **Validates: Requirements 3.4**

- [x] 13. Animation renderer





  - Implement ui/animation/engine.py with AnimationRenderer class
  - Create render_frame method with cursor management (move up, clear lines)
  - Implement frame height tracking for clearing previous frames
  - Add animate method with duration support and on_complete callback
  - Integrate with TimingEngine for frame index calculation
  - Add pause/resume support for terminal resize
  - _Requirements: 2.5_

- [x] 13.1 Write property test for animation pause/resume


  - **Property 7: Animation pause and resume on resize**
  - **Validates: Requirements 2.5**
5
- [x] 14. Create sample ANSI frame files

s



  - Create placeholder ANSI frames for rainbow-banner (6 frames per scheme)
  - Create placeholder ANSI frames for rainbow-logo (6 frames per scheme)
  - Add metadata headers (scheme, frame number, width, height)
  - Create static fallback banner and logo files
  - _Requirements: 2.1, 3.5_

- [x] 15. Banner component





  - Implement ui/components/banner.py with Banner class
  - Add support for animated, static, minimal, none styles
  - Integrate with AssetManager for frame loading
  - Implement color cycling with AnimationRenderer
  - Add responsive scaling for narrow terminals
  - Integrate with configuration for style and scheme selection
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 15.1 Write property test for banner color cycling


  - **Property 32: Banner color cycling rate**
  - **Validates: Requirements 10.3**

- [x] 15.2 Write property test for banner scaling


  - **Property 33: Banner responsive scaling**
  - **Validates: Requirements 10.5**

- [x] 16. Logo component





  - Implement ui/components/logo.py with Logo class
  - Add support for inline, header, footer, floating positions
  - Integrate with AssetManager for frame loading
  - Implement animation support with color cycling
  - _Requirements: 10.1_

- [x] 17. Status and logging components





  - Implement ui/components/status.py with StatusComponent class
  - Create logging/handler.py with StyledLogHandler
  - Implement logging/formatter.py with level-based formatting
  - Add logging/levels.py with custom log levels (TRACE, SUCCESS)
  - Create LEVEL_STYLES mapping (glyph and color per level)
  - Implement timestamp formatting
  - Add file logging with rotation support
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 17.1 Write property test for log formatting


  - **Property 44: Log message formatting**
  - **Validates: Requirements 15.1**

- [x] 17.2 Write property test for log color coding


  - **Property 45: Log level color coding**
  - **Validates: Requirements 15.2**

- [x] 17.3 Write property test for file logging


  - **Property 46: File logging persistence**
  - **Validates: Requirements 15.4**

- [x] 18. Prompt component





  - Implement ui/components/prompt.py with Prompt class
  - Add support for text, number, choice, path, confirm variants
  - Implement validation with utils/validators.py (range, pattern, length, enum, custom)
  - Add error display and re-entry support
  - Implement CTRL+C handling with KeyboardInterrupt
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 18.1 Write property test for prompt display


  - **Property 35: Prompt text and cursor display**
  - **Validates: Requirements 12.1**


- [x] 18.2 Write property test for validation feedback





  - **Property 36: Validation error feedback**
  - **Validates: Requirements 12.3**


- [x] 18.3 Write property test for validation rules





  - **Property 37: Validation rule application**
  - **Validates: Requirements 12.5**

- [x] 19. Confirmation component





  - Implement ui/components/confirm.py with Confirmation class
  - Add support for yesno, yesno_yes, destructive, timed variants
  - Implement word confirmation for destructive variant
  - Add timeout support for timed variant
  - Set default to NO for destructive actions
  - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

- [x] 19.1 Write property test for confirmation display


  - **Property 48: Destructive action confirmation display**
  - **Validates: Requirements 16.1**

- [x] 19.2 Write property test for destructive word confirmation


  - **Property 49: Destructive variant word confirmation**
  - **Validates: Requirements 16.3**

- [x] 19.3 Write property test for default NO


  - **Property 51: Destructive action default NO**
  - **Validates: Requirements 16.5**

- [x] 20. Menu component





  - Implement ui/components/menu.py with Menu class
  - Add numbered option display with cursor indicator
  - Implement arrow key navigation (using rich or direct terminal input)
  - Add number key direct selection
  - Implement Enter to confirm, ESC to cancel
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 20.1 Write property test for menu option numbering


  - **Property 34: Menu option numbering**
  - **Validates: Requirements 11.1**

- [x] 21. Table component





  - Implement ui/components/table.py with Table class
  - Add column rendering for rank, URL, source
  - Implement auto-sizing based on content and terminal width
  - Add URL truncation with ellipsis
  - Implement keyboard navigation (j/k, PgUp/PgDn)
  - Add inline filtering with / key
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [x] 21.1 Write property test for table columns


  - **Property 38: Table column rendering**
  - **Validates: Requirements 13.1**

- [x] 21.2 Write property test for column auto-sizing


  - **Property 39: Table column auto-sizing**
  - **Validates: Requirements 13.2**

- [x] 21.3 Write property test for URL truncation


  - **Property 40: URL truncation with ellipsis**
  - **Validates: Requirements 13.3**

- [x] 22. Progress component





  - Implement ui/components/progress.py with Progress class
  - Add support for bar, spinner, counter, transfer, rainbow variants
  - Implement percentage calculation and display
  - Add real-time result count updates
  - Implement elapsed time display
  - Add CTRL+C cancellation support
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [x] 22.1 Write property test for progress percentage


  - **Property 41: Progress percentage display**
  - **Validates: Requirements 14.1**

- [x] 22.2 Write property test for counter updates

  - **Property 42: Progress counter updates**
  - **Validates: Requirements 14.3**

- [x] 23. Search adapter interface





  - Implement adapters/base.py with SearchAdapter abstract base class
  - Define abstract properties: name, display_name
  - Define abstract methods: search (generator), validate_options
  - Add on_rate_limit method with default implementation
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 23.1 Write property test for adapter interface compliance


  - **Property 12: Adapter interface compliance**
  - **Validates: Requirements 4.1**

- [x] 23.2 Write property test for generator-based search


  - **Property 13: Generator-based search results**
  - **Validates: Requirements 4.2**

- [x] 24. Adapter registry





  - Implement adapters/registry.py with AdapterRegistry class
  - Add register class method for adapter registration
  - Implement get method with AdapterNotFoundError
  - Add list_available method
  - Implement discovery from built-in modules
  - Add plugin discovery (mudhound_adapter_* packages) - basic structure
  - Add user adapter discovery (~/.mudhound/adapters/) - basic structure
  - _Requirements: 4.5_

- [x] 25. DuckDuckGo adapter implementation





  - Implement adapters/duckduckgo.py with DuckDuckGoAdapter class
  - Integrate duckduckgo-search library
  - Implement search method as generator yielding SearchResult objects
  - Add support for max_results, region, safesearch, time_limit options
  - Implement validate_options method
  - Add rate limit detection and on_rate_limit handling
  - Add network error handling with NetworkError exceptions
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 25.1 Write property test for max results enforcement


  - **Property 16: Max results enforcement**
  - **Validates: Requirements 5.2**

- [x] 25.2 Write property test for result structure


  - **Property 17: Search result structure completeness**
  - **Validates: Requirements 5.4**

- [-] 26. Search engine orchestration



  - Implement core/engine.py with SearchEngine class
  - Add search method that coordinates adapter, progress display, and result collection
  - Implement session management with SearchSession creation
  - Add error handling and retry logic
  - Integrate with ResultStore for persistence
  - Add cancellation support (CTRL+C)
  - _Requirements: 6.1_

- [ ] 26.1 Write property test for search initiation
  - **Property 18: Search command initiation**
  - **Validates: Requirements 6.1**

- [ ] 27. Result storage and history
  - Implement core/store.py with ResultStore class
  - Create SQLite database schema for search history
  - Implement persist method for SearchSession storage
  - Add list method for recent searches
  - Implement show method for retrieving full results by ID
  - Add replay method that retrieves original parameters
  - Implement delete and clear methods
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 27.1 Write property test for session persistence
  - **Property 25: Search session persistence**
  - **Validates: Requirements 8.1**

- [ ] 27.2 Write property test for history retrieval
  - **Property 27: History retrieval by ID**
  - **Validates: Requirements 8.4**

- [ ] 27.3 Write property test for replay parameters
  - **Property 28: History replay parameter preservation**
  - **Validates: Requirements 8.5**

- [ ] 28. Export system
  - Implement cli/commands/export.py with export command
  - Add JSON export with json.dumps
  - Add CSV export with csv.DictWriter
  - Add TXT export with formatted text
  - Add URLs export (one per line)
  - Implement file writing with error handling
  - Add ExportError for I/O failures
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 28.1 Write property test for JSON round trip
  - **Property 29: JSON export round trip**
  - **Validates: Requirements 9.1**

- [ ] 28.2 Write property test for CSV round trip
  - **Property 30: CSV export round trip**
  - **Validates: Requirements 9.2**

- [ ] 28.3 Write property test for URLs format
  - **Property 31: URLs export format**
  - **Validates: Requirements 9.4**

- [ ] 29. CLI application setup
  - Implement cli/app.py with Typer application
  - Add global options (verbose, quiet, no-color, no-animation, theme, config, help)
  - Implement version command
  - Add callback for global option processing
  - Set up command registration
  - _Requirements: 20.1, 20.2, 20.4_

- [ ] 30. Search command
  - Implement cli/commands/search.py with search command
  - Add query argument and all options (max, engine, region, safesearch, time, output, format, quiet, interactive)
  - Integrate with SearchEngine for execution
  - Implement quiet mode output suppression
  - Add output file writing
  - Implement interactive mode with live filtering
  - Add stdin support with --stdin flag
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 30.1 Write property test for quiet mode
  - **Property 19: Quiet mode output suppression**
  - **Validates: Requirements 6.3**

- [ ] 30.2 Write property test for output file writing
  - **Property 20: Output file writing**
  - **Validates: Requirements 6.4**

- [ ] 30.3 Write property test for stdin reading
  - **Property 65: Stdin query reading**
  - **Validates: Requirements 20.5**

- [ ] 31. Config command
  - Implement cli/commands/config.py with config command
  - Add list subcommand
  - Add get subcommand with key argument
  - Add set subcommand with key and value arguments
  - Add reset subcommand with confirmation
  - Add edit subcommand that opens $EDITOR
  - _Requirements: 7.3, 7.4, 7.5_

- [ ] 32. History command
  - Implement cli/commands/history.py with history command
  - Add list subcommand with limit option
  - Add show subcommand with id argument
  - Add replay subcommand with id argument
  - Add delete subcommand with id argument and confirmation
  - Add clear subcommand with confirmation
  - _Requirements: 8.3, 8.4, 8.5_

- [ ] 33. Interactive mode
  - Implement cli/commands/interactive.py with interactive command
  - Create main menu with search, history, export, config, quit options
  - Implement session state management
  - Add navigation flow (menu → operation → results → menu)
  - Implement goodbye component display on quit
  - Add CTRL+C handling with exit confirmation
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5_

- [ ] 33.1 Write property test for session state preservation
  - **Property 62: Interactive session state preservation**
  - **Validates: Requirements 19.2**

- [ ] 34. Error handler implementation
  - Implement error display formatting in ui/components/
  - Add error type classification logic
  - Create suggestion system for common errors
  - Implement verbose mode stack trace display
  - Add RateLimitError special handling with retry_after display
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ] 34.1 Write property test for error formatting
  - **Property 57: Error message formatting**
  - **Validates: Requirements 18.1**

- [ ] 34.2 Write property test for error classification
  - **Property 60: Error type classification**
  - **Validates: Requirements 18.4**

- [ ] 35. Default configuration file
  - Create data/config.default.toml with all configuration sections
  - Set sensible defaults (engine=duckduckgo, max_results=50, theme=default, animation=enabled, etc.)
  - Add comments explaining each option
  - _Requirements: 7.1_

- [ ] 36. Default theme files
  - Create data/themes/default.toml with MudHound default theme
  - Create data/themes/minimal.toml with minimal theme
  - Create data/themes/hacker.toml with hacker theme
  - Define color palettes for each theme
  - _Requirements: 17.1_

- [ ] 37. CLI argument validation
  - Implement input validation in cli/commands/
  - Add invalid argument handling with usage display
  - Set non-zero exit codes for errors
  - _Requirements: 20.3_

- [ ] 37.1 Write property test for invalid argument handling
  - **Property 64: Invalid argument handling**
  - **Validates: Requirements 20.3**

- [ ] 38. Integration and wiring
  - Wire all components together in __main__.py
  - Register DuckDuckGo adapter with AdapterRegistry
  - Initialize configuration system
  - Set up logging system
  - Connect CLI commands to core functionality
  - _Requirements: All_

- [ ] 39. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 40. Documentation
  - Create README.md with installation and usage instructions
  - Add docstrings to all public classes and methods
  - Create examples directory with sample usage
  - Document configuration options
  - Add troubleshooting guide

- [ ] 41. Build and packaging
  - Verify pyproject.toml is complete
  - Test installation with pip install -e .
  - Verify mh command works
  - Test on Windows, Linux, and Mac if possible
  - Create distribution package
