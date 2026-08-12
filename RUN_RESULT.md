# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 真实 ASR 运行 | 否 |
| 离线契约验证 | 通过（2026-08-12） |
| 验证模型占位 size | `tiny` |
| 真实音频时长 / 语言 / 转写耗时 | — |
| 未运行原因 | 仓库没有真实音频；未安装 `faster-whisper`、下载模型权重或使用外部资源 |

## 验证范围

在一次性的 `git archive` 副本中创建空白占位音频，并以纯内存 `faster_whisper` 桩验证了：

- 缺少 `samples/sample.wav` 时返回退出码 2；
- 模型以 `cpu` / `int8` 参数加载，音频以 `beam_size=1` 转写；
- 分段文本、语言、概率、时长会正确汇总到 `output/transcript.txt` 和 `output/result.json`；
- 模型加载失败与转写失败均返回退出码 1；
- `main.py` 通过 Python 语法编译检查。

验证结束后已移除占位音频和一次性副本。桩转写不能证明真实音频质量、模型权重、FFmpeg、识别准确率或性能。
