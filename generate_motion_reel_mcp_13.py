"""
sIA Motion Graphics Reel Generator: Reel #13 (Model Context Protocol - MCP)
Genera un reel cinemático vertical (1080x1920) 100% código en HyperFrames:
- El infierno de las APIs REST heterogéneas para agentes (Acto 1).
- La arquitectura MCP: bus estándar cliente-servidor JSON-RPC 2.0 (Acto 2).
- Servidores MCP modulares: SQL Database, Filesystem, Git Tools.
- Badges de telemetría: JSON-RPC 2.0 Nativo, Estándar Abierto Anthropic, Cero Acoplamiento.
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

SOURCE_AUDIO = AUDIO_DIR / "sIA_DeepDive_MCP_Agentes_Produccion.mp3"
TARGET_REEL = REELS_DIR / "sIA_Reel_13_MCP_Agentes_Produccion.mp4"
DURATION = 21.0
START_OFFSET = "00:00:47.0"

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
    <div id="root" data-composition-id="sia_motion_reel_mcp" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
          radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 65%),
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

      /* HERO STAGE: REST SPAGHETTI VS MCP BUS */
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

      /* ACT 1: SPAGHETTI REST */
      .rest-container {
        position: absolute;
        width: 860px;
        height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      /* ACT 2: MCP BUS ARCHITECTURE */
      .mcp-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 0;
      }
      .mcp-svg {
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
          sIA DEEP DIVE • AGENTIC PROTOCOLS
        </div>
        <div class="badge-telemetry">
          ANTHROPIC MCP // BUS ESTÁNDAR
        </div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card" id="hookCard">
        <div class="hook-label">
          <span>🌐</span> EL NUEVO BUS DE DATOS UNIVERSAL
        </div>
        <div class="hook-title">
          "Las APIs REST están muriendo. El futuro de los agentes se llama <span class="alert-hl">Model Context Protocol</span>."
        </div>
      </div>

      <!-- HERO STAGE (REST Spaghetti vs MCP Bus) -->
      <div class="hero-stage" id="heroStage">
        <div class="stage-header">
          <span id="stageTitle">EL COLAPSO DE LAS APIS REST EN AGENTES</span>
          <span id="stageTelemetry">ACOPILAMIENTO: N × M // ALTO RIESGO</span>
        </div>

        <!-- ACT 1: Spaghetti REST Architecture Visual -->
        <div class="rest-container" id="restContainer">
          <svg width="800" height="460" viewBox="0 0 800 460">
            <!-- Central LLM -->
            <circle cx="400" cy="230" r="60" fill="#1e1b4b" stroke="#ef4444" stroke-width="3"/>
            <text x="400" y="225" fill="#ffffff" font-family="JetBrains Mono" font-size="16" text-anchor="middle" font-weight="900">LLM AGENT</text>
            <text x="400" y="248" fill="#f87171" font-family="JetBrains Mono" font-size="12" text-anchor="middle">Custom Prompts</text>

            <!-- Scattered Incompatible Endpoints -->
            <rect x="80" y="80" width="160" height="60" rx="10" fill="#450a0a" stroke="#ef4444" stroke-width="2"/>
            <text x="160" y="115" fill="#fca5a5" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">REST API #1 (SQL)</text>

            <rect x="560" y="80" width="160" height="60" rx="10" fill="#450a0a" stroke="#ef4444" stroke-width="2"/>
            <text x="640" y="115" fill="#fca5a5" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">REST API #2 (Files)</text>

            <rect x="80" y="320" width="160" height="60" rx="10" fill="#450a0a" stroke="#ef4444" stroke-width="2"/>
            <text x="160" y="355" fill="#fca5a5" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">REST API #3 (GitHub)</text>

            <rect x="560" y="320" width="160" height="60" rx="10" fill="#450a0a" stroke="#ef4444" stroke-width="2"/>
            <text x="640" y="355" fill="#fca5a5" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">REST API #4 (Slack)</text>

            <!-- Tangled Spaghetti lines -->
            <line x1="240" y1="110" x2="350" y2="190" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="6 4"/>
            <line x1="560" y1="110" x2="450" y2="190" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="6 4"/>
            <line x1="240" y1="350" x2="350" y2="270" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="6 4"/>
            <line x1="560" y1="350" x2="450" y2="270" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="6 4"/>

            <!-- Warning banner -->
            <rect x="180" y="410" width="440" height="40" rx="10" fill="rgba(220, 38, 38, 0.2)" stroke="#ef4444" stroke-width="1.5"/>
            <text x="400" y="435" fill="#fee2e2" font-family="JetBrains Mono" font-size="15" text-anchor="middle" font-weight="800">⚠️ INFRAESTRUCTURA FRÁGIL • N × M ESQUEMAS</text>
          </svg>
        </div>

        <!-- ACT 2: MCP Protocol Bus Blueprint -->
        <div class="mcp-container" id="mcpContainer">
          <svg class="mcp-svg" viewBox="0 0 860 640">
            <!-- MCP Host / Client Node (Left) -->
            <rect x="50" y="180" width="220" height="240" rx="18" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" stroke-width="2.5"/>
            <text x="160" y="230" fill="#67e8f9" font-family="JetBrains Mono" font-size="20" text-anchor="middle" font-weight="900">MCP HOST</text>
            <text x="160" y="260" fill="#94a3b8" font-family="JetBrains Mono" font-size="14" text-anchor="middle">Antigravity / Claude</text>
            
            <rect x="70" y="280" width="180" height="50" rx="8" fill="rgba(0,0,0,0.4)"/>
            <text x="160" y="312" fill="#38bdf8" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">JSON-RPC 2.0</text>
            
            <rect x="70" y="345" width="180" height="50" rx="8" fill="rgba(0,0,0,0.4)"/>
            <text x="160" y="377" fill="#34d399" font-family="JetBrains Mono" font-size="14" text-anchor="middle" font-weight="700">✓ DYNAMIC DISCOVERY</text>

            <!-- Universal MCP Bus Pipe (Center) -->
            <rect id="mcpBus" x="320" y="120" width="120" height="360" rx="16" fill="rgba(139, 92, 246, 0.25)" stroke="#a855f7" stroke-width="3"/>
            <text x="380" y="160" fill="#ffffff" font-family="JetBrains Mono" font-size="18" text-anchor="middle" font-weight="900">MCP</text>
            <text x="380" y="185" fill="#c084fc" font-family="JetBrains Mono" font-size="14" text-anchor="middle">BUS</text>

            <!-- Bus Connectors -->
            <line x1="270" y1="300" x2="320" y2="300" stroke="#06b6d4" stroke-width="4"/>

            <!-- Modular MCP Servers (Right) -->
            <!-- Server 1: SQL Database -->
            <line x1="440" y1="180" x2="520" y2="180" stroke="#a855f7" stroke-width="3"/>
            <rect x="520" y="140" width="280" height="80" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
            <text x="660" y="175" fill="#e0f2fe" font-family="JetBrains Mono" font-size="16" text-anchor="middle" font-weight="800">DATABASE SERVER</text>
            <text x="660" y="200" fill="#94a3b8" font-family="JetBrains Mono" font-size="13" text-anchor="middle">tools/read_query • schema</text>

            <!-- Server 2: Filesystem -->
            <line x1="440" y1="300" x2="520" y2="300" stroke="#a855f7" stroke-width="3"/>
            <rect x="520" y="260" width="280" height="80" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
            <text x="660" y="295" fill="#a7f3d0" font-family="JetBrains Mono" font-size="16" text-anchor="middle" font-weight="800">FILESYSTEM SERVER</text>
            <text x="660" y="320" fill="#94a3b8" font-family="JetBrains Mono" font-size="13" text-anchor="middle">resources/read • scoped</text>

            <!-- Server 3: Git / Bash -->
            <line x1="440" y1="420" x2="520" y2="420" stroke="#a855f7" stroke-width="3"/>
            <rect x="520" y="380" width="280" height="80" rx="12" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
            <text x="660" y="415" fill="#e9d5ff" font-family="JetBrains Mono" font-size="16" text-anchor="middle" font-weight="800">CLI & REPO SERVER</text>
            <text x="660" y="440" fill="#94a3b8" font-family="JetBrains Mono" font-size="13" text-anchor="middle">tools/run_command • git</text>
          </svg>
        </div>

        <!-- Telemetry Metrics Grid -->
        <div class="metrics-grid">
          <div class="metric-badge">
            <span class="metric-value">JSON-RPC</span>
            <span class="metric-desc">Protocolo Estándar 2.0</span>
          </div>
          <div class="metric-badge">
            <span class="metric-value">0% Lock-in</span>
            <span class="metric-desc">Interoperable en Cualquier LLM</span>
          </div>
        </div>
      </div>

      <!-- SUBTITLES & AUDIO CARD -->
      <div class="subtitles-card">
        <div class="speaker-tag" id="speakerTag">
          <span>🎙️</span> JORGE (ARQUITECTURA DE INTEGRACIÓN)
        </div>
        <div class="subtitles-text" id="subtitlesText">
          "Y la tesis central con la que abrimos hoy es contundente: el protocolo MCP está reemplazando a las APIs REST..."
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

      // ACT 1 (0.0s - 9.5s): El colapso de las APIs REST para agentes
      tl.from(".header-hud", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.2);
      tl.from("#hookCard", { scale: 0.95, opacity: 0, duration: 0.8, ease: "power3.out" }, 0.4);
      tl.from("#restContainer", { scale: 0.85, opacity: 0, duration: 1.0, ease: "power3.out" }, 0.6);

      // Subtitles Sync Act 1
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Y la tesis central con la que abrimos hoy es contundente...";
      }, null, 0.2);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "...el protocolo MCP está reemplazando a las APIs REST como el bus estándar entre IA y herramientas.";
      }, null, 3.5);

      // TRANSITION TO ACT 2 (9.5s): Dalia presenta el Bus MCP
      tl.call(() => {
        document.getElementById("speakerTag").innerHTML = "<span>🎙️</span> DALIA (ARQUITECTURA AGÉNTICA)";
        document.getElementById("stageTitle").innerHTML = "MODEL CONTEXT PROTOCOL // BUS UNIVERSAL";
        document.getElementById("stageTelemetry").innerHTML = "ESTÁNDAR ABIERTO • CLIENTE/SERVIDOR";
      }, null, 9.5);

      // Fade out REST, Fade in MCP
      tl.to("#restContainer", { opacity: 0, scale: 0.9, duration: 0.7, ease: "power2.in" }, 9.5);
      tl.to("#mcpContainer", { opacity: 1, duration: 0.8, ease: "power2.out" }, 10.2);

      // Subtitles Act 2
      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "Las piezas encajan con precisión: en lugar de acoplar código a cada API individual...";
      }, null, 10.0);

      tl.call(() => {
        document.getElementById("subtitlesText").innerHTML = "<span style='color: #38bdf8; font-weight: 800;'>...MCP expone herramientas y recursos en un protocolo único JSON-RPC 2.0 seguro y dinámico.</span>";
      }, null, 14.5);
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
    print("🎬 RENDERIZANDO VIDEO MOTION GRAPHICS: MCP AGENTES (REEL #13)")
    print("=" * 50)
    extract_teaser_audio()
    write_hyperframes_html()
    render_with_hyperframes()

if __name__ == "__main__":
    main()
