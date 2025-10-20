"""Basic example of using ps1-wrapper.

This script demonstrates how to create a simple file processor
with PowerShell wrapper generation capability.
"""

import argparse
import sys
from pathlib import Path

# Import ps1_wrapper - adjust import path as needed
try:
    from argparse_ps1_wrapper import generate_ps1_wrapper
except ImportError:
    # If running from examples directory before installation
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from argparse_ps1_wrapper import generate_ps1_wrapper


def process_file(input_file: Path, output_file: Path | None, verbose: bool) -> None:
    """Process a file (example logic).

    Args:
        input_file: Input file path
        output_file: Output file path (optional)
        verbose: Whether to print verbose output
    """
    if verbose:
        print(f"Processing file: {input_file}")

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Example processing
    content = input_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    if verbose:
        print(f"Read {len(lines)} lines from {input_file}")

    # Determine output
    if output_file is None:
        output_file = input_file.with_stem(f"{input_file.stem}_processed")

    if verbose:
        print(f"Writing output to: {output_file}")

    # Write output (in this example, just uppercase)
    output_content = "\n".join(line.upper() for line in lines)
    output_file.write_text(output_content, encoding="utf-8")

    print(f"✓ Successfully processed {input_file} → {output_file}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Process text files by converting them to uppercase")

    parser.add_argument(
        "input",
        type=Path,
        help="Input text file to process",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: input_processed.txt)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--make-ps1",
        type=Path,
        nargs="?",
        const=Path("."),
        default=None,
        metavar="OUTPUT_DIR",
        help="Generate PowerShell wrapper script and exit (default: current directory)",
    )

    args = parser.parse_args()

    # Handle wrapper generation
    if args.make_ps1 is not None:
        output_dir = args.make_ps1.resolve()

        if not output_dir.exists():
            print(f"Error: Output directory does not exist: {output_dir}", file=sys.stderr)
            return 1

        if not output_dir.is_dir():
            print(f"Error: Output path is not a directory: {output_dir}", file=sys.stderr)
            return 1

        try:
            output_path = generate_ps1_wrapper(
                parser,
                script_path=Path(__file__).resolve(),
                output_dir=output_dir,
                skip_dests={"make_ps1"},  # Don't include --make-ps1 in wrapper
            )
            print(f"✓ Generated PowerShell wrapper: {output_path}")
            return 0
        except Exception as e:
            print(f"Error generating wrapper: {e}", file=sys.stderr)
            return 1

    # Normal processing
    try:
        process_file(args.input, args.output, args.verbose)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
