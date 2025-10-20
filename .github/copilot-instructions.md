# argparse-ps1-wrapper Project Setup

## Project Complete ✓

**argparse-ps1-wrapper** is a Python library for generating PowerShell wrapper scripts from Python argparse parsers.

### Project Structure

```
argparse-ps1-wrapper/
├── src/
│   └── argparse_ps1_wrapper/
│       ├── __init__.py         # Package initialization
│       └── ps1_wrapper.py      # Core generator logic
├── examples/
│   ├── basic_example.py        # Simple usage example
│   ├── advanced_example.py     # Complex usage example
│   └── README.md               # Examples documentation
├── tests/
│   ├── __init__.py             # Tests package
│   └── test_ps1_wrapper.py     # Unit tests
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # GitHub Actions CI/CD
│   └── copilot-instructions.md # This file
├── pyproject.toml              # Modern Python packaging config
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

### Features Implemented

- ✅ Core wrapper generation functionality (`ps1_wrapper.py`)
- ✅ Type mapping (int, float, Path, bool, switch)
- ✅ Positional and optional argument support
- ✅ Boolean flag handling
- ✅ MIT License with author Shimarch
- ✅ Comprehensive documentation with examples
- ✅ Modern Python packaging (src layout, Python 3.11+)
- ✅ Unit tests with pytest
- ✅ GitHub Actions CI/CD workflow
- ✅ Development tools configuration (ruff, black)
- ✅ Ready for GitHub and PyPI publication

### Quick Start

**Installation:**

```bash
pip install -e .
```

**Basic Usage:**

```python
from argparse_ps1_wrapper import generate_ps1_wrapper
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

### Next Steps for GitHub Publication

1. **Initialize Git repository:**

   ```bash
   git init
   git add .
   git commit -m "Initial commit: argparse-ps1-wrapper v0.1.0"
   ```

2. **Create GitHub repository:**

   - Go to https://github.com/new
   - Name: `argparse-ps1-wrapper`
   - Description: "Generate PowerShell wrapper scripts from Python argparse parsers"
   - Public repository
   - Don't initialize with README (we have one)

3. **Push to GitHub:**

   ```bash
   git remote add origin https://github.com/shimarch/argparse-ps1-wrapper.git
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
python advanced_example.py --make-ps1
```

### License

MIT License - Copyright (c) 2025 Shimarch
