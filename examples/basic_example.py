#!/usr/bin/env python3"""Basic example of argparse-ps1-wrapper usage.

"""Basic example of using uv-ps1-wrapper.

This example demonstrates:

This example demonstrates how to generate a PowerShell wrapper script- Simple argument parsing with argparse

for a simple Python script with basic argument types.- Generating a PowerShell wrapper script

"""- Using positional and optional arguments

"""

import argparse

from pathlib import Pathimport argparse

import sys

# Try importing from installed package, fall back to development importfrom pathlib import Path

try:

    from uv_ps1_wrapper import generate_ps1_wrappertry:

except ImportError:    from argparse_ps1_wrapper import generate_ps1_wrapper

    import sysexcept ImportError:

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))    # If running from examples directory before installation

    from uv_ps1_wrapper import generate_ps1_wrapper    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    from argparse_ps1_wrapper import generate_ps1_wrapper



def main():

    """Main function demonstrating basic wrapper generation."""def main() -> int:

    parser = argparse.ArgumentParser(description="Process a file with optional verbosity")    """Main entry point."""

    parser.add_argument("input_file", type=Path, help="Input file to process")    parser = argparse.ArgumentParser(

    parser.add_argument("-o", "--output", type=Path, help="Output file path")        description="Process text files by converting them to uppercase"

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")    )

    parser.add_argument("--make-ps1", action="store_true", help="Generate PowerShell wrapper script")

    parser.add_argument(

    args = parser.parse_args()        "input",

        type=Path,

    if args.make_ps1:        help="Input text file to process",

        # Generate PowerShell wrapper script    )

        output = generate_ps1_wrapper(

            parser,    parser.add_argument(

            script_path=Path(__file__).resolve(),        "-o",

            skip_dests={"make_ps1"},  # Skip the --make-ps1 argument itself        "--output",

        )        type=Path,

        print(f"Generated PowerShell wrapper: {output}")        help="Output file path (optional)",

        return    )



    # Normal script logic here    parser.add_argument(

    print(f"Processing file: {args.input_file}")        "-v",

    if args.output:        "--verbose",

        print(f"Output to: {args.output}")        action="store_true",

    if args.verbose:        help="Enable verbose output",

        print("Verbose mode enabled")    )



    parser.add_argument(

if __name__ == "__main__":        "--make-ps1",

    main()        action="store_true",

        help="Generate PowerShell wrapper script and exit",
    )

    args = parser.parse_args()

    # Handle wrapper generation
    if args.make_ps1:
        try:
            output_path = generate_ps1_wrapper(
                parser,
                script_path=Path(__file__).resolve(),
                skip_dests={"make_ps1"},
            )
            print(f"✅ Generated PowerShell wrapper: {output_path}")
            print(f"\nUsage:")
            print(f"  .\\{output_path.name} -Input data.txt")
            print(
                f"  .\\{output_path.name} -Input data.txt -Output result.txt -Verbose"
            )
            return 0
        except Exception as e:
            print(f"Error generating wrapper: {e}", file=sys.stderr)
            return 1

    # Normal processing
    if args.verbose:
        print(f"Processing file: {args.input}")

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1

    # Example processing
    content = args.input.read_text(encoding="utf-8")
    lines = content.splitlines()

    if args.verbose:
        print(f"Read {len(lines)} lines")

    # Determine output
    if args.output is None:
        output_file = args.input.with_stem(f"{args.input.stem}_processed")
    else:
        output_file = args.output

    if args.verbose:
        print(f"Writing output to: {output_file}")

    # Write output (uppercase conversion)
    output_content = "\n".join(line.upper() for line in lines)
    output_file.write_text(output_content, encoding="utf-8")

    print(f"✅ Successfully processed {args.input} → {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
