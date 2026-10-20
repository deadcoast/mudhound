# Crown Documentation Specification

## 0.0.0

### PROTOCOL

> [!NOTE]
> purpose: AI-optimized document ecosystem for Claude Code
> dependencies: TODO.md, CHANGELOG.md, VALIDATION.md, SD.md
> status: 'specification'

---

## Overview

Crown is an AI-optimized documentation ecosystem designed for Claude Code. It provides structured workflows for:

1. **Task Tracking** - TODO.md with version-controlled task lists
2. **Completion Recording** - CHANGELOG.md with cross-referenced entries
3. **Verification Tracking** - VALIDATION.md with test and verification results
4. **Codebase Review** - SD.md (SeekAndDestroy) systematic analysis

All documents are interconnected through a cross-reference tagging system that enables:
- Full traceability from origin to verification
- Token-efficient context loading
- Version-split archives for history preservation
- AI agent navigation through structured references

---

## Core Documents

### TODO.md

> [!NOTE]
> alias: `/crown:todo`
> purpose: Task tracking and work items
> location: TODO.md (LIVE in root)
> archive: docs/TODO/complete/, docs/TODO/pending/

**Structure:**
```markdown
# TODO.md

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'description of current state'

---

- YYYY-MM-DD

- [ ] [A] Task description
- [x] [B] Completed task

---

### A) Task Title

> [!IMPORTANT]
> Detailed description of the task.
> [VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]

---
```

**Lifecycle:**
1. Tasks added with `- [ ] [LETTER] Description`
2. Work performed on task
3. Task marked complete `- [x] [LETTER]`
4. Cross-references created to CHANGELOG and VALIDATION
5. When all tasks complete, version archived to docs/TODO/complete/

### CHANGELOG.md

> [!NOTE]
> alias: `/crown:status` (for viewing)
> purpose: Completion tracking and release history
> location: CHANGELOG.md (root, not archived)

**Structure:**
```markdown
# Changelog

## 0.0.0

### A) PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, VALIDATION.md
> status: 'tracking completed work'

---

## X.X.X

- YYYY-MM-DD

> [!IMPORTANT]
> Summary of this version's work
> [TODO.md], [ver:`X.X.X`]
> [VALIDATION.md], [ver:`X.X.X`]

### A) Category - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| Feature | ✅ | [VALIDATION.md], [ver:`X.X.X`, sect:`A)`] |

---
```

### VALIDATION.md

> [!NOTE]
> alias: `/crown:validate` (for checking)
> purpose: Verification and integration status
> location: VALIDATION.md (root, not archived)

**Structure:**
```markdown
# Validation

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking validation findings'

---

- YYYY-MM-DD

### A) Component - VERIFIED

> [!NOTE]
> Description of what was verified
> [TODO.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]

**Verification:**
- pytest: N passed, N failed
- mypy: clean
- ruff: clean

---
```

### SD.md

> [!NOTE]
> alias: `/crown:sd`
> purpose: Systematic codebase review
> location: SD.md (LIVE in root)
> archive: docs/SD/complete/, docs/SD/pending/
> principle: INTEGRATION OVER DELETION

**Structure:**
```markdown
# SeekAndDestroy

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: 'current phase status'
> principle: INTEGRATION OVER DELETION

---

- YYYY-MM-DD

### Quadrant Summary

| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | core/, adapters/ | 25 | PENDING |
| Q2 | cli/, commands/ | 18 | COMPLETE |
| Q3 | ui/, components/ | 42 | IN_PROGRESS |
| Q4 | tests/, utils/ | 67 | PENDING |

---

### Findings

| ID | Location | Type | Severity | Status |
|----|----------|------|----------|--------|
| 1 | file.py:45 | U | HIGH | NEW |

---
```

---

## Cross-Reference System

### Format

The ONLY valid cross-reference format:
```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

### Components

| Component | Syntax | Example |
| ----------- | -------- | --------- |
| Document | `[NAME.md]` | `[TODO.md]` |
| Version | `[ver:\`X.X.X\`]` | `[ver:\`0.0.1\`]` |
| Section | `[sect:\`Y)\`]` | `[sect:\`A)\`]` |

### Variations

**Document + Version:**
```
[TODO.md], [ver:`0.0.1`]
```

**Document + Version + Section:**
```
[CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

**Multiple Sections:**
```
[VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
```

**Multiple Versions:**
```
[TODO.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

**Section Range:**
```
[TODO.md], [ver:`0.0.1`, sect:`C)`-`N)`]
```

### Flow

```
Origin (user request, SD finding, bug report)
    ↓
[TODO.md], [ver:X.X.X, sect:A)] ← Task created
    ↓
Work performed
    ↓
[CHANGELOG.md], [ver:X.X.X, sect:A)] ← Completion recorded
    ↓
[VALIDATION.md], [ver:X.X.X, sect:A)] ← Verification documented
    ↓
Archive to docs/*/complete/
```

---

## Blockquote Types

### [!NOTE]
Metadata, protocol information, informational content.

### [!IMPORTANT]
Task descriptions, key information requiring attention.

### [!WARNING]
SD findings, issues discovered, problems identified.

### [!TIP]
Navigation hints, next steps, helpful suggestions.

### [!CAUTION]
Critical rules that MUST be followed.

---

## File Organization

```
PROJECT_ROOT/
├── TODO.md              # LIVE task tracking
├── CHANGELOG.md         # Completion history
├── VALIDATION.md        # Verification records
├── SD.md                # LIVE codebase review
│
├── Docs/
│   └── crown.md         # Project-specific crown spec
│
├── docs/
│   ├── TODO/
│   │   ├── complete/    # Archived TODO versions
│   │   │   ├── 0.0.1.md
│   │   │   └── 0.0.2.md
│   │   └── pending/     # Incomplete TODO versions
│   │
│   └── SD/
│       ├── complete/    # Completed SD passes
│       │   ├── 0.0.1-Q1.md
│       │   └── 0.0.1-Q3.md
│       └── pending/     # Incomplete passes
│
└── templates/           # Document templates
    ├── TODO.template.md
    ├── CHANGELOG.template.md
    ├── VALIDATION.template.md
    └── SD.template.md
```

---

## SD Workflow

### Phases

| Phase | Command | Purpose |
| ------- | --------- | --------- |
| R | `/crown:sd R` | Recon - map quadrants |
| S | `/crown:sd S Q1` | Scan - analyze quadrant |
| F | `/crown:sd F` | Flag - organize findings |
| X | `/crown:sd X` | Resolve - execute integrations |
| V | `/crown:sd V` | Verify - run tests, archive |

### Finding Types

| Type | Name | Resolution |
| ------ | ------ | ------------ |
| U | UNUSED | Find integration point |
| I | INTEGRATION | Add missing connections |
| T | TYPE | Add type annotations |
| P | PATTERN | Refactor to standard |

### Severity Levels

| Level | Criteria |
| ------- | ---------- |
| HIGH | Core functionality, user-facing |
| MEDIUM | Internal quality, incomplete feature |
| LOW | Minor, documentation |

### Core Principle

> [!CAUTION]
> **INTEGRATION OVER DELETION**
>
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find integration path.
> Deletion requires EXPLICIT user approval.

---

## Quadrant System

### Default Configuration

| Quadrant | Purpose | Patterns |
| ---------- | --------- | ---------- |
| Q1 | Core Logic | core/, lib/, adapters/, models/ |
| Q2 | User Interfaces | cli/, commands/, cmd/, api/ |
| Q3 | Visual Elements | ui/, components/, views/, frontend/ |
| Q4 | Support | tests/, utils/, helpers/, logging/ |

Quadrants are auto-detected by `/crown:init` and stored in SD.md.

---

## Commands

| Command | Description |
| --------- | ------------- |
| `/crown:init [name]` | Initialize crown in repository |
| `/crown:status` | Display ecosystem state |
| `/crown:todo [letter]` | Execute TODO workflow |
| `/crown:sd [phase] [quad]` | Execute SD workflow |
| `/crown:validate` | Validate cross-references |
| `/crown:continue` | Resume from current state |

---

## Token Efficiency Principles

1. **Split by version** - Archive completed versions
2. **Load relevant only** - Reference instead of copy
3. **Minimal index** - Just current state in LIVE docs
4. **Never duplicate** - Cross-reference instead

---
