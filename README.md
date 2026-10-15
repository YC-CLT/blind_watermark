# blind-watermark

数字盲水印工具，集成了两种互补的算法，覆盖 CTF 常见题型。

本项目整合了两个开源项目：

| 算法 | 来源 | 作者 |
|------|------|------|
| DWT-DCT-SVD 频域水印 | [blind_watermark](https://github.com/guofei9987/blind_watermark) | [@guofei9987](https://github.com/guofei9987) |
| FFT 空域水印 | [BlindWaterMark](https://github.com/fire-keeper/BlindWaterMark) | [@fire-keeper](https://github.com/fire-keeper) |

## 安装

```bash
uv sync
uv tool install -e .
```

## 快速对比

| | embed / extract | fft encode / decode |
|------|------|------|
| 算法 | DWT-DCT-SVD 频域 | FFT 空域 |
| 提取需要原图 | 不需要 | **需要** |
| 水印格式 | 文字 / 图片 / 二进制 | 仅图片 |
| 鲁棒性 | 强（抗旋转/裁剪/缩放） | 弱 |
| 典型场景 | 单张图提取文字水印 | 给原图 + 含水印图，提取图片水印 |

---

## 子命令

### `embed` — 嵌入水印

```bash
# 嵌入字符串
blind_watermark embed ori_img.jpeg "Hello World" embedded.png

# 嵌入图片（路径引号可省略）
blind_watermark embed ori_img.jpeg watermark.png embedded.png

# 嵌入二进制
blind_watermark embed --wm-mode bit ori_img.jpeg "True,False,True,True" embedded.png
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `image` | 必填 | 原图路径 |
| `watermark` | 必填 | 水印文字，或水印图片路径 |
| `output` | `embedded.png` | 输出图片路径 |
| `--wm-mode` | 自动检测 | `str` / `img` / `bit` |
| `-c, --compress` | None | JPEG 压缩率 0-100 |
| `--pwd-img` | 1 | 图片密码：DCT 系数打乱种子 |
| `--pwd-wm` | 1 | 水印密码：bit 序列打乱种子 |
| `--block-shape` | 4 4 | DCT 分块大小（高 宽） |
| `--core-mode` | common | 核心模式 |
| `--processes` | None | 并行进程数 |

> 嵌入字符串时，命令会打印水印 bit 长度，提取时要用到。

### `extract` — 提取水印

```bash
# 提取字符串：wm_shape 填上一步打印的 bit 长度
blind_watermark extract embedded.png 111

# 提取图片：wm_shape 填 宽,高
blind_watermark extract embedded.png 64,64 -o extracted_wm.png

# 提取二进制
blind_watermark extract --wm-mode bit embedded.png 6
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `image` | 必填 | 含水印图路径 |
| `wm_shape` | 必填 | 水印形状：`"111"` (bit 长度) 或 `"64,64"` (宽,高) |
| `-o, --output` | None | 图片水印输出路径（img 模式） |
| `--wm-mode` | 自动检测 | `str` / `img` / `bit` |
| `--pwd-img` | 1 | 图片密码，需与嵌入时一致 |
| `--pwd-wm` | 1 | 水印密码，需与嵌入时一致 |
| `--block-shape` | 4 4 | 需与嵌入时一致 |
| `--core-mode` | common | 核心模式 |
| `--processes` | None | 并行进程数 |

---

### `fft` — FFT 空域水印

与 [BlindWaterMark](https://github.com/fire-keeper/BlindWaterMark) 兼容。提取时必须提供原图。

子命令：`fft encode` / `fft decode`

```bash
# 嵌入
blind_watermark fft encode ori.png wm.png output.png

# 提取（必须提供原图！）
blind_watermark fft decode ori.png output.png extracted_wm.png

# 指定种子和强度
blind_watermark fft encode ori.png wm.png out.png --seed 12345678 --alpha 5.0
blind_watermark fft decode ori.png out.png wm.png --seed 12345678 --alpha 5.0

# Python 2 兼容模式（与旧版 BlindWaterMark 交互时使用）
blind_watermark fft decode ori.png out.png wm.png --oldseed
```

| 参数 | 默认值 | 适用 | 说明 |
|------|--------|------|------|
| `image` | 必填 | encode / decode | 原图路径 |
| `watermark` | 必填 | encode | 水印图路径 |
| `watermarked` | 必填 | decode | 含水印图路径 |
| `output` | 必填 | encode / decode | 输出路径 |
| `--seed` | 20160930 | encode / decode | 随机种子，加解密必须一致 |
| `--alpha` | 3.0 | encode / decode | 水印强度，加解密必须一致 |
| `--oldseed` | False | encode / decode | Python 2 兼容随机算法 |

---

## Python API

### WaterMark（DWT）

```python
from blind_watermark import WaterMark

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('ori_img.jpeg')
bwm.read_wm('Hello World', mode='str')
bwm.embed('embedded.png')

# 提取
bwm1 = WaterMark(password_img=1, password_wm=1)
result = bwm1.extract('embedded.png', wm_shape=111, mode='str')
```

### WaterMarkFFT（FFT）

```python
from blind_watermark import WaterMarkFFT

bwm = WaterMarkFFT(seed=20160930, alpha=3.0)
bwm.encode('ori.png', 'wm.png', 'output.png')
bwm.decode('ori.png', 'output.png', 'extracted.png')
```

| 方法 | 说明 |
|------|------|
| `.encode(原图, 水印图, 输出)` | 嵌入 |
| `.decode(原图, 含水印图, 输出)` | 提取（需原图） |
| `.encode_arr(img, wm)` | 数组版嵌入 |
| `.decode_arr(img, img_wm)` | 数组版提取 |
