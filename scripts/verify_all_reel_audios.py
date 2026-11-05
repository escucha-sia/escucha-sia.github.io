import hashlib
import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
reels = [
    BASE_DIR / "reels" / "sIA_Reel_Stupy_07_Dulces_Montes_Tomy.mp4",
    BASE_DIR / "reels" / "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4",
    BASE_DIR / "reels" / "sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4",
    BASE_DIR / "reels" / "sIA_Terror_01_Las_Escaleras_Reel.mp4"
]

hashes = {}
for r in reels:
    if r.exists():
        wav = BASE_DIR / "scratch" / f"aud_{r.stem}.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(r), "-t", "10", "-vn", str(wav)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        h = hashlib.sha256(wav.read_bytes()).hexdigest()
        hashes[r.name] = h
        print(f"{r.name}: hash {h[:16]}... size: {wav.stat().st_size}")
    else:
        print(f"Missing: {r.name}")

unique_hashes = set(hashes.values())
print(f"Total evaluated: {len(hashes)}, Unique hashes: {len(unique_hashes)}")
assert len(hashes) == len(unique_hashes), "Duplicate audio detected!"
print("[SUCCESS] ALL REELS HAVE 100% UNIQUE AUDIOS!")
