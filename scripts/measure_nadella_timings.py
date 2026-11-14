import sys
import subprocess
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
SCRATCH_DIR = ROOT_DIR / "scratch"
OUT_JSON = SCRATCH_DIR / "nadella_timestamps.json"

sys.path.insert(0, str(ROOT_DIR / "scripts"))
from generate_nadella_audio import DIALOGUE

def measure_segments():
    print("📏 Midiendo duración precisa de los 19 segmentos de audio generados...")
    timestamps = []
    current_time = 0.0

    for idx, item in enumerate(DIALOGUE):
        seg_file = SCRATCH_DIR / f"seg_{idx:02d}_{item['voice']}.mp3"
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(seg_file)
        ], capture_output=True, text=True)
        dur = float(res.stdout.strip())

        timestamps.append({
            "idx": idx,
            "act": item["act"],
            "voice": item["voice"],
            "start": round(current_time, 3),
            "end": round(current_time + dur, 3),
            "dur": round(dur, 3),
            "text": item["text"]
        })
        current_time += dur

    print(f"Total acumulado: {current_time:.2f}s")
    for t in timestamps:
        print(f"Acto {t['act']} | [{t['start']:06.2f}s - {t['end']:06.2f}s] {t['voice']}: {t['text'][:50]}...")

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(timestamps, f, indent=2, ensure_ascii=False)
    print(f"✓ Guardado en {OUT_JSON}")

if __name__ == "__main__":
    measure_segments()
