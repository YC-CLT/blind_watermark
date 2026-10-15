# AGENTS.md

## 环境

- Python 3.13.14，uv 管理依赖
- pyproject.toml 管理依赖和入口点，`[dependency-groups].dev`（非废弃的 `tool.uv.dev-dependencies`）
- **命令**：用 `cmd-exec-mcp`

## 关键文件

| 文件 | 作用 |
|------|------|
| `pyproject.toml` | uv 项目配置、依赖、entry point、pytest 配置 |
| `blind_watermark/blind_watermark.py` | WaterMark 主类，embed/extract 入口（DWT） |
| `blind_watermark/bwm_core.py` | DWT-DCT-SVD 盲水印核心算法 |
| `blind_watermark/cli_tools.py` | CLI 命令行工具（embed/extract + fft encode/decode） |
| `blind_watermark/fft_core.py` | FFT 空域水印核心算法（fft_encode/fft_decode） |
| `blind_watermark/fft_watermark.py` | WaterMarkFFT 类，FFT 文件 I/O 封装 |
| `blind_watermark/att.py` | 6 种攻击模拟 |
| `blind_watermark/recover.py` | 裁剪还原 |
| `tests/conftest.py` | 共享 pytest fixture（ori_img, wm_img, default_bwm, default_fft...） |
| `tests/test_integration.py` | DWT 全链路集成测试（embed→extract） |

## 关键常量

| 常量 | 位置 | 说明 |
|------|------|------|
| `__version__` | `blind_watermark/version.py` | 版本号，pyproject.toml 中需同步 |
| `seed=20160930` | `blind_watermark/fft_core.py` | FFT 水印默认随机种子 |
| `alpha=3.0` | `blind_watermark/fft_core.py` | FFT 水印默认嵌入强度 |

## 规则

- **测试命令**: `uv run pytest tests/ -v` 运行全部测试，`uv run pytest tests/test_xxx.py -v` 运行单个文件
- **CLI 入口点必须有 `if __name__ == '__main__'`**：否则 `python -m` 模式不工作；entry point 虽然能走，但 `-m` 是重要调试通道
- **只用 pyproject.toml 管依赖**：不要再建 requirements.txt 或 setup.py
- **block_shape 传参必须 tuple**：argparse 吐出 list，需 `tuple(args.block_shape)` 转换

## 查文献指南

## 工具

- MCP详见 `mcp_tools_summary.csv`
- 部分工具有相应的skill
- `Read` 无法访问 `D:\Temp`，MCP 长输出需 `Copy-Item` 到项目根目录，正则替换 `\\n` 为 `\n`
- **Edit `replace_all` 错误**：`replace_all=True` 无法使用。优先用 PowerShell `Select-String` + 正则做精确替换，或手动逐处 Edit
- 浏览器操控用 `chrome-devtools-edge`（Edge CDP），**禁止用 `cua-driver` 操控浏览器**
- **WebFetch 无法使用**：用 `wet-mcp extract`

## 工作流

0. 读AGENTS.md
1. 构想：调用 brainstorming → 产出 `docs/superpowers/specs/<date>-design.md`
2. 计划：调用 writing-plans → 产出 `docs/superpowers/plans/<date>-plan.md`
3. 发派：调用 dispatching-parallel-agents 产出给n号机（目前只有1，2号机）的提示词 `docs/superpowers/subprompts/<date>-plan-subprompt-n.md` ，用于手动发派（当前环境是win且不支持子代理，无法自动 dispatch），创建`docs/superpowers/subprompts/<date>-plan-process.md` 用于记录进度，防止冲突
4. 实施：调用 executing-plans
   - 先隔离，使用git创建新的dev分支（1号机）或者进入已有分支（2号机）  
   - 遇到 bug 自动触发 systematic-debugging（先找根因再修）
   - 写代码自动触发 test-driven-development（先写测试再实现）
5. 验证：调用 verification-before-completion → 跑验证命令确认完成
6. 记录：调用 writing-agents → 写CHANGELOG.md + 经验教训到AGENTS.md
7. 提交：调用 finishing-a-development-branch → 分组提交

## 经验/坑点

- **editable install .pth 编码**：uv 生成 `.pth` 用 UTF-8，但 CPython `site.py` 用 locale 编码读取。中文 Windows（locale=GBK）下含中文的路径会乱码 → `sys.path` 缺项 → entry point `ModuleNotFoundError`。修复：把 `.pth` 文件用 GBK 重写。Python 3.13 无此问题。
- **optparse 已废弃**：CLI 工具需用 argparse，子命令模式更清晰。
- **entry point exe 调试**：zipapp exe 内容可通过 `zipfile.ZipFile('xxx.exe').read('__main__.py')` 查看。
- **uv sync --no-dev 会卸载 dev 包**：验证时不带 dev 需注意 ipykernel 等会被移除。
- **pwd-img vs pwd-wm**：两个独立密码种子。pwd-img 打乱 DCT 系数顺序（藏哪里），pwd-wm 打乱水印 bit 序列（怎么藏）。任何一个不对都提取失败。
- **wm_shape 格式**：字符串/bit 模式填整数如 `111`；图片模式填 `宽,高` 如 `64,64`。嵌入时会打印 bit 长度，提取时原样填回。
- **README 需同步 CLI 变更**：改 CLI 后要更新 README 的命令行示例和参数说明，这是用户第一入口。
- **FFT 算法提取需原图**：与 DWT 不同，`fft decode` 必须提供原图，否则无法反演 `(FFT(含水印) - FFT(原图)) / alpha`。read_img 中的 "原图" 语义对 FFT 是干净的原始图像。
- **FFT oldseed 双重要求**：仅 `random.seed(seed, version=1)` 不够，Py3 的 `random.shuffle` 实现也变了，必须用自定义 `_old_shuffle` 完全模拟 Py2 行为。
- **np.uint8 截断 vs np.clip 钳制**：FFT decode 中 `rwm` 值为 float64，可能超出 [0,255]。`np.clip(x, 0, 255)` 钳制溢出值到边界再转 uint8，`np.uint8(x)` 直接模 256 截断（类似 C 的 `(uint8_t)x`），二者结果不同。Ref 原版用逐像素 `np.uint8(rwm[i][j])`，要保持兼容必须一致。
- **cv2.imread 中文路径**：OpenCV 的 `cv2.imread` 对含中文的绝对路径返回 None，但相对路径正常（Windows 下）。规避：`open(path, 'rb')` + `np.frombuffer` + `cv2.imdecode`；写出同理用 `cv2.imencode` + `buf.tofile(path)`。