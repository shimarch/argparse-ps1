# uv-ps1-wrapper development Makefile

.PHONY: help install install-dev test test-cov lint format check pre-commit-install clean

# Default target
help:
	@echo "Available targets:"
	@echo "  install          Install package in development mode"
	@echo "  install-dev      Install package with development dependencies"
	@echo "  test            Run tests"
	@echo "  test-cov        Run tests with coverage"
	@echo "  lint            Run ruff linter"
	@echo "  format          Run black formatter and ruff formatter"
	@echo "  check           Run all checks (lint + format check)"
	@echo "  pre-commit-install  Install pre-commit hooks"
	@echo "  clean           Clean build artifacts"

# Install package in development mode
install:
	uv pip install -e .

# Install package with development dependencies
install-dev:
	uv pip install -e ".[dev]"

# Run tests
test:
	uv run pytest tests/ -v

# Run tests with coverage
test-cov:
	uv run pytest tests/ -v --cov=uv_ps1_wrapper --cov-report=term

# Run ruff linter
lint:
	uv run ruff check src/ tests/ examples/

# Run formatters
format:
	uv run black src/ tests/ examples/
	uv run ruff format src/ tests/ examples/

# Run all checks
check:
	uv run ruff check src/ tests/ examples/
	uv run black --check src/ tests/ examples/
	uv run ruff format --check src/ tests/ examples/

# Install pre-commit hooks
pre-commit-install:
	uv run pre-commit install

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
