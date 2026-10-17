"""
sIA Motion Graphics Reel Generator: Reel #10 (Jev: Sistema 1 vs LLMs)
Genera un reel cinemático vertical (1080x1920) 100% código en HyperFrames:
- Comparativa de latencia: LLM Estocástico (2,400ms) vs Jev Sistema 1 (3.8ms).
- Matriz vectorial de decisiones con tipado estricto (choice, score, boolean).
- HUD de acción DOOM en tiempo real sin alucinación de texto.
- Badges de telemetría: 3.8ms Latencia, 630x Más Rápido, Tipado Estricto Nativo.
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

SOURCE_AUDIO = AUDIO_DIR / "sIA_DeepDive_Jev_TypeSafe_Sistema1.mp3"
TARGET_REEL = REELS_DIR / "sIA_Reel_10_Jev_TypeSafe_Sistema1.mp4"
DURATION = 21.0
START_OFFSET = "00:00:46.0"

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
        "-af", "afade=t=out:st=19.5:d=1.5",
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
    <div id="root" data-composition-id="sia_motion_reel_jev" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
          radial-gradient(circle at 50% 15%, rgba(6, 182, 212, 0.22) 0%, transparent 60%),
          radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 65%),
          linear-gradient(180deg, #030712 0%, #08162b 50%, #030712 100%);
      }

      /* Grid de precisión técnica */
      .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(6, 182, 212, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(6, 182, 212, 0.06) 1px, transparent 1px);
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
        background: rgba(6, 182, 212, 0.18);
        border: 1px solid rgba(6, 182, 212, 0.5);
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #67e8f9;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.3);
      }
      .badge-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #06b6d4;
        box-shadow: 0 0 14px #06b6d4;
      }
      .badge-telemetry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(6, 182, 212, 0.3);
        padding: 8px 20px;
        border-radius: 8px;
        letter-spacing: 1px;
      }

      /* HOOK CARD */
      .hook-card {
        margin-top: 30px;
        padding: 34px 40px;
        background: rgba(10, 20, 38, 0.85);
        border: 1px solid rgba(6, 182, 212, 0.4);
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
        color: #38bdf8;
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
        color: #38bdf8;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.7);
      }

      /* HERO STAGE: LATENCIA & SISTEMA 1 JEV */
      .hero-stage {
        position: relative;
        width: 100%;
        height: 820px;
        margin-top: 25px;
        border-radius: 32px;
        background: rgba(8, 16, 32, 0.90);
        border: 1px solid rgba(6, 182, 212, 0.3);
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
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: 1.5px;
        z-index: 20;
      }

      /* ACT 1: LATENCY BENCHMARK VISUAL */
      .benchmark-container {
        position: absolute;
        width: 860px;
        height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      /* ACT 2: SISTEMA 1 VECTOR DECISION ENGINE */
      .engine-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
      }
      .engine-svg {
        width: 860px;
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
        background: rgba(10, 20, 38, 0.85);
        border: 1px solid rgba(6, 182, 212, 0.4);
        padding: 16px 20px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
      }
      .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 800;
        color: #38bdf8;
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
        background: rgba(10, 20, 38, 0.85);
        border: 1px solid rgba(6, 182, 212, 0.35);
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
        color: #38bdf8;
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
        background: linear-gradient(180deg, #06b6d4, #0284c7);
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
      }

      /* FOOTER / SPOTIFY CTA */
      .footer-cta {
        margin-top: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 36px;
        background: rgba(10, 20, 38, 0.75);
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
        background: #0891b2;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
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
          sIA DEEP DIVE • SISTEMA 1
        </div>
        <div class="badge-telemetry">
          TYPESAFE JEV // DETERMINISMO
        </div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card" id="hookCard">
        <div class="hook-label">
          <span>🎯</span> ARQUITECTURA DE DECISIONES NEURALES
        </div>
        <div class="hook-title">
          "¿Por qué usar un LLM para tomar decisiones es el <span class="alert-hl">peor error de ingeniería</span>?"
        </div>
      </div>

      <!-- HERO STAGE (Latency Benchmark vs Jev System 1) -->
      <div class="hero-stage" id="heroStage">
        <div class="stage-header">
          <span id="stageTitle">LATENCIA & DETERMINISMO EN TIEMPO REAL</span>
          <span id="stageTelemetry">BENCHMARK: LLM vs SISTEMA 1</span>
        </div>

        <!-- ACT 1: Latency & Failure Bar -->
        <div class="benchmark-container" id="benchmarkContainer">
          <svg width="800" height="460" viewBox="0 0 800 460">
            <!-- LLM Row -->
            <text x="50" y="80" fill="#f87171" font-family="JetBrains Mono" font-size="20" font-weight="800">LLM GENERATIVO (TOKENS)</text>
            <rect x="50" y="100" width="700" height="70" rx="14" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" stroke-width="2"/>
            <rect id="barLlm" x="50" y="100" width="660" height="70" rx="14" fill="#dc2626"/>
            <text x="80" y="145" fill="#ffffff" font-family="JetBrains Mono" font-size="24" font-weight="900">2,400 ms  •  Alucinación Estocástica</text>

            <!-- Jev Sistema 1 Row -->
            <text x="50" y="240" fill="#38bdf8" font-family="JetBrains Mono" font-size="20" font-weight="800">JEV SISTEMA 1 (TIPADO DISCRIMINATIVO)</text>
            <rect x="50" y="260" width="700" height="70" rx="14" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" stroke-width="2"/>
            <rect id="barJev" x="50" y="260" width="80" height="70" rx="14" fill="#06b6d4"/>
            <text x="160" y="305" fill="#e0f2fe" font-family="JetBrains Mono" font-size="24" font-weight="900">3.8 ms  •  630x Más Rápido (Tipado Estricto)</text>

            <!-- Difference callout -->
            <rect x="180" y="375" width="440" height="50" rx="12" fill="rgba(6, 182, 212, 0.2)" stroke="#38bdf8" stroke-width="2"/>
            <text x="400" y="407" fill="#67e8f9" font-family="JetBrains Mono" font-size="18" text-anchor="middle" font-weight="800">⚡ 630x MENOR LATENCIA • DETERMINISTA</text>
          </svg>
        </div>

        <!-- ACT 2: Jev Neural Decision Matrix & DOOM HUD -->
        <div class="engine-container" id="engineContainer">
          <svg class="engine-svg" viewBox="0 0 860 640">
            <!-- DOOM Tactical Wireframe Viewport -->
            <rect x="60" y="60" width="440" height="340" rx="16" fill="#020a16" stroke="#06b6d4" stroke-width="2.5"/>
            <line x1="280" y1="70" x2="280" y2="390" stroke="rgba(6, 182, 212, 0.2)" stroke-width="1.5"/>
            <line x1="70" y1="230" x2="490" y2="230" stroke="rgba(6, 182, 212, 0.2)" stroke-width="1.5"/>
            
            <!-- Crosshairs -->
            <circle cx="280" cy="230" r="30" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6 4"/>
            <circle cx="280" cy="230" r="4" fill="#38bdf8"/>
            <text x="80" y="95" fill="#38bdf8" font-family="JetBrains Mono" font-size="14" font-weight="700">DOOM ENGINE // 60 FPS</text>
            <text x="80" y="120" fill="#94a3b8" font-family="JetBrains Mono" font-size="13">ENEMIGO A 12m (ÁNGULO: 34°)</text>

            <!-- Typesafe Output Structure Node -->
            <rect x="530" y="60" width="280" height="340" rx="18" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" stroke-width="2.5"/>
            <text x="670" y="105" fill="#38bdf8" font-family="JetBrains Mono" font-size="18" text-anchor="middle" font-weight="800">TYPESAFE OUTPUT</text>

            <rect x="550" y="130" width="240" height="60" rx="10" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" stroke-width="1.5"/>
            <text x="565" y="155" fill="#94a3b8" font-family="JetBrains Mono" font-size="13">choice(action):</text>
            <text x="565" y="177" fill="#67e8f9" font-family="JetBrains Mono" font-size="16" font-weight="800">"SHOOT_SHOTGUN"</text>

            <rect x="550" y="210" width="240" height="60" rx="10" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" stroke-width="1.5"/>
            <text x="565" y="235" fill="#94a3b8" font-family="JetBrains Mono" font-size="13">score(confidence):</text>
            <text x="565" y="257" fill="#67e8f9" font-family="JetBrains Mono" font-size="16" font-weight="800">0.9984 (MATEMÁTICO)</text>

            <rect x="550" y="290" width="240" height="60" rx="10" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" stroke-width="1.5"/>
            <text x="565" y="315" fill="#94a3b8" font-family="JetBrains Mono" font-size="13">boolean(evade):</text>
            <text x="565" y="337" fill="#67e8f9" font-family="JetBrains Mono" font-size="16" font-weight="800">TRUE (STRAFE_LEFT)</text>
          </svg>
        </div>

        <!-- Telemetry Metrics Grid -->
        <div class="metrics-grid">
          <div class="metric-badge">
            <span class="metric-value">3.8 ms</span>
            <span class="metric-desc">Latencia de Inferencia en GPU</span>
          </div>
          <div class="metric-badge">
            <span class="metric-value">0% Texto</span>
            <span class="metric-desc">Tipado Estricto Discriminativo</span>
          </div>
        </div>
      </div>

      <!-- SUBTITLES & AUDIO CARD -->
      <div class="subtitles-card">
        <div class="speaker-tag" id="speakerTag">
          <span>🎙️</span> JORGE (INFRAESTRUCTURA)
        </div>
        <div class="subtitles-text" id="subtitlesText">
          "Nuestra tesis central es contundente: usar LLMs generativos para decisiones fue un error arquitectónico..."
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
          ESCUCHAR DEEP DIVE
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

      // 3. MASTER TIMELINE FOR VIDEO
      const tl = gsap.timeline();

      // ACT 1 (0.0s - 10.5s): El error de usar LLMs para decisiones
      tl.from(".header-hud", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
      tl.from("#hookCard", { scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.4);
      tl.from("#benchmarkContainer", { scale: 0.85, opacity: 0, duration: 1.0, ease: "power3.out" }, 0.6);

      // Latency Bars
      tl.from("#barLlm", { width: 0, duration: 2.0, ease: "power2.out" }, 1.0);
      tl.from("#barJev", { width: 0, duration: 0.3, ease: "power4.out" }, 3.5);

      // Subtitles Sync Act 1
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Nuestra tesis central es contundente: usar LLMs generativos para decisiones fue un error arquitectónico...";
      }, null, 0.2);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "...cuando les pedimos velocidad en código son lentos, caros y peligrosamente estocásticos.";
      }, null, 5.5);

      // TRANSITION TO ACT 2 (10.5s): Dalia presenta Sistema 1 discriminativo
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> DALIA (ARQUITECTURA DE IA)";
        document.getElementById("stageTitle").innerHTML = "SISTEMA 1 // MOTOR DISCRIMINATIVO DISCRETO";
        document.getElementById("stageTelemetry").innerHTML = "TIPADO NATIVO • LATENCIA: 3.8ms";
      }, null, 10.5);

      // Fade out Benchmark, Fade in Engine
      tl.to("#benchmarkContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 10.5);
      tl.to("#engineContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 11.2);

      // Subtitles Act 2
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Jev inaugura la era del Sistema 1: redes discriminativas que no conversan ni generan texto...";
      }, null, 11.0);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "<span style='color: #38bdf8; font-weight: 800;'>...evalúan estados en milisegundos y devuelven tipos de datos matemáticamente estructurados.</span>";
      }, null, 15.5);
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
    print("🎬 RENDERIZANDO VIDEO MOTION GRAPHICS: JEV (SISTEMA 1)")
    print("=" * 50)
    extract_teaser_audio()
    write_hyperframes_html()
    render_with_hyperframes()

if __name__ == "__main__":
    main()
