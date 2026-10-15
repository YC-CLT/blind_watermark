import cv2
import numpy as np
from .fft_core import fft_encode, fft_decode


def _imread(path):
    try:
        buf = np.fromfile(path, dtype=np.uint8)
    except FileNotFoundError:
        raise FileNotFoundError(f"can't find {path}")
    img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"can't find {path}")
    return img


def _imwrite(path, img):
    ext = '.' + path.rsplit('.', 1)[-1]
    success, buf = cv2.imencode(ext, img)
    if success:
        buf.tofile(path)


class WaterMarkFFT:

    def __init__(self, seed=20160930, alpha=3.0, oldseed=False):
        self.seed = seed
        self.alpha = alpha
        self.oldseed = oldseed

    def encode(self, img_file, wm_file, output):
        img = _imread(img_file)
        wm = _imread(wm_file)

        result = self.encode_arr(img, wm)
        _imwrite(output, result)
        return result

    def decode(self, img_file, img_wm_file, output):
        img = _imread(img_file)
        img_wm = _imread(img_wm_file)

        result = self.decode_arr(img, img_wm)
        _imwrite(output, result)
        return result

    def encode_arr(self, img, wm):
        result = fft_encode(img, wm, self.seed, self.alpha, self.oldseed)
        return np.clip(result, 0, 255).astype(np.uint8)

    def decode_arr(self, img, img_wm):
        return fft_decode(img, img_wm, self.seed, self.alpha, self.oldseed)