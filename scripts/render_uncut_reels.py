import os
import sys
import math
import shutil
import hashlib
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
NODE_PATH = r"C:\Carlos\nodejs"

def get_duration(file_path: Path) -> float:
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ], capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def get_audio_sha256(mp4_path: Path) -> str:
    res = subprocess.run([
        "ffmpeg", "-v", "error", "-i", str(mp4_path),
        "-map", "0:a:0", "-f", "wav", "-"
    ], capture_output=True, check=True)
    return hashlib.sha256(res.stdout).hexdigest()[:16]

def write_engine_index(comp_id: str, title: str, bg_color: str, total_dur: float):
    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{title}</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: {bg_color};
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
    <div id="root" data-composition-id="{comp_id}" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{total_dur:.1f}"
        data-track-index="0"
        data-volume="1.0"
        src="assets/current_clip.mp3"
      ></audio>

      <div
        id="main-scene"
        class="clip"
        data-composition-id="scene"
        data-composition-src="compositions/scene.html"
        data-start="0"
        data-duration="{total_dur:.1f}"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""
    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

def mix_uncut_audio(raw_voice_path: Path, total_dur: float):
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    music_track = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    fade_out_start = max(1.0, total_dur - 1.5)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_voice_path),
        "-stream_loop", "-1", "-i", str(music_track),
        "-filter_complex",
        f"[1:a]volume=0.14,afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out_start:.1f}:d=1.5[bg];"
        f"[0:a]apad=whole_dur={total_dur:.1f}[vpad];"
        "[vpad][bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        f"[mixed]afade=t=out:st={fade_out_start:.1f}:d=1.5[faded];"
        "[faded]loudnorm=I=-16:LRA=10:TP=-1.5[norm]",
        "-map", "[norm]",
        "-ar", "44100", "-b:a", "192k",
        str(clip_audio)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.copy2(clip_audio, ENGINE_DIR / "assets" / "audio.mp3")
    actual_dur = get_duration(clip_audio)
    print(f"  🎵 current_clip.mp3 mezclado sin cortes: {actual_dur:.2f}s (target: {total_dur:.1f}s)")

def build_scene_stupy_11(t1: float, t2: float, t3: float, total_dur: float) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 11 - TV Boxes Malware</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #060913;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#06b6d4 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}
      .cyber-scanlines {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          0deg,
          rgba(6, 182, 212, 0.04) 0px,
          rgba(6, 182, 212, 0.04) 2px,
          transparent 2px,
          transparent 4px
        );
        z-index: 2;
        pointer-events: none;
      }}
      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 80px;
        color: rgba(239, 68, 68, 0.06);
        text-transform: uppercase;
        transform: rotate(-12deg) scale(1.4);
        top: 25%;
        z-index: 0;
        line-height: 1.1;
      }}
      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 80px 60px 100px 60px;
      }}
      .header-box {{ display: flex; flex-direction: column; gap: 16px; }}
      .brand-row {{ display: flex; align-items: center; justify-content: space-between; }}
      .brand-pill {{
        background: #ef4444;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(6, 182, 212, 0.15);
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #0284c7;
      }}
      .chapters-bar {{ display: flex; gap: 10px; width: 100%; margin-top: 10px; }}
      .chapter-pill {{
        flex: 1;
        padding: 12px 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 15px;
        color: #94a3b8;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }}
      .chapter-pill.active {{
        background: #0284c7;
        color: #ffffff;
        border-color: #38bdf8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        transform: scale(1.04);
      }}
      .main-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 50px 45px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(6, 182, 212, 0.25);
        border: 6px solid #ef4444;
        position: relative;
        min-height: 820px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}
      .scene {{
        display: none;
        flex-direction: column;
        gap: 24px;
        text-align: center;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
      }}
      @keyframes popIn {{
        0% {{ opacity: 0; transform: scale(0.92); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
      .myth-tag {{
        display: inline-block;
        align-self: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 26px;
        padding: 8px 24px;
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}
      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 52px;
        line-height: 1.1;
        letter-spacing: -1px;
        color: #09090f;
      }}
      .punch-pill {{
        display: inline-block;
        align-self: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 38px;
        padding: 16px 36px;
        border-radius: 20px;
        line-height: 1.2;
        border: 3px solid #000;
      }}
      .metric-box {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: #f8fafc;
        border: 4px dashed #94a3b8;
        border-radius: 20px;
        padding: 24px;
        margin-top: 10px;
      }}
      .final-pill {{
        background: #0284c7;
        color: #fff;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(2, 132, 199, 0.4);
      }}
      .footer-badge {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
      .channel-tag {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 26px; color: #94a3b8; letter-spacing: 1px; }}
      .progress-bar-container {{
        width: 100%;
        height: 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }}
      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #ef4444 0%, #06b6d4 100%);
        width: 0%;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="cyber-scanlines"></div>
    <div class="bg-ticker">MALWARE &bull; ROOT &bull; PROXY &bull; VETO &bull; GOOGLE</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🚨 sIA Sec #02</div>
          <div class="tag-pill">SUPPLY CHAIN HACK</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill active" id="chap-1">01 Caballo Troya</div>
          <div class="chapter-pill" id="chap-2">02 Firmware Root</div>
          <div class="chapter-pill" id="chap-3">03 Proxy Malicioso</div>
          <div class="chapter-pill" id="chap-4">04 Veto Histórico</div>
        </div>
      </div>

      <div class="main-card">
        <div class="scene" id="scene-1" style="display: flex;">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">ALERTA DE SEGURIDAD</div>
          <div class="headline-black">¿TV BOX BARATA EN TU SALA?</div>
          <div class="punch-pill" style="background: #fee2e2; color: #b91c1c; border-color: #ef4444;">1.3 MILLONES INFECTADAS</div>
          <div class="metric-box">
            <div style="font-size: 32px; font-weight: 900; color: #b91c1c;">⚠️ MALWARE DE FÁBRICA</div>
            <div style="font-size: 24px; font-weight: 700; color: #64748b;">No fue un clic falso: venía inyectado en el chip</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">Google desmanteló la masiva botnet XCPE.</div>
        </div>

        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #0284c7; color: #fff;">INGENIERÍA DEL ROOTKIT</div>
          <div class="headline-black">x.cpe / com.oemservice</div>
          <div class="punch-pill" style="background: #000; color: #38bdf8; border-color: #38bdf8;">PERMISOS SUPERUSUARIO</div>
          <div class="metric-box" style="background: #e0f2fe; border-color: #0284c7;">
            <div style="font-size: 30px; font-weight: 900; color: #0369a1;">⚡ PERSISTENCIA EN BOOTLOADER</div>
            <div style="font-size: 24px; font-weight: 700; color: #0284c7;">Al formatear de fábrica, el chip lo reinstala</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">Videostrong (MECOOL/T95) violó todo Android.</div>
        </div>

        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #7c3aed; color: #fff;">EL MODELO CLANDESTINO</div>
          <div class="headline-black">TU WI-FI COMO ESCUDO HACKER</div>
          <div class="punch-pill" style="background: #f3e8ff; color: #6b21a8; border-color: #7c3aed;">PROXY RESIDENCIAL OSCURO</div>
          <div class="metric-box" style="background: #faf5ff; border-color: #7c3aed;">
            <div style="font-size: 30px; font-weight: 900; color: #6b21a8;">📡 TELEMETRÍA POR MQTT</div>
            <div style="font-size: 24px; font-weight: 700; color: #7c3aed;">Fraude de clics, espionaje LAN y ataques con tu IP</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">La policía investigaba la IP del módem de tu casa.</div>
        </div>

        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">RESPUESTA DE GOOGLE</div>
          <div class="headline-black">EXPULSIÓN DEFINITIVA</div>
          <div class="punch-pill" style="background: #fee2e2; color: #991b1b; font-size: 34px;">VETO TOTAL A VIDEOSTRONG</div>
          <div class="final-pill">🎧 EPISODIO COMPLETO EN SPOTIFY</div>
          <div style="font-size: 26px; font-weight: 800; color: #0284c7; margin-top: 14px;">Lee los IoCs y puertos en sIA Journal (link en bio)</div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="channel-tag">@escucha_sia &bull; Spotify Show</div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>

    <script>
      function updateTimeline(time) {{
        const s1 = document.getElementById('scene-1');
        const s2 = document.getElementById('scene-2');
        const s3 = document.getElementById('scene-3');
        const s4 = document.getElementById('scene-4');

        const c1 = document.getElementById('chap-1');
        const c2 = document.getElementById('chap-2');
        const c3 = document.getElementById('chap-3');
        const c4 = document.getElementById('chap-4');

        s1.style.display = 'none';
        s2.style.display = 'none';
        s3.style.display = 'none';
        s4.style.display = 'none';

        c1.classList.remove('active');
        c2.classList.remove('active');
        c3.classList.remove('active');
        c4.classList.remove('active');

        if (time < {t1:.2f}) {{
          s1.style.display = 'flex';
          c1.classList.add('active');
        }} else if (time < {t2:.2f}) {{
          s2.style.display = 'flex';
          c2.classList.add('active');
        }} else if (time < {t3:.2f}) {{
          s3.style.display = 'flex';
          c3.classList.add('active');
        }} else {{
          s4.style.display = 'flex';
          c4.classList.add('active');
        }}

        const pct = Math.min(100, Math.max(0, (time / {total_dur:.1f}) * 100));
        document.querySelector('.progress-bar-fill').style.width = pct + '%';
      }}

      window.__hyperframes = {{
        seek: function(t) {{
          updateTimeline(t);
        }}
      }};
    </script>
  </div>
  </body>
</html>"""

def build_scene_stupy_12(t1: float, t2: float, t3: float, total_dur: float) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 12 - Knight Capital $440M Bug</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #09090f;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#f59e0b 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}
      .finance-grid {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          0deg,
          rgba(245, 158, 11, 0.04) 0px,
          rgba(245, 158, 11, 0.04) 2px,
          transparent 2px,
          transparent 4px
        );
        z-index: 2;
        pointer-events: none;
      }}
      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 80px;
        color: rgba(239, 68, 68, 0.06);
        text-transform: uppercase;
        transform: rotate(-12deg) scale(1.4);
        top: 25%;
        z-index: 0;
        line-height: 1.1;
      }}
      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 80px 60px 100px 60px;
      }}
      .header-box {{ display: flex; flex-direction: column; gap: 16px; }}
      .brand-row {{ display: flex; align-items: center; justify-content: space-between; }}
      .brand-pill {{
        background: #f59e0b;
        color: #000000;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #ef4444;
      }}
      .chapters-bar {{ display: flex; gap: 10px; width: 100%; margin-top: 10px; }}
      .chapter-pill {{
        flex: 1;
        padding: 12px 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 15px;
        color: #94a3b8;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }}
      .chapter-pill.active {{
        background: #f59e0b;
        color: #000000;
        border-color: #fbbf24;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.6);
        transform: scale(1.04);
      }}
      .main-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 50px 45px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(245, 158, 11, 0.25);
        border: 6px solid #f59e0b;
        position: relative;
        min-height: 820px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}
      .scene {{
        display: none;
        flex-direction: column;
        gap: 24px;
        text-align: center;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
      }}
      @keyframes popIn {{
        0% {{ opacity: 0; transform: scale(0.92); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
      .myth-tag {{
        display: inline-block;
        align-self: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 26px;
        padding: 8px 24px;
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}
      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 52px;
        line-height: 1.1;
        letter-spacing: -1px;
        color: #09090f;
      }}
      .punch-pill {{
        display: inline-block;
        align-self: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 38px;
        padding: 16px 36px;
        border-radius: 20px;
        line-height: 1.2;
        border: 3px solid #000;
      }}
      .metric-box {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: #f8fafc;
        border: 4px dashed #94a3b8;
        border-radius: 20px;
        padding: 24px;
        margin-top: 10px;
      }}
      .final-pill {{
        background: #f59e0b;
        color: #000;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4);
      }}
      .footer-badge {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
      .channel-tag {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 26px; color: #94a3b8; letter-spacing: 1px; }}
      .progress-bar-container {{
        width: 100%;
        height: 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }}
      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #f59e0b 0%, #ef4444 100%);
        width: 0%;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="finance-grid"></div>
    <div class="bg-ticker">WALL STREET &bull; DEVOPS &bull; 440M &bull; POWERPEG &bull; BUG</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">📉 sIA Corp #07</div>
          <div class="tag-pill">DEVOPS DISASTER</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill active" id="chap-1">01 Wall Street</div>
          <div class="chapter-pill" id="chap-2">02 Código Zombi</div>
          <div class="chapter-pill" id="chap-3">03 Deploy Manual</div>
          <div class="chapter-pill" id="chap-4">04 $440 Millones</div>
        </div>
      </div>

      <div class="main-card">
        <div class="scene" id="scene-1" style="display: flex;">
          <div class="myth-tag" style="background: #f59e0b; color: #000;">CATÁSTROFE FINANCIERA</div>
          <div class="headline-black">$440M EN 45 MINUTOS</div>
          <div class="punch-pill" style="background: #fef3c7; color: #92400e; border-color: #f59e0b;">1 VARIABLE BOOLEANA</div>
          <div class="metric-box">
            <div style="font-size: 32px; font-weight: 900; color: #b45309;">⚡ 17% DE NYSE Y NASDAQ</div>
            <div style="font-size: 24px; font-weight: 700; color: #64748b;">Knight Capital dominaba el trading algorítmico</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">La peor pesadilla de DevOps de la historia.</div>
        </div>

        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">DEAD CODE DESASTRE</div>
          <div class="headline-black">FLAG POWERPEG (2003)</div>
          <div class="punch-pill" style="background: #000; color: #f87171; border-color: #ef4444;">REUTILIZACIÓN FATAL</div>
          <div class="metric-box" style="background: #fee2e2; border-color: #ef4444;">
            <div style="font-size: 30px; font-weight: 900; color: #b91c1c;">💀 CÓDIGO ZOMBI DE 9 AÑOS</div>
            <div style="font-size: 24px; font-weight: 700; color: #991b1b;">Reutilizaron un flag viejo para una función nueva</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">Nunca dejes código muerto en producción.</div>
        </div>

        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #7c3aed; color: #fff;">ERROR DE DEVOPS</div>
          <div class="headline-black">7 DE 8 SERVIDORES</div>
          <div class="punch-pill" style="background: #f3e8ff; color: #6b21a8; border-color: #7c3aed;">EL SERVIDOR OLVIDADO</div>
          <div class="metric-box" style="background: #faf5ff; border-color: #7c3aed;">
            <div style="font-size: 30px; font-weight: 900; color: #6b21a8;">🔄 BUCLE INFINITO A LAS 9:30 AM</div>
            <div style="font-size: 24px; font-weight: 700; color: #7c3aed;">Compraba al precio más alto y vendía al más bajo</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">4 millones de ejecuciones descontroladas.</div>
        </div>

        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">QUIEBRA EN 45 MINUTOS</div>
          <div class="headline-black">$10 MILLONES POR MINUTO</div>
          <div class="punch-pill" style="background: #fef2f2; color: #991b1b; font-size: 34px;">VENTA FORZOSA DE KNIGHT</div>
          <div class="final-pill">🎧 EPISODIO COMPLETO EN SPOTIFY</div>
          <div style="font-size: 26px; font-weight: 800; color: #b45309; margin-top: 14px;">Lee el reporte oficial de la SEC en sIA Journal</div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="channel-tag">@escucha_sia &bull; Spotify Show</div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>

    <script>
      function updateTimeline(time) {{
        const s1 = document.getElementById('scene-1');
        const s2 = document.getElementById('scene-2');
        const s3 = document.getElementById('scene-3');
        const s4 = document.getElementById('scene-4');

        const c1 = document.getElementById('chap-1');
        const c2 = document.getElementById('chap-2');
        const c3 = document.getElementById('chap-3');
        const c4 = document.getElementById('chap-4');

        s1.style.display = 'none';
        s2.style.display = 'none';
        s3.style.display = 'none';
        s4.style.display = 'none';

        c1.classList.remove('active');
        c2.classList.remove('active');
        c3.classList.remove('active');
        c4.classList.remove('active');

        if (time < {t1:.2f}) {{
          s1.style.display = 'flex';
          c1.classList.add('active');
        }} else if (time < {t2:.2f}) {{
          s2.style.display = 'flex';
          c2.classList.add('active');
        }} else if (time < {t3:.2f}) {{
          s3.style.display = 'flex';
          c3.classList.add('active');
        }} else {{
          s4.style.display = 'flex';
          c4.classList.add('active');
        }}

        const pct = Math.min(100, Math.max(0, (time / {total_dur:.1f}) * 100));
        document.querySelector('.progress-bar-fill').style.width = pct + '%';
      }}

      window.__hyperframes = {{
        seek: function(t) {{
          updateTimeline(t);
        }}
      }};
    </script>
  </div>
  </body>
</html>"""

def build_scene_stupy_13(t1: float, t2: float, t3: float, total_dur: float) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 13 - XZ Utils Backdoor 500ms</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #020617;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#10b981 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}
      .matrix-grid {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          0deg,
          rgba(16, 185, 129, 0.04) 0px,
          rgba(16, 185, 129, 0.04) 2px,
          transparent 2px,
          transparent 4px
        );
        z-index: 2;
        pointer-events: none;
      }}
      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 80px;
        color: rgba(16, 185, 129, 0.06);
        text-transform: uppercase;
        transform: rotate(-12deg) scale(1.4);
        top: 25%;
        z-index: 0;
        line-height: 1.1;
      }}
      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 80px 60px 100px 60px;
      }}
      .header-box {{ display: flex; flex-direction: column; gap: 16px; }}
      .brand-row {{ display: flex; align-items: center; justify-content: space-between; }}
      .brand-pill {{
        background: #10b981;
        color: #000000;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #059669;
      }}
      .chapters-bar {{ display: flex; gap: 10px; width: 100%; margin-top: 10px; }}
      .chapter-pill {{
        flex: 1;
        padding: 12px 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 15px;
        color: #94a3b8;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }}
      .chapter-pill.active {{
        background: #059669;
        color: #ffffff;
        border-color: #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.6);
        transform: scale(1.04);
      }}
      .main-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 50px 45px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(16, 185, 129, 0.25);
        border: 6px solid #10b981;
        position: relative;
        min-height: 820px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}
      .scene {{
        display: none;
        flex-direction: column;
        gap: 24px;
        text-align: center;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
      }}
      @keyframes popIn {{
        0% {{ opacity: 0; transform: scale(0.92); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
      .myth-tag {{
        display: inline-block;
        align-self: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 26px;
        padding: 8px 24px;
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}
      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 52px;
        line-height: 1.1;
        letter-spacing: -1px;
        color: #09090f;
      }}
      .punch-pill {{
        display: inline-block;
        align-self: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 38px;
        padding: 16px 36px;
        border-radius: 20px;
        line-height: 1.2;
        border: 3px solid #000;
      }}
      .metric-box {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: #f8fafc;
        border: 4px dashed #94a3b8;
        border-radius: 20px;
        padding: 24px;
        margin-top: 10px;
      }}
      .final-pill {{
        background: #059669;
        color: #fff;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(5, 150, 105, 0.4);
      }}
      .footer-badge {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
      .channel-tag {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 26px; color: #94a3b8; letter-spacing: 1px; }}
      .progress-bar-container {{
        width: 100%;
        height: 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }}
      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        width: 0%;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="matrix-grid"></div>
    <div class="bg-ticker">XZ UTILS &bull; SSH BACKDOOR &bull; JIA TAN &bull; 500MS &bull; FREUND</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🛡️ sIA Sec #03</div>
          <div class="tag-pill">CYBER ESPIONAGE</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill active" id="chap-1">01 El Enigma 500ms</div>
          <div class="chapter-pill" id="chap-2">02 Infiltración 2 Años</div>
          <div class="chapter-pill" id="chap-3">03 Llave Maestra SSH</div>
          <div class="chapter-pill" id="chap-4">04 El Héroe Andrés</div>
        </div>
      </div>

      <div class="main-card">
        <div class="scene" id="scene-1" style="display: flex;">
          <div class="myth-tag" style="background: #10b981; color: #000;">EL DÍA QUE INTERNET CASI CAE</div>
          <div class="headline-black">500 MILISEGUNDOS DE LAG</div>
          <div class="punch-pill" style="background: #d1fae5; color: #065f46; border-color: #10b981;">EL BACKDOOR DE XZ UTILS</div>
          <div class="metric-box">
            <div style="font-size: 32px; font-weight: 900; color: #047857;">⚡ AFECTABA A TODO LINUX</div>
            <div style="font-size: 24px; font-weight: 700; color: #64748b;">Servidores bancarios, nubes y gobiernos en jaque</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">La mayor conspiración en código abierto.</div>
        </div>

        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #6366f1; color: #fff;">INGENIERÍA SOCIAL</div>
          <div class="headline-black">JIA TAN: 2 AÑOS DE PACIENCIA</div>
          <div class="punch-pill" style="background: #000; color: #818cf8; border-color: #6366f1;">GANÁNDOSE AL MANTENEDOR</div>
          <div class="metric-box" style="background: #eef2ff; border-color: #6366f1;">
            <div style="font-size: 30px; font-weight: 900; color: #4338ca;">🕵️ PRESIÓN CON CUENTAS TÍTERE</div>
            <div style="font-size: 24px; font-weight: 700; color: #6366f1;">Inyectó el código en archivos de prueba corruptos</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">Compilación oculta mediante macros M4.</div>
        </div>

        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">EXPLOIT DE KERNEL</div>
          <div class="headline-black">BYPASS ROOT EN OPENSSH</div>
          <div class="punch-pill" style="background: #fee2e2; color: #b91c1c; border-color: #ef4444;">HOOK IFUNC EN LIBLZMA</div>
          <div class="metric-box" style="background: #fef2f2; border-color: #ef4444;">
            <div style="font-size: 30px; font-weight: 900; color: #b91c1c;">🔑 CONTROL TOTAL SIN REGISTROS</div>
            <div style="font-size: 24px; font-weight: 700; color: #ef4444;">Una clave privada podía mandar órdenes a cualquier servidor</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">A horas de entrar a Debian y Red Hat estables.</div>
        </div>

        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #10b981; color: #000;">EL INGENIERO OBSERVADOR</div>
          <div class="headline-black">ANDRÉS FREUND</div>
          <div class="punch-pill" style="background: #d1fae5; color: #065f46; font-size: 34px;">MICRO-BENCHMARK DE POSTGRESQL</div>
          <div class="final-pill">🎧 EPISODIO COMPLETO EN SPOTIFY</div>
          <div style="font-size: 26px; font-weight: 800; color: #059669; margin-top: 14px;">Lee el post-mortem en sIA Journal (link en bio)</div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="channel-tag">@escucha_sia &bull; Spotify Show</div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>

    <script>
      function updateTimeline(time) {{
        const s1 = document.getElementById('scene-1');
        const s2 = document.getElementById('scene-2');
        const s3 = document.getElementById('scene-3');
        const s4 = document.getElementById('scene-4');

        const c1 = document.getElementById('chap-1');
        const c2 = document.getElementById('chap-2');
        const c3 = document.getElementById('chap-3');
        const c4 = document.getElementById('chap-4');

        s1.style.display = 'none';
        s2.style.display = 'none';
        s3.style.display = 'none';
        s4.style.display = 'none';

        c1.classList.remove('active');
        c2.classList.remove('active');
        c3.classList.remove('active');
        c4.classList.remove('active');

        if (time < {t1:.2f}) {{
          s1.style.display = 'flex';
          c1.classList.add('active');
        }} else if (time < {t2:.2f}) {{
          s2.style.display = 'flex';
          c2.classList.add('active');
        }} else if (time < {t3:.2f}) {{
          s3.style.display = 'flex';
          c3.classList.add('active');
        }} else {{
          s4.style.display = 'flex';
          c4.classList.add('active');
        }}

        const pct = Math.min(100, Math.max(0, (time / {total_dur:.1f}) * 100));
        document.querySelector('.progress-bar-fill').style.width = pct + '%';
      }}

      window.__hyperframes = {{
        seek: function(t) {{
          updateTimeline(t);
        }}
      }};
    </script>
  </div>
  </body>
</html>"""

def render_and_distribute(reel_filename: str):
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
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("HyperFrames stdout:", res.stdout)
        print("HyperFrames stderr:", res.stderr)
        raise RuntimeError(f"Error en HyperFrames: {res.stderr}")

    output_mp4 = renders_dir / "video.mp4"
    if not output_mp4.exists():
        candidates = list(renders_dir.glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)

    if not output_mp4.exists():
        raise RuntimeError("No se encontró video renderizado en renders/")

    target_reel = REELS_DIR / reel_filename
    shutil.copy2(output_mp4, target_reel)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / reel_filename)
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / reel_filename)

    dur = get_duration(target_reel)
    sha = get_audio_sha256(target_reel)
    size_mb = target_reel.stat().st_size / (1024 * 1024)
    print(f"  ✅ Renderizado SIN CORTES: {reel_filename} | Duración={dur:.2f}s | Tamaño={size_mb:.2f}MB | AudioSHA={sha}")

def main():
    configs = [
        {
            "id": "sia_motion_reel_stupy_11",
            "title": "sIA Reel Stupy 11 - TV Boxes Malware",
            "bg": "#060913",
            "temp_dir": BASE_DIR / "temp_audio_stupy_11",
            "reel_file": "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
            "builder": build_scene_stupy_11
        },
        {
            "id": "sia_motion_reel_stupy_12",
            "title": "sIA Reel Stupy 12 - Knight Capital $440M Bug",
            "bg": "#09090f",
            "temp_dir": BASE_DIR / "temp_audio_stupy_12",
            "reel_file": "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
            "builder": build_scene_stupy_12
        },
        {
            "id": "sia_motion_reel_stupy_13",
            "title": "sIA Reel Stupy 13 - XZ Utils Backdoor 500ms",
            "bg": "#020617",
            "temp_dir": BASE_DIR / "temp_audio_stupy_13",
            "reel_file": "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4",
            "builder": build_scene_stupy_13
        }
    ]

    for cfg in configs:
        print("\n" + "="*75)
        print(f"🎬 PROCESANDO REEL ELÁSTICO SIN CORTES: {cfg['title']}")
        print("="*75)
        tdir = cfg["temp_dir"]
        chunks = sorted(tdir.glob("chunk_*.mp3"))
        durs = [get_duration(c) for c in chunks]
        raw_voice = tdir / "raw_reel_voice.mp3"
        voice_dur = get_duration(raw_voice)
        total_dur = float(math.ceil(voice_dur + 2.0))

        t1 = durs[0]
        t2 = durs[0] + durs[1]
        t3 = durs[0] + durs[1] + durs[2]

        print(f"  ⏱️ Voz real: {voice_dur:.2f}s | Duración elástica Reel: {total_dur:.1f}s")
        print(f"  📍 Transiciones exactas por capítulo: Cap1=0..{t1:.2f}s | Cap2={t1:.2f}..{t2:.2f}s | Cap3={t2:.2f}..{t3:.2f}s | Cap4={t3:.2f}..{total_dur:.1f}s")

        mix_uncut_audio(raw_voice, total_dur)
        write_engine_index(cfg["id"], cfg["title"], cfg["bg"], total_dur)
        scene_html = cfg["builder"](t1, t2, t3, total_dur)
        (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
        render_and_distribute(cfg["reel_file"])

    print("\n🎉 ¡TODOS LOS 3 REELS NUEVOS RENDERIZADOS CON DURACIÓN COMPLETA SIN CORTES!")

if __name__ == "__main__":
    main()
