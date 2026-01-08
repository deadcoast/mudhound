# TODO.md - Example from MudHound

## 0.0.1

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

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

---

## Key Patterns Demonstrated

1. **Task checklist** with letter identifiers: `- [x] [A] Description`
2. **Section details** matching letters: `### A) Title`
3. **Cross-references** to related documents:
   - `[VALIDATION.md], [ver:X.X.X, sect:Y)]`
   - `[CHANGELOG.md], [ver:X.X.X, sect:Y)]`
4. **Blockquote metadata** with `> [!IMPORTANT]`
