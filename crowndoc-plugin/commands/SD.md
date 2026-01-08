---
description: Execute the SeekAndDestroy workflow - systematic codebase review with integration bias, NEVER deletion
argument-hint: "[phase] [quadrant] (e.g., 'R', 'S Q1', 'S Q2', 'F', 'X', 'V')"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

# /crowndoc:SD

Execute the SeekAndDestroy (SD) workflow for systematic codebase review.

---

## Purpose

The SD workflow provides systematic codebase analysis to identify:
1. Unused code that should be INTEGRATED (not deleted)
2. Disconnected components that need wiring
3. Missing type annotations
4. Pattern violations

**CRITICAL PRINCIPLE:**

> [!CAUTION]
> **INTEGRATION OVER DELETION**
>
> The SD workflow is NOT about finding code to delete.
> Unused code represents value: incomplete features, infrastructure, defensive code.
>
> NEVER delete as first solution.
> ALWAYS investigate origin and intent.
> ALWAYS find integration path.
> Deletion requires EXPLICIT user approval.

---

## Workflow Phases

```
SD:R (Recon)
    ↓
SD:S Q1 → SD:S Q2 → SD:S Q3 → SD:S Q4 (Scan each quadrant)
    ↓
SD:F (Flag - organize findings)
    ↓
SD:X (Resolve - execute integrations)
    ↓
SD:V (Verify - confirm and archive)
```

---

## Phase SD:R - RECON

### Trigger

- `crowndoc: SD` with no prior state
- `SD:R` explicit command
- Fresh SD.md (status "ready")

### Purpose

Map the entire codebase, categorize into quadrants, establish scope for systematic review.

### Execution

**Step 1: Recursive Directory Scan**

```python
# Get complete project structure
all_items = list_dir(".", recursive=True)

# Separate files and directories
directories = [item for item in all_items if is_directory(item)]
files = [item for item in all_items if is_file(item)]

# Filter to code files only
code_extensions = [".py", ".js", ".ts", ".rs", ".go", ".java", ".cpp", ".c", ".h"]
code_files = [f for f in files if any(f.endswith(ext) for ext in code_extensions)]
```

**Step 2: Load Quadrant Configuration**

```python
# Check for custom quadrant config in Docs/crowndoc.md
if file_exists("Docs/crowndoc.md"):
    crowndoc_spec = read_file("Docs/crowndoc.md")
    quadrants = parse_quadrant_config(crowndoc_spec)
else:
    # Use default quadrants
    quadrants = {
        "Q1": {
            "name": "Core",
            "patterns": ["core", "lib", "src/core", "adapters", "assets", "models"],
            "description": "Core business logic and external interfaces"
        },
        "Q2": {
            "name": "CLI/Commands",
            "patterns": ["cli", "commands", "cmd", "bin", "scripts", "api"],
            "description": "User-facing interfaces"
        },
        "Q3": {
            "name": "UI",
            "patterns": ["ui", "components", "views", "templates", "animation", "frontend"],
            "description": "Visual and UI elements"
        },
        "Q4": {
            "name": "Support",
            "patterns": ["tests", "test", "utils", "helpers", "logging", "config"],
            "description": "Support infrastructure"
        }
    }
```

**Step 3: Categorize Files**

```python
categorized = {q: [] for q in quadrants.keys()}
uncategorized = []

for file_path in code_files:
    matched = False
    for qname, qdata in quadrants.items():
        for pattern in qdata["patterns"]:
            if pattern in file_path.lower():
                categorized[qname].append(file_path)
                matched = True
                break
        if matched:
            break
    
    if not matched:
        uncategorized.append(file_path)

# Count files per quadrant
for qname in quadrants:
    quadrants[qname]["files"] = categorized[qname]
    quadrants[qname]["count"] = len(categorized[qname])
```

**Step 4: Update SD.md**

```python
sd_version = get_current_version("SD.md") or "0.0.1"

sd_content = f"""# SeekAndDestroy

## {sd_version}

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: 'recon complete - ready for scanning'
> principle: INTEGRATION OVER DELETION

---

- {TODAY_DATE}

### RECON Summary

| Quadrant | Name | Directories | Files | Status |
|----------|------|-------------|-------|--------|
| Q1 | {quadrants["Q1"]["name"]} | {quadrants["Q1"]["patterns"]} | {quadrants["Q1"]["count"]} | PENDING |
| Q2 | {quadrants["Q2"]["name"]} | {quadrants["Q2"]["patterns"]} | {quadrants["Q2"]["count"]} | PENDING |
| Q3 | {quadrants["Q3"]["name"]} | {quadrants["Q3"]["patterns"]} | {quadrants["Q3"]["count"]} | PENDING |
| Q4 | {quadrants["Q4"]["name"]} | {quadrants["Q4"]["patterns"]} | {quadrants["Q4"]["count"]} | PENDING |
| Total | | | {sum(q["count"] for q in quadrants.values())} | |

### Uncategorized Files

{chr(10).join(f"- {f}" for f in uncategorized) if uncategorized else "None - all files categorized"}

> [!TIP]
> Recommend starting with Q1 (core functionality).
> Use `SD:S Q1` to begin scanning.

---

"""

write_file("SD.md", sd_content)
```

**Step 5: Output Summary**

```
SD:R complete - Recon finished

╔═══════════════════════════════════════════════════════════════════╗
║                        QUADRANT SUMMARY                           ║
╠═══════════════════════════════════════════════════════════════════╣
║ Q1 │ Core           │ core/, adapters/, assets/    │ 15 files    ║
║ Q2 │ CLI/Commands   │ cli/, commands/              │ 12 files    ║
║ Q3 │ UI             │ ui/, components/, animation/ │ 28 files    ║
║ Q4 │ Support        │ tests/, utils/, logging/     │ 45 files    ║
╠═══════════════════════════════════════════════════════════════════╣
║ Total: 100 files                                                  ║
╚═══════════════════════════════════════════════════════════════════╝

Uncategorized: {N} files (see SD.md for list)

Recommendation: Start with Q1 (smallest, contains core functionality)

Next: SD:S Q1
```

---

## Phase SD:S - SCAN

### Trigger

- `SD:S Q1`, `SD:S Q2`, `SD:S Q3`, or `SD:S Q4`

### Purpose

Deep analysis of one quadrant to identify integration issues, unused code, type problems, and pattern violations.

### Execution

**Step 1: Load Quadrant Files**

```python
# Get files for target quadrant
quadrant = "Q1"  # From argument
sd_content = read_file("SD.md")
quadrant_files = parse_quadrant_files(sd_content, quadrant)

print(f"Scanning {quadrant}: {len(quadrant_files)} files")
```

**Step 2: Analyze Each File**

```python
findings = []

for file_path in quadrant_files:
    print(f"  Analyzing: {file_path}")
    
    # Get symbol overview
    symbols = get_symbols_overview(file_path)
    
    for symbol in symbols:
        # Check export status
        is_exported = check_if_exported(symbol, file_path)
        
        # Find references to this symbol
        references = find_referencing_symbols(symbol.name, file_path)
        
        # Analyze
        if is_exported and len(references) == 0:
            # Exported but never used externally - investigate!
            findings.append({
                "type": "U",
                "severity": "HIGH",
                "location": f"{file_path}:{symbol.line}",
                "symbol": symbol.name,
                "issue": "Exported symbol with no external references",
                "status": "NEW"
            })
        
        # Check for type annotations
        if symbol.kind in ["function", "method"] and not has_type_annotations(symbol):
            findings.append({
                "type": "T",
                "severity": "LOW",
                "location": f"{file_path}:{symbol.line}",
                "symbol": symbol.name,
                "issue": "Missing type annotations",
                "status": "NEW"
            })
```

**Step 3: Analyze Imports**

```python
for file_path in quadrant_files:
    imports = parse_imports(file_path)
    used_names = find_used_names(file_path)
    
    for imp in imports:
        if imp.name not in used_names:
            findings.append({
                "type": "U",
                "severity": "LOW",
                "location": f"{file_path}:{imp.line}",
                "symbol": imp.name,
                "issue": "Unused import",
                "status": "NEW"
            })
```

**Step 4: INVESTIGATE Each Finding (CRITICAL)**

This step is NOT optional. For EVERY finding:

```python
for finding in findings:
    print(f"  Investigating: {finding['symbol']} at {finding['location']}")
    
    # Read surrounding context
    file_content = read_file(finding['location'].split(':')[0])
    context = extract_surrounding_lines(file_content, finding['location'], context=10)
    
    # Check for related comments/docstrings
    comments = extract_comments_near(file_content, finding['location'])
    
    # Check git history (if available)
    try:
        git_log = run_command(f"git log -3 --oneline -- {finding['location'].split(':')[0]}")
        finding['git_history'] = git_log
    except:
        finding['git_history'] = "Git history unavailable"
    
    # Search for TODO/FIXME references
    todos = search_for_pattern(f"TODO.*{finding['symbol']}|FIXME.*{finding['symbol']}")
    
    # Hypothesize purpose
    if finding['type'] == 'U':
        # Look for where this SHOULD be used
        potential_callers = find_potential_integration_points(finding['symbol'])
        finding['integration_candidates'] = potential_callers
    
    # Document investigation
    finding['investigation'] = {
        "context": context,
        "comments": comments,
        "todos": todos,
        "hypothesis": generate_hypothesis(finding)
    }
```

**Step 5: Document Findings in SD.md**

```python
# Read current SD.md
sd_content = read_file("SD.md")

# Add findings section for this quadrant
findings_section = f"""

### {quadrant} SCAN - Findings

| ID | Location | Type | Severity | Symbol | Status |
|----|----------|------|----------|--------|--------|
"""

for i, finding in enumerate(findings, 1):
    findings_section += f"| {i} | `{finding['location']}` | {finding['type']} | {finding['severity']} | {finding['symbol']} | {finding['status']} |\n"

findings_section += "\n---\n"

# Add detailed finding descriptions
for i, finding in enumerate(findings, 1):
    findings_section += f"""
### {quadrant} Finding {i}: {finding['symbol']}

> [!WARNING]
> type: {finding['type']} ({TYPE_NAMES[finding['type']]})
> severity: {finding['severity']}
> location: `{finding['location']}`

**Issue:** {finding['issue']}

**Investigation:**
```
Context:
{finding['investigation']['context']}

Related comments:
{finding['investigation']['comments']}

Git history:
{finding['git_history']}

Related TODOs:
{finding['investigation']['todos']}
```

**Hypothesis:** {finding['investigation']['hypothesis']}

**Integration Candidates:** {finding.get('integration_candidates', 'N/A')}

**Recommendation:** {generate_recommendation(finding)}

---

"""

# Update quadrant status
sd_content = update_quadrant_status(sd_content, quadrant, "SCANNED")

# Append findings
sd_content += findings_section

write_file("SD.md", sd_content)
```

**Step 6: Generate TODO Entries**

```python
# For significant findings, create TODO entries
todo_content = read_file("TODO.md")

for finding in findings:
    if finding['severity'] in ['HIGH', 'MEDIUM']:
        # Determine next available letter
        next_letter = get_next_task_letter(todo_content)
        
        # Create checklist item
        checklist_item = f"- [ ] [{next_letter}] {finding['issue']}: {finding['symbol']}"
        
        # Create section
        section = f"""
### {next_letter}) {finding['issue']}

> [!IMPORTANT]
> SD finding from {quadrant} scan.
> [SD.md], [ver:`{sd_version}`, sect:`{quadrant} Finding {i}`]
> [VALIDATION.md], [ver:`{todo_version}`, sect:`{next_letter})`]
> [CHANGELOG.md], [ver:`{todo_version}`, sect:`{next_letter})`]

**Symbol:** `{finding['symbol']}`
**Location:** `{finding['location']}`
**Analysis:** {finding['investigation']['hypothesis']}
**Integration Path:** {finding.get('integration_candidates', 'To be determined')}

"""
        
        # Add to TODO.md
        todo_content = add_task_to_todo(todo_content, checklist_item, section)

write_file("TODO.md", todo_content)
```

**Step 7: Output Summary**

```
SD:S {quadrant} complete

╔═══════════════════════════════════════════════════════════════════╗
║                        SCAN RESULTS                               ║
╠═══════════════════════════════════════════════════════════════════╣
║ Files scanned: {N}                                                ║
║ Findings: {TOTAL}                                                 ║
║   ├── HIGH severity: {N}                                          ║
║   ├── MEDIUM severity: {N}                                        ║
║   └── LOW severity: {N}                                           ║
║                                                                   ║
║ By type:                                                          ║
║   ├── U (Unused): {N}                                             ║
║   ├── I (Integration): {N}                                        ║
║   ├── T (Type): {N}                                               ║
║   └── P (Pattern): {N}                                            ║
╚═══════════════════════════════════════════════════════════════════╝

TODO entries created: {N}
Cross-references: [SD.md], [ver:{VERSION}] → [TODO.md]

Next quadrant: {NEXT_Q} ({N} files)
Or: SD:F to review and organize all findings
```

---

## Phase SD:F - FLAG

### Trigger

- `SD:F` explicit command

### Purpose

Review and organize all findings before resolution phase.

### Execution

**Step 1: Aggregate All Findings**

```python
sd_content = read_file("SD.md")

# Parse all findings from all quadrants
all_findings = []
for quadrant in ["Q1", "Q2", "Q3", "Q4"]:
    quadrant_findings = parse_quadrant_findings(sd_content, quadrant)
    all_findings.extend(quadrant_findings)

print(f"Total findings: {len(all_findings)}")
```

**Step 2: Prioritize Findings**

```python
# Sort by severity, then type
severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
type_order = {"U": 0, "I": 1, "T": 2, "P": 3}

all_findings.sort(key=lambda f: (
    severity_order.get(f['severity'], 99),
    type_order.get(f['type'], 99)
))
```

**Step 3: Verify TODO Entries**

```python
todo_content = read_file("TODO.md")

for finding in all_findings:
    if finding['severity'] in ['HIGH', 'MEDIUM']:
        # Check if TODO entry exists
        expected_ref = f"[SD.md], [ver:`{sd_version}`, sect:`{finding['id']}`]"
        if expected_ref not in todo_content:
            warn(f"Missing TODO entry for {finding['id']}")
            # Create missing entry
```

**Step 4: Generate Resolution Plan**

```python
resolution_plan = """
### Resolution Plan

#### Priority 1: HIGH Severity
"""

for f in all_findings:
    if f['severity'] == 'HIGH':
        resolution_plan += f"""
- [{f['id']}] {f['symbol']} ({f['type']})
  - Location: {f['location']}
  - Action: {get_resolution_action(f)}
  - TODO: [{f['todo_letter']}]
"""

resolution_plan += """
#### Priority 2: MEDIUM Severity
"""
# ... continue for MEDIUM, LOW

# Update SD.md
sd_content = append_section(sd_content, resolution_plan)
write_file("SD.md", sd_content)
```

**Step 5: Output**

```
SD:F complete - Findings organized

╔═══════════════════════════════════════════════════════════════════╗
║                      RESOLUTION PLAN                              ║
╠═══════════════════════════════════════════════════════════════════╣
║ Priority 1 (HIGH):                                                ║
║   [1] calculate_cache_key (U) → Integrate with SearchEngine      ║
║   [2] UIRenderer.flush (I) → Connect to search output            ║
║                                                                   ║
║ Priority 2 (MEDIUM):                                              ║
║   [3] ConfigManager.save (U) → Add config save command           ║
║   ...                                                             ║
║                                                                   ║
║ Priority 3 (LOW):                                                 ║
║   [7] adapter.search (T) → Add return type annotation            ║
║   ...                                                             ║
╚═══════════════════════════════════════════════════════════════════╝

All findings have TODO entries.

Next: SD:X (resolve findings in priority order)
```

---

## Phase SD:X - RESOLVE

### Trigger

- `SD:X` explicit command

### Purpose

Execute resolution for each finding, following "integration over deletion" principle.

### Execution by Finding Type

#### Type U (UNUSED) Resolution

**NEVER DELETE FIRST. Always find integration point.**

```python
for finding in findings_type_u:
    print(f"Resolving: {finding['symbol']}")
    
    # Step 1: Identify integration point
    integration_candidates = finding.get('integration_candidates', [])
    
    if not integration_candidates:
        # Find potential callers
        candidates = find_potential_callers(finding['symbol'])
        print(f"  Potential integration points: {candidates}")
    
    # Step 2: Select best integration
    best_candidate = select_best_integration(integration_candidates)
    
    # Step 3: Implement integration
    if best_candidate:
        # Add the call/import to integrate
        add_integration_code(finding['symbol'], best_candidate)
        
        # Verify integration
        refs = find_referencing_symbols(finding['symbol'])
        if len(refs) > 0:
            finding['status'] = 'RESOLVED'
            print(f"  ✅ Integrated into {best_candidate}")
        else:
            print(f"  ⚠️ Integration failed - needs manual review")
    else:
        # Cannot auto-integrate
        print(f"  ⚠️ No clear integration path - flagging for review")
        finding['status'] = 'NEEDS_REVIEW'
```

#### Type I (INTEGRATION) Resolution

```python
for finding in findings_type_i:
    print(f"Resolving: {finding['symbol']}")
    
    # Step 1: Trace current connection path
    path = trace_integration_path(finding['symbol'])
    print(f"  Current path: {' → '.join(path) if path else 'Disconnected'}")
    
    # Step 2: Find missing link
    entry_points = get_entry_points()  # CLI commands, UI entry, etc.
    
    for entry in entry_points:
        if could_connect(finding['symbol'], entry):
            # Step 3: Add missing connection
            add_connection(finding['symbol'], entry)
            print(f"  ✅ Connected to {entry}")
            finding['status'] = 'RESOLVED'
            break
```

#### Type T (TYPE) Resolution

```python
for finding in findings_type_t:
    print(f"Resolving: {finding['symbol']}")
    
    # Step 1: Analyze usage to infer types
    usages = find_symbol_usages(finding['symbol'])
    inferred_types = infer_types_from_usages(usages)
    
    # Step 2: Add annotations
    add_type_annotations(finding['symbol'], inferred_types)
    
    # Step 3: Verify with type checker
    result = run_command("mypy " + finding['location'].split(':')[0])
    if "error" not in result:
        finding['status'] = 'RESOLVED'
        print(f"  ✅ Types added, mypy clean")
    else:
        print(f"  ⚠️ Type errors remain: {result}")
```

#### Type P (PATTERN) Resolution

```python
for finding in findings_type_p:
    print(f"Resolving: {finding['symbol']}")
    
    # Step 1: Identify project pattern
    similar_code = find_similar_patterns(finding['symbol'])
    standard_pattern = extract_common_pattern(similar_code)
    
    # Step 2: Refactor to pattern
    refactor_to_pattern(finding['symbol'], standard_pattern)
    
    # Step 3: Verify consistency
    result = run_command("ruff check " + finding['location'].split(':')[0])
    if "error" not in result:
        finding['status'] = 'RESOLVED'
        print(f"  ✅ Pattern applied")
```

### Update Documents After Resolution

```python
# Update SD.md with resolution status
sd_content = read_file("SD.md")
for finding in all_findings:
    sd_content = update_finding_status(sd_content, finding['id'], finding['status'])
write_file("SD.md", sd_content)

# Update TODO.md - mark tasks complete
todo_content = read_file("TODO.md")
for finding in all_findings:
    if finding['status'] == 'RESOLVED' and finding.get('todo_letter'):
        todo_content = mark_task_complete(todo_content, finding['todo_letter'])
write_file("TODO.md", todo_content)

# Update CHANGELOG.md
changelog_content = read_file("CHANGELOG.md")
# Add resolution entries...
write_file("CHANGELOG.md", changelog_content)
```

### Output

```
SD:X complete - Resolutions executed

╔═══════════════════════════════════════════════════════════════════╗
║                      RESOLUTION SUMMARY                           ║
╠═══════════════════════════════════════════════════════════════════╣
║ Resolved: {N}                                                     ║
║   ├── Type U (Unused → Integrated): {N}                           ║
║   ├── Type I (Disconnected → Connected): {N}                      ║
║   ├── Type T (Untyped → Annotated): {N}                           ║
║   └── Type P (Non-standard → Pattern): {N}                        ║
║                                                                   ║
║ Needs Review: {N}                                                 ║
║   └── [Details of items needing manual attention]                 ║
╚═══════════════════════════════════════════════════════════════════╝

Documents updated:
├── SD.md - Finding statuses updated
├── TODO.md - Tasks marked complete
└── CHANGELOG.md - Completions recorded

Next: SD:V (verify all resolutions)
```

---

## Phase SD:V - VERIFY

### Trigger

- `SD:V` explicit command

### Purpose

Verify all resolutions work correctly, run tests, complete the pass.

### Execution

**Step 1: Run Test Suite**

```bash
pytest tests/ -v
```

```python
test_result = run_command("pytest tests/ -v")
tests_passed = parse_test_results(test_result)

if tests_passed['failed'] > 0:
    print(f"⚠️ {tests_passed['failed']} tests failed")
    # Must investigate before proceeding
    raise "Tests failing - cannot complete verification"
else:
    print(f"✅ {tests_passed['passed']} tests passed")
```

**Step 2: Run Type Checker**

```bash
mypy mudhound/
```

```python
mypy_result = run_command("mypy mudhound/")
if "error" in mypy_result:
    print(f"⚠️ Type errors found")
    # Must fix before proceeding
else:
    print(f"✅ Type check clean")
```

**Step 3: Run Linter**

```bash
ruff check mudhound/
```

```python
ruff_result = run_command("ruff check mudhound/")
if "error" in ruff_result or "warning" in ruff_result:
    print(f"⚠️ Lint issues found")
else:
    print(f"✅ Lint check clean")
```

**Step 4: Manual Verification**

```python
# For each resolved finding, verify it works
for finding in resolved_findings:
    print(f"Verify: {finding['symbol']}")
    
    # Check it's now referenced
    refs = find_referencing_symbols(finding['symbol'])
    if len(refs) > 0:
        print(f"  ✅ Now has {len(refs)} references")
    else:
        print(f"  ⚠️ Still no references")
```

**Step 5: Update VALIDATION.md**

```python
validation_content = read_file("VALIDATION.md")

validation_entry = f"""
## {validation_version}

### A) SD Pass {quadrant} - VERIFIED

> [!NOTE]
> workflow: SD
> pass: [docs/SD/complete/{sd_version}-{quadrant}.md]
> status: COMPLETE

**Verification:**
- pytest: {tests_passed['passed']} passed, {tests_passed['failed']} failed
- mypy: {'clean' if mypy_clean else 'errors'}
- ruff: {'clean' if ruff_clean else 'issues'}
- Manual: all integrations verified

**Findings Resolved:**
{chr(10).join(f"- Finding {f['id']}: {f['symbol']} ✅" for f in resolved_findings)}

**Cross-references:**
- [TODO.md], [ver:`{todo_version}`, sect:`A)`-`{last_letter})`]
- [CHANGELOG.md], [ver:`{changelog_version}`, sect:`A)`]
- [SD.md], [ver:`{sd_version}`]

---
"""

validation_content = add_version_entry(validation_content, validation_entry)
write_file("VALIDATION.md", validation_content)
```

**Step 6: Archive SD Pass**

```python
# Copy current SD quadrant content to archive
archive_content = extract_quadrant_content(sd_content, quadrant)
archive_path = f"docs/SD/complete/{sd_version}-{quadrant}.md"
write_file(archive_path, archive_content)

print(f"✅ Archived to {archive_path}")
```

**Step 7: Update SD.md for Next Quadrant**

```python
# Mark quadrant complete
sd_content = update_quadrant_status(sd_content, quadrant, "✅ COMPLETE")

# Check if more quadrants pending
pending_quadrants = get_pending_quadrants(sd_content)

if pending_quadrants:
    next_q = pending_quadrants[0]
    sd_content = update_status(sd_content, f"ready for {next_q} scan")
    print(f"Next: SD:S {next_q}")
else:
    # All quadrants complete
    sd_content = update_status(sd_content, "all quadrants complete")
    print("All quadrants verified! SD workflow complete.")
    
    # Archive final state
    archive_path = f"docs/SD/complete/{sd_version}-final.md"
    write_file(archive_path, sd_content)

write_file("SD.md", sd_content)
```

**Step 8: Output**

```
SD:V complete - Verification passed

╔═══════════════════════════════════════════════════════════════════╗
║                      VERIFICATION RESULTS                         ║
╠═══════════════════════════════════════════════════════════════════╣
║ Tests: 150 passed, 0 failed                                       ║
║ Types: clean (mypy)                                               ║
║ Lint: clean (ruff)                                                ║
║ Manual: all integrations verified                                 ║
╠═══════════════════════════════════════════════════════════════════╣
║ Findings resolved: {N}                                            ║
║ Archive: docs/SD/complete/{VERSION}-{QUADRANT}.md                 ║
╚═══════════════════════════════════════════════════════════════════╝

Quadrant {QUADRANT} complete!

{IF_MORE_QUADRANTS}
Remaining quadrants: {Q2, Q3, Q4}
Next: SD:S {NEXT_Q}
{ELSE}
All quadrants complete!
SD workflow finished.
{ENDIF}
```

---

## Finding Types Reference

| Type | Name | Meaning | Resolution Approach |
|------|------|---------|---------------------|
| U | UNUSED | Symbol has no references | Find integration point, add call |
| I | INTEGRATION | Connected internally but not to entry point | Trace path, add missing link |
| T | TYPE | Missing type annotations | Infer from usage, add annotation |
| P | PATTERN | Doesn't follow project patterns | Identify pattern, refactor |

---

## Severity Levels

| Level | Criteria | Priority |
|-------|----------|----------|
| HIGH | Core functionality, exported symbols, user-facing | Resolve first |
| MEDIUM | Internal integration, incomplete features | Resolve second |
| LOW | Style, annotations, minor patterns | Resolve last |

---

## Cross-Reference Flow

```
SD finding created
    ↓
[TODO.md], [ver:`X.X.X`, sect:`A)`] - Task generated
    ↓
Resolution work performed
    ↓
[CHANGELOG.md], [ver:`X.X.X`, sect:`A)`] - Completion recorded
    ↓
Verification complete
    ↓
[VALIDATION.md], [ver:`X.X.X`, sect:`A)`] - Verified
    ↓
Pass archived to docs/SD/complete/X.X.X-Q1.md
```

---
