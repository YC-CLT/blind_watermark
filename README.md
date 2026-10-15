# blind-watermark

基于频域（DWT-DCT-SVD）和空域（FFT）的数字盲水印，覆盖两种 CTF 题型。

本项目是对 [blind_watermark](https://github.com/guofei9987/blind_watermark) 的整合，额外集成了 [BlindWaterMark](https://github.com/fire-keeper/BlindWaterMark) 的 FFT 空域水印算法。

## 两种水印算法

| 特性 | DWT (embed/extract) | FFT (fft encode/decode) |
|------|---------------------|-------------------------|
| 算法 | DWT-DCT-SVD 频域 | FFT 空域 |
| 提取需原图 | 不需要 | **需要** |
| 水印格式 | 文字 / 图片 / 二进制 | 仅图片 |
| 鲁棒性 | 强（抗旋转/裁剪/缩放） | 弱 |
| 典型场景 | 单张图，提取文字水印 | 给原图+含水印图，提取图片水印 |

更多效果演示、抗攻击测试、原理说明 → [原始项目](https://github.com/guofei9987/blind_watermark)

# 安装

```bash
uv sync
uv tool install -e .
```

# 如何使用

## 命令行中使用

### 嵌入/提取文字水印

```bash
# 嵌入：末尾打印 wm_bit 长度
blind_watermark embed --pwd-img 1234 ori_img.jpeg "Hello World" embedded.png

# 提取：wm_shape 填上一步打印的 bit 长度
blind_watermark extract --pwd-img 1234 embedded.png 111
```

### 嵌入/提取图片水印

```bash
blind_watermark embed ori_img.jpeg watermark.png embedded.png
blind_watermark extract embedded.png 64,64 -o extracted_wm.png
```

### 全部参数

```bash
blind_watermark embed --help
```

| 参数 | 默认值 | embed | extract | 说明 |
|------|--------|-------|---------|------|
| `image` (位置1) | 必填 | ✓ | ✓ | 原图/含水印图路径 |
| `watermark` (位置2) | 必填 | ✓ | — | 水印文字或图片路径 |
| `output` (位置3) | `embedded.png` | ✓ | — | 输出路径 |
| `wm_shape` (位置2) | 必填 | — | ✓ | 水印形状，`"111"` 或 `"64,64"` |
| `-o, --output` | None | — | ✓ | 提取结果输出（img 模式） |
| `--pwd-img` | 1 | ✓ | ✓ | 图片密码：DCT 系数打乱种子 |
| `--pwd-wm` | 1 | ✓ | ✓ | 水印密码：bit 序列打乱种子 |
| `--wm-mode` | auto | ✓ | ✓ | str / img / bit |
| `--block-shape` | 4 4 | ✓ | ✓ | DCT 块大小 |
| `-c, --compress` | None | ✓ | — | JPEG 压缩率 0-100 |
| `--processes` | None | ✓ | ✓ | 并行进程数 |
| `--core-mode` | common | ✓ | ✓ | 核心模式 |

### 调试模式

```bash
python -m blind_watermark.cli_tools embed --pwd-img 1234 ori_img.jpeg "test" out.png
python -m blind_watermark.cli_tools extract --pwd-img 1234 out.png 39
```

### FFT 空域水印

FFT 算法与 [BlindWaterMark](https://github.com/fire-keeper/BlindWaterMark) 兼容，提取时必须提供原图。

```bash
# 嵌入水印
blind_watermark fft encode ori.png wm.png output.png

# 提取水印（需要原图！）
blind_watermark fft decode ori.png output.png extracted_wm.png

# 指定随机种子和水印强度
blind_watermark fft encode ori.png wm.png out.png --seed 12345678 --alpha 5.0
blind_watermark fft decode ori.png out.png wm.png --seed 12345678 --alpha 5.0

# Python 2 兼容模式
blind_watermark fft decode ori.png out.png wm.png --oldseed
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `image` (位置1) | 必填 | 原图路径 |
| `watermark` (位置2) | 必填 | 水印图（encode）/ 含水印图（decode） |
| `output` (位置3) | 必填 | 输出路径 |
| `--seed` | 20160930 | 随机种子，加解密必须一致 |
| `--alpha` | 3.0 | 水印强度，加解密必须一致 |
| `--oldseed` | False | Python 2 兼容模式 |

## Python 中使用

### 嵌入字符串

```python
from blind_watermark import WaterMark

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('pic/ori_img.jpg')
bwm.read_wm('@guofei9987 开源万岁！', mode='str')
bwm.embed('output/embedded.png')
len_wm = len(bwm.wm_bit)  # 提取时需要
```

提取：

```python
bwm = WaterMark(password_img=1, password_wm=1)
result = bwm.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(result)
```

### 嵌入图片

```python
bwm = WaterMark(password_wm=1, password_img=1)
bwm.read_img('pic/ori_img.jpg')
bwm.read_wm('pic/watermark.png')
bwm.embed('output/embedded.png')
```

提取：

```python
bwm = WaterMark(password_wm=1, password_img=1)
bwm.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png')
```

### 嵌入二进制数据

```python
bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_ori_img('pic/ori_img.jpg')
bwm.read_wm([True, False, True, True, True, False], mode='bit')
bwm.embed('output/embedded.png')
```

提取：

```python
bwm = WaterMark(password_img=1, password_wm=1)
result = bwm.extract('output/embedded.png', wm_shape=6, mode='bit')
print(result)
```

### FFT — WaterMarkFFT

```python
from blind_watermark import WaterMarkFFT

bwm = WaterMarkFFT(seed=20160930, alpha=3.0)
bwm.encode('ori.png', 'wm.png', 'output.png')
bwm.decode('ori.png', 'output.png', 'extracted.png')

# Python 2 兼容模式
bwm_old = WaterMarkFFT(oldseed=True)
bwm_old.encode('ori.png', 'wm.png', 'out_old.png')
```

| 方法 | 说明 |
|------|------|
| `WaterMarkFFT(seed, alpha, oldseed)` | 创建实例 |
| `.encode(原图, 水印图, 输出)` | 嵌入水印 |
| `.decode(原图, 含水印图, 输出)` | 提取水印（需原图） |
| `.encode_arr(img, wm)` | 数组版嵌入 |
| `.decode_arr(img, img_wm)` | 数组版提取 |

# 并行计算

```python
WaterMark(..., processes=None)
```

`processes`: 进程数，`None` 表示全部核心。

## 相关项目

- [blind_watermark](https://github.com/guofei9987/blind_watermark) — 原始项目，更多效果演示、抗攻击测试、原理说明
- [text_blind_watermark](https://github.com/guofei9987/text_blind_watermark) — 文本盲水印
- [HideInfo](https://github.com/guofei9987/HideInfo) — 藏物于图、藏物于音、藏图于文