# Changelog

## 0.0.0

### A) PROTOCOL

> [!NOTE]
> This document tracks completed work and releases. It complements the `TODO.md` and `VALIDATION.md` documents
> The document is organized canonically by version
> These are living documents, when one is changed, the others must be updated

---

## 0.0.1

- 2026-01-07

> [!IMPORTANT]
> Initial release of MudHound. Core infrastructure is complete
> [TODO.md], [ver:`0.0.1`] - Outstanding work items
> [VALIDATION.md], [ver:`0.0.1`,`0.0.2`,`0.0.3`,`0.0.4`] - Validation findings

### A) Core Infrastructure - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| Data Models (`core/result.py`) | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`A)`] |
| Search Engine (`core/engine.py`) | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`B)`] |
| Exception Hierarchy (`core/exceptions.py`) | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`C)`] |
| Config Manager (`core/config.py`) | ✅ | [VALIDATION.md], [ver:`0.0.4`, sect:`A)`] |
| Result Store (`core/store.py`) | ✅ | [VALIDATION.md], [ver:`0.0.4`, sect:`A)`] |

### B) Adapter System - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| DuckDuckGo Adapter | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`D)`] |
| Adapter Registry | ✅ | [VALIDATION.md], [ver:`0.0.1`, sect:`E)`] |
| Plugin Discovery | ✅ | [VALIDATION.md], [ver:`0.0.4`, sect:`B)`] |

### C) CLI Commands - PARTIAL

| Component | Status | Reference |
| --------- | ------ | --------- |
| `mh config` | ✅ | [VALIDATION.md], [ver:`0.0.2`, sect:`A)`] |
| `mh history` | ✅ | [VALIDATION.md], [ver:`0.0.2`, sect:`A)`] |
| `mh interactive` | ✅ | [VALIDATION.md], [ver:`0.0.2`, sect:`A)`] |
| `mh version` | ✅ | [VALIDATION.md], [ver:`0.0.2`, sect:`A)`] |
| `mh search` | ❌ | [TODO.md], [ver:`0.0.1`, sect:`A)`] |
| `mh export` | ❌ | [TODO.md], [ver:`0.0.1`, sect:`B)`] |

### D) UI System - PARTIAL

| Component | Status | Reference |
| --------- | ------ | --------- |
| Assets System | ✅ | [VALIDATION.md], [ver:`0.0.3`, sect:`A)`] |
| Theme Engine | ✅ | [VALIDATION.md], [ver:`0.0.3`, sect:`B)`] |
| Animation System | ✅ | [VALIDATION.md], [ver:`0.0.3`, sect:`B)`] |
| Banner Component | ✅ | [VALIDATION.md], [ver:`0.0.3`, sect:`B)`] |
| Menu Component | ✅ | [VALIDATION.md], [ver:`0.0.3`, sect:`B)`] |
| Floating Components | ❌ | [TODO.md], [ver:`0.0.1`, sect:`D)`-`K)`] |

### E) Logging System - COMPLETE

| Component | Status | Reference |
| --------- | ------ | --------- |
| Custom Levels | ✅ | [VALIDATION.md], [ver:`0.0.4`, sect:`C)`] |
| Styled Formatter | ✅ | [VALIDATION.md], [ver:`0.0.4`, sect:`C)`] |
| File Handler | ✅ | [VALIDATION.md], [ver:`0.0.4`, sect:`C)`] |

### F) Utils - PARTIAL

| Component | Status | Reference |
| --------- | ------ | --------- |
| Terminal utils | ⚠️ | [VALIDATION.md], [ver:`0.0.4`, sect:`D)`] |
| Validators | ⚠️ | [VALIDATION.md], [ver:`0.0.4`, sect:`D)`] |

---

## 0.0.2

- YEAR-MM-DD

> [!NOTE]
> Placeholder for next release
> [TODO.md], [ver:`0.0.2`]
> [VALIDATION.md], [ver:`0.0.5`]

---
