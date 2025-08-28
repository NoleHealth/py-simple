# Installation Guide

This document provides step-by-step instructions for setting up the py-simple project.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**: The project requires Python 3.8 or higher
- **Git**: For cloning the repository and version control

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

## Installation Steps

### 1. Install uv (Recommended)

`uv` is a fast Python package installer and resolver. It's the recommended tool for managing dependencies in this project.

#### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Alternative: Install via pip
```bash
pip install uv
```

#### Verify uv Installation
```bash
uv --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/py-simple.git
cd py-simple
```

### 3. Set Up Virtual Environment
```bash
# Create virtual environment using uv
make venv
# or manually:
uv venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 4. Install Dependencies

#### Production Dependencies Only
```bash
make install
# or manually:
uv pip install -e .
```

#### Development Dependencies (Recommended)
```bash
make install-dev
# or manually:
uv pip install -e ".[dev]"
```

### 5. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your settings (optional)
# The default values will work for the example API
```

### 6. Verify Installation
```bash
# Test the installation
make run
# or manually:
uv run python -m py_simple.main

# Run linting (optional)
make lint

# Run tests (optional)
make test
```

## Alternative Installation Methods

### Using pip (Traditional Method)
If you prefer not to use `uv`, you can install using traditional pip:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e .

# For development
pip install -e ".[dev]"
```

### Using Poetry
If you're already using Poetry in your workflow:

```bash
# First convert pyproject.toml to poetry format or create poetry.lock
poetry install
poetry run python -m py_simple.main
```

## IDE Setup

### VS Code
The project includes VS Code settings in `.vscode/settings.json` that will:
- Set the correct Python interpreter path
- Enable Black formatting on save
- Enable Ruff linting
- Configure code actions for import organization

#### Recommended VS Code Extensions
- Python (ms-python.python)
- Black Formatter (ms-python.black-formatter)
- Ruff (charliermarsh.ruff)

### Other IDEs
For other IDEs, configure:
- Python interpreter: `.venv/bin/python` (Linux/macOS) or `.venv\Scripts\python.exe` (Windows)
- Formatter: Black
- Linter: Ruff

## Troubleshooting

### Common Issues

#### uv command not found
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export PATH="$HOME/.cargo/bin:$PATH"

# Then reload your shell or run:
source ~/.bashrc  # or ~/.zshrc
```

#### Python version conflicts
```bash
# Specify Python version explicitly with uv
uv venv --python python3.9 .venv
# or
uv venv --python /path/to/python3.9 .venv
```

#### Permission issues on Windows
Run your terminal as Administrator when installing uv or creating virtual environments.

#### SSL certificate errors
```bash
# If you encounter SSL issues with uv
uv pip install --trusted-host pypi.org --trusted-host pypi.python.org -e .
```

### Getting Help

If you encounter issues:
1. Check the [troubleshooting section](#troubleshooting) above
2. Review the error messages carefully
3. Check that all prerequisites are installed correctly
4. Verify your Python version meets the requirements

## Next Steps

Once installation is complete, see:
- [Usage Guide](how-to-use.md) - Learn how to use the application
- [Git Commands](git-commands.md) - Git workflow for contributors