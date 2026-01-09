---
description: Display crown ecosystem state - versions, pending tasks, active workflows, suggested actions
allowed-tools: Read, Glob
---

Display the complete current state of the crown documentation ecosystem.

## Execution

### 1. Read Core Documents

Read and parse each document:

**TODO.md:**
- Extract version from `## X.X.X`
- Count pending tasks (unchecked `[ ]`)
- Count completed tasks (checked `[x]`)
- Extract status from PROTOCOL block

**CHANGELOG.md:**
- Extract latest version
- Get recent entry summary

**VALIDATION.md:**
- Extract latest version
- Count verified items

**SD.md:**
- Extract version and status
- Parse quadrant table (Q1-Q4 status)
- Count findings by status

### 2. Count Archives

```
docs/TODO/complete/*.md  → completed TODO versions
docs/TODO/pending/*.md   → pending TODO versions
docs/SD/complete/*.md    → completed SD passes
docs/SD/pending/*.md     → pending SD passes
```

### 3. Detect Active Workflow

Priority order:
1. **SD active** (status not "ready"/"complete") → Resume SD phase
2. **TODO pending** (unchecked tasks exist) → Work next task
3. **TODO complete** (all checked) → Archive version
4. **Nothing active** → Offer choices

### 4. Output Format

```
crown status

TODO.md [ver:X.X.X]
├── Status: {status}
├── Pending: {N} tasks ({letters})
├── Completed: {N} tasks ({letters})
└── Next: {next_task}

CHANGELOG.md [ver:X.X.X]
└── Latest: {summary}

VALIDATION.md [ver:X.X.X]
└── Verified: {N} items

SD.md [ver:X.X.X]
├── Status: {status}
├── Q1: {status} ({files} files)
├── Q2: {status} ({files} files)
├── Q3: {status} ({files} files)
└── Q4: {status} ({files} files)

Archive:
├── TODO versions: {N}
└── SD passes: {N}

Active: {workflow_type}
Next: {suggested_action}
```

### 5. Suggest Next Actions

Based on state:
- SD active → `/crown:sd {phase}`
- TODO pending → `/crown:todo {letter}`
- TODO complete → `/crown:todo` (will archive)
- Nothing → `/crown:sd R` or add tasks
