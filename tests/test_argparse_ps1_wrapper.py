"""Tests for argparse_ps1_wrapper.py module."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import pytest


def test_import():
    """Test that the package can be imported."""
    from argparse_ps1_wrapper import generate_ps1_wrapper

    assert callable(generate_ps1_wrapper)


def test_generate_basic_wrapper():
    """Test generating a basic PowerShell wrapper."""
    from argparse_ps1_wrapper import generate_ps1_wrapper

    # Create a simple parser
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input", type=Path, help="Input file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "test_script.py"
        script_path.write_text("# Test script", encoding="utf-8")

        output_dir = Path(tmpdir)
        ps1_path = generate_ps1_wrapper(parser, script_path, output_dir)

        # Check that the file was created
        assert ps1_path.exists()
        assert ps1_path.suffix == ".ps1"

        # Check that the content includes expected elements
        content = ps1_path.read_text(encoding="utf-8")
        assert "[CmdletBinding()]" in content
        assert "param(" in content
        assert "$Input" in content or "$input" in content.lower()
        assert "$Verbose" in content or "$verbose" in content.lower()


def test_generate_wrapper_with_skip_dests():
    """Test generating wrapper with skipped arguments."""
    from argparse_ps1_wrapper import generate_ps1_wrapper

    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--make-ps1", type=Path, nargs="?", const=Path("."))

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "test.py"
        script_path.write_text("# Test", encoding="utf-8")

        ps1_path = generate_ps1_wrapper(
            parser, script_path, Path(tmpdir), skip_dests={"make_ps1"}
        )

        content = ps1_path.read_text(encoding="utf-8")
        # make_ps1 should not be in the generated script
        assert "make-ps1" not in content.lower() or "makeps1" not in content.lower()


def test_generate_wrapper_invalid_output_dir():
    """Test that invalid output directory raises ValueError."""
    from argparse_ps1_wrapper import generate_ps1_wrapper

    parser = argparse.ArgumentParser()
    parser.add_argument("input")

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "test.py"
        script_path.write_text("# Test", encoding="utf-8")

        # Non-existent directory
        with pytest.raises(ValueError, match="does not exist"):
            generate_ps1_wrapper(parser, script_path, Path(tmpdir) / "nonexistent")

        # File instead of directory
        file_path = Path(tmpdir) / "file.txt"
        file_path.write_text("test", encoding="utf-8")
        with pytest.raises(ValueError, match="not a directory"):
            generate_ps1_wrapper(parser, script_path, file_path)


def test_type_mapping():
    """Test that Python types are correctly mapped to PowerShell types."""
    from argparse_ps1_wrapper import generate_ps1_wrapper

    parser = argparse.ArgumentParser()
    parser.add_argument("--int-arg", type=int)
    parser.add_argument("--float-arg", type=float)
    parser.add_argument("--path-arg", type=Path)
    parser.add_argument("--flag", action="store_true")

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "test.py"
        script_path.write_text("# Test", encoding="utf-8")

        ps1_path = generate_ps1_wrapper(parser, script_path, Path(tmpdir))
        content = ps1_path.read_text(encoding="utf-8")

        # Check type mappings
        assert "[int]" in content
        assert "[double]" in content or "[float]" in content
        assert "[string]" in content
        assert "[switch]" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
