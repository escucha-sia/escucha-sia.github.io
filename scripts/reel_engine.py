#!/usr/bin/env python3
"""
reel_engine.py - Motor Unificado y Soberano de Producción de Reels (sIA Podcast)
Reemplaza los scripts individuales ad-hoc integrando la tríada:
1. El Manual: Formato estricto de 45 segundos, 4 escenas, voces Jorge/Dalia +6%, safe zones.
2. La Caja de Herramientas: Edge-TTS + FFmpeg loudnorm + GSAP / HyperFrames GPU.
3. La Prueba de Terminado: Auto-auditoría determinista con verify_reel.py.
"""

import os
import sys
import json
import shutil
import asyncio
import argparse
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SHORTS_DIR = BASE_DIR / "02_Reels_Shorts"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
NODE_PATH = r"C:\Carlos\nodejs"

REELS_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"
TARGET_DURATION = 45.0

THEMES = {
    "cyan": {"primary": "#06b6d4", "badge_bg": "#0891b2", "hl": "#22d3ee", "border": "#06b6d4"},
    "purple": {"primary": "#a855f7", "badge_bg": "#7c3aed", "hl": "#c084fc", "border": "#a855f7"},
    "amber": {"primary": "#f59e0b", "badge_bg": "#d97706", "hl": "#fbbf24", "border": "#f59e0b"},
    "emerald": {"primary": "#10b981", "badge_bg": "#059669", "hl": "#34d399", "border": "#10b981"},
    "red": {"primary": "#ef4444", "badge_bg": "#dc2626", "hl": "#f87171", "border": "#ef4444"}
}

async def synthesize_dialogue(dialogue: list, temp_dir: Path):
    temp_dir.mkdir(parents=True, exist_ok=True)
    chunk_files = []
    print("🎙️ Sintetizando voces en paralelo con Edge-TTS (es-MX +6%)...")
    
    for idx, item in enumerate(dialogue):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        speaker = item.get("speaker", "JORGE").upper()
        voice = VOICE_DALIA if "DALIA" in speaker else VOICE_JORGE
        clean_text = item["text"].replace("Sia", "Sia").replace("sIA", "Sia")
        
        communicator = edge_tts.Communicate(clean_text, voice, rate="+6%")
        await communicator.save(str(chunk_path))
        chunk_files.append(chunk_path)
        print(f"   [OK] Escena {idx+1} ({speaker}): {len(clean_text)} chars")
        
    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    
    music_src = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-stream_loop", "-1", "-i", str(music_src),
        "-filter_complex",
        f"[1:a]volume=0.032,afade=t=in:st=0:d=1.0,afade=t=out:st=43.5:d=1.5[bg];"
        f"[0:a]apad=whole_dur={TARGET_DURATION}[vox];"
        f"[vox][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,"
        f"acompressor=threshold=-20dB:ratio=2.5:attack=15:release=120,"
        f"loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-t", str(TARGET_DURATION),
        str(clip_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Pista de audio maestra ensamblada y normalizada (-16 LUFS).")
    return clip_audio

def build_composition(spec: dict):
    theme_key = spec.get("theme", "cyan")
    theme = THEMES.get(theme_key, THEMES["cyan"])
    badge_tag = spec.get("badge_tag", "sIA #45 • ARQUITECTURA")
    hook_title = spec.get("title", "¿El Mito del Código de la IA?")
    
    d = spec.get("dialogue", [])
    t1 = d[0]["text"] if len(d) > 0 else "Pregunta provocadora de la industria..."
    t2 = d[1]["text"] if len(d) > 1 else "Evidencia técnica y porcentaje de fallas..."
    t3 = d[2]["text"] if len(d) > 2 else "La pesadilla en producción a las 3 de la mañana..."
    t4 = d[3]["text"] if len(d) > 3 else "La regla de oro arquitectónica."

    index_html = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #080a12;
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
    <div id="root" data-composition-id="sia_reel_factory" data-no-timeline data-start="0" data-duration="{TARGET_DURATION}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{TARGET_DURATION}"
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
        data-duration="{TARGET_DURATION}"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""
    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    scene_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,800;0,900;1,900&family=Space+Grotesk:wght@700;800;900&family=JetBrains+Mono:wght@700;800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1080px;
        height: 1920px;
        background: #090b14;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* Halftone Matrix Background */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(255, 255, 255, 0.12) 2px, transparent 2px);
        background-size: 26px 26px;
        opacity: 0.85;
      }}

      /* Safe Zones Protection: Top 180px, Bottom 260px */
      .safe-content {{
        position: absolute;
        top: 180px;
        bottom: 260px;
        left: 60px;
        right: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      .header-badge {{
        display: inline-block;
        background: {theme["badge_bg"]};
        color: #ffffff;
        padding: 12px 28px;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 2px;
        border-radius: 8px;
        border: 2px solid {theme["primary"]};
        box-shadow: 4px 4px 0px rgba(0,0,0,0.8);
      }}

      .main-title {{
        font-size: 52px;
        font-weight: 900;
        line-height: 1.15;
        margin-top: 24px;
        color: #ffffff;
        text-shadow: 2px 2px 0px #000;
      }}

      .main-title .hl {{
        color: {theme["hl"]};
      }}

      /* Dialogue Card */
      .dialogue-card {{
        background: rgba(15, 23, 42, 0.94);
        border: 3px solid {theme["border"]};
        border-radius: 16px;
        padding: 36px;
        box-shadow: 8px 8px 0px rgba(0,0,0,0.9);
        min-height: 480px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}

      .speaker-pill {{
        align-self: flex-start;
        background: #000000;
        color: {theme["hl"]};
        border: 2px solid {theme["border"]};
        padding: 8px 20px;
        font-size: 22px;
        font-weight: 900;
        border-radius: 999px;
        margin-bottom: 20px;
      }}

      .dialogue-text {{
        font-size: 38px;
        font-weight: 800;
        line-height: 1.35;
        color: #f8fafc;
      }}

      /* Footer Bar */
      .footer-cta {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #020617;
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 16px 24px;
      }}

      .footer-brand {{
        font-size: 26px;
        font-weight: 900;
        color: #38bdf8;
      }}

      .footer-sub {{
        font-size: 18px;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
      }}

      .progress-bar {{
        position: absolute;
        bottom: 0;
        left: 0;
        height: 10px;
        background: {theme["primary"]};
        width: 100%;
        animation: progress {TARGET_DURATION}s linear forwards;
      }}

      @keyframes progress {{
        from {{ width: 0%; }}
        to {{ width: 100%; }}
      }}
    </style>
  </head>
  <body>
    <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: relative; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="safe-content">
      <div>
        <div class="header-badge">{badge_tag}</div>
        <div class="main-title">{hook_title}</div>
      </div>

      <div class="dialogue-card" id="card">
        <div id="p1" style="display: block;">
          <div class="speaker-pill">🎙️ JORGE • EL GANCHO</div>
          <p class="dialogue-text">{t1}</p>
        </div>
        <div id="p2" style="display: none;">
          <div class="speaker-pill">🎙️ DALIA • EL DATO DURO</div>
          <p class="dialogue-text">{t2}</p>
        </div>
        <div id="p3" style="display: none;">
          <div class="speaker-pill">🎙️ JORGE • EL DOLOR REAL</div>
          <p class="dialogue-text">{t3}</p>
        </div>
        <div id="p4" style="display: none;">
          <div class="speaker-pill">🎙️ DALIA • LA REGLA DE ORO</div>
          <p class="dialogue-text">{t4}</p>
        </div>
      </div>

      <div class="footer-cta">
        <div>
          <div class="footer-brand">sIA Podcast</div>
          <div class="footer-sub">escucha-sia.github.io</div>
        </div>
        <div style="font-size: 22px; font-weight: 900; color: #10b981;">DISPONIBLE EN SPOTIFY</div>
      </div>
    </div>
    <div class="progress-bar"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      
      // Scene switches deterministically aligned with 45s audio
      tl.to("#p1", {{ opacity: 0, duration: 0.3 }}, 8.5);
      tl.set("#p1", {{ display: "none" }}, 8.8);
      tl.set("#p2", {{ display: "block", opacity: 0 }}, 8.8);
      tl.to("#p2", {{ opacity: 1, duration: 0.4 }}, 8.9);

      tl.to("#p2", {{ opacity: 0, duration: 0.3 }}, 20.5);
      tl.set("#p2", {{ display: "none" }}, 20.8);
      tl.set("#p3", {{ display: "block", opacity: 0 }}, 20.8);
      tl.to("#p3", {{ opacity: 1, duration: 0.4 }}, 20.9);

      tl.to("#p3", {{ opacity: 0, duration: 0.3 }}, 33.5);
      tl.set("#p3", {{ display: "none" }}, 33.8);
      tl.set("#p4", {{ display: "block", opacity: 0 }}, 33.8);
      tl.to("#p4", {{ opacity: 1, duration: 0.4 }}, 33.9);

      window.__timelines = window.__timelines || {{}};
      window.__timelines["scene"] = tl;
      tl.seek(0);
    </script>
    </div>
  </body>
</html>"""
    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Composición HTML/GSAP con Safe Zones generada.")

def render_video(output_filename: str):
    print(f"⚡ Renderizando video MP4 con HyperFrames GPU...")
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    
    renders_dir = ENGINE_DIR / "renders"
    if renders_dir.exists():
        for f in renders_dir.glob("*.mp4"):
            try: f.unlink()
            except Exception: pass

    cmd = ["cmd.exe", "/c", f"set PATH={NODE_PATH};%PATH% && cd /d {ENGINE_DIR} && npx hyperframes render --gpu"]
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Error en HyperFrames:\n{res.stderr}\n{res.stdout}")
        raise RuntimeError(f"Fallo de renderizado: {res.stderr}")
        
    candidates = list((ENGINE_DIR / "renders").glob("*.mp4"))
    if not candidates:
        raise RuntimeError("No se generó ningún archivo MP4 en renders/")
        
    generated_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
    target_mp4 = REELS_DIR / output_filename
    spotify_mp4 = SPOTIFY_REELS_DIR / output_filename
    
    shutil.copy2(generated_mp4, target_mp4)
    shutil.copy2(generated_mp4, spotify_mp4)
    print(f"📦 Video guardado en: {target_mp4}")
    print(f"   -> Copiado a Spotify: {spotify_mp4}")
    
    # Poster Frame
    poster_path = REELS_DIR / f"{target_mp4.stem}_poster.jpg"
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "00:00:03",
        "-i", str(target_mp4),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if poster_path.exists():
        shutil.copy2(poster_path, SPOTIFY_REELS_DIR / poster_path.name)
        print(f"📸 Poster capturado en: {poster_path}")
        
    return target_mp4

def generate_obsidian_note(spec: dict, mp4_filename: str):
    slug = Path(mp4_filename).stem
    note_path = SHORTS_DIR / f"{slug}.md"
    content = f"""---
id: {slug}
titulo: "{spec.get('title', 'Reel sIA')}"
tipo: reel
formato: 1080x1920_vertical
duracion: 45s
estado: publicado
video: "{mp4_filename}"
poster: "{slug}_poster.jpg"
tags: [reel, sia_podcast, tiktok, instagram, spotifylocal]
---

# 🎬 {spec.get('title', 'Reel sIA')}

> **Ficha Técnica:** {spec.get('badge_tag', 'sIA Podcast')} | 45.0s | Edge-TTS (Jorge & Dalia +6%) | Safe Zones TikTok/IG.

## 🎥 Video
![[{mp4_filename}]]

## 🎙️ Guion Canónico
{json.dumps(spec.get('dialogue', []), indent=2, ensure_ascii=False)}
"""
    note_path.write_text(content, encoding="utf-8")
    print(f"📝 Ficha Obsidian creada: {note_path}")

async def produce(spec: dict):
    slug = spec.get("id", "sIA_Reel_Nuevo")
    mp4_name = f"{slug}.mp4"
    
    temp_dir = ENGINE_DIR / f"temp_{slug}"
    await synthesize_dialogue(spec.get("dialogue", []), temp_dir)
    build_composition(spec)
    target_mp4 = render_video(mp4_name)
    generate_obsidian_note(spec, mp4_name)
    
    # Run DoD verification
    print("\n🔍 Ejecutando Prueba de Terminado (DoD)...")
    verify_script = BASE_DIR / "scripts" / "verify_reel.py"
    res = subprocess.run([sys.executable, str(verify_script), str(target_mp4)])
    if res.returncode == 0:
        print("🎉 ¡PRODUCCIÓN Y VERIFICACIÓN COMPLETADA CON ÉXITO!")
    else:
        print("⚠️ Advertencia: La verificación detectó anomalías. Revisa la salida anterior.")

def main():
    parser = argparse.ArgumentParser(description="sIA Reel Factory CLI")
    parser.add_argument("--spec", required=True, help="Ruta al archivo JSON con la especificación del reel")
    args = parser.parse_args()
    
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Error: No existe el archivo {spec_path}")
        sys.exit(1)
        
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    asyncio.run(produce(spec))

if __name__ == '__main__':
    main()
