import numpy as np
import pytest
from blind_watermark.fft_core import (
    _old_shuffle,
    _shuffle_args,
    fft_encode,
    fft_decode,
)


def test_old_shuffle_is_permutation():
    x = list(range(20))
    _old_shuffle(x)
    assert sorted(x) == list(range(20))
    assert x != list(range(20))


def test_old_shuffle_deterministic():
    import random
    random.seed(42, version=1)
    x1 = list(range(20))
    _old_shuffle(x1)

    random.seed(42, version=1)
    x2 = list(range(20))
    _old_shuffle(x2)

    assert x1 == x2


def test_shuffle_args_oldseed_vs_default():
    m1, n1 = _shuffle_args(10, 10, seed=42, oldseed=True)
    m2, n2 = _shuffle_args(10, 10, seed=42, oldseed=False)
    assert m1 != m2 or n1 != n2


def test_fft_encode_decode_roundtrip(ori_img, wm_img):
    wm_3ch = np.stack([wm_img] * 3, axis=-1)

    encoded = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0)
    decoded = fft_decode(ori_img, encoded, seed=42, alpha=3.0)

    assert decoded.shape == ori_img.shape
    assert decoded.dtype == np.uint8
    decoded_region = decoded[:wm_3ch.shape[0], :wm_3ch.shape[1]]
    assert np.mean(np.abs(decoded_region.astype(float) - wm_3ch.astype(float))) < 100


def test_fft_encode_decode_wrong_seed_fails(ori_img, wm_img):
    wm_3ch = np.stack([wm_img] * 3, axis=-1)

    encoded = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0)
    decoded_wrong = fft_decode(ori_img, encoded, seed=99, alpha=3.0)

    decoded_region = decoded_wrong[:wm_3ch.shape[0], :wm_3ch.shape[1]]
    assert np.mean(np.abs(decoded_region.astype(float) - wm_3ch.astype(float))) > 80


def test_fft_encode_decode_oldseed_roundtrip(ori_img, wm_img):
    wm_3ch = np.stack([wm_img] * 3, axis=-1)

    encoded = fft_encode(ori_img, wm_3ch, seed=20160930, alpha=3.0, oldseed=True)
    decoded = fft_decode(ori_img, encoded, seed=20160930, alpha=3.0, oldseed=True)

    decoded_region = decoded[:wm_3ch.shape[0], :wm_3ch.shape[1]]
    assert np.mean(np.abs(decoded_region.astype(float) - wm_3ch.astype(float))) < 100


def test_fft_encode_watermark_too_large(ori_img):
    too_large = np.zeros((ori_img.shape[0], ori_img.shape[1], 3), dtype=np.uint8)
    with pytest.raises(AssertionError):
        fft_encode(ori_img, too_large, seed=42)


def test_fft_encode_rejects_watermark_wider_than_image(ori_img):
    too_wide = np.zeros((10, ori_img.shape[1] + 1, 3), dtype=np.uint8)
    with pytest.raises(AssertionError):
        fft_encode(ori_img, too_wide, seed=42)


def test_fft_encode_decode_legacy_roundtrip(ori_img, wm_img):
    """legacy=True 保持修复前的行为，encode→decode 自洽"""
    wm_3ch = np.stack([wm_img] * 3, axis=-1)
    encoded = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0, legacy=True)
    decoded = fft_decode(ori_img, encoded, seed=42, alpha=3.0, legacy=True)
    decoded_region = decoded[:wm_3ch.shape[0], :wm_3ch.shape[1]]
    assert np.mean(np.abs(decoded_region.astype(float) - wm_3ch.astype(float))) < 100


def test_fft_legacy_vs_nonlegacy_encode_differs(ori_img, wm_img):
    """legacy=False 与 legacy=True 应产生不同编码图像"""
    wm_3ch = np.stack([wm_img] * 3, axis=-1)
    enc_new = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0, legacy=False)
    enc_old = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0, legacy=True)
    assert not np.allclose(enc_new, enc_old), "两种模式应产生不同编码图像"


def test_fft_legacy_and_nonlegacy_extract_same_from_own_encoded(ori_img, wm_img):
    """legacy 与 non-legacy 各自编码后用自己的解码器，提取质量应一致"""
    wm_3ch = np.stack([wm_img] * 3, axis=-1)
    enc_new = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0, legacy=False)
    dec_new = fft_decode(ori_img, enc_new, seed=42, alpha=3.0, legacy=False)
    enc_old = fft_encode(ori_img, wm_3ch, seed=42, alpha=3.0, legacy=True)
    dec_old = fft_decode(ori_img, enc_old, seed=42, alpha=3.0, legacy=True)
    new_crop = dec_new[:wm_3ch.shape[0], :wm_3ch.shape[1]]
    old_crop = dec_old[:wm_3ch.shape[0], :wm_3ch.shape[1]]
    diff_new = np.mean(np.abs(new_crop.astype(float) - wm_3ch.astype(float)))
    diff_old = np.mean(np.abs(old_crop.astype(float) - wm_3ch.astype(float)))
    assert diff_new < 100
    assert diff_old < 100
    assert np.allclose(new_crop, old_crop, atol=1), (
        f"两种模式的提取结果应相同，diff_new={diff_new}, diff_old={diff_old}"
    )