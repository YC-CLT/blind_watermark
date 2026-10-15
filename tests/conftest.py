import pytest
import cv2
import numpy as np
from blind_watermark import WaterMark
from blind_watermark.version import bw_notes


@pytest.fixture(scope="session")
def test_image_path():
    return "examples/pic/ori_img.jpeg"


@pytest.fixture(scope="session")
def test_wm_img_path():
    return "examples/pic/watermark.png"


@pytest.fixture(scope="session")
def ori_img(test_image_path):
    img = cv2.imread(test_image_path)
    assert img is not None, f"Test image not found: {test_image_path}"
    return img


@pytest.fixture(scope="session")
def wm_img(test_wm_img_path):
    img = cv2.imread(test_wm_img_path, cv2.IMREAD_GRAYSCALE)
    assert img is not None, f"Watermark image not found: {test_wm_img_path}"
    return img


@pytest.fixture
def default_bwm():
    return WaterMark(password_img=1, password_wm=1)


@pytest.fixture(autouse=True)
def no_bw_notes():
    bw_notes.close()


from blind_watermark.fft_watermark import WaterMarkFFT


@pytest.fixture(scope="session")
def fft_ori_img(ori_img):
    return ori_img


@pytest.fixture(scope="session")
def fft_wm_img(wm_img):
    img_3ch = cv2.cvtColor(wm_img, cv2.COLOR_GRAY2BGR)
    return img_3ch


@pytest.fixture
def default_fft():
    return WaterMarkFFT(seed=20160930, alpha=3.0)