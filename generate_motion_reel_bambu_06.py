"""
sIA Motion Graphics Reel Generator: Reel #06 (Bambu Lab & Tolerancias PETG)
Genera un reel cinemático vertical (1080x1920) 100% código en HyperFrames:
- Curva de calibración de flujo dinámico (Pressure Advance) animada con SVG y GSAP.
- Extrusor CoreXY vectorial con engranajes en rotación y sensor Micro-LiDAR.
- Cono láser de escaneo en tiempo real sobre la cama caliente.
- Badges de telemetría de ingeniería: 500 mm/s, 7μm LiDAR, 0.02mm Tolerancia.
- Embudo cinemático hacia Spotify y el Blog técnico con código y APA.
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

SOURCE_AUDIO = AUDIO_DIR / "sIA_Daily_S04_Maker_3D_Bambu_Polimeros4D_2026-10-12.mp3"
TARGET_REEL = REELS_DIR / "sIA_Reel_06_Maker_Bambu_Lab_PETG.mp4"
DURATION = 18.5
START_OFFSET = "00:00:22.8"

def extract_teaser_audio():
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-ss", START_OFFSET,
        "-t", str(DURATION),
        "-i", str(SOURCE_AUDIO),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-af", "afade=t=out:st=17.0:d=1.5",
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
        background: #02140d;
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
    <div id="root" data-composition-id="sia_motion_reel_bambu" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
        background: #02140d;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f0fdf4;
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
          radial-gradient(circle at 50% 15%, rgba(16, 185, 129, 0.20) 0%, transparent 60%),
          radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 65%),
          linear-gradient(180deg, #02140d 0%, #032115 50%, #02140d 100%);
      }

      /* Grid de precisión técnica */
      .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(16, 185, 129, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(16, 185, 129, 0.06) 1px, transparent 1px);
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
        background: rgba(16, 185, 129, 0.18);
        border: 1px solid rgba(16, 185, 129, 0.5);
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #6ee7b7;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.3);
      }
      .badge-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 14px #10b981;
      }
      .badge-telemetry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 8px 20px;
        border-radius: 8px;
        letter-spacing: 1px;
      }

      /* HOOK CARD */
      .hook-card {
        margin-top: 30px;
        padding: 34px 40px;
        background: rgba(6, 28, 19, 0.85);
        border: 1px solid rgba(16, 185, 129, 0.4);
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
        color: #34d399;
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
        color: #10b981;
        text-shadow: 0 0 20px rgba(16, 185, 129, 0.7);
      }

      /* HERO STAGE: DIAGRAMAS ACTIVOS */
      .hero-stage {
        position: relative;
        width: 100%;
        height: 820px;
        margin-top: 25px;
        border-radius: 32px;
        background: rgba(3, 20, 14, 0.90);
        border: 1px solid rgba(16, 185, 129, 0.3);
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
        color: #10b981;
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 20;
      }

      /* ACT 1: FLOW RATE VS PRESSURE ADVANCE GRAPH */
      .flow-graph-container {
        position: absolute;
        width: 860px;
        height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      /* ACT 2: ISOMETRIC COREXY TOOLHEAD & LIDAR */
      .extruder-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
      }
      .extruder-svg {
        width: 840px;
        height: 640px;
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
        background: rgba(6, 28, 19, 0.85);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 16px 20px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
      }
      .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 800;
        color: #10b981;
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
        background: rgba(6, 28, 19, 0.85);
        border: 1px solid rgba(16, 185, 129, 0.35);
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
        color: #34d399;
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
        color: #f0fdf4;
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
        background: linear-gradient(180deg, #10b981, #047857);
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
      }

      /* FOOTER / SPOTIFY CTA */
      .footer-cta {
        margin-top: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 36px;
        background: rgba(6, 28, 19, 0.75);
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
        background: #059669;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
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
          sIA #37 • FABRICACIÓN ADITIVA
        </div>
        <div class="badge-telemetry">
          COREXY // BAMBU X1C
        </div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card" id="hookCard">
        <div class="hook-label">
          <span>⚙️</span> FÍSICA DE EXTRUSIÓN & POLÍMEROS TÉCNICOS
        </div>
        <div class="hook-title">
          "¿Por qué tus piezas de PETG <span class="alert-hl">se deforman y fallan</span> en tolerancias críticas?"
        </div>
      </div>

      <!-- HERO STAGE (Flow Calibration & Micro-LiDAR) -->
      <div class="hero-stage" id="heroStage">
        <div class="stage-header">
          <span id="stageTitle">CALIBRACIÓN DE FLUJO DINÁMICO // PRESSURE ADVANCE</span>
          <span id="stageTelemetry">BOQUILLA: 0.4mm • TEMP: 265°C</span>
        </div>

        <!-- ACT 1: Flow Rate Graph -->
        <div class="flow-graph-container" id="graphContainer">
          <svg width="800" height="480" viewBox="0 0 800 480">
            <defs>
              <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#10b981"/>
                <stop offset="100%" stop-color="#34d399"/>
              </linearGradient>
            </defs>

            <!-- Graph Grid Lines -->
            <line x1="80" y1="40" x2="80" y2="400" stroke="rgba(16, 185, 129, 0.3)" stroke-width="2"/>
            <line x1="80" y1="400" x2="760" y2="400" stroke="rgba(16, 185, 129, 0.3)" stroke-width="2"/>
            <line x1="80" y1="280" x2="760" y2="280" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1.5" stroke-dasharray="6 6"/>
            <line x1="80" y1="160" x2="760" y2="160" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1.5" stroke-dasharray="6 6"/>

            <!-- Axis Labels -->
            <text x="60" y="50" fill="#10b981" font-family="JetBrains Mono" font-size="16" text-anchor="end" font-weight="700">FLUJO (mm³/s)</text>
            <text x="760" y="435" fill="#94a3b8" font-family="JetBrains Mono" font-size="16" text-anchor="end">TIEMPO / GIRO EN ESQUINA →</text>
            <text x="65" y="285" fill="#64748b" font-family="JetBrains Mono" font-size="14" text-anchor="end">12 mm³/s</text>
            <text x="65" y="165" fill="#64748b" font-family="JetBrains Mono" font-size="14" text-anchor="end">24 mm³/s</text>

            <!-- Target Steady Flow (Ideal) -->
            <line x1="80" y1="200" x2="760" y2="200" stroke="#10b981" stroke-width="3" stroke-dasharray="8 6"/>
            <text x="750" y="185" fill="#34d399" font-family="JetBrains Mono" font-size="16" text-anchor="end" font-weight="800">FLUJO OBJETIVO LINEAL</text>

            <!-- Error Curve (Uncalibrated PETG: Corner Bulge) -->
            <path id="uncalibratedCurve" d="M 80,200 Q 220,200 280,70 T 420,330 T 560,200 L 760,200" fill="none" stroke="#ef4444" stroke-width="4.5" stroke-linecap="round"/>
            <circle cx="340" cy="95" r="10" fill="#ef4444"/>
            <text x="360" y="90" fill="#fca5a5" font-family="JetBrains Mono" font-size="18" font-weight="800">ESQUINA HINCHADA (+0.35mm)</text>

            <!-- Compensated Curve (Pressure Advance Activo) -->
            <path id="calibratedCurve" d="M 80,200 L 260,200 Q 290,190 320,200 Q 360,208 400,200 L 760,200" fill="none" stroke="url(#emeraldGrad)" stroke-width="5" stroke-linecap="round"/>
            <text x="500" y="240" fill="#6ee7b7" font-family="JetBrains Mono" font-size="18" font-weight="800">✓ PRESIÓN COMPENSADA (0.02mm)</text>
          </svg>
        </div>

        <!-- ACT 2: Isometric Toolhead & Micro-LiDAR -->
        <div class="extruder-container" id="extruderContainer">
          <svg class="extruder-svg" viewBox="0 0 840 640">
            <defs>
              <linearGradient id="lidarBeam" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#10b981" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.1"/>
              </linearGradient>
            </defs>

            <!-- Bed Grid Plane -->
            <polygon points="120,520 420,380 720,520 420,620" fill="rgba(6, 28, 19, 0.7)" stroke="rgba(16, 185, 129, 0.4)" stroke-width="2"/>
            <line x1="220" y1="475" x2="620" y2="475" stroke="rgba(16, 185, 129, 0.2)" stroke-width="1.5"/>
            <line x1="320" y1="430" x2="520" y2="430" stroke="rgba(16, 185, 129, 0.2)" stroke-width="1.5"/>

            <!-- Toolhead Core Body -->
            <polygon points="320,160 520,160 520,340 320,340" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
            <polygon points="320,160 380,120 580,120 520,160" fill="#1e293b" stroke="#10b981" stroke-width="3"/>
            <polygon points="520,160 580,120 580,300 520,340" fill="#0f172a" stroke="#10b981" stroke-width="3"/>

            <!-- Cooling Fan Circle -->
            <circle cx="420" cy="240" r="50" fill="#02140d" stroke="#34d399" stroke-width="3"/>
            <circle cx="420" cy="240" r="16" fill="#10b981"/>

            <!-- Dual Drive Extrusion Gears -->
            <circle id="gearLeft" cx="370" cy="180" r="22" fill="none" stroke="#6ee7b7" stroke-width="4" stroke-dasharray="8 6"/>
            <circle id="gearRight" cx="410" cy="180" r="22" fill="none" stroke="#6ee7b7" stroke-width="4" stroke-dasharray="8 6"/>

            <!-- Dual Micro-LiDAR Sensor Pods -->
            <rect x="340" y="340" width="36" height="24" fill="#10b981" rx="4"/>
            <rect x="464" y="340" width="36" height="24" fill="#10b981" rx="4"/>
            <circle cx="358" cy="352" r="6" fill="#ffffff"/>
            <circle cx="482" cy="352" r="6" fill="#ffffff"/>

            <!-- Nozzle Cone -->
            <polygon points="405,340 435,340 423,375 417,375" fill="#f59e0b" stroke="#d97706" stroke-width="2"/>

            <!-- Micro-LiDAR Laser Beam Scanning Bed -->
            <polygon id="laserCone" points="358,360 482,360 560,510 280,510" fill="url(#lidarBeam)" stroke="#34d399" stroke-width="1.5" stroke-dasharray="4 4"/>
            
            <!-- Scanning Line on Bed -->
            <line id="scanLine" x1="280" y1="510" x2="560" y2="510" stroke="#34d399" stroke-width="4"/>
            <text x="420" y="550" fill="#6ee7b7" font-family="JetBrains Mono" font-size="18" font-weight="800" text-anchor="middle">ESCANEO DE CAPA: RESOLUCIÓN 7μm</text>
          </svg>
        </div>

        <!-- Telemetry Metrics Grid -->
        <div class="metrics-grid">
          <div class="metric-badge">
            <span class="metric-value" id="valSpeed">500 mm/s</span>
            <span class="metric-desc">Velocidad Cinemática CoreXY</span>
          </div>
          <div class="metric-badge">
            <span class="metric-value" id="valTol">0.02 mm</span>
            <span class="metric-desc">Tolerancia Dinámica con LiDAR</span>
          </div>
        </div>
      </div>

      <!-- SUBTITLES & AUDIO CARD -->
      <div class="subtitles-card">
        <div class="speaker-tag" id="speakerTag">
          <span>🎙️</span> JORGE (FABRICACIÓN ADITIVA)
        </div>
        <div class="subtitles-text" id="subtitlesText">
          "El filamento PETG es el caballo de batalla, pero su tendencia al stringing sigue frustrando a creadores..."
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
          ESCUCHAR DEBATE
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

      // 3. Rotating Extruder Gears
      gsap.to("#gearLeft", { rotation: 360, transformOrigin: "center center", duration: 2.0, repeat: -1, ease: "none" });
      gsap.to("#gearRight", { rotation: -360, transformOrigin: "center center", duration: 2.0, repeat: -1, ease: "none" });

      // 4. Scanning LiDAR Laser Animation
      gsap.to("#laserCone", {
        opacity: 0.35,
        duration: 0.6,
        repeat: -1,
        yoyo: true,
        ease: "power2.inOut"
      });

      // 5. MASTER TIMELINE FOR VIDEO
      const tl = gsap.timeline();

      // ACT 1 (0.0s - 9.5s): Jorge explica el error de flujo y stringing en PETG
      tl.from(".header-hud", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
      tl.from("#hookCard", { scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.4);
      tl.from("#graphContainer", { scale: 0.85, opacity: 0, duration: 1.0, ease: "power3.out" }, 0.6);

      // Draw uncalibrated curve
      tl.from("#uncalibratedCurve", { strokeDashoffset: 1200, duration: 2.5, ease: "power2.out" }, 1.0);
      tl.from("#calibratedCurve", { strokeDashoffset: 1000, duration: 2.5, ease: "power2.out" }, 3.5);

      // Subtitles Sync Act 1
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "El filamento PETG es el caballo de batalla para piezas mecánicas por su resistencia al impacto...";
      }, null, 0.2);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "...sin embargo, el stringing y la adhesión excesiva siguen arruinando tolerancias críticas.";
      }, null, 5.0);

      // TRANSITION TO ACT 2 (9.5s): Dalia presenta la solución Micro-LiDAR
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> DALIA (INGENIERÍA)";
        document.getElementById("stageTitle").innerHTML = "MICRO-LIDAR & CALIBRACIÓN DINÁMICA DE FLUJO";
        document.getElementById("stageTelemetry").innerHTML = "PRESSURE ADVANCE: ACTIVO • SENSORES: DUAL 7μm";
      }, null, 9.5);

      // Fade out Graph, Fade in Extruder
      tl.to("#graphContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 9.5);
      tl.to("#extruderContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 10.2);

      // Subtitles Act 2
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "En Bambu Studio y Orca Slicer calibramos la compensación de flujo dinámico con el sensor Micro-LiDAR...";
      }, null, 10.0);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "<span style='color: #10b981; font-weight: 800;'>Pressure Advance ecualiza la presión en boquilla: orificios y rodamientos encajan a la primera.</span>";
      }, null, 14.0);

      // Telemetry counts
      tl.from("#valSpeed", { textContent: "100 mm/s", duration: 1.5, ease: "power1.out" }, 10.5);
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
        "-ss", "13.5",
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
    print("🎬 RENDERIZANDO VIDEO MOTION GRAPHICS: sIA #37 (BAMBU LAB)")
    print("=" * 50)
    extract_teaser_audio()
    write_hyperframes_html()
    render_with_hyperframes()

if __name__ == "__main__":
    main()
