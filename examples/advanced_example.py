#!/usr/bin/env python3
"""Advanced example demonstrating multiple argument types.

This example shows how to handle:
- Multiple positional arguments
- Various optional argument types
- Boolean flags
- Choices/enums
"""

import argparse
import sys
from enum import Enum
from pathlib import Path

# Try importing from installed package, fall back to development import
try:
    from uv_ps1_wrapper import generate_ps1_wrapper
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from uv_ps1_wrapper import generate_ps1_wrapper


class LogLevel(Enum):
    """Log level enumeration."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Advanced file converter with multiple options"
    )

    # Positional arguments
    parser.add_argument(
        "input_file",
        type=Path,
        help="Input file to process",
    )

    parser.add_argument(
        "output_dir",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Output directory (default: current directory)",
    )

    # Optional arguments with various types
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="Number of iterations (default: 1)",
    )

    parser.add_argument(
        "-r",
        "--rate",
        type=float,
        default=1.0,
        help="Processing rate (default: 1.0)",
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=["fast", "normal", "thorough"],
        default="normal",
        help="Processing mode (default: normal)",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        choices=[level.value for level in LogLevel],
        default=LogLevel.INFO.value,
        help="Log level (default: info)",
    )

    # Boolean flags
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files",
    )

    # Special argument for wrapper generation
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

    # Configure logging level
    log_level = LogLevel(args.log_level)

    if args.verbose or log_level == LogLevel.DEBUG:
        print(f"Input file: {args.input_file}")
        print(f"Output directory: {args.output_dir}")
        print(f"Count: {args.count}")
        print(f"Rate: {args.rate}")
        print(f"Mode: {args.mode}")
        print(f"Log level: {log_level.value}")
        print(f"Dry run: {args.dry_run}")
        print(f"Force: {args.force}")

    # Validate input
    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        return 1

    # Create output directory if needed
    if not args.dry_run:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    # Simulate processing based on mode
    for i in range(args.count):
        if args.verbose:
            print(f"Processing iteration {i + 1}/{args.count}")

        # Determine output file name
        suffix = f"_processed_{args.mode}"
        if args.count > 1:
            suffix += f"_{i + 1}"

        output_file = (
            args.output_dir / f"{args.input_file.stem}{suffix}{args.input_file.suffix}"
        )

        if output_file.exists() and not args.force:
            if log_level.value in [LogLevel.INFO.value, LogLevel.DEBUG.value]:
                print(
                    f"Skipping {output_file} (already exists, use --force to overwrite)"
                )
            continue

        if args.dry_run:
            print(f"Would create: {output_file}")
        else:
            # Simulate different processing based on mode
            content = args.input_file.read_text(encoding="utf-8")

            if args.mode == "fast":
                processed_content = content.upper()
            elif args.mode == "thorough":
                processed_content = content.lower().replace(" ", "_")
            else:  # normal
                processed_content = content.title()

            output_file.write_text(processed_content, encoding="utf-8")

            if args.verbose:
                print(f"Created: {output_file}")

    if not args.dry_run:
        print(f"✅ Successfully processed {args.input_file}")
        print(f"   Output directory: {args.output_dir}")
        print(f"   Files created: {args.count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
