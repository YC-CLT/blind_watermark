import cv2
import numpy as np
from blind_watermark.fft_watermark import WaterMarkFFT


def test_default_fft_seed(default_fft):
    assert default_fft.seed == 20160930
    assert default_fft.alpha == 3.0
    assert default_fft.oldseed is False
    assert default_fft.legacy is False


def test_watermarkfft_custom_params():
    bwm = WaterMarkFFT(seed=12345, alpha=5.0, oldseed=True, legacy=True)
    assert bwm.seed == 12345
    assert bwm.alpha == 5.0
    assert bwm.oldseed is True
    assert bwm.legacy is True


def test_encode_decode_file_roundtrip(default_fft, fft_ori_img, fft_wm_img, tmp_path):
    ori_path = tmp_path / "ori.png"
    wm_path = tmp_path / "wm.png"
    out_path = tmp_path / "out.png"
    extracted_path = tmp_path / "extracted.png"

    cv2.imwrite(str(ori_path), fft_ori_img)
    cv2.imwrite(str(wm_path), fft_wm_img)

    default_fft.encode(str(ori_path), str(wm_path), str(out_path))
    assert out_path.exists()

    default_fft.decode(str(ori_path), str(out_path), str(extracted_path))
    assert extracted_path.exists()

    result = cv2.imread(str(extracted_path))
    assert result is not None
    assert result.shape == fft_ori_img.shape

    result_crop = result[:fft_wm_img.shape[0], :fft_wm_img.shape[1]]
    assert np.mean(np.abs(result_crop.astype(float) - fft_wm_img.astype(float))) < 150


def test_encode_decode_file_legacy_roundtrip(fft_ori_img, fft_wm_img, tmp_path):
    """legacy=True 文件级 roundtrip 自洽"""
    bwm = WaterMarkFFT(seed=20160930, alpha=3.0, legacy=True)
    ori_path = tmp_path / "ori.png"
    wm_path = tmp_path / "wm.png"
    out_path = tmp_path / "out.png"
    extracted_path = tmp_path / "extracted.png"

    cv2.imwrite(str(ori_path), fft_ori_img)
    cv2.imwrite(str(wm_path), fft_wm_img)

    bwm.encode(str(ori_path), str(wm_path), str(out_path))
    assert out_path.exists()

    bwm.decode(str(ori_path), str(out_path), str(extracted_path))
    assert extracted_path.exists()

    result = cv2.imread(str(extracted_path))
    result_crop = result[:fft_wm_img.shape[0], :fft_wm_img.shape[1]]
    assert np.mean(np.abs(result_crop.astype(float) - fft_wm_img.astype(float))) < 150


def test_encode_file_not_found(default_fft, tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError, match="can't find"):
        default_fft.encode("nonexistent.png", "nonexistent_wm.png", str(tmp_path / "out.png"))


def test_decode_file_not_found(default_fft, fft_ori_img, tmp_path):
    import pytest
    ori_path = tmp_path / "ori.png"
    cv2.imwrite(str(ori_path), fft_ori_img)
    with pytest.raises(FileNotFoundError, match="can't find"):
        default_fft.decode(str(ori_path), "nonexistent.png", str(tmp_path / "out.png"))


def test_encode_arr_decode_arr_roundtrip(default_fft, fft_ori_img, fft_wm_img):
    encoded = default_fft.encode_arr(fft_ori_img, fft_wm_img)
    assert encoded.shape == fft_ori_img.shape
    assert encoded.dtype == np.uint8

    decoded = default_fft.decode_arr(fft_ori_img, encoded)
    assert decoded.shape == fft_ori_img.shape

    decoded_crop = decoded[:fft_wm_img.shape[0], :fft_wm_img.shape[1]]
    assert np.mean(np.abs(decoded_crop.astype(float) - fft_wm_img.astype(float))) < 150


def test_encode_arr_decode_arr_legacy_roundtrip(fft_ori_img, fft_wm_img):
    """legacy=True arr 级 roundtrip 自洽"""
    bwm = WaterMarkFFT(seed=20160930, alpha=3.0, legacy=True)
    encoded = bwm.encode_arr(fft_ori_img, fft_wm_img)
    decoded = bwm.decode_arr(fft_ori_img, encoded)
    decoded_crop = decoded[:fft_wm_img.shape[0], :fft_wm_img.shape[1]]
    assert np.mean(np.abs(decoded_crop.astype(float) - fft_wm_img.astype(float))) < 150


def test_different_seed_no_recovery(fft_ori_img, fft_wm_img):
    bwm1 = WaterMarkFFT(seed=42)
    bwm2 = WaterMarkFFT(seed=99)

    encoded = bwm1.encode_arr(fft_ori_img, fft_wm_img)
    decoded = bwm2.decode_arr(fft_ori_img, encoded)

    decoded_crop = decoded[:fft_wm_img.shape[0], :fft_wm_img.shape[1]]
    diff = np.mean(np.abs(decoded_crop.astype(float) - fft_wm_img.astype(float)))
    assert diff > 80, f"Expected large difference, got {diff}"


def test_legacy_vs_nonlegacy_encode_differs(fft_ori_img, fft_wm_img):
    """legacy=False 与 legacy=True 应产生不同编码图像"""
    bwm_new = WaterMarkFFT(seed=42, alpha=3.0, legacy=False)
    bwm_old = WaterMarkFFT(seed=42, alpha=3.0, legacy=True)
    enc_new = bwm_new.encode_arr(fft_ori_img, fft_wm_img)
    enc_old = bwm_old.encode_arr(fft_ori_img, fft_wm_img)
    assert not np.allclose(enc_new, enc_old), "两种模式应产生不同编码图像"