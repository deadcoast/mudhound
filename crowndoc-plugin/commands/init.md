---
description: Initialize the crowndoc documentation ecosystem in a repository - creates all documents, templates, folder structure, and customizes quadrants based on project
argument-hint: "[project-name]"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

# /crowndoc:init

Initialize the crowndoc AI-optimized documentation ecosystem in the current repository.

---

## Purpose

This command transforms a repository into a crowndoc-enabled project by:
1. Creating all four core documents with proper PROTOCOL blocks
2. Establishing the archive folder structure
3. Generating templates for future versions
4. Creating specification documents
5. Customizing quadrants based on actual project structure

The initialization is idempotent - running it again will not destroy existing data but will create any missing components.

---

## Pre-Execution Checks

### Check 1: Existing crowndoc Documents

```python
# Check for existing documents
existing = []
for doc in ["TODO.md", "CHANGELOG.md", "VALIDATION.md", "SD.md"]:
    if file_exists(doc):
        existing.append(doc)

if existing:
    # Warn but don't abort - will merge/preserve
    warn(f"Existing documents found: {existing}")
    warn("Will preserve existing content and add missing structure")
```

### Check 2: Git Repository

```bash
# Verify git repo exists (recommended but not required)
git status
# If not a git repo, warn that git history features won't work
```

### Check 3: Project Type Detection

```python
# Detect project type for quadrant customization
project_indicators = {
    "python": ["pyproject.toml", "setup.py", "requirements.txt"],
    "node": ["package.json", "tsconfig.json"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
}

for lang, indicators in project_indicators.items():
    for indicator in indicators:
        if file_exists(indicator):
            project_type = lang
            break
```

---

## Execution Steps

### Step 1: Create Folder Structure

```bash
# Documentation folders
mkdir -p Docs                           # Specification documents
mkdir -p docs/TODO/complete             # Archived TODO versions
mkdir -p docs/TODO/pending              # Incomplete TODO versions
mkdir -p docs/SD/complete               # Completed SD passes
mkdir -p docs/SD/pending                # Incomplete SD passes
mkdir -p templates                      # Document templates
```

**Verification:**
```bash
# Confirm structure
ls -la Docs docs/TODO docs/SD templates
```

### Step 2: Scan Project Structure for Quadrants

```python
# Get all directories in project
all_dirs = list_dir(".", recursive=True)

# Categorize into initial quadrants
quadrants = {
    "Q1": {
        "directories": [],
        "description": "Core business logic and external interfaces",
        "patterns": ["core", "lib", "src/core", "adapters", "assets", "models"]
    },
    "Q2": {
        "directories": [],
        "description": "User-facing interfaces",
        "patterns": ["cli", "commands", "cmd", "bin", "scripts", "api"]
    },
    "Q3": {
        "directories": [],
        "description": "Visual and UI elements",
        "patterns": ["ui", "components", "views", "templates", "animation", "frontend"]
    },
    "Q4": {
        "directories": [],
        "description": "Support infrastructure",
        "patterns": ["tests", "test", "utils", "helpers", "logging", "config"]
    }
}

# Match directories to quadrants
for dir_path in all_dirs:
    dir_name = basename(dir_path).lower()
    for qname, qdata in quadrants.items():
        for pattern in qdata["patterns"]:
            if pattern in dir_name:
                qdata["directories"].append(dir_path)
                break

# Count files per quadrant
for qname, qdata in quadrants.items():
    qdata["file_count"] = count_files(qdata["directories"])
```

### Step 3: Create TODO.md

**If TODO.md exists:** Preserve content, ensure PROTOCOL block present
**If TODO.md doesn't exist:** Create from template

```markdown
# TODO.md

## 0.0.1

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

- {CURRENT_DATE}

> [!TIP]
> crowndoc initialized. Ready for task tracking.
> Use `crowndoc: status` to view current state.
> Use `crowndoc: SD` to begin codebase review.

---

```

### Step 4: Create CHANGELOG.md

**If exists:** Preserve, add 0.0.0 PROTOCOL if missing
**If doesn't exist:** Create with initial structure

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

- {CURRENT_DATE}

> [!IMPORTANT]
> crowndoc ecosystem initialized.
> [TODO.md], [ver:`0.0.1`] - Task tracking ready
> [VALIDATION.md], [ver:`0.0.1`] - Validation ready

### A) Initialization - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| TODO.md created | ✅ | - |
| CHANGELOG.md created | ✅ | - |
| VALIDATION.md created | ✅ | - |
| SD.md created | ✅ | - |
| Folder structure created | ✅ | - |
| Templates created | ✅ | - |
| Quadrants configured | ✅ | See [Docs/crowndoc.md] |

---

```

### Step 5: Create VALIDATION.md

```markdown
# Validation

## 0.0.1

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking validation findings and integration status'

---

- {CURRENT_DATE}

### A) crowndoc Initialization - VERIFIED

> [!NOTE]
> crowndoc ecosystem successfully initialized.
> [TODO.md], [ver:`0.0.1`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]

**Verification:**
- Folder structure: ✅ Created
- Core documents: ✅ All 4 present
- Templates: ✅ All 4 created
- Quadrants: ✅ Configured for project

---

```

### Step 6: Create SD.md

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

- {CURRENT_DATE}

### Quadrant Configuration

| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | {Q1_DIRS} | {Q1_COUNT} | PENDING |
| Q2 | {Q2_DIRS} | {Q2_COUNT} | PENDING |
| Q3 | {Q3_DIRS} | {Q3_COUNT} | PENDING |
| Q4 | {Q4_DIRS} | {Q4_COUNT} | PENDING |

> [!TIP]
> Use `SD:R` to begin reconnaissance.
> Use `SD:S Q1` to scan first quadrant.
> See [Docs/SD.md] for workflow specification.

---

```

### Step 7: Create Docs/crowndoc.md Specification

```markdown
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

**Quadrants (customized for this project):**
- Q1: {Q1_DIRS}
- Q2: {Q2_DIRS}
- Q3: {Q3_DIRS}
- Q4: {Q4_DIRS}

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
> `[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]`
> example: `[TODO.md], [ver:`0.0.2`, sect:`A)`]`

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

```

### Step 8: Create Docs/SD.md Workflow Specification

```markdown
# SeekAndDestroy Workflow Specification

## 0.0.0

### PROTOCOL

> [!NOTE]
> purpose: SD workflow detailed specification
> dependencies: SD.md (LIVE document)
> status: 'specification'

---

## Philosophy

### Integration Over Deletion

> [!CAUTION]
> The SD workflow is NOT about finding code to delete.
> It is about understanding the codebase and INTEGRATING unused elements.
>
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find the integration path.
> Deletion requires EXPLICIT user approval.

### Why This Matters

Unused code often represents:
- Incomplete features waiting for connection
- Infrastructure for future functionality
- Historical context that informs architecture
- Defensive code for edge cases

Deleting first destroys this value. Integration preserves it.

---

## Phases

### SD:R - RECON

**Purpose:** Map the codebase, establish scope

**Actions:**
1. Recursive directory scan
2. Categorize into quadrants
3. Count files per quadrant
4. Output scope summary
5. Recommend starting quadrant

**Output:** Updated SD.md with quadrant table

### SD:S - SCAN

**Purpose:** Deep analysis of one quadrant

**Actions:**
1. Get symbol overview for each file
2. Check reference status for each symbol
3. Check import usage
4. Trace integration paths
5. INVESTIGATE each finding (critical)
6. Document findings in SD.md
7. Generate TODO entries

**Critical Rule:** Never flag without investigation

### SD:F - FLAG

**Purpose:** Review and organize findings

**Actions:**
1. Aggregate all findings
2. Prioritize by severity/type
3. Verify TODO entries exist
4. Output resolution plan

### SD:X - RESOLVE

**Purpose:** Execute resolutions

**Actions by Type:**
- U (Unused): Find integration point, connect
- I (Integration): Trace path, add missing links
- T (Type): Add proper annotation
- P (Pattern): Refactor to standard

**Critical Rule:** Never delete as first solution

### SD:V - VERIFY

**Purpose:** Confirm all resolutions work

**Actions:**
1. Run test suite
2. Run type checker
3. Run linter
4. Manual verification
5. Update VALIDATION.md
6. Archive pass to docs/SD/complete/

---

## Finding Types

| Type | Name | Meaning | Resolution |
|------|------|---------|------------|
| U | UNUSED | No references found | Find integration point |
| I | INTEGRATION | Exists but disconnected | Add missing connections |
| T | TYPE | Missing/wrong annotation | Add proper types |
| P | PATTERN | Doesn't match standards | Refactor to pattern |

---

## Severity Levels

| Severity | Criteria | Priority |
|----------|----------|----------|
| HIGH | Core functionality affected, user-facing impact | Resolve first |
| MEDIUM | Incomplete feature, internal quality issue | Resolve second |
| LOW | Minor inconsistency, documentation issue | Resolve last |

---

## Cross-Reference Flow

```
SD finding → [TODO.md], [ver:`X.X.X`, sect:`Y)`]
    ↓
Resolution work performed
    ↓
[CHANGELOG.md], [ver:`X.X.X`, sect:`Z)`]
    ↓
Verification complete
    ↓
[VALIDATION.md], [ver:`X.X.X`, sect:`W)`]
    ↓
Pass archived to docs/SD/complete/
```

---

```

### Step 9: Create Templates

**templates/TODO.template.md:**
```markdown
# TODO.md

## {VERSION}

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

- {DATE}

{TASK_CHECKLIST}

---

{TASK_SECTIONS}

---

```

**templates/CHANGELOG.template.md:**
```markdown
# Changelog

## 0.0.0

### A) PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, VALIDATION.md
> status: 'tracking completed work and releases'

---

## {VERSION}

- {DATE}

> [!IMPORTANT]
> {SUMMARY}
> [TODO.md], [ver:`{VERSION}`] - Work items
> [VALIDATION.md], [ver:`{VERSION}`] - Validation

{SECTIONS}

---

```

**templates/VALIDATION.template.md:**
```markdown
# Validation

## {VERSION}

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking validation findings and integration status'

---

- {DATE}

{SECTIONS}

---

```

**templates/SD.template.md:**
```markdown
# SeekAndDestroy

## {VERSION}

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md
> status: '{STATUS}'
> principle: INTEGRATION OVER DELETION

---

- {DATE}

### Quadrant Configuration

| Quadrant | Directories | Files | Status |
|----------|-------------|-------|--------|
| Q1 | {Q1} | {Q1_COUNT} | {Q1_STATUS} |
| Q2 | {Q2} | {Q2_COUNT} | {Q2_STATUS} |
| Q3 | {Q3} | {Q3_COUNT} | {Q3_STATUS} |
| Q4 | {Q4} | {Q4_COUNT} | {Q4_STATUS} |

{FINDINGS}

---

```

### Step 10: Output Initialization Summary

```
crowndoc initialized successfully!

Project: {PROJECT_NAME}
Date: {CURRENT_DATE}

Documents Created:
├── TODO.md (ver: 0.0.1) - Ready for task tracking
├── CHANGELOG.md (ver: 0.0.1) - Recording initialization
├── VALIDATION.md (ver: 0.0.1) - Verification ready
└── SD.md (ver: 0.0.1) - Ready for codebase review

Specifications:
├── Docs/crowndoc.md - Ecosystem specification
└── Docs/SD.md - SD workflow specification

Folder Structure:
├── docs/TODO/complete/ - For archived TODO versions
├── docs/TODO/pending/ - For incomplete versions
├── docs/SD/complete/ - For completed SD passes
├── docs/SD/pending/ - For incomplete passes
└── templates/ - Document templates

Quadrant Configuration:
├── Q1: {Q1_DIRS} ({Q1_COUNT} files)
├── Q2: {Q2_DIRS} ({Q2_COUNT} files)
├── Q3: {Q3_DIRS} ({Q3_COUNT} files)
└── Q4: {Q4_DIRS} ({Q4_COUNT} files)

Next Steps:
├── [crowndoc: status] - View current state
├── [crowndoc: TODO] - Begin task workflow
└── [crowndoc: SD] or [SD:R] - Begin codebase review

Cross-references use format:
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

---

## Error Handling

### Existing Files

If documents exist:
- Preserve existing content
- Add PROTOCOL block if missing
- Add version structure if missing
- Do not overwrite user content

### Permission Errors

```
Error: Cannot create folder structure
Check: Write permissions on project directory
Action: Request appropriate permissions or run in writable location
```

### Project Type Unknown

If project type cannot be detected:
- Use default quadrant patterns
- Note in output that quadrants may need customization
- Point to Docs/crowndoc.md for customization

---

## Post-Initialization

After initialization, the user can:
1. Customize quadrants in Docs/crowndoc.md
2. Begin task tracking with `crowndoc: TODO`
3. Start codebase review with `crowndoc: SD`
4. Check status with `crowndoc: status`

---
