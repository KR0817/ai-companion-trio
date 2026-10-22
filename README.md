# 三人同行 · AI Companion Trio

GPT 龙娘敲键盘，Claude 橙书娘翻书，DeepSeek 大肥鱼捧着一大碗白米饭——三个伙伴一起陪你工作。

这是一个适配 **Codex 桌面版本地 v2 宠物格式**的社区同人桌宠。无需 API Key，动画和离线预览均在本地运行。代码采用 **MIT**；美术素材采用 **CC BY-NC-SA 4.0（署名、非商业性使用、相同方式共享）**。

| 一起工作 | 一起跳跃 | 等你回来 |
| :---: | :---: | :---: |
| ![键盘、书和白米饭](docs/images/running.gif) | ![三人跳跃](docs/images/jumping.gif) | ![待机](docs/images/idle.gif) |

## 安装

1. 前往 [Releases](https://github.com/KR0817/ai-companion-trio/releases/latest)，下载 `ai-companion-trio-v1.0.0.zip` 并解压。
2. 将其中的 `ai-companion-trio` 文件夹复制到你的 Codex 数据目录下的 `pets` 文件夹。默认 Windows 路径是 `%USERPROFILE%\.codex\pets\`；设置了 `CODEX_HOME` 时，使用该目录下的 `pets`。
3. 打开 **Codex → 设置 → Mini & Pets → 刷新**，选择 **三人同行**。

安装后的两个必要文件应位于同一层：

```text
~/.codex/pets/ai-companion-trio/
├── pet.json
└── spritesheet.webp
```

已有同名版本时先自行备份。源码 ZIP 的根目录也包含这两个文件，可以手动复制；包内的许可证与署名文件建议一同保留。

本次在 Windows Codex `26.1016.8120.0` 环境核对了本地加载格式。其他平台、宿主版本和真实任务事件未实测；离线动画检查不等同于原生应用启用验证。

## 动作与预览

双击根目录的 [`preview.html`](preview.html) 可在浏览器中离线切换九种动作、浅色或深色背景、两倍显示、慢速播放及鼠标注视。

| 状态 | 内容 |
| --- | --- |
| `idle` | 呼吸、眨眼 |
| `running-right` / `running-left` | 三人一起向左右行走 |
| `waving` | 挥手打招呼 |
| `jumping` | 蹲下、腾空、落地 |
| `failed` | 低头、担心、恢复精神 |
| `waiting` | 等待回应 |
| `running` | GPT 用键盘，Claude 看书，DeepSeek 捧白米饭 |
| `review` | 带着键盘、书和饭碗一起检查成果 |
| `look` | 16 个鼠标注视方向 |

[全部动作视频](docs/images/all-states.mp4) · [全帧图](docs/images/contact-sheet.png) · [校验摘要](docs/validation.json)

## 编辑与构建

[`source/frames/`](source/frames/) 包含全部 **73 张可编辑透明 PNG**，每张 `192 × 208`。[`source/frames.json`](source/frames.json) 记录帧顺序和动作时长。构建工具只需要 Python 3.10+ 和 Pillow。

```console
python -m venv .venv
# Activate the environment using the command for your operating system.
python -m pip install -r requirements.txt
python tools/build.py --check
python tools/build.py --output build
```

Windows PowerShell 激活命令为 `.\.venv\Scripts\Activate.ps1`；macOS/Linux 为 `source .venv/bin/activate`。

`--check` 检查帧尺寸、透明留白、清单、图集和源帧的逐像素一致性及发布哈希。`--output` 生成新的 `pet.json` 和无损 WebP，遇到已有输出文件会停止。编辑源帧后先构建新图集，再做原尺寸视觉检查；`--check` 用于核对当前发布版，会在源帧与发布版不同后报告差异。

角色由 AI 图像工具生成。这里提供的是可以确定性重新组装的最终帧源码；生成式绘画本身无法仅凭文字保证逐像素复现。不同 libwebp 版本可能产生不同的压缩字节，构建工具会检查解码后的 RGBA 像素一致。

## 已验证与已知细节

- 图集为 `1536 × 2288`，8 列、11 行；57 张动作帧、16 张注视帧、15 个透明空格。
- 发布图集通过结构校验、质量检查及 Pets MCP 校验；跳跃离地 61 px，落地与待机基线一致。
- 四个主注视方向通过三位独立盲测复核。`112.5°` 的向下幅度较轻，部分注视方向切换有小幅体型变化。
- 向右行走由向左动作逐帧镜像，时间顺序保持，因此两侧角色的屏幕位置随转向交换。
- 已检查浏览器中原尺寸与两倍尺寸的播放及浅色、深色背景；原生宠物选择和任务事件仍需在使用环境中确认。

## 来源与许可

形象参考自 [weit0529/gpt-pet](https://github.com/weit0529/gpt-pet)、[fywdy/chatgpt-chibi-pets](https://github.com/fywdy/chatgpt-chibi-pets) 和 [Buds-2025/DeepSeek-pet](https://github.com/Buds-2025/DeepSeek-pet)。完整作者署名、固定版本、修改说明和原始声明见 [`NOTICE.md`](NOTICE.md)。

本项目是非官方同人作品，与 OpenAI、Anthropic、DeepSeek 无隶属或背书关系。品牌名称仅用于识别角色来源。代码开放使用；美术素材保留上游的非商用要求。具体范围见 [`LICENSE`](LICENSE)。
