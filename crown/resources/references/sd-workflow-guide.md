# SeekAndDestroy Workflow Guide

## Philosophy

> [!CAUTION]
> **INTEGRATION OVER DELETION**
>
> The SD workflow is NOT about finding code to delete.
> It is about understanding the codebase and INTEGRATING unused elements.
>
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find the integration path.
> Deletion requires EXPLICIT user approval.

---

## Why Integration Over Deletion?

Unused code often represents:
- **Incomplete features** waiting for connection
- **Infrastructure** for future functionality
- **Historical context** that informs architecture
- **Defensive code** for edge cases not yet encountered

Deleting first destroys this value. Integration preserves and activates it.

---

## Workflow Phases

### Phase R: RECON

**Command:** `/crown:sd R`

**Purpose:** Map the codebase into quadrants

**Actions:**
1. Recursive directory scan of project
2. Categorize directories into Q1-Q4
3. Count files per quadrant
4. Update SD.md with quadrant table
5. Identify uncategorized items

**Output:**
```markdown
| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | core/, adapters/ | 25 | PENDING |
| Q2 | cli/, commands/ | 18 | PENDING |
| Q3 | ui/, components/ | 42 | PENDING |
| Q4 | tests/, utils/ | 67 | PENDING |
```

**Next:** Choose starting quadrant (usually Q1 - smallest, core)

---

### Phase S: SCAN

**Command:** `/crown:sd S Q1` (or Q2, Q3, Q4)

**Purpose:** Deep analysis of one quadrant

**Actions:**
1. For each file in quadrant:
   - Get symbol overview (classes, functions, variables)
   - Check export status (is it in `__init__.py`?)
   - Find references to each symbol
2. Flag symbols with no references
3. **INVESTIGATE each finding** (required, not optional)
4. Document integration paths
5. Generate TODO entries for significant findings

**Investigation Requirements:**

For EVERY flagged item:
```markdown
### Finding: symbol_name

**Location:** `file.py:45`
**Type:** Function
**Exported:** Yes
**References:** None

**Investigation:**
1. Surrounding context: [read nearby code]
2. Related symbols: [what else is in this module?]
3. Git history: [when/why was it added?]
4. Comments/TODOs: [any notes?]
5. Tests: [any related tests?]

**Analysis:** [why does this exist?]

**Integration Path:**
1. [where should it be imported]
2. [where should it be called]
3. [how does it connect to user workflow]
```

**Output:** Findings documented in SD.md, TODO entries created

---

### Phase F: FLAG

**Command:** `/crown:sd F`

**Purpose:** Organize and prioritize all findings

**Actions:**
1. Aggregate findings from all scanned quadrants
2. Sort by severity (HIGH → MEDIUM → LOW)
3. Sort by type (U → I → T → P)
4. Verify TODO entries exist for each
5. Generate resolution plan

**Priority Matrix:**

| Severity | Type U | Type I | Type T | Type P |
|----------|--------|--------|--------|--------|
| HIGH | 1 | 2 | 5 | 6 |
| MEDIUM | 3 | 4 | 7 | 8 |
| LOW | 9 | 10 | 11 | 12 |

**Output:** Prioritized resolution plan

---

### Phase X: RESOLVE

**Command:** `/crown:sd X`

**Purpose:** Execute integrations for each finding

**Type U (UNUSED) Resolution:**
```
1. Review investigation and integration path
2. Identify best integration point
3. Add import statement
4. Add function call
5. Verify symbol now has references
6. Update TODO task as complete
```

**Type I (INTEGRATION) Resolution:**
```
1. Trace current connection path
2. Find where chain breaks
3. Add missing link (import, call, etc.)
4. Verify end-to-end connection
5. Update TODO task as complete
```

**Type T (TYPE) Resolution:**
```
1. Analyze usage to infer types
2. Add type annotations
3. Run mypy to verify
4. Update TODO task as complete
```

**Type P (PATTERN) Resolution:**
```
1. Identify project pattern from similar code
2. Refactor to match pattern
3. Run linter to verify
4. Update TODO task as complete
```

**Output:** Resolved findings, updated TODO/CHANGELOG

---

### Phase V: VERIFY

**Command:** `/crown:sd V`

**Purpose:** Confirm all resolutions work correctly

**Actions:**
1. Run test suite: `pytest`
2. Run type checker: `mypy`
3. Run linter: `ruff check`
4. Manual verification of integrations
5. Update VALIDATION.md with results
6. Archive pass to docs/SD/complete/

**Verification Criteria:**
- All tests pass
- No new type errors
- No new lint errors
- Integrations function correctly

**Output:**
```markdown
### Q1 Pass - VERIFIED

**Verification:**
- pytest: 150 passed, 0 failed
- mypy: clean
- ruff: clean
- Manual: all integrations verified

**Archive:** docs/SD/complete/0.0.1-Q1.md
```

---

## Finding Types

### U: UNUSED

**Definition:** Symbol exists but has no references

**Examples:**
- Function defined but never called
- Class defined but never instantiated
- Import statement never used
- Variable assigned but never read

**Resolution:** Find where it SHOULD be used and add the call

### I: INTEGRATION

**Definition:** Symbol exists and works, but not connected to user workflow

**Examples:**
- Feature implemented but not in CLI
- Utility function not exposed
- Component complete but not rendered

**Resolution:** Add the missing connection to entry point

### T: TYPE

**Definition:** Missing or incorrect type annotations

**Examples:**
- Function without return type
- Parameter using `Any` when specific type known
- Missing generic type parameters

**Resolution:** Add proper type annotations

### P: PATTERN

**Definition:** Code doesn't follow project patterns

**Examples:**
- Different error handling style
- Inconsistent naming convention
- Different module structure

**Resolution:** Refactor to match established pattern

---

## Quadrant Defaults

| Quadrant | Directories | Focus |
|----------|-------------|-------|
| Q1 | core/, lib/, adapters/, models/ | Core business logic |
| Q2 | cli/, commands/, cmd/, api/ | User interfaces |
| Q3 | ui/, components/, views/, frontend/ | Visual elements |
| Q4 | tests/, utils/, helpers/, logging/ | Support infrastructure |

Customize in `/crown:init` or Docs/crown.md.

---

## SD Document Flow

```
/crown:sd R
    ↓
SD.md updated with quadrant table
    ↓
/crown:sd S Q1
    ↓
SD.md updated with findings
TODO.md updated with generated tasks
    ↓
/crown:sd F
    ↓
SD.md updated with resolution plan
    ↓
/crown:sd X
    ↓
Work performed
TODO.md tasks marked complete
CHANGELOG.md updated
    ↓
/crown:sd V
    ↓
VALIDATION.md updated
SD.md pass archived to docs/SD/complete/
    ↓
Continue to next quadrant or complete
```

---
