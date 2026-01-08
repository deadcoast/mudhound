# Cross-Reference Patterns

## The ONLY Format

```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

---

## Valid Examples

### Single document, single version
```
[TODO.md], [ver:`0.0.1`]
```

### Single document, version + section
```
[CHANGELOG.md], [ver:`0.0.1`, sect:`A)`]
```

### Single document, multiple sections
```
[VALIDATION.md], [ver:`0.0.3`, sect:`B)`,`E)`]
```

### Single document, multiple versions
```
[VALIDATION.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`]
```

### Section range
```
[TODO.md], [ver:`0.0.1`, sect:`C)`-`N)`]
```

---

## Cross-Reference Flow

### SD Finding → TODO
```markdown
### A) Unused SearchCache

> [!WARNING]
> type: U (UNUSED)
> severity: MEDIUM
> location: `core/cache.py:45`
> [TODO.md], [ver:`0.0.7`, sect:`A)`]
```

### TODO Completion → CHANGELOG
```markdown
### A) Integrate SearchCache

> [!IMPORTANT]
> SearchCache integrated into engine.
> [VALIDATION.md], [ver:`0.0.8`, sect:`A)`]
> [CHANGELOG.md], [ver:`0.0.7`, sect:`A)`]
```

### CHANGELOG Entry
```markdown
### A) Core Improvements

| Component | Status | Reference |
| --------- | ------ | --------- |
| SearchCache | ✅ | [VALIDATION.md], [ver:`0.0.8`, sect:`A)`] |
```

### VALIDATION Entry
```markdown
### A) SearchCache Integration Verified

> [!NOTE]
> pytest: 150 passed
> Integration tested in engine.py
> [TODO.md], [ver:`0.0.7`, sect:`A)`] - Original task
> [CHANGELOG.md], [ver:`0.0.7`, sect:`A)`] - Completion
```

---

## Traceability

Every change can be traced:
1. **Origin**: Where was this identified? (SD finding, user request)
2. **Task**: Where is the work tracked? (TODO.md)
3. **Completion**: Where is it documented? (CHANGELOG.md)
4. **Verification**: Where is it validated? (VALIDATION.md)

All linked via `[ver:X.X.X, sect:Y)]` references.
