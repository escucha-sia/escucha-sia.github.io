#!/usr/bin/env python3
"""
produce_notisias_reel.py - Generador del Piloto de 'notisIAs' (sIA Podcast)
Formato: Split-Screen Vertical 1080x1920 (9:16)
- Superior: Dalia en Estudio Virtual Tech (Sprite + micro-animación)
- Centro: Cintillo 'notisIAs' + Subtítulos Dinámicos de Alto Impacto
- Inferior: Videowall con 3 noticias técnicas (Blackwell, Slopsquatting, MCP)
Duración: 45.0 Segundos CERRADOS (-16 LUFS EBU R128)
"""

import os
import sys
import json
import shutil
import asyncio
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
REELS_DIR = BASE_DIR / "reels"
SHORTS_DIR = BASE_DIR / "02_Reels_Shorts"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
NODE_PATH = r"C:\Carlos\nodejs"

REELS_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "es-MX-DaliaNeural"
TARGET_DURATION = 45.0
OUTPUT_SLUG = "notisIAs_01_Blackwell_VibeCoding_MCP"
OUTPUT_MP4 = f"{OUTPUT_SLUG}.mp4"

CHUNKS = [
    {
        "id": "c0",
        "title": "01 • HARDWARE & CLOUD",
        "badge": "NVIDIA BLACKWELL: 130 kW",
        "text": "¡Arrancamos con las notisIAs de hoy! En Hardware: los racks Blackwell de NVIDIA consumen ciento treinta kilovatios, obligando a instalar refrigeración líquida directa al silicio para no derretirse.",
        "start": 0.5,
        "end": 12.3
    },
    {
        "id": "c1",
        "title": "02 • CIBERSEGURIDAD",
        "badge": "CRISIS DE SLOPSQUATTING",
        "text": "En Ciberseguridad: estalla el Slopsquatting. Piratas informáticos están creando librerías falsas que la inteligencia artificial alucina durante el Vaib Couding, infectando miles de proyectos.",
        "start": 12.5,
        "end": 24.3
    },
    {
        "id": "c2",
        "title": "03 • ARQUITECTURA & AGENTES",
        "badge": "MCP EN LA LINUX FOUNDATION",
        "text": "Y en Arquitectura: Anthropic donó el protocolo M C P a la Linux Foundation. El estándar para conectar modelos con herramientas locales ya fue adoptado por Open A I y Google.",
        "start": 24.5,
        "end": 35.2
    },
    {
        "id": "c3",
        "title": "DISPONIBLE EN SPOTIFY",
        "badge": "sIA PODCAST COMPLETO",
        "text": "El análisis a fondo de estas notisIAs está en Spotify y escucha guion sia punto github punto io. ¡Soy Dalia y nos vemos mañana!",
        "start": 35.5,
        "end": 44.0
    }
]

async def step1_synthesize_audio():
    print("="*70)
    print("🎙️ PASO 1: Sintetizando audio de notisIAs con Dalia (+7%)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_notisias_01"
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_files = []
    for idx, c in enumerate(CHUNKS):
        out_f = temp_dir / f"chunk_{idx}.mp3"
        clean = c["text"].replace("notisIAs", "notisias")
        comm = edge_tts.Communicate(clean, VOICE, rate="+7%")
        await comm.save(str(out_f))
        chunk_files.append(out_f)
        print(f"   [OK] Bloque {idx+1}: {len(clean)} chars")

    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")

    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    music_src = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-stream_loop", "-1", "-i", str(music_src),
        "-filter_complex",
        f"[1:a]volume=0.030,afade=t=in:st=0:d=0.8,afade=t=out:st=43.5:d=1.5[bg];"
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
    print("✅ Pista de audio para notisIAs masterizada a -16 LUFS.")

def step2_build_split_screen_html():
    print("="*70)
    print("🎨 PASO 2: Construyendo Plantilla Split-Screen de notisIAs...")
    print("="*70)

    scene_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,700;0,800;0,900;1,900&family=Space+Grotesk:wght@600;700;800;900&family=JetBrains+Mono:wght@700;800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1080px;
        height: 1920px;
        background: #060810;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* Background Grid */
      .bg-grid {{
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(to right, rgba(6, 182, 212, 0.05) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(6, 182, 212, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
      }}

      /* Studio Header: Top 150px to 220px */
      .header-bar {{
        position: absolute;
        top: 140px;
        left: 60px;
        right: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 50;
      }}
      .brand-badge {{
        background: #0f172a;
        border: 2px solid #06b6d4;
        padding: 10px 24px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.35);
      }}
      .brand-name {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 28px;
        letter-spacing: 1px;
      }}
      .brand-name span {{
        color: #06b6d4;
      }}
      .live-tag {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 20px;
        font-weight: 800;
        color: #ef4444;
      }}
      .live-dot {{
        width: 12px;
        height: 12px;
        background: #ef4444;
        border-radius: 50%;
        box-shadow: 0 0 10px #ef4444;
      }}

      /* ================= TOP HALF: VIRTUAL STUDIO (Y: 220 to 930) ================= */
      .top-studio {{
        position: absolute;
        top: 220px;
        left: 60px;
        right: 60px;
        height: 720px;
        border-radius: 28px;
        background: radial-gradient(circle at 50% 30%, #1e1b4b 0%, #090919 80%);
        border: 2px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.7), inset 0 0 60px rgba(168, 85, 247, 0.15);
        overflow: hidden;
        display: flex;
        align-items: flex-end;
        justify-content: center;
      }}

      .studio-halo {{
        position: absolute;
        top: 20px;
        width: 480px;
        height: 480px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.35) 0%, transparent 70%);
        filter: blur(40px);
      }}

      .studio-desk {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 120px;
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-top: 3px solid #38bdf8;
        box-shadow: 0 -10px 25px rgba(56, 189, 248, 0.25);
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 50px;
      }}
      .desk-label {{
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #94a3b8;
      }}
      .desk-channel {{
        font-size: 22px;
        font-weight: 900;
        color: #38bdf8;
      }}

      .dalia-avatar {{
        position: absolute;
        bottom: 30px;
        height: 640px;
        z-index: 5;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.85));
        animation: daliaFloat 4s ease-in-out infinite alternate;
      }}
      @keyframes daliaFloat {{
        0% {{ transform: translateY(0px) scale(1); }}
        100% {{ transform: translateY(-8px) scale(1.008); }}
      }}

      /* ================= CENTER: TICKER / SUBTITLE STRIP (Y: 960 to 1100) ================= */
      .center-strip {{
        position: absolute;
        top: 960px;
        left: 60px;
        right: 60px;
        height: 140px;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(16px);
        border: 2px solid #06b6d4;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 20px rgba(6, 182, 212, 0.2);
        overflow: hidden;
        z-index: 30;
      }}
      .sub-card {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 14px 28px;
        opacity: 0;
      }}
      .strip-badge {{
        font-size: 16px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #22d3ee;
        text-transform: uppercase;
        margin-bottom: 4px;
      }}
      .strip-text {{
        font-family: 'Montserrat', sans-serif;
        font-size: 24px;
        font-weight: 900;
        line-height: 1.3;
        color: #ffffff;
      }}
      .strip-text .hl {{
        color: #facc15;
        text-shadow: 0 0 10px rgba(250, 204, 21, 0.4);
      }}

      /* ================= BOTTOM HALF: VIDEOWALL EVIDENCE (Y: 1120 to 1660) ================= */
      .bottom-videowall {{
        position: absolute;
        top: 1120px;
        left: 60px;
        right: 60px;
        height: 540px;
        background: #020617;
        border: 3px solid #1e293b;
        border-radius: 28px;
        overflow: hidden;
        box-shadow: 0 20px 45px rgba(0,0,0,0.9), inset 0 0 40px rgba(0,0,0,0.8);
      }}

      .videowall-screen {{
        position: absolute;
        inset: 0;
        padding: 40px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        opacity: 0;
      }}

      /* Screen 1: Blackwell */
      #screen-0 {{
        background: linear-gradient(135deg, #091319 0%, #031c26 100%);
        border: 2px solid #06b6d4;
        border-radius: 24px;
      }}
      /* Screen 2: Slopsquatting */
      #screen-1 {{
        background: linear-gradient(135deg, #1a0b12 0%, #2a0b15 100%);
        border: 2px solid #f43f5e;
        border-radius: 24px;
      }}
      /* Screen 3: MCP */
      #screen-2 {{
        background: linear-gradient(135deg, #0c1427 0%, #171e3d 100%);
        border: 2px solid #6366f1;
        border-radius: 24px;
      }}
      /* Screen 4: Outro */
      #screen-3 {{
        background: linear-gradient(135deg, #022c22 0%, #064e3b 100%);
        border: 2px solid #10b981;
        border-radius: 24px;
      }}

      /* ================= KEYFRAME ANIMATIONS (45.0s CLOSED) ================= */
      @keyframes animCue0 {{
        0%, 26.89% {{ opacity: 1; transform: scale(1) translateY(0); pointer-events: auto; }}
        27.56%, 100% {{ opacity: 0; transform: scale(0.97) translateY(12px); pointer-events: none; }}
      }}
      @keyframes animCue1 {{
        0%, 26.89% {{ opacity: 0; transform: scale(0.97) translateY(12px); pointer-events: none; }}
        27.56%, 53.56% {{ opacity: 1; transform: scale(1) translateY(0); pointer-events: auto; }}
        54.22%, 100% {{ opacity: 0; transform: scale(0.97) translateY(12px); pointer-events: none; }}
      }}
      @keyframes animCue2 {{
        0%, 53.56% {{ opacity: 0; transform: scale(0.97) translateY(12px); pointer-events: none; }}
        54.22%, 77.78% {{ opacity: 1; transform: scale(1) translateY(0); pointer-events: auto; }}
        78.44%, 100% {{ opacity: 0; transform: scale(0.97) translateY(12px); pointer-events: none; }}
      }}
      @keyframes animCue3 {{
        0%, 77.78% {{ opacity: 0; transform: scale(0.97) translateY(12px); pointer-events: none; }}
        78.44%, 100% {{ opacity: 1; transform: scale(1) translateY(0); pointer-events: auto; }}
      }}

      #screen-0, #sub-card-0 {{ animation: animCue0 45s linear forwards; }}
      #screen-1, #sub-card-1 {{ animation: animCue1 45s linear forwards; }}
      #screen-2, #sub-card-2 {{ animation: animCue2 45s linear forwards; }}
      #screen-3, #sub-card-3 {{ animation: animCue3 45s linear forwards; }}

      .vw-tag {{
        display: inline-block;
        padding: 8px 18px;
        font-size: 16px;
        font-weight: 900;
        letter-spacing: 2px;
        border-radius: 8px;
        text-transform: uppercase;
        width: fit-content;
      }}
      .vw-headline {{
        font-size: 38px;
        font-weight: 900;
        line-height: 1.2;
        margin: 12px 0;
      }}
      .vw-card-box {{
        background: rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.12);
        padding: 20px;
        border-radius: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        line-height: 1.4;
      }}

      /* Footer Omnichannel: Bottom 1690px */
      .footer-bar {{
        position: absolute;
        bottom: 150px;
        left: 60px;
        right: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        background: rgba(15, 23, 42, 0.85);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
      }}
      .footer-brand {{
        font-weight: 900;
        font-size: 22px;
        color: #ffffff;
      }}
      .footer-spotify {{
        color: #10b981;
        font-weight: 800;
        font-size: 20px;
        letter-spacing: 1px;
      }}
    </style>
  </head>
  <body>
    <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
      <div class="bg-grid"></div>

      <!-- Header -->
      <div class="header-bar">
        <div class="brand-badge">
          <span style="font-size: 28px;">⚡</span>
          <div class="brand-name">noti<span>sIA</span>s</div>
        </div>
        <div class="live-tag">
          <div class="live-dot"></div>
          <span>FLASH DIARIO</span>
        </div>
      </div>

      <!-- Top Half: Studio with Dalia -->
      <div class="top-studio">
        <div class="studio-halo"></div>
        <img id="dalia-img" class="dalia-avatar" src="../assets/dalia_host.png" alt="Dalia" />
        <div class="studio-desk">
          <div class="desk-label">CONDUCTORA • DALIA</div>
          <div class="desk-channel">sIA PODCAST</div>
        </div>
      </div>

      <!-- Center Strip: Dynamic Subtitles (4 Cues) -->
      <div class="center-strip">
        <div id="sub-card-0" class="sub-card">
          <div class="strip-badge">01 • HARDWARE & CLOUD</div>
          <div class="strip-text">¡Arrancamos con las <span class="hl">notisIAs</span> de hoy! En Hardware: los racks Blackwell de NVIDIA consumen 130 kW...</div>
        </div>
        <div id="sub-card-1" class="sub-card">
          <div class="strip-badge">02 • CIBERSEGURIDAD</div>
          <div class="strip-text">En Ciberseguridad: estalla el <span class="hl">Slopsquatting</span>. Librerías falsas que la IA alucina durante el Vibe Coding...</div>
        </div>
        <div id="sub-card-2" class="sub-card">
          <div class="strip-badge">03 • ARQUITECTURA & AGENTES</div>
          <div class="strip-text">Y en Arquitectura: Anthropic donó el <span class="hl">protocolo MCP</span> a la Linux Foundation. El estándar ya adoptado por OpenAI y Google...</div>
        </div>
        <div id="sub-card-3" class="sub-card">
          <div class="strip-badge">DISPONIBLE EN SPOTIFY</div>
          <div class="strip-text">El análisis a fondo de estas <span class="hl">notisIAs</span> está en Spotify y en <span class="hl">escucha-sia.github.io</span>...</div>
        </div>
      </div>

      <!-- Bottom Half: Videowall Evidence Screens -->
      <div class="bottom-videowall">
        <!-- Screen 0: Blackwell -->
        <div id="screen-0" class="videowall-screen">
          <div>
            <div class="vw-tag" style="background: #0891b2; color: #fff;">NVIDIA NVL72 • CRISIS TÉRMICA</div>
            <div class="vw-headline">130,000 Watts por Rack: El Aire ya no Enfría</div>
          </div>
          <div class="vw-card-box" style="border-left: 5px solid #06b6d4;">
            ⚡ Consumo récord: 130 kW por rack<br/>
            ❄️ Transición: Direct-to-Chip Liquid Cooling<br/>
            ⚠️ Riesgo: Fugas de fluido a 100% de carga
          </div>
        </div>

        <!-- Screen 1: Slopsquatting -->
        <div id="screen-1" class="videowall-screen">
          <div>
            <div class="vw-tag" style="background: #be123c; color: #fff;">CIBERSEGURIDAD • VIBE CODING</div>
            <div class="vw-headline">Slopsquatting: El Veneno de las Alucinaciones</div>
          </div>
          <div class="vw-card-box" style="border-left: 5px solid #f43f5e;">
            🚨 Vector: Paquetes npm/PyPI inexistentes<br/>
            🎯 Blanco: Desarrolladores en Cursor sin auditar<br/>
            🛡️ Solución: Guardrails y Zero Trust
          </div>
        </div>

        <!-- Screen 2: MCP -->
        <div id="screen-2" class="videowall-screen">
          <div>
            <div class="vw-tag" style="background: #4338ca; color: #fff;">ESTÁNDAR ABIERTO • LINUX FOUNDATION</div>
            <div class="vw-headline">Model Context Protocol: La Muerte del Caos</div>
          </div>
          <div class="vw-card-box" style="border-left: 5px solid #6366f1;">
            🔌 Arquitectura: Conector universal N+M<br/>
            🤝 Adopción: Anthropic, OpenAI, Google<br/>
            🧠 Paradigma: Single-Brain + Modular Tools
          </div>
        </div>

        <!-- Screen 3: Outro -->
        <div id="screen-3" class="videowall-screen">
          <div>
            <div class="vw-tag" style="background: #047857; color: #fff;">EPISODIO COMPLETO • SPOTIFY</div>
            <div class="vw-headline">Escucha el Debate sin Filtro en sIA Podcast</div>
          </div>
          <div class="vw-card-box" style="border-left: 5px solid #10b981;">
            🎧 Disponible en Spotify Archivos Locales<br/>
            📖 Revista digital: escucha-sia.github.io<br/>
            🚀 Suscríbete para las notisIAs diarias
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="footer-bar">
        <div class="footer-brand">sIA Podcast • México</div>
        <div class="footer-spotify">DISPONIBLE EN SPOTIFY 🟢</div>
      </div>
    </div>
  </body>
</html>"""
    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Composición Split-Screen generada en sia_tiktok_batch_engine/compositions/scene.html")

def step3_render_video():
    print("="*70)
    print("⚡ PASO 3: Renderizando video MP4 con HyperFrames GPU...")
    print("="*70)
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
    target_mp4 = REELS_DIR / OUTPUT_MP4
    spotify_mp4 = SPOTIFY_REELS_DIR / OUTPUT_MP4

    shutil.copy2(generated_mp4, target_mp4)
    shutil.copy2(generated_mp4, spotify_mp4)
    print(f"📦 Video guardado en: {target_mp4}")
    print(f"   -> Copiado a Spotify: {spotify_mp4}")

    # Poster frame
    poster_path = REELS_DIR / f"{OUTPUT_SLUG}_poster.jpg"
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

def step4_verify(target_mp4: Path):
    print("\n" + "="*70)
    print("🔍 PASO 4: Ejecutando Prueba de Terminado (DoD)...")
    print("="*70)
    verify_script = BASE_DIR / "scripts" / "verify_reel.py"
    res = subprocess.run([sys.executable, str(verify_script), str(target_mp4)])
    if res.returncode == 0:
        print("🎉 ¡PRUEBA DE TERMINADO (DoD) SUPERADA CON ÉXITO!")
    else:
        print("⚠️ Advertencia: DoD reportó detalles a revisar.")

def step5_obsidian_note():
    note_path = SHORTS_DIR / f"{OUTPUT_SLUG}.md"
    content = f"""---
id: {OUTPUT_SLUG}
titulo: "notisIAs #01 • Blackwell 130kW, Slopsquatting y MCP"
tipo: reel_notisias
formato: 1080x1920_vertical_split_screen
duracion: 45s
estado: publicado
video: "{OUTPUT_MP4}"
poster: "{OUTPUT_SLUG}_poster.jpg"
tags: [notisIAs, sia_podcast, split_screen, dalia_vtuber, tiktok]
---

# ⚡ notisIAs #01 • Las 3 del Día

> **Ficha Técnica:** notisIAs | 45.0s | Dalia Split-Screen VTuber + Videowall | Edge-TTS (+7%) | Safe Zones TikTok/IG.

## 🎥 Video
![[{OUTPUT_MP4}]]

## 🎙️ Escaleta Canónica
1. **01 • Hardware & Cloud:** Racks NVIDIA Blackwell NVL72 consumen 130 kW forzando refrigeración líquida direct-to-chip.
2. **02 • Ciberseguridad:** Crisis del Slopsquatting inyectando malware en librerías alucinadas por IA durante Vibe Coding.
3. **03 • Arquitectura & Agentes:** Donación de MCP a la Linux Foundation como nuevo estándar universal adoptado por OpenAI y Google.
4. **Cierre:** Convocatoria a Spotify y escucha-sia.github.io.
"""
    note_path.write_text(content, encoding="utf-8")
    print(f"📝 Ficha Obsidian creada: {note_path}")

async def main():
    await step1_synthesize_audio()
    step2_build_split_screen_html()
    target_mp4 = step3_render_video()
    step4_verify(target_mp4)
    step5_obsidian_note()
    print("\n🚀 ¡PILOTO DE notisIAs PRODUCIDO AL 100%!")

if __name__ == '__main__':
    asyncio.run(main())
