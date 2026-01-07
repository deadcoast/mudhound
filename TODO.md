# TODO.md

## 0.0.0

### A) PROTOCOL

> [!NOTE]
> This document tracks TODO items and outstanding work. It complements the main `README.md` and `Docs/design.md` documents
> The document is organized canonically by version, and is directly linked to the `CHANGELOG.md` and `VALIDATION.md` documents
> These are living documents, when one is changed, the others must be updated

---

## 0.0.1

<!-- This section is a simplified, minimal tasklist 'index' -->
> 2026-01-07

- [ ] [A] Implement `mh search` command
- [ ] [B] Register export command in CLI
- [ ] [C] Integrate custom Table component (replace rich.Table)
- [ ] [D] Integrate floating UI components (~6)
- [ ] [E] Integrate UIRenderer into CLI workflow
- [ ] [F] Integrate LayoutManager into CLI workflow
- [ ] [G] Integrate Prompt component (replace direct input())
- [ ] [H] Integrate Logo component into CLI
- [ ] [I] Integrate StatusComponent into CLI
- [ ] [J] Integrate Progress component into search workflow
- [ ] [K] Integrate ErrorHandler into CLI
- [ ] [L] Connect utils/validators.py to cli/validation.py
- [ ] [M] Use is_terminal_size_adequate() at startup

---

### A) Implement `mh search` command

> [!IMPORTANT]
> Missing Search Command - The primary CLI use case (`mh search`) isn't implemented.
> [VALIDATION.md], [ver:`0.0.2`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### B) Register export command in CLI

> [!IMPORTANT]
> Export functions exist but command not registered in main app.
> [VALIDATION.md], [ver:`0.0.2`, sect:`C)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### C) Integrate custom Table component

> [!IMPORTANT]
> Duplicated Table Functionality - Custom `Table` component exists but `rich.Table` is used in history commands.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### D) Integrate floating UI components

> [!IMPORTANT]
> ~6 Floating Components - Well-implemented but never integrated into the CLI workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### E) Integrate UIRenderer

> [!IMPORTANT]
> `ui/renderer.py`: Exported but not used in CLI workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### F) Integrate LayoutManager

> [!IMPORTANT]
> `ui/layout.py`: Exported but not used in CLI workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### G) Integrate Prompt component

> [!IMPORTANT]
> `ui/components/prompt.py`: Not used (direct `input()` used instead).
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### H) Integrate Logo component

> [!IMPORTANT]
> `ui/components/logo.py`: Only used in demo file.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### I) Integrate StatusComponent

> [!IMPORTANT]
> `ui/components/status.py`: Complete but unused.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### J) Integrate Progress component

> [!IMPORTANT]
> `ui/components/progress.py`: Complete but unused in search workflow.
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### K) Integrate ErrorHandler

> [!IMPORTANT]
> `ui/components/error.py`: Complete but unused (Rich console prints used directly).
> [VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### L) Connect validators

> [!IMPORTANT]
> `utils/validators.py` not used by `cli/validation.py` - duplicate validation logic.
> [VALIDATION.md], [ver:`0.0.4`, sect:`D)`,`F)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

### M) Terminal size check

> [!IMPORTANT]
> `is_terminal_size_adequate()` exported but never called at startup.
> [VALIDATION.md], [ver:`0.0.4`, sect:`D)`,`F)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`PENDING`]

---

## 0.0.2

<!-- Placeholder for next version -->
> YEAR-MM-DD

- [ ] [A]

### A)

> [!IMPORTANT]
> Placeholder
> [VALIDATION.md], [ver:``, sect:``]
> [CHANGELOG.md], [ver:``, sect:``]

---
