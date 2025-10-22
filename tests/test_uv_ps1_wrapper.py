"""Tests for uv_ps1_wrapper package."""

import argparse
import tempfile
from pathlib import Path

from uv_ps1_wrapper import generate_ps1_wrapper


def test_import():
    """Test that the package can be imported."""
    from uv_ps1_wrapper import generate_ps1_wrapper

    assert callable(generate_ps1_wrapper)


def test_generate_basic_wrapper():
    """Test generating a basic PowerShell wrapper."""
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input_file", type=Path, help="Input file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_script.ps1"
        script_path = Path(__file__).parent / "test_script.py"

        result = generate_ps1_wrapper(
            parser, script_path=script_path, output_path=output_path
        )

        assert result == output_path
        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "param(" in content
        # InputFile is positional argument, mapped as string
        assert "[string]$InputFile" in content
        assert "[switch]$Verbose" in content


def test_generate_wrapper_with_skip_dests():
    """Test generating wrapper with skip_dests parameter."""
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input_file", type=Path, help="Input file")
    parser.add_argument("--make-ps1", action="store_true", help="Generate PS1 wrapper")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_script.ps1"
        script_path = Path(__file__).parent / "test_script.py"

        result = generate_ps1_wrapper(
            parser,
            script_path=script_path,
            output_path=output_path,
            skip_dests={"make_ps1"},
        )

        assert result == output_path
        content = output_path.read_text(encoding="utf-8")
        assert "make-ps1" not in content.lower()
        assert "makeps1" not in content.lower()


def test_generate_wrapper_with_output_path():
    """Test generating wrapper with custom output_path."""
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input_file", type=Path)

    with tempfile.TemporaryDirectory() as tmpdir:
        custom_output = Path(tmpdir) / "custom_wrapper.ps1"
        script_path = Path(__file__).parent / "test_script.py"

        result = generate_ps1_wrapper(
            parser, script_path=script_path, output_path=custom_output
        )

        assert result == custom_output
        assert custom_output.exists()


def test_type_mapping():
    """Test Python to PowerShell type mapping."""
    parser = argparse.ArgumentParser(description="Test types")
    parser.add_argument("--count", type=int, help="Count")
    parser.add_argument("--rate", type=float, help="Rate")
    parser.add_argument("--path", type=Path, help="Path")
    parser.add_argument("--flag", action="store_true", help="Flag")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_types.ps1"
        script_path = Path(__file__).parent / "test_script.py"

        generate_ps1_wrapper(parser, script_path=script_path, output_path=output_path)

        content = output_path.read_text(encoding="utf-8")
        assert "[int]$Count" in content
        assert "[double]$Rate" in content
        # Path is mapped as string, not System.IO.FileInfo
        assert "[string]$Path" in content
        assert "[switch]$Flag" in content


def test_runner_parameter():
    """Test runner parameter (default is 'uv')."""
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input_file", type=Path)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_runner.ps1"
        script_path = Path(__file__).parent / "test_script.py"

        # Default runner should be 'uv'
        generate_ps1_wrapper(parser, script_path=script_path, output_path=output_path)

        content = output_path.read_text(encoding="utf-8")
        # Should contain direct script execution (not uv run --project)
        assert "uv" in content.lower()
        assert "Direct script mode" in content


def test_project_mode():
    """Test project mode with project_root and command_name."""
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input_file", type=Path)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_project.ps1"
        project_root = Path(tmpdir)
        script_path = project_root / "test_script.py"

        # Create a mock Python script
        script_path.write_text('print("test")', encoding="utf-8")

        # Create a mock pyproject.toml with [project.scripts] section
        pyproject_content = """
[project]
name = "test-project"
version = "0.1.2"

[project.scripts]
test-command = "test_module:main"
"""
        (project_root / "pyproject.toml").write_text(
            pyproject_content, encoding="utf-8"
        )

        generate_ps1_wrapper(
            parser,
            script_path=script_path,
            output_path=output_path,
            command_name="test-command",
        )

        content = output_path.read_text(encoding="utf-8")
        # Should use 'uv run --project' for project mode
        assert "uv run" in content
        assert "--project" in content
        assert "test-command" in content
        assert "test-command" in content
        assert "--project" in content


def test_cross_drive_paths():
    """Test handling of paths on different drives (Windows specific)."""
    parser = argparse.ArgumentParser(description="Test script")
    parser.add_argument("input_file", type=Path, help="Input file")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_cross_drive.ps1"
        script_path = Path(__file__).resolve()

        # Test direct script mode (no command_name) to avoid pyproject.toml validation
        # This tests the cross-drive path calculation in _calculate_script_relative_path
        generate_ps1_wrapper(
            parser,
            script_path=script_path,
            output_path=output_path,
            # No project_root or command_name - uses direct script mode
        )

        content = output_path.read_text(encoding="utf-8")
        # Should contain the script execution command
        assert '"run"' in content  # Check for "run" argument
        assert '& "uv"' in content  # Check for uv execution
        # Should handle path calculation gracefully
        assert "$ScriptPath" in content
