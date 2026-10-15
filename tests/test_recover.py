import numpy as np
from blind_watermark.recover import estimate_crop_parameters, recover_crop


def test_estimate_crop_no_scale(ori_img):
    h, w = ori_img.shape[:2]
    half = ori_img[:h // 2, :, :]
    loc, shape, score, scale_infer = estimate_crop_parameters(
        tem_img=half, ori_img=ori_img, scale=(1, 1)
    )
    x1, y1, x2, y2 = loc
    assert score > 0.9
    assert y1 == 0
    assert scale_infer == 1


def test_recover_crop_shape(ori_img):
    h, w = ori_img.shape[:2]
    half = ori_img[:h // 2, :, :]
    out = recover_crop(tem_img=half, loc=(0, 0, w, h // 2), image_o_shape=(h, w))
    assert out.shape[:2] == (h, w)


def test_recover_crop_content(ori_img):
    h, w = ori_img.shape[:2]
    half = ori_img[:h // 2, :, :]
    out = recover_crop(tem_img=half, loc=(0, 0, w, h // 2), image_o_shape=(h, w))
    recovered_half = out[:h // 2, :, :]
    assert np.array_equal(recovered_half, half.astype(np.float64))