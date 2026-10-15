import cv2
import numpy as np
from .fft_core import fft_encode, fft_decode


class WaterMarkFFT:

    def __init__(self, seed=20160930, alpha=3.0, oldseed=False):
        self.seed = seed
        self.alpha = alpha
        self.oldseed = oldseed

    def encode(self, img_file, wm_file, output):
        img = cv2.imread(img_file)
        if img is None:
            raise FileNotFoundError(f"can't find {img_file}")
        wm = cv2.imread(wm_file)
        if wm is None:
            raise FileNotFoundError(f"can't find {wm_file}")

        result = self.encode_arr(img, wm)
        cv2.imwrite(output, result)
        return result

    def decode(self, img_file, img_wm_file, output):
        img = cv2.imread(img_file)
        if img is None:
            raise FileNotFoundError(f"can't find {img_file}")
        img_wm = cv2.imread(img_wm_file)
        if img_wm is None:
            raise FileNotFoundError(f"can't find {img_wm_file}")

        result = self.decode_arr(img, img_wm)
        cv2.imwrite(output, result)
        return result

    def encode_arr(self, img, wm):
        result = fft_encode(img, wm, self.seed, self.alpha, self.oldseed)
        return np.clip(result, 0, 255).astype(np.uint8)

    def decode_arr(self, img, img_wm):
        return fft_decode(img, img_wm, self.seed, self.alpha, self.oldseed)