# LEARNING — api-lab-whisper-asr-minimal

> 这份文件回答：「我跑完这个仓库，应该真的学到什么？」

## 你跑完应该能回答的问题

1. ASR（语音识别）和 LLM 在"输入输出"上有什么本质区别？
2. Whisper 的 size（tiny / base / small / medium / large）分别在权衡什么？
3. 一段 10 秒的中文音频，本机 CPU 上跑 tiny 大概需要多久？为什么？
4. 为什么这类语音模型常常**离线本地跑**，而不是去云端？

## 实操验证清单（务必动手）

### 阶段 A — 环境就绪
- [ ] 装 ffmpeg（`brew install ffmpeg` / `apt install ffmpeg`）
- [ ] `python3 -m venv .venv && source .venv/bin/activate`
- [ ] `pip install -r requirements.txt`

### 阶段 B — 准备音频
- [ ] 录一段 5～15 秒的清晰中文（macOS 语音备忘录就行）
- [ ] 导出，重命名为 `sample.wav`，放到 `samples/`
- [ ] 验证 `ls samples/` 能看到 `sample.wav`
- [ ] 因为 `.gitignore` 已经把音频排除了，**它不会被 push**

### 阶段 C — 跑通最小调用
- [ ] `python3 main.py`
  - 第一次会下载 ~75MB 的 tiny 权重
  - 之后再跑只是秒级加载
- [ ] 看终端：
  - 检测语言（应当 `language=zh`）
  - 转写文字（可能略有错误，这是 tiny 的能力上限）
  - 转写耗时
- [ ] `cat output/transcript.txt` 看完整文字版

### 阶段 D — size 阶梯实验（强烈建议）
**这一步是本仓库最有价值的实验。**

- [ ] 在 `.env` 里把 `WHISPER_MODEL_SIZE` 改成 `base`（约 150MB），重跑同一个 `sample.wav`：
  - 转写质量是否变好？
  - 耗时是否明显变长？
- [ ] 改成 `small`（约 460MB），再跑：
  - 中文识别质量通常会有明显跳跃
  - 耗时 CPU 上可能翻倍
- [ ] **不要**直接跳到 `medium` 或 `large-v3`，除非你有兴趣等很久或显卡够用
- [ ] 把 size 改回 `tiny`（保持仓库默认状态）

### 阶段 E — 离线验证
- [ ] 装好模型权重后，**断网**再跑一次
- [ ] 应该完全成功——这是为什么 ASR 通常被当作"边缘 AI"的代表

## 自检题

1. ASR 的输入是音频，输出是文本。它和"TTS（语音合成）"互为反操作——你能描述 TTS 应该怎么调吗？（不需要写代码，只需说出 Input/Output）
2. tiny 模型对中文识别经常会把"AI"听成"哎"——这是模型问题、量化问题、还是音频问题？怎么判断？
3. 一段长音频（5 分钟）和短音频（5 秒），转写耗时是大致线性的吗？
4. faster-whisper 比原版 Whisper 快是为什么？（提示：CTranslate2 推理引擎）

## 与其它仓库的连接

| 关系 | 仓库 | 为什么去看 |
| --- | --- | --- |
| **不是 LLM 的小模型** | `api-lab-embedding-minimal` | embedding 也是"非 chat"任务；两者放一起，你会理解"AI 不止 chat" |
| **本地化** | `api-lab-ollama-local-minimal` / `api-lab-lmstudio-local-minimal` | ASR 通常本地跑，跟本地 LLM 是同一类隐私 / 离线场景 |
| **多模态串联** | `api-lab-gemini-minimal` | Gemini 这类多模态模型也能直接吃音频；想清楚 ASR + LLM 串联 vs 一体化多模态有啥取舍 |

## 你应该感受到的"啊哈"瞬间

- 当你看到模型把你说的"今天天气真好"识别成"今天天气真好"——你会平淡地接受"这就是 AI"。
- 当你看到模型把"调用 API"识别成"调用衣派"或别的奇怪东西——你会明白"小模型也有它的极限"。
- 当你提着 size 一档一档加上去，看着同一段音频识别质量肉眼可见地变好——**你已经亲手摸到了"模型大小 ↔ 能力上限"这条曲线**。
- 当你**断网**还能转写——你彻底理解"本地小模型"的价值不在于性能，在于"它属于你"。
