# py-simple

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting](https://img.shields.io/badge/linting-ruff-blue.svg)](https://github.com/astral-sh/ruff)
[![Package Manager](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)

A simple Python template for API data processing and analysis. Fetch JSON data from public APIs, process it, and save results to local files.

## Features

- **Fast setup** with `uv` package manager
- **Configurable** via environment variables
- **Data processing** with built-in statistics
- **Organized output** with timestamped files
- **Clean code** with Black formatting and Ruff linting
- **Comprehensive docs** and examples
- **VS Code ready** with pre-configured settings

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/py-simple.git
cd py-simple

# Set up virtual environment and install dependencies
make venv
source .venv/bin/activate  # Linux/macOS
make install-dev

# Set up environment configuration
cp .env.example .env
# Edit .env with your preferred settings (optional - defaults work fine)

# Run with default settings
make run
```

## What It Does

The application:

1. **Fetches** JSON data from a configurable API endpoint
2. **Processes** the data to generate useful statistics
3. **Saves** both raw data and processed summaries to timestamped files

**Example Output:**

- `data/processed_raw_20240115_103043.json` - Original API data
- `data/processed_summary_20240115_103043.json` - Statistics and metadata

## Configuration

Copy the example configuration file and customize as needed:

```bash
cp .env.example .env
```

Then edit `.env` to customize behavior:

```env
# API Configuration
API_URL=https://jsonplaceholder.typicode.com/posts  # Change to your API
API_TIMEOUT=30                                      # Request timeout in seconds

# Output Configuration
DATA_FOLDER=data                                    # Directory for output files
OUTPUT_PREFIX=processed_                            # Filename prefix
LOG_LEVEL=INFO                                      # DEBUG, INFO, WARNING, ERROR
```

**Note:** The application works with default values even without a `.env` file, but creating one allows you to customize the behavior for your specific needs.

## Usage Examples

```bash
# Default usage (JSONPlaceholder posts)
make run

# Fetch different data
API_URL=https://jsonplaceholder.typicode.com/users make run

# Custom output location
DATA_FOLDER=my_data OUTPUT_PREFIX=api_ make run

# Debug mode
LOG_LEVEL=DEBUG make run
```

## Development

### Available Commands

```bash
make help           # Show all available commands
make venv           # Create virtual environment
make install        # Install production dependencies
make install-dev    # Install development dependencies
make run            # Run the application
make lint           # Run linting with auto-fix
make format         # Format code with Black
make test           # Run tests
make clean          # Clean up build artifacts
```

### Code Quality

This project uses modern Python tooling:

- **[uv](https://github.com/astral-sh/uv)** - Fast Python package installer
- **[Black](https://github.com/psf/black)** - Code formatting
- **[Ruff](https://github.com/astral-sh/ruff)** - Fast Python linter
- **[pytest](https://pytest.org)** - Testing framework

### VS Code Integration

The project includes VS Code settings for:

- Python interpreter configuration
- Auto-formatting on save with Black
- Linting with Ruff
- Import organization

**Recommended Extensions:**

- Python (ms-python.python)
- Black Formatter (ms-python.black-formatter)
- Ruff (charliermarsh.ruff)

## Project Structure

```
py-simple/
├── py_simple/                  # Main Python package
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   └── main.py                # Main application logic
├── data/                      # Output directory for processed data
├── docs/                      # Documentation
│   ├── git-commands.md        # Git workflow guide
│   ├── installation.md        # Setup instructions
│   └── how-to-use.md         # Usage guide
├── tests/                     # Test suite
├── .vscode/                   # VS Code configuration
│   └── settings.json
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore rules
├── Makefile                 # Build and development commands
├── pyproject.toml          # Project configuration and dependencies
└── README.md               # This file
```

## Requirements

- **Python 3.8+**
- **uv** (recommended) or pip for package management
- **Git** for version control

## Installation

See the [Installation Guide](docs/installation.md) for detailed setup instructions.

## Usage

See the [Usage Guide](docs/how-to-use.md) for examples and configuration options.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and test them
4. Run the linter: `make lint`
5. Commit your changes: `git commit -m "Add: your feature description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Create a Pull Request

See [Git Commands](docs/git-commands.md) for detailed workflow instructions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Free fake API for testing
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter
- [Black](https://github.com/psf/black) - Python code formatter
