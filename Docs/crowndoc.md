# Crown Documentation

> Triple Crown: Three Document Utility Leadership

## Overview

Crown is a three-document ecosystem designed for AI-assisted development workflows. It provides structured, cross-referenced documentation that enables AI agents to track project status, understand context, and execute tasks with precision.

The name "Crown" derives from "Triple Crown" - representing the three interconnected documents that together provide complete project leadership.

---

## The Three Documents

### 1. TODO.md - Task Tracking

**Purpose:** Tracks outstanding work items and their status.

**Role:** The "what needs to be done" document.

| Element | Description |
| ------- | ----------- |
| Checklist index | Quick-scan task list with `[x]`/`[ ]` markers |
| Task sections | Detailed description of each task |
| Cross-references | Links to VALIDATION (where found) and CHANGELOG (where tracked) |

### 2. CHANGELOG.md - Completion Tracking

**Purpose:** Records completed work and release status.

**Role:** The "what has been done" document.

| Element | Description |
| ------- | ----------- |
| Version sections | Organized by release version |
| Category tables | Components grouped by system area |
| Status indicators | ✅ complete, ⚠️ partial, ❌ pending |
| Cross-references | Links to VALIDATION (verification) and TODO (pending work) |

### 3. VALIDATION.md - Verification & Analysis

**Purpose:** Documents validation findings, integration status, and architectural analysis.

**Role:** The "what is the current state" document.

| Element | Description |
| ------- | ----------- |
| Validation passes | Each pass documents a specific area of the codebase |
| Status tables | Detailed component-level status |
| Issues identified | Problems found during validation |
| Cross-references | Links to TODO (work items) and CHANGELOG (completion) |

---

## Document Structure

### Protocol Section (0.0.0)

Every crown document begins with a protocol section:

```markdown
## 0.0.0

### A) PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: [other crown documents]
> status: '[document purpose]'
```

### Version Sections

Each version follows this structure:

```markdown
## X.X.X

- YEAR-MM-DD

> [!IMPORTANT]
> Brief summary of this version/pass
> [DOCUMENT.md], [ver:`X.X.X`] - Description
> [DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`] - Description

### A) Section Title

[Content - tables, descriptions, etc.]
```

### Cross-Reference Format

```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

- `DOCUMENT.md` - The target document (TODO.md, CHANGELOG.md, VALIDATION.md)
- `ver:` - Version number in the target document
- `sect:` - Section letter(s) within that version

---

## Status Indicators

| Symbol | Meaning |
| ------ | ------- |
| ✅ | Complete / Integrated |
| ⚠️ | Partial / Needs attention |
| ❌ | Missing / Not integrated |
| `[x]` | Task completed (TODO.md only) |
| `[ ]` | Task pending (TODO.md only) |

---

## Information Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         VALIDATION.md                       │
│                    (Analysis & Findings)                    │
│                                                             │
│   Identifies issues, tracks integration status              │
│   Points TO: TODO (work items), CHANGELOG (completion)      │
└──────────────────────────┬──────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
┌───────────────────────┐     ┌───────────────────────┐
│       TODO.md         │     │     CHANGELOG.md      │
│   (Work to be done)   │     │   (Work completed)    │
│                       │     │                       │
│ Tracks tasks from     │     │ Records completion    │
│ VALIDATION findings   │────>│ of TODO items         │
│                       │     │                       │
│ Points TO:            │     │ Points TO:            │
│ - VALIDATION (source) │     │ - VALIDATION (verify) │
│ - CHANGELOG (track)   │     │ - TODO (pending)      │
└───────────────────────┘     └───────────────────────┘
```

---

## Usage Workflow

### 1. Validation Pass

Run a validation pass on a codebase area:

1. Create/update a version section in VALIDATION.md
2. Document findings with tables and analysis
3. For each issue found, reference the TODO item that will address it

### 2. Task Creation

For each issue identified:

1. Add task to TODO.md checklist index
2. Create detailed section with cross-references back to VALIDATION
3. Reference the CHANGELOG section where completion will be tracked

### 3. Task Execution

When completing a task:

1. Implement the solution
2. Mark task `[x]` in TODO.md checklist
3. Update CHANGELOG.md with completion status (✅)
4. Update VALIDATION.md to reflect new state

### 4. Living Updates

When any document changes:

1. Verify cross-references remain valid
2. Update related sections in other documents
3. Maintain consistency across all three documents

---

## Design Rationale

### Why Three Documents?

| Concern | Document | Benefit |
| ------- | -------- | ------- |
| What to do | TODO.md | Clear task tracking |
| What's done | CHANGELOG.md | Progress visibility |
| Current state | VALIDATION.md | Context awareness |

Single documents become unwieldy. Separation provides:
- **Focus**: Each document has one job
- **Navigation**: Easy to find relevant information
- **Scalability**: Documents remain manageable as projects grow

### Why Cross-References?

- **Traceability**: Every task links to its source (VALIDATION) and destination (CHANGELOG)
- **Verification**: Claims can be verified by following references
- **AI Navigation**: Agents can traverse the graph to understand context

### Why This Format?

Optimized for AI agent consumption:

1. **Structured**: Consistent format enables reliable parsing
2. **Concise**: Key-value protocol sections, minimal prose
3. **Linked**: Cross-references provide navigation without repetition
4. **Scannable**: Tables and indicators enable quick status checks
5. **Contextual**: Just enough information without overwhelming

### Why "Canonical Versioning"?

Versions in crown documents represent:
- **TODO.md**: Release targets (work planned for version X.X.X)
- **CHANGELOG.md**: Actual releases (work completed in version X.X.X)
- **VALIDATION.md**: Validation passes (analysis performed for version X.X.X)

This allows tracking of work across the development lifecycle.

---

## Templates

Templates are provided in `/templates/`:

- `TODO.template.md`
- `CHANGELOG.template.md`
- `VALIDATION.template.md`

Use these as starting points for new crown document systems.

---

## Best Practices

### DO

- Keep documents synchronized
- Use consistent cross-reference format
- Update all three documents when state changes
- Use tables for structured data
- Keep descriptions concise

### DON'T

- Let documents drift out of sync
- Add prose where tables suffice
- Create orphan references
- Skip the protocol section
- Mix concerns between documents

---

## Example Cross-Reference Chain

**Issue discovered:**

```
VALIDATION.md 0.0.3 section B identifies:
"Table component is not used (Rich tables used instead)"
```

**Task created:**

```
TODO.md 0.0.1 section C:
"Integrate custom Table component"
References: [VALIDATION.md], [ver:`0.0.3`, sect:`B)`]
```

**Completion tracked:**

```
CHANGELOG.md 0.0.1 section D:
"Table Component | ✅ | [VALIDATION.md], [ver:`0.0.3`, sect:`B)`]"
```

**Validation updated:**

```
VALIDATION.md 0.0.3 section B:
"Table | ✅ | [TODO.md], [ver:`0.0.1`, sect:`C)`] - COMPLETED"
```

---

## Summary

Crown documentation provides a structured, cross-referenced system for tracking project state across three concerns: what needs to be done (TODO), what has been done (CHANGELOG), and what is the current state (VALIDATION). The format is optimized for AI agent workflows while remaining human-readable.

The triple crown approach ensures no aspect of project management is neglected while maintaining clear separation of concerns and full traceability of decisions and changes.
