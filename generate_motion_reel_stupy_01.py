"""
sIA Stupy-Style Motion Reel Generator:
Tema: El Mito de la IA y el Código (Copiar y pegar código te hace 10x más rápido. ¿O no?)
Estilo Visual: Cómic-Pop / Halftone Dot Matrix / Simetría Vectorial / Kinetic Typography / Pop-in Accents
Duración: 45.0 Segundos
"""

import os
import sys
import shutil
import asyncio
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
NODE_PATH = r"C:\Program Files\nodejs"

TARGET_REEL = REELS_DIR / "sIA_Reel_Stupy_01_Mito_IA_Codigo.mp4"
DURATION = 45.0

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Copiar código de la Inteligencia Artificial te hace diez veces más productivo? Eso es lo que prometen en Twitter y Silicon Valley..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Pero un estudio de Stanford y GitHub reveló la letra chiquita: programas cincuenta y cinco por ciento más rápido, sí... ¡pero introduces cuarenta y un por ciento más de fallos de seguridad y deuda técnica invisible!"
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Es la trampa de la ilusión de competencia: generar cien líneas de código que no entiendes tarda treinta segundos. Pero depurar una alucinación a las tres de la mañana te cuesta cuatro horas y la caída del servidor."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "La IA no sustituye tu criterio técnico; solo multiplica la velocidad a la que cometes errores. Aprende a programar con arquitectura real en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def generate_reel_audio():
    print("🎙️ Sintetizando audio cerrado de 45 segundos estilo Stupy-Doo...")
    temp_dir = ENGINE_DIR / "temp_audio_stupy_01"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        clean_text = item["text"].replace("Sia", "Sia").replace("sIA", "Sia")
        communicate = edge_tts.Communicate(clean_text, item["voice"], rate="+6%")
        await communicate.save(str(chunk_path))
        chunk_files.append(chunk_path)
        
    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate background bed with subtle audio tension and loudness normalization
    music_src = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-stream_loop", "-1", "-i", str(music_src),
        "-filter_complex",
        f"[1:a]volume=0.032,afade=t=in:st=0:d=1.0,afade=t=out:st=43.5:d=1.5[bg];"
        f"[0:a]apad=whole_dur={DURATION}[vox];"
        f"[vox][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,"
        f"acompressor=threshold=-20dB:ratio=2.5:attack=15:release=120,"
        f"loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-t", str(DURATION),
        str(clip_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Audio cerrado de 45 segundos procesado con éxito.")

def write_hyperframes_html():
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
    <div id="root" data-composition-id="sia_motion_reel_stupy_01" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{DURATION}"
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
        data-duration="{DURATION}"
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
        color: #0b0d17;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* 1. HALFTONE COMIC PATTERN BACKGROUND */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(255, 255, 255, 0.12) 2px, transparent 2px);
        background-size: 26px 26px;
        opacity: 0.85;
        z-index: 1;
      }}

      /* 2. GIANT BACKGROUND GHOST WATERMARK TICKER */
      .bg-ticker {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        font-size: 130px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.04);
        line-height: 1.0;
        letter-spacing: -2px;
        pointer-events: none;
        z-index: 2;
        transform: rotate(-12deg) scale(1.2);
        animation: tickerDrift 45s linear infinite;
      }}
      @keyframes tickerDrift {{
        0% {{ transform: rotate(-12deg) translateY(0); }}
        50% {{ transform: rotate(-12deg) translateY(-80px); }}
        100% {{ transform: rotate(-12deg) translateY(0); }}
      }}

      /* 3. SYMMETRICAL ORGANIC VECTOR FRAMING (STUPY DOO BORDER) */
      .comic-frame-left, .comic-frame-right {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 140px;
        z-index: 5;
        pointer-events: none;
      }}
      .comic-frame-left {{
        left: 0;
        background: radial-gradient(circle at 0% 50%, rgba(255, 87, 34, 0.15), transparent 70%);
      }}
      .comic-frame-right {{
        right: 0;
        background: radial-gradient(circle at 100% 50%, rgba(255, 87, 34, 0.15), transparent 70%);
      }}

      /* Stylized Ink Lines on Borders */
      .ink-bracket {{
        position: absolute;
        stroke: #ffffff;
        stroke-width: 8;
        fill: none;
        stroke-linecap: round;
        filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.2));
      }}

      /* 4. TOP BRAND BAR */
      .brand-bar {{
        position: absolute;
        top: 70px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 16px;
        background: #000;
        border: 4px solid #fff;
        padding: 12px 32px;
        border-radius: 999px;
        box-shadow: 6px 6px 0px #ff4500;
        z-index: 20;
      }}
      .brand-dot {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #ff4500;
        animation: pulseDot 1s infinite alternate;
      }}
      @keyframes pulseDot {{
        0% {{ transform: scale(0.85); opacity: 0.7; }}
        100% {{ transform: scale(1.2); opacity: 1; }}
      }}
      .brand-title {{
        color: #fff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900;
        font-size: 26px;
        letter-spacing: 2px;
      }}

      /* 5. CENTER HERO CARD (COMIC SHIELD / OVAL) */
      .center-shield {{
        position: absolute;
        top: 220px;
        left: 50%;
        transform: translateX(-50%);
        width: 900px;
        height: 1420px;
        background: #f8fafc;
        border-radius: 48px;
        border: 7px solid #000;
        box-shadow: 20px 20px 0px rgba(0, 0, 0, 0.95);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 70px 50px 60px 50px;
        z-index: 10;
        overflow: hidden;
      }}

      /* Inner Halftone on Shield */
      .center-shield::before {{
        content: "";
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(0, 0, 0, 0.05) 1.5px, transparent 1.5px);
        background-size: 16px 16px;
        pointer-events: none;
      }}

      /* SCENE WRAPPER & VISIBILITY CONTROL */
      .scene {{
        position: absolute;
        inset: 60px 40px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        text-align: center;
        opacity: 0;
        transform: scale(0.92);
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
        pointer-events: none;
      }}

      /* TIMELINE VISIBILITY (45s TOTAL) */
      /* Scene 1: 0s to 8.5s (The Myth) */
      @keyframes showScene1 {{
        0% {{ opacity: 0; transform: scale(0.85); }}
        2% {{ opacity: 1; transform: scale(1); }}
        18% {{ opacity: 1; transform: scale(1); }}
        20% {{ opacity: 0; transform: scale(1.08); }}
        100% {{ opacity: 0; }}
      }}
      #scene-1 {{
        animation: showScene1 45s forwards;
      }}

      /* Scene 2: 8.5s to 20.5s (The Stanford & GitHub Research) */
      @keyframes showScene2 {{
        0%, 19% {{ opacity: 0; transform: scale(0.85); }}
        21% {{ opacity: 1; transform: scale(1); }}
        44% {{ opacity: 1; transform: scale(1); }}
        46% {{ opacity: 0; transform: scale(1.08); }}
        100% {{ opacity: 0; }}
      }}
      #scene-2 {{
        animation: showScene2 45s forwards;
      }}

      /* Scene 3: 20.5s to 33.5s (The 3 AM Hallucination Trap) */
      @keyframes showScene3 {{
        0%, 45% {{ opacity: 0; transform: scale(0.85); }}
        47% {{ opacity: 1; transform: scale(1); }}
        73% {{ opacity: 1; transform: scale(1); }}
        75% {{ opacity: 0; transform: scale(1.08); }}
        100% {{ opacity: 0; }}
      }}
      #scene-3 {{
        animation: showScene3 45s forwards;
      }}

      /* Scene 4: 33.5s to 45s (The Truth & CTA) */
      @keyframes showScene4 {{
        0%, 74% {{ opacity: 0; transform: scale(0.85); }}
        76% {{ opacity: 1; transform: scale(1); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
      #scene-4 {{
        animation: showScene4 45s forwards;
      }}

      /* TYPOGRAPHY COMPONENTS (STUPY STYLE) */
      .myth-tag {{
        font-family: 'Space Grotesk', sans-serif;
        background: #000;
        color: #fff;
        font-size: 26px;
        font-weight: 800;
        padding: 10px 24px;
        border-radius: 12px;
        letter-spacing: 2px;
        display: inline-block;
        box-shadow: 4px 4px 0px #ff4500;
      }}

      .headline-black {{
        font-size: 64px;
        font-weight: 900;
        line-height: 1.08;
        color: #05070d;
        text-transform: uppercase;
        letter-spacing: -1px;
        margin: 20px 0;
      }}

      .punch-pill {{
        background: #ff4500;
        color: #fff !important;
        font-size: 72px;
        font-weight: 900;
        padding: 16px 40px;
        border-radius: 16px;
        display: inline-block;
        border: 5px solid #000;
        box-shadow: 8px 8px 0px #000;
        transform: rotate(-3deg);
        animation: popPunch 0.8s infinite alternate ease-in-out;
      }}
      @keyframes popPunch {{
        0% {{ transform: rotate(-3deg) scale(0.98); }}
        100% {{ transform: rotate(-3deg) scale(1.04); }}
      }}

      /* METRIC DUAL CARDS (SCENE 2) */
      .metric-grid {{
        display: flex;
        flex-direction: column;
        gap: 24px;
        width: 100%;
        margin-top: 10px;
      }}
      .metric-card {{
        background: #fff;
        border: 5px solid #000;
        border-radius: 24px;
        padding: 24px 30px;
        box-shadow: 8px 8px 0px #000;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }}
      .metric-card.good {{
        border-color: #059669;
        box-shadow: 8px 8px 0px #059669;
      }}
      .metric-card.danger {{
        border-color: #dc2626;
        box-shadow: 8px 8px 0px #dc2626;
      }}
      .metric-val {{
        font-size: 68px;
        font-weight: 900;
      }}
      .metric-val.green {{ color: #059669; }}
      .metric-val.red {{ color: #dc2626; }}
      .metric-desc {{
        font-size: 32px;
        font-weight: 800;
        text-align: right;
        color: #000;
        line-height: 1.15;
      }}

      /* COMPARISON ROW (SCENE 3) */
      .compare-box {{
        background: #000;
        color: #fff;
        border-radius: 24px;
        padding: 30px 36px;
        width: 100%;
        text-align: left;
        box-shadow: 10px 10px 0px #ff4500;
        border: 4px solid #fff;
        font-family: 'JetBrains Mono', monospace;
      }}
      .code-line {{
        font-size: 28px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 16px;
      }}
      .tag-fast {{
        background: #10b981;
        color: #000;
        padding: 4px 14px;
        border-radius: 6px;
        font-weight: 900;
        font-size: 22px;
      }}
      .tag-slow {{
        background: #ef4444;
        color: #fff;
        padding: 4px 14px;
        border-radius: 6px;
        font-weight: 900;
        font-size: 22px;
      }}

      /* FOOTER CALL TO ACTION (SCENE 4) */
      .final-pill {{
        background: #000;
        color: #00f0ff;
        border: 5px solid #00f0ff;
        padding: 20px 40px;
        border-radius: 20px;
        font-size: 34px;
        font-weight: 900;
        box-shadow: 8px 8px 0px #00f0ff;
        margin-top: 20px;
        letter-spacing: 1px;
      }}

      /* BOTTOM PROGRESS BAR */
      .progress-bar-container {{
        position: absolute;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 860px;
        height: 14px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 999px;
        overflow: hidden;
        z-index: 20;
      }}
      .progress-fill {{
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #ff4500, #00f0ff);
        animation: fillProgress 45s linear forwards;
      }}
      @keyframes fillProgress {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}
    </style>
  </head>
  <body>
    <!-- 1. Halftone comic overlay -->
    <div class="halftone-overlay"></div>

    <!-- 2. Giant ghost typography ticker -->
    <div class="bg-ticker">
      <div>ILUSIÓN DE COMPETENCIA</div>
      <div>IA & CÓDIGO 10X</div>
      <div>ALUCINACIÓN A LAS 3 AM</div>
      <div>DEUDA TÉCNICA INVISIBLE</div>
      <div>SIA TECH MEDIA</div>
    </div>

    <!-- 3. Symmetrical organic comic frames -->
    <div class="comic-frame-left"></div>
    <div class="comic-frame-right"></div>

    <!-- 4. Top Brand Pill -->
    <div class="brand-bar">
      <div class="brand-dot"></div>
      <div class="brand-title">SIA • DESMINTIENDO EL HYPE</div>
    </div>

    <!-- 5. Center Comic Shield Card -->
    <div class="center-shield">
      
      <!-- SCENE 1: EL MITO (0s - 8.5s) -->
      <div class="scene" id="scene-1">
        <div class="myth-tag">EL MITO DE SILICON VALLEY</div>
        <div class="headline-black">
          COPIAR CÓDIGO CON IA<br>TE HACE 10 VECES<br>MÁS RÁPIDO
        </div>
        <div class="punch-pill">¿O NO? 🤖</div>
        <div style="font-size: 32px; font-weight: 800; color: #64748b; margin-top: 20px;">
          Lo que dicen en Twitter...
        </div>
      </div>

      <!-- SCENE 2: LA INVESTIGACIÓN CIENTÍFICA (8.5s - 20.5s) -->
      <div class="scene" id="scene-2">
        <div class="myth-tag" style="background: #1e293b; box-shadow: 4px 4px 0px #38bdf8;">ESTUDIO GITHUB & STANFORD</div>
        <div class="headline-black" style="font-size: 56px;">
          LA LETRA CHIQUITA<br>DEL COPILOTO
        </div>
        <div class="metric-grid">
          <div class="metric-card good">
            <span class="metric-val green">+55%</span>
            <span class="metric-desc">VELOCIDAD<br>DE ESCRITURA</span>
          </div>
          <div class="metric-card danger">
            <span class="metric-val red">+41%</span>
            <span class="metric-desc">FALLOS DE<br>SEGURIDAD</span>
          </div>
        </div>
        <div style="background: #fee2e2; border: 3px solid #ef4444; color: #b91c1c; padding: 12px 24px; border-radius: 12px; font-weight: 900; font-size: 26px; margin-top: 10px;">
          ⚠️ DEUDA TÉCNICA INVISIBLE
        </div>
      </div>

      <!-- SCENE 3: LA TRAMPA DE LA ILUSIÓN (20.5s - 33.5s) -->
      <div class="scene" id="scene-3">
        <div class="myth-tag" style="background: #7c2d12; box-shadow: 4px 4px 0px #ea580c;">PSICOLOGÍA DEL SOFTWARE</div>
        <div class="headline-black" style="font-size: 52px;">
          LA ILUSIÓN DE<br>COMPETENCIA
        </div>
        <div class="compare-box">
          <div class="code-line">
            <span class="tag-fast">30 SEG</span>
            <span>Generar 100 líneas con IA</span>
          </div>
          <div style="border-top: 2px dashed #475569; margin: 16px 0;"></div>
          <div class="code-line">
            <span class="tag-slow">4 HORAS</span>
            <span>Depurar el bug a las 3 AM</span>
          </div>
        </div>
        <div style="font-size: 34px; font-weight: 900; color: #dc2626; margin-top: 15px;">
          💥 Y el servidor colapsado.
        </div>
      </div>

      <!-- SCENE 4: LA VERDAD Y LLAMADA A LA ACCIÓN (33.5s - 45s) -->
      <div class="scene" id="scene-4">
        <div class="myth-tag" style="background: #0f172a; box-shadow: 4px 4px 0px #06b6d4;">LA REGLA DE ORO</div>
        <div class="headline-black" style="font-size: 58px;">
          LA IA NO SUSTITUYE<br>TU PENSAMIENTO
        </div>
        <div class="punch-pill" style="font-size: 42px; background: #000; border-color: #ff4500; color: #ff4500 !important; box-shadow: 8px 8px 0px #ff4500;">
          SOLO MULTIPLICA TUS ERRORES
        </div>
        <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 20px;">
          Aprende arquitectura real en:
        </div>
        <div class="final-pill">
          ESCUCHA-SIA.GITHUB.IO
        </div>
      </div>

    </div>

    <!-- 6. Bottom Progress Bar -->
    <div class="progress-bar-container">
      <div class="progress-fill"></div>
    </div>
  </body>
</html>"""

    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Plantilla HyperFrames en estilo Cómic-Pop / Stupy generada con éxito.")

def render_motion_reel():
    print("🎬 Renderizando Reel estilo Stupy en HyperFrames GPU...")
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
        raise RuntimeError(f"Fallo al renderizar Reel en HyperFrames: {res.stderr}")
    
    output_mp4 = ENGINE_DIR / "renders" / "video.mp4"
    if not output_mp4.exists():
        candidates = list((ENGINE_DIR / "renders").glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
            
    if not output_mp4.exists():
        raise RuntimeError(f"Fallo al renderizar Reel: {res.stderr or res.stdout}")
        
    REELS_DIR.mkdir(parents=True, exist_ok=True)
    SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(output_mp4, TARGET_REEL)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / TARGET_REEL.name)
    
    size_mb = TARGET_REEL.stat().st_size / (1024 * 1024)
    print(f"✅ ¡Video Stupy-Style generado con éxito! ({size_mb:.2f} MB)")
    print(f"   -> {TARGET_REEL}")
    
    poster_path = REELS_DIR / f"{TARGET_REEL.stem}_poster.jpg"
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "00:00:04",
        "-i", str(TARGET_REEL),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if poster_path.exists():
        shutil.copy2(poster_path, SPOTIFY_REELS_DIR / poster_path.name)
        print(f"   -> Póster capturado en: {poster_path}")

async def run():
    await generate_reel_audio()
    write_hyperframes_html()
    render_motion_reel()
    print("\n🎉 ¡Prototipo Stupy-Style listo!")

if __name__ == '__main__':
    asyncio.run(run())
