---
description: Execute SeekAndDestroy codebase review - systematic analysis with INTEGRATION OVER DELETION principle
argument-hint: "[phase] [quadrant] (R, S Q1, S Q2, S Q3, S Q4, F, X, V)"
allowed-tools: Read, Write, Bash, Glob, Grep
---

Execute the SeekAndDestroy (SD) workflow for systematic codebase review.

> [!CAUTION]
> **INTEGRATION OVER DELETION**
> 
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find integration path.
> Deletion requires EXPLICIT user approval.

## Phases

### SD R - RECON

Map the codebase and categorize into quadrants.

**Execute:**
1. Recursive directory scan
2. Categorize files into Q1-Q4
3. Count files per quadrant
4. Update SD.md with quadrant table

**Output:**
```markdown
| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | core/, adapters/ | 25 | PENDING |
| Q2 | cli/, commands/ | 18 | PENDING |
| Q3 | ui/, components/ | 42 | PENDING |
| Q4 | tests/, utils/ | 67 | PENDING |
```

### SD S Q{n} - SCAN

Analyze one quadrant for integration issues.

**Execute:**
1. For each file in quadrant:
   - Get symbol overview
   - Find references to each symbol
   - Check export status
2. Flag unreferenced symbols
3. **INVESTIGATE each finding** (not optional):
   - Read surrounding context
   - Check git history
   - Find related comments/TODOs
   - Hypothesize purpose
   - Find integration path
4. Document findings with integration paths
5. Generate TODO entries for significant findings

**Finding Types:**
- **U (UNUSED)**: No references found → Find integration point
- **I (INTEGRATION)**: Exists but disconnected → Add connection
- **T (TYPE)**: Missing annotation → Add types
- **P (PATTERN)**: Doesn't match standards → Refactor

**Severity:**
- **HIGH**: Core functionality, user-facing
- **MEDIUM**: Internal quality, incomplete feature
- **LOW**: Minor inconsistency, documentation

**Output:**
```markdown
### Q{n} SCAN - Findings

| ID | Location | Type | Severity | Symbol | Status |
|----|----------|------|----------|--------|--------|
| 1 | file.py:45 | U | HIGH | func_name | NEW |

### Q{n} Finding 1: func_name

> [!WARNING]
> type: U (UNUSED)
> severity: HIGH
> location: `file.py:45`

**Investigation:**
- Context: Part of caching module
- Git: Added in commit abc123
- Purpose: Cache search results

**Integration Path:**
1. Import in engine.py
2. Call from search()

**TODO:** [TODO.md], [ver:`X.X.X`, sect:`A)`]
```

### SD F - FLAG

Organize and prioritize all findings.

**Execute:**
1. Aggregate findings from all scanned quadrants
2. Sort by severity (HIGH → MEDIUM → LOW)
3. Verify TODO entries exist
4. Generate resolution plan

### SD X - RESOLVE

Execute resolutions for each finding.

**Type U Resolution:**
1. Find integration point
2. Add missing import/call
3. Verify symbol now has references
4. **NEVER delete first**

**Type I Resolution:**
1. Trace connection path
2. Add missing links
3. Verify end-to-end

**Type T Resolution:**
1. Infer types from usage
2. Add annotations
3. Verify with mypy

**Type P Resolution:**
1. Identify project pattern
2. Refactor to match
3. Verify consistency

### SD V - VERIFY

Verify all resolutions work correctly.

**Execute:**
1. Run test suite: `pytest`
2. Run type checker: `mypy`
3. Run linter: `ruff check`
4. Manual verification
5. Update VALIDATION.md
6. Archive pass to `docs/SD/complete/{version}-Q{n}.md`

## Cross-Reference Flow

```
SD finding created
    ↓
[TODO.md], [ver:X.X.X, sect:A)] - Task generated
    ↓
Resolution work performed
    ↓
[CHANGELOG.md], [ver:X.X.X, sect:A)] - Completion recorded
    ↓
[VALIDATION.md], [ver:X.X.X, sect:A)] - Verified
    ↓
Pass archived to docs/SD/complete/
```
