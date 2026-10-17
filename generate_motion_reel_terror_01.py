"""
sIA Motion Graphics Reel Generator: Terror #01 (Escaleras en el Bosque)
Genera un reel cinemático vertical (1080x1920) 100% código en HyperFrames:
- Radar táctico SAR con barrido continuo 360° en SVG.
- Detección de anomalía con pulso rojo y coordenadas GPS.
- Esquema isométrico vectorial de la escalera que se dibuja peldaño por peldaño.
- Callouts tácticos: 0 Cimientos, Madera Pulida, Cero Musgo, Silencio Acústico.
- Banner de protocolo de emergencia y subtítulos cinemáticos.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
NODE_PATH = r"C:\Carlos\nodejs"

SOURCE_AUDIO = AUDIO_DIR / "sIA_Terror_01_Las_Escaleras_del_Bosque_2026-10-15.mp3"
TARGET_REEL = REELS_DIR / "sIA_Terror_01_Las_Escaleras_Reel.mp4"
DURATION = 22.5

def extract_teaser_audio():
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:00.0",
        "-t", str(DURATION),
        "-i", str(SOURCE_AUDIO),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-af", "afade=t=out:st=21.0:d=1.5",
        str(clip_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✂️ Audio teaser extraído correctamente.")

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
        background: #020617;
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
    <div id="root" data-composition-id="sia_motion_reel_terror" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800;900&family=JetBrains+Mono:wght@600;700;800&family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
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
        background: #020617;
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
          radial-gradient(circle at 50% 15%, rgba(220, 38, 38, 0.18) 0%, transparent 60%),
          radial-gradient(circle at 50% 70%, rgba(15, 23, 42, 0.8) 0%, transparent 70%),
          linear-gradient(180deg, #020617 0%, #090d16 50%, #020617 100%);
      }

      /* Grid de telemetría militar */
      .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(239, 68, 68, 0.05) 1px, transparent 1px),
          linear-gradient(90deg, rgba(239, 68, 68, 0.05) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
      }

      /* Scanlines sutiles */
      .scanline {
        position: absolute;
        inset: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
        background-size: 100% 4px;
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
        background: rgba(220, 38, 38, 0.18);
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
        animation: pulse 1s infinite alternate;
      }
      @keyframes pulse {
        from { opacity: 0.4; }
        to { opacity: 1; }
      }
      .badge-telemetry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 8px 20px;
        border-radius: 8px;
        letter-spacing: 1px;
      }

      /* HOOK CARD */
      .hook-card {
        margin-top: 30px;
        padding: 34px 40px;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(239, 68, 68, 0.35);
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
        color: #ef4444;
        text-shadow: 0 0 20px rgba(239, 68, 68, 0.7);
      }

      /* HERO STAGE: RADAR & STAIRCASE DIAGRAM */
      .hero-stage {
        position: relative;
        width: 100%;
        height: 820px;
        margin-top: 25px;
        border-radius: 32px;
        background: rgba(10, 15, 29, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.25);
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
        color: #ef4444;
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 20;
      }

      /* RADAR WRAPPER (Act 1) */
      .radar-container {
        position: absolute;
        width: 600px;
        height: 600px;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .radar-sweep {
        position: absolute;
        width: 560px;
        height: 560px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, rgba(239, 68, 68, 0.45) 0deg, transparent 65deg, transparent 360deg);
        transform-origin: center center;
      }

      /* VECTOR STAIRCASE (Act 2) */
      .staircase-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
      }
      .iso-svg {
        width: 780px;
        height: 640px;
      }

      /* TACTICAL CALLOUT PINS */
      .callout-badge {
        position: absolute;
        padding: 12px 20px;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(239, 68, 68, 0.6);
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #fca5a5;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8), 0 0 15px rgba(239, 68, 68, 0.3);
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .pin-1 { top: 120px; right: 80px; }
      .pin-2 { bottom: 180px; left: 70px; }
      .pin-3 { top: 280px; left: 60px; }

      /* WARNING CHEVRON BAR */
      .warning-bar {
        position: absolute;
        bottom: 24px;
        left: 32px;
        right: 32px;
        padding: 16px 24px;
        background: rgba(220, 38, 38, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.6);
        border-radius: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #fee2e2;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 14px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.2);
      }
      .warning-icon {
        color: #ef4444;
        font-size: 26px;
      }

      /* SUBTITLES & AUDIO CARD */
      .subtitles-card {
        margin-top: 25px;
        padding: 30px 40px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.3);
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
        background: linear-gradient(180deg, #ef4444, #991b1b);
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
      <div class="scanline"></div>

      <!-- TOP BAR -->
      <div class="header-hud">
        <div class="badge-series">
          <div class="badge-dot"></div>
          sIA TERROR • EXPEDIENTE #01
        </div>
        <div class="badge-telemetry">
          SAR LOGS // CLASIFICADO
        </div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card" id="hookCard">
        <div class="hook-label">
          <span>⚠️</span> TESTIMONIO DE BÚSQUEDA Y RESCATE (r/nosleep)
        </div>
        <div class="hook-title">
          "Si en mitad del bosque ves una <span class="alert-hl">escalera solitaria</span>... jamás subas."
        </div>
      </div>

      <!-- HERO STAGE (Radar & Staircase Diagram) -->
      <div class="hero-stage" id="heroStage">
        <div class="stage-header">
          <span id="stageTitle">RADAR DE BÚSQUEDA // SECTOR NORTE D-7</span>
          <span id="stageTelemetry">COORD: 46°51'N 121°45'W</span>
        </div>

        <!-- ACT 1: Tactical Radar Grid -->
        <div class="radar-container" id="radarContainer">
          <svg width="560" height="560" viewBox="0 0 560 560" style="position: absolute;">
            <!-- Radar rings -->
            <circle cx="280" cy="280" r="260" fill="none" stroke="rgba(239, 68, 68, 0.25)" stroke-width="2" stroke-dasharray="8 6"/>
            <circle cx="280" cy="280" r="190" fill="none" stroke="rgba(239, 68, 68, 0.3)" stroke-width="2"/>
            <circle cx="280" cy="280" r="120" fill="none" stroke="rgba(239, 68, 68, 0.4)" stroke-width="2"/>
            <circle cx="280" cy="280" r="50" fill="none" stroke="rgba(239, 68, 68, 0.5)" stroke-width="2"/>
            
            <!-- Crosshairs -->
            <line x1="280" y1="10" x2="280" y2="550" stroke="rgba(239, 68, 68, 0.2)" stroke-width="1.5"/>
            <line x1="10" y1="280" x2="550" y2="280" stroke="rgba(239, 68, 68, 0.2)" stroke-width="1.5"/>
            
            <!-- Angle ticks -->
            <text x="280" y="32" fill="#ef4444" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">000° N</text>
            <text x="535" y="285" fill="#ef4444" font-family="JetBrains Mono" font-size="14" text-anchor="end" font-weight="700">090° E</text>
            <text x="280" y="542" fill="#ef4444" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">180° S</text>
            <text x="25" y="285" fill="#ef4444" font-family="JetBrains Mono" font-size="14" text-anchor="start" font-weight="700">270° W</text>

            <!-- Anomaly Beacon Ping (At 45 degrees, r=160) -->
            <g id="radarBlip" transform="translate(393, 167)">
              <circle r="22" fill="none" stroke="#ef4444" stroke-width="2">
                <animate attributeName="r" values="6;32" dur="1.2s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="1;0" dur="1.2s" repeatCount="indefinite"/>
              </circle>
              <circle r="8" fill="#ef4444"/>
              <text x="20" y="6" fill="#fca5a5" font-family="JetBrains Mono" font-size="16" font-weight="800">ANOMALÍA DETECTADA</text>
            </g>
          </svg>
          <!-- Rotating Radar Sweep Line -->
          <div class="radar-sweep" id="radarSweep"></div>
        </div>

        <!-- ACT 2: Vector Staircase Blueprint -->
        <div class="staircase-container" id="staircaseContainer">
          <svg class="iso-svg" viewBox="0 0 780 640">
            <defs>
              <linearGradient id="stepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#450a0a" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.6"/>
              </linearGradient>
              <filter id="redGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>

            <!-- Forest Terrain Grid Ground Plane -->
            <polygon points="120,480 390,340 660,480 390,620" fill="rgba(15, 23, 42, 0.6)" stroke="rgba(239, 68, 68, 0.3)" stroke-width="1.5" stroke-dasharray="6 4"/>
            <text x="390" y="585" fill="#64748b" font-family="JetBrains Mono" font-size="18" text-anchor="middle">SUELO VIRGEN // BOSQUE DENSO (SIN CIMIENTOS)</text>

            <!-- ISOMETRIC STAIRS (5 Steps) -->
            <!-- Step 1 -->
            <g id="step1" class="stair-step">
              <polygon points="260,450 340,410 440,410 360,450" fill="url(#stepGrad)" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="260,450 360,450 360,480 260,480" fill="#2d0a0a" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="360,450 440,410 440,440 360,480" fill="#1f0707" stroke="#ef4444" stroke-width="2.5"/>
            </g>

            <!-- Step 2 -->
            <g id="step2" class="stair-step">
              <polygon points="290,400 370,360 470,360 390,400" fill="url(#stepGrad)" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="290,400 390,400 390,430 290,430" fill="#2d0a0a" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="390,400 470,360 470,390 390,430" fill="#1f0707" stroke="#ef4444" stroke-width="2.5"/>
            </g>

            <!-- Step 3 -->
            <g id="step3" class="stair-step">
              <polygon points="320,350 400,310 500,310 420,350" fill="url(#stepGrad)" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="320,350 420,350 420,380 320,380" fill="#2d0a0a" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="420,350 500,310 500,340 420,380" fill="#1f0707" stroke="#ef4444" stroke-width="2.5"/>
            </g>

            <!-- Step 4 -->
            <g id="step4" class="stair-step">
              <polygon points="350,300 430,260 530,260 450,300" fill="url(#stepGrad)" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="350,300 450,300 450,330 350,330" fill="#2d0a0a" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="450,300 530,260 530,290 450,330" fill="#1f0707" stroke="#ef4444" stroke-width="2.5"/>
            </g>

            <!-- Step 5 (Top into the void) -->
            <g id="step5" class="stair-step">
              <polygon points="380,250 460,210 560,210 480,250" fill="url(#stepGrad)" stroke="#ef4444" stroke-width="2.5" filter="url(#redGlow)"/>
              <polygon points="380,250 480,250 480,280 380,280" fill="#2d0a0a" stroke="#ef4444" stroke-width="2.5"/>
              <polygon points="480,250 560,210 560,240 480,280" fill="#1f0707" stroke="#ef4444" stroke-width="2.5"/>
            </g>

            <!-- Handrail line ascending into nothingness -->
            <path id="handrail" d="M 260,420 L 380,220" stroke="#fca5a5" stroke-width="4" stroke-dasharray="6 4" fill="none"/>
            <circle cx="380" cy="220" r="10" fill="#ef4444" filter="url(#redGlow)"/>

            <!-- Upward arrow into void -->
            <path d="M 510,190 L 510,120" stroke="#ef4444" stroke-width="3" stroke-dasharray="5 5" fill="none"/>
            <polygon points="510,105 500,125 520,125" fill="#ef4444"/>
            <text x="510" y="85" fill="#fca5a5" font-family="JetBrains Mono" font-size="20" font-weight="800" text-anchor="middle">HACIA EL VACÍO</text>
          </svg>

          <!-- TACTICAL PINS -->
          <div class="callout-badge pin-1" id="pin1">
            <span>⛔</span> 0 RUINAS / 0 CIMIENTOS
          </div>
          <div class="callout-badge pin-2" id="pin2">
            <span>✨</span> MADERA PULIDA (CERO MUSGO)
          </div>
          <div class="callout-badge pin-3" id="pin3">
            <span>🔇</span> SILENCIO ACÚSTICO TOTAL
          </div>
        </div>

        <!-- WARNING PROTOCOL BAR -->
        <div class="warning-bar" id="warningBar">
          <span class="warning-icon">⚠️</span>
          <span>PROTOCOLO SAR 7B: NO TE ACERQUES • NO MIRES DIRECTO • NO SUBAS</span>
        </div>
      </div>

      <!-- SUBTITLES & AUDIO CARD -->
      <div class="subtitles-card">
        <div class="speaker-tag" id="speakerTag">
          <span>🎙️</span> OFICIAL SAR (JORGE)
        </div>
        <div class="subtitles-text" id="subtitlesText">
          "Hay una orden estricta que todo rescatista aprende en su primera semana..."
        </div>
        <div class="waveform-row" id="waveform">
          <!-- 24 bars -->
        </div>
      </div>

      <!-- FOOTER / SPOTIFY CTA -->
      <div class="footer-cta">
        <div class="spotify-brand">
          <svg class="spotify-logo" viewBox="0 0 24 24">
            <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.503 17.308c-.218.358-.684.472-1.042.254-2.855-1.745-6.45-2.14-10.684-1.173-.408.093-.816-.162-.909-.57-.093-.408.162-.816.57-.909 4.637-1.06 8.604-.616 11.811 1.356.358.218.472.684.254 1.042zm1.47-3.268c-.275.448-.863.593-1.311.318-3.268-2.01-8.25-2.593-12.116-1.419-.505.153-1.043-.134-1.196-.639-.153-.505.134-1.043.639-1.196 4.417-1.341 9.907-.696 13.666 1.625.448.275.593.863.318 1.311zm.126-3.41c-3.918-2.327-10.37-2.542-14.103-1.408-.601.183-1.24-.162-1.423-.763-.183-.601.162-1.24.763-1.423 4.288-1.302 11.411-1.053 15.918 1.623.541.321.718 1.026.397 1.567-.321.541-1.026.718-1.567.397z"/>
          </svg>
          <div>
            <div class="brand-title">sIA Terror en Spotify</div>
            <div class="brand-sub">escucha-sia.github.io</div>
          </div>
        </div>
        <div class="action-pill">
          ESCUCHAR HISTORIA
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

      // 3. Continuous Radar Sweep
      gsap.to("#radarSweep", {
        rotation: 360,
        duration: 3.5,
        repeat: -1,
        ease: "none"
      });

      // 4. Warning Bar Flashing
      gsap.to("#warningBar", {
        backgroundColor: "rgba(220, 38, 38, 0.35)",
        borderColor: "rgba(239, 68, 68, 0.9)",
        duration: 0.6,
        repeat: -1,
        yoyo: true,
        ease: "power2.inOut"
      });

      // 5. MASTER TIMELINE FOR VIDEO
      const tl = gsap.timeline();

      // ACT 1 (0.0s - 10.5s): El Radar y la advertencia inicial
      tl.from(".header-hud", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
      tl.from("#hookCard", { scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.4);
      tl.from("#radarContainer", { scale: 0.8, opacity: 0, duration: 1.0, ease: "power3.out" }, 0.6);

      // Subtitles Sync
      // 0s: Orden estricta
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Hay una orden estricta que todo rescatista novato aprende en su primera semana...";
      }, null, 0.2);

      // 5.5s: Nadie la menciona a turistas
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "No está en los manuales oficiales. Nadie la menciona frente a los turistas...";
      }, null, 5.5);

      // TRANSITION TO ACT 2 (10.5s): Aparece la escalera en el claro
      tl.call(() => {
        document.getElementById("stageTitle").innerHTML = "ESTRUCTURA ANÓMALA // RECONSTRUCCIÓN ISOMÉTRICA";
        document.getElementById("stageTelemetry").innerHTML = "DESNIVEL: 5 PELDAÑOS • SIN SOPORTE";
      }, null, 10.5);

      // Fade out Radar, Fade in Staircase
      tl.to("#radarContainer", { opacity: 0, scale: 1.1, duration: 0.8, ease: "power2.in" }, 10.5);
      tl.to("#staircaseContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 11.2);

      // Subtitles: Si en mitad de la maleza densa...
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Pero si en mitad de la maleza densa encuentras un tramo de escaleras solitario...";
      }, null, 10.8);

      // Draw Steps 1 by 1
      tl.from("#step1", { y: 30, opacity: 0, duration: 0.4, ease: "back.out(1.5)" }, 11.5);
      tl.from("#step2", { y: 30, opacity: 0, duration: 0.4, ease: "back.out(1.5)" }, 12.0);
      tl.from("#step3", { y: 30, opacity: 0, duration: 0.4, ease: "back.out(1.5)" }, 12.5);
      tl.from("#step4", { y: 30, opacity: 0, duration: 0.4, ease: "back.out(1.5)" }, 13.0);
      tl.from("#step5", { y: 30, opacity: 0, duration: 0.5, ease: "back.out(1.5)" }, 13.5);
      tl.from("#handrail", { strokeDashoffset: 300, duration: 0.8, ease: "power2.out" }, 14.0);

      // Callout pins pop in
      tl.from("#pin1", { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)" }, 14.4);
      tl.from("#pin2", { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)" }, 15.2);
      tl.from("#pin3", { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(2)" }, 16.0);

      // Subtitles: JAMÁS TE ACERQUES
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "<span style='color: #ef4444; font-weight: 900;'>...JAMÁS TE ACERQUES. Y bajo ninguna circunstancia subas por ellas.</span>";
      }, null, 16.8);

      // Pulsing dramatic effect on climax (16.8s -> 22.5s)
      tl.to("#staircaseContainer", { scale: 1.04, duration: 5.0, ease: "power1.out" }, 17.0);
    </script>
  </body>
</html>
"""
    with open(ENGINE_DIR / "compositions" / "scene.html", "w", encoding="utf-8") as f:
        f.write(scene_html)
    print("📝 Archivos index.html y compositions/scene.html generados.")

def render_with_hyperframes():
    print("⚡ Ejecutando HyperFrames GPU render...")
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
        "-ss", "16.0",
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

def main():
    print("=" * 50)
    print("🎬 RENDERIZANDO VIDEO MOTION GRAPHICS: sIA TERROR #01")
    print("=" * 50)
    extract_teaser_audio()
    write_hyperframes_html()
    render_with_hyperframes()

if __name__ == "__main__":
    main()
