import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
SCRATCH_DIR = BASE_DIR / "scratch"
REEL_FILENAME = "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"

renders_dir = ENGINE_DIR / "renders"
candidates = list(renders_dir.glob("*.mp4"))
print("Found in renders_dir:", [c.name for c in candidates])

if candidates:
    output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
    target_reel = REELS_DIR / REEL_FILENAME
    shutil.copy2(output_mp4, target_reel)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_FILENAME)
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / REEL_FILENAME)
    print(f"Copied {output_mp4.name} ({output_mp4.stat().st_size / (1024*1024):.2f} MB) -> {target_reel}")

    out_audit = SCRATCH_DIR / "zote_fixed_frames"
    out_audit.mkdir(parents=True, exist_ok=True)
    for sec in [5, 40, 75, 115, 165, 200]:
        fp = out_audit / f"zote_fixed_{sec}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sec), "-i", str(target_reel),
            "-vframes", "1", "-q:v", "2", str(fp)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  Frame {sec}s: {fp.name} ({fp.stat().st_size} bytes)")
