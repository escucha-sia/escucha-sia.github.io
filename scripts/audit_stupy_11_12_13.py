import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
REELS_DIR = BASE_DIR / "reels"
SCRATCH_DIR = BASE_DIR / "scratch" / "audit_stupy_11_12_13"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

reels = [
    "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
    "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
    "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4"
]

for r in reels:
    p = REELS_DIR / r
    if p.exists():
        stem = p.stem
        for sec in [4, 16, 28, 42]:
            out = SCRATCH_DIR / f"{stem}_{sec}s.jpg"
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(sec), "-i", str(p),
                "-vframes", "1", "-q:v", "2", str(out)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Extracted {out.name} ({out.stat().st_size} bytes)")
