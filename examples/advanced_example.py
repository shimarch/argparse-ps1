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

try:
    from argparse_ps1_wrapper import generate_ps1_wrapper
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from argparse_ps1_wrapper import generate_ps1_wrapper


class LogLevel(Enum):
    """Log level enumeration."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Advanced file converter with multiple options")

    # Positional arguments
    parser.add_argument(
        "source",
        type=Path,
        help="Source file or directory",
    )

    parser.add_argument(
        "destination",
        type=Path,
        help="Destination file or directory",
    )

    # String option
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="json",
        choices=["json", "yaml", "xml", "csv"],
        help="Output format (default: json)",
    )

    # Integer option
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=4,
        help="Number of threads to use (default: 4)",
    )

    # Float option
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Timeout in seconds (default: 30.0)",
    )

    # Boolean flags
    parser.add_argument(
        "-r",
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
        type=Path,
        nargs="?",
        const=Path("."),
        default=None,
        metavar="OUTPUT_DIR",
        help="Generate PowerShell wrapper script and exit",
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
                skip_dests={"make_ps1"},
            )
            print(f"✓ Generated PowerShell wrapper: {output_path}")
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
