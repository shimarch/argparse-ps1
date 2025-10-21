#!/usr/bin/env python3
"""Basic example of uv-ps1-wrapper usage.

This example demonstrates:
- Simple argument parsing with argparse
- Generating a PowerShell wrapper script
- Using positional and optional arguments
"""

import argparse
import sys
from pathlib import Path

# Try importing from installed package, fall back to development import
try:
    from uv_ps1_wrapper import generate_ps1_wrapper
except ImportError:
    # If running from examples directory before installation
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from uv_ps1_wrapper import generate_ps1_wrapper


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process text files by converting them to uppercase"
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input text file to process",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path (default: input_uppercase.txt)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--make-ps1",
        action="store_true",
        help="Generate PowerShell wrapper script",
    )

    args = parser.parse_args()

    if args.make_ps1:
        # Generate PowerShell wrapper script
        output = generate_ps1_wrapper(
            parser,
            script_path=Path(__file__).resolve(),
            skip_dests={"make_ps1"},  # Skip the --make-ps1 argument itself
        )
        print(f"Generated PowerShell wrapper: {output}")
        return 0

    # Process the file
    if args.verbose:
        print(f"Processing file: {args.input}")

    try:
        content = args.input.read_text(encoding="utf-8")
        uppercase_content = content.upper()

        if args.output:
            output_path = args.output
        else:
            output_path = args.input.with_suffix(".uppercase" + args.input.suffix)

        output_path.write_text(uppercase_content, encoding="utf-8")

        if args.verbose:
            print(f"Wrote output to: {output_path}")
        else:
            print(str(output_path))

        return 0

    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
