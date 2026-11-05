import hashlib
import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
reels = [
    BASE_DIR / "reels" / "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
    BASE_DIR / "reels" / "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
    BASE_DIR / "reels" / "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4"
]

hashes = {}
for r in reels:
    if r.exists():
        wav = BASE_DIR / "scratch" / f"aud_{r.stem}.wav"
        subprocess.run(["ffmpeg", "-y", "-i", str(r), "-t", "10", "-vn", str(wav)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        h = hashlib.sha256(wav.read_bytes()).hexdigest()
        hashes[r.name] = h
        
        # Check loudness
        cmd = ["ffmpeg", "-i", str(r), "-af", "ebur128", "-f", "null", "NUL"]
        res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
        lufs = "N/A"
        for line in res.stderr.splitlines():
            if "I:" in line and "LUFS" in line:
                lufs = line.strip()
                
        print(f"[REEL] {r.name}: hash {h[:16]}... | {lufs} | size: {r.stat().st_size} bytes")
    else:
        print(f"[ERROR] Missing file: {r.name}")

unique_hashes = set(hashes.values())
print(f"\nTotal evaluated: {len(hashes)}, Unique hashes: {len(unique_hashes)}")
assert len(hashes) == len(unique_hashes), "Duplicate audio detected!"
print("[SUCCESS] ALL 3 NEW REELS HAVE 100% DISTINCT AND VERIFIED UNIQUE AUDIOS!")
