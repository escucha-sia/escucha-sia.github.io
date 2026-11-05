import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
REEL_FILE = BASE_DIR / "reels" / "sIA_Terror_01_Las_Escaleras_Reel.mp4"
TEMP_DIR = BASE_DIR / "scratch"

def check_reel():
    print(f"Auditing Reel: {REEL_FILE.name}")
    print(f"Exists: {REEL_FILE.exists()}, Size: {REEL_FILE.stat().st_size} bytes")
    
    # Check volume and LUFS
    cmd = [
        "ffmpeg", "-i", str(REEL_FILE),
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "NUL"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    
    integrated_lufs = None
    true_peak = None
    for line in res.stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            integrated_lufs = line.strip()
        if "Peak:" in line and "dBFS" in line:
            true_peak = line.strip()
            
    print(f"Integrated Loudness: {integrated_lufs}")
    print(f"True Peak: {true_peak}")

if __name__ == "__main__":
    check_reel()
