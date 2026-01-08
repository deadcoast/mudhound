---
description: Continue crown workflow from current state - auto-detect active workflow and resume
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

Resume the crown workflow from the current state, automatically detecting what work is in progress.

## Execution

### 1. Read All LIVE Documents

Parse current state from:
- TODO.md (version, pending tasks, status)
- SD.md (version, phase, quadrant progress)
- CHANGELOG.md (latest version)
- VALIDATION.md (latest version)

### 2. Detect Active Workflow

**Priority Order:**

1. **SD Workflow Active**
   - SD.md status is NOT "ready" or "complete"
   - Resume at current phase
   
2. **TODO Workflow Active**
   - Pending tasks exist (unchecked `[ ]`)
   - Work on next task
   
3. **TODO Ready to Archive**
   - All tasks complete (`[x]`)
   - Archive version
   
4. **Nothing Active**
   - No pending work
   - Offer choices

### 3. Display Current State

```
crown continue

Current State:
├── TODO.md [ver:0.0.9]
│   ├── Pending: 22 tasks (A-V)
│   └── Status: active
│
└── SD.md [ver:0.0.1]
    └── Status: ready

Active Workflow: TODO
Resuming at: Task [A]
```

### 4. Resume Appropriate Workflow

**If SD Active:**
```
Resuming SD workflow...

Phase: SD:S Q2
Status: 4 files remaining

Continuing scan...
```

**If TODO Active:**
```
Resuming TODO workflow...

Version: 0.0.9
Next task: [A] Restructure plugin to Claude Code conventions

Working on task A...
```

**If TODO Ready to Archive:**
```
TODO version 0.0.9 complete!

All 22 tasks finished.
Archiving to docs/TODO/complete/0.0.9.md...

TODO.md incremented to 0.0.10
```

**If Nothing Active:**
```
No active workflow.

Options:
├── /crown:sd R    - Begin codebase review
├── /crown:todo    - Add new tasks
└── /crown:status  - View full status
```

### 5. Execute and Update

After resuming:
- Execute the workflow step
- Update all affected documents
- Create cross-references
- Report completion and next step

## State Detection Logic

| SD Status | TODO Status | Action |
|-----------|-------------|--------|
| ready | pending tasks | Resume TODO |
| scanning Q2 | any | Resume SD:S Q2 |
| flagging | any | Resume SD:F |
| resolving | any | Resume SD:X |
| verifying | any | Resume SD:V |
| complete | pending tasks | Resume TODO |
| complete | all complete | Archive TODO |
| ready | empty | Offer choices |
