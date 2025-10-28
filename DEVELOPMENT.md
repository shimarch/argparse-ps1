# Development Guide

This document provides detailed instructions for developing and publishing the `argparse-ps1` package using modern Python tooling with `uv`.

## Development Setup

### 1. Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Python 3.11+ (uv will manage Python versions for you)

### 2. Environment Setup

```bash
# Clone the repository
git clone https://github.com/shimarch/argparse-ps1.git
cd argparse-ps1

# Install in development mode with dependencies
uv sync --all-extras
```

### 3. Type Information

This package includes type annotations and a `py.typed` file to support static type checking with tools like Pylance, mypy, and other type checkers.

**Type checker setup:**

- The package is marked as typed with `py.typed` file
- VS Code/Pylance configuration is included in `.vscode/settings.json`
- Package metadata includes `"Typing :: Typed"` classifier

**Resolving type stub warnings:**

If you see "stub file not found" warnings in Pylance:

1. Ensure the package is installed in development mode: `uv pip install -e .`
2. Restart VS Code language server: `Ctrl+Shift+P` → "Python: Restart Language Server"
3. Check that `py.typed` exists in `src/argparse_ps1/`

### 4. Running Tests

```bash
# Run all tests
uv run python -m pytest tests/ -v

# Run tests with coverage
uv run python -m pytest tests/ -v --cov=argparse_ps1 --cov-report=html

# Run specific test
uv run python -m pytest tests/test_argparse_ps1.py::test_import -v

# Run tests with coverage report
uv run python -m pytest tests/ -v --cov=argparse_ps1 --cov-report=term
```

### 4. Code Quality

Code quality checks are automatically enforced by pre-commit hooks. You can also run them manually:

```bash
# Format code with black
uv run black src tests examples

# Lint with ruff
uv run ruff check src tests examples

# Fix linting issues automatically
uv run ruff check --fix src tests examples

# Format with ruff
uv run ruff format src tests examples

# Run all checks
uv run ruff check src tests examples
uv run black --check src tests examples
uv run ruff format --check src tests examples
```

_Note: These checks run automatically on every commit via pre-commit hooks._

## Pre-commit Hooks

Pre-commit hooks ensure code quality before each commit by automatically running formatters and linters.

```bash
# Install pre-commit hooks (one-time setup)
uv run pre-commit install

# Run pre-commit on all files manually
uv run pre-commit run --all-files

# Pre-commit hooks will automatically run on each git commit
# If hooks fail, fix the issues and commit again
```

## Version Management and Publishing

### 1. Version Update Process

When ready to release a new version:

1. **Update version in `pyproject.toml`**:

   ```toml
   [project]
   name = "argparse-ps1"
   version = "0.1.3"  # Increment version following semantic versioning
   ```

2. **Update version in source code** (if applicable):

   ```python
   # In src/argparse_ps1/__init__.py
   __version__ = "0.1.3"
   ```

### 2. Daily Development Workflow

#### Push to Main Branch (Automatic TestPyPI Publishing)

```bash
# After making changes and updating version
git add .
git commit -m "Bump version to 0.1.3 and add new features"
git push origin main
```

**Result**: GitHub Actions automatically publishes to TestPyPI for testing.

#### Create Release Tag (Automatic PyPI Publishing)

```bash
# Create and push a version tag for production release
git tag v0.1.3
git push origin v0.1.3
```

**Result**: GitHub Actions automatically publishes to production PyPI.

### 3. Package Verification

#### Check TestPyPI Installation

```bash
# Test installation from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ argparse-ps1

# Verify functionality
python -c "from argparse_ps1 import generate_ps1_wrapper; print('TestPyPI installation successful!')"
```

#### Check PyPI Installation

```bash
# Check if package is available on PyPI
uv pip install argparse-ps1

# Verify installation
python -c "from argparse_ps1 import generate_ps1_wrapper; print('PyPI installation successful!')"

# Check package information
pip show argparse-ps1
```

### 4. Build and Test Locally

```bash
# Clean and build package
uv build --clean

# Check distribution quality
uv run twine check dist/*

# Test wheel contents
python -m zipfile -l dist/*.whl

# Manual upload to TestPyPI (if needed)
uv run twine upload --repository testpypi dist/*

# Manual upload to PyPI (if needed)
uv run twine upload dist/*
```

## Clean Build Artifacts

Clean build artifacts when you encounter build issues or need a fresh build environment.

**When to clean:**

- Build errors or inconsistent builds
- When switching between development and production builds
- After making changes to `pyproject.toml`
- Troubleshooting import or packaging issues

```bash
# Clean all build artifacts
rm -rf build/ dist/ *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```
