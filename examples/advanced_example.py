#!/usr/bin/env python3"""Advanced example demonstrating multiple argument types.

"""Advanced example of using uv-ps1-wrapper.

This example shows how to handle:

This example demonstrates how to generate a PowerShell wrapper script- Multiple positional arguments

for a Python script with various argument types and options.- Various optional argument types

"""- Boolean flags

- Choices/enums

import argparse"""

from pathlib import Path

import argparse

# Try importing from installed package, fall back to development importimport sys

try:from enum import Enum

    from uv_ps1_wrapper import generate_ps1_wrapperfrom pathlib import Path

except ImportError:

    import systry:

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))    from argparse_ps1_wrapper import generate_ps1_wrapper

    from uv_ps1_wrapper import generate_ps1_wrapperexcept ImportError:

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    from argparse_ps1_wrapper import generate_ps1_wrapper

def main():

    """Main function demonstrating advanced wrapper generation."""

    parser = argparse.ArgumentParser(class LogLevel(Enum):

        description="Advanced script with multiple argument types",    """Log level enumeration."""

        epilog="Example: python advanced_example.py input.txt --count 10 --rate 0.5 --mode fast"

    )    DEBUG = "debug"

    INFO = "info"

    # Positional arguments    WARNING = "warning"

    parser.add_argument("input_file", type=Path, help="Input file to process")    ERROR = "error"

    parser.add_argument("output_dir", type=Path, nargs="?", default=Path("."), help="Output directory")



    # Optional arguments with various typesdef main() -> int:

    parser.add_argument("-c", "--count", type=int, default=1, help="Number of iterations")    """Main entry point."""

    parser.add_argument("-r", "--rate", type=float, default=1.0, help="Processing rate")    parser = argparse.ArgumentParser(

    parser.add_argument("-m", "--mode", choices=["fast", "normal", "thorough"], default="normal", help="Processing mode")        description="Advanced file converter with multiple options"

    )

    # Boolean flags

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")    # Positional arguments

    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")    parser.add_argument(

    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")        "source",

        type=Path,

    # File paths        help="Source file or directory",

    parser.add_argument("--config", type=Path, help="Configuration file")    )

    parser.add_argument("--log-file", type=Path, help="Log file path")

    parser.add_argument(

    # Wrapper generation flag        "destination",

    parser.add_argument("--make-ps1", action="store_true", help="Generate PowerShell wrapper script")        type=Path,

        help="Destination file or directory",

    args = parser.parse_args()    )



    if args.make_ps1:    # String option

        # Generate PowerShell wrapper script    parser.add_argument(

        output = generate_ps1_wrapper(        "-f",

            parser,        "--format",

            script_path=Path(__file__).resolve(),        type=str,

            skip_dests={"make_ps1"},        default="json",

        )        choices=["json", "yaml", "xml", "csv"],

        print(f"Generated PowerShell wrapper: {output}")        help="Output format (default: json)",

        return    )



    # Normal script logic here    # Integer option

    print(f"Processing: {args.input_file}")    parser.add_argument(

    print(f"Output directory: {args.output_dir}")        "-t",

    print(f"Count: {args.count}, Rate: {args.rate}, Mode: {args.mode}")        "--threads",

        type=int,

    if args.verbose:        default=4,

        print("Verbose mode enabled")        help="Number of threads to use (default: 4)",

    if args.quiet:    )

        print("Quiet mode enabled")

    if args.dry_run:    # Float option

        print("Dry run mode - no changes will be made")    parser.add_argument(

        "--timeout",

    if args.config:        type=float,

        print(f"Using config: {args.config}")        default=30.0,

    if args.log_file:        help="Timeout in seconds (default: 30.0)",

        print(f"Logging to: {args.log_file}")    )



    # Boolean flags

if __name__ == "__main__":    parser.add_argument(

    main()        "-r",

        "--recursive",
        action="store_true",
        help="Process directories recursively",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making changes",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files",
    )

    # Log level with choices
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Logging level (default: info)",
    )

    # Path option
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Configuration file path",
    )

    # PowerShell wrapper generation
    parser.add_argument(
        "--make-ps1",
        action="store_true",
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
            print(
                f"  .\\{output_path.name} -Source data/ -Destination output/ -Format yaml"
            )
            return 0
        except Exception as e:
            print(f"Error generating wrapper: {e}", file=sys.stderr)
            return 1

    # Display configuration
    print("Configuration:")
    print(f"  Source: {args.source}")
    print(f"  Destination: {args.destination}")
    print(f"  Format: {args.format}")
    print(f"  Threads: {args.threads}")
    print(f"  Timeout: {args.timeout}s")
    print(f"  Recursive: {args.recursive}")
    print(f"  Verbose: {args.verbose}")
    print(f"  Dry Run: {args.dry_run}")
    print(f"  Overwrite: {args.overwrite}")
    print(f"  Log Level: {args.log_level}")
    if args.config:
        print(f"  Config: {args.config}")

    # Your processing logic here
    if args.dry_run:
        print("\n[DRY RUN] No changes will be made")

    print("\n✓ Processing complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
