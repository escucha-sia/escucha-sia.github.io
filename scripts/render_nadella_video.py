import os
import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
ENGINE_DIR = ROOT_DIR / "sia_tiktok_batch_engine"
REELS_DIR = ROOT_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
NODE_PATH = r"C:\Program Files\nodejs"

TOTAL_DUR = 274.25
MASTER_AUDIO = ROOT_DIR / "audio" / "sIA_Corp_13_Microsoft_Nadella_Despidos_IA_2026-11-13.mp3"
REEL_FILENAME = "sIA_Storybook_19_Microsoft_Nadella_Despidos_IA.mp4"

def get_duration(video_path):
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ], capture_output=True, text=True)
    return float(res.stdout.strip())

def prepare_engine():
    print("[*] Configurando batch engine con audio maestro y composición de Nadella...")
    # 1. Copy audio
    target_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    shutil.copy2(MASTER_AUDIO, target_audio)
    print(f"  [✓] Audio maestro copiado a {target_audio}")

    # 2. Update index.html
    index_html_content = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>sIA Crónicas #13 - La Paradoja de Nadella: Despidos Masivos y Fiebre de Silicio</title>
    <style>
      body {{
        margin: 0;
        padding: 0;
        background: #000;
        overflow: hidden;
      }}
      #root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
      }}
      .clip {{
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="sia_cronicas_13_nadella_layoffs" data-no-timeline data-start="0" data-duration="{TOTAL_DUR}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{TOTAL_DUR}"
        data-track-index="0"
        data-volume="1.0"
        src="assets/current_clip.mp3"
      ></audio>

      <div
        id="main-scene"
        class="clip"
        data-composition-id="nadella_layoffs_scene"
        data-composition-src="compositions/nadella_layoffs_scene.html"
        data-start="0"
        data-duration="{TOTAL_DUR}"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""
    with open(ENGINE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print(f"  [✓] index.html actualizado con data-duration={TOTAL_DUR}")

def render_video():
    prepare_engine()
    
    print(f"🚀 Iniciando renderizado GPU HyperFrames de {REEL_FILENAME}...")
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

    target_reel = REELS_DIR / REEL_FILENAME
    shutil.copy2(output_mp4, target_reel)
    print(f"✓ Video maestro guardado en reels/: {target_reel}")

    if SPOTIFY_REELS_DIR.exists():
        shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_FILENAME)
        print(f"✓ Respaldo local Spotify: {SPOTIFY_REELS_DIR / REEL_FILENAME}")
        
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / REEL_FILENAME)
        print(f"✓ Respaldo Google Drive: {GDRIVE_REELS_DIR / REEL_FILENAME}")

    dur = get_duration(target_reel)
    size_mb = target_reel.stat().st_size / (1024 * 1024)
    print(f"🎉 Video maestro vertical generado: {target_reel} ({dur:.2f}s / {dur/60:.2f} min, {size_mb:.2f} MB)")
    
    # Generate video poster thumbnail at 35s (Act 1 Silicio vs Salarios)
    poster_filename = REEL_FILENAME.replace(".mp4", "_poster.jpg")
    target_poster = REELS_DIR / poster_filename
    subprocess.run([
        "ffmpeg", "-y", "-ss", "00:00:35", "-i", str(target_reel),
        "-vframes", "1", "-q:v", "2", str(target_poster)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✓ Poster generado: {target_poster}")

if __name__ == "__main__":
    render_video()
