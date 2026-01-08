# crowndoc

AI-optimized documentation ecosystem with cross-referenced workflows for TODO, CHANGELOG, VALIDATION, and SeekAndDestroy codebase review.

## Overview

crowndoc is a documentation format designed for AI agents, not human consumption. It provides:

- **Cross-referenced documents** that link via `[DOCUMENT.md], [ver:X.X.X, sect:Y)]`
- **Token-efficient structure** with versioned archives and minimal LIVE documents
- **Workflow automation** for task tracking and codebase review
- **Integration over deletion** principle for unused code

## Installation

```bash
# Claude Code
cc --plugin-dir /path/to/crowndoc-plugin

# Or copy to project
cp -r crowndoc-plugin/.claude-plugin /your/project/
```

## Commands

| Command | Description |
| ------- | ----------- |
| `/crowndoc:init` | Initialize crowndoc in a repository |
| `/crowndoc:status` | Show current state across all documents |
| `/crowndoc:TODO` | Execute TODO workflow |
| `/crowndoc:SD [phase]` | Execute SeekAndDestroy workflow |
| `/crowndoc:validate` | Validate cross-references |
| `/crowndoc:continue` | Resume from current state |

## Document Structure

```
ROOT/
├── TODO.md          # LIVE task tracking
├── CHANGELOG.md     # Completion tracking
├── VALIDATION.md    # Verification
├── SD.md            # LIVE codebase review
├── Docs/
│   ├── crowndoc.md  # Specification
│   └── SD.md        # SD workflow spec
├── docs/
│   ├── TODO/
│   │   ├── complete/   # Archived versions
│   │   └── pending/    # Incomplete revisions
│   └── SD/
│       ├── complete/   # Completed passes
│       └── pending/    # Incomplete passes
└── templates/
```

## Cross-Reference Format

```
[DOCUMENT.md], [ver:X.X.X, sect:Y)]
```

Examples:
- `[TODO.md], [ver:0.0.1, sect:A)]`
- `[CHANGELOG.md], [ver:0.0.2, sect:B),C)]`
- `[VALIDATION.md], [ver:0.1.0]`

## Workflows

### TODO Workflow

1. Read TODO.md (LIVE)
2. Work pending tasks
3. Update cross-references to CHANGELOG.md, VALIDATION.md
4. Archive completed version to docs/TODO/complete/

### SD Workflow (SeekAndDestroy)

| Phase | Command | Action |
| ----- | ------- | ------ |
| Recon | `SD:R` | Map quadrants, count files |
| Scan | `SD:S Q1` | Scan quadrant, flag findings |
| Flag | `SD:F` | Document findings, create TODO entries |
| Resolve | `SD:X` | Integrate (never delete first) |
| Verify | `SD:V` | Run tests, update VALIDATION.md |

### Finding Types

- **U: UNUSED** - investigate & integrate
- **I: INTEGRATION** - connect to workflow
- **T: TYPE** - fix annotation
- **P: PATTERN** - apply standard

## Principles

### Token Efficiency

- Split files by version
- Load only relevant sections
- Minimal index in LIVE documents
- Archive completed work

### Integration Over Deletion

> **NEVER delete unused code first.**
> Investigate origin and design intent.
> Find integration path.
> Deletion requires explicit approval.

## Skills

- `crowndoc-format` - Document structure and cross-referencing
- `crowndoc-workflows` - TODO and SD workflow execution

## Agent

- `crowndoc-workflow` - Executes crowndoc workflows automatically

## License

MIT
