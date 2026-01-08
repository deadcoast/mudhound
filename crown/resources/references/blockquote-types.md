# Blockquote Types Reference

Crown uses GitHub-flavored markdown alerts for semantic markup. Each type has a specific purpose.

---

## [!NOTE]

**Purpose:** Metadata, protocol information, informational content

**Usage:** PROTOCOL blocks, configuration details, neutral information

**Example:**
```markdown
> [!NOTE]
> versioning: canonical
> dependencies: TODO.md, CHANGELOG.md
> status: 'tracking task completion'
```

**When to use:**
- Document PROTOCOL blocks
- Metadata about documents/sections
- Configuration information
- Neutral informational content
- Cross-reference context

---

## [!IMPORTANT]

**Purpose:** Task descriptions, key information requiring attention

**Usage:** TODO task sections, significant details, action items

**Example:**
```markdown
> [!IMPORTANT]
> Implement the search command with pagination support.
> Must handle empty results gracefully.
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

**When to use:**
- TODO task descriptions
- Key requirements
- Action items
- Important details that shouldn't be missed
- Version summaries in CHANGELOG

---

## [!WARNING]

**Purpose:** SD findings, issues discovered, problems identified

**Usage:** SD workflow findings, issue documentation, problems

**Example:**
```markdown
> [!WARNING]
> type: U (UNUSED)
> severity: HIGH
> location: `core/cache.py:45`
```

**When to use:**
- SD scan findings
- Identified issues
- Problems that need resolution
- Quality concerns
- Integration gaps

---

## [!TIP]

**Purpose:** Navigation hints, next steps, helpful suggestions

**Usage:** Workflow guidance, archive references, suggestions

**Example:**
```markdown
> [!TIP]
> Previous version: [docs/TODO/complete/0.0.8.md]
> Completed versions: [docs/TODO/complete/]
> Use `/crown:status` to see current state.
```

**When to use:**
- Navigation to archives
- Workflow guidance
- Helpful suggestions
- Next step recommendations
- Links to related content

---

## [!CAUTION]

**Purpose:** Critical rules that MUST be followed, destructive warnings

**Usage:** Integration over deletion principle, critical constraints

**Example:**
```markdown
> [!CAUTION]
> NEVER delete unused code first.
> Investigate origin and design intent.
> Find integration path.
> Deletion requires explicit approval.
```

**When to use:**
- Critical rules (like integration over deletion)
- Destructive action warnings
- Constraints that must not be violated
- Safety-critical information
- Irreversible action warnings

---

## Usage in Documents

### TODO.md

```markdown
### PROTOCOL
> [!NOTE]
> versioning: canonical
> ...

### A) Task Title
> [!IMPORTANT]
> Task description...

> [!TIP]
> Previous version: [docs/TODO/complete/...]
```

### CHANGELOG.md

```markdown
### PROTOCOL
> [!NOTE]
> versioning: canonical
> ...

## 0.0.1
> [!IMPORTANT]
> Version summary...
```

### VALIDATION.md

```markdown
### A) Component - VERIFIED
> [!NOTE]
> Verification description...
```

### SD.md

```markdown
### PROTOCOL
> [!NOTE]
> status: 'scanning Q1'
> principle: INTEGRATION OVER DELETION

> [!CAUTION]
> NEVER delete unused code first.

### Finding 1
> [!WARNING]
> type: U (UNUSED)
> severity: HIGH

> [!TIP]
> Next: /crown:sd S Q2
```

---

## Rendering

These blockquotes render as styled callouts in:
- GitHub
- Many markdown renderers
- Documentation systems

Example appearance:
- NOTE: Blue/gray information box
- IMPORTANT: Purple/magenta emphasis box
- WARNING: Yellow/orange warning box
- TIP: Green suggestion box
- CAUTION: Red danger box

---

## Best Practices

### DO
- Use consistent type for same purpose
- Keep content concise
- Include cross-references where appropriate
- Use most appropriate type for context

### DON'T
- Mix types arbitrarily
- Use WARNING for non-issues
- Use CAUTION for minor notes
- Nest blockquotes

---
