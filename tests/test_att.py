import numpy as np
from blind_watermark import att


def test_cut_att3(ori_img, tmp_path):
    h, w = ori_img.shape[:2]
    loc = (10, 10, w - 10, h - 10)
    out = att.cut_att3(input_img=ori_img, loc=loc)
    assert out.shape[0] == h - 20
    assert out.shape[1] == w - 20


def test_cut_att3_with_scale(ori_img, tmp_path):
    h, w = ori_img.shape[:2]
    loc = (10, 10, w - 10, h - 10)
    out = att.cut_att3(input_img=ori_img, loc=loc, scale=0.5)
    expected_h = round((h - 20) * 0.5)
    expected_w = round((w - 20) * 0.5)
    assert out.shape[0] == expected_h
    assert out.shape[1] == expected_w


def test_cut_att3_from_file(ori_img, test_image_path, tmp_path):
    out_path = str(tmp_path / "cut_test.jpg")
    h, w = ori_img.shape[:2]
    out = att.cut_att3(input_filename=test_image_path, output_file_name=out_path,
                       loc=(10, 10, w - 10, h - 10))
    assert out.shape[0] == h - 20
    assert out.shape[1] == w - 20


def test_resize_att(ori_img, tmp_path):
    out = att.resize_att(input_img=ori_img, out_shape=(200, 200))
    assert out.shape[:2] == (200, 200)


def test_bright_att(ori_img):
    out_bright = att.bright_att(input_img=ori_img, ratio=1.5)
    assert (out_bright >= ori_img).all() or out_bright.max() == 255
    out_dim = att.bright_att(input_img=ori_img, ratio=0.5)
    assert (out_dim <= ori_img).all()
    assert out_dim.max() <= 255


def test_shelter_att(ori_img):
    out = att.shelter_att(input_img=ori_img, ratio=0.05, n=3)
    assert out.shape == ori_img.shape
    white_mask = (out == 255).all(axis=2)
    assert white_mask.sum() > 0


def test_salt_pepper_att(ori_img):
    out = att.salt_pepper_att(input_img=ori_img, ratio=0.05)
    assert out.shape == ori_img.shape
    diff = (out != ori_img).any(axis=2)
    assert diff.sum() > 0


def test_rot_att(ori_img):
    out = att.rot_att(input_img=ori_img, angle=45)
    assert out.shape == ori_img.shape