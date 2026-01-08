---
description: Validate all crowndoc cross-references - ensure every reference resolves to existing documents, versions, and sections
allowed-tools: ["Read", "Grep", "Glob"]
---

# /crowndoc:validate

Validate the integrity of all cross-references in the crowndoc ecosystem.

---

## Purpose

Cross-references are the backbone of crowndoc's traceability. This command:
1. Scans all crowndoc documents for references
2. Parses each reference into components
3. Validates that targets exist
4. Reports broken or orphaned references
5. Optionally suggests or applies fixes

This ensures the documentation ecosystem remains navigable and accurate.

---

## Reference Format Reminder

The ONLY valid cross-reference format:

```
[DOCUMENT.md], [ver:`X.X.X`, sect:`Y)`]
```

**Components:**
- Document: `[TODO.md]`, `[CHANGELOG.md]`, `[VALIDATION.md]`, `[SD.md]`
- Version: `[ver:\`X.X.X\`]`
- Section (optional): `[sect:\`A)\`]`

**Valid Variations:**
```
[TODO.md], [ver:`0.0.1`]                        # Document + Version
[TODO.md], [ver:`0.0.1`, sect:`A)`]             # Document + Version + Section
[TODO.md], [ver:`0.0.1`, sect:`A)`,`B)`]        # Multiple sections
[TODO.md], [ver:`0.0.1`,`0.0.2`]                # Multiple versions
[TODO.md], [ver:`0.0.1`, sect:`A)`-`N)`]        # Section range
```

---

## Execution Steps

### Step 1: Identify All crowndoc Files

```python
# Core documents
core_docs = [
    "TODO.md",
    "CHANGELOG.md",
    "VALIDATION.md",
    "SD.md"
]

# Specification documents
spec_docs = glob("Docs/*.md")

# Archived documents
archived_todos = glob("docs/TODO/complete/*.md")
archived_todos_pending = glob("docs/TODO/pending/*.md")
archived_sd = glob("docs/SD/complete/*.md")
archived_sd_pending = glob("docs/SD/pending/*.md")

# All crowndoc files
all_crowndoc_files = (
    core_docs + 
    spec_docs + 
    archived_todos + 
    archived_todos_pending + 
    archived_sd + 
    archived_sd_pending
)

print(f"Scanning {len(all_crowndoc_files)} crowndoc files...")
```

### Step 2: Extract All References

```python
# Reference pattern
REFERENCE_PATTERN = r'\[([A-Z]+\.md)\],\s*\[ver:`([^`]+)`(?:,\s*sect:`([^`]+)`)?\]'

all_references = []

for file_path in all_crowndoc_files:
    content = read_file(file_path)
    
    for match in re.finditer(REFERENCE_PATTERN, content):
        reference = {
            "source_file": file_path,
            "source_line": get_line_number(content, match.start()),
            "full_match": match.group(0),
            "target_doc": match.group(1),
            "target_version": match.group(2),
            "target_section": match.group(3) if match.group(3) else None,
            "status": "PENDING"
        }
        all_references.append(reference)

print(f"Found {len(all_references)} cross-references")
```

### Step 3: Parse Version Specifications

```python
def parse_version_spec(version_str):
    """
    Parse version specifications like:
    - `0.0.1` → ["0.0.1"]
    - `0.0.1`,`0.0.2` → ["0.0.1", "0.0.2"]
    """
    versions = []
    for v in re.findall(r'`([^`]+)`', version_str):
        versions.append(v)
    return versions

def parse_section_spec(section_str):
    """
    Parse section specifications like:
    - `A)` → ["A)"]
    - `A)`,`B)` → ["A)", "B)"]
    - `A)`-`N)` → ["A)", "B)", ..., "N)"]
    """
    if not section_str:
        return []
    
    # Check for range
    range_match = re.match(r'`([A-Z])\)`-`([A-Z])\)`', section_str)
    if range_match:
        start = ord(range_match.group(1))
        end = ord(range_match.group(2))
        return [f"{chr(i)})" for i in range(start, end + 1)]
    
    # Multiple sections
    sections = []
    for s in re.findall(r'`([A-Z]\))`', section_str):
        sections.append(s)
    return sections

# Apply parsing
for ref in all_references:
    ref["parsed_versions"] = parse_version_spec(ref["target_version"])
    ref["parsed_sections"] = parse_section_spec(ref["target_section"])
```

### Step 4: Build Document Index

```python
# Index all documents and their contents
document_index = {}

for doc in ["TODO.md", "CHANGELOG.md", "VALIDATION.md", "SD.md"]:
    if file_exists(doc):
        content = read_file(doc)
        
        # Extract versions
        versions = re.findall(r'^## (\d+\.\d+\.\d+)', content, re.MULTILINE)
        
        # For each version, extract sections
        version_sections = {}
        for version in versions:
            version_content = extract_version_content(content, version)
            sections = re.findall(r'^### ([A-Z])\)', version_content, re.MULTILINE)
            version_sections[version] = sections
        
        document_index[doc] = {
            "versions": versions,
            "sections_by_version": version_sections
        }

# Also index archived documents
for archived in archived_todos + archived_sd:
    # Extract version from filename
    version = extract_version_from_filename(archived)
    content = read_file(archived)
    sections = re.findall(r'^### ([A-Z])\)', content, re.MULTILINE)
    
    # Determine original document
    if "TODO" in archived:
        doc_name = "TODO.md"
    else:
        doc_name = "SD.md"
    
    # Add to index
    if doc_name not in document_index:
        document_index[doc_name] = {"versions": [], "sections_by_version": {}}
    
    if version not in document_index[doc_name]["versions"]:
        document_index[doc_name]["versions"].append(version)
    
    document_index[doc_name]["sections_by_version"][version] = sections
```

### Step 5: Validate Each Reference

```python
validation_results = {
    "valid": [],
    "broken_document": [],
    "broken_version": [],
    "broken_section": [],
    "warnings": []
}

for ref in all_references:
    target_doc = ref["target_doc"]
    
    # Check 1: Document exists
    if target_doc not in document_index:
        ref["status"] = "BROKEN_DOCUMENT"
        ref["error"] = f"Document {target_doc} not found"
        validation_results["broken_document"].append(ref)
        continue
    
    doc_info = document_index[target_doc]
    
    # Check 2: Version(s) exist
    for version in ref["parsed_versions"]:
        if version not in doc_info["versions"]:
            ref["status"] = "BROKEN_VERSION"
            ref["error"] = f"Version {version} not found in {target_doc}"
            validation_results["broken_version"].append(ref)
            continue
    
    # Check 3: Section(s) exist (if specified)
    if ref["parsed_sections"]:
        for version in ref["parsed_versions"]:
            available_sections = doc_info["sections_by_version"].get(version, [])
            for section in ref["parsed_sections"]:
                section_letter = section.rstrip(")")
                if section_letter not in available_sections:
                    ref["status"] = "BROKEN_SECTION"
                    ref["error"] = f"Section {section} not found in {target_doc} version {version}"
                    validation_results["broken_section"].append(ref)
                    continue
    
    # All checks passed
    if ref["status"] == "PENDING":
        ref["status"] = "VALID"
        validation_results["valid"].append(ref)
```

### Step 6: Find Orphaned Sections

```python
# Sections that exist but are never referenced
orphaned_sections = []

for doc_name, doc_info in document_index.items():
    for version, sections in doc_info["sections_by_version"].items():
        for section in sections:
            # Check if any reference points to this section
            expected_ref_pattern = f"[{doc_name}], [ver:`{version}`, sect:`{section})"
            
            referenced = False
            for ref in all_references:
                if (ref["target_doc"] == doc_name and 
                    version in ref["parsed_versions"] and
                    section in [s.rstrip(")") for s in ref["parsed_sections"]]):
                    referenced = True
                    break
            
            if not referenced:
                orphaned_sections.append({
                    "document": doc_name,
                    "version": version,
                    "section": section,
                    "suggestion": "Add cross-reference or verify section is needed"
                })
```

### Step 7: Generate Report

```python
# Calculate statistics
total = len(all_references)
valid = len(validation_results["valid"])
broken = (
    len(validation_results["broken_document"]) +
    len(validation_results["broken_version"]) +
    len(validation_results["broken_section"])
)

print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║                   CROWNDOC VALIDATION REPORT                      ║
╚═══════════════════════════════════════════════════════════════════╝

Summary:
├── Total references: {total}
├── Valid: {valid} ✅
├── Broken: {broken} ❌
│   ├── Missing documents: {len(validation_results["broken_document"])}
│   ├── Missing versions: {len(validation_results["broken_version"])}
│   └── Missing sections: {len(validation_results["broken_section"])}
└── Orphaned sections: {len(orphaned_sections)} ⚠️
""")

# Detail broken references
if broken > 0:
    print("""
Broken References:
""")
    
    for category, refs in [
        ("Missing Documents", validation_results["broken_document"]),
        ("Missing Versions", validation_results["broken_version"]),
        ("Missing Sections", validation_results["broken_section"])
    ]:
        if refs:
            print(f"\n{category}:")
            for ref in refs:
                print(f"""
  {ref["source_file"]}:{ref["source_line"]}
  └── {ref["full_match"]}
      Error: {ref["error"]}
""")

# Detail orphaned sections
if orphaned_sections:
    print("""
Orphaned Sections (no incoming references):
""")
    for orphan in orphaned_sections:
        print(f"""
  {orphan["document"]} [ver:{orphan["version"]}] ### {orphan["section"]})
  └── {orphan["suggestion"]}
""")
```

### Step 8: Suggest Fixes

```python
suggestions = []

# For broken versions
for ref in validation_results["broken_version"]:
    # Check if version exists in archive
    doc_type = "TODO" if ref["target_doc"] == "TODO.md" else "SD"
    for version in ref["parsed_versions"]:
        archive_path = f"docs/{doc_type}/complete/{version}.md"
        if file_exists(archive_path):
            suggestions.append({
                "reference": ref["full_match"],
                "suggestion": f"Version exists in archive. Reference is valid for historical lookup.",
                "action": None
            })
        else:
            # Find closest version
            available = document_index.get(ref["target_doc"], {}).get("versions", [])
            if available:
                closest = find_closest_version(version, available)
                suggestions.append({
                    "reference": ref["full_match"],
                    "suggestion": f"Did you mean version {closest}?",
                    "action": f"Replace `{version}` with `{closest}`"
                })

# For broken sections
for ref in validation_results["broken_section"]:
    # Check if section letter was renamed
    for version in ref["parsed_versions"]:
        available = document_index[ref["target_doc"]]["sections_by_version"].get(version, [])
        for section in ref["parsed_sections"]:
            section_letter = section.rstrip(")")
            if section_letter not in available and available:
                suggestions.append({
                    "reference": ref["full_match"],
                    "suggestion": f"Section {section} not found. Available: {available}",
                    "action": f"Update section letter or verify source document"
                })

# Output suggestions
if suggestions:
    print("""
Suggested Fixes:
""")
    for i, sug in enumerate(suggestions, 1):
        print(f"""
  [{i}] {sug["reference"]}
      └── {sug["suggestion"]}
          {f"Action: {sug['action']}" if sug["action"] else ""}
""")
```

---

## Validation Rules

### Rule 1: Document Must Exist

Target document must be one of:
- Core documents: TODO.md, CHANGELOG.md, VALIDATION.md, SD.md
- Specification documents in Docs/
- Any file path if explicitly quoted

### Rule 2: Version Must Exist

Version must exist either:
- In the live document (current versions)
- In the archive (docs/*/complete/*.md)
- In pending (docs/*/pending/*.md)

### Rule 3: Section Must Exist in Version

If section is specified:
- Section letter must exist in the specified version
- Section letter must match pattern `X)` where X is A-Z

### Rule 4: Reference Consistency

References should be bidirectional where appropriate:
- If A references B, B should reference A (for related items)
- TODO → CHANGELOG → VALIDATION chain should be complete

---

## Auto-Fix Mode

With `--fix` flag:

```python
def auto_fix_references():
    for ref in validation_results["broken_version"]:
        # Only fix obvious cases
        closest = find_closest_version(ref["target_version"], available_versions)
        if is_likely_typo(ref["target_version"], closest):
            # Auto-fix
            fix_reference(ref["source_file"], ref["full_match"], fixed_match)
            print(f"Fixed: {ref['full_match']} → {fixed_match}")
    
    # Do NOT auto-fix section issues (too risky)
    # Do NOT auto-fix missing documents (requires investigation)
```

---

## Output Formats

### Summary Output (default)

```
crowndoc validation: ✅ All 42 references valid
```

or

```
crowndoc validation: ❌ 3 broken references found

Run with --verbose for details
```

### Verbose Output (--verbose)

Full report as shown in Step 7.

### JSON Output (--json)

```json
{
  "total": 42,
  "valid": 39,
  "broken": 3,
  "broken_references": [
    {
      "source_file": "TODO.md",
      "source_line": 45,
      "reference": "[CHANGELOG.md], [ver:`0.0.9`]",
      "error": "Version 0.0.9 not found in CHANGELOG.md"
    }
  ],
  "orphaned_sections": [
    {
      "document": "TODO.md",
      "version": "0.0.5",
      "section": "F"
    }
  ],
  "suggestions": [...]
}
```

---

## Integration with Other Commands

### Called By

- `crowndoc: status` - quick health check
- `crowndoc: TODO` - before archiving versions
- `crowndoc: SD` - before completing passes

### Triggers

Consider running validation:
- After completing any version
- Before archiving
- When documents are modified
- As part of CI/CD

---

## Error Handling

### File Read Errors

```
Warning: Cannot read docs/TODO/complete/0.0.3.md
└── File may be corrupted or permissions issue
```

### Pattern Parse Errors

```
Warning: Malformed reference in CHANGELOG.md:78
└── [TODO.md, [ver:0.0.1]  ← Missing closing bracket
```

### Large File Handling

For very large documents (>1MB):
- Use streaming parse
- Limit memory usage
- Report progress

---

## Best Practices

### DO

- Run validation before archiving any version
- Fix broken references immediately
- Review orphaned sections periodically
- Use consistent reference format

### DON'T

- Ignore broken reference warnings
- Create references to non-existent targets
- Modify archived documents (creates broken refs)
- Use non-standard reference formats

---
