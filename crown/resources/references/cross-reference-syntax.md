# Cross-Reference Syntax Reference

## The Format

```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

This is the ONLY valid cross-reference format in crown documents.

---

## Components

### Document Component

Specifies which document is being referenced.

| Document | Purpose |
|----------|---------|
| `[TODO.md]` | Task tracking |
| `[CHANGELOG.md]` | Completion records |
| `[VALIDATION.md]` | Verification |
| `[SD.md]` | Codebase review |

### Version Component

Specifies which version within the document.

**Single version:**
```
[ver:`0.0.1`]
```

**Multiple versions:**
```
[ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

### Section Component

Specifies which section within the version.

**Single section:**
```
[sect:`A)`]
```

**Multiple sections:**
```
[sect:`A)`,`B)`,`C)`]
```

**Section range:**
```
[sect:`A)`-`N)`]
```

---

## Valid Combinations

### Document + Version

Reference an entire version:
```markdown
[TODO.md], [ver:`0.0.1`]
```

Use when referring to all tasks in a version.

### Document + Version + Section

Reference a specific section:
```markdown
[CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

Use when referring to a specific task or category.

### Document + Version + Multiple Sections

Reference several related sections:
```markdown
[VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
```

Use when multiple sections are related.

### Document + Multiple Versions

Reference across versions:
```markdown
[TODO.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

Use when tracking evolution across versions.

### Document + Version + Section Range

Reference a range of sections:
```markdown
[TODO.md], [ver:`0.0.1`, sect:`C)`-`N)`]
```

Use when referring to a block of related tasks.

---

## Where References Appear

### In TODO.md Task Sections

```markdown
### A) Task Title

> [!IMPORTANT]
> Description of the task.
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

Points forward to where completion will be recorded.

### In CHANGELOG.md Entries

```markdown
### A) Feature - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| Feature | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
```

Points to verification record.

### In VALIDATION.md Entries

```markdown
### A) Feature - VERIFIED

> [!NOTE]
> Verification of feature.
> [TODO.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

Points back to source and completion.

### In SD.md Findings

```markdown
### Q1 Finding 1

> [!WARNING]
> type: U (UNUSED)

**TODO:** [TODO.md], [ver:`0.0.1`, sect:`A)`]
```

Points to generated task.

---

## Resolution Rules

### Document Resolution

1. Check root document first (TODO.md, CHANGELOG.md, etc.)
2. For archived versions, check docs/*/complete/
3. For pending versions, check docs/*/pending/

### Version Resolution

1. Parse `## X.X.X` headers in document
2. Match requested version
3. If not found in root, check archives

### Section Resolution

1. Parse `### Y)` headers within version
2. Match requested section letter
3. Section must exist in specified version

---

## Validation

Use `/crown:validate` to check all references:
- Verifies documents exist
- Verifies versions exist
- Verifies sections exist
- Reports broken references
- Identifies orphaned sections

---

## Common Patterns

### Task Completion Flow

```
TODO task created:
  [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
  [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]

CHANGELOG entry added:
  [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]

VALIDATION entry added:
  [TODO.md], [ver:`0.0.1`, sect:`A)`]
  [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

### SD Finding Flow

```
SD finding documented:
  [TODO.md], [ver:`0.0.1`, sect:`A)`]

TODO task references back:
  [SD.md], [ver:`0.0.1`, sect:`Q1 Finding 1`]
```

---

## Anti-Patterns

### DON'T: Invent new formats
```markdown
❌ [TODO.md v0.0.1 section A]
❌ TODO.md:0.0.1:A
❌ (see TODO.md version 0.0.1)
```

### DON'T: Omit backticks
```markdown
❌ [TODO.md], [ver:0.0.1, sect:A)]
```

### DON'T: Mix formats
```markdown
❌ [TODO.md], [ver:`0.0.1`], section A
```

### DO: Use exact format
```markdown
✅ [TODO.md], [ver:`0.0.1`, sect:`A)`]
```

---
