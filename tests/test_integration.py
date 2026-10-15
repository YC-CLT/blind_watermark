import numpy as np
from blind_watermark import WaterMark


def test_embed_extract_str(ori_img, tmp_path):
    out_path = str(tmp_path / "embedded.png")
    bwm = WaterMark(password_img=1, password_wm=1)
    bwm.read_img(img=ori_img)
    text = "HelloWorld"
    bwm.read_wm(text, mode="str")
    bwm.embed(filename=out_path)

    bwm2 = WaterMark(password_img=1, password_wm=1)
    result = bwm2.extract(filename=out_path, wm_shape=len(bwm.wm_bit), mode="str")
    assert result == text


def test_embed_extract_str_custom_pwd(ori_img, tmp_path):
    out_path = str(tmp_path / "embedded_pwd.png")
    bwm = WaterMark(password_img=42, password_wm=99)
    bwm.read_img(img=ori_img)
    text = "CTF2026"
    bwm.read_wm(text, mode="str")
    bwm.embed(filename=out_path)

    bwm2 = WaterMark(password_img=42, password_wm=99)
    result = bwm2.extract(filename=out_path, wm_shape=len(bwm.wm_bit), mode="str")
    assert result == text


def test_embed_extract_bit(ori_img, tmp_path):
    out_path = str(tmp_path / "embedded_bit.png")
    bwm = WaterMark(password_img=1, password_wm=1)
    bwm.read_img(img=ori_img)
    bits = [True, False, True, True, False, True, False, False]
    bwm.read_wm(bits, mode="bit")
    bwm.embed(filename=out_path)

    bwm2 = WaterMark(password_img=1, password_wm=1)
    result = bwm2.extract(filename=out_path, wm_shape=len(bits), mode="bit")
    assert result.dtype == bool
    assert np.array_equal(result, np.array(bits))


def test_embed_extract_wrong_pwd_fails(ori_img, tmp_path):
    out_path = str(tmp_path / "embedded_wrong.png")
    bwm = WaterMark(password_img=1, password_wm=1)
    bwm.read_img(img=ori_img)
    text = "Secret"
    bwm.read_wm(text, mode="str")
    bwm.embed(filename=out_path)

    bwm2 = WaterMark(password_img=1, password_wm=999)
    result = bwm2.extract(filename=out_path, wm_shape=len(bwm.wm_bit), mode="str")
    assert result != text


def test_embed_extract_after_jpeg_compress(ori_img, tmp_path):
    out_path = str(tmp_path / "compressed.jpg")
    bwm = WaterMark(password_img=1, password_wm=1)
    bwm.read_img(img=ori_img)
    text = "Test"
    bwm.read_wm(text, mode="str")
    bwm.embed(filename=out_path, compression_ratio=90)

    bwm2 = WaterMark(password_img=1, password_wm=1)
    result = bwm2.extract(filename=out_path, wm_shape=len(bwm.wm_bit), mode="str")
    assert result == text