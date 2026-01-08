# Cross-Reference Patterns

Real examples of cross-reference usage in crown documents.

---

## Pattern 1: Task Creation

When creating a new task in TODO.md:

```markdown
### A) Implement Search Command

> [!IMPORTANT]
> Create the `mh search` CLI command with query support.
> [VALIDATION.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

Points forward to where completion and verification will be recorded.

---

## Pattern 2: Task Completion

When completing a task, update CHANGELOG.md:

```markdown
## 0.0.1

- 2026-01-07

> [!IMPORTANT]
> Initial release with search functionality.
> [TODO.md], [ver:`0.0.1`]
> [VALIDATION.md], [ver:`0.0.1`]

### A) Search Command - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| `mh search` command | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
| Query parsing | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
| Result display | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
```

Points to source (TODO) and verification (VALIDATION).

---

## Pattern 3: Verification Record

When verifying completed work:

```markdown
### A) Search Command - VERIFIED

> [!NOTE]
> Search command implementation verified.
> [TODO.md], [ver:`0.0.1`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]

**Verification:**
- pytest: 25 passed
- mypy: clean
- ruff: clean
- Manual: command works correctly
```

Points back to source and completion record.

---

## Pattern 4: SD Finding to TODO

When SD scan generates a finding:

**In SD.md:**
```markdown
### Q1 Finding 1: unused_cache_function

> [!WARNING]
> type: U (UNUSED)
> severity: HIGH
> location: `core/cache.py:45`

**TODO:** [TODO.md], [ver:`0.0.2`, sect:`A)`]
```

**In TODO.md:**
```markdown
### A) Integrate Cache Function

> [!IMPORTANT]
> SD finding: cache function exists but not connected.
> [SD.md], [ver:`0.0.1`, sect:`Q1 Finding 1`]
> [VALIDATION.md], [ver:`0.0.2`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.2`, sect:`A)`]
```

Bidirectional reference between SD finding and generated task.

---

## Pattern 5: Multiple Sections

When referencing multiple related sections:

```markdown
> [!IMPORTANT]
> UI integration complete.
> [TODO.md], [ver:`0.0.1`, sect:`C)`,`E)`,`J)`]
> [CHANGELOG.md], [ver:`0.0.1`, sect:`D)`]
```

References sections C, E, and J from TODO version 0.0.1.

---

## Pattern 6: Section Range

When referencing a range of sections:

```markdown
> [!NOTE]
> All UI components integrated.
> [TODO.md], [ver:`0.0.1`, sect:`C)`-`N)`]
```

References sections C through N (inclusive).

---

## Pattern 7: Multiple Versions

When work spans multiple versions:

```markdown
> [!NOTE]
> Feature developed across versions.
> [TODO.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

References three different TODO versions.

---

## Pattern 8: Archive Reference

After archiving a version:

```markdown
> [!TIP]
> Previous version: [docs/TODO/complete/0.0.1.md]
> All completed versions: [docs/TODO/complete/]
```

Points to archived version for history.

---

## Pattern 9: SD Pass Archive

After completing an SD pass:

```markdown
> [!NOTE]
> Q1 pass complete.
> [docs/SD/complete/0.0.1-Q1.md]
> [VALIDATION.md], [ver:`0.1.0`, sect:`A)`]
```

Points to archived pass and verification.

---

## Pattern 10: Cross-Document Chain

Complete traceability chain:

```
TODO.md 0.0.1 sect:A
    │
    ├──→ CHANGELOG.md 0.0.1 sect:A
    │         │
    │         └──→ VALIDATION.md 0.0.1 sect:A
    │                    │
    │                    ├──→ TODO.md 0.0.1 sect:A (back)
    │                    └──→ CHANGELOG.md 0.0.1 sect:A (back)
    │
    └──→ VALIDATION.md 0.0.1 sect:A
```

Every document links to related documents, creating full traceability.

---

## Validation

Use `/crown:validate` to verify all references resolve:

```
crown validation

References: 42 total
├── Valid: 42 ✅
└── Broken: 0 ❌

All references valid.
```

---
