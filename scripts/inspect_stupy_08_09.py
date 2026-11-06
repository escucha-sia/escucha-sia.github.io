import subprocess
from pathlib import Path

ENGINE_DIR = Path(r"C:\Carlos\noticias_podcast\sia_tiktok_batch_engine")

for name in ["temp_audio_stupy_08", "temp_audio_stupy_09", "temp_audio_terror", "temp_audio_terror_02"]:
    d = ENGINE_DIR / name
    if d.exists():
        print(f"=== {name} ===")
        total = 0.0
        for f in sorted(d.glob("*.mp3")):
            res = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(f)
            ], capture_output=True, text=True)
            dur = float(res.stdout.strip())
            print(f"  {f.name}: {dur:.2f}s")
