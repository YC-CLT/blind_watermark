# blind-watermark

基于频域的数字盲水印  

# 安装

```bash
uv sync
uv tool install -e .
```

# 如何使用

## 命令行中使用

### 嵌入/提取文字水印

```bash
# 嵌入：嵌入时末尾会打印 wm_bit 长度（例如 111）
blind_watermark embed --pwd-img 1234 ori_img.jpeg "Hello World" embedded.png
# 输出: Watermark length (bits): 111

# 提取：wm_shape 填上一步打印的 bit 长度
blind_watermark extract --pwd-img 1234 embedded.png 111
# 输出: Hello World
```

### 嵌入/提取图片水印

```bash
# 嵌入：auto mode 下程序自动检测 watermark 参数是图片路径
blind_watermark embed ori_img.jpeg watermark.png embedded.png

# 提取：wm_shape 为水印图片的宽,高，-o 指定输出路径
blind_watermark extract embedded.png 64,64 -o extracted_wm.png
```

### 全部参数

```bash
blind_watermark embed --help
```

核心参数说明：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--pwd-img` | 1 | 图片密码：控制 DCT 系数打乱，决定水印藏在频域的哪个位置 |
| `--pwd-wm` | 1 | 水印密码：控制水印 bit 序列打乱，决定水印以什么顺序写入 |
| `--block-shape H W` | 4 4 | DCT 块大小，越大容量越小但鲁棒性越强 |
| `--wm-mode` | auto | 水印类型：str（文字）/ img（图片）/ bit（二进制） |
| `-c, --compress` | None | JPEG 压缩率 0-100，越小压缩越多 |
| `--processes` | None | 并行进程数，None = 全部核心 |

### 调试模式

如果 `blind_watermark` 入口点有问题，可以用模块方式：

```bash
python -m blind_watermark.cli_tools embed --pwd-img 1234 ori_img.jpeg "test" out.png
python -m blind_watermark.cli_tools extract --pwd-img 1234 out.png 39
```

## Python 中使用

原图 + 水印 = 打上水印的图

![origin_image](docs/原图.jpeg) + '@guofei9987 开源万岁！' = ![打上水印的图](docs/打上水印的图.jpg)

参考 [代码](/examples/example_str.py)

嵌入水印

```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img.jpg')
wm = '@guofei9987 开源万岁！'
bwm1.read_wm(wm, mode='str')
bwm1.embed('output/embedded.png')
len_wm = len(bwm1.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
```

提取水印

```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)
```

Output:
>@guofei9987 开源万岁！

### 各种攻击后的效果

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|旋转攻击45度|![旋转攻击](docs/旋转攻击.jpg)|'@guofei9987 开源万岁！'|
|随机截图|![截屏攻击](docs/截屏攻击2_还原.jpg)|'@guofei9987 开源万岁！'|
|多遮挡| ![多遮挡攻击](docs/多遮挡攻击.jpg) |'@guofei9987 开源万岁！'|
|纵向裁剪|![横向裁剪攻击](docs/横向裁剪攻击_填补.jpg)|'@guofei9987 开源万岁！'|
|横向裁剪|![纵向裁剪攻击](docs/纵向裁剪攻击_填补.jpg)|'@guofei9987 开源万岁！'|
|缩放攻击|![缩放攻击](docs/缩放攻击.jpg)|'@guofei9987 开源万岁！'|
|椒盐攻击|![椒盐攻击](docs/椒盐攻击.jpg)|'@guofei9987 开源万岁！'|
|亮度攻击|![亮度攻击](docs/亮度攻击.jpg)|'@guofei9987 开源万岁！'|

### 嵌入图片

参考 [代码](/examples/example_str.py)

嵌入：

```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# read original image
bwm1.read_img('pic/ori_img.jpg')
# read watermark
bwm1.read_wm('pic/watermark.png')
# embed
bwm1.embed('output/embedded.png')
```

提取：

```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png', )
```

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|旋转攻击45度|![旋转攻击](docs/旋转攻击.jpg)|![旋转攻击](docs/旋转攻击_提取水印.png)|
|随机截图|![截屏攻击](docs/截屏攻击2_还原.jpg)|![截屏攻击](docs/截屏攻击_提取水印.png)|
|多遮挡| ![多遮挡攻击](docs/多遮挡攻击.jpg) |![多遮挡_提取水印](docs/多遮挡攻击_提取水印.png)|

### 隐水印还可以是二进制数据

参考 [代码](/examples/example_bit.py)

作为 demo， 如果要嵌入是如下长度为6的二进制数据

```python
wm = [True, False, True, True, True, False]
```

嵌入水印

```python
# 除了嵌入图片，也可以嵌入比特类数据
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_ori_img('pic/ori_img.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/打上水印的图.png')
```

解水印：（注意设定水印形状 `wm_shape`）

```python
bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
wm_extract = bwm1.extract('output/打上水印的图.png', mode='bit')
print(wm_extract)
```

解出的水印是一个0～1之间的实数，方便用户自行卡阈值。如果水印信息量远小于图片可容纳量，偏差极小。

# 并行计算

```python
WaterMark(..., processes=None)
```

- `processes`: 整数，指定线程数。默认为 `None`, 表示使用全部线程。

## 相关项目

- text_blind_watermark (文本盲水印，把信息隐秘地打入文本): [https://github.com/guofei9987/text_blind_watermark](https://github.com/guofei9987/text_blind_watermark)  
- HideInfo（藏物于图、藏物于音、藏图于文）：[https://github.com/guofei9987/HideInfo](https://github.com/guofei9987/HideInfo)
