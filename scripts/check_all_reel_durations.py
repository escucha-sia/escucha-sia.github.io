import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"

for root in [BASE_DIR, ENGINE_DIR]:
    for d in sorted(root.glob("temp_audio*")):
        if d.is_dir():
            total = 0.0
            chunks = sorted(d.glob("*.mp3"))
            chunk_only = [c for c in chunks if "raw" not in c.name and "norm" not in c.name]
            for c in chunk_only:
                res = subprocess.run([
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", str(c)
                ], capture_output=True, text=True)
                try:
                    total += float(res.stdout.strip())
                except:
                    pass
            print(f"{root.name}/{d.name}: {len(chunk_only)} chunks -> total voice = {total:.2f}s")
