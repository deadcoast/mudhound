# crown-format

When asked about crown document format, cross-reference syntax, PROTOCOL blocks, section identifiers, version numbering, or blockquote types, this skill provides the complete specification for crown's AI-optimized documentation structure.

---

## Purpose

crown is an AI-optimized documentation ecosystem. Documents are structured for:
1. **AI agent context extraction** - Efficient parsing
2. **Token efficiency** - Version splitting, minimal index
3. **Cross-reference traceability** - Every change tracked
4. **Repository knowledge mapping** - Complete codebase state

---

## Core Documents

### TODO.md
- **Purpose:** Task tracking and work items
- **Location:** TODO.md (LIVE in root)
- **Archive:** docs/TODO/complete/, docs/TODO/pending/

### CHANGELOG.md
- **Purpose:** Completion tracking and release history
- **Location:** CHANGELOG.md (root)

### VALIDATION.md
- **Purpose:** Verification and integration status
- **Location:** VALIDATION.md (root)

### SD.md
- **Purpose:** Systematic codebase review (SeekAndDestroy)
- **Location:** SD.md (LIVE in root)
- **Archive:** docs/SD/complete/, docs/SD/pending/

---

## Cross-Reference Format

### The ONLY Format

```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

This is the sole cross-reference format. Do not invent alternatives.

### Components

| Component | Format | Example |
|-----------|--------|---------|
| Document | `[NAME.md]` | `[TODO.md]` |
| Version | `[ver:\`X.X.X\`]` | `[ver:\`0.0.1\`]` |
| Section | `[sect:\`Y)\`]` | `[sect:\`A)\`]` |

### Valid Combinations

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
[VALIDATION.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

**Section Range:**
```
[TODO.md], [ver:`0.0.1`, sect:`C)`-`N)`]
```

---

## Document Structure

Every crown document follows this structure:

```markdown
# DOCUMENT.md

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: OTHER.md, ANOTHER.md
> status: 'description'

---

- YEAR-MM-DD

[Content sections]

---
```

### PROTOCOL Block

Every document begins with PROTOCOL:
```markdown
### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking TODO items'
```

### Section Identifiers

Use capital letters: A), B), C), etc.

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
```

Checklist letters MUST match section letters.

---

## Blockquote Types

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
Navigation hints, next steps, suggestions.
```markdown
> [!TIP]
> Previous version: [docs/TODO/complete/0.0.7.md]
```

### [!CAUTION]
Critical rules that MUST be followed.
```markdown
> [!CAUTION]
> NEVER delete unused code first.
```

---

## Version Numbers

Format: `X.X.X` (semantic-style)
- PATCH: Incremented for completed TODO versions
- MINOR: Significant feature sets
- MAJOR: Breaking changes or milestones

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
│   └── crown.md         # Specification
│
├── docs/
│   ├── TODO/
│   │   ├── complete/    # Archived versions
│   │   └── pending/     # Incomplete versions
│   │
│   └── SD/
│       ├── complete/    # Completed passes
│       └── pending/     # Incomplete passes
│
└── templates/
    ├── TODO.template.md
    ├── CHANGELOG.template.md
    ├── VALIDATION.template.md
    └── SD.template.md
```

### LIVE vs Archive

**LIVE (root):** Current working state
**Archive (docs/*/complete/):** Completed versions
**Pending (docs/*/pending/):** Interrupted work

---

## Token Efficiency

1. **Split by version** - Archive completed versions
2. **Load relevant only** - Reference instead of copy
3. **Minimal index** - Just current state in LIVE
4. **Never duplicate** - Cross-reference instead
