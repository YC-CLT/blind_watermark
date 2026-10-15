import re
from blind_watermark.version import __version__, bw_notes


def test_version_format():
    assert re.match(r"^\d+\.\d+\.\d+", __version__), f"Invalid semver: {__version__}"


def test_bw_notes_close():
    bw_notes.close()
    assert bw_notes.show is False