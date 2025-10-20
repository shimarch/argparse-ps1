# argparse-ps1-wrapper

**Generate PowerShell wrapper scripts from Python argparse parsers**

[![PyPI version](https://badge.fury.io/py/argparse-ps1-wrapper.svg)](https://badge.fury.io/py/argparse-ps1-wrapper)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/shimarch/argparse-ps1-wrapper/workflows/CI/badge.svg)](https://github.com/shimarch/argparse-ps1-wrapper/actions)

`argparse-ps1-wrapper` is a Python library that automatically generates PowerShell (.ps1) wrapper scripts for Python scripts that use `argparse` for command-line argument parsing. This allows users to interact with your Python scripts through a native PowerShell interface with proper parameter binding, tab completion, and help documentation.

## Features

- 🚀 **Automatic Generation**: Generates PowerShell wrappers directly from `ArgumentParser` objects
- 🎯 **Type Mapping**: Automatically maps Python types to PowerShell parameter types
- 📝 **Native Interface**: Provides idiomatic PowerShell parameter names (PascalCase) and help text
- ⚙️ **Flexible**: Supports positional arguments, optional arguments, flags, and more
- 🎨 **Customizable**: Skip specific arguments or customize the output
- 🔧 **Zero Dependencies**: Uses only Python standard library

## Installation

### From PyPI

```bash
pip install argparse-ps1-wrapper
```

### From source

```bash
git clone https://github.com/shimarch/argparse-ps1-wrapper.git
cd argparse-ps1-wrapper
pip install -e .
```

## Quick Start

Here''s a simple example of how to use `argparse-ps1-wrapper`:

### Python Script (`my_script.py`)

```python
import argparse
from pathlib import Path
from argparse_ps1_wrapper import generate_ps1_wrapper

def main():
    parser = argparse.ArgumentParser(
        description="Process some files"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input file to process"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file path"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--make-ps1",
        type=Path,
        nargs="?",
        const=Path("."),
        default=None,
        help="Generate PowerShell wrapper and exit"
    )

    args = parser.parse_args()

    # Handle wrapper generation
    if args.make_ps1 is not None:
        output_path = generate_ps1_wrapper(
            parser,
            script_path=Path(__file__).resolve(),
            output_dir=args.make_ps1,
            skip_dests={"make_ps1"}  # Don''t include this arg in wrapper
        )
        print(f"Generated PowerShell wrapper: {output_path}")
        return

    # Your script logic here
    print(f"Processing {args.input}")
    if args.verbose:
        print("Verbose mode enabled")

if __name__ == "__main__":
    main()
```

### Generate the Wrapper

```bash
python my_script.py --make-ps1
```

This creates `my_script.ps1` with native PowerShell syntax.

### Use the Generated Wrapper

```powershell
# Run with PowerShell-style syntax
.\my_script.ps1 -Input "data.txt" -Output "result.txt" -Verbose

# Use positional arguments
.\my_script.ps1 "data.txt"

# Get help
Get-Help .\my_script.ps1
```

## How It Works

1. **Parses ArgumentParser**: Extracts all arguments, options, and their metadata
2. **Maps Types**: Converts Python types to PowerShell parameter types:
   - `int` → `int`
   - `float` → `double`
   - `Path`, `str` → `string`
   - `store_true`, `store_false` → `switch`
3. **Generates PowerShell**: Creates a native PowerShell script with proper parameter definitions
4. **Handles Invocation**: The wrapper calls the Python script with the correct arguments

## API Reference

### `generate_ps1_wrapper()`

```python
def generate_ps1_wrapper(
    parser: argparse.ArgumentParser,
    script_path: Path,
    output_dir: Path,
    *,
    skip_dests: set[str] | None = None,
) -> Path
```

Generate a PowerShell wrapper script for an argparse-based Python script.

**Parameters:**

- `parser` (ArgumentParser): The ArgumentParser object from your Python script
- `script_path` (Path): Path to the Python script to wrap
- `output_dir` (Path): Directory where the .ps1 file will be created
- `skip_dests` (set[str] | None): Set of argument destinations to skip in the wrapper

**Returns:**

- `Path`: Path to the generated .ps1 file

**Raises:**

- `ValueError`: If output_dir doesn''t exist or isn''t a directory

## Examples

See the [`examples/`](examples/) directory for complete working examples:

- [`basic_example.py`](examples/basic_example.py) - Simple file processor
- [`advanced_example.py`](examples/advanced_example.py) - Complex script with multiple argument types

## Requirements

- Python 3.11 or higher
- No external dependencies

## Development

### Setup development environment

```bash
# Clone the repository
git clone https://github.com/shimarch/argparse-ps1-wrapper.git
cd argparse-ps1-wrapper

# Install with dev dependencies
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/ -v
```

### Run linting

```bash
ruff check src/ tests/
black --check src/ tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For detailed development instructions, including testing, publishing, and release procedures, see [DEVELOPMENT.md](DEVELOPMENT.md).

### Quick Start for Contributors

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Shimarch**

## Acknowledgments

- Inspired by the need to provide native PowerShell interfaces to Python tools
- Built with Python''s `argparse` module

## Changelog

### 0.1.0 (2025-01-19)

- Initial release
- Basic wrapper generation functionality
- Support for positional and optional arguments
- Type mapping for common Python types
- Comprehensive test suite
- GitHub Actions CI/CD
