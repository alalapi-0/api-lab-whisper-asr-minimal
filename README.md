# api-lab-whisper-asr-minimal

> 最小化体验：把一段本地音频转成文字（**ASR**）。

## 这个仓库不是 LLM

| 类型 | 输入 | 输出 |
| --- | --- | --- |
| 聊天模型（LLM） | 文本 | 文本 |
| **ASR（语音识别）** | 音频 | 文本 |
| TTS（语音合成） | 文本 | 音频 |

跑这个仓库，是为了让你直观感受到：「AI 不只是聊天的，它也能听」。

## 它在做什么

- 加载 `faster-whisper` 的 **tiny** 模型（约 75MB）
- 读 `samples/sample.wav`
- 输出文字到 `output/transcript.txt`、结构化结果到 `output/result.json`

## 准备工作

1. **装依赖**：
   ```bash
   cd api-lab-whisper-asr-minimal
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **装 ffmpeg**（faster-whisper 解码音频要用）：
   - macOS：`brew install ffmpeg`
   - Ubuntu：`sudo apt install ffmpeg`
   - Windows：从 ffmpeg.org 下载并加到 PATH
3. **放音频**：把任意 5～15 秒的音频文件命名为 `sample.wav`，丢进 `samples/`。
   详见 `samples/README.md`。
4. **跑起来**：
   ```bash
   python3 main.py
   cat output/transcript.txt
   ```

## .env.example

```
WHISPER_MODEL_SIZE=tiny
```

可选大小（越大越准但越慢、占内存越多）：

`tiny` < `base` < `small` < `medium` < `large-v3`

**默认 tiny。本仓库不下载更大的模型。**

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `没找到音频文件` | `samples/sample.wav` 不存在 | 按 `samples/README.md` 放好音频 |
| `没装 faster-whisper` | 没装依赖 | `pip install -r requirements.txt` |
| `加载/下载模型失败` | 网络无法访问 HF / 磁盘不够 | 检查网络；不要循环重试 |
| `转写过程异常` 提到 ffmpeg | 没装 ffmpeg | 装上即可 |
| 识别结果是空字符串 | 音频太静 / 格式有问题 | 换一段更清晰的音频 |

## 你应该能感受到的事

- 同样是「小模型」，**ASR 模型和 LLM 是完全不同的东西**：架构不同、目的不同、用法不同。
- tiny 模型对中文的识别效果有限，识别有错很正常，**这就是为什么大家会去用更大的 size**。
- 跑一次小段音频在 Mac CPU 上通常 1～10 秒，**真实可感**。

## 不会做的事

- 不会自动下载大模型（默认 tiny）
- 不会上传音频到任何云端服务
- 不会反复重试
- 不会把音频文件提交到 git（已在 `.gitignore`）
