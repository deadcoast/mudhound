---
description: Initialize crown documentation ecosystem - creates TODO.md, CHANGELOG.md, VALIDATION.md, SD.md with cross-reference system
argument-hint: "[project-name]"
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

Initialize the crown AI-optimized documentation ecosystem in this repository.

## Execution

### 1. Create Core Documents

Create these files in project root:

**TODO.md:**
```markdown
# TODO.md

## 0.0.1

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

- {DATE}

> [!TIP]
> crown initialized. Ready for task tracking.
> Use `/crown:status` to view current state.
> Use `/crown:sd R` to begin codebase review.

---
```

**CHANGELOG.md:**
```markdown
# Changelog

## 0.0.0

### A) PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, VALIDATION.md
> status: 'tracking completed work and releases'

---

## 0.0.1

- {DATE}

> [!IMPORTANT]
> crown ecosystem initialized.
> [TODO.md], [ver:`0.0.1`]
> [VALIDATION.md], [ver:`0.0.1`]

### A) Initialization - COMPLETE

| Component | Status |
| --------- | ------ |
| TODO.md | ✅ |
| CHANGELOG.md | ✅ |
| VALIDATION.md | ✅ |
| SD.md | ✅ |
| Folder structure | ✅ |

---
```

**VALIDATION.md:**
```markdown
# Validation

## 0.0.1

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking validation findings'

---

- {DATE}

### A) Initialization - VERIFIED

> [!NOTE]
> crown ecosystem initialized successfully.
> [TODO.md], [ver:`0.0.1`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]

**Verification:**
- All documents created ✅
- Folder structure created ✅

---
```

**SD.md:**
```markdown
# SeekAndDestroy

## 0.0.1

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: 'ready for codebase review'
> principle: INTEGRATION OVER DELETION

---

- {DATE}

> [!TIP]
> Use `/crown:sd R` to begin reconnaissance.
> Use `/crown:sd S Q1` to scan first quadrant.

---
```

### 2. Create Folder Structure

```bash
mkdir -p Docs
mkdir -p docs/TODO/complete docs/TODO/pending
mkdir -p docs/SD/complete docs/SD/pending
mkdir -p templates
```

### 3. Detect Project Structure

Scan project directories and categorize into quadrants:

| Pattern | Quadrant | Description |
|---------|----------|-------------|
| core/, lib/, adapters/, models/ | Q1 | Core business logic |
| cli/, commands/, cmd/, api/ | Q2 | User interfaces |
| ui/, components/, views/, frontend/ | Q3 | Visual elements |
| tests/, utils/, helpers/, logging/ | Q4 | Support infrastructure |

Count files per quadrant and update SD.md with quadrant table.

### 4. Create Specification

Create `Docs/crown.md` with:
- Document purposes (TODO, CHANGELOG, VALIDATION, SD)
- Cross-reference format: `[DOC.md], [ver:X.X.X, sect:Y)]`
- Quadrant configuration for this project
- Workflow commands

### 5. Output Summary

```
crown initialized!

Documents:
├── TODO.md [ver:0.0.1]
├── CHANGELOG.md [ver:0.0.1]
├── VALIDATION.md [ver:0.0.1]
└── SD.md [ver:0.0.1]

Quadrants:
├── Q1: {dirs} ({count} files)
├── Q2: {dirs} ({count} files)
├── Q3: {dirs} ({count} files)
└── Q4: {dirs} ({count} files)

Next: /crown:status or /crown:sd R
```

## Cross-Reference Format

All documents use: `[DOCUMENT.md], [ver:X.X.X, sect:Y)]`

Examples:
- `[TODO.md], [ver:0.0.1, sect:A)]`
- `[CHANGELOG.md], [ver:0.0.1]`
- `[VALIDATION.md], [ver:0.0.1, sect:A),B)]`
