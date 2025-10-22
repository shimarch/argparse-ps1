#!/usr/bin/env python3
"""Example using python runner instead of uv.

This example demonstrates:
- Using runner="python"
- PATH-dependent python execution
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
    parser = argparse.ArgumentParser(description="Python runner example")

    parser.add_argument(
        "-o",
        "--option",
        type=str,
        help="String option argument",
    )

    parser.add_argument(
        "--make-ps1",
        action="store_true",
        help="Generate PowerShell wrapper script",
    )

    args = parser.parse_args()

    if args.make_ps1:
        # Generate PowerShell wrapper script using python runner
        output = generate_ps1_wrapper(
            parser,
            script_path=Path(__file__).resolve(),
            skip_dests={"make_ps1"},
            runner="python",  # Use python instead of uv
        )
        print(f"Generated PowerShell wrapper: {output}")
        return 0

    # Handle the option
    if args.option:
        print(f"Python runner - Option value: {args.option}")
    else:
        print(
            "Python runner - No option provided. Use --option <value> to set a value."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
