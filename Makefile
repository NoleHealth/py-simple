# Python Template Project Makefile
# Uses uv for fast Python package management

.PHONY: help venv activate install install-dev run test lint format build clean

# Default target
help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv:  ## Create virtual environment using uv
	uv venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

activate:  ## Activate virtual environment (source this in your shell)
	@echo "To activate the virtual environment, run:"
	@echo "  source .venv/bin/activate"
	@echo ""
	@echo "Or on Windows:"
	@echo "  .venv\\Scripts\\activate"

install:  ## Install project dependencies
	uv pip install -e .

install-dev:  ## Install development dependencies
	uv pip install -e ".[dev]"

build:  ## Build the project (syntax check)
	uv pip install -e .
	python -m py_compile py_simple/*.py

lint:  ## Run linter with auto-fix
	uv run ruff check --fix .
	uv run ruff format .

format:  ## Apply auto-formatting
	uv run ruff format .
	uv run ruff check --fix .

test:  ## Run tests
	uv run pytest tests/

run:  ## Run the main script
	uv run python -m py_simple.main

example:  ## Show example CLI usage
	@echo "Example commands to run the CLI:"
	@echo "  make run                    # Run with default settings"
	@echo "  API_URL=https://api.example.com make run  # Override API URL"
	@echo "  uv run python -m py_simple.main --help    # Show help"

clean:  ## Clean up build artifacts and cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Print actual commands that will be executed
print-commands:  ## Print the commands that make targets will execute
	@echo "Virtual environment setup:"
	@echo "  uv venv .venv"
	@echo ""
	@echo "Install dependencies:"
	@echo "  uv pip install -e ."
	@echo ""
	@echo "Lint and format:"
	@echo "  uv run ruff check --fix ."
	@echo "  uv run ruff format ."
	@echo ""
	@echo "Run main script:"
	@echo "  uv run python -m py_simple.main"