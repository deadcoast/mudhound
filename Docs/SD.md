# SD - SeekAndDestroy

## Agent Workflow

> [!NOTE]
> type: executable workflow
> trigger: `crowndoc: SD`
> purpose: systematic codebase review with integration bias

---

## SD:R - RECON

**Execute:**
1. `list_dir` recursive on project root
2. Categorize paths into quadrants:
   - Q1: core/, adapters/, assets/
   - Q2: cli/, commands/
   - Q3: ui/, components/, animation/
   - Q4: tests/, utils/, logging/
3. Count files per quadrant
4. Output scope summary

**Decision:** Select quadrant with most unknowns or user-specified target.

---

## SD:S - SCAN

**Execute for target quadrant:**
1. `get_symbols_overview` on each file
2. For each symbol, check:
   - Is it exported?
   - Is it referenced? (`find_referencing_symbols`)
   - If unreferenced: FLAG as type U (UNUSED)
3. For each import, check:
   - Is it used in file?
   - If unused: FLAG as type U
4. For each component/class:
   - Trace integration path to CLI entry
   - If disconnected: FLAG as type I (INTEGRATION)

**CRITICAL:** Do NOT mark for deletion. Investigate WHY it exists.

**For each UNUSED finding:**
1. Read surrounding code context
2. Check git history if available
3. Search for TODO/FIXME comments
4. Hypothesize intended use case
5. Document integration path

---

## SD:F - FLAG

**For each finding, document:**
1. Location: file:line
2. Type: U/I/T/P
3. Severity: HIGH/MEDIUM/LOW
4. Analysis: why it exists, intended purpose
5. Integration path: how to connect it

**Generate TODO entry:**
- Create `[TODO.md], [ver:X.X.X, sect:Y)]` reference
- Add to root TODO.md as new task

---

## SD:X - RESOLVE

**For each flagged item:**

**If type U (UNUSED):**
1. Find where it SHOULD be used
2. Add the missing call/import/integration
3. Verify it works
4. NEVER delete as first solution

**If type I (INTEGRATION):**
1. Trace from component to CLI
2. Identify missing connection point
3. Add integration code
4. Test the integration

**If type T (TYPE):**
1. Add proper type annotation
2. Verify with mypy

**If type P (PATTERN):**
1. Apply project standard
2. Verify consistency

**Update CHANGELOG:** `[CHANGELOG.md], [ver:X.X.X, sect:Y)]`

---

## SD:V - VERIFY

**Execute:**
1. `pytest` - all tests pass
2. `mypy` - no type errors
3. `ruff check` - no lint errors
4. Manual verification of integrations

**Update VALIDATION:** `[VALIDATION.md], [ver:X.X.X, sect:Y)]`

---

## Tool Usage

**Discovery:**
- `list_dir` - map structure
- `get_symbols_overview` - file contents
- `find_symbol` - locate definitions
- `find_referencing_symbols` - trace usage

**Analysis:**
- `read_file` - context understanding
- `search_for_pattern` - find related code

**Modification:**
- `replace_symbol_body` - update definitions
- `insert_after_symbol` - add integrations
- `replace_content` - targeted fixes

**Verification:**
- `execute_shell_command` - run tests/linters

---

## State Tracking

**Current state stored in SD.md (LIVE):**
- Active quadrant
- Scan progress
- Pending findings
- Resolution status

**Completed passes moved to:** docs/SD/complete/

---

## Integration with Crown Docs

**SD finding → TODO task:**
```
SD finding in Q1, type U, severity MEDIUM
↓
[TODO.md], [ver:0.0.7, sect:A)] - Integrate unused SearchCache
```

**TODO completion → CHANGELOG:**
```
Task completed
↓
[CHANGELOG.md], [ver:0.0.7, sect:A)] - SearchCache integrated into engine
```

**Verification → VALIDATION:**
```
Tests pass, integration verified
↓
[VALIDATION.md], [ver:0.0.10, sect:A)] - SearchCache integration validated
```

---

## Decision Tree

```
START
  ↓
SD:R → Map quadrants
  ↓
Select quadrant (user choice or highest priority)
  ↓
SD:S → Scan files
  ↓
For each file:
  ├─ Symbols referenced? → YES → Skip
  └─ NO → Investigate
           ├─ Integration path found? → FLAG type I
           ├─ Type issue? → FLAG type T
           ├─ Pattern violation? → FLAG type P
           └─ Truly unused? → FLAG type U, document WHY
  ↓
SD:F → Generate TODO entries
  ↓
SD:X → Resolve (INTEGRATE, not delete)
  ↓
SD:V → Verify
  ↓
Move pass to complete/
  ↓
Next quadrant or END
```

---

## Commands

`crowndoc: SD` - Start workflow, execute SD:R
`SD:R` - RECON phase
`SD:S Q1` - SCAN quadrant 1
`SD:S Q2` - SCAN quadrant 2
`SD:S Q3` - SCAN quadrant 3
`SD:S Q4` - SCAN quadrant 4
`SD:F` - FLAG phase (after scan)
`SD:X` - RESOLVE phase
`SD:V` - VERIFY phase
`SD:status` - Current state
`SD:next` - Proceed to next phase

---
