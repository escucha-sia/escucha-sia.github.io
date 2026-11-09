import os
import sys
import shutil
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
ENGINE_DIR = ROOT_DIR / "sia_tiktok_batch_engine"
REELS_DIR = ROOT_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
NODE_PATH = r"C:\Program Files\nodejs"

def get_duration(video_path):
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ], capture_output=True, text=True)
    return float(res.stdout.strip())

def render_solarwinds_video():
    reel_filename = "sIA_Storybook_16_SolarWinds_SUNBURST_Compilador_RAM.mp4"
    print(f"🚀 Iniciando renderizado GPU de {reel_filename}...")
    
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    
    renders_dir = ENGINE_DIR / "renders"
    if renders_dir.exists():
        for old_vid in renders_dir.glob("*.mp4"):
            try:
                old_vid.unlink()
            except Exception:
                pass

    cmd = ["cmd.exe", "/c", f"set PATH={NODE_PATH};%PATH% && cd /d {ENGINE_DIR} && npx hyperframes render --gpu"]
    print("Ejecutando HyperFrames GPU render...")
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"HyperFrames render error: {res.stderr}\nStdout: {res.stdout}")
        
    print("Render completado por HyperFrames. Buscando archivo de salida...")
    output_mp4 = renders_dir / "video.mp4"
    if not output_mp4.exists():
        candidates = list(renders_dir.glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)

    if not output_mp4.exists():
        raise RuntimeError("No se encontró el video generado en renders/")

    target_reel = REELS_DIR / reel_filename
    shutil.copy2(output_mp4, target_reel)
    print(f"✓ Video guardado en reels/: {target_reel}")

    if SPOTIFY_REELS_DIR.exists():
        shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / reel_filename)
        print(f"✓ Respaldo local Spotify: {SPOTIFY_REELS_DIR / reel_filename}")
        
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / reel_filename)
        print(f"✓ Respaldo Google Drive: {GDRIVE_REELS_DIR / reel_filename}")

    dur = get_duration(target_reel)
    size_mb = target_reel.stat().st_size / (1024 * 1024)
    print(f"🎉 Video maestro vertical generado: {target_reel} ({dur:.2f}s / {dur/60:.2f} min, {size_mb:.2f} MB)")
    
    # Generate video poster thumbnail at 10s
    poster_filename = reel_filename.replace(".mp4", "_poster.jpg")
    target_poster = REELS_DIR / poster_filename
    subprocess.run([
        "ffmpeg", "-y", "-ss", "00:00:15", "-i", str(target_reel),
        "-vframes", "1", "-q:v", "2", str(target_poster)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✓ Poster generado: {target_poster}")

if __name__ == "__main__":
    render_solarwinds_video()
