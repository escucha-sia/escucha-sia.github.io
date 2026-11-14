import json
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
TIMESTAMPS_FILE = ROOT_DIR / "scratch" / "apagon_timestamps.json"
OUT_HTML = ROOT_DIR / "sia_tiktok_batch_engine" / "compositions" / "apagon_global_scene.html"

with open(TIMESTAMPS_FILE, "r", encoding="utf-8") as f:
    segments = json.load(f)

TOTAL_DUR = 258.22

# 5 Actos definidos según los timings de audio
acts = [
    {"num": 1, "title": "EL MINUTO CERO: APAGÓN", "start": 0.0, "end": 50.02},
    {"num": 2, "title": "LA CHISPA: RECONFIGURACIÓN", "start": 50.02, "end": 92.83},
    {"num": 3, "title": "DOMINÓ DE HEALTH CHECKS", "start": 92.83, "end": 146.16},
    {"num": 4, "title": "THUNDERING HERD: ESTAMPIDA", "start": 146.16, "end": 202.97},
    {"num": 5, "title": "AUTOPSIA FORENSE & DEBATE", "start": 202.97, "end": 258.22}
]

card_css = []
for act in acts:
    s_pct = (act["start"] / TOTAL_DUR) * 100
    e_pct = (act["end"] / TOTAL_DUR) * 100
    num = act["num"]
    card_css.append(f"""
    #card-{num} {{
      animation: scene{num}Anim {TOTAL_DUR}s linear infinite;
    }}
    @keyframes scene{num}Anim {{
      0%, {max(0, s_pct - 0.05):.3f}% {{ opacity: 0; visibility: hidden; pointer-events: none; }}
      {s_pct:.3f}%, {e_pct - 0.05:.3f}% {{ opacity: 1; visibility: visible; pointer-events: auto; }}
      {e_pct:.3f}%, 100% {{ opacity: 0; visibility: hidden; pointer-events: none; }}
    }}""")

chap_css = []
for act in acts:
    num = act["num"]
    s_pct = (act["start"] / TOTAL_DUR) * 100
    e_pct = (act["end"] / TOTAL_DUR) * 100
    chap_css.append(f"""
    #pill-{num} {{ animation: c{num}Anim {TOTAL_DUR}s linear infinite; }}
    @keyframes c{num}Anim {{
      0%, {max(0, s_pct - 0.05):.3f}% {{ background: rgba(255, 255, 255, 0.06); color: #94a3b8; border-color: rgba(255, 255, 255, 0.12); }}
      {s_pct:.3f}%, {e_pct - 0.05:.3f}% {{ background: #ef4444; color: #fff; border-color: #ef4444; font-weight: 900; box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); }}
      {e_pct:.3f}%, 100% {{ background: rgba(255, 255, 255, 0.06); color: #94a3b8; border-color: rgba(255, 255, 255, 0.12); }}
    }}""")

sub_items = []
sub_css = []
for idx, seg in enumerate(segments):
    s_pct = (seg["start"] / TOTAL_DUR) * 100
    e_pct = (seg["end"] / TOTAL_DUR) * 100
    icon = "🎙️ JORGE" if seg["voice"] == "Jorge" else "🎙️ DALIA"
    badge_bg = "linear-gradient(135deg, #0284c7, #38bdf8)" if seg["voice"] == "Jorge" else "linear-gradient(135deg, #ec4899, #f43f5e)"

    sub_items.append(f"""
    <div id="sub-{idx}" class="sub-bubble">
      <div class="sub-speaker" style="background: {badge_bg};">{icon}</div>
      <div class="sub-text">{seg['text']}</div>
    </div>
    """)

    sub_css.append(f"""
    #sub-{idx} {{ animation: sub{idx}Anim {TOTAL_DUR}s linear infinite; }}
    @keyframes sub{idx}Anim {{
      0%, {max(0, s_pct - 0.05):.3f}% {{ opacity: 0; transform: translateY(14px) scale(0.98); visibility: hidden; }}
      {s_pct:.3f}%, {e_pct - 0.05:.3f}% {{ opacity: 1; transform: translateY(0) scale(1); visibility: visible; }}
      {e_pct:.3f}%, 100% {{ opacity: 0; transform: translateY(-8px) scale(0.98); visibility: hidden; }}
    }}
    """)

html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>sIA Crónicas #14 - El Apagón Global de Microsoft</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800;900&family=Montserrat:wght@400;600;700;800;900&family=Space+Grotesk:wght@500;700;800&display=swap');

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: 1080px;
      height: 1920px;
      background: #030611;
      font-family: 'Montserrat', sans-serif;
      color: #fff;
      overflow: hidden;
    }}

    #scene-root {{
      position: relative;
      width: 1080px;
      height: 1920px;
      background: radial-gradient(circle at 50% 30%, #0d1527 0%, #030611 75%);
      overflow: hidden;
    }}

    .bg-grid {{
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(239, 68, 68, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(239, 68, 68, 0.04) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
    }}

    .laser-scanner {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, transparent, #ef4444, #38bdf8, transparent);
      box-shadow: 0 0 20px #ef4444, 0 0 40px #38bdf8;
      animation: laserSweep 3.2s ease-in-out infinite;
      z-index: 50;
      pointer-events: none;
    }}
    @keyframes laserSweep {{
      0% {{ transform: translateY(0); opacity: 0; }}
      10% {{ opacity: 1; }}
      90% {{ opacity: 1; }}
      100% {{ transform: translateY(1920px); opacity: 0; }}
    }}

    .top-header {{
      position: absolute;
      top: 36px;
      left: 40px;
      right: 40px;
      height: 90px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 40;
    }}

    .show-badge {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(239, 68, 68, 0.12);
      border: 2px solid #ef4444;
      padding: 10px 22px;
      border-radius: 999px;
      box-shadow: 0 0 25px rgba(239, 68, 68, 0.35);
    }}

    .dot-beacon {{
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #ef4444;
      box-shadow: 0 0 14px #ef4444;
      animation: beaconPulse 1s infinite alternate;
    }}
    @keyframes beaconPulse {{
      0% {{ transform: scale(0.9); opacity: 0.6; }}
      100% {{ transform: scale(1.4); opacity: 1; }}
    }}

    .show-title {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 900;
      font-size: 21px;
      letter-spacing: 1.5px;
      color: #fff;
    }}

    .channel-handle {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      color: #94a3b8;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 8px 18px;
      border-radius: 999px;
    }}

    .act-navigator {{
      position: absolute;
      top: 140px;
      left: 40px;
      right: 40px;
      height: 50px;
      display: flex;
      gap: 10px;
      z-index: 40;
    }}

    .act-pill {{
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 12px;
      border: 1.5px solid rgba(255, 255, 255, 0.12);
      background: rgba(255, 255, 255, 0.05);
      font-family: 'JetBrains Mono', monospace;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 1px;
      color: #94a3b8;
      text-transform: uppercase;
      transition: all 0.3s ease;
    }}

    {"".join(chap_css)}

    .main-stage {{
      position: absolute;
      top: 206px;
      left: 40px;
      right: 40px;
      height: 1330px;
      z-index: 20;
    }}

    .scene-card {{
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      background: #040817;
      border-radius: 24px;
      border: 2px solid rgba(239, 68, 68, 0.35);
      padding: 24px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }}

    {"".join(card_css)}

    .card-topbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 14px;
      margin-bottom: 16px;
    }}

    .card-act-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      color: #ef4444;
      font-weight: 800;
      letter-spacing: 2px;
    }}

    .card-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 25px;
      font-weight: 900;
      color: #fff;
      letter-spacing: 0.5px;
    }}

    .card-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid #ef4444;
      color: #fca5a5;
      padding: 4px 12px;
      border-radius: 6px;
      font-weight: 700;
    }}

    .subtitles-container {{
      position: absolute;
      bottom: 56px;
      left: 40px;
      right: 40px;
      height: 250px;
      z-index: 30;
      display: flex;
      justify-content: center;
      align-items: center;
      background: rgba(4, 8, 23, 0.88);
      border: 1.5px solid rgba(56, 189, 248, 0.25);
      border-radius: 20px;
      padding: 20px 28px;
      backdrop-filter: blur(14px);
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
    }}

    .sub-bubble {{
      position: absolute;
      inset: 20px 28px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      gap: 12px;
      opacity: 0;
      visibility: hidden;
      transition: all 0.25s ease;
    }}

    .sub-speaker {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: 1.5px;
      color: #fff;
      padding: 5px 14px;
      border-radius: 6px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }}

    .sub-text {{
      font-family: 'Montserrat', sans-serif;
      font-size: 25.5px;
      font-weight: 700;
      line-height: 1.34;
      color: #ffffff;
      text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
    }}

    {"".join(sub_css)}

    .bottom-telemetry {{
      position: absolute;
      bottom: 14px;
      left: 40px;
      right: 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: #64748b;
      z-index: 30;
    }}

    @keyframes alertBlink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}

    @keyframes radarSpin {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}

    @keyframes clockPulse {{
      0%, 100% {{ text-shadow: 0 0 20px #ef4444, 0 0 45px rgba(239, 68, 68, 0.7); transform: scale(1); }}
      50% {{ text-shadow: 0 0 35px #ef4444, 0 0 70px rgba(239, 68, 68, 0.95); transform: scale(1.02); }}
    }}

    @keyframes packetFlow {{
      0% {{ stroke-dashoffset: 80; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    @keyframes shockwave {{
      0% {{ r: 10; opacity: 1; }}
      100% {{ r: 180; opacity: 0; }}
    }}

    @keyframes hazardScroll {{
      from {{ background-position: 0 0; }}
      to {{ background-position: 60px 0; }}
    }}
  </style>
</head>
<body>
  <div id="scene-root" data-composition-id="apagon_global_scene" data-no-timeline data-start="0" data-duration="{TOTAL_DUR}" data-width="1080" data-height="1920">
    <div class="bg-grid"></div>
    <div class="laser-scanner"></div>

    <!-- TOP HEADER -->
    <header class="top-header">
      <div class="show-badge">
        <div class="dot-beacon"></div>
        <div class="show-title">sIA CRÓNICAS #14</div>
      </div>
      <div class="channel-handle">@escucha_sia &bull; DILOG&Iacute;A MICROSOFT &bull; PARTE 2</div>
    </header>

    <!-- ACT NAVIGATOR -->
    <nav class="act-navigator">
      <div id="pill-1" class="act-pill">1. MINUTO CERO</div>
      <div id="pill-2" class="act-pill">2. LA CHISPA</div>
      <div id="pill-3" class="act-pill">3. HEALTH CHECKS</div>
      <div id="pill-4" class="act-pill">4. THUNDERING HERD</div>
      <div id="pill-5" class="act-pill">5. AUTOPSIA FORENSE</div>
    </nav>

    <!-- MAIN VISUAL STAGE (75% SCREEN) -->
    <main class="main-stage">

      <!-- ========================================== -->
      <!-- ACTO 1: SCROLL-STOPPER • MINUTO CERO APAGÓN -->
      <!-- ========================================== -->
      <article id="card-1" class="scene-card" style="border-color: #ef4444;">
        <div class="card-topbar">
          <div>
            <div class="card-act-num">ACTO 01 &bull; EL MINUTO CERO DEL COLAPSO</div>
            <h2 class="card-title">EL D&Iacute;A QUE MICROSOFT SE APAG&Oacute;</h2>
          </div>
          <div class="card-tag" style="background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #ff6b6b; animation: alertBlink 0.8s infinite;">
            SEV-0 &bull; CRISIS GLOBAL
          </div>
        </div>

        <div style="width: 100%; height: 16px; background: repeating-linear-gradient(45deg, #ef4444, #ef4444 14px, #000 14px, #000 28px); border-radius: 4px; margin-bottom: 14px; animation: hazardScroll 2s linear infinite;"></div>

        <!-- CRONÓMETRO GIGANTE DE APAGÓN -->
        <div style="background: rgba(15, 23, 42, 0.95); border: 2.5px solid #ef4444; border-radius: 18px; padding: 18px 24px; text-align: center; box-shadow: 0 0 35px rgba(239, 68, 68, 0.35); margin-bottom: 18px;">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #fca5a5; letter-spacing: 3px; font-weight: 800; margin-bottom: 6px;">
            TIEMPO FUERA DE SERVICIO GLOBAL (DOWNTIME)
          </div>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 54px; font-weight: 900; color: #ff334b; animation: clockPulse 1.8s ease-in-out infinite; letter-spacing: 4px;">
            18h : 42m : 10s
          </div>
          <div style="display: flex; justify-content: center; gap: 16px; margin-top: 8px;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; background: rgba(239,68,68,0.2); padding: 4px 10px; border-radius: 6px; color: #ff8585; font-weight: bold;">74 PA&Iacute;SES A OSCURAS</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; background: rgba(56,189,248,0.15); padding: 4px 10px; border-radius: 6px; color: #38bdf8; font-weight: bold;">0% CIBERATAQUE</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; background: rgba(245,158,11,0.15); padding: 4px 10px; border-radius: 6px; color: #fbbf24; font-weight: bold;">100% INGENIER&Iacute;A</span>
          </div>
        </div>

        <!-- RADAR GLOBAL DE COLAPSO -->
        <div style="flex: 1; position: relative; background: #030614; border: 1.5px solid rgba(239, 68, 68, 0.3); border-radius: 18px; overflow: hidden; display: flex; flex-direction: column;">
          <div style="padding: 10px 16px; background: rgba(239, 68, 68, 0.08); border-bottom: 1px solid rgba(239, 68, 68, 0.2); display: flex; justify-content: space-between; align-items: center;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #f87171; font-weight: bold;">🛰️ RADAR DE AFECTACI&Oacute;N DE TELECOMUNICACIONES</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94a3b8;">12-NOV-2026 &bull; 13:26 ET</span>
          </div>

          <svg viewBox="0 0 940 500" style="width: 100%; height: 100%;">
            <defs>
              <pattern id="radarGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
              </pattern>
              <filter id="redGlow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="8" result="blur"/>
                <feMerge>
                  <feMergeNode in="blur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>

            <rect width="940" height="500" fill="url(#radarGrid)"/>
            <circle cx="470" cy="250" r="100" fill="none" stroke="rgba(239, 68, 68, 0.15)" stroke-width="1.5" stroke-dasharray="4 4"/>
            <circle cx="470" cy="250" r="200" fill="none" stroke="rgba(239, 68, 68, 0.12)" stroke-width="1.5" stroke-dasharray="6 6"/>
            <circle cx="470" cy="250" r="300" fill="none" stroke="rgba(239, 68, 68, 0.08)" stroke-width="1.5"/>

            <g transform="translate(470, 250)">
              <g style="animation: radarSpin 6s linear infinite; transform-origin: 0 0;">
                <line x1="0" y1="0" x2="350" y2="0" stroke="rgba(239, 68, 68, 0.6)" stroke-width="2"/>
                <polygon points="0,0 350,0 350,-40" fill="rgba(239, 68, 68, 0.08)"/>
              </g>
            </g>

            <!-- Londres -->
            <g transform="translate(440, 160)">
              <circle r="22" fill="none" stroke="#ef4444" stroke-width="1.5" opacity="0.8" style="animation: alertBlink 1s infinite;"/>
              <circle r="7" fill="#ef4444" filter="url(#redGlow)"/>
              <text x="18" y="5" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">LONDRES [BANCO DE INGLATERRA]</text>
              <text x="18" y="22" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">OFFLINE &bull; LIQUIDACI&Oacute;N DETENIDA</text>
            </g>

            <!-- Frankfurt -->
            <g transform="translate(490, 190)">
              <circle r="18" fill="none" stroke="#ef4444" stroke-width="1.5" opacity="0.8" style="animation: alertBlink 1.2s infinite;"/>
              <circle r="6" fill="#ef4444" filter="url(#redGlow)"/>
              <text x="16" y="5" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">FR&Aacute;NCFORT [DESPACHO A&Eacute;REO]</text>
              <text x="16" y="20" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">OFFLINE &bull; RETRASOS MASIVOS</text>
            </g>

            <!-- Nueva York -->
            <g transform="translate(240, 210)">
              <circle r="24" fill="none" stroke="#ef4444" stroke-width="2" style="animation: alertBlink 0.9s infinite;"/>
              <circle r="8" fill="#ef4444" filter="url(#redGlow)"/>
              <text x="-210" y="5" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">NUEVA YORK [ENTRA ID]</text>
              <text x="-210" y="22" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">AUTENTICACI&Oacute;N: 0% TOKEN FAIL</text>
            </g>

            <!-- Tokio -->
            <g transform="translate(760, 220)">
              <circle r="18" fill="none" stroke="#ef4444" stroke-width="1.5" opacity="0.8" style="animation: alertBlink 1.4s infinite;"/>
              <circle r="6" fill="#ef4444" filter="url(#redGlow)"/>
              <text x="-160" y="5" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">TOKIO [M365 ASIA]</text>
              <text x="-160" y="20" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">TIMEOUT GENERALIZADO</text>
            </g>

            <!-- Sao Paulo -->
            <g transform="translate(320, 380)">
              <circle r="16" fill="none" stroke="#ef4444" stroke-width="1.5" opacity="0.8" style="animation: alertBlink 1.1s infinite;"/>
              <circle r="5" fill="#ef4444" filter="url(#redGlow)"/>
              <text x="16" y="5" fill="#fff" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">S&Atilde;O PAULO [HOSPITALES]</text>
              <text x="16" y="20" fill="#f87171" font-family="'JetBrains Mono'" font-size="10.5">HISTORIALES INACCESIBLES</text>
            </g>

            <path d="M 240 210 Q 340 160 440 160" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 4" opacity="0.6"/>
            <path d="M 440 160 L 490 190" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 4" opacity="0.6"/>
            <path d="M 490 190 Q 620 180 760 220" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 4" opacity="0.6"/>
            <path d="M 240 210 Q 280 300 320 380" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 4" opacity="0.6"/>
          </svg>

          <div style="background: rgba(0,0,0,0.6); padding: 8px 16px; border-top: 1px solid rgba(255,255,255,0.08); display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11.5px;">
            <span style="color: #ef4444;">🔴 AZURE WAN: STATUS COLLAPSED</span>
            <span style="color: #f59e0b;">⚠️ TEAMS: 0 CALLS CONNECTED</span>
            <span style="color: #38bdf8;">🌐 OUTLOOK: CONNECTION TIMEOUT</span>
          </div>
        </div>

        <div style="margin-top: 14px; background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px 18px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #fff; line-height: 1.4;">
            <strong>LA MAYOR CA&Iacute;DA DE LA D&Eacute;CADA:</strong> No fue una tormenta solar ni sabotaje militar. Fue el software automatizado de Microsoft comi&eacute;ndose a s&iacute; mismo en un ciclo mortal sin intervenci&oacute;n humana.
          </div>
        </div>
      </article>

      <!-- ========================================== -->
      <!-- ACTO 2: LA CHISPA: RECONFIGURACIÓN DE RUTINA -->
      <!-- ========================================== -->
      <article id="card-2" class="scene-card" style="border-color: #f59e0b;">
        <div class="card-topbar">
          <div>
            <div class="card-act-num" style="color: #f59e0b;">ACTO 02 &bull; EL ORIGEN INVISIBLE</div>
            <h2 class="card-title">LA CHISPA: UNA REGLA DE RED DE RUTINA</h2>
          </div>
          <div class="card-tag" style="background: rgba(245, 158, 11, 0.15); border-color: #f59e0b; color: #fbbf24;">
            SCRIPT AUTOM&Aacute;TICO
          </div>
        </div>

        <div style="text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cbd5e1; margin-bottom: 12px;">
          DESPLIEGUE DESATENDIDO EN CL&Uacute;STERES AZURE FRONT-DOOR (13:26 ET)
        </div>

        <div style="flex: 1; position: relative; background: #030614; border: 1.5px solid rgba(245, 158, 11, 0.3); border-radius: 18px; padding: 16px; display: flex; flex-direction: column; gap: 14px;">
          
          <!-- FILA 1: PIPELINE CI/CD DESATENDIDO -->
          <div style="background: rgba(15, 23, 42, 0.95); border: 1.5px solid #38bdf8; border-radius: 14px; padding: 14px 20px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 14px;">
              <span style="font-size: 26px;">⚙️</span>
              <div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 14px; color: #38bdf8; font-weight: bold;">push_wan_capacity_v4.py</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 12.5px; color: #94a3b8;">Actualizaci&oacute;n de balanceo din&aacute;mico de tr&aacute;fico regional</div>
              </div>
            </div>
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #ff8585; font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 4px 10px; border-radius: 6px; font-weight: bold;">
              CERO AUDITOR&Iacute;A HUMANA
            </div>
          </div>

          <!-- DIAGRAMA SVG CENTRAL: PROPAGACIÓN Y COLAPSO DE MEMORIA -->
          <div style="flex: 1; background: #02040d; border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 12px; overflow: hidden;">
            <svg viewBox="0 0 900 360" style="width: 100%; height: 100%;">
              <defs>
                <linearGradient id="flowGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#38bdf8"/>
                  <stop offset="50%" stop-color="#f59e0b"/>
                  <stop offset="100%" stop-color="#ef4444"/>
                </linearGradient>
              </defs>

              <!-- Servidor de Despliegue CI/CD -->
              <g transform="translate(100, 180)">
                <rect x="-80" y="-55" width="160" height="110" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
                <text x="0" y="-20" text-anchor="middle" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">DEPLOY SCRIPT</text>
                <text x="0" y="5" text-anchor="middle" fill="#fff" font-family="'Space Grotesk'" font-size="12">Sin Validaci&oacute;n</text>
                <text x="0" y="25" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="10.5">Autom&aacute;tico</text>
              </g>

              <!-- Líneas animadas hacia el Switch Wan -->
              <path d="M 180 180 L 410 180" fill="none" stroke="url(#flowGrad)" stroke-width="4" stroke-dasharray="10 6" style="animation: packetFlow 1s linear infinite;"/>

              <!-- WAN Core Router Central -->
              <g transform="translate(470, 180)">
                <rect x="-85" y="-95" width="170" height="190" rx="16" fill="#0f172a" stroke="#ef4444" stroke-width="2.5"/>
                <text x="0" y="-60" text-anchor="middle" fill="#ef4444" font-family="'JetBrains Mono'" font-size="13" font-weight="900">ROUTER WAN CORE</text>
                <line x1="-70" y1="-45" x2="70" y2="-45" stroke="rgba(255,255,255,0.1)"/>

                <text x="0" y="-20" text-anchor="middle" fill="#fca5a5" font-family="'Space Grotesk'" font-size="11">Tabla BGP Saturada</text>
                <text x="0" y="0" text-anchor="middle" fill="#ff4d4d" font-family="'JetBrains Mono'" font-size="16" font-weight="900">MEMORIA: 100%</text>

                <!-- Barra de memoria en rojo -->
                <rect x="-65" y="15" width="130" height="16" rx="4" fill="rgba(255,255,255,0.1)"/>
                <rect x="-65" y="15" width="130" height="16" rx="4" fill="#ef4444" style="animation: alertBlink 0.8s infinite;"/>

                <text x="0" y="55" text-anchor="middle" fill="#fbbf24" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">LATENCIA: 620ms</text>
                <text x="0" y="75" text-anchor="middle" fill="#ef4444" font-family="'JetBrains Mono'" font-size="10">TIMEOUT DE SOCKETS</text>
              </g>

              <!-- Conexiones a Clústeres de Regiones -->
              <path d="M 555 140 Q 640 100 720 90" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="8 4" style="animation: packetFlow 0.8s linear infinite;"/>
              <path d="M 555 180 L 720 180" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="8 4" style="animation: packetFlow 0.8s linear infinite;"/>
              <path d="M 555 220 Q 640 260 720 270" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="8 4" style="animation: packetFlow 0.8s linear infinite;"/>

              <!-- Clústeres afectados -->
              <g transform="translate(790, 90)">
                <rect x="-65" y="-30" width="130" height="60" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">AMER-EAST</text>
                <text x="0" y="12" text-anchor="middle" fill="#ef4444" font-family="'JetBrains Mono'" font-size="10">BUFFER DROPS</text>
              </g>

              <g transform="translate(790, 180)">
                <rect x="-65" y="-30" width="130" height="60" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">EMEA-WEST</text>
                <text x="0" y="12" text-anchor="middle" fill="#ef4444" font-family="'JetBrains Mono'" font-size="10">SOCKET STALL</text>
              </g>

              <g transform="translate(790, 270)">
                <rect x="-65" y="-30" width="130" height="60" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">APAC-SOUTH</text>
                <text x="0" y="12" text-anchor="middle" fill="#ef4444" font-family="'JetBrains Mono'" font-size="10">PACKET LOSS</text>
              </g>
            </svg>
          </div>

          <!-- FILA 3: CAUSA RAÍZ TÉCNICA -->
          <div style="background: rgba(245, 158, 11, 0.08); border: 1.5px solid rgba(245, 158, 11, 0.4); border-radius: 14px; padding: 14px 18px;">
            <div style="font-family: 'Montserrat', sans-serif; font-size: 14px; font-weight: 800; color: #fbbf24; margin-bottom: 6px;">
              🔬 LA AUTOPSIA DEL ERROR DE CONFIGURACI&Oacute;N:
            </div>
            <ul style="list-style: none; font-family: 'Space Grotesk', sans-serif; font-size: 12.5px; color: #cbd5e1; line-height: 1.45;">
              <li style="margin-bottom: 4px;">&bull; <strong>El Cambio:</strong> Se alter&oacute; la ponderaci&oacute;n regional para favorecer centros con menor costo el&eacute;ctrico.</li>
              <li>&bull; <strong>La Falla L&oacute;gica:</strong> La regla no conten&iacute;a sintaxis inv&aacute;lida, sino una condici&oacute;n recursiva que multiplicaba las tablas BGP por cada hilo de ejecuci&oacute;n concurrente.</li>
            </ul>
          </div>

        </div>

        <div style="margin-top: 14px; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 16px; text-align: center;">
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #94a3b8;">
            CON EQUIPOS DE INGENIER&Iacute;A COMPLETOS, ESTE ERROR SE ABORTABA EN 60 SEGUNDOS.
          </span>
        </div>
      </article>

      <!-- ========================================== -->
      <!-- ACTO 3: DOMINÓ DE HEALTH CHECKS CIEGOS -->
      <!-- ========================================== -->
      <article id="card-3" class="scene-card" style="border-color: #a855f7;">
        <div class="card-topbar">
          <div>
            <div class="card-act-num" style="color: #c084fc;">ACTO 03 &bull; EL MECANISMO DESTRUCCI&Oacute;N</div>
            <h2 class="card-title">LA CASCADA DE HEALTH CHECKS CIEGOS</h2>
          </div>
          <div class="card-tag" style="background: rgba(168, 85, 247, 0.15); border-color: #a855f7; color: #e9d5ff;">
            EFECTO DOMIN&Oacute;
          </div>
        </div>

        <div style="text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cbd5e1; margin-bottom: 12px;">
          EL SOFTWARE DISE&Ntilde;ADO PARA PROTEGER LA NUBE LA DERRIB&Oacute; EN 15 MINUTOS
        </div>

        <div style="flex: 1; position: relative; background: #030614; border: 1.5px solid rgba(168, 85, 247, 0.3); border-radius: 18px; padding: 16px; display: flex; flex-direction: column; gap: 14px;">
          
          <!-- SIMULACIÓN SVG: TRES SERVIDORES CAYENDO EN DOMINÓ -->
          <div style="flex: 1; background: #02040d; border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 12px; overflow: hidden;">
            <svg viewBox="0 0 900 360" style="width: 100%; height: 100%;">
              <defs>
                <filter id="purpleGlow">
                  <feGaussianBlur stdDeviation="6" result="blur"/>
                  <feMerge>
                    <feMergeNode in="blur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>

              <!-- Algoritmo de Monitoreo / Prober Central -->
              <g transform="translate(450, 45)">
                <rect x="-160" y="-25" width="320" height="50" rx="10" fill="#1e1026" stroke="#c084fc" stroke-width="2"/>
                <text x="0" y="5" text-anchor="middle" fill="#c084fc" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">HEALTH PROBER: PING CADA 500ms</text>
              </g>

              <!-- Peticiones de Probe hacia Nodos -->
              <path d="M 370 70 L 180 140" fill="none" stroke="#c084fc" stroke-width="2" stroke-dasharray="6 4" style="animation: packetFlow 1s linear infinite;"/>
              <path d="M 450 70 L 450 140" fill="none" stroke="#c084fc" stroke-width="2" stroke-dasharray="6 4" style="animation: packetFlow 1s linear infinite;"/>
              <path d="M 530 70 L 720 140" fill="none" stroke="#c084fc" stroke-width="2" stroke-dasharray="6 4" style="animation: packetFlow 1s linear infinite;"/>

              <!-- NODO 1 (LENTO -> MARCADO MUERTO) -->
              <g transform="translate(180, 230)">
                <rect x="-90" y="-80" width="180" height="160" rx="14" fill="#0f172a" stroke="#ef4444" stroke-width="2.5"/>
                <text x="0" y="-50" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">NODO A (ORIGEN)</text>
                <line x1="-70" y1="-35" x2="70" y2="-35" stroke="rgba(255,255,255,0.1)"/>
                <text x="0" y="-12" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="12">Latencia: 620ms</text>
                <text x="0" y="8" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">Timeout Excedido</text>
                <rect x="-70" y="22" width="140" height="28" rx="6" fill="#ef4444"/>
                <text x="0" y="41" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="12" font-weight="900">MUERTO (503)</text>
                <text x="0" y="68" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="10">Tr&aacute;fico desviado 100%</text>
              </g>

              <!-- FLECHA TRANSFERENCIA CARGA 1 -> 2 -->
              <g transform="translate(315, 230)">
                <path d="M -35 0 L 35 0" fill="none" stroke="#ef4444" stroke-width="4" stroke-dasharray="8 4" style="animation: packetFlow 0.6s linear infinite;"/>
                <text x="0" y="-12" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="10.5" font-weight="bold">+100% TR&Aacute;FICO</text>
              </g>

              <!-- NODO 2 (RECIBE DOBLE CARGA -> MUERTO) -->
              <g transform="translate(450, 230)">
                <rect x="-90" y="-80" width="180" height="160" rx="14" fill="#0f172a" stroke="#ef4444" stroke-width="2.5"/>
                <text x="0" y="-50" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">NODO B (VECINO)</text>
                <line x1="-70" y1="-35" x2="70" y2="-35" stroke="rgba(255,255,255,0.1)"/>
                <text x="0" y="-12" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="12">Carga: 200% Tr&aacute;fico</text>
                <text x="0" y="8" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">CPU al 100% (800ms)</text>
                <rect x="-70" y="22" width="140" height="28" rx="6" fill="#ef4444"/>
                <text x="0" y="41" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="12" font-weight="900">MUERTO (503)</text>
                <text x="0" y="68" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="10">Tr&aacute;fico desviado 100%</text>
              </g>

              <!-- FLECHA TRANSFERENCIA CARGA 2 -> 3 -->
              <g transform="translate(585, 230)">
                <path d="M -35 0 L 35 0" fill="none" stroke="#ef4444" stroke-width="4" stroke-dasharray="8 4" style="animation: packetFlow 0.6s linear infinite;"/>
                <text x="0" y="-12" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="10.5" font-weight="bold">+300% TR&Aacute;FICO</text>
              </g>

              <!-- NODO 3 (COLAPSO TOTAL REGIÓN) -->
              <g transform="translate(720, 230)">
                <rect x="-90" y="-80" width="180" height="160" rx="14" fill="#0f172a" stroke="#ef4444" stroke-width="2.5"/>
                <text x="0" y="-50" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">REGI&Oacute;N AZURE</text>
                <line x1="-70" y1="-35" x2="70" y2="-35" stroke="rgba(255,255,255,0.1)"/>
                <text x="0" y="-12" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="12">Carga Imposible</text>
                <text x="0" y="8" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="11">Blackout Total</text>
                <rect x="-70" y="22" width="140" height="28" rx="6" fill="#ef4444" style="animation: alertBlink 0.6s infinite;"/>
                <text x="0" y="41" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="12" font-weight="900">APAG&Oacute;N REGIONAL</text>
                <text x="0" y="68" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="10">15 min tras la chispa</text>
              </g>
            </svg>
          </div>

          <!-- PANELES DE EXPLICACIÓN FORENSE -->
          <div style="background: rgba(15, 23, 42, 0.9); border-left: 4px solid #a855f7; border-radius: 12px; padding: 14px 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-family: 'Montserrat', sans-serif; font-size: 14.5px; font-weight: 800; color: #e9d5ff;">
                LA PARADOJA DE LA ALTA DISPONIBILIDAD:
              </span>
              <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; background: rgba(168,85,247,0.2); color: #c084fc; padding: 2px 8px; border-radius: 4px; font-weight: bold;">
                EUTANASIA DIGITAL
              </span>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #cbd5e1; line-height: 1.4;">
              El balanceador retir&oacute; a todos los servidores sanos del cat&aacute;logo activo porque tardaban unos milisegundos de m&aacute;s. No se quem&oacute; ning&uacute;n cable: <strong>fue el sistema de emergencia suicidando a sus propios servidores</strong>.
            </p>
          </div>

        </div>

        <div style="margin-top: 14px; background: rgba(168, 85, 247, 0.08); border-left: 4px solid #a855f7; border-radius: 8px; padding: 10px 16px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #fff;">
            <strong>MEC&Aacute;NICA CIEGA:</strong> Asumir que un servidor ocupado est&aacute; muerto es el mayor pecado de dise&ntilde;o en arquitectura cloud distribuida.
          </div>
        </div>
      </article>

      <!-- ========================================== -->
      <!-- ACTO 4: THUNDERING HERD: LA ESTAMPIDA -->
      <!-- ========================================== -->
      <article id="card-4" class="scene-card" style="border-color: #ec4899;">
        <div class="card-topbar">
          <div>
            <div class="card-act-num" style="color: #f472b6;">ACTO 04 &bull; EL MONSTRUO DISTRIBUIDO</div>
            <h2 class="card-title">THUNDERING HERD: LA ESTAMPIDA</h2>
          </div>
          <div class="card-tag" style="background: rgba(236, 72, 153, 0.15); border-color: #ec4899; color: #fbcfe8;">
            COLD START SUICIDE
          </div>
        </div>

        <div style="text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cbd5e1; margin-bottom: 12px;">
          50,000,000 DE CLIENTES REINTENTANDO CONEXI&Oacute;N EN EL MISMO MILISEGUNDO
        </div>

        <div style="flex: 1; position: relative; background: #030614; border: 1.5px solid rgba(236, 72, 153, 0.3); border-radius: 18px; padding: 16px; display: flex; flex-direction: column; gap: 14px;">
          
          <!-- SIMULACIÓN SVG: ESTAMPIDA DE MILLONES DE CLIENTES CONTRA EL NODO -->
          <div style="flex: 1; background: #02040d; border: 1px solid rgba(236, 72, 153, 0.2); border-radius: 12px; overflow: hidden;">
            <svg viewBox="0 0 900 360" style="width: 100%; height: 100%;">
              <defs>
                <filter id="pinkGlow">
                  <feGaussianBlur stdDeviation="8" result="blur"/>
                  <feMerge>
                    <feMergeNode in="blur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>

              <!-- Ondas de choque que destruyen el nodo central -->
              <circle cx="450" cy="180" r="120" fill="none" stroke="#ef4444" stroke-width="2" opacity="0.6" style="animation: alertBlink 0.6s infinite;"/>
              <circle cx="450" cy="180" r="80" fill="none" stroke="#ec4899" stroke-width="2" opacity="0.8"/>

              <!-- Servidor en arranque en frío (Víctima) -->
              <g transform="translate(450, 180)">
                <rect x="-85" y="-60" width="170" height="120" rx="14" fill="#0f172a" stroke="#ec4899" stroke-width="3"/>
                <text x="0" y="-30" text-anchor="middle" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">COLD START SERVER</text>
                <text x="0" y="-5" text-anchor="middle" fill="#fff" font-family="'Space Grotesk'" font-size="14" font-weight="900">CPU: 100% CRASH</text>
                <rect x="-65" y="8" width="130" height="18" rx="4" fill="#ef4444"/>
                <text x="0" y="22" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="11" font-weight="900">ASFIXIA DE SOCKETS</text>
                <text x="0" y="44" text-anchor="middle" fill="#f472b6" font-family="'JetBrains Mono'" font-size="10">Muere antes de abrir TLS</text>
              </g>

              <!-- Clientes bombardeando alrededor -->
              <!-- Arriba -->
              <g transform="translate(450, 40)">
                <rect x="-100" y="-20" width="200" height="40" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="5" text-anchor="middle" fill="#ff6b6b" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">TEAMS: 20M REINTENTOS</text>
                <path d="M 0 20 L 0 110" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 4" style="animation: packetFlow 0.5s linear infinite;"/>
              </g>

              <!-- Abajo -->
              <g transform="translate(450, 320)">
                <rect x="-100" y="-20" width="200" height="40" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="5" text-anchor="middle" fill="#ff6b6b" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">OUTLOOK: 15M REINTENTOS</text>
                <path d="M 0 -20 L 0 -110" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 4" style="animation: packetFlow 0.5s linear infinite;"/>
              </g>

              <!-- Izquierda -->
              <g transform="translate(130, 180)">
                <rect x="-90" y="-25" width="180" height="50" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="-4" text-anchor="middle" fill="#ff6b6b" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">AZURE APIS & SDKs</text>
                <text x="0" y="14" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="10">Sin Exponential Backoff</text>
                <path d="M 90 0 L 355 0" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 4" style="animation: packetFlow 0.5s linear infinite;"/>
              </g>

              <!-- Derecha -->
              <g transform="translate(770, 180)">
                <rect x="-90" y="-25" width="180" height="50" rx="8" fill="#1e1026" stroke="#ef4444" stroke-width="1.5"/>
                <text x="0" y="-4" text-anchor="middle" fill="#ff6b6b" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">BANCOS & HOSPITALES</text>
                <text x="0" y="14" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="10">Reconexi&oacute;n Inmediata</text>
                <path d="M -90 0 L -355 0" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 4" style="animation: packetFlow 0.5s linear infinite;"/>
              </g>
            </svg>
          </div>

          <!-- LA SOLUCIÓN TÉCNICA EXTREMA -->
          <div style="background: rgba(15, 23, 42, 0.95); border: 1.5px solid #10b981; border-radius: 14px; padding: 14px 18px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
              <span style="font-size: 20px;">🛡️</span>
              <span style="font-family: 'Montserrat', sans-serif; font-size: 14px; font-weight: 800; color: #34d399;">
                LA &Uacute;NICA SALIDA: BLACKHOLING Y LEVANTAMIENTO A OSCURAS
              </span>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 12.5px; color: #cbd5e1; line-height: 1.4;">
              Para revivir a los nodos, los ingenieros tuvieron que <strong>desconectar a medio planeta de golpe</strong> tirando las rutas BGP al vac&iacute;o (Blackholing). Solo con el tr&aacute;fico a cero pudieron iniciar los procesos, calentar la memoria cach&eacute; e ir abriendo compuertas paulatina y manualmente.
            </p>
          </div>

        </div>

        <div style="margin-top: 14px; background: rgba(236, 72, 153, 0.08); border-left: 4px solid #ec4899; border-radius: 8px; padding: 10px 16px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #fff;">
            <strong>ENCENDER UNA CERILLA EN MEDIO DE UN HURAC&Aacute;N:</strong> Intentar levantar una nube ca&iacute;da con millones de clientes golpeando la puerta es el reto m&aacute;s dif&iacute;cil de la computaci&oacute;n moderna.
          </div>
        </div>
      </article>

      <!-- ========================================== -->
      <!-- ACTO 5: AUTOPSIA FORENSE & DEBATE -->
      <!-- ========================================== -->
      <article id="card-5" class="scene-card" style="border-color: #38bdf8;">
        <div class="card-topbar">
          <div>
            <div class="card-act-num" style="color: #38bdf8;">ACTO 05 &bull; EL VEREDICTO DE REDMOND</div>
            <h2 class="card-title">LA FACTURA DE LA PARADOJA DE NADELLA</h2>
          </div>
          <div class="card-tag" style="background: rgba(56, 189, 248, 0.15); border-color: #38bdf8; color: #38bdf8;">
            VEREDICTO FORENSE
          </div>
        </div>

        <!-- BALANCE FINAL DE LA CRISIS -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 14px;">
          <div style="background: rgba(15, 23, 42, 0.9); border: 1.5px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #94a3b8;">DOWNTIME TOTAL</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 900; color: #ef4444; margin-top: 4px;">18h 42m</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.9); border: 1.5px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #94a3b8;">PA&Iacute;SES PARALIZADOS</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 900; color: #f59e0b; margin-top: 4px;">74</div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.9); border: 1.5px solid rgba(56, 189, 248, 0.4); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #94a3b8;">PENALIZACI&Oacute;N SLA</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 900; color: #38bdf8; margin-top: 4px;">+$10,000M</div>
          </div>
        </div>

        <!-- CAJA DE DEBATE COMUNITARIO -->
        <div style="flex: 1; background: rgba(15, 23, 42, 0.95); border: 2px solid #38bdf8; border-radius: 18px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 0 30px rgba(56, 189, 248, 0.2);">
          
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-family: 'Montserrat', sans-serif; font-size: 18px; font-weight: 900; color: #fff;">
                🗳️ DEBATE DE INGENIER&Iacute;A: ¿QUI&Eacute;N TIENE LA CULPA?
              </span>
              <span style="background: rgba(56, 189, 248, 0.2); border: 1px solid #38bdf8; color: #38bdf8; font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 3px 10px; border-radius: 999px; font-weight: bold;">
                ¡COMENTA AQU&Iacute;!
              </span>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #cbd5e1; line-height: 1.35;">
              ¿Deber&iacute;an los gobiernos multar el monocultivo de nube o fue un accidente inevitable en sistemas hipercomplejos?
            </p>
          </div>

          <!-- COMPARATIVA TÉCNICA VISUAL -->
          <div style="background: #030614; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px 16px;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94a3b8; margin-bottom: 8px;">
              LA LECCI&Oacute;N ARQUITECT&Oacute;NICA DEFINITIVA:
            </div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #fff; line-height: 1.4;">
              Puedes invertir <strong>$50,000 millones en silicio de inteligencia artificial</strong>, pero cuando una reconfiguraci&oacute;n de red entra en cascada, ning&uacute;n LLM sabe qu&eacute; router reiniciar. La intuici&oacute;n humana veterana es insustituible.
            </div>
          </div>

          <!-- OPCIÓN 1 -->
          <div style="background: rgba(3, 6, 17, 0.85); border: 1.5px solid #0284c7; border-radius: 12px; padding: 12px 16px; display: flex; align-items: center; gap: 14px;">
            <div style="width: 32px; height: 32px; background: #0284c7; color: #fff; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 900;">
              1
            </div>
            <div style="flex: 1;">
              <div style="font-family: 'Montserrat', sans-serif; font-size: 13.5px; font-weight: 800; color: #fff;">
                PROHIBIR EL MONOCULTIVO DE NUBE
              </div>
              <div style="font-family: 'Space Grotesk', sans-serif; font-size: 11.5px; color: #94a3b8;">
                Ning&uacute;n banco ni hospital debe atarse a un solo proveedor que pueda apagarse 20 horas.
              </div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: #38bdf8; font-weight: bold;">
              #MultiCloud
            </div>
          </div>

          <!-- OPCIÓN 2 -->
          <div style="background: rgba(3, 6, 17, 0.85); border: 1.5px solid #10b981; border-radius: 12px; padding: 12px 16px; display: flex; align-items: center; gap: 14px;">
            <div style="width: 32px; height: 32px; background: #10b981; color: #000; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 900;">
              2
            </div>
            <div style="flex: 1;">
              <div style="font-family: 'Montserrat', sans-serif; font-size: 13.5px; font-weight: 800; color: #fff;">
                DESPIDOS MASIVOS COMO FACTOR CLAVE
              </div>
              <div style="font-family: 'Space Grotesk', sans-serif; font-size: 11.5px; color: #94a3b8;">
                Cambiar 22,500 ingenieros por modelos de lenguaje dej&oacute; a la infraestructura sin defensas.
              </div>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: #34d399; font-weight: bold;">
              #HumanInTheLoop
            </div>
          </div>

          <div style="background: rgba(56, 189, 248, 0.08); border-radius: 8px; padding: 8px; text-align: center;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; color: #94a3b8;">
              🚗 Esc&uacute;chanos en <strong>Spotify: sIA Podcast</strong> &bull; Art&iacute;culos completos en <strong>escucha-sia.github.io</strong>
            </span>
          </div>

        </div>
      </article>

    </main>

    <!-- SUBTITLES BOX -->
    <section class="subtitles-container">
      {"".join(sub_items)}
    </section>

    <!-- BOTTOM TELEMETRY -->
    <footer class="bottom-telemetry">
      <div>🚗 ¿En el coche? Esc&uacute;chanos en Spotify: sIA Podcast</div>
      <div>TikTok: @escucha_sia &bull; escucha-sia.github.io</div>
    </footer>
  </div>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Escena compilada exitosamente en {OUT_HTML}")
