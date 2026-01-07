"""Demo script for the Table component."""

from mudhound.core.result import SearchResult
from mudhound.ui.components.table import Table
from mudhound.ui.layout import LayoutManager

# Create some sample search results
results = [
    SearchResult(
        url="https://www.example.com/page1",
        title="Example Page 1",
        snippet="This is a snippet from example page 1",
        source="example.com",
        rank=1,
        metadata={},
    ),
    SearchResult(
        url="https://www.verylongdomainname.com/very/long/path/to/resource",
        title="Very Long URL Example",
        snippet="This demonstrates URL truncation",
        source="verylongdomainname.com",
        rank=2,
        metadata={},
    ),
    SearchResult(
        url="https://www.python.org/docs",
        title="Python Documentation",
        snippet="Official Python documentation",
        source="python.org",
        rank=3,
        metadata={},
    ),
    SearchResult(
        url="https://github.com/python/cpython",
        title="CPython Repository",
        snippet="The Python programming language",
        source="github.com",
        rank=4,
        metadata={},
    ),
    SearchResult(
        url="https://stackoverflow.com/questions/tagged/python",
        title="Python Questions",
        snippet="Questions tagged with python",
        source="stackoverflow.com",
        rank=5,
        metadata={},
    ),
]

# Create layout manager
layout_manager = LayoutManager()

# Create table
table = Table(results=results, layout_manager=layout_manager,
              use_color=True, page_size=10)

# Render the table
print("Table Component Demo")
print("=" * 80)
print()

rendered_lines = table.render()
for line in rendered_lines:
    print(line)

print()
print("=" * 80)
print("Table rendered successfully!")
print(f"Total results: {len(results)}")
print(f"Terminal size: {layout_manager.get_terminal_size()}")
