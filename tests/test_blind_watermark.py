from unittest.mock import patch
import numpy as np
import pytest
from blind_watermark import WaterMark


def test_read_wm_str(default_bwm):
    with patch.object(default_bwm.bwm_core, "read_wm"):
        default_bwm.read_wm("Hello", mode="str")
        assert default_bwm.wm_size > 0
        assert isinstance(default_bwm.wm_bit, np.ndarray)
        assert default_bwm.wm_bit.dtype == bool


def test_read_wm_bit(default_bwm):
    with patch.object(default_bwm.bwm_core, "read_wm"):
        bits = [True, False, True, True, False]
        default_bwm.read_wm(bits, mode="bit")
        assert default_bwm.wm_size == 5
        assert default_bwm.wm_bit.dtype == bool
        assert default_bwm.wm_bit.sum() == sum(bits)


def test_wm_size(default_bwm):
    with patch.object(default_bwm.bwm_core, "read_wm"):
        text = "Test123"
        default_bwm.read_wm(text, mode="str")
        assert default_bwm.wm_size == len(default_bwm.wm_bit)


def test_extract_decrypt_rearranges(default_bwm):
    default_bwm.wm_size = 10
    wm_avg = np.arange(10, dtype=float)
    result = default_bwm.extract_decrypt(wm_avg.copy())
    assert result.shape == (10,)
    # extract_decrypt rearranges elements using password seed
    assert set(result) == set(range(10))


def test_extract_decrypt_consistent(default_bwm):
    default_bwm.wm_size = 10
    wm_avg = np.arange(10, dtype=float)
    r1 = default_bwm.extract_decrypt(wm_avg.copy())
    r2 = default_bwm.extract_decrypt(wm_avg.copy())
    assert np.array_equal(r1, r2)


def test_invalid_mode_raises(default_bwm):
    with patch.object(default_bwm.bwm_core, "read_wm"):
        with pytest.raises(AssertionError):
            default_bwm.read_wm("test", mode="unknown")