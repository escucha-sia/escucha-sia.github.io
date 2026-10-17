"""
sIA Motion Graphics Reel Generator: Reel #16 / Episodio #40
Tema: Tesla Roadster SpaceX Package (Cold Gas Thrusters & Aerodinámica Aeroespacial)
Duración: 45.0 Segundos CERRADOS (Producto Terminado Completo)
- Audio propio sintetizado en 45 segundos con arco narrativo completo (Jorge + Dalia).
- No es un corte truncado: inicio, tensión del neumático, diagrama vectorial de toberas y cierre.
- Redirección omnicanal total: enlaza visual y verbalmente a Spotify y al Blog con código.
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
NODE_PATH = r"C:\Carlos\nodejs"

TARGET_REEL = REELS_DIR / "sIA_Reel_16_Tesla_Roadster_SpaceX_Gas_Frio.mp4"
DURATION = 45.0

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Por qué los superdeportivos eléctricos jamás podrán bajar de uno punto cinco segundos... a menos que dejen de ser autos?"
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El asfalto tiene un límite físico insalvable: el coeficiente de fricción de los neumáticos. Por más caballos de fuerza que inyectes, las ruedas patinan y la potencia se disipa en humo."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "La solución de SpaceX es empujar el aire: diez toberas de Laval supersónicas alimentadas por tanques COPV a setecientos bar de presión. No solo acelera de cero a cien en cero punto ocho segundos: genera empuje vectorial para estabilizar el coche en curvas y saltos."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El auto murió: es una nave espacial en asfalto. Tienes el diagrama termodinámico completo en escucha-sia punto github punto io, y el debate a fondo sobre seguridad en el episodio cuarenta de Spotify."
    }
]

async def generate_reel_audio():
    print("🎙️ Sintetizando audio cerrado de 45 segundos para el Reel...")
    temp_dir = ENGINE_DIR / "temp_audio"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        communicate = edge_tts.Communicate(item["text"], item["voice"], rate="+3%")
        await communicate.save(str(chunk_path))
        chunk_files.append(chunk_path)
        
    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-af", f"apad=whole_dur={DURATION},afade=t=out:st=44.0:d=1.0",
        str(clip_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Audio del Reel sintetizado y ensamblado con éxito.")

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
        background: #030712;
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
    <div id="root" data-composition-id="sia_motion_reel_roadster" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
</html>
"""
    with open(ENGINE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    scene_html = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800;900&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html, body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #030712;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
      }
      
      .canvas-container {
        position: relative;
        width: 1080px;
        height: 1920px;
        padding: 80px 60px 100px 60px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: 
          radial-gradient(circle at 50% 15%, rgba(239, 68, 68, 0.22) 0%, transparent 60%),
          radial-gradient(circle at 80% 80%, rgba(249, 115, 22, 0.15) 0%, transparent 65%),
          linear-gradient(180deg, #030712 0%, #111827 50%, #030712 100%);
      }

      /* Grid de precisión técnica */
      .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(239, 68, 68, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(239, 68, 68, 0.06) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
      }

      /* TOP BAR */
      .header-hud {
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
      }
      .badge-series {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 10px 24px;
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid rgba(239, 68, 68, 0.5);
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #fca5a5;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.3);
      }
      .badge-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #ef4444;
        box-shadow: 0 0 14px #ef4444;
      }
      .badge-telemetry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 8px 20px;
        border-radius: 8px;
        letter-spacing: 1px;
      }

      /* HOOK CARD */
      .hook-card {
        margin-top: 30px;
        padding: 34px 40px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 28px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        z-index: 10;
      }
      .hook-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 3px;
        color: #f87171;
        text-transform: uppercase;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .hook-title {
        font-size: 38px;
        font-weight: 900;
        line-height: 1.25;
        letter-spacing: -0.5px;
        color: #ffffff;
      }
      .hook-title .alert-hl {
        color: #f97316;
        text-shadow: 0 0 20px rgba(249, 115, 22, 0.7);
      }

      /* HERO STAGE: 3 ACTOS EN GSAP */
      .hero-stage {
        position: relative;
        width: 100%;
        height: 820px;
        margin-top: 25px;
        border-radius: 32px;
        background: rgba(15, 23, 42, 0.90);
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.8);
        overflow: hidden;
        z-index: 10;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
      .stage-header {
        position: absolute;
        top: 24px;
        left: 32px;
        right: 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #f87171;
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 20;
      }

      /* ACT 1: TIRE FRICTION SATURATION */
      .friction-container {
        position: absolute;
        width: 860px;
        height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      /* ACT 2: SPACEX COPV & THRUSTERS BLUEPRINT */
      .spacex-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
      }
      .spacex-svg {
        width: 860px;
        height: 640px;
      }

      /* ACT 3: OMNICHANNEL FLYWHEEL CTA */
      .flywheel-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 24px;
        padding: 40px;
        opacity: 0;
        z-index: 30;
      }
      .flywheel-card {
        width: 100%;
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid rgba(239, 68, 68, 0.6);
        border-radius: 20px;
        padding: 24px 32px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
      }
      .card-icon {
        font-size: 40px;
      }
      .card-info {
        display: flex;
        flex-direction: column;
      }
      .card-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
      }
      .card-desc {
        font-family: 'JetBrains Mono', monospace;
        font-size: 16px;
        color: #fca5a5;
        margin-top: 4px;
      }

      /* BADGES & TELEMETRY */
      .metrics-grid {
        position: absolute;
        bottom: 30px;
        left: 32px;
        right: 32px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        z-index: 20;
      }
      .metric-badge {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 16px 20px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
      }
      .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 800;
        color: #f97316;
        letter-spacing: -1px;
      }
      .metric-desc {
        font-size: 17px;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 4px;
      }

      /* SUBTITLES & AUDIO CARD */
      .subtitles-card {
        margin-top: 25px;
        padding: 30px 40px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-radius: 28px;
        backdrop-filter: blur(20px);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        z-index: 10;
      }
      .speaker-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #f87171;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .subtitles-text {
        font-size: 30px;
        font-weight: 700;
        line-height: 1.35;
        color: #f8fafc;
        margin-top: 10px;
      }

      /* AUDIO WAVEFORM */
      .waveform-row {
        margin-top: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        height: 48px;
      }
      .bar {
        width: 8px;
        height: 16px;
        background: linear-gradient(180deg, #ef4444, #f97316);
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
      }

      /* FOOTER / SPOTIFY CTA */
      .footer-cta {
        margin-top: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 36px;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        z-index: 10;
      }
      .spotify-brand {
        display: flex;
        align-items: center;
        gap: 16px;
      }
      .spotify-logo {
        width: 44px;
        height: 44px;
        fill: #1db954;
      }
      .brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
      }
      .brand-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        color: #94a3b8;
      }
      .action-pill {
        padding: 14px 28px;
        background: #dc2626;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.6);
      }
    </style>
  </head>
  <body>
    <div id="scene-root" class="canvas-container" data-composition-id="scene" data-width="1080" data-height="1920">
      <div class="grid-overlay"></div>

      <!-- TOP BAR -->
      <div class="header-hud">
        <div class="badge-series">
          <div class="badge-dot"></div>
          sIA #40 • AEROESPACIAL
        </div>
        <div class="badge-telemetry">
          TESLA ROADSTER // SPACEX
        </div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card" id="hookCard">
        <div class="hook-label">
          <span>🚀</span> FÍSICA DE PROPULSIÓN & TRACCIÓN EXTREMA
        </div>
        <div class="hook-title">
          "¿Por qué los superdeportivos jamás bajarán de 1.5s... <span class="alert-hl">a menos que dejen de ser autos</span>?"
        </div>
      </div>

      <!-- HERO STAGE: 3 ACTOS EN GSAP -->
      <div class="hero-stage" id="heroStage">
        <div class="stage-header">
          <span id="stageTitle">LÍMITE DE ADHERENCIA NEUMÁTICO-ASFALTO</span>
          <span id="stageTelemetry">COEFICIENTE μ: SATURADO</span>
        </div>

        <!-- ACT 1: Tire Friction Saturation -->
        <div class="friction-container" id="frictionContainer">
          <svg width="800" height="460" viewBox="0 0 800 460">
            <!-- Road Line -->
            <line x1="50" y1="340" x2="750" y2="340" stroke="#64748b" stroke-width="4"/>
            <line x1="50" y1="346" x2="750" y2="346" stroke="#f97316" stroke-width="2" stroke-dasharray="10 8"/>

            <!-- Spinning Tire Vector -->
            <circle cx="280" cy="240" r="100" fill="#0f172a" stroke="#f87171" stroke-width="8"/>
            <circle cx="280" cy="240" r="50" fill="#1e293b" stroke="#ffffff" stroke-width="3"/>
            <circle cx="280" cy="240" r="15" fill="#f97316"/>
            <!-- Tire treads -->
            <line x1="280" y1="140" x2="280" y2="160" stroke="#f87171" stroke-width="6"/>
            <line x1="280" y1="320" x2="280" y2="340" stroke="#f87171" stroke-width="6"/>
            <line x1="180" y1="240" x2="200" y2="240" stroke="#f87171" stroke-width="6"/>
            <line x1="360" y1="240" x2="380" y2="240" stroke="#f87171" stroke-width="6"/>

            <!-- Friction Curve on Right -->
            <line x1="480" y1="100" x2="480" y2="320" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
            <line x1="480" y1="320" x2="750" y2="320" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
            <text x="470" y="110" fill="#f87171" font-family="JetBrains Mono" font-size="14" text-anchor="end">FUERZA (N)</text>
            <text x="750" y="350" fill="#94a3b8" font-family="JetBrains Mono" font-size="14" text-anchor="end">SLIP RATIO →</text>

            <path id="frictionCurve" d="M 480,320 Q 550,140 600,160 T 740,200" fill="none" stroke="#ef4444" stroke-width="4.5"/>
            <circle cx="600" cy="160" r="8" fill="#ef4444"/>
            <text x="615" y="150" fill="#fca5a5" font-family="JetBrains Mono" font-size="16" font-weight="800">LÍMITE: 1.6s</text>

            <!-- Alert banner -->
            <rect x="180" y="380" width="440" height="50" rx="12" fill="rgba(220, 38, 38, 0.2)" stroke="#ef4444" stroke-width="2"/>
            <text x="400" y="412" fill="#fee2e2" font-family="JetBrains Mono" font-size="17" text-anchor="middle" font-weight="800">⚠️ DESLIZAMIENTO: EL CAUCHO NO PUEDE MÁS</text>
          </svg>
        </div>

        <!-- ACT 2: SpaceX COPV & 10 Thrusters Blueprint -->
        <div class="spacex-container" id="spacexContainer">
          <svg class="spacex-svg" viewBox="0 0 860 640">
            <defs>
              <linearGradient id="thrusterBlast" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ef4444" stop-opacity="0.9"/>
                <stop offset="50%" stop-color="#f97316" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#fbbf24" stop-opacity="0"/>
              </linearGradient>
            </defs>

            <!-- Car Top-Down Chassis Wireframe -->
            <rect x="220" y="140" width="420" height="240" rx="40" fill="#0f172a" stroke="#f97316" stroke-width="3"/>
            <polygon points="220,190 280,160 580,160 640,190" fill="#1e293b"/>
            
            <!-- Carbon Fiber COPV Tanks (Center/Rear) -->
            <rect x="260" y="210" width="160" height="100" rx="20" fill="#1e1b4b" stroke="#38bdf8" stroke-width="2.5"/>
            <text x="340" y="255" fill="#38bdf8" font-family="JetBrains Mono" font-size="16" text-anchor="middle" font-weight="900">COPV TANKS</text>
            <text x="340" y="280" fill="#e0f2fe" font-family="JetBrains Mono" font-size="14" text-anchor="middle">700 BAR (10K PSI)</text>

            <!-- 2 Rear Supersonic Thrusters -->
            <polygon points="220,220 180,200 180,250" fill="#f97316"/>
            <polygon points="220,270 180,250 180,300" fill="#f97316"/>

            <!-- Supersonic Mach Expansion Plumes -->
            <polygon id="plume1" points="180,225 30,195 30,255" fill="url(#thrusterBlast)"/>
            <polygon id="plume2" points="180,275 30,245 30,305" fill="url(#thrusterBlast)"/>
            <text x="110" y="255" fill="#ffffff" font-family="JetBrains Mono" font-size="18" font-weight="900">MACH 1+</text>

            <!-- Perimeter Attitude Thrusters (Corners) -->
            <circle cx="250" cy="150" r="12" fill="#ef4444"/>
            <circle cx="610" cy="150" r="12" fill="#ef4444"/>
            <circle cx="250" cy="370" r="12" fill="#ef4444"/>
            <circle cx="610" cy="370" r="12" fill="#ef4444"/>

            <text x="430" y="440" fill="#fca5a5" font-family="JetBrains Mono" font-size="18" font-weight="800" text-anchor="middle">10 TOBERAS DE LAVAL // CONTROL DE ACTITUD ACS</text>
          </svg>
        </div>

        <!-- ACT 3: Omnichannel Flywheel Card -->
        <div class="flywheel-container" id="flywheelContainer">
          <div class="flywheel-card">
            <div class="card-icon">🎧</div>
            <div class="card-info">
              <span class="card-title">sIA Podcast en Spotify</span>
              <span class="card-desc">Episodio #40: El debate de homologación y seguridad vial</span>
            </div>
          </div>
          <div class="flywheel-card" style="border-color: #38bdf8;">
            <div class="card-icon">📖</div>
            <div class="card-info">
              <span class="card-title">Revista Técnica Digital</span>
              <span class="card-desc">escucha-sia.github.io • Ecuaciones de empuje y fuentes APA</span>
            </div>
          </div>
        </div>

        <!-- Telemetry Metrics Grid -->
        <div class="metrics-grid">
          <div class="metric-badge">
            <span class="metric-value">0.8 s</span>
            <span class="metric-desc">0 a 100 km/h (Sub-1s)</span>
          </div>
          <div class="metric-badge">
            <span class="metric-value">700 Bar</span>
            <span class="metric-desc">Presión en Tanques COPV</span>
          </div>
        </div>
      </div>

      <!-- SUBTITLES & AUDIO CARD -->
      <div class="subtitles-card">
        <div class="speaker-tag" id="speakerTag">
          <span>🎙️</span> JORGE (ANÁLISIS MECATRÓNICO)
        </div>
        <div class="subtitles-text" id="subtitlesText">
          "¿Por qué los superdeportivos eléctricos jamás podrán bajar de 1.5 segundos... a menos que dejen de ser autos?"
        </div>
        <div class="waveform-row" id="waveform">
          <!-- 28 bars -->
        </div>
      </div>

      <!-- FOOTER / SPOTIFY CTA -->
      <div class="footer-cta">
        <div class="spotify-brand">
          <svg class="spotify-logo" viewBox="0 0 24 24">
            <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.503 17.308c-.218.358-.684.472-1.042.254-2.855-1.745-6.45-2.14-10.684-1.173-.408.093-.816-.162-.909-.57-.093-.408.162-.816.57-.909 4.637-1.06 8.604-.616 11.811 1.356.358.218.472.684.254 1.042zm1.47-3.268c-.275.448-.863.593-1.311.318-3.268-2.01-8.25-2.593-12.116-1.419-.505.153-1.043-.134-1.196-.639-.153-.505.134-1.043.639-1.196 4.417-1.341 9.907-.696 13.666 1.625.448.275.593.863.318 1.311zm.126-3.41c-3.918-2.327-10.37-2.542-14.103-1.408-.601.183-1.24-.162-1.423-.763-.183-.601.162-1.24.763-1.423 4.288-1.302 11.411-1.053 15.918 1.623.541.321.718 1.026.397 1.567-.321.541-1.026.718-1.567.397z"/>
          </svg>
          <div>
            <div class="brand-title">sIA Podcast en Spotify</div>
            <div class="brand-sub">escucha-sia.github.io</div>
          </div>
        </div>
        <div class="action-pill">
          ESCUCHAR EPISODIO #40
        </div>
      </div>
    </div>

    <script>
      // 1. Build Reactive Waveform
      const waveContainer = document.getElementById("waveform");
      const barCount = 28;
      const bars = [];
      for (let i = 0; i < barCount; i++) {
        const b = document.createElement("div");
        b.className = "bar";
        waveContainer.appendChild(b);
        bars.push(b);
      }

      // 2. Animate Waveform
      bars.forEach((bar, index) => {
        gsap.to(bar, {
          height: gsap.utils.random(14, 46),
          duration: gsap.utils.random(0.2, 0.45),
          repeat: -1,
          yoyo: true,
          ease: "power1.inOut",
          delay: index * 0.02
        });
      });

      // 3. Pulsing Thruster Plumes
      gsap.to(["#plume1", "#plume2"], {
        scaleX: 1.15,
        opacity: 0.6,
        transformOrigin: "right center",
        duration: 0.25,
        repeat: -1,
        yoyo: true,
        ease: "power2.inOut"
      });

      // 4. MASTER TIMELINE FOR 45 SECONDS (Producto Terminado)
      const tl = gsap.timeline();

      // ACT 1 (0.0s - 18.0s): El límite del caucho
      tl.from(".header-hud", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
      tl.from("#hookCard", { scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.4);
      tl.from("#frictionContainer", { scale: 0.85, opacity: 0, duration: 1.0, ease: "power3.out" }, 0.6);
      tl.from("#frictionCurve", { strokeDashoffset: 600, duration: 3.0, ease: "power2.out" }, 1.5);

      // Subtitles Sync Act 1
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "¿Por qué los superdeportivos eléctricos jamás podrán bajar de 1.5 segundos... a menos que dejen de ser autos?";
      }, null, 0.2);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "El asfalto tiene un límite físico: el coeficiente de fricción de los neumáticos. Las ruedas patinan y la potencia se disipa en humo.";
      }, null, 6.5);

      // TRANSITION TO ACT 2 (18.0s): Dalia presenta las toberas SpaceX
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> DALIA (INGENIERÍA AEROESPACIAL)";
        document.getElementById("stageTitle").innerHTML = "PROPULSIÓN DE GAS FRÍO // COPV & LAVAL";
        document.getElementById("stageTelemetry").innerHTML = "PRESIÓN: 700 BAR • 10 TOBERAS ACS";
      }, null, 18.0);

      // Fade out Friction, Fade in SpaceX
      tl.to("#frictionContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 18.0);
      tl.to("#spacexContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 18.7);

      // Subtitles Act 2
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "La solución de SpaceX es empujar el aire: diez toberas de Laval supersónicas alimentadas por tanques COPV a setecientos bar...";
      }, null, 18.5);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "<span style='color: #f97316; font-weight: 800;'>...acelera de cero a cien en 0.8s y genera empuje vectorial para estabilizar el coche en curvas y saltos.</span>";
      }, null, 26.0);

      // TRANSITION TO ACT 3 (34.0s - 45.0s): Cierre de Ingeniería & Flywheel Omnicanal
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> JORGE & DALIA (VEREDICTO)";
        document.getElementById("stageTitle").innerHTML = "VEREDICTO & REDIRECCIÓN OMNICANAL";
        document.getElementById("stageTelemetry").innerHTML = "RECURSOS Y DEBATE COMPLETO";
      }, null, 34.0);

      // Fade out SpaceX Blueprint, Fade in Flywheel Card
      tl.to("#spacexContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 34.0);
      tl.to("#flywheelContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 34.7);

      // Subtitles Act 3
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "El auto murió: es una nave espacial en asfalto. Diagrama completo en escucha-sia.github.io y debate en el episodio 40 de Spotify.";
      }, null, 34.5);
    </script>
  </body>
</html>
"""
    with open(ENGINE_DIR / "compositions" / "scene.html", "w", encoding="utf-8") as f:
        f.write(scene_html)
    print("📝 Archivos index.html y compositions/scene.html generados.")

def render_with_hyperframes():
    print("⚡ Ejecutando HyperFrames GPU render (45 segundos)...")
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    
    cmd = [
        "cmd.exe", "/c",
        f"cd /d {ENGINE_DIR} && npx hyperframes render --gpu"
    ]
    res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error en HyperFrames render:\n{res.stderr}\n{res.stdout}")
        sys.exit(1)
        
    generated_mp4 = ENGINE_DIR / "renders" / "index.mp4"
    if not generated_mp4.exists():
        potential = sorted(list((ENGINE_DIR / "renders").glob("sia_tiktok_batch_engine_*.mp4")), key=os.path.getmtime, reverse=True)
        if potential:
            generated_mp4 = potential[0]
        else:
            print("❌ No se encontró el archivo mp4 renderizado.")
            sys.exit(1)
            
    shutil.copy2(generated_mp4, TARGET_REEL)
    shutil.copy2(generated_mp4, SPOTIFY_REELS_DIR / TARGET_REEL.name)
    
    poster_path = REELS_DIR / (TARGET_REEL.stem + "_poster.jpg")
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "26.0",
        "-i", str(TARGET_REEL),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    size_mb = os.path.getsize(TARGET_REEL) / (1024 * 1024)
    print(f"✅ ¡Video Motion Graphics generado con éxito! ({size_mb:.2f} MB)")
    print(f"   -> {TARGET_REEL}")
    print(f"   -> Póster en: {poster_path}")

async def main():
    print("=" * 60)
    print("🎬 RENDERIZANDO VIDEO MOTION GRAPHICS: sIA #40 (TESLA ROADSTER SPACEX)")
    print("=" * 60)
    await generate_reel_audio()
    write_hyperframes_html()
    render_with_hyperframes()

if __name__ == "__main__":
    asyncio.run(main())
