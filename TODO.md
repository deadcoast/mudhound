# TODO.md

## 0.0.0

### A) PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

## 0.0.1

- 2026-01-07

- [x] [A] Implement `mh search` command
- [x] [B] Register export command in CLI
- [x] [C] Integrate custom Table component (replace rich.Table)
- [x] [D] Integrate floating UI components (~6)
- [x] [E] Integrate UIRenderer into CLI workflow
- [x] [F] Integrate LayoutManager into CLI workflow
- [x] [G] Integrate Prompt component (replace direct input())
- [x] [H] Integrate Logo component into CLI
- [x] [I] Integrate StatusComponent into CLI
- [x] [J] Integrate Progress component into search workflow
- [x] [K] Integrate ErrorHandler into CLI
- [x] [L] Connect utils/validators.py to cli/validation.py
- [x] [M] Use is_terminal_size_adequate() at startup
- [x] [N] Fix failing tests after UI integration

---

### A) Implement `mh search` command

> [!IMPORTANT]
> Missing Search Command - The primary CLI use case (`mh search`) isn't implemented.
> [VALIDATION.md], [ver:`0.0.2`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`C)`]

### B) Register export command in CLI

> [!IMPORTANT]
> Export functions exist but command not registered in main app.
> [VALIDATION.md], [ver:`0.0.2`, sect:`C)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`C)`]

### C) Integrate custom Table component

> [!IMPORTANT]
> Duplicated Table Functionality - Custom `Table` component exists but `rich.Table` is used in history commands.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### D) Integrate floating UI components

> [!IMPORTANT]
> ~6 Floating Components - Well-implemented but never integrated into the CLI workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### E) Integrate UIRenderer

> [!IMPORTANT]
> `ui/renderer.py`: Exported but not used in CLI workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### F) Integrate LayoutManager

> [!IMPORTANT]
> `ui/layout.py`: Exported but not used in CLI workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### G) Integrate Prompt component

> [!IMPORTANT]
> `ui/components/prompt.py`: Not used (direct `input()` used instead).
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### H) Integrate Logo component

> [!IMPORTANT]
> `ui/components/logo.py`: Only used in demo file.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### I) Integrate StatusComponent

> [!IMPORTANT]
> `ui/components/status.py`: Complete but unused.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### J) Integrate Progress component

> [!IMPORTANT]
> `ui/components/progress.py`: Complete but unused in search workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### K) Integrate ErrorHandler

> [!IMPORTANT]
> `ui/components/error.py`: Complete but unused (Rich console prints used directly).
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]

### L) Connect validators

> [!IMPORTANT]
> `utils/validators.py` not used by `cli/validation.py` - duplicate validation logic.
> [VALIDATION.md], [ver:`0.0.4`, sect:`D)`,`F)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`F)`]

### M) Terminal size check

> [!IMPORTANT]
> `is_terminal_size_adequate()` exported but never called at startup.
> [VALIDATION.md], [ver:`0.0.4`, sect:`D)`,`F)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`F)`]

### N) Fix failing tests after UI integration

> [!IMPORTANT]
> UI component integrations caused 2 test failures that needed fixing.
> [VALIDATION.md], [ver:`0.0.5`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`G)`]

---

## 0.0.2

- 2026-01-07

- [ ] [A] Fix Mypy type errors in core modules
- [ ] [B] Add exception chaining (`raise ... from`) throughout codebase
- [ ] [C] Fix unused variable warnings (Ruff F841/B007)
- [ ] [D] Fix demo file type annotations

---

### A) Fix Mypy type errors in core modules

  > [!IMPORTANT]
  > 8 Mypy type errors (severity 8) across core modules requiring type annotation fixes.
  > Source: [ERRORLOG.md] - Mypy errors section
  > [VALIDATION.md], [ver:`0.0.6`, sect:`A)`]
  > [CHANGELOG.md], [ver:`0.0.2`, sect:`A)`]

  **Scope:**
- `adapters/duckduckgo.py:95` - safesearch parameter type mismatch (int→str)
- `core/config.py:179` - List[Any] assignment to Dict[str, Any]
- `core/store.py:407` - Any return type vs int declaration
- `logging/levels.py:32-33` - Logger missing trace/success attributes
- `__main__.py:87` - implicit Optional type (PEP 484)

  **Validation:** `mypy mudhound/` returns 0 errors

  ---

### B) Add exception chaining (`raise ... from`) throughout codebase

  > [!IMPORTANT]
  > ~42 Ruff B904 warnings: "Within an `except` clause, raise exceptions with `raise ... from err`"
  > This improves debugging by preserving the original exception context.
  > Source: [ERRORLOG.md] - B904 warnings section
  > [VALIDATION.md], [ver:`0.0.6`, sect:`B)`]
  > [CHANGELOG.md], [ver:`0.0.2`, sect:`B)`]

  **Pattern to apply:**

  ```python
  # Before
  except SomeException:
      raise NewException("message")

  # After
  except SomeException as err:
      raise NewException("message") from err

  Affected modules (by count):
  - adapters/duckduckgo.py (7)
  - core/config.py (10)
  - core/engine.py (3)
  - core/store.py (5)
  - cli/commands/*.py (8)
  - ui/components/*.py (5)
  - logging/handler.py (2)
  - utils/validators.py (2)

  Validation: ruff check mudhound/ --select=B904 returns 0 warnings

  ---
  C) Fix unused variable warnings (Ruff F841/B007)

  [!IMPORTANT]
  5 unused variable warnings indicating dead code or loop variable issues.
  Source: [ERRORLOG.md] - F841/B007 warnings section
  [VALIDATION.md], [ver:0.0.6, sect:C)]
  [CHANGELOG.md], [ver:0.0.2, sect:C)]

  Locations:
  - core/store.py:299 - filename assigned but never used (F841)
  - core/store.py:318 - filename assigned but never used (F841)
  - core/config.py:265 - key loop variable not used (B007 - use _)
  - ui/animation/engine.py:193 - _ loop variable unused (B007)
  - ui/renderer.py:129 - _ loop variable unused (B007)

  Validation: ruff check mudhound/ --select=F841,B007 returns 0 warnings

  ---
  D) Fix demo file type annotations

  [!IMPORTANT]
  2 type annotation issues in demo files.
  Source: [ERRORLOG.md] - Demo file errors section
  [VALIDATION.md], [ver:0.0.6, sect:D)]
  [CHANGELOG.md], [ver:0.0.2, sect:D)]

  Locations:
  - demo_files/demo_progress.py:36 - Mypy error
  - demo_files/demo_table.py:24 - Mypy error

  Validation: mypy demo_files/ returns 0 errors

  ---

  ## Corresponding VALIDATION.md Entry

  Add to VALIDATION.md under a new section `0.0.6`:

  ```markdown
  ## 0.0.6

  ### A) Mypy Type Fixes Validated
  - [ ] `mypy mudhound/` passes with 0 errors
  - [ ] Type annotations consistent with runtime behavior
  - [TODO.md], [ver:`0.0.2`, sect:`A)`]

  ### B) Exception Chaining Complete
  - [ ] `ruff check mudhound/ --select=B904` returns 0 warnings
  - [ ] All `except` blocks use `raise ... from err` pattern
  - [TODO.md], [ver:`0.0.2`, sect:`B)`]

  ### C) Unused Variables Resolved
  - [ ] `ruff check mudhound/ --select=F841,B007` returns 0 warnings
  - [ ] No dead code assignments
  - [TODO.md], [ver:`0.0.2`, sect:`C)`]

  ### D) Demo Files Type-Clean
  - [ ] `mypy demo_files/` passes with 0 errors
  - [TODO.md], [ver:`0.0.2`, sect:`D)`]

  ---
  Corresponding CHANGELOG.md Entry

  Add to CHANGELOG.md under a new section 0.0.2:

  ## 0.0.2

  ### A) Type System Improvements
  - Fixed Mypy type errors in duckduckgo adapter, config, store, and logging modules  
  - Added proper Optional type annotations per PEP 484
  - [TODO.md], [ver:`0.0.2`, sect:`A)`]

  ### B) Exception Handling Improvements
  - Added exception chaining (`raise ... from err`) throughout codebase
  - Improved debugging experience with preserved exception context
  - ~42 exception handlers updated
  - [TODO.md], [ver:`0.0.2`, sect:`B)`]

  ### C) Code Cleanup
  - Removed unused variable assignments
  - Fixed loop variable naming conventions
  - [TODO.md], [ver:`0.0.2`, sect:`C)`]

  ### D) Demo Files Cleanup
  - Fixed type annotations in demo files
  - [TODO.md], [ver:`0.0.2`, sect:`D)`]

  ---
  ★ Insight ─────────────────────────────────────
  Crown Cross-Reference Pattern: Each task creates a triad:
  - TODO.md defines the work (what to do)
  - CHANGELOG.md documents the outcome (what changed)
  - VALIDATION.md verifies completion (how to confirm)

  The [DOCUMENT.md], [ver:X, sect:Y] syntax creates navigable links between documents.
  ─────────────────────────────────────────────────

  ---
  The spec groups the ~55 individual linter errors into 4 actionable tasks (A-D) with:
  - Clear scope boundaries
  - Validation commands that return 0 errors/warnings
  - Cross-references to maintain crown document synchronization
  - The ERRORLOG.md JSON dump remains the source of truth for specific line numbers 

## 0.0.3

- YEAR-MM-DD

- [ ] [A] Placeholder

---

### A) Placeholder

> [!IMPORTANT]
> Placeholder for next version.
> [VALIDATION.md], [ver:`0.0.5`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.2`, sect:`A)`]

---
