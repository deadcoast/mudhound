# Crown Documentation

## 0.0.0

### PROTOCOL

> [!NOTE]
> purpose: AI-optimized document ecosystem
> dependencies: TODO.md, CHANGELOG.md, VALIDATION.md, SD.md
> status: 'specification'

---

## Core Documents

### TODO.md

> [!NOTE]
> alias: `crowndoc: TODO`
> purpose: task tracking
> file: TODO.md (LIVE), docs/TODO/complete/, docs/TODO/pending/

### CHANGELOG.md

> [!NOTE]
> alias: `crowndoc: CHANGE`
> purpose: completion tracking

### VALIDATION.md

> [!NOTE]
> alias: `crowndoc: VAL`
> purpose: verification

---

## Extended Workflows

### SD.md - SeekAndDestroy

> [!NOTE]
> alias: `crowndoc: SD`
> purpose: comprehensive codebase review
> principle: INTEGRATION OVER DELETION
> file: SD.md (LIVE), docs/SD/complete/, docs/SD/pending/
> spec: [Docs/SD.md]

**Quadrants:**
- Q1: `core/`, `adapters/`, `assets/`
- Q2: `cli/`, `commands/`
- Q3: `ui/`, `components/`, `animation/`
- Q4: `tests/`, `utils/`, `logging/`

**Phases:**
- `SD:R` - recon (map quadrants)
- `SD:S QX` - scan quadrant
- `SD:F` - flag findings
- `SD:X` - resolve
- `SD:V` - verify

**Finding Types:**
- U: UNUSED - investigate & integrate
- I: INTEGRATION - connect to workflow
- T: TYPE - fix annotation
- P: PATTERN - apply standard

---

## Reference Format

> [!NOTE]
> `[DOCUMENT.md], [ver:X.X.X, sect:Y)]`
> example: `[TODO.md], [ver:0.0.2, sect:A)]`

---

## File Organization

### LIVE Documents

> [!NOTE]
> TODO.md - current tasks
> SD.md - current review

### Complete

> [!NOTE]
> docs/TODO/complete/ - completed TODO versions
> docs/SD/complete/ - completed SD passes

### Pending

> [!NOTE]
> docs/TODO/pending/ - incomplete revisions
> docs/SD/pending/ - incomplete passes

---

## Commands

### Core

> [!NOTE]
> `crowndoc: continue` - continue workflow
> `crowndoc: status` - current state
> `crowndoc: TODO` - task workflow

### SD

> [!NOTE]
> `crowndoc: SD` - initialize SD
> `SD:R` - recon
> `SD:S Q1` - scan quadrant 1
> `SD:F` - review flags
> `SD:X` - resolve
> `SD:V` - verify

---

## Principles

### Token Efficiency

> [!IMPORTANT]
> Split files by version.
> Load only relevant pass/version.
> Minimal index, details via `ver`/`sect` reference.

### Integration Over Deletion

> [!CAUTION]
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find integration path.
> Deletion requires explicit approval.

---
