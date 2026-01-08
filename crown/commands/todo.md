---
description: Execute crown TODO workflow - work on tasks, update cross-references, archive completed versions
argument-hint: "[task-letter]"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

Execute the crown TODO workflow for task tracking and completion.

## Execution

### 1. Read Current State

Parse TODO.md:
- Version from `## X.X.X`
- Tasks from `- [ ] [A]` or `- [x] [A]` patterns
- Sections from `### A)` headers
- Cross-references from blockquotes

### 2. Determine Action

**If task-letter provided:**
- Work on specific task
- Read section `### {letter})`
- Execute work described
- Mark complete `[x]`

**If no argument:**
- Find first pending task
- Work on it
- Or archive if all complete

### 3. Execute Task

For each task:
1. Read task section for details
2. Parse cross-references (where to update)
3. Perform the actual work
4. Update task section with completion details

### 4. Mark Complete

Change checklist:
```markdown
- [ ] [A] Task description
```
To:
```markdown
- [x] [A] Task description
```

### 5. Update Cross-References

**CHANGELOG.md** - Add completion entry:
```markdown
### {letter}) {Category} - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| {component} | ✅ | [VALIDATION.md], [ver:`X.X.X`, sect:`{letter})`] |
```

**VALIDATION.md** - Add verification (if applicable):
```markdown
### {letter}) {Component} - VERIFIED

> [!NOTE]
> {description}
> [TODO.md], [ver:`X.X.X`, sect:`{letter})`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`{letter})`]

**Verification:**
- {test_results}
```

### 6. Archive Version (When All Complete)

When all tasks are `[x]`:

1. **Verify completion:**
   - All checklist items checked
   - Cross-references in place

2. **Archive:**
   ```
   Copy TODO.md → docs/TODO/complete/{version}.md
   ```

3. **Increment version:**
   ```markdown
   ## {next_version}
   
   > [!TIP]
   > Previous version: [docs/TODO/complete/{version}.md]
   ```

### 7. Output

```
Task [{letter}] complete.

Updates:
├── TODO.md - Marked complete
├── CHANGELOG.md - Entry added
└── VALIDATION.md - Verification added

Cross-references:
├── [TODO.md], [ver:`X.X.X`, sect:`{letter})`]
├── [CHANGELOG.md], [ver:`X.X.X`, sect:`{letter})`]
└── [VALIDATION.md], [ver:`X.X.X`, sect:`{letter})`]

Remaining: {N} tasks
Next: /crown:todo {next_letter}
```

## Adding New Tasks

When adding tasks:
```markdown
- [ ] [A] Task description

---

### A) Task Title

> [!IMPORTANT]
> Detailed description of work required.
> [VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

Checklist letter MUST match section letter.
