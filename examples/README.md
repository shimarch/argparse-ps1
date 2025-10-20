# Examples

This directory contains example scripts demonstrating how to use `ps1-wrapper`.

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

- Multiple positional arguments
- Various option types (string, int, float, path)
- Boolean flags
- Choices/enums

**Usage:**

```bash
# Run the Python script
python advanced_example.py source.txt dest.txt

# With many options
python advanced_example.py source.txt dest.txt -f yaml -t 8 --timeout 60.0 -r -v

# Generate PowerShell wrapper
python advanced_example.py --make-ps1

# Use the generated PowerShell wrapper
.\advanced_example.ps1 -Source source.txt -Destination dest.txt -Format yaml -Threads 8 -Recursive -Verbose
```

## Running Examples

1. **Install ps1-wrapper** (if not already installed):

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
