# blind-watermark

基于频域的数字盲水印。

本项目是对 [blind_watermark](https://github.com/guofei9987/blind_watermark) 的简单整合，方便本地开发和测试。

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

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--pwd-img` | 1 | 图片密码：DCT 系数打乱种子 |
| `--pwd-wm` | 1 | 水印密码：bit 序列打乱种子 |
| `--block-shape H W` | 4 4 | DCT 块大小 |
| `--wm-mode` | auto | str / img / bit |
| `-c, --compress` | None | JPEG 压缩率 0-100 |
| `--processes` | None | 并行进程数 |

### 调试模式

```bash
python -m blind_watermark.cli_tools embed --pwd-img 1234 ori_img.jpeg "test" out.png
python -m blind_watermark.cli_tools extract --pwd-img 1234 out.png 39
```

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

# 并行计算

```python
WaterMark(..., processes=None)
```

`processes`: 进程数，`None` 表示全部核心。

## 相关项目

- [blind_watermark](https://github.com/guofei9987/blind_watermark) — 原始项目，更多效果演示、抗攻击测试、原理说明
- [text_blind_watermark](https://github.com/guofei9987/text_blind_watermark) — 文本盲水印
- [HideInfo](https://github.com/guofei9987/HideInfo) — 藏物于图、藏物于音、藏图于文