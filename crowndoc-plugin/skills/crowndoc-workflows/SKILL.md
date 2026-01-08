# crowndoc-workflows

When executing crowndoc workflows, continuing work, managing TODO/SD tasks, archiving versions, or understanding the flow between documents, this skill provides complete workflow specifications and execution guides.

---

## Purpose

This skill defines the operational workflows for the crowndoc ecosystem. While `crowndoc-format` teaches document structure and syntax, `crowndoc-workflows` teaches how to **execute** the documentation system - how work flows through documents, how versions progress, and how the ecosystem maintains traceability.

The workflows are designed for AI agents executing documentation tasks. Every workflow:
1. Produces traceable cross-references
2. Maintains version integrity
3. Preserves complete audit trail
4. Optimizes for token efficiency

---

## Workflow Hierarchy

```
crowndoc ecosystem
├── TODO Workflow (task tracking)
│   ├── Add Task
│   ├── Execute Task
│   ├── Complete Task
│   └── Complete Version
│
├── SD Workflow (codebase review)
│   ├── SD:R (Recon)
│   ├── SD:S (Scan)
│   ├── SD:F (Flag)
│   ├── SD:X (Resolve)
│   └── SD:V (Verify)
│
├── Validation Workflow (verification)
│   ├── Record Verification
│   ├── Link to Source
│   └── Update Status
│
└── Changelog Workflow (completion tracking)
    ├── Record Completion
    ├── Create Tables
    └── Link References
```

---

## TODO Workflow

### Triggers

- `crowndoc: TODO` - explicit TODO workflow
- `crowndoc: continue` - when TODO.md has pending tasks
- User adds new work items
- SD workflow generates findings

### 1. Read Current State

**Action:** Read TODO.md from project root

**Extract:**
```markdown
## X.X.X                    # Current version

### PROTOCOL
> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'CURRENT_STATUS'
```

**Parse Tasks:**
```markdown
- [ ] [A] Uncompleted task     # pending = True
- [x] [B] Completed task       # pending = False
- [ ] [C] Another pending      # pending = True
```

**Output State:**
```
TODO.md [ver:X.X.X]
├── Status: CURRENT_STATUS
├── Pending: 2 tasks (A, C)
├── Completed: 1 task (B)
└── Next: Task A
```

### 2. Execute Task

**For each pending task, follow this sequence:**

**Step 1: Read Task Section**
```markdown
### A) Task Title

> [!IMPORTANT]
> Description of the task and what it involves.
> [VALIDATION.md], [ver:`X.X.X`, sect:`Y)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`Z)`]
```

**Step 2: Parse Cross-References**

Extract linked versions and sections:
- VALIDATION.md version X.X.X, section Y
- CHANGELOG.md version X.X.X, section Z

These indicate where completion will be recorded.

**Step 3: Perform Work**

Execute the actual task:
- Code changes
- Documentation updates
- Configuration modifications
- Test additions

**Step 4: Record Results**

Update task section with completion details:
```markdown
### A) Task Title

> [!IMPORTANT]
> Description of the task and what it involves.
> [VALIDATION.md], [ver:`X.X.X`, sect:`Y)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`Z)`]

**Completed:**
- Performed action 1
- Performed action 2
- Verification: passed
```

### 3. Complete Task

**Step 1: Mark Checklist Complete**

Update the checklist item:
```markdown
- [x] [A] Previously pending task  # Changed from [ ] to [x]
```

**Step 2: Update CHANGELOG.md**

Add or update the version entry:
```markdown
## X.X.X

- YEAR-MM-DD

> [!IMPORTANT]
> Work in progress for this version
> [TODO.md], [ver:`X.X.X`] - Work items
> [VALIDATION.md], [ver:`X.X.X`] - Validation

### A) Category - STATUS

| Component | Status | Reference |
| --------- | ------ | --------- |
| Component | ✅ | [VALIDATION.md], [ver:`X.X.X`, sect:`Y)`] |
```

**Step 3: Update VALIDATION.md (if verification performed)**

```markdown
## X.X.X

### A) Verified Component

> [!NOTE]
> Verification of component functionality
> [TODO.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]

**Verification:**
- Test: passed
- Lint: clean
- Type: clean
```

### 4. Complete Version

When ALL tasks in a version are complete (`[x]`):

**Step 1: Verify All Complete**
```python
# Pseudo-logic
tasks = parse_tasks(todo_md)
all_complete = all(task.checked for task in tasks)
if not all_complete:
    raise "Cannot complete version - pending tasks remain"
```

**Step 2: Finalize CHANGELOG Entry**

Ensure version entry is complete:
- All sections have status tables
- All cross-references are accurate
- Summary blockquote is finalized

**Step 3: Finalize VALIDATION Entry**

Ensure all verifications recorded:
- Test results documented
- Linter results documented
- Cross-references accurate

**Step 4: Archive TODO Version**

```bash
# Copy current TODO.md to archive
cp TODO.md docs/TODO/complete/X.X.X.md
```

The archived file preserves:
- Complete version header
- All task checklists (all `[x]`)
- All task sections with completion details
- All cross-references

**Step 5: Increment Root TODO.md**

Replace content with next version:
```markdown
# TODO.md

## X.X.Y

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

- YEAR-MM-DD

> [!TIP]
> All previous tasks complete. Ready for new work items.
> Previous version: [docs/TODO/complete/X.X.X.md]
> Completed versions: [docs/TODO/complete/](docs/TODO/complete/)

---
```

**Step 6: Verify Archive**

```bash
# Confirm archive exists
ls docs/TODO/complete/X.X.X.md  # Should exist
```

### 5. Add New Tasks

When new work is identified:

**Step 1: Determine Next Letter**

Find highest letter in current version:
```markdown
- [ ] [A] Existing task
- [ ] [B] Existing task
# Next letter: C
```

**Step 2: Add Checklist Item**

```markdown
- [ ] [A] Existing task
- [ ] [B] Existing task
- [ ] [C] New task description
```

**Step 3: Add Task Section**

After existing sections:
```markdown
### C) New Task Title

> [!IMPORTANT]
> Detailed description of what this task involves.
> Why it's needed, what will change.
> [VALIDATION.md], [ver:`X.X.X`, sect:`C)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`C)`]
```

**Step 4: Update Status**

If status was "ready for new work", update to active:
```markdown
> status: 'tracking TODO items and outstanding work'
```

---

## SD Workflow (SeekAndDestroy)

### Core Philosophy

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

### Workflow Overview

SD systematically reviews the entire codebase:
1. Divides code into quadrants (logical groupings)
2. Scans each quadrant for integration status
3. Flags findings with type and severity
4. Resolves by integration (not deletion)
5. Verifies all changes work correctly

### Quadrant System

Default quadrants (customize per project):

| Quadrant | Directories | Focus |
|----------|-------------|-------|
| Q1 | core/, adapters/, assets/ | Core business logic, external interfaces |
| Q2 | cli/, commands/ | User-facing interfaces |
| Q3 | ui/, components/, animation/ | Visual elements |
| Q4 | tests/, utils/, logging/ | Support infrastructure |

Quadrants should be:
- Logically cohesive
- Approximately equal in scope
- Independent enough for isolated review

### SD:R - RECON Phase

**Trigger:** `SD:R` or `crowndoc: SD` with no prior state

**Purpose:** Map the codebase, categorize into quadrants, establish scope

**Execution:**

**Step 1: Scan Project Structure**
```
list_dir recursive on project root
```

**Step 2: Categorize Files**

For each file/directory:
- Match against quadrant patterns
- Count files per quadrant
- Identify uncategorized items

**Step 3: Generate Quadrant Summary**

```markdown
## SD.md

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: 'codebase review in progress'

---

### RECON Summary

| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | core/, adapters/, assets/ | 15 | PENDING |
| Q2 | cli/, commands/ | 12 | PENDING |
| Q3 | ui/, components/, animation/ | 28 | PENDING |
| Q4 | tests/, utils/, logging/ | 45 | PENDING |
| Total | | 100 | |

### Uncategorized
- scripts/ (3 files) - consider adding to Q4
- docs/ (10 files) - documentation, not code
```

**Step 4: Update SD.md**

Create or update SD.md with:
- PROTOCOL block
- Quadrant summary table
- Status indicators
- Recommendation for first quadrant

**Step 5: Output Next Action**

```
SD:R complete.

Quadrant summary:
- Q1: 15 files (core, adapters, assets)
- Q2: 12 files (cli, commands)
- Q3: 28 files (ui, components, animation)
- Q4: 45 files (tests, utils, logging)

Recommend: Start with Q1 (smallest, core functionality)

Next: SD:S Q1
```

### SD:S - SCAN Phase

**Trigger:** `SD:S Q1`, `SD:S Q2`, `SD:S Q3`, or `SD:S Q4`

**Purpose:** Deep analysis of one quadrant to identify integration issues

**Execution:**

**Step 1: Load Quadrant Files**

```
For each file in quadrant:
    file_list.append(file_path)
```

**Step 2: Symbol Analysis**

For each file:
```python
# Get overview of symbols
symbols = get_symbols_overview(file)

for symbol in symbols:
    # Check if exported (in __init__.py or __all__)
    is_exported = check_export_status(symbol)
    
    # Find references to this symbol
    references = find_referencing_symbols(symbol)
    
    # Analyze integration status
    if is_exported and len(references) == 0:
        # Exported but never used - FINDING
        flag_as_unused(symbol, severity=HIGH)
    elif not is_exported and len(references) == 0:
        # Internal and unused - check if it's called internally
        internal_refs = find_internal_references(symbol, file)
        if len(internal_refs) == 0:
            flag_as_unused(symbol, severity=MEDIUM)
```

**Step 3: Import Analysis**

For each file:
```python
imports = parse_imports(file)
used_symbols = find_used_symbols(file)

for imported in imports:
    if imported not in used_symbols:
        flag_as_unused_import(imported, severity=LOW)
```

**Step 4: Integration Path Analysis**

For each flagged symbol:
```python
# Trace potential integration paths
entry_points = find_cli_entry_points()
ui_components = find_ui_entry_points()

for entry in entry_points + ui_components:
    # Can this symbol connect to an entry?
    path = find_connection_path(symbol, entry)
    if path:
        record_integration_path(symbol, path)
```

**Step 5: Investigation (CRITICAL)**

For EACH flagged item, DO NOT just flag - INVESTIGATE:

```markdown
### Investigation: unused_function in core/cache.py

**Symbol:** `calculate_cache_key`
**Location:** core/cache.py:45
**Type:** Function
**Exported:** Yes (in __init__.py)
**References:** None found

**Investigation:**
1. Surrounding context: Part of caching module
2. Git history: Added in commit abc123 "Add cache infrastructure"
3. Related symbols: `CacheManager`, `cache_store` - all used
4. TODO/FIXME: None found
5. Docstring: "Calculate unique cache key for search results"

**Analysis:**
This appears to be infrastructure for result caching that was added but not yet
connected to the search workflow. The search engine yields results but doesn't
cache them for repeated queries.

**Integration Path:**
1. SearchEngine.search() should check cache first
2. On cache miss, perform search and store result
3. calculate_cache_key generates the lookup key

**Recommendation:** Type I (INTEGRATION) - connect to search workflow
**Severity:** MEDIUM (functionality incomplete, not broken)
```

**Step 6: Document Findings**

Update SD.md with findings:
```markdown
### Q1 SCAN - Findings

| ID | Location | Type | Severity | Summary |
|----|----------|------|----------|---------|
| 1 | core/cache.py:45 | I | MEDIUM | Cache infrastructure not connected |
| 2 | core/utils.py:12 | U | LOW | Unused helper function |
| 3 | adapters/base.py:89 | T | LOW | Missing return type annotation |

---

### Finding 1: Cache Infrastructure

> [!WARNING]
> type: I (INTEGRATION)
> severity: MEDIUM
> location: `core/cache.py:45`

**Symbol:** `calculate_cache_key`
**Analysis:** Cache infrastructure exists but not connected to search workflow.
**Integration Path:**
1. Modify SearchEngine.search() to use CacheManager
2. Add cache lookup before network request
3. Store results after successful search

**Generated TODO:**
[TODO.md], [ver:`X.X.X`, sect:`A)`] - Integrate cache into search workflow
```

**Step 7: Generate TODO Entries**

For findings requiring work:
```markdown
# Add to TODO.md

- [ ] [A] Integrate cache infrastructure into search workflow

---

### A) Cache Integration

> [!IMPORTANT]
> SD finding: Cache infrastructure (calculate_cache_key, CacheManager) 
> exists but not connected to search workflow.
> [SD.md], [ver:`X.X.X`, sect:`Q1 Finding 1`]
> [VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

### SD:F - FLAG Phase

**Trigger:** `SD:F`

**Purpose:** Review and organize all findings before resolution

**Execution:**

**Step 1: Aggregate Findings**

Collect all findings from SD.md:
```markdown
| Quadrant | ID | Type | Severity | Status |
|----------|-----|------|----------|--------|
| Q1 | 1 | I | MEDIUM | NEW |
| Q1 | 2 | U | LOW | NEW |
| Q1 | 3 | T | LOW | NEW |
| Q3 | 4 | U | HIGH | NEW |
| Q3 | 5 | P | MEDIUM | NEW |
```

**Step 2: Prioritize**

Order by:
1. Severity (HIGH → MEDIUM → LOW)
2. Type (U → I → T → P)
3. Quadrant order

**Step 3: Verify TODO Entries**

For each finding:
```python
# Check TODO.md has corresponding entry
todo_entry = find_todo_entry(finding.cross_reference)
if not todo_entry:
    create_todo_entry(finding)
```

**Step 4: Output Resolution Plan**

```
SD:F complete.

Findings by priority:
1. [HIGH] Q3 Finding 4: Unused UI component - needs integration
2. [MEDIUM] Q1 Finding 1: Cache not connected - needs integration
3. [MEDIUM] Q3 Finding 5: Pattern violation - needs standardization
4. [LOW] Q1 Finding 2: Unused helper - investigate purpose
5. [LOW] Q1 Finding 3: Missing type - add annotation

All findings have TODO entries.

Next: SD:X (resolve findings)
```

### SD:X - RESOLVE Phase

**Trigger:** `SD:X`

**Purpose:** Execute resolution for each finding

**Execution by Finding Type:**

#### Type U (UNUSED) Resolution

**Philosophy:** Unused code exists for a reason. Find that reason.

**Step 1: Deep Investigation**
```python
# Investigate thoroughly
context = read_surrounding_code(symbol)
history = git_log(symbol.file)
comments = find_comments_near(symbol)
tests = find_related_tests(symbol)
```

**Step 2: Determine Integration Point**
```python
# Where SHOULD this be used?
candidates = []

# Check CLI commands
for command in cli_commands:
    if symbol_could_serve(command, symbol):
        candidates.append(command)

# Check UI components
for component in ui_components:
    if symbol_could_serve(component, symbol):
        candidates.append(component)

# Check core workflows
for workflow in core_workflows:
    if symbol_could_serve(workflow, symbol):
        candidates.append(workflow)
```

**Step 3: Implement Integration**
```python
# Add the missing connection
best_candidate = select_best_integration(candidates)
implement_integration(symbol, best_candidate)
```

**Step 4: Verify Integration**
```bash
# Run tests
pytest tests/

# Verify symbol is now referenced
find_referencing_symbols(symbol)  # Should return results
```

**Step 5: Update Documents**
```markdown
# TODO.md - mark complete
- [x] [A] Integrate cache infrastructure

# CHANGELOG.md - record completion
### A) Cache Integration - COMPLETE
| Component | Status | Reference |
| --------- | ------ | --------- |
| Cache integration | ✅ | [VALIDATION.md], [ver:`X.X.X`, sect:`A)`] |

# SD.md - mark resolved
| ID | Location | Type | Severity | Status |
|----|----------|------|----------|--------|
| 1 | core/cache.py:45 | I | MEDIUM | RESOLVED |
```

#### Type I (INTEGRATION) Resolution

**Step 1: Trace Connection Path**
```python
# Map from component to CLI/UI entry
component = find_component(finding.location)
entry_point = find_nearest_entry_point(component)
path = trace_path(component, entry_point)
```

**Step 2: Identify Missing Links**
```python
# Find where the chain breaks
for i, node in enumerate(path):
    next_node = path[i + 1] if i + 1 < len(path) else None
    if next_node and not are_connected(node, next_node):
        missing_links.append((node, next_node))
```

**Step 3: Implement Connections**
```python
for source, target in missing_links:
    add_integration_code(source, target)
```

**Step 4: Test End-to-End**
```bash
# Verify integration works
python -m cli.main [command that should use component]
```

#### Type T (TYPE) Resolution

**Step 1: Analyze Required Type**
```python
# Determine correct type from usage
usages = find_symbol_usages(symbol)
inferred_type = infer_type_from_usages(usages)
```

**Step 2: Add Annotation**
```python
# Add proper type annotation
# Before:
def calculate_cache_key(query, options):
    ...

# After:
def calculate_cache_key(query: SearchQuery, options: SearchOptions) -> str:
    ...
```

**Step 3: Verify with Type Checker**
```bash
mypy mudhound/
```

#### Type P (PATTERN) Resolution

**Step 1: Identify Project Pattern**
```python
# Find established pattern
similar_code = find_similar_patterns(symbol)
standard_pattern = extract_common_pattern(similar_code)
```

**Step 2: Apply Pattern**
```python
# Refactor to match pattern
refactor_to_pattern(symbol, standard_pattern)
```

**Step 3: Verify Consistency**
```bash
# Check all similar code follows pattern
ruff check mudhound/
```

### SD:V - VERIFY Phase

**Trigger:** `SD:V`

**Purpose:** Verify all resolutions work correctly, complete the pass

**Execution:**

**Step 1: Run Full Test Suite**
```bash
pytest tests/ -v
# Record: X passed, Y failed
# If failures: investigate and fix before continuing
```

**Step 2: Run Type Checker**
```bash
mypy mudhound/
# Record: clean or N errors
# If errors: investigate and fix before continuing
```

**Step 3: Run Linter**
```bash
ruff check mudhound/
# Record: clean or N issues
# If issues: investigate and fix before continuing
```

**Step 4: Manual Verification**
```
For each resolved finding:
1. Verify the integration works as expected
2. Check no regressions introduced
3. Confirm cross-references are accurate
```

**Step 5: Update VALIDATION.md**
```markdown
## X.X.X

### A) SD Pass Q1 - VERIFIED

> [!NOTE]
> workflow: SD
> pass: [docs/SD/complete/X.X.X-Q1.md]
> status: COMPLETE

**Verification:**
- pytest: 150 passed, 0 failed
- mypy: clean
- ruff: clean
- Manual: all integrations functional

**Findings Resolved:**
- Finding 1: Cache integration ✅
- Finding 2: Unused helper integrated ✅
- Finding 3: Type annotation added ✅

**Cross-references:**
- [TODO.md], [ver:`X.X.X`, sect:`A)`-`C)`]
- [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

**Step 6: Archive SD Pass**
```bash
# Create archive file
cp SD.md docs/SD/complete/X.X.X-Q1.md
```

**Step 7: Update SD.md for Next Quadrant**
```markdown
## SD.md

## X.X.X

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: 'codebase review in progress'

---

### Progress

| Quadrant | Status | Pass |
|----------|--------|------|
| Q1 | ✅ COMPLETE | [docs/SD/complete/X.X.X-Q1.md] |
| Q2 | PENDING | - |
| Q3 | PENDING | - |
| Q4 | PENDING | - |

> [!TIP]
> Q1 complete. Proceed with: SD:S Q2
```

### Complete SD Workflow

When all quadrants complete:

**Step 1: Verify All Quadrants**
```markdown
| Quadrant | Status | Pass |
|----------|--------|------|
| Q1 | ✅ COMPLETE | [docs/SD/complete/X.X.X-Q1.md] |
| Q2 | ✅ COMPLETE | [docs/SD/complete/X.X.X-Q2.md] |
| Q3 | ✅ COMPLETE | [docs/SD/complete/X.X.X-Q3.md] |
| Q4 | ✅ COMPLETE | [docs/SD/complete/X.X.X-Q4.md] |
```

**Step 2: Final Verification**
```bash
# Full suite
pytest tests/
mypy mudhound/
ruff check mudhound/
```

**Step 3: Archive Final SD State**
```bash
# Archive overall SD for this version
cp SD.md docs/SD/complete/X.X.X-final.md
```

**Step 4: Reset SD.md**
```markdown
## SD.md

## X.X.Y

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: 'ready for new codebase review'

---

> [!TIP]
> Previous review: [docs/SD/complete/X.X.X-final.md]
> All quadrants verified. Ready for new SD workflow.
```

---

## Finding Types Reference

### U: UNUSED

**Definition:** Code exists but has no references

**Investigation Required:**
1. Why was it created?
2. What was the intended use?
3. Is there a TODO/FIXME about it?
4. Was it part of incomplete work?

**Resolution:** Find integration point, NEVER delete first

**Example Findings:**
- Function exported but never called
- Class defined but never instantiated
- Import never used
- Variable assigned but never read

### I: INTEGRATION

**Definition:** Code exists and is referenced, but not connected to user-facing workflow

**Investigation Required:**
1. What's the integration path?
2. Which entry point should connect?
3. What's blocking the connection?

**Resolution:** Add missing integration code

**Example Findings:**
- Component fully implemented but not in CLI
- Utility function called internally but not exposed
- Feature complete but not accessible

### T: TYPE

**Definition:** Missing or incorrect type annotations

**Investigation Required:**
1. What's the correct type?
2. What do usages expect?
3. Are there related typed symbols?

**Resolution:** Add proper type annotation

**Example Findings:**
- Function missing return type
- Parameter using `Any` when specific type known
- Generic where specific type appropriate

### P: PATTERN

**Definition:** Code doesn't follow project patterns/standards

**Investigation Required:**
1. What's the established pattern?
2. Why does this code differ?
3. Was there a reason for deviation?

**Resolution:** Refactor to match pattern

**Example Findings:**
- Different error handling style
- Inconsistent naming convention
- Different module structure

---

## Cross-Reference Maintenance

### Creating References

Every workflow action creates cross-references:

```markdown
# When creating TODO from SD finding:
[SD.md], [ver:`X.X.X`, sect:`Q1 Finding 1`]

# When completing task:
[CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]

# When verifying:
[VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
```

### Validating References

Before completing any version:
```python
for reference in find_all_references(document):
    target = resolve_reference(reference)
    if not target.exists():
        report_broken_reference(reference)
```

### Updating References on Version Change

When archiving:
```python
# References to archived version should use archive path
old_ref = "[TODO.md], [ver:`0.0.1`, sect:`A)`]"
# Still valid - version is in TODO.md history or archive
# Cross-reference points to version, not file location
```

---

## Workflow State Detection

### Detecting Active Workflow

```python
def detect_active_workflow():
    # Check SD.md first (higher priority)
    sd_status = read_sd_status()
    if sd_status not in ["READY", "COMPLETE"]:
        return "SD", sd_status
    
    # Check TODO.md
    pending_tasks = count_pending_tasks()
    if pending_tasks > 0:
        return "TODO", pending_tasks
    
    # No active workflow
    return None, None
```

### Resume Points

**SD Resume:**
```
SD:R COMPLETE → Resume at SD:S
SD:S Q1 COMPLETE → Resume at SD:S Q2 (or SD:F if all scanned)
SD:F COMPLETE → Resume at SD:X
SD:X COMPLETE → Resume at SD:V
SD:V COMPLETE for Qn → Resume at SD:S Q(n+1)
```

**TODO Resume:**
```
Tasks pending → Resume at first unchecked task
All tasks checked → Trigger version completion
No tasks → Ready for new work
```

---

## Error Recovery

### Interrupted Workflow

If workflow interrupted mid-execution:

1. Check document state
2. Identify last completed step
3. Resume from that point
4. Verify no partial state

### Conflicting Changes

If documents modified externally:

1. Archive current state to pending/
2. Resolve conflicts manually
3. Resume workflow
4. Update cross-references

### Failed Verification

If SD:V fails:

1. Identify failing tests/checks
2. Diagnose root cause
3. Fix without breaking resolutions
4. Re-run verification
5. Only proceed when all pass

---

## Best Practices

### DO

- Always investigate before flagging
- Document integration paths for every finding
- Run full verification before completing phases
- Archive completed work immediately
- Keep cross-references accurate

### DON'T

- Flag without investigation
- Delete code without explicit approval
- Skip verification steps
- Leave partial work in LIVE documents
- Create orphaned references

---
