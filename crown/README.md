# crown

AI-optimized documentation ecosystem for Claude Code. Structured workflows for task tracking, codebase review, and cross-referenced documentation.

## What is crown?

crown provides Claude Code with a systematic approach to:

1. **Track Work** - TODO.md with version-controlled task lists
2. **Record Completions** - CHANGELOG.md with cross-referenced entries
3. **Verify Outcomes** - VALIDATION.md with test/lint results
4. **Review Codebases** - SD.md (SeekAndDestroy) systematic analysis

All documents are interconnected through cross-references:
```
[TODO.md], [ver:`0.0.1`, sect:`A)`]
```

## Installation

### Option 1: Plugin Directory
```bash
claude --plugin-dir /path/to/crown
```

### Option 2: Copy to Project
Copy the `crown/` folder into your project directory and load with `--plugin-dir`.

## Quick Start

### Initialize crown
```
/init myproject
```

Creates:
- TODO.md, CHANGELOG.md, VALIDATION.md, SD.md
- Folder structure (docs/TODO/complete/, docs/SD/complete/)
- Docs/crown.md specification
- Auto-detected quadrant configuration

### Check Status
```
/status
```

Shows current state of all documents, active workflow, suggested next action.

### Track Work
```
/todo
```

Works through pending tasks, updates cross-references, archives completed versions.

### Review Codebase
```
/sd R
```

Begins SeekAndDestroy workflow - systematic codebase analysis with INTEGRATION OVER DELETION principle.

## Commands

All commands appear with `(plugin:crown)` label in `/help`.

| Command | Description |
|---------|-------------|
| `/init [name]` | Initialize crown in repository |
| `/status` | Display ecosystem state |
| `/todo [letter]` | Execute TODO workflow |
| `/sd [phase] [quadrant]` | Execute SD workflow |
| `/validate` | Validate cross-references |
| `/continue` | Resume from current state |

## Core Principles

### 1. Cross-Reference Everything

Every action creates traceable links between documents:
```
[TODO.md], [ver:`0.0.1`, sect:`A)`]    # Task source
[CHANGELOG.md], [ver:`0.0.1`, sect:`A)`] # Completion record
[VALIDATION.md], [ver:`0.0.1`, sect:`A)`] # Verification
```

### 2. Integration Over Deletion

> **NEVER delete unused code first.**

The SD workflow finds unused code and investigates WHY it exists, then finds where it SHOULD be used. Deletion requires explicit user approval.

### 3. Token Efficiency

- Archive completed versions to reduce context size
- Reference instead of duplicate content
- Keep LIVE documents minimal

## Document Structure

### TODO.md
```markdown
## 0.0.1

### PROTOCOL
> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking tasks'

---

- [ ] [A] Pending task
- [x] [B] Complete task

---

### A) Task Title
> [!IMPORTANT]
> Description
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
```

### CHANGELOG.md
```markdown
## 0.0.1

> [!IMPORTANT]
> Version summary
> [TODO.md], [ver:`0.0.1`]

### A) Category - COMPLETE

| Component | Status | Reference |
|-----------|--------|-----------|
| Feature | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
```

### SD.md
```markdown
## 0.0.1

### PROTOCOL
> [!NOTE]
> status: 'scanning Q1'
> principle: INTEGRATION OVER DELETION

### Quadrant Summary
| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | core/ | 25 | IN_PROGRESS |
```

## SD Workflow Phases

| Phase | Command | Description |
|-------|---------|-------------|
| R | `/sd R` | Recon - map quadrants |
| S | `/sd S Q1` | Scan - analyze quadrant |
| F | `/sd F` | Flag - organize findings |
| X | `/sd X` | Resolve - execute integrations |
| V | `/sd V` | Verify - run tests, archive |

## Finding Types

| Type | Meaning | Resolution |
|------|---------|------------|
| U | UNUSED | Find integration point |
| I | INTEGRATION | Add missing connections |
| T | TYPE | Add type annotations |
| P | PATTERN | Refactor to standard |

## File Organization

```
project/
├── TODO.md           # LIVE tasks
├── CHANGELOG.md      # Completion history
├── VALIDATION.md     # Verification records
├── SD.md             # LIVE codebase review
├── Docs/
│   └── crown.md      # Specification
└── docs/
    ├── TODO/
    │   └── complete/ # Archived versions
    └── SD/
        └── complete/ # Completed passes
```

## Skills

crown includes three skills:

- **crown-format** - Document structure and cross-reference syntax
- **crown-workflow** - TODO and SD workflow execution
- **crown-context** - Codebase mapping and context feeding

## Agent

The `crown` agent triggers automatically when users ask about:
- Project state or progress
- Tracking work or tasks
- Codebase review
- Documentation status
- Continuing interrupted work

## Hooks

Hooks automatically:
- Validate cross-references when crown documents change
- Detect version completion and suggest archiving
- Suggest next SD phase after updates

## Example Session

```
User: /init myproject

Claude: crown initialized!
        TODO.md [ver:0.0.1]
        Quadrants: Q1(25), Q2(18), Q3(42), Q4(67)

User: /sd R

Claude: Recon complete.
        Q1: core/, adapters/ (25 files)
        Q2: cli/, commands/ (18 files)
        Next: /sd S Q1

User: /sd S Q1

Claude: Scanning Q1...
        Finding 1: calculate_cache_key (UNUSED, HIGH)
        - Investigation: Cache infrastructure not connected
        - Integration path: Add to SearchEngine.search()
        TODO entry created: [TODO.md], [ver:`0.0.1`, sect:`A)`]

User: /todo A

Claude: Working on task A: Integrate cache...
        [implementation]
        Task [A] complete.
        CHANGELOG updated.
        VALIDATION updated.
```

## License

MIT
