# MudHound

Terminal-based batch URL extraction tool with animated UI and multiple search engine support.

## Features

- 🔍 Batch keyword searches across multiple search engines
- 🎨 Animated terminal UI with rainbow color cycling
- 🎯 Modular adapter architecture for search engines
- 📊 Export results in multiple formats (JSON, CSV, TXT, URLs)
- 📜 Search history and replay functionality
- ⚙️ Extensive configuration options
- 🎭 Multiple themes and color schemes

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/mudhound/mudhound.git
cd mudhound

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Using pip (when published)

```bash
pip install mudhound
```

## Quick Start

```bash
# Basic search
mh search "python libraries"

# Search with options
mh search "machine learning" --max 100 --region us-en

# Interactive mode
mh interactive

# View search history
mh history list

# Export results
mh export --format json --output results.json

# Configure settings
mh config set general.max_results 100
mh config list
```

## Usage

### Search Command

```bash
mh search <query> [OPTIONS]

Options:
  --max INTEGER          Maximum number of results (default: 50)
  --engine TEXT          Search engine to use (default: duckduckgo)
  --region TEXT          Search region (default: wt-wt)
  --safesearch TEXT      Safe search level (default: moderate)
  --time TEXT            Time limit for results
  --output PATH          Output file path
  --format TEXT          Output format (json, csv, txt, urls)
  --quiet                Suppress UI output
  --interactive          Enable interactive mode with live filtering
```

### Configuration

MudHound looks for configuration files in the following order:
1. Path specified with `--config` flag
2. `MUDHOUND_CONFIG` environment variable
3. `./mudhound.toml` (current directory)
4. `~/.config/mudhound/config.toml` (XDG standard)
5. `~/.mudhound/config.toml` (legacy location)
6. Built-in defaults

### Themes

Available themes:
- `default` - MudHound default theme
- `minimal` - Minimal color scheme
- `hacker` - Matrix-inspired green theme

```bash
# Set theme
mh --theme hacker search "cybersecurity"

# Or configure permanently
mh config set ui.theme hacker
```

## Development

### Project Structure

```
mudhound/
├── cli/              # Command layer (Typer app, commands)
├── ui/               # Presentation layer (renderer, frames, animation)
├── core/             # Core layer (engine, store, config)
├── adapters/         # Adapter layer (search engines)
├── assets/           # ANSI art and static files
├── logging/          # Logging subsystem
├── utils/            # Utility functions
└── data/             # Default configuration and themes
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mudhound --cov-report=html

# Run property-based tests
pytest tests/property/

# Run specific test file
pytest tests/unit/test_config.py
```

### Code Quality

```bash
# Format code
black mudhound/

# Lint code
ruff check mudhound/

# Type checking
mypy mudhound/
```

## Requirements

- Python 3.8+
- Terminal with ANSI color support
- Minimum terminal size: 60 columns × 10 rows

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for CLI
- UI powered by [Rich](https://rich.readthedocs.io/)
- Search via [duckduckgo-search](https://github.com/deedy5/duckduckgo_search)
