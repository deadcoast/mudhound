---
description: Display comprehensive crowndoc ecosystem state - versions, pending tasks, active workflows, archive counts, and suggested next actions
allowed-tools: ["Read", "Glob"]
---

# /crowndoc:status

Display the complete current state of the crowndoc documentation ecosystem.

---

## Purpose

This command provides a comprehensive view of:
1. All four core documents and their versions
2. Pending vs completed tasks in TODO.md
3. Active SD workflow phase and quadrant progress
4. Archive statistics (completed versions and passes)
5. Cross-reference health
6. Suggested next actions based on current state

This is a read-only command - it does not modify any documents.

---

## Execution Steps

### Step 1: Read TODO.md

```python
# Read and parse TODO.md
todo_content = read_file("TODO.md")

# Extract version
todo_version = extract_version(todo_content)  # e.g., "0.0.8"

# Parse tasks
tasks = parse_tasks(todo_content)
pending_tasks = [t for t in tasks if not t.checked]
completed_tasks = [t for t in tasks if t.checked]

# Extract status from PROTOCOL block
todo_status = extract_protocol_status(todo_content)

# Build TODO state
todo_state = {
    "version": todo_version,
    "pending_count": len(pending_tasks),
    "pending_tasks": [t.letter for t in pending_tasks],
    "completed_count": len(completed_tasks),
    "completed_tasks": [t.letter for t in completed_tasks],
    "status": todo_status,
    "next_task": pending_tasks[0] if pending_tasks else None
}
```

### Step 2: Read CHANGELOG.md

```python
# Read and parse CHANGELOG.md
changelog_content = read_file("CHANGELOG.md")

# Extract latest version
latest_version = extract_latest_version(changelog_content)

# Extract recent entries (last version)
recent_entries = extract_version_entries(changelog_content, latest_version)

# Get section count
section_count = count_sections(recent_entries)

# Build CHANGELOG state
changelog_state = {
    "latest_version": latest_version,
    "section_count": section_count,
    "recent_summary": extract_summary(recent_entries)
}
```

### Step 3: Read VALIDATION.md

```python
# Read and parse VALIDATION.md
validation_content = read_file("VALIDATION.md")

# Extract current version
validation_version = extract_latest_version(validation_content)

# Extract recent validations
recent_validations = extract_version_entries(validation_content, validation_version)

# Count verified items
verified_count = count_verified_items(recent_validations)

# Build VALIDATION state
validation_state = {
    "version": validation_version,
    "verified_count": verified_count,
    "recent_summary": extract_summary(recent_validations)
}
```

### Step 4: Read SD.md

```python
# Read and parse SD.md
sd_content = read_file("SD.md")

# Extract version
sd_version = extract_version(sd_content)

# Extract status from PROTOCOL
sd_status = extract_protocol_status(sd_content)

# Parse quadrant table
quadrants = parse_quadrant_table(sd_content)

# Determine active phase
active_phase = determine_active_phase(sd_content, quadrants)

# Count findings
findings = parse_findings(sd_content)
findings_by_status = group_by_status(findings)

# Build SD state
sd_state = {
    "version": sd_version,
    "status": sd_status,
    "active_phase": active_phase,
    "quadrants": quadrants,
    "findings": {
        "total": len(findings),
        "new": len(findings_by_status.get("NEW", [])),
        "resolved": len(findings_by_status.get("RESOLVED", []))
    }
}
```

### Step 5: Count Archive Documents

```python
# Count archived TODO versions
todo_complete = count_files("docs/TODO/complete/*.md")
todo_pending = count_files("docs/TODO/pending/*.md")

# Count archived SD passes
sd_complete = count_files("docs/SD/complete/*.md")
sd_pending = count_files("docs/SD/pending/*.md")

# Build archive state
archive_state = {
    "todo_complete": todo_complete,
    "todo_pending": todo_pending,
    "sd_complete": sd_complete,
    "sd_pending": sd_pending
}
```

### Step 6: Check Cross-Reference Health

```python
# Quick cross-reference scan (not full validation)
issues = []

# Check TODO references
for ref in find_references("TODO.md"):
    if not reference_resolves(ref):
        issues.append(f"TODO.md: broken reference {ref}")

# Check CHANGELOG references
for ref in find_references("CHANGELOG.md"):
    if not reference_resolves(ref):
        issues.append(f"CHANGELOG.md: broken reference {ref}")

# Limit to first 5 issues for status display
xref_health = {
    "issues_found": len(issues),
    "sample_issues": issues[:5],
    "status": "healthy" if len(issues) == 0 else "needs attention"
}
```

### Step 7: Determine Active Workflow

```python
# Determine what workflow is currently active
def get_active_workflow():
    # Check SD first (higher priority)
    if sd_state["status"] not in ["ready", "complete", "READY", "COMPLETE"]:
        return {
            "type": "SD",
            "phase": sd_state["active_phase"],
            "description": f"SD workflow active at phase {sd_state['active_phase']}"
        }
    
    # Check TODO
    if todo_state["pending_count"] > 0:
        return {
            "type": "TODO",
            "task": todo_state["next_task"],
            "description": f"TODO workflow active, {todo_state['pending_count']} tasks pending"
        }
    
    # Nothing active
    return {
        "type": None,
        "description": "No active workflow - ready for new work"
    }

active_workflow = get_active_workflow()
```

### Step 8: Generate Suggested Actions

```python
def get_suggested_actions():
    actions = []
    
    # Based on active workflow
    if active_workflow["type"] == "SD":
        phase = sd_state["active_phase"]
        if phase == "R":
            actions.append(("[SD:S Q1]", "Begin scanning first quadrant"))
        elif phase.startswith("S"):
            quadrant = phase.split(" ")[1] if " " in phase else "Q1"
            actions.append(("[SD:F]", "Review and organize findings"))
        elif phase == "F":
            actions.append(("[SD:X]", "Resolve flagged findings"))
        elif phase == "X":
            actions.append(("[SD:V]", "Verify resolutions"))
        elif phase == "V":
            next_q = get_next_quadrant(quadrants)
            if next_q:
                actions.append((f"[SD:S {next_q}]", f"Scan next quadrant ({next_q})"))
            else:
                actions.append(("[crowndoc: TODO]", "SD complete - check TODO tasks"))
    
    elif active_workflow["type"] == "TODO":
        task = todo_state["next_task"]
        actions.append(("[crowndoc: TODO]", f"Continue with task {task.letter}: {task.title}"))
    
    else:
        # No active workflow
        if sd_state["status"] == "ready":
            actions.append(("[crowndoc: SD]", "Begin codebase review"))
        actions.append(("[crowndoc: TODO]", "Add new tasks"))
    
    # Always useful
    actions.append(("[crowndoc: validate]", "Validate cross-references"))
    
    return actions

suggested_actions = get_suggested_actions()
```

---

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║                      crowndoc status                             ║
╚══════════════════════════════════════════════════════════════════╝

TODO.md [ver:X.X.X]
├── Status: {STATUS_DESCRIPTION}
├── Pending: {N} tasks ({LETTERS})
├── Completed: {N} tasks ({LETTERS})
└── Next: {NEXT_TASK_LETTER} - {NEXT_TASK_TITLE}

CHANGELOG.md [ver:X.X.X]
├── Sections: {N}
└── Latest: {RECENT_SUMMARY}

VALIDATION.md [ver:X.X.X]
├── Verified: {N} items
└── Latest: {RECENT_SUMMARY}

SD.md [ver:X.X.X]
├── Status: {SD_STATUS}
├── Phase: {ACTIVE_PHASE}
├── Quadrants:
│   ├── Q1: {STATUS} ({FILE_COUNT} files)
│   ├── Q2: {STATUS} ({FILE_COUNT} files)
│   ├── Q3: {STATUS} ({FILE_COUNT} files)
│   └── Q4: {STATUS} ({FILE_COUNT} files)
└── Findings: {TOTAL} ({NEW} new, {RESOLVED} resolved)

Archive:
├── TODO versions: {N} completed, {N} pending
└── SD passes: {N} completed, {N} pending

Cross-references: {HEALTHY|NEEDS_ATTENTION}
{IF ISSUES: └── {N} issues found (use [crowndoc: validate] for details)}

Active Workflow: {WORKFLOW_DESCRIPTION}

Suggested Actions:
├── {ACTION_1} - {DESCRIPTION_1}
├── {ACTION_2} - {DESCRIPTION_2}
└── {ACTION_3} - {DESCRIPTION_3}
```

---

## State Detection Logic

### TODO State Patterns

| State | Indicators | Next Action |
|-------|------------|-------------|
| Empty | No tasks, status "ready" | Add new tasks |
| Active | Unchecked tasks exist | Work on next task |
| Completing | All tasks checked | Archive version |
| Error | Missing PROTOCOL | Reinitialize |

### SD State Patterns

| State | Indicators | Next Action |
|-------|------------|-------------|
| Ready | Status "ready", no active phase | Begin with SD:R |
| Recon | Phase R complete, quadrants mapped | SD:S Q1 |
| Scanning | Phase S for quadrant Qn | Continue scanning or SD:F |
| Flagging | Findings documented | SD:X |
| Resolving | Working through findings | Complete and SD:V |
| Verifying | Running verification | Archive pass |
| Complete | All quadrants done | Start new cycle |

### Workflow Priority

When determining active workflow:
1. SD workflow takes priority (if not READY/COMPLETE)
2. TODO workflow is secondary (if pending tasks)
3. Neither active = ready for new work

---

## Missing Document Handling

If a core document is missing:

```
⚠️ Missing Documents:
├── TODO.md - NOT FOUND
└── SD.md - NOT FOUND

Action required: Run [crowndoc: init] to create missing documents
```

If optional folders are missing:

```
ℹ️ Archive folders not found (will be created on first archive):
├── docs/TODO/complete/
└── docs/SD/complete/
```

---

## Verbose Mode

With verbose flag, include additional details:

```
TODO.md [ver:X.X.X] (VERBOSE)
├── File: TODO.md
├── Size: {N} bytes
├── Last modified: {TIMESTAMP}
├── PROTOCOL:
│   ├── versioning: canonical
│   ├── dependencies: VALIDATION.md, CHANGELOG.md
│   └── status: {STATUS}
├── Tasks:
│   ├── [A] {TITLE} - {CHECKED/UNCHECKED}
│   ├── [B] {TITLE} - {CHECKED/UNCHECKED}
│   └── [C] {TITLE} - {CHECKED/UNCHECKED}
└── Cross-references: {N} outgoing, {N} incoming
```

---

## Error Conditions

### Document Parse Error

```
Error: Cannot parse TODO.md
├── Expected version header (## X.X.X) not found
└── Action: Check document structure, may need manual repair
```

### Cross-Reference Issues

```
Cross-references: NEEDS ATTENTION
├── 3 broken references found
├── Sample:
│   ├── [TODO.md], [ver:0.0.5, sect:Z)] - Section not found
│   └── [CHANGELOG.md], [ver:0.0.9] - Version not found
└── Run [crowndoc: validate] for complete report
```

---

## Integration with Other Commands

Status informs users about next steps:
- Suggests `crowndoc: TODO` when tasks pending
- Suggests `crowndoc: SD` when review ready
- Suggests `crowndoc: validate` when issues detected
- Suggests `crowndoc: init` when documents missing

---
