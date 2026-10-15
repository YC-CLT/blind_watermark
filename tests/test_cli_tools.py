import subprocess
import pytest
from blind_watermark.cli_tools import _parse_shape


def test_parse_shape_single():
    assert _parse_shape("64") == 64


def test_parse_shape_tuple():
    assert _parse_shape("64,64") == (64, 64)


def test_parse_shape_invalid():
    with pytest.raises((ValueError, SystemExit)):
        _parse_shape("a,b")


def test_cli_help():
    result = subprocess.run(
        ["uv", "run", "blind_watermark", "--help"],
        cwd=".", capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "embed" in result.stdout
    assert "extract" in result.stdout


def test_cli_version():
    result = subprocess.run(
        ["uv", "run", "blind_watermark", "--version"],
        cwd=".", capture_output=True, text=True,
    )
    assert result.returncode == 0