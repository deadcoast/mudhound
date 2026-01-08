# SD.md

## 0.0.0

### PROTOCOL

> [!NOTE]
> workflow: SeekAndDestroy
> alias: `crowndoc: SD`
> dependencies: TODO.md, CHANGELOG.md, VALIDATION.md
> status: 'comprehensive codebase review'

---

## Overview

> [!IMPORTANT]
> SD systematically reviews codebase by quadrant.
> Findings generate TODO entries via `[TODO.md], [ver:X.X.X, sect:Y)]`.
> INTEGRATION OVER DELETION - unused code is investigated, never deleted first.

---

## Quadrants

> [!NOTE]
> Q1: `core/`, `adapters/`, `assets/`
> Q2: `cli/`, `commands/`
> Q3: `ui/`, `components/`, `animation/`
> Q4: `tests/`, `utils/`, `logging/`

---

## Phases

### SD:R - RECON

> [!NOTE]
> Map codebase into quadrants.
> Define scope for each quadrant.

### SD:S - SCAN

> [!NOTE]
> Review target quadrant.
> Document findings as sections (A, B, C...).

### SD:F - FLAG

> [!NOTE]
> Classify findings by type and severity.
> Generate `[TODO.md], [ver:X.X.X, sect:Y)]` entries.

### SD:X - RESOLVE

> [!NOTE]
> Apply integration solutions.
> Update `[CHANGELOG.md], [ver:X.X.X, sect:Y)]`.

### SD:V - VERIFY

> [!NOTE]
> Validate resolutions.
> Update `[VALIDATION.md], [ver:X.X.X, sect:Y)]`.

---

## Finding Types

> [!NOTE]
> U: UNUSED - investigate & integrate
> I: INTEGRATION - connect to workflow
> T: TYPE - fix annotation
> P: PATTERN - apply standard

---

## Severity

> [!NOTE]
> HIGH: breaks functionality
> MEDIUM: affects quality
> LOW: minor improvement

---

## Status

> [!NOTE]
> 🔍 scanning
> 🚩 flagged
> 🔧 resolving
> ✅ resolved

---

## Resolution

> [!CAUTION]
> 1. INTEGRATE - find integration path
> 2. DEFER - document for future
> 3. REMOVE - requires explicit approval, LAST RESORT

---

## Commands

> [!NOTE]
> `crowndoc: SD` - initialize
> `SD:R` - recon
> `SD:S Q1` - scan quadrant
> `SD:F` - review flags
> `SD:X` - resolve
> `SD:V` - verify

---

## File Structure

> [!NOTE]
> SD.md - LIVE document
> docs/SD/complete/ - completed passes
> docs/SD/pending/ - passes needing revision

---
