---
name: crown-workflow
description: This skill should be used when the user asks to "execute TODO workflow", "run SD codebase review", "archive completed version", "continue crown workflow", "mark task complete", or asks about SeekAndDestroy phases or task tracking.
version: 0.1.0
---

# crown-workflow

When executing crown workflows, managing TODO tasks, running SD codebase reviews, archiving versions, or understanding cross-reference flow, this skill provides complete workflow execution patterns and step-by-step guides.

---

## TODO Workflow

### Entry Points

**Trigger:** `/crown:todo` or `/crown:continue` with pending tasks

### Execution Flow

1. **Read State**
   - Parse TODO.md version and tasks
   - Identify pending (`[ ]`) and completed (`[x]`)
   
2. **Execute Task**
   - Read task section `### A)`
   - Perform work described
   - Record completion details
   
3. **Mark Complete**
   - Change `[ ]` to `[x]`
   
4. **Update Cross-References**
   - Add CHANGELOG entry
   - Add VALIDATION entry (if verification)
   
5. **Archive Version** (when all complete)
   - Copy to docs/TODO/complete/{version}.md
   - Increment root to next version

### Adding Tasks

```markdown
- [ ] [A] Task description

---

### A) Task Title

> [!IMPORTANT]
> Detailed description.
> [VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

---

## SD Workflow (SeekAndDestroy)

### Core Principle

> [!CAUTION]
> **INTEGRATION OVER DELETION**
>
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find integration path.
> Deletion requires EXPLICIT user approval.

### Phases

#### SD R - RECON

**Purpose:** Map codebase into quadrants

**Execute:**
1. Recursive directory scan
2. Categorize into Q1-Q4
3. Count files per quadrant
4. Update SD.md with table

**Default Quadrants:**
- Q1: core/, adapters/, models/ (Core logic)
- Q2: cli/, commands/, api/ (User interfaces)
- Q3: ui/, components/, views/ (Visual elements)
- Q4: tests/, utils/, logging/ (Support)

#### SD S Q{n} - SCAN

**Purpose:** Deep analysis of one quadrant

**Execute:**
1. For each file: get symbol overview
2. Find references to each symbol
3. Flag unreferenced symbols
4. **INVESTIGATE each finding**
5. Document integration paths
6. Generate TODO entries

**Investigation (REQUIRED):**
- Read surrounding context
- Check git history
- Find related comments/TODOs
- Hypothesize purpose
- Identify where it SHOULD be used

#### SD F - FLAG

**Purpose:** Organize findings before resolution

**Execute:**
1. Aggregate all findings
2. Sort by severity (HIGH → MEDIUM → LOW)
3. Verify TODO entries exist
4. Generate resolution plan

#### SD X - RESOLVE

**Purpose:** Execute integrations

**Type U (UNUSED):**
1. Find integration point
2. Add import/call
3. Verify references exist
4. NEVER delete first

**Type I (INTEGRATION):**
1. Trace connection path
2. Add missing links
3. Verify end-to-end

**Type T (TYPE):**
1. Infer from usage
2. Add annotations
3. Verify with mypy

**Type P (PATTERN):**
1. Identify project pattern
2. Refactor to match
3. Verify consistency

#### SD V - VERIFY

**Purpose:** Confirm resolutions work

**Execute:**
1. Run tests: `pytest`
2. Type check: `mypy`
3. Lint: `ruff check`
4. Manual verification
5. Update VALIDATION.md
6. Archive pass

---

## Finding Types

| Type | Name | Meaning | Resolution |
|------|------|---------|------------|
| U | UNUSED | No references | Find integration point |
| I | INTEGRATION | Exists but disconnected | Add connections |
| T | TYPE | Missing annotation | Add types |
| P | PATTERN | Doesn't match standard | Refactor |

## Severity Levels

| Level | Criteria | Priority |
|-------|----------|----------|
| HIGH | Core functionality, user-facing | First |
| MEDIUM | Internal quality, incomplete | Second |
| LOW | Minor, documentation | Last |

---

## Cross-Reference Flow

```
Origin (SD finding, user request)
    ↓
[TODO.md], [ver:X.X.X, sect:A)] - Task created
    ↓
Work performed
    ↓
[CHANGELOG.md], [ver:X.X.X, sect:A)] - Completion
    ↓
[VALIDATION.md], [ver:X.X.X, sect:A)] - Verification
    ↓
Archive to docs/*/complete/
```

---

## State Detection

For `/crown:continue`:

1. Check SD.md status
   - If not "ready"/"complete" → Resume SD phase
2. Check TODO.md tasks
   - If pending exists → Resume TODO
   - If all complete → Archive version
3. Otherwise → Offer choices

**Priority:** SD > TODO > Clean state

---

## Version Archiving

When all tasks complete:

1. Verify all `[x]`
2. Verify cross-references exist
3. Copy to docs/TODO/complete/{version}.md
4. Increment root TODO.md
5. Clear tasks, add TIP for previous version

```markdown
> [!TIP]
> Previous version: [docs/TODO/complete/0.0.9.md]
```
