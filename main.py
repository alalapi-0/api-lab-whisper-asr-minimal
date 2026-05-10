"""api-lab-whisper-asr-minimal

体验 ASR（自动语音识别）最小调用：
- 用 faster-whisper 加载 tiny 模型（默认）
- 读取 samples/sample.wav
- 输出识别文字到 output/transcript.txt 和 output/result.json

ASR 不是 LLM！它的输入是声音，输出是文字。
"""

import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).parent
SAMPLE_PATH = REPO_ROOT / "samples" / "sample.wav"


def main() -> int:
    load_dotenv()
    model_size = os.getenv("WHISPER_MODEL_SIZE", "tiny").strip() or "tiny"

    print(f"[信息] 模型大小: {model_size}")
    print("[信息] 第一次运行会下载该 size 对应的权重；tiny 大约 75MB。")

    if not SAMPLE_PATH.exists():
        print(f"[失败] 没找到音频文件: {SAMPLE_PATH}")
        print("       请把一段音频放到 samples/，文件名必须是 sample.wav。")
        print("       具体说明见 samples/README.md。")
        return 2

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[失败] 没装 faster-whisper。请先运行: pip install -r requirements.txt")
        return 2

    print("[信息] 正在加载 Whisper 模型（仅 CPU，int8 量化以省内存）……")
    started = time.time()
    try:
        # device='cpu' + compute_type='int8' 在 macOS / Linux 上几乎都能跑
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    except Exception as exc:
        print(f"[失败] 加载/下载模型失败: {exc}")
        print("       常见原因: 网络不通 / 磁盘不足 / 模型 size 名拼错（应为 tiny / base / small ...）")
        return 1
    load_elapsed = time.time() - started
    print(f"[信息] 模型加载耗时 {load_elapsed:.2f}s")

    print(f"[信息] 转写音频: {SAMPLE_PATH}")
    started = time.time()
    try:
        segments, info = model.transcribe(str(SAMPLE_PATH), beam_size=1)
        # segments 是迭代器，遍历一次就消费完
        text_parts = []
        seg_records = []
        for seg in segments:
            text_parts.append(seg.text)
            seg_records.append({
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text,
            })
    except Exception as exc:
        print(f"[失败] 转写过程异常: {exc}")
        print("       常见原因: 音频文件损坏 / ffmpeg 未安装 / 文件不是支持的格式")
        return 1
    elapsed = time.time() - started

    full_text = "".join(text_parts).strip()

    print()
    print("[成功] 识别结果：")
    print(full_text if full_text else "（识别为空，可能是静音音频）")
    print()
    print(f"[信息] 检测语言: {info.language} (prob={info.language_probability:.2f})")
    print(f"[信息] 转写耗时: {elapsed:.2f}s")

    out_dir = REPO_ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "transcript.txt").write_text(full_text, encoding="utf-8")
    result = {
        "model_size": model_size,
        "audio": str(SAMPLE_PATH.relative_to(REPO_ROOT)),
        "language": info.language,
        "language_probability": round(info.language_probability, 4),
        "duration_seconds": round(info.duration, 3),
        "transcribe_seconds": round(elapsed, 3),
        "load_seconds": round(load_elapsed, 3),
        "full_text": full_text,
        "segments": seg_records,
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_dir / 'transcript.txt'}")
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
