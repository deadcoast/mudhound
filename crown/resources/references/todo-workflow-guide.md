# TODO Workflow Guide

## Overview

The TODO workflow manages the complete lifecycle of task tracking:
1. Adding new tasks
2. Executing work
3. Marking completion
4. Updating cross-references
5. Archiving completed versions

---

## Commands

| Command | Purpose |
| --------- | --------- |
| `/crown:todo` | Work on next pending task |
| `/crown:todo A` | Work on specific task A |
| `/crown:continue` | Resume TODO if active |

---

## Task Structure

### Checklist Item

```markdown
- [ ] [A] Task description
```

Components:
- `- [ ]` or `- [x]` - Checkbox (pending/complete)
- `[A]` - Letter identifier (A-Z)
- Description - Brief task summary

### Task Section

```markdown
### A) Task Title

> [!IMPORTANT]
> Detailed description of what needs to be done.
> Why this task exists and what it accomplishes.
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

Components:
- `### A)` - Section header matching checklist letter
- Blockquote with description and cross-references
- Additional details, scope, context as needed

---

## Workflow Execution

### Step 1: Read Current State

```
/crown:todo
```

Parses TODO.md:
- Extracts current version
- Identifies pending tasks (`[ ]`)
- Identifies completed tasks (`[x]`)
- Finds next task to work on

### Step 2: Execute Task

For the pending task:
1. Read task section for full details
2. Parse cross-references (where to update)
3. Perform the actual work described
4. Document completion in task section

### Step 3: Mark Complete

Change checklist:
```markdown
- [ ] [A] Task description
```
To:
```markdown
- [x] [A] Task description
```

### Step 4: Update Cross-References

**Add to CHANGELOG.md:**
```markdown
### A) Category - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| Component | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
```

**Add to VALIDATION.md (if verification performed):**
```markdown
### A) Component - VERIFIED

> [!NOTE]
> What was verified and how.
> [TODO.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]

**Verification:**
- Tests: passed
- Linting: clean
```

### Step 5: Report Progress

```
Task [A] complete.

Updates:
├── TODO.md - Marked complete
├── CHANGELOG.md - Entry added
└── VALIDATION.md - Verification added

Remaining: 5 tasks (B, C, D, E, F)
Next: /crown:todo B
```

---

## Adding New Tasks

### Determine Next Letter

Find highest letter in current version:
```markdown
- [x] [A] Completed task
- [ ] [B] Pending task
# Next letter: C
```

### Add Checklist Item

```markdown
- [x] [A] Completed task
- [ ] [B] Pending task
- [ ] [C] New task description
```

### Add Task Section

After existing sections:
```markdown
### C) New Task Title

> [!IMPORTANT]
> Detailed description of the new task.
> What needs to be done and why.
> [VALIDATION.md], [ver:`0.0.1`, sect:`C)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`C)`]
```

---

## Version Archiving

### Trigger

When all tasks in a version are complete (`[x]`).

### Process

1. **Verify completion:**
   - All checklist items marked `[x]`
   - All cross-references in place
   - CHANGELOG entries exist
   - VALIDATION entries exist (where applicable)

2. **Archive current version:**
   ```
   Copy TODO.md → docs/TODO/complete/X.X.X.md
   ```

3. **Increment root TODO.md:**
   ```markdown
   ## X.X.Y
   
   ### PROTOCOL
   
   > [!NOTE]
   > versioning: canonical
   > dependencies: VALIDATION.md, CHANGELOG.md
   > status: 'ready for new work'
   
   ---
   
   - YYYY-MM-DD
   
   > [!TIP]
   > Previous version: [docs/TODO/complete/X.X.X.md]
   > Completed versions: [docs/TODO/complete/]
   
   ---
   ```

4. **Verify archive:**
   - Archive file exists
   - Root TODO.md has new version
   - Previous content preserved in archive

---

## Cross-Reference Flow

```
Task created in TODO.md
├── Points to: [VALIDATION.md], [ver:X.X.X, sect:A)]
└── Points to: [CHANGELOG.md], [ver:X.X.X, sect:A)]

    ↓ (work completed)

CHANGELOG.md entry added
└── Points to: [VALIDATION.md], [ver:X.X.X, sect:A)]

    ↓ (verification done)

VALIDATION.md entry added
├── Points back: [TODO.md], [ver:X.X.X, sect:A)]
└── Points back: [CHANGELOG.md], [ver:X.X.X, sect:A)]
```

---

## Best Practices

### DO
- One task per letter
- Specific, actionable descriptions
- Create cross-references immediately
- Archive promptly when complete
- Keep task scope focused

### DON'T
- Multiple unrelated items in one task
- Vague descriptions
- Skip cross-reference creation
- Leave completed versions unarchived
- Mix different types of work in one task

---

## Task Naming Patterns

### Good Task Names
- "Implement search command"
- "Fix cache integration"
- "Add type annotations to engine"
- "Validate cross-references"

### Bad Task Names
- "Stuff"
- "Various fixes"
- "Update things"
- "Work on code"

---

## Handling Large Tasks

For complex work, break into subtasks:

```markdown
### A) Implement Search Feature

> [!IMPORTANT]
> Complete search implementation.
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]

**Subtasks:**
1. [ ] Define SearchQuery model
2. [ ] Implement search engine
3. [ ] Add CLI command
4. [ ] Write tests
5. [ ] Document usage
```

Or split into separate tasks:
```markdown
- [ ] [A] Define SearchQuery model
- [ ] [B] Implement search engine
- [ ] [C] Add search CLI command
- [ ] [D] Write search tests
- [ ] [E] Document search feature
```

---

## Error Recovery

### Incomplete Task

If task cannot be completed:
1. Document blocker in task section
2. Leave task unchecked
3. Create new task for blocker resolution
4. Resume when unblocked

### Conflicting Changes

If external changes conflict:
1. Archive current state to docs/TODO/pending/
2. Resolve conflicts manually
3. Resume workflow
4. Update cross-references

---
