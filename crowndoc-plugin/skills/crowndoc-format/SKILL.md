# crowndoc-format

When asked about crowndoc format, document structure, cross-referencing, AI-optimized documentation, or repository knowledge mapping, this skill teaches the complete crowndoc specification and format system.

---

## Purpose

crowndoc is an AI-optimized documentation ecosystem. It is NOT designed for human consumption. Every design decision prioritizes:

1. **AI agent context extraction** - Documents structured for efficient parsing
2. **Token efficiency** - Minimal repetition, version-split files, lazy loading via references
3. **Cross-reference traceability** - Every change traceable through the ecosystem
4. **Repository knowledge mapping** - Complete codebase state captured in linked documents

---

## Core Documents

The ecosystem consists of four interconnected documents:

### TODO.md

> [!NOTE]
> alias: `crowndoc: TODO`
> purpose: Task tracking and work items
> location: TODO.md (LIVE in root)
> archive: docs/TODO/complete/, docs/TODO/pending/

TODO.md is the LIVE task tracker. It contains:
- Current version number
- PROTOCOL block with dependencies
- Checklist of tasks with letter identifiers
- Detailed sections for each task with cross-references

**Lifecycle:**
1. Tasks added as `- [ ] [A] Description`
2. Work performed, task marked `- [x] [A]`
3. Cross-references created to CHANGELOG and VALIDATION
4. When all tasks complete, version archived to docs/TODO/complete/X.X.X.md
5. Root TODO.md incremented to next version

### CHANGELOG.md

> [!NOTE]
> alias: `crowndoc: CHANGE`
> purpose: Completion tracking and release history
> location: CHANGELOG.md (root)

CHANGELOG.md records completed work. It contains:
- Version entries in reverse chronological order
- PROTOCOL block establishing dependencies
- Categorized completion tables with status indicators
- Cross-references to TODO.md (source tasks) and VALIDATION.md (verification)

**Entry Pattern:**
```markdown
## X.X.X

- YEAR-MM-DD

> [!IMPORTANT]
> Summary of this release
> [TODO.md], [ver:`X.X.X`] - Work items
> [VALIDATION.md], [ver:`X.X.X`] - Validation

### A) Category Name - STATUS

| Component | Status | Reference |
| --------- | ------ | --------- |
| Component | ✅ | [VALIDATION.md], [ver:`X.X.X`, sect:`Y)`] |
```

### VALIDATION.md

> [!NOTE]
> alias: `crowndoc: VAL`
> purpose: Verification and integration status
> location: VALIDATION.md (root)

VALIDATION.md tracks verification outcomes. It contains:
- Version entries for validation passes
- PROTOCOL block with dependencies
- Verification results (test counts, linter status)
- Cross-references linking back to TODO and CHANGELOG

**Entry Pattern:**
```markdown
## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking validation findings'

---

### A) Component/Feature Verified

> [!NOTE]
> Description of verification
> [TODO.md], [ver:`X.X.X`, sect:`Y)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`Z)`]

**Verification:**
- pytest: N passed
- mypy: clean
- ruff: clean
```

### SD.md (SeekAndDestroy)

> [!NOTE]
> alias: `crowndoc: SD`
> purpose: Systematic codebase review
> location: SD.md (LIVE in root)
> archive: docs/SD/complete/, docs/SD/pending/
> spec: Docs/SD.md

SD.md tracks codebase review passes. It is an extended workflow document that:
- Divides codebase into quadrants (Q1-Q4)
- Tracks scan progress per quadrant
- Records findings with type/severity/location
- Generates TODO entries for issues found
- Enforces INTEGRATION OVER DELETION principle

---

## Document Structure

Every crowndoc file follows this exact structure:

```markdown
# DOCUMENT.md

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: OTHER.md, ANOTHER.md
> status: 'description of document purpose'

---

- YEAR-MM-DD

[Content sections with letter identifiers]

---
```

### Version Numbers

- Format: `X.X.X` (semantic-style but used for document versioning)
- LIVE documents show current working version
- Archived documents preserve completed versions
- Version increments when all tasks/items complete

### PROTOCOL Block

Every document begins with a PROTOCOL block:

```markdown
### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: DOCUMENT1.md, DOCUMENT2.md
> status: 'current state description'
```

This establishes:
- Versioning scheme (always `canonical`)
- Document dependencies (what this doc links to)
- Current status of the document

### Section Identifiers

Sections use capital letter identifiers: A), B), C), etc.

```markdown
### A) Section Title

> [!IMPORTANT]
> Description
> [DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

Task checklists use bracketed letters:
```markdown
- [ ] [A] Pending task
- [x] [B] Completed task
- [ ] [C] Another pending task
```

The checklist letters MUST match the section letters below.

---

## Cross-Reference System

### The ONLY Format

```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

This is the SOLE cross-reference format. Do not invent alternatives.

### Components

| Component | Format | Example |
|-----------|--------|---------|
| Document | `[NAME.md]` | `[TODO.md]` |
| Version | `[ver:\`X.X.X\`]` | `[ver:\`0.0.1\`]` |
| Section | `[sect:\`Y)\`]` | `[sect:\`A)\`]` |

### Valid Combinations

**Document + Version only:**
```
[TODO.md], [ver:`0.0.1`]
```

**Document + Version + Section:**
```
[CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

**Document + Version + Multiple Sections:**
```
[VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
```

**Document + Multiple Versions:**
```
[VALIDATION.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

**Section Range:**
```
[TODO.md], [ver:`0.0.1`, sect:`C)`-`N)`]
```

### Cross-Reference Flow

Every change flows through the ecosystem:

```
Origin (SD finding, user request, bug report)
    ↓
[TODO.md], [ver:X.X.X, sect:Y)] - Task created
    ↓
Work performed
    ↓
[CHANGELOG.md], [ver:X.X.X, sect:Z)] - Completion recorded
    ↓
[VALIDATION.md], [ver:X.X.X, sect:W)] - Verification documented
```

This creates full traceability from origin to verification.

---

## Blockquote Types

crowndoc uses GitHub-flavored markdown alerts for semantic markup:

### [!NOTE]
Metadata, protocol information, informational content.
```markdown
> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
```

### [!IMPORTANT]
Task descriptions, key information requiring attention.
```markdown
> [!IMPORTANT]
> Critical task that blocks other work.
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
```

### [!WARNING]
SD findings, issues discovered, problems identified.
```markdown
> [!WARNING]
> type: U (UNUSED)
> severity: HIGH
> location: `core/cache.py:45`
```

### [!TIP]
Navigation hints, next steps, helpful suggestions.
```markdown
> [!TIP]
> Completed versions: [docs/TODO/complete/]
> Use `crowndoc: status` to see current state.
```

### [!CAUTION]
Critical rules that MUST be followed, destructive warnings.
```markdown
> [!CAUTION]
> NEVER delete unused code first.
> Investigate origin and design intent.
> Deletion requires explicit approval.
```

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
│   ├── crowndoc.md      # Specification document
│   └── SD.md            # SD workflow specification
│
├── docs/
│   ├── TODO/
│   │   ├── complete/    # Archived completed versions
│   │   │   ├── 0.0.1.md
│   │   │   ├── 0.0.2.md
│   │   │   └── ...
│   │   └── pending/     # Incomplete revisions (conflicts)
│   │
│   └── SD/
│       ├── complete/    # Completed SD passes
│       │   ├── 0.0.1-Q1.md
│       │   ├── 0.0.1-Q3.md
│       │   └── ...
│       └── pending/     # Incomplete passes
│
└── templates/
    ├── TODO.template.md
    ├── CHANGELOG.template.md
    ├── VALIDATION.template.md
    └── SD.template.md
```

### LIVE vs Archive

**LIVE Documents (root):**
- TODO.md - Current working tasks
- SD.md - Current codebase review pass
- Always contain the active version being worked on

**Archive (docs/*/complete/):**
- Completed versions moved here when all items done
- Preserves full history without bloating LIVE docs
- Enables token-efficient loading (load only needed version)

**Pending (docs/*/pending/):**
- Incomplete revisions that couldn't be finished
- Conflict resolutions in progress
- Work that was interrupted

---

## Token Efficiency Principles

### 1. Split Files by Version

DON'T keep all history in one file. DO archive completed versions.

```
❌ TODO.md with 50 versions of history
✅ TODO.md (current) + docs/TODO/complete/0.0.1.md, 0.0.2.md, ...
```

### 2. Load Only Relevant Content

Use cross-references to point to specific versions/sections rather than duplicating content.

```
❌ Copying full task description to CHANGELOG
✅ [TODO.md], [ver:`0.0.1`, sect:`A)`] - Reference only
```

### 3. Minimal Index in LIVE Documents

LIVE docs contain minimal content - just current state and references.

```markdown
# TODO.md

## 0.0.8

### PROTOCOL
> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'ready for new work'

---

> [!TIP]
> Completed versions: [docs/TODO/complete/]

---
```

### 4. Details via Reference

When you need details about a past version, load the specific archived file:
- `docs/TODO/complete/0.0.1.md` for TODO version 0.0.1 details
- `docs/SD/complete/0.0.1-Q3.md` for SD pass Q3 details

### 5. Never Duplicate Content

If information exists in one document, reference it from others. Don't copy.

---

## Version Progression Workflow

### Starting a New Version

1. Root TODO.md is empty (no pending tasks)
2. New tasks identified
3. Add tasks with checklist and sections:
   ```markdown
   - [ ] [A] Task description
   - [ ] [B] Another task
   
   ---
   
   ### A) Task Title
   > [!IMPORTANT]
   > Description
   > [VALIDATION.md], [ver:`X.X.X`, sect:`Y)`]
   > [CHANGELOG.md], [ver:`X.X.X`, sect:`Z)`]
   ```

### Completing Tasks

1. Perform work for task
2. Mark checklist item complete: `- [x] [A]`
3. Update section with completion details
4. Create/update CHANGELOG entry
5. Create/update VALIDATION entry if verification needed

### Completing a Version

When all tasks in a version are complete:

1. **Archive TODO version:**
   ```
   Copy TODO.md content → docs/TODO/complete/X.X.X.md
   ```

2. **Finalize CHANGELOG entry:**
   - Ensure all sections have status tables
   - All cross-references point to correct versions

3. **Finalize VALIDATION entry:**
   - Record verification results
   - Link back to TODO and CHANGELOG

4. **Increment root TODO.md:**
   ```markdown
   ## X.X.Y  # Next version
   
   > [!TIP]
   > Previous version: [docs/TODO/complete/X.X.X.md]
   ```

---

## Status Indicators

Use these consistently across documents:

| Indicator | Meaning |
|-----------|---------|
| ✅ | Complete, verified, passing |
| ❌ | Failed, blocked, not started |
| ⚠️ | Warning, partial, needs attention |
| 🔍 | In progress, scanning, investigating |

---

## Best Practices

### DO

- Always include PROTOCOL block
- Use exact cross-reference format
- Archive completed versions promptly
- Link every change to TODO, CHANGELOG, VALIDATION
- Use semantic blockquote types
- Keep LIVE documents minimal

### DON'T

- Invent new reference formats
- Keep all history in LIVE documents
- Duplicate content across documents
- Skip cross-references
- Use inconsistent section identifiers
- Mix completed and pending work in same version

---

## Templates

Templates are provided in `templates/` directory:
- `TODO.template.md` - Task tracking template
- `CHANGELOG.template.md` - Completion tracking template
- `VALIDATION.template.md` - Verification template
- `SD.template.md` - SD pass template

Use these as starting points, customizing version numbers and content.

---
