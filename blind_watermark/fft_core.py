import random
import numpy as np


def _old_shuffle(x):
    for i in reversed(range(1, len(x))):
        j = int(random.random() * (i + 1))
        x[i], x[j] = x[j], x[i]


def _shuffle_args(h, w, seed, oldseed):
    if oldseed:
        random.seed(seed, version=1)
    else:
        random.seed(seed)

    m = list(range(h))
    n = list(range(w))

    if oldseed:
        _old_shuffle(m)
        _old_shuffle(n)
    else:
        random.shuffle(m)
        random.shuffle(n)

    return m, n


def fft_encode(img, wm, seed=20160930, alpha=3.0, oldseed=False):
    img = img.astype(np.float64)
    wm = wm.astype(np.float64)

    H, W = img.shape[0], img.shape[1]
    half_H = int(H * 0.5)

    assert half_H > wm.shape[0], (
        f"watermark height ({wm.shape[0]}) must be smaller than "
        f"half of image height ({half_H})"
    )
    assert W > wm.shape[1], (
        f"watermark width ({wm.shape[1]}) must be smaller than "
        f"image width ({W})"
    )

    hwm = np.zeros((half_H, W, img.shape[2]), dtype=np.float64)
    hwm[:wm.shape[0], :wm.shape[1]] = wm

    m, n = _shuffle_args(half_H, W, seed, oldseed)
    hwm2 = hwm.copy()
    for i in range(half_H):
        for j in range(W):
            hwm[i, j] = hwm2[m[i], n[j]]

    rwm = np.zeros_like(img)
    rwm[:half_H, :W] = hwm
    for i in range(half_H):
        for j in range(W):
            rwm[H - i - 1, W - j - 1] = hwm[i, j]

    f1 = np.fft.fft2(img)
    f2 = f1 + alpha * rwm
    img_wm = np.real(np.fft.ifft2(f2))

    return img_wm


def fft_decode(img, img_wm, seed=20160930, alpha=3.0, oldseed=False):
    img = img.astype(np.float64)
    img_wm = img_wm.astype(np.float64)

    H, W = img.shape[0], img.shape[1]
    half_H = int(H * 0.5)

    m, n = _shuffle_args(half_H, W, seed, oldseed)

    f1 = np.fft.fft2(img)
    f2 = np.fft.fft2(img_wm)
    rwm = np.real((f2 - f1) / alpha)

    wm_out = np.zeros(rwm.shape, dtype=np.uint8)
    for i in range(half_H):
        for j in range(W):
            wm_out[m[i], n[j]] = np.uint8(rwm[i, j])
    for i in range(half_H):
        for j in range(W):
            wm_out[H - i - 1, W - j - 1] = wm_out[i, j]

    return wm_out