# Examples

This directory contains example scripts demonstrating how to use `uv-ps1-wrapper`.

## Basic Example

[`basic_example.py`](basic_example.py) - A simple file processor that converts text to uppercase.

**Usage:**

```bash
# Run the Python script
python basic_example.py input.txt

# With options
python basic_example.py input.txt -o output.txt -v

# Generate PowerShell wrapper
python basic_example.py --make-ps1

# Use the generated PowerShell wrapper
.\basic_example.ps1 -Input input.txt -Verbose
```

## Advanced Example

[`advanced_example.py`](advanced_example.py) - A more complex script demonstrating:

- Optional Path arguments- Multiple positional arguments

- Various option types (string, int, float, path)

Run with:- Boolean flags

````bash- Choices/enums

python advanced_example.py --make-ps1

```**Usage:**



This generates `Advanced-Example.ps1` for PowerShell use:```bash

```powershell# Run the Python script

.\Advanced-Example.ps1 input.txt -Count 10 -Rate 0.5 -Mode fast -Verbosepython advanced_example.py source.txt dest.txt

````

# With many options

## Development Modepython advanced_example.py source.txt dest.txt -f yaml -t 8 --timeout 60.0 -r -v

Both examples include fallback imports for development:# Generate PowerShell wrapper

````pythonpython advanced_example.py --make-ps1

try:

    from uv_ps1_wrapper import generate_ps1_wrapper# Use the generated PowerShell wrapper

except ImportError:.\advanced_example.ps1 -Source source.txt -Destination dest.txt -Format yaml -Threads 8 -Recursive -Verbose

    import sys```

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    from uv_ps1_wrapper import generate_ps1_wrapper## Running Examples

````

1. **Install ps1-wrapper** (if not already installed):

This allows testing without installing the package.

```bash
pip install -e ..
```

2. **Create a test file**:

   ```bash
   echo "hello world" > test.txt
   ```

3. **Run basic example**:

   ```bash
   python basic_example.py test.txt
   ```

4. **Generate wrapper**:

   ```bash
   python basic_example.py --make-ps1
   ```

5. **Use the wrapper** (in PowerShell):
   ```powershell
   .\basic_example.ps1 -Input test.txt
   ```
