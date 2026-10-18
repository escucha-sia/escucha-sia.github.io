"""
sIA Motion Graphics Reel Generator: Reel #08 (Data Contracts Semánticos)
Tema: Data Contracts Semánticos: Blindando Pipelines contra Mutaciones de Esquema
Duración: 45.0 Segundos CERRADOS (Producto Terminado Completo)
- Audio propio sintetizado en 45 segundos con arco narrativo completo (Jorge + Dalia).
- No es un corte truncado: inicio, pesadilla del pipeline roto a las 3am, YAML Gate & DLQ, y cierre.
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

TARGET_REEL = REELS_DIR / "sIA_Reel_08_Data_Contratos_Semanticos.mp4"
DURATION = 45.0

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Por qué los equipos de datos siguen despertando a las tres de la mañana por pipelines destruidos en producción?"
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Cualquier cambio imprevisto en la base de origen muta silenciosamente el esquema, corrompe las tablas de Snowflake o BigQuery y derrumba los tableros de métricas del negocio."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "La solución son los Data Contracts semánticos: especificaciones YAML declarativas y validación en CI/CD que interceptan anomalías en menos de cinco milisegundos, aislando paquetes corruptos en una Dead Letter Queue."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Aprende a implementar contratos semánticos con dbt en escucha guion sia punto github punto io, y escucha el análisis técnico en el episodio treinta y cinco de Spotify."
    }
]

async def generate_reel_audio():
    print("🎙️ Sintetizando audio cerrado de 45 segundos para el Reel #08...")
    temp_dir = ENGINE_DIR / "temp_audio_data"
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
    print("✅ Audio del Reel #08 sintetizado y ensamblado con éxito.")

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
        background: #090514;
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
    <div id="root" data-composition-id="sia_motion_reel_data" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
        background: #090514;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f5f3ff;
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
          radial-gradient(circle at 50% 15%, rgba(168, 85, 247, 0.22) 0%, transparent 60%),
          radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 65%),
          linear-gradient(180deg, #090514 0%, #150d2a 50%, #090514 100%);
      }

      /* Grid de arquitectura de datos */
      .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(168, 85, 247, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(168, 85, 247, 0.06) 1px, transparent 1px);
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
        background: rgba(168, 85, 247, 0.18);
        border: 1px solid rgba(168, 85, 247, 0.5);
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #d8b4fe;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.3);
      }
      .badge-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #a855f7;
        box-shadow: 0 0 14px #a855f7;
      }
      .badge-telemetry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 8px 20px;
        border-radius: 8px;
        letter-spacing: 1px;
      }

      /* HOOK CARD */
      .hook-card {
        margin-top: 30px;
        padding: 34px 40px;
        background: rgba(18, 10, 36, 0.85);
        border: 1px solid rgba(168, 85, 247, 0.4);
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
        color: #c084fc;
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
        color: #c084fc;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.7);
      }

      /* HERO STAGE: SCHEMA MUTATION VS DATA CONTRACTS */
      .hero-stage {
        position: relative;
        width: 100%;
        height: 820px;
        margin-top: 25px;
        border-radius: 32px;
        background: rgba(12, 7, 24, 0.90);
        border: 1px solid rgba(168, 85, 247, 0.3);
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
        color: #c084fc;
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 20;
      }

      /* ACT 1: SCHEMA BREAKING FAILURE */
      .breaking-container {
        position: absolute;
        width: 860px;
        height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      /* ACT 2: YAML DATA CONTRACT GATE */
      .contract-gate-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
      }
      .contract-svg {
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
        background: rgba(18, 10, 36, 0.95);
        border: 2px solid rgba(168, 85, 247, 0.6);
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
        color: #d8b4fe;
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
        background: rgba(18, 10, 36, 0.85);
        border: 1px solid rgba(168, 85, 247, 0.4);
        padding: 16px 20px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
      }
      .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 800;
        color: #c084fc;
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
        background: rgba(18, 10, 36, 0.85);
        border: 1px solid rgba(168, 85, 247, 0.35);
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
        color: #c084fc;
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
        background: linear-gradient(180deg, #c084fc, #9333ea);
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
      }

      /* FOOTER / SPOTIFY CTA */
      .footer-cta {
        margin-top: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 36px;
        background: rgba(18, 10, 36, 0.75);
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
        background: #9333ea;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
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
          sIA DAILY • INGENIERÍA DE DATOS
        </div>
        <div class="badge-telemetry">
          DATA CONTRACTS // DBT & CI/CD
        </div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card" id="hookCard">
        <div class="hook-label">
          <span>🛡️</span> GOBERNANZA TÉCNICA DE DATOS
        </div>
        <div class="hook-title">
          "¿Por qué los pipelines de datos siguen <span class="alert-hl">rompiéndose a las 3:00 AM</span>?"
        </div>
      </div>

      <!-- HERO STAGE (Schema Mutation vs Data Contract Gate) -->
      <div class="hero-stage" id="heroStage">
        <div class="stage-header">
          <span id="stageTitle">MUTACIÓN SILENCIOSA vs YAML GATE</span>
          <span id="stageTelemetry">ENFORCEMENT EN TIEMPO REAL</span>
        </div>

        <!-- ACT 1: Breaking Pipeline Visual -->
        <div class="breaking-container" id="breakingContainer">
          <svg width="800" height="460" viewBox="0 0 800 460">
            <!-- Source Database Node -->
            <rect x="60" y="160" width="180" height="120" rx="16" fill="#1e1b4b" stroke="#a855f7" stroke-width="2.5"/>
            <text x="150" y="210" fill="#c084fc" font-family="JetBrains Mono" font-size="18" text-anchor="middle" font-weight="800">POSTGRES DB</text>
            <text x="150" y="240" fill="#94a3b8" font-family="JetBrains Mono" font-size="14" text-anchor="middle">user_id: string ⚠️</text>

            <!-- Pipe with error pulse -->
            <path id="pipe1" d="M 240,220 L 520,220" stroke="#ef4444" stroke-width="5" stroke-dasharray="10 6"/>

            <!-- Breaking Data Packet -->
            <g id="errorPacket" transform="translate(360, 190)">
              <rect width="60" height="60" rx="10" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/>
              <text x="30" y="38" fill="#ffffff" font-family="JetBrains Mono" font-size="24" text-anchor="middle" font-weight="900">💥</text>
            </g>

            <!-- Destination Warehouse Node -->
            <rect x="520" y="160" width="220" height="120" rx="16" fill="#450a0a" stroke="#ef4444" stroke-width="2.5"/>
            <text x="630" y="205" fill="#fca5a5" font-family="JetBrains Mono" font-size="18" text-anchor="middle" font-weight="800">BIGQUERY PROD</text>
            <text x="630" y="235" fill="#f87171" font-family="JetBrains Mono" font-size="14" text-anchor="middle">SchemaMismatchError</text>
            <text x="630" y="260" fill="#ef4444" font-family="JetBrains Mono" font-size="13" text-anchor="middle" font-weight="800">[DASHBOARD DOWN]</text>

            <!-- Error Banner -->
            <rect x="180" y="340" width="440" height="50" rx="12" fill="rgba(220, 38, 38, 0.2)" stroke="#ef4444" stroke-width="2"/>
            <text x="400" y="372" fill="#fee2e2" font-family="JetBrains Mono" font-size="17" text-anchor="middle" font-weight="800">🚨 MUTACIÓN SILENCIOSA EN PRODUCCIÓN</text>
          </svg>
        </div>

        <!-- ACT 2: Data Contract Engine Blueprint -->
        <div class="contract-gate-container" id="contractContainer">
          <svg class="contract-svg" viewBox="0 0 860 640">
            <defs>
              <linearGradient id="purpleGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.9"/>
                <stop offset="100%" stop-color="#6d28d9" stop-opacity="0.7"/>
              </linearGradient>
            </defs>

            <!-- Source Node -->
            <rect x="50" y="240" width="160" height="100" rx="14" fill="#1e1b4b" stroke="#8b5cf6" stroke-width="2"/>
            <text x="130" y="285" fill="#c084fc" font-family="JetBrains Mono" font-size="16" text-anchor="middle" font-weight="800">EVENT PRODUCER</text>
            <text x="130" y="315" fill="#94a3b8" font-family="JetBrains Mono" font-size="13" text-anchor="middle">JSON Stream</text>

            <!-- Arrow to Contract Gate -->
            <line x1="210" y1="290" x2="310" y2="290" stroke="#a855f7" stroke-width="3" stroke-dasharray="6 4"/>

            <!-- YAML CONTRACT GATE (Central Filter Engine) -->
            <rect id="yamlGate" x="310" y="160" width="240" height="260" rx="20" fill="url(#purpleGlow)" stroke="#c084fc" stroke-width="3"/>
            <text x="430" y="205" fill="#ffffff" font-family="JetBrains Mono" font-size="20" text-anchor="middle" font-weight="900">⚡ DATA CONTRACT</text>
            <text x="430" y="235" fill="#e9d5ff" font-family="JetBrains Mono" font-size="14" text-anchor="middle">specification: v2.1.yaml</text>
            
            <rect x="330" y="255" width="200" height="70" rx="10" fill="rgba(0,0,0,0.5)"/>
            <text x="345" y="282" fill="#34d399" font-family="JetBrains Mono" font-size="14" font-weight="700">✓ user_id: UUID (regex)</text>
            <text x="345" y="308" fill="#34d399" font-family="JetBrains Mono" font-size="14" font-weight="700">✓ amount: numeric(12,2)</text>

            <rect x="330" y="340" width="200" height="60" rx="10" fill="rgba(0,0,0,0.5)"/>
            <text x="430" y="365" fill="#c084fc" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">CI/CD ENFORCEMENT</text>
            <text x="430" y="388" fill="#94a3b8" font-family="JetBrains Mono" font-size="12" text-anchor="middle">Validación &lt; 5ms</text>

            <!-- Branch 1: Valid Path to Lakehouse -->
            <path d="M 550,240 Q 640,240 670,180" fill="none" stroke="#10b981" stroke-width="3.5"/>
            <rect x="670" y="130" width="160" height="90" rx="14" fill="#064e3b" stroke="#10b981" stroke-width="2.5"/>
            <text x="750" y="170" fill="#6ee7b7" font-family="JetBrains Mono" font-size="15" text-anchor="middle" font-weight="800">LAKEHOUSE</text>
            <text x="750" y="195" fill="#34d399" font-family="JetBrains Mono" font-size="13" text-anchor="middle">✓ INGESTIÓN LIMPIA</text>

            <!-- Branch 2: Quarantine Path to DLQ -->
            <path d="M 550,340 Q 640,340 670,400" fill="none" stroke="#ef4444" stroke-width="3.5" stroke-dasharray="6 4"/>
            <rect x="670" y="360" width="160" height="90" rx="14" fill="#450a0a" stroke="#ef4444" stroke-width="2.5"/>
            <text x="750" y="400" fill="#fca5a5" font-family="JetBrains Mono" font-size="15" text-anchor="middle" font-weight="800">DLQ QUARANTINE</text>
            <text x="750" y="425" fill="#ef4444" font-family="JetBrains Mono" font-size="13" text-anchor="middle">⛔ MUTACIÓN BLOQUEADA</text>
          </svg>
        </div>

        <!-- ACT 3: Omnichannel Flywheel Card -->
        <div class="flywheel-container" id="flywheelContainer">
          <div class="flywheel-card">
            <div class="card-icon">🎧</div>
            <div class="card-info">
              <span class="card-title">sIA Daily en Spotify</span>
              <span class="card-desc">Episodio #35: Data Contracts Semánticos y FHE en producción</span>
            </div>
          </div>
          <div class="flywheel-card" style="border-color: #38bdf8;">
            <div class="card-icon">📖</div>
            <div class="card-info">
              <span class="card-title">Revista Técnica Digital</span>
              <span class="card-desc">escucha-sia.github.io • Esquemas YAML, dbt tests y arquitectura</span>
            </div>
          </div>
        </div>

        <!-- Telemetry Metrics Grid -->
        <div class="metrics-grid">
          <div class="metric-badge">
            <span class="metric-value">&lt; 5 ms</span>
            <span class="metric-desc">Latencia de Validación en Stream</span>
          </div>
          <div class="metric-badge">
            <span class="metric-value">0% Fallos</span>
            <span class="metric-desc">Tableros de Negocio en Producción</span>
          </div>
        </div>
      </div>

      <!-- SUBTITLES & AUDIO CARD -->
      <div class="subtitles-card">
        <div class="speaker-tag" id="speakerTag">
          <span>🎙️</span> JORGE (INGENIERÍA DE DATOS)
        </div>
        <div class="subtitles-text" id="subtitlesText">
          "¿Por qué los equipos de datos siguen despertando a las tres de la mañana por pipelines destruidos en producción?"
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
          ESCUCHAR CAPÍTULO
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

      // 3. Pulse YAML Gate
      gsap.to("#yamlGate", {
        stroke: "#e9d5ff",
        duration: 1.2,
        repeat: -1,
        yoyo: true,
        ease: "power2.inOut"
      });

      // 4. MASTER TIMELINE FOR VIDEO (45.0s CLOSED PRODUCT)
      const tl = gsap.timeline();

      // ACT 1 (0.0s - 16.0s): El pipeline roto en producción
      tl.from(".header-hud", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
      tl.from("#hookCard", { scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.4);
      tl.from("#breakingContainer", { scale: 0.85, opacity: 0, duration: 1.0, ease: "power3.out" }, 0.6);

      // Subtitles Sync Act 1
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "¿Por qué los equipos de datos siguen despertando a las tres de la mañana por pipelines destruidos en producción?";
      }, null, 0.2);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Cualquier cambio imprevisto en origen muta el esquema silenciosamente, corrompe las tablas analíticas y derrumba los tableros del negocio.";
      }, null, 6.0);

      // TRANSITION TO ACT 2 (16.0s - 34.0s): Dalia presenta YAML Contract Gate
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> DALIA (ARQUITECTURA DE DATOS)";
        document.getElementById("stageTitle").innerHTML = "YAML CONTRACT GATE // CI/CD ENFORCEMENT";
        document.getElementById("stageTelemetry").innerHTML = "LATENCIA: < 5ms • DEAD LETTER QUEUE";
      }, null, 16.0);

      // Fade out Breaking, Fade in Contract Gate
      tl.to("#breakingContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 16.0);
      tl.to("#contractContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 16.7);

      // Subtitles Act 2
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "La solución son los Data Contracts semánticos: especificaciones YAML declarativas y validación en CI/CD que interceptan anomalías en menos de cinco milisegundos...";
      }, null, 16.5);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "<span style='color: #c084fc; font-weight: 800;'>...aislando paquetes corruptos en una Dead Letter Queue antes de contaminar el lago analítico.</span>";
      }, null, 25.0);

      // TRANSITION TO ACT 3 (34.0s - 45.0s): Veredicto & Tripartite Flywheel
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> JORGE & DALIA (VEREDICTO)";
        document.getElementById("stageTitle").innerHTML = "VEREDICTO & REDIRECCIÓN OMNICANAL";
        document.getElementById("stageTelemetry").innerHTML = "DATA CONTRACTS Y PRODUCCIÓN";
      }, null, 34.0);

      // Fade out Contract Gate, Fade in Flywheel Card
      tl.to("#contractContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 34.0);
      tl.to("#flywheelContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 34.7);

      // Subtitles Act 3
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Aprende a implementar contratos con dbt en escucha-sia.github.io, y escucha el análisis técnico en el episodio 35 de Spotify.";
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
        "-ss", "20.0",
        "-i", str(TARGET_REEL),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    size_mb = os.path.getsize(TARGET_REEL) / (1024 * 1024)
    print(f"✅ ¡Video Motion Graphics Reel #08 generado con éxito! ({size_mb:.2f} MB)")
    print(f"   -> {TARGET_REEL}")
    print(f"   -> Póster en: {poster_path}")

async def main():
    print("=" * 60)
    print("🎬 RENDERIZANDO VIDEO MOTION GRAPHICS: sIA #08 (DATA CONTRACTS SEMÁNTICOS)")
    print("=" * 60)
    await generate_reel_audio()
    write_hyperframes_html()
    render_with_hyperframes()

if __name__ == "__main__":
    asyncio.run(main())
