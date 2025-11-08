# argparse-ps1 Project Setup

## Project Complete ✓

**argparse-ps1** is a Python library for generating PowerShell wrapper scripts from Python argparse parsers.

### Project Structure

```
argparse-ps1/
├── src/
│   └── argparse_ps1/
│       ├── __init__.py         # Package initialization
│       ├── argparse_ps1.py     # Core generator logic
│       └── py.typed            # Type marker for mypy/pyright
├── examples/
│   ├── basic_example.py        # Simple usage example
│   ├── example.py              # Complex usage example
│   ├── example_python.py       # Python runner example
│   ├── example_uv_project.py   # UV project mode example
│   └── README.md               # Examples documentation
├── tests/
│   ├── __init__.py             # Tests package
│   └── test_uv_ps1_wrapper.py  # Unit tests
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # GitHub Actions CI/CD
│   ├── copilot-instructions.md # This file
│   └── PUBLISHING.md           # Publishing guide
├── pyproject.toml              # Modern Python packaging config
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── DEVELOPMENT.md              # Development guide
├── .gitignore                  # Git ignore rules
└── .pre-commit-config.yaml     # Pre-commit hooks
```

### Features Implemented

- ✅ Core wrapper generation functionality (`argparse_ps1.py`)
- ✅ Type mapping (int, float, Path, bool, switch)
- ✅ Positional and optional argument support
- ✅ Boolean flag handling
- ✅ UV runner support with project mode
- ✅ Python direct execution mode
- ✅ MIT License with author Shimarch
- ✅ Comprehensive documentation with examples
- ✅ Modern Python packaging (src layout, Python 3.11+)
- ✅ Full type annotations with py.typed
- ✅ Unit tests with pytest
- ✅ GitHub Actions CI/CD workflow
- ✅ Development tools configuration (ruff, black, pyright)
- ✅ Pre-commit hooks
- ✅ Ready for GitHub and PyPI publication

### Quick Start

**Installation:**

```bash
pip install -e .
```

**Basic Usage:**

```python
from argparse_ps1 import generate_ps1_wrapper
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="My script")
parser.add_argument("input", type=Path)
parser.add_argument("-v", "--verbose", action="store_true")

output = generate_ps1_wrapper(
    parser,
    script_path=Path(__file__).resolve(),
    output_dir=Path(".")
)
```

### Development

**Install development dependencies:**

```bash
pip install -e ".[dev]"
```

**Run tests:**

```bash
pytest tests/ -v
```

**Type checking:**

```bash
pyright src/
```

**Linting:**

```bash
ruff check src/ tests/
```

### Next Steps for GitHub Publication

1. **Initialize Git repository:**

   ```bash
   git init
   git add .
   git commit -m "Initial commit: argparse-ps1 v0.1.5"
   ```

2. **Create GitHub repository:**

   - Go to https://github.com/new
   - Name: `argparse-ps1`
   - Description: "Generate PowerShell wrapper scripts from Python argparse parsers"
   - Public repository
   - Don't initialize with README (we have one)

3. **Push to GitHub:**

   ```bash
   git remote add origin https://github.com/shimarch/argparse-ps1.git
   git branch -M main
   git push -u origin main
   ```

4. **Publish to PyPI:**

   ```bash
   # Install build tools
   pip install build twine

   # Build the package
   python -m build

   # Upload to Test PyPI (optional, for testing)
   twine upload --repository testpypi dist/*

   # Upload to PyPI
   twine upload dist/*
   ```

5. **Run tests before publishing:**

   ```bash
   # Install test dependencies
   pip install -e ".[test]"

   # Run tests
   pytest tests/ -v
   ```

### Testing Examples

Run the example scripts to verify functionality:

```bash
cd examples
python basic_example.py --make-ps1
python example.py --make-ps1
```

### License

MIT License - Copyright (c) 2025 Shimarch
