import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")

for d in sorted(BASE_DIR.glob("temp_audio_stupy_*")):
    for f in d.glob("*.mp3"):
        if "raw" in f.name or "concat" in f.name:
            res = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(f)
            ], capture_output=True, text=True)
            print(f"{d.name}/{f.name}: {res.stdout.strip()}s")
    # Also sum individual chunks
    total = 0.0
    chunks = sorted(d.glob("chunk_*.mp3"))
    for c in chunks:
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(c)
        ], capture_output=True, text=True)
        try:
            total += float(res.stdout.strip())
        except:
            pass
    print(f"  -> {d.name} sum of {len(chunks)} chunks = {total:.2f}s")
