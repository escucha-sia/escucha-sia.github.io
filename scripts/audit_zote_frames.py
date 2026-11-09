import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
VID = BASE_DIR / "reels" / "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"
OUT = BASE_DIR / "scratch" / "zote_frames_audit"
OUT.mkdir(parents=True, exist_ok=True)

for sec in [5, 40, 75, 115, 165, 200]:
    fp = OUT / f"zote_{sec}s.jpg"
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(sec), "-i", str(VID),
        "-vframes", "1", "-q:v", "2", str(fp)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Extracted {fp.name}: exists={fp.exists()}")
