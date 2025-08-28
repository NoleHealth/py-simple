# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python learning template (`py-simple`) designed as a starter project for developers learning Python project setup, configuration management, and modern development practices. The core application fetches JSON data from APIs, processes it with statistical analysis, and saves timestamped output files.

## Architecture

**Core Components:**

- `py_simple/main.py` - Main application pipeline: fetch → process → save with logging throughout
- `py_simple/config.py` - Environment-based configuration using python-dotenv with property-based access
- Data flow: API call → JSON processing → dual file output (raw data + summary with statistics)

**Key Design Patterns:**

- Pipeline architecture with clear separation of concerns (fetch/process/save)
- Configuration via environment variables with sensible defaults
- Comprehensive logging at each pipeline stage
- Timestamped output files for data lineage tracking

## Development Commands

**Essential Commands:**

```bash
# Setup and dependencies
make venv                    # Create .venv using uv
make install-dev            # Install with dev dependencies
source .venv/bin/activate   # Activate environment

# Code quality
make lint                   # Run ruff check --fix . && ruff format .
make test                   # Run pytest with coverage (80% minimum)

# Running
make run                    # Execute main pipeline
API_URL=https://example.com make run  # Override config via env vars
```

**Testing:**

```bash
uv run pytest tests/                    # All tests
uv run pytest tests/test_main.py       # Single test file
uv run pytest -k "test_process_data"   # Single test function
uv run pytest --cov-report=html        # Generate HTML coverage report
```

**CLI Usage:**

```bash
uv run python -m py_simple.main --help                    # Show help
uv run python -m py_simple.main --api-url URL             # Override API URL
uv run python -m py_simple.main --data-folder PATH        # Override data folder
make run-cli-example                                       # Run with CLI args example
```

## Configuration System

The application uses a property-based Config class that loads from (in priority order):

1. CLI arguments (highest priority) - `--api-url`, `--data-folder`
2. Environment variables
3. `.env` file in project root
4. Hardcoded defaults (lowest priority)

**Key Environment Variables:**

- `API_URL` - Data source endpoint (default: JSONPlaceholder posts)
- `API_TIMEOUT` - Request timeout in seconds (default: 30)
- `DATA_FOLDER` - Output directory (default: "data")
- `OUTPUT_PREFIX` - Filename prefix (default: "processed\_")
- `LOG_LEVEL` - Logging verbosity (default: "INFO")

## Learning Resources

The `docs/learning/prompts/` directory contains 12 progressive learning exercises designed to teach:

- Code walkthrough and refactoring (prompts 1-3)
- Automation and deployment (prompts 4-5)
- Dependencies, tooling, and testing (prompts 6-8)
- Error handling and configuration (prompts 9-10)
- Package management and CI/CD (prompts 11-12)

Each prompt guides creation of timestamped learning documents following the pattern: `docs/learning/YYYYMMDDHHMM-topic.md`

## Package Management

Uses `uv` for fast dependency resolution with `pyproject.toml` configuration:

- Core dependencies: `requests`, `python-dotenv`
- Dev dependencies: `ruff`, `pytest`, `pytest-cov`
- Python 3.8+ compatibility
- Note: The pyproject.toml has some malformed configuration sections that need fixing

## Output Structure

The application generates two types of files in the configured data folder:

- `{prefix}raw_{timestamp}.json` - Original API response data
- `{prefix}summary_{timestamp}.json` - Processed statistics including user counts, title length averages, and per-user item counts

## Known Issues

None currently identified. The template is ready for learning and development use.
