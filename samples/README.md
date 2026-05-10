# samples/

把你想测试的音频文件放进这个目录，**重命名为 `sample.wav`**。

支持格式：通常 wav / mp3 / m4a / flac 都行（faster-whisper 内部用 ffmpeg 解码）。
建议用 5～15 秒的短音频，避免第一次跑就被推理时间劝退。

## 不会被提交到 git

仓库的 `.gitignore` 已经把 `samples/*.wav` 等忽略掉，不会把你的音频意外推到 GitHub。

## 没有音频怎么办？

1. macOS：打开「语音备忘录」录一段，导出 m4a，重命名为 `sample.wav`
2. 或用任何录音软件录 5 秒中文/英文，导出为 wav

只要文件最终叫 `sample.wav` 放在这个目录里就行。
