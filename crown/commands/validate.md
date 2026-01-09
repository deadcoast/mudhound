---
description: Validate crown cross-references - ensure all references resolve to existing documents, versions, sections
allowed-tools: Read, Glob, Grep
---

Validate the integrity of all cross-references in the crown ecosystem.

## Execution

### 1. Identify All crown Files

Scan these locations:
- Root: TODO.md, CHANGELOG.md, VALIDATION.md, SD.md
- Specs: Docs/*.md
- Archives: docs/TODO/complete/*.md, docs/TODO/pending/*.md
- Archives: docs/SD/complete/*.md, docs/SD/pending/*.md

### 2. Extract All References

Find all patterns matching:
```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
[DOCUMENT.md], [ver:`X.X.X`]
```

For each reference, extract:
- Target document
- Target version(s)
- Target section(s) if specified

### 3. Parse Version Specifications

**Single:** `[ver:\`0.0.1\`]` → ["0.0.1"]
**Multiple:** `[ver:\`0.0.1\`,\`0.0.2\`]` → ["0.0.1", "0.0.2"]

### 4. Parse Section Specifications

**Single:** `[sect:\`A)\`]` → ["A)"]
**Multiple:** `[sect:\`A)\`,\`B)\`]` → ["A)", "B)"]
**Range:** `[sect:\`A)\`-\`N)\`]` → ["A)", "B)", ..., "N)"]

### 5. Validate Each Reference

**Check 1: Document exists**
- Root document OR
- Archive path (docs/*/complete/*.md)

**Check 2: Version exists**
- `## X.X.X` header in document OR
- Archive file named X.X.X.md

**Check 3: Section exists (if specified)**
- `### Y)` header in that version

### 6. Find Orphaned Sections

Sections that exist but are never referenced:
- No incoming `[sect:\`Y)\`]` references
- May indicate:
  - Missing cross-reference
  - Section should be removed
  - Incomplete linking

### 7. Output Report

```
crown validation

References: 42 total
├── Valid: 39 ✅
└── Broken: 3 ❌

Broken References:
├── TODO.md:45
│   └── [CHANGELOG.md], [ver:`0.0.9`]
│       Error: Version 0.0.9 not found
│
└── VALIDATION.md:78
    └── [TODO.md], [ver:`0.0.5`, sect:`Z)`]
        Error: Section Z) not found in version 0.0.5

Orphaned Sections:
└── TODO.md [ver:0.0.7] ### F)
    └── No incoming references

Suggestions:
├── [1] Update version reference to 0.0.8
└── [2] Add cross-reference to section F) or remove
```

### 8. Suggest Fixes

For resolvable issues:
- Typos in version numbers
- Renamed sections
- Missing references

Do NOT auto-fix without confirmation.

## Reference Format Reminder

The ONLY valid format:
```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

Components:
- Document: `[TODO.md]`, `[CHANGELOG.md]`, etc.
- Version: `[ver:\`X.X.X\`]`
- Section: `[sect:\`Y)\`]` (optional)
