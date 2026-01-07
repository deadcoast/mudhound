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

- YEAR-MM-DD

- [ ] [A] Placeholder

---

### A) Placeholder

> [!IMPORTANT]
> Placeholder for next version.
> [VALIDATION.md], [ver:`0.0.5`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.2`, sect:`A)`]

---
