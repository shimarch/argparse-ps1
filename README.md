# uv-ps1-wrapper# argparse-ps1-wrapper

**Generate PowerShell wrapper scripts for Python scripts executed with uv\*\***Generate PowerShell wrapper scripts from Python argparse parsers\*\*

[![PyPI version](https://badge.fury.io/py/uv-ps1-wrapper.svg)](https://badge.fury.io/py/uv-ps1-wrapper)[![PyPI version](https://badge.fury.io/py/argparse-ps1-wrapper.svg)](https://badge.fury.io/py/argparse-ps1-wrapper)

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![CI](https://github.com/shimarch/uv-ps1-wrapper/workflows/CI/badge.svg)](https://github.com/shimarch/uv-ps1-wrapper/actions)[![CI](https://github.com/shimarch/argparse-ps1-wrapper/workflows/CI/badge.svg)](https://github.com/shimarch/argparse-ps1-wrapper/actions)

`uv-ps1-wrapper` is a Python library that automatically generates PowerShell (.ps1) wrapper scripts for Python scripts that use `argparse` for command-line argument parsing. This allows users to interact with your Python scripts through a native PowerShell interface with proper parameter binding, tab completion, and help documentation.`argparse-ps1-wrapper` is a Python library that automatically generates PowerShell (.ps1) wrapper scripts for Python scripts that use `argparse` for command-line argument parsing. This allows users to interact with your Python scripts through a native PowerShell interface with proper parameter binding, tab completion, and help documentation.

The generated wrappers use `uv` as the Python runner, making them ideal for modern Python projects.## Features

## Features- 🚀 **Automatic Generation**: Generates PowerShell wrappers directly from `ArgumentParser` objects

- 🎯 **Type Mapping**: Automatically maps Python types to PowerShell parameter types

- 🚀 **Automatic Generation**: Generates PowerShell wrappers directly from `ArgumentParser` objects- 📝 **Native Interface**: Provides idiomatic PowerShell parameter names (PascalCase) and help text

- 🎯 **Type Mapping**: Automatically maps Python types to PowerShell parameter types- ⚙️ **Flexible**: Supports positional arguments, optional arguments, flags, and more

- 📝 **Native Interface**: Provides idiomatic PowerShell parameter names (PascalCase) and help text- 🎨 **Customizable**: Skip specific arguments or customize the output

- ⚙️ **Flexible**: Supports positional arguments, optional arguments, flags, and more- 🔧 **Zero Dependencies**: Uses only Python standard library

- 🎨 **Customizable**: Skip specific arguments or customize the output

- 🔧 **Zero Dependencies**: Uses only Python standard library## Installation

- ⚡ **uv Integration**: Designed for use with `uv` package manager

### From PyPI

## Installation

```bash

### From PyPIpip install argparse-ps1-wrapper

```

```bash

pip install uv-ps1-wrapper### From source

```

````bash

### From sourcegit clone https://github.com/shimarch/argparse-ps1-wrapper.git

cd argparse-ps1-wrapper

```bashpip install -e .

git clone https://github.com/shimarch/uv-ps1-wrapper.git```

cd uv-ps1-wrapper

pip install -e .## Quick Start

````

Here's a simple example of how to use `argparse-ps1-wrapper`:

## Quick Start

### Python Script (`my_script.py`)

Here's a simple example of how to use `uv-ps1-wrapper`:

````python

### Python Script (`my_script.py`)import argparse

from pathlib import Path

```pythonfrom argparse_ps1_wrapper import generate_ps1_wrapper

import argparse

from pathlib import Pathdef main():

from uv_ps1_wrapper import generate_ps1_wrapper    parser = argparse.ArgumentParser(

        description="Process some files"

def main():    )

    parser = argparse.ArgumentParser(    parser.add_argument(

        description="Process some files"        "input",

    )        type=Path,

    parser.add_argument("input_file", type=Path, help="Input file to process")        help="Input file to process"

    parser.add_argument("-o", "--output", type=Path, help="Output file")    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")    parser.add_argument(

    parser.add_argument("--make-ps1", action="store_true", help="Generate PowerShell wrapper")        "-o", "--output",

            type=Path,

    args = parser.parse_args()        help="Output file path"

        )

    if args.make_ps1:    parser.add_argument(

        output = generate_ps1_wrapper(        "-v", "--verbose",

            parser,        action="store_true",

            script_path=Path(__file__).resolve(),        help="Enable verbose output"

            skip_dests={"make_ps1"}    )

        )    parser.add_argument(

        print(f"Generated: {output}")        "--make-ps1",

        return        action="store_true",

            help="Generate PowerShell wrapper and exit"

    # Your script logic here    )

    print(f"Processing {args.input_file}")

    if args.verbose:    args = parser.parse_args()

        print("Verbose mode enabled")

    # Handle wrapper generation

if __name__ == "__main__":    if args.make_ps1:

    main()        output_path = generate_ps1_wrapper(

```            parser,

            script_path=Path(__file__).resolve(),

### Generate the Wrapper            skip_dests={"make_ps1"}

        )

```bash        print(f"Generated: {output_path}")

python my_script.py --make-ps1        return

````

    # Your script logic here

This creates `My-Script.ps1` in the same directory. print(f"Processing {args.input}")

    if args.verbose:

### Use the PowerShell Wrapper print("Verbose mode enabled")

````powershellif __name__ == "__main__":

.\My-Script.ps1 input.txt -Output output.txt -Verbose    main()

.\My-Script.ps1 -Help```

````

### Generate the Wrapper

## API Reference

```bash

### `generate_ps1_wrapper()`python my_script.py --make-ps1

```

````python

def generate_ps1_wrapper(This creates `my_script.ps1` with native PowerShell syntax.

    parser: argparse.ArgumentParser,

    *,### Use the Generated Wrapper

    script_path: Path,

    output_path: Path | None = None,```powershell

    output_dir: Path | None = None,# Run with PowerShell-style syntax

    skip_dests: Iterable[str] | None = None,.\my_script.ps1 -Input "data.txt" -Output "result.txt" -Verbose

    runner: str = "uv",

    project_root: Path | None = None,# Use positional arguments

    command_name: str | None = None,.\my_script.ps1 "data.txt"

) -> Path

```# Get help

Get-Help .\my_script.ps1

#### Parameters```



- **`parser`**: The `ArgumentParser` object to generate wrapper for## How It Works

- **`script_path`**: Absolute path to the Python script

- **`output_path`**: Output path for the .ps1 file (optional)1. **Parses ArgumentParser**: Extracts all arguments, options, and their metadata

- **`output_dir`**: Directory where .ps1 will be placed (default: script's directory)2. **Maps Types**: Converts Python types to PowerShell parameter types:

- **`skip_dests`**: Set of parameter destinations to skip in the wrapper   - `int` → `int`

- **`runner`**: Command to run Python (default: `"uv"`)   - `float` → `double`

- **`project_root`**: Path to project root (pyproject.toml location). If specified, uses `uv run --project` mode   - `Path`, `str` → `string`

- **`command_name`**: Command name registered in `[project.scripts]`. Required if `project_root` is specified   - `store_true`, `store_false` → `switch`

3. **Generates PowerShell**: Creates a native PowerShell script with proper parameter definitions

#### Returns4. **Handles Invocation**: The wrapper calls the Python script with the correct arguments



`Path` object pointing to the generated .ps1 file## API Reference



## Usage Modes### `generate_ps1_wrapper()`



### Direct Script Mode```python

def generate_ps1_wrapper(

The simplest mode - directly executes the Python script:    parser: argparse.ArgumentParser,

    *,

```python    script_path: Path,

generate_ps1_wrapper(    output_path: Path | None = None,

    parser,    output_dir: Path | None = None,

    script_path=Path(__file__).resolve(),    skip_dests: Iterable[str] | None = None,

)    runner: str = "uv",

```    project_root: Path | None = None,

    command_name: str | None = None,

Generated PowerShell wrapper will execute:) -> Path

```powershell```

& "uv" "C:\path\to\script.py" $Arguments

```Generate a PowerShell wrapper script for an argparse-based Python script.



### Project Mode**Parameters:**



For projects with `pyproject.toml` and registered commands:- `parser` (ArgumentParser): The ArgumentParser object from your Python script

- `script_path` (Path): Path to the Python script (absolute path)

```python- `output_path` (Path | None): Output path for the .ps1 file (optional)

generate_ps1_wrapper(- `output_dir` (Path | None): Directory where .ps1 will be placed (default: script's directory)

    parser,- `skip_dests` (Iterable[str] | None): Parameter destinations to skip in the wrapper

    script_path=Path(__file__).resolve(),- `runner` (str): Command to run Python (default: "uv")

    project_root=Path(__file__).parent.parent,- `project_root` (Path | None): Path to project root (pyproject.toml location). If specified, uses `--project` mode

    command_name="my-command",- `command_name` (str | None): Command name registered in `[project.scripts]`. Required if `project_root` is specified

)

```**Returns:**



Generated PowerShell wrapper will execute:- `Path`: Path to the generated .ps1 file

```powershell

& "uv" "run" "--project" $ProjectRoot "my-command" $Arguments**Modes:**

````

1. **Direct Script Mode** (default): Runs Python file directly

## Type Mapping ```python

generate_ps1_wrapper(parser, script_path=Path(**file**).resolve())

Python types are automatically mapped to PowerShell parameter types: ```

| Python Type | PowerShell Type |2. **Project Mode**: Uses `uv run --project` with registered command

|------------|----------------| ```python

| `Path` | `[System.IO.FileInfo]` | generate_ps1_wrapper(

| `int` | `[int]` | parser,

| `float` | `[double]` | script_path=Path(**file**).resolve(),

| `bool` / `action="store_true"` | `[switch]` | project_root=Path("/path/to/project"),

| Other | `[string]` | command_name="my-command"

)

## Examples ```

See the [`examples/`](examples/) directory for more detailed examples:## Examples

- [`basic_example.py`](examples/basic_example.py) - Simple wrapper generationSee the [`examples/`](examples/) directory for complete working examples:

- [`advanced_example.py`](examples/advanced_example.py) - Complex argument types

- [`basic_example.py`](examples/basic_example.py) - Simple file processor

## Development- [`advanced_example.py`](examples/advanced_example.py) - Complex script with multiple argument types

### Setup## Requirements

```bash- Python 3.11 or higher

git clone https://github.com/shimarch/uv-ps1-wrapper.git- No external dependencies

cd uv-ps1-wrapper

uv sync --all-extras## Development

```

### Setup development environment

### Run Tests

````bash

```bash# Clone the repository

uv run pytest tests/ -vgit clone https://github.com/shimarch/argparse-ps1-wrapper.git

```cd argparse-ps1-wrapper



### Run Tests with Coverage# Install with dev dependencies

pip install -e ".[dev]"

```bash```

uv run pytest tests/ --cov=uv_ps1_wrapper --cov-report=html

```### Run tests



### Format Code```bash

pytest tests/ -v

```bash```

uv tool run black .

uv tool run ruff check .### Run linting

````

````bash

## Licenseruff check src/ tests/

black --check src/ tests/

MIT License - Copyright (c) 2025 Shimarch```



## Contributing## Contributing



Contributions are welcome! Please feel free to submit a Pull Request.Contributions are welcome! Please feel free to submit a Pull Request.



## LinksFor detailed development instructions, including testing, publishing, and release procedures, see [DEVELOPMENT.md](DEVELOPMENT.md).



- **PyPI**: https://pypi.org/project/uv-ps1-wrapper/### Quick Start for Contributors

- **GitHub**: https://github.com/shimarch/uv-ps1-wrapper

- **Issues**: https://github.com/shimarch/uv-ps1-wrapper/issues1. Fork the repository

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
````
