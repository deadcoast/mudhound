# TODO.md

## 0.0.5

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'implementing search feature'

---

- 2026-01-07

- [x] [A] Define SearchQuery data model
- [x] [B] Implement SearchEngine core
- [ ] [C] Add search CLI command
- [ ] [D] Integrate progress display
- [ ] [E] Write search tests

---

### A) Define SearchQuery Data Model

> [!IMPORTANT]
> Create Pydantic model for search queries with validation.
> Must support terms, filters, and pagination options.
> [VALIDATION.md], [ver:`0.0.5`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.5`, sect:`A)`]

**Completed:**
- Created `core/result.py` with SearchQuery model
- Added field validation for terms (non-empty)
- Added pagination: max_results, offset
- Added filter support: date_range, source

---

### B) Implement SearchEngine Core

> [!IMPORTANT]
> Core search engine with adapter pattern.
> Must support multiple search backends via adapters.
> [VALIDATION.md], [ver:`0.0.5`, sect:`B)`]
> [CHANGELOG.md], [ver:`0.0.5`, sect:`B)`]

**Completed:**
- Created `core/engine.py` with SearchEngine class
- Implemented adapter registration
- Added retry logic with exponential backoff
- Progress callbacks for UI integration

---

### C) Add Search CLI Command

> [!IMPORTANT]
> Register `mh search` command in CLI application.
> Must accept query terms and display results.
> [VALIDATION.md], [ver:`0.0.5`, sect:`C)`]
> [CHANGELOG.md], [ver:`0.0.5`, sect:`C)`]

**Scope:**
1. Create `cli/commands/search.py`
2. Register in main Typer app
3. Accept positional query argument
4. Support --max-results, --format options
5. Display results in table format

---

### D) Integrate Progress Display

> [!IMPORTANT]
> Show progress during search operations.
> Use custom Progress component from ui/.
> [VALIDATION.md], [ver:`0.0.5`, sect:`D)`]
> [CHANGELOG.md], [ver:`0.0.5`, sect:`D)`]

**Scope:**
1. Import Progress from `ui/components/progress.py`
2. Connect to SearchEngine progress callbacks
3. Display during network requests
4. Show result count on completion

---

### E) Write Search Tests

> [!IMPORTANT]
> Comprehensive tests for search functionality.
> Unit tests and property-based tests.
> [VALIDATION.md], [ver:`0.0.5`, sect:`E)`]
> [CHANGELOG.md], [ver:`0.0.5`, sect:`E)`]

**Scope:**
1. Unit tests for SearchQuery validation
2. Unit tests for SearchEngine
3. Mock adapter for testing
4. Property tests with Hypothesis
5. CLI command integration tests

---
