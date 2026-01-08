---
description: Execute the TODO workflow - read current tasks, work on pending items, create cross-references, complete and archive versions
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

# /crowndoc:TODO

Execute the crowndoc TODO workflow for task tracking, completion, and version management.

---

## Purpose

The TODO workflow manages the complete lifecycle of task tracking:
1. Reading and parsing current TODO state
2. Working on pending tasks
3. Marking tasks complete with cross-references
4. Completing and archiving versions
5. Incrementing to next version

This is the primary workflow for tracking work items and ensuring every change is documented with proper cross-references.

---

## Workflow Entry Points

### Entry Point 1: Active Tasks Exist

When TODO.md has unchecked tasks (`[ ]`):
- Read task details
- Execute work for task
- Mark complete with cross-references
- Update CHANGELOG.md and VALIDATION.md

### Entry Point 2: All Tasks Complete

When all tasks are checked (`[x]`):
- Verify cross-references are in place
- Archive version to docs/TODO/complete/
- Increment root TODO.md to next version
- Reset for new work

### Entry Point 3: No Tasks (Empty Version)

When TODO.md has no tasks:
- Ready to add new work items
- User specifies new tasks
- Create checklist and sections

---

## Execution Steps

### Phase 1: Read Current State

```python
# Read TODO.md from project root
todo_content = read_file("TODO.md")

# Extract current version
version = extract_version_header(todo_content)
# Pattern: ## X.X.X

# Extract PROTOCOL block
protocol = extract_protocol_block(todo_content)
# Extract: versioning, dependencies, status

# Parse task checklist
tasks = []
for line in todo_content.split("\n"):
    if match := re.match(r"- \[([ x])\] \[([A-Z])\] (.+)", line):
        tasks.append({
            "checked": match.group(1) == "x",
            "letter": match.group(2),
            "title": match.group(3)
        })

# Parse task sections
sections = {}
for match in re.finditer(r"### ([A-Z])\) (.+?)(?=### [A-Z]\)|---|\Z)", todo_content, re.DOTALL):
    letter = match.group(1)
    content = match.group(2)
    sections[letter] = {
        "title": content.split("\n")[0].strip(),
        "body": content,
        "cross_refs": extract_cross_references(content)
    }

# Calculate state
pending_tasks = [t for t in tasks if not t["checked"]]
completed_tasks = [t for t in tasks if t["checked"]]
```

**Output State Report:**
```
TODO.md [ver:{VERSION}]

Status: {PROTOCOL_STATUS}

Tasks:
├── Pending: {N}
│   {FOR EACH PENDING TASK}
│   └── [{LETTER}] {TITLE}
└── Completed: {N}
    {FOR EACH COMPLETED TASK}
    └── [{LETTER}] {TITLE} ✅
```

### Phase 2: Handle Based on State

#### Case A: Pending Tasks Exist

```
Pending tasks found.

Next task: [{LETTER}] {TITLE}

Reading task details...
```

**Step 2A.1: Read Task Section**

```python
task = pending_tasks[0]  # First pending task
section = sections[task["letter"]]

# Extract cross-references
xrefs = section["cross_refs"]
# e.g., [VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
#       [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

**Step 2A.2: Display Task Details**

```
Task: [{LETTER}] {TITLE}

Description:
{SECTION_BODY}

Cross-references:
├── {XREF_1}
└── {XREF_2}

Proceeding with task execution...
```

**Step 2A.3: Execute Task Work**

This is where actual work happens:
- Code changes
- Documentation updates
- Configuration modifications
- Test additions

The work depends on what the task describes.

**Step 2A.4: Record Completion**

```python
# Update TODO.md - mark task complete
new_content = todo_content.replace(
    f"- [ ] [{task['letter']}]",
    f"- [x] [{task['letter']}]"
)

# Add completion details to section
section_pattern = f"### {task['letter']}) "
completion_text = """

**Completed:**
- {COMPLETION_DETAIL_1}
- {COMPLETION_DETAIL_2}
- Verified: {VERIFICATION_STATUS}
"""
# Insert completion text after blockquote

write_file("TODO.md", new_content)
```

**Step 2A.5: Update CHANGELOG.md**

```python
# Read current CHANGELOG
changelog = read_file("CHANGELOG.md")

# Find or create version entry
version_entry = find_version_entry(changelog, version)
if not version_entry:
    # Create new version entry
    new_entry = f"""
## {version}

- {TODAY_DATE}

> [!IMPORTANT]
> {VERSION_SUMMARY}
> [TODO.md], [ver:`{version}`] - Work items
> [VALIDATION.md], [ver:`{version}`] - Validation

### {task['letter']}) {CATEGORY_NAME} - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| {COMPONENT_NAME} | ✅ | [VALIDATION.md], [ver:`{version}`, sect:`{task['letter']}`)] |

---
"""
    # Insert after previous version
    changelog = insert_version_entry(changelog, new_entry)
else:
    # Add section to existing version
    section_entry = f"""
### {task['letter']}) {CATEGORY_NAME} - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| {COMPONENT_NAME} | ✅ | [VALIDATION.md], [ver:`{version}`, sect:`{task['letter']}`)] |
"""
    changelog = add_section_to_version(changelog, version, section_entry)

write_file("CHANGELOG.md", changelog)
```

**Step 2A.6: Update VALIDATION.md (if verification performed)**

```python
# If task required verification
if task_requires_verification:
    validation = read_file("VALIDATION.md")
    
    # Find or create version entry
    version_entry = find_version_entry(validation, version)
    if not version_entry:
        new_entry = f"""
## {version}

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking validation findings'

---

- {TODAY_DATE}

### {task['letter']}) {COMPONENT_NAME} - VERIFIED

> [!NOTE]
> {VERIFICATION_DESCRIPTION}
> [TODO.md], [ver:`{version}`, sect:`{task['letter']}`)]
> [CHANGELOG.md], [ver:`{version}`, sect:`{task['letter']}`)]

**Verification:**
- {TEST_RESULT}
- {LINT_RESULT}
- {TYPE_RESULT}

---
"""
        validation = insert_version_entry(validation, new_entry)
    
    write_file("VALIDATION.md", validation)
```

**Step 2A.7: Report Completion**

```
Task [{LETTER}] complete.

Updates:
├── TODO.md - Task marked complete
├── CHANGELOG.md - Completion recorded
└── VALIDATION.md - Verification recorded

Cross-references created:
├── [TODO.md], [ver:`{VERSION}`, sect:`{LETTER})`]
├── [CHANGELOG.md], [ver:`{VERSION}`, sect:`{LETTER})`]
└── [VALIDATION.md], [ver:`{VERSION}`, sect:`{LETTER})`]

Remaining tasks: {N}
{IF REMAINING}
Next: [{NEXT_LETTER}] {NEXT_TITLE}
{ELSE}
All tasks complete! Ready to archive version.
```

#### Case B: All Tasks Complete

When all checklist items are `[x]`:

```
All tasks in version {VERSION} complete.

Archiving version...
```

**Step 2B.1: Verify All Complete**

```python
# Double-check all tasks are checked
all_complete = all(t["checked"] for t in tasks)
if not all_complete:
    raise "Not all tasks complete - cannot archive"

# Verify cross-references exist
for task in tasks:
    xrefs = sections[task["letter"]]["cross_refs"]
    if not xrefs:
        warn(f"Task {task['letter']} has no cross-references")
```

**Step 2B.2: Finalize CHANGELOG Entry**

```python
# Ensure version entry is complete
changelog = read_file("CHANGELOG.md")
version_entry = extract_version_entry(changelog, version)

# Verify all task sections present
for task in tasks:
    if task["letter"] not in version_entry:
        warn(f"CHANGELOG missing section for task {task['letter']}")
```

**Step 2B.3: Finalize VALIDATION Entry**

```python
# Ensure validation entry is complete
validation = read_file("VALIDATION.md")
version_entry = extract_version_entry(validation, version)

# Note: Not all tasks require validation entries
```

**Step 2B.4: Archive TODO Version**

```python
# Copy current TODO.md to archive
archive_path = f"docs/TODO/complete/{version}.md"
copy_file("TODO.md", archive_path)

# Verify archive created
if not file_exists(archive_path):
    raise f"Failed to create archive at {archive_path}"
```

**Step 2B.5: Increment Root TODO.md**

```python
# Parse version and increment
major, minor, patch = version.split(".")
new_version = f"{major}.{minor}.{int(patch) + 1}"

# Create new TODO.md content
new_todo = f"""# TODO.md

## {new_version}

### PROTOCOL

> [!NOTE]
> versioning: canonical
> dependencies: VALIDATION.md, CHANGELOG.md
> status: 'tracking TODO items and outstanding work'

---

- {TODAY_DATE}

> [!TIP]
> All previous tasks complete. Ready for new work items.
> Previous version: [docs/TODO/complete/{version}.md]
> Completed versions: [docs/TODO/complete/](docs/TODO/complete/)

---

"""

write_file("TODO.md", new_todo)
```

**Step 2B.6: Report Archive Complete**

```
Version {VERSION} archived successfully.

Archive:
└── docs/TODO/complete/{VERSION}.md

Root TODO.md incremented to version {NEW_VERSION}

Cross-reference summary:
├── {CHANGELOG_REFS} entries in CHANGELOG.md
└── {VALIDATION_REFS} entries in VALIDATION.md

Ready for new work items.

Use [crowndoc: status] to view current state.
```

#### Case C: No Tasks (Empty Version)

When TODO.md has no pending or completed tasks:

```
TODO.md [ver:{VERSION}] is empty.

No tasks currently defined. Ready for new work items.

To add tasks:
1. Describe the work to be done
2. I will create checklist items and sections
3. Cross-references will be established automatically
```

**Adding New Tasks:**

```python
# User provides task descriptions
new_tasks = get_user_tasks()  # e.g., ["Implement feature X", "Fix bug Y"]

# Determine starting letter
existing_letters = [t["letter"] for t in tasks]
next_letter = get_next_letter(existing_letters)  # e.g., "A"

# Create checklist
checklist = ""
for i, task_desc in enumerate(new_tasks):
    letter = chr(ord(next_letter) + i)
    checklist += f"- [ ] [{letter}] {task_desc}\n"

# Create sections
sections_content = ""
for i, task_desc in enumerate(new_tasks):
    letter = chr(ord(next_letter) + i)
    sections_content += f"""
### {letter}) {task_desc}

> [!IMPORTANT]
> {DETAILED_DESCRIPTION}
> [VALIDATION.md], [ver:`{version}`, sect:`{letter})`]
> [CHANGELOG.md], [ver:`{version}`, sect:`{letter})`]

"""

# Update TODO.md
todo_content = insert_tasks(todo_content, checklist, sections_content)
write_file("TODO.md", todo_content)
```

---

## Cross-Reference Management

### Creating References

Every task completion creates these cross-references:

**In TODO.md section:**
```markdown
> [!IMPORTANT]
> Description of task
> [VALIDATION.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

**In CHANGELOG.md:**
```markdown
| Component | Status | Reference |
| --------- | ------ | --------- |
| Component | ✅ | [VALIDATION.md], [ver:`X.X.X`, sect:`A)`] |
```

**In VALIDATION.md:**
```markdown
> [!NOTE]
> Verification description
> [TODO.md], [ver:`X.X.X`, sect:`A)`]
> [CHANGELOG.md], [ver:`X.X.X`, sect:`A)`]
```

### Reference Validation

Before archiving, validate all references resolve:

```python
all_refs = []
all_refs.extend(extract_references("TODO.md"))
all_refs.extend(extract_references("CHANGELOG.md"))
all_refs.extend(extract_references("VALIDATION.md"))

broken = []
for ref in all_refs:
    if not reference_resolves(ref):
        broken.append(ref)

if broken:
    warn(f"Broken references found: {broken}")
    # Prompt for fix or continue
```

---

## Version Number Management

### Version Format

Versions use semantic-style numbering: `MAJOR.MINOR.PATCH`

- **PATCH**: Incremented for each completed TODO version
- **MINOR**: Incremented for significant feature sets
- **MAJOR**: Incremented for breaking changes or major milestones

### Automatic Increment

By default, completing a version increments PATCH:
- `0.0.1` → `0.0.2`
- `0.0.9` → `0.0.10`

### Manual Override

User can specify version on new tasks:
```
Starting new TODO version: 0.1.0 (minor increment for feature release)
```

---

## Error Handling

### Missing TODO.md

```
Error: TODO.md not found

Action: Run [crowndoc: init] to initialize crowndoc ecosystem
```

### Malformed TODO.md

```
Error: Cannot parse TODO.md

Issues:
├── Missing version header (## X.X.X)
└── Missing PROTOCOL block

Action: Check document structure, may need manual repair
```

### Cross-Reference Conflicts

```
Warning: Cross-reference conflict detected

Reference: [CHANGELOG.md], [ver:`0.0.5`, sect:`A)`]
Issue: Section A) already exists in CHANGELOG 0.0.5

Options:
1. Append to existing section
2. Create new section letter
3. Skip cross-reference

Select: _
```

### Archive Failure

```
Error: Cannot archive version

Issue: docs/TODO/complete/ directory does not exist

Action: Creating directory...
mkdir -p docs/TODO/complete/

Retry: Copying TODO.md to archive...
```

---

## Integration with Other Workflows

### From SD Workflow

When SD:F generates findings:
```
SD finding generated TODO entry:

- [ ] [A] Integrate cache infrastructure

Cross-reference:
[SD.md], [ver:`0.0.1`, sect:`Q1 Finding 1`]
```

The TODO workflow then handles execution and completion.

### To CHANGELOG/VALIDATION

Every task completion flows to:
- CHANGELOG.md for completion record
- VALIDATION.md for verification record

This maintains the crowndoc traceability chain.

---

## Best Practices

### DO

- Mark tasks complete as soon as work is done
- Create cross-references immediately
- Archive promptly when version complete
- Keep task descriptions specific and actionable
- Link to SD findings when applicable

### DON'T

- Leave tasks unchecked when work is complete
- Skip cross-reference creation
- Modify archived versions (docs/TODO/complete/)
- Mix multiple unrelated items in one task
- Forget to update CHANGELOG and VALIDATION

---
