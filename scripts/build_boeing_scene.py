import json
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Load timestamps
with open("scratch/boeing_timestamps.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

TOTAL_DUR = 270.65

ACTS = [
    {"num": 1, "start": 0.0, "end": 57.5, "title": "EL PECADO GEOMÉTRICO", "tag": "CFM LEAP-1B & AERODINÁMICA"},
    {"num": 2, "start": 57.5, "end": 117.7, "title": "UN SOLO SENSOR", "tag": "FALLO DE VELETA AOA"},
    {"num": 3, "start": 117.7, "end": 169.0, "title": "EL TORNILLO SINFÍN", "tag": "JACKSCREW & ESTABILIZADOR"},
    {"num": 4, "start": 169.0, "end": 217.4, "title": "LA BATALLA EN CABINA", "tag": "EL LOOP DE 5 SEGUNDOS"},
    {"num": 5, "start": 217.4, "end": 270.65, "title": "MANUAL CENSURADO & VOTACIÓN", "tag": "ENCUESTA CAPÍTULO #12"}
]

# Generate card keyframe CSS
cards_css = []
for act in ACTS:
    s_pct = (act["start"] / TOTAL_DUR) * 100
    e_pct = (act["end"] / TOTAL_DUR) * 100
    num = act["num"]
    
    if num == 1:
        css = f"""
        @keyframes scene1Anim {{
          0% {{ opacity: 1; visibility: visible; transform: scale(1); z-index: 5; pointer-events: auto; }}
          {e_pct - 0.1:.3f}% {{ opacity: 1; visibility: visible; transform: scale(1); z-index: 5; pointer-events: auto; }}
          {e_pct:.3f}%, 100% {{ opacity: 0; visibility: hidden; transform: scale(0.96); z-index: 0; pointer-events: none; }}
        }}"""
    elif num == 5:
        css = f"""
        @keyframes scene5Anim {{
          0%, {s_pct - 0.1:.3f}% {{ opacity: 0; visibility: hidden; transform: scale(0.96); z-index: 0; pointer-events: none; }}
          {s_pct:.3f}%, 100% {{ opacity: 1; visibility: visible; transform: scale(1); z-index: 5; pointer-events: auto; }}
        }}"""
    else:
        css = f"""
        @keyframes scene{num}Anim {{
          0%, {s_pct - 0.1:.3f}% {{ opacity: 0; visibility: hidden; transform: scale(0.96); z-index: 0; pointer-events: none; }}
          {s_pct:.3f}%, {e_pct - 0.1:.3f}% {{ opacity: 1; visibility: visible; transform: scale(1); z-index: 5; pointer-events: auto; }}
          {e_pct:.3f}%, 100% {{ opacity: 0; visibility: hidden; transform: scale(0.96); z-index: 0; pointer-events: none; }}
        }}"""
    cards_css.append(css)

# Generate chapter pills animation
chap_css = []
colors = ["#38bdf8", "#f43f5e", "#a855f7", "#eab308", "#10b981"]
for idx, act in enumerate(ACTS):
    num = act["num"]
    col = colors[idx]
    s_pct = (act["start"] / TOTAL_DUR) * 100
    e_pct = (act["end"] / TOTAL_DUR) * 100
    if num == 1:
        css = f"""
        @keyframes c1Anim {{
          0%, {e_pct - 0.1:.3f}% {{ background: {col}; color: #000; border-color: #fff; box-shadow: 0 0 16px {col}; transform: scale(1.05); }}
          {e_pct:.3f}%, 100% {{ background: rgba(255,255,255,0.06); color: #94a3b8; border-color: rgba(255,255,255,0.12); transform: scale(1); }}
        }}"""
    elif num == 5:
        css = f"""
        @keyframes c5Anim {{
          0%, {s_pct - 0.1:.3f}% {{ background: rgba(255,255,255,0.06); color: #94a3b8; border-color: rgba(255,255,255,0.12); transform: scale(1); }}
          {s_pct:.3f}%, 100% {{ background: {col}; color: #000; border-color: #fff; box-shadow: 0 0 20px {col}; transform: scale(1.08); }}
        }}"""
    else:
        css = f"""
        @keyframes c{num}Anim {{
          0%, {s_pct - 0.1:.3f}% {{ background: rgba(255,255,255,0.06); color: #94a3b8; border-color: rgba(255,255,255,0.12); transform: scale(1); }}
          {s_pct:.3f}%, {e_pct - 0.1:.3f}% {{ background: {col}; color: #000; border-color: #fff; box-shadow: 0 0 16px {col}; transform: scale(1.05); }}
          {e_pct:.3f}%, 100% {{ background: rgba(255,255,255,0.06); color: #94a3b8; border-color: rgba(255,255,255,0.12); transform: scale(1); }}
        }}"""
    chap_css.append(css)

# Generate subtitle pill items and CSS
sub_items_html = []
sub_css = []
for idx, seg in enumerate(segments):
    s_pct = (seg["start"] / TOTAL_DUR) * 100
    e_pct = (seg["end"] / TOTAL_DUR) * 100
    is_jorge = seg["voice"] == "Jorge"
    badge_col = "#38bdf8" if is_jorge else "#ec4899"
    badge_text = "JORGE" if is_jorge else "DALIA"
    
    sub_items_html.append(f"""
      <div class="sub-item" id="sub-{idx}">
        <div class="speaker-tag" style="background:{badge_col}; color:#000;">🎙️ {badge_text}</div>
        <div class="sub-text">{seg["text"]}</div>
      </div>""")
      
    sub_css.append(f"""
      #sub-{idx} {{
        animation: subAnim_{idx} {TOTAL_DUR}s linear infinite;
      }}
      @keyframes subAnim_{idx} {{
        0%, {max(0, s_pct - 0.05):.3f}% {{ opacity: 0; transform: translateY(12px) scale(0.97); pointer-events: none; display: none; }}
        {s_pct:.3f}%, {e_pct - 0.05:.3f}% {{ opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; display: flex; }}
        {e_pct:.3f}%, 100% {{ opacity: 0; transform: translateY(-8px) scale(0.97); pointer-events: none; display: none; }}
      }}""")

# Build final HTML
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>sIA Crónicas #11: Boeing 737 MAX y el MCAS</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@600;700;800&family=JetBrains+Mono:wght@700;800&display=swap');

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: 1080px;
      height: 1920px;
      background: #040813;
      color: #fff;
      font-family: 'Space Grotesk', sans-serif;
      overflow: hidden;
      position: relative;
    }}

    /* Fondo dinámico estilo Blueprint Aeronáutico con Scanlines */
    .blueprint-grid {{
      position: absolute;
      inset: 0;
      background-image: 
        radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.06) 0%, transparent 80%),
        linear-gradient(rgba(14, 165, 233, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(14, 165, 233, 0.08) 1px, transparent 1px),
        linear-gradient(rgba(14, 165, 233, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(14, 165, 233, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 80px 80px, 80px 80px, 16px 16px, 16px 16px;
      z-index: 1;
    }}

    .scanlines {{
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.15) 2px, transparent 2px, transparent 4px);
      pointer-events: none;
      z-index: 2;
    }}

    .watermark {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-25deg);
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 110px;
      color: rgba(255, 255, 255, 0.015);
      letter-spacing: 16px;
      white-space: nowrap;
      pointer-events: none;
      z-index: 1;
    }}

    /* HEADER TÁCTICO (130px) */
    .tactical-header {{
      position: absolute;
      top: 24px;
      left: 40px;
      right: 40px;
      height: 110px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      z-index: 10;
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .brand-badge {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(2, 132, 199, 0.2);
      border: 1.5px solid #0284c7;
      padding: 8px 18px;
      border-radius: 999px;
      box-shadow: 0 0 20px rgba(2, 132, 199, 0.4);
    }}

    .brand-dot {{
      width: 14px;
      height: 14px;
      background: #38bdf8;
      border-radius: 50%;
      box-shadow: 0 0 12px #38bdf8;
      animation: pulseDot 1s infinite alternate;
    }}
    @keyframes pulseDot {{ 0% {{ opacity: 0.5; transform: scale(0.8); }} 100% {{ opacity: 1; transform: scale(1.2); }} }}

    .brand-name {{
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 22px;
      letter-spacing: 2px;
      color: #fff;
    }}

    .channel-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 17px;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .chapter-pills {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 10px;
      margin-top: 8px;
    }}

    .chap-pill {{
      text-align: center;
      padding: 8px 6px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.5px;
      border: 1.5px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.06);
      color: #94a3b8;
      transition: all 0.2s;
    }}

    /* CSS FOR CHAPTER PILLS */
    {chap_css[0]}
    {chap_css[1]}
    {chap_css[2]}
    {chap_css[3]}
    {chap_css[4]}

    #pill-1 {{ animation: c1Anim {TOTAL_DUR}s linear infinite; }}
    #pill-2 {{ animation: c2Anim {TOTAL_DUR}s linear infinite; }}
    #pill-3 {{ animation: c3Anim {TOTAL_DUR}s linear infinite; }}
    #pill-4 {{ animation: c4Anim {TOTAL_DUR}s linear infinite; }}
    #pill-5 {{ animation: c5Anim {TOTAL_DUR}s linear infinite; }}

    /* PROGRESS BAR */
    .progress-bar-container {{
      position: absolute;
      top: 146px;
      left: 40px;
      right: 40px;
      height: 5px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 999px;
      overflow: hidden;
      z-index: 10;
    }}
    .progress-bar {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #38bdf8, #f43f5e, #a855f7, #eab308, #10b981);
      animation: progressAnim {TOTAL_DUR}s linear infinite;
    }}
    @keyframes progressAnim {{
      0% {{ width: 0%; }}
      100% {{ width: 100%; }}
    }}

    /* ====================================================================
       CANVAS TÉCNICO VIVO CENTRAL (75% DE LA PANTALLA: y=160px a y=1560px)
       CERO AVATARES: 100% ESPACIO AEROESPACIAL CON MOVIMIENTO CONTINUO
       ==================================================================== */
    .main-stage {{
      position: absolute;
      top: 160px;
      left: 40px;
      width: 1000px;
      height: 1390px;
      z-index: 5;
    }}

    .scene-card {{
      position: absolute;
      inset: 0;
      border-radius: 24px;
      background: #040817;
      border: 1.5px solid rgba(56, 189, 248, 0.3);
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), inset 0 0 40px rgba(14, 165, 233, 0.08);
      padding: 32px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    /* CSS FOR SCENE CARDS TRANSITIONS */
    {cards_css[0]}
    {cards_css[1]}
    {cards_css[2]}
    {cards_css[3]}
    {cards_css[4]}

    #card-1 {{ animation: scene1Anim {TOTAL_DUR}s linear infinite; }}
    #card-2 {{ animation: scene2Anim {TOTAL_DUR}s linear infinite; }}
    #card-3 {{ animation: scene3Anim {TOTAL_DUR}s linear infinite; }}
    #card-4 {{ animation: scene4Anim {TOTAL_DUR}s linear infinite; }}
    #card-5 {{ animation: scene5Anim {TOTAL_DUR}s linear infinite; }}

    .card-topbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .card-title-group {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .card-act-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      color: #38bdf8;
      font-weight: 800;
      letter-spacing: 2px;
    }}

    .card-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 28px;
      font-weight: 900;
      letter-spacing: 0.5px;
      color: #fff;
    }}

    .card-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      font-weight: 800;
    }}

    .canvas-viewport {{
      flex: 1;
      width: 100%;
      position: relative;
      background: #020610;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    /* ====================================================================
       ANIMACIONES PROCEDURALES EN MOVIMIENTO CONTINUO
       ==================================================================== */
    @keyframes turbineSpin {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}

    @keyframes airflowLoop {{
      0% {{ stroke-dashoffset: 400; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    @keyframes pulseLiftVector {{
      0% {{ transform: translateY(0) scaleY(1); opacity: 0.8; }}
      50% {{ transform: translateY(-12px) scaleY(1.15); opacity: 1; }}
      100% {{ transform: translateY(0) scaleY(1); opacity: 0.8; }}
    }}

    @keyframes pitchTorqueArc {{
      0% {{ stroke-dashoffset: 200; opacity: 0.4; }}
      50% {{ stroke-dashoffset: 50; opacity: 1; }}
      100% {{ stroke-dashoffset: 200; opacity: 0.4; }}
    }}

    @keyframes vaneOscillate {{
      0% {{ transform: rotate(-4deg); }}
      30% {{ transform: rotate(6deg); }}
      60% {{ transform: rotate(-2deg); }}
      85% {{ transform: rotate(32deg); }} /* JAM STALL POSITION */
      100% {{ transform: rotate(32deg); }}
    }}

    @keyframes hudWaveScan {{
      0% {{ stroke-dashoffset: 600; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    @keyframes alertFlashRed {{
      0%, 100% {{ opacity: 0.2; transform: scale(0.98); }}
      50% {{ opacity: 1; transform: scale(1.02); }}
    }}

    @keyframes jackscrewTurn {{
      0% {{ transform: translateY(0); }}
      100% {{ transform: translateY(30px); }}
    }}

    @keyframes stabDeflect {{
      0% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(-9deg); }} /* NOSE DOWN TRIM */
      100% {{ transform: rotate(-14deg); }}
    }}

    @keyframes yokeShake {{
      0%, 100% {{ transform: translate(0, 0); }}
      20% {{ transform: translate(-3px, 4px); }}
      40% {{ transform: translate(3px, -3px); }}
      60% {{ transform: translate(-2px, -4px); }}
      80% {{ transform: translate(4px, 2px); }}
    }}

    @keyframes mcasPulseRing {{
      0% {{ transform: scale(0.8); opacity: 1; }}
      80% {{ transform: scale(1.4); opacity: 0; }}
      100% {{ transform: scale(0.8); opacity: 0; }}
    }}

    @keyframes altimeterScroll {{
      0% {{ transform: translateY(0); }}
      100% {{ transform: translateY(-380px); }}
    }}

    /* ====================================================================
       SUBTÍTULOS KINETIC PUNCH-PILL (y=1570px a y=1810px)
       ==================================================================== */
    .subtitles-container {{
      position: absolute;
      top: 1570px;
      left: 40px;
      right: 40px;
      height: 230px;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
    }}

    .sub-item {{
      position: absolute;
      width: 100%;
      height: 100%;
      background: rgba(6, 11, 24, 0.92);
      border: 2px solid rgba(255, 255, 255, 0.15);
      border-radius: 24px;
      padding: 24px 32px;
      box-shadow: 0 16px 50px rgba(0, 0, 0, 0.9);
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 12px;
    }}

    .speaker-tag {{
      align-self: flex-start;
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: 16px;
      padding: 6px 16px;
      border-radius: 999px;
      letter-spacing: 1px;
    }}

    .sub-text {{
      font-size: 26px;
      font-weight: 700;
      line-height: 1.35;
      color: #fff;
      letter-spacing: -0.3px;
    }}

    {chr(10).join(sub_css)}

    /* FOOTER OMNICANAL (y=1820px a 1900px) */
    .omnichannel-footer {{
      position: absolute;
      bottom: 24px;
      left: 40px;
      right: 40px;
      height: 70px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 10;
    }}

    .footer-left {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 17px;
      font-weight: 700;
      color: #38bdf8;
    }}

    .footer-right {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 16px;
      font-weight: 800;
      color: #94a3b8;
    }}
    .footer-pill {{
      background: rgba(255, 255, 255, 0.08);
      padding: 6px 14px;
      border-radius: 8px;
      color: #fff;
    }}
  </style>
</head>
<body>
  <div id="scene-root" data-composition-id="boeing_scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
  <div class="blueprint-grid"></div>
  <div class="scanlines"></div>
  <div class="watermark">sIA CRÓNICAS #11 • BOEING 737 MAX</div>

  <!-- HEADER TÁCTICO -->
  <div class="tactical-header">
    <div class="header-top">
      <div class="brand-badge">
        <div class="brand-dot"></div>
        <div class="brand-name">sIA CRÓNICAS #11</div>
      </div>
      <div class="channel-tag">@escucha_sia • SPOTIFY & TIKTOK</div>
    </div>
    <div class="chapter-pills">
      <div class="chap-pill" id="pill-1">1. CFM LEAP-1B</div>
      <div class="chap-pill" id="pill-2">2. SENSOR AOA</div>
      <div class="chap-pill" id="pill-3">3. JACKSCREW</div>
      <div class="chap-pill" id="pill-4">4. LOOP 5s</div>
      <div class="chap-pill" id="pill-5">5. VOTACIÓN</div>
    </div>
  </div>

  <div class="progress-bar-container">
    <div class="progress-bar"></div>
  </div>

  <!-- STAGE PRINCIPAL (CERO AVATARES: 100% ESPACIO AEROESPACIAL) -->
  <div class="main-stage">

    <!-- ACTO 1: CFM LEAP-1B Y LA ALTERACIÓN AERODINÁMICA -->
    <div class="scene-card" id="card-1">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 01 • GEOMETRÍA DEL MOTOR</div>
          <div class="card-title">EL PECADO GEOMÉTRICO: CFM LEAP-1B</div>
        </div>
        <div class="card-tag">AERODINÁMICA INESTABLE</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#020713;">
          <defs>
            <linearGradient id="streamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.1"/>
              <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.9"/>
              <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.2"/>
            </linearGradient>
            <filter id="glowAir">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          <!-- TÍTULO SUPERIOR SVG -->
          <text x="470" y="70" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">COMPARATIVA ESTRUCTURAL: 737 CLÁSICO VS 737 MAX</text>

          <!-- SILUETA FUSELAJE 737 (BLUEPRINT) -->
          <path d="M 120 480 Q 280 430 520 430 L 780 430 Q 860 430 890 320 L 890 510 L 780 500 L 260 500 Z" fill="rgba(14, 165, 233, 0.08)" stroke="#38bdf8" stroke-width="2.5" />
          <!-- Cabina y Ventanas -->
          <path d="M 160 460 Q 220 445 260 445" stroke="#38bdf8" stroke-width="2" fill="none" />
          <circle cx="180" cy="460" r="3" fill="#38bdf8" />
          <circle cx="205" cy="455" r="3" fill="#38bdf8" />
          <circle cx="230" cy="450" r="3" fill="#38bdf8" />

          <!-- ALA PRINCIPAL -->
          <path d="M 400 490 L 640 590 L 620 620 L 370 500 Z" fill="rgba(14, 165, 233, 0.15)" stroke="#0284c7" stroke-width="2" />

          <!-- MOTOR 737 CLÁSICO (LÍNEA PUNTEADA ORIGINAL BAJO EL ALA) -->
          <g opacity="0.4">
            <rect x="420" y="550" width="180" height="90" rx="45" fill="none" stroke="#94a3b8" stroke-dasharray="6 6" stroke-width="2" />
            <text x="510" y="600" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">ORIGINAL (1967)</text>
          </g>

          <!-- MOTOR GIGANTE CFM LEAP-1B (DESPLAZADO AL FRENTE Y ARRIBA) -->
          <g transform="translate(0, 0)">
            <!-- Soporte Pylon Adelantado -->
            <path d="M 360 470 L 310 520 L 440 520 L 410 470 Z" fill="rgba(56, 189, 248, 0.25)" stroke="#38bdf8" stroke-width="2" />
            <!-- Góndola Motor Enorme -->
            <rect x="250" y="500" width="260" height="150" rx="75" fill="rgba(2, 6, 23, 0.9)" stroke="#f43f5e" stroke-width="3.5" filter="url(#glowAir)" />
            <!-- Diámetro +15% Label -->
            <line x1="230" y1="500" x2="230" y2="650" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4 4"/>
            <text x="210" y="580" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="14" font-weight="bold" transform="rotate(-90 210 580)">DIÁMETRO +15%</text>

            <!-- TURBINA GIRATORIA CONTINUA -->
            <g transform="translate(295, 575)">
              <circle cx="0" cy="0" r="55" fill="#090d1a" stroke="#38bdf8" stroke-width="2" />
              <g style="animation: turbineSpin 0.35s linear infinite; transform-origin: 0px 0px;">
                <line x1="-50" y1="0" x2="50" y2="0" stroke="#38bdf8" stroke-width="3" />
                <line x1="0" y1="-50" x2="0" y2="50" stroke="#38bdf8" stroke-width="3" />
                <line x1="-35" y1="-35" x2="35" y2="35" stroke="#38bdf8" stroke-width="3" />
                <line x1="-35" y1="35" x2="35" y2="-35" stroke="#38bdf8" stroke-width="3" />
                <circle cx="0" cy="0" r="14" fill="#f43f5e" />
              </g>
            </g>
          </g>

          <!-- LÍNEAS DE FLUJO AERODINÁMICO EN MOVIMIENTO PERPETUO -->
          <g filter="url(#glowAir)">
            <path d="M 60 520 Q 220 480 380 460 T 700 480 T 880 490" fill="none" stroke="url(#streamGrad)" stroke-width="3" stroke-dasharray="50 30" style="animation: airflowLoop 1.2s linear infinite;" />
            <path d="M 60 550 Q 200 520 250 510 T 520 530 T 880 520" fill="none" stroke="url(#streamGrad)" stroke-width="3" stroke-dasharray="60 40" style="animation: airflowLoop 1.0s linear infinite;" />
            <path d="M 60 620 Q 180 630 250 640 T 520 660 T 880 620" fill="none" stroke="url(#streamGrad)" stroke-width="2.5" stroke-dasharray="40 25" style="animation: airflowLoop 0.9s linear infinite;" />
            <path d="M 60 460 Q 220 420 480 410 T 880 420" fill="none" stroke="url(#streamGrad)" stroke-width="2" stroke-dasharray="45 35" style="animation: airflowLoop 1.4s linear infinite;" />
          </g>

          <!-- VECTOR DE SUSTENTACIÓN ADICIONAL PARÁSITA (PULSANTE) -->
          <g style="animation: pulseLiftVector 1.8s ease-in-out infinite;">
            <line x1="380" y1="500" x2="380" y2="330" stroke="#f43f5e" stroke-width="5" marker-end="url(#arrow)" />
            <polygon points="380,310 368,340 392,340" fill="#f43f5e" />
            <rect x="300" y="270" width="160" height="40" rx="8" fill="#f43f5e" />
            <text x="380" y="296" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="15" font-weight="900">FUERZA LIFT +F_L</text>
          </g>

          <!-- ARCO DE TORQUE PITCH-UP DESCONTROLADO -->
          <path d="M 180 390 A 80 80 0 0 1 140 490" fill="none" stroke="#f59e0b" stroke-width="4" stroke-dasharray="10 6" style="animation: pitchTorqueArc 1.5s linear infinite;" />
          <polygon points="175,375 190,395 168,400" fill="#f59e0b" />
          <text x="90" y="360" fill="#f59e0b" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">MOMENTO PITCH-UP ⬆️</text>

          <!-- PANEL TÉCNICO HUD INFERIOR -->
          <g transform="translate(60, 830)">
            <rect width="820" height="280" rx="16" fill="rgba(15, 23, 42, 0.85)" stroke="#38bdf8" stroke-width="1.5" />
            
            <text x="40" y="45" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">TELEMETRÍA AERODINÁMICA BOEING 737 MAX</text>
            <line x1="40" y1="60" x2="780" y2="60" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <text x="40" y="105" fill="#94a3b8" font-family="'Space Grotesk'" font-size="18">Posicionamiento Góndola:</text>
            <text x="450" y="105" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">+48 cm Adelantado / +20 cm Elevado</text>

            <text x="40" y="150" fill="#94a3b8" font-family="'Space Grotesk'" font-size="18">Efecto en Ángulo de Ataque:</text>
            <text x="450" y="150" fill="#f59e0b" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">Empuje Parásito hacia arriba (Pitch-Up)</text>

            <text x="40" y="195" fill="#94a3b8" font-family="'Space Grotesk'" font-size="18">Riesgo Crítico Certificación:</text>
            <text x="450" y="195" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">Pérdida de Sustentación (Aerodynamic Stall)</text>

            <rect x="40" y="220" width="740" height="40" rx="8" fill="rgba(244, 63, 94, 0.2)" stroke="#f43f5e" stroke-width="1.5"/>
            <text x="410" y="246" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="15" font-weight="900">SOLUCIÓN DE BOEING: PARCHE DE SOFTWARE SILENCIOSO (MCAS)</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 2: EL FALLO DEL SENSOR ÚNICO DE ÁNGULO DE ATAQUE -->
    <div class="scene-card" id="card-2">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 02 • ARQUITECTURA DE SENSORES</div>
          <div class="card-title">UN SOLO SENSOR: VELETA AOA DEFECTUOSA</div>
        </div>
        <div class="card-tag" style="border-color:#f43f5e; color:#f43f5e;">CERO REDUNDANCIA</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#020713;">
          <!-- TÍTULO SUPERIOR SVG -->
          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">CIRCUITO DE ADQUISICIÓN DE DATOS: AOA A LA FCC</text>

          <!-- SECCIÓN PROA DEL AVIÓN -->
          <path d="M 80 600 Q 180 320 540 320 L 540 600 Z" fill="rgba(14, 165, 233, 0.08)" stroke="#38bdf8" stroke-width="2.5" />
          
          <!-- VELETA METÁLICA DE ÁNGULO DE ATAQUE (ROTANDO / OSCILANDO) -->
          <g transform="translate(280, 440)">
            <circle cx="0" cy="0" r="42" fill="#0f172a" stroke="#38bdf8" stroke-width="3" />
            <circle cx="0" cy="0" r="12" fill="#f43f5e" />
            <!-- Vane Vane Vane (animada oscilando y clavándose en 32°) -->
            <g style="animation: vaneOscillate 3s ease-in-out infinite; transform-origin: 0px 0px;">
              <polygon points="0,-8 95,0 0,8" fill="#f59e0b" stroke="#fff" stroke-width="2" />
              <line x1="0" y1="0" x2="110" y2="0" stroke="#f43f5e" stroke-width="2" stroke-dasharray="3 3"/>
              <text x="120" y="5" fill="#f59e0b" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">AOA: +32.1°</text>
            </g>
          </g>

          <text x="280" y="520" text-anchor="middle" fill="#38bdf8" font-family="'Montserrat'" font-size="15" font-weight="900">VELETA IZQUIERDA (AOA)</text>

          <!-- CABLEADO DIGITAL HACIA LA FCC -->
          <path d="M 320 440 L 540 440 L 680 440" fill="none" stroke="#f43f5e" stroke-width="4" stroke-dasharray="12 8" style="animation: airflowLoop 1s linear infinite;" />

          <!-- BLOQUE FCC (FLIGHT CONTROL COMPUTER) -->
          <g transform="translate(680, 360)">
            <rect width="200" height="160" rx="14" fill="#090d1a" stroke="#f43f5e" stroke-width="3" />
            <text x="100" y="45" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="17" font-weight="900">BOEING FCC</text>
            <text x="100" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">FLIGHT COMPUTER</text>
            <rect x="25" y="100" width="150" height="35" rx="6" fill="#f43f5e" />
            <text x="100" y="123" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">MCAS TRIGGER: ON</text>
          </g>

          <!-- SENSOR DERECHO DESCONECTADO (PUNTO CRÍTICO DE FALLA) -->
          <g transform="translate(280, 680)" opacity="0.45">
            <circle cx="0" cy="0" r="35" fill="#0f172a" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 4" />
            <polygon points="0,-6 70,0 0,6" fill="#94a3b8" />
            <text x="110" y="6" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="14">AOA REAL: 4.2°</text>
            <text x="0" y="55" text-anchor="middle" fill="#94a3b8" font-family="'Montserrat'" font-size="13">VELETA DERECHA</text>
          </g>

          <!-- LÍNEA CORTADA CON TACHA -->
          <path d="M 320 680 L 520 680 L 600 530" fill="none" stroke="#64748b" stroke-width="2.5" stroke-dasharray="6 6" />
          <g transform="translate(480, 680)">
            <circle cx="0" cy="0" r="16" fill="#f43f5e" />
            <line x1="-8" y1="-8" x2="8" y2="8" stroke="#fff" stroke-width="3"/>
            <line x1="8" y1="-8" x2="-8" y2="8" stroke="#fff" stroke-width="3"/>
          </g>
          <text x="510" y="660" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">IGNORADO POR EL CÓDIGO</text>

          <!-- MONITOR DE FORMA DE ONDA / OSCILOSCOPIO DINÁMICO -->
          <g transform="translate(60, 780)">
            <rect width="820" height="340" rx="18" fill="rgba(2, 6, 23, 0.95)" stroke="#38bdf8" stroke-width="2" />
            <rect x="20" y="20" width="780" height="50" rx="10" fill="rgba(244, 63, 94, 0.2)" stroke="#f43f5e" stroke-width="1.5" style="animation: alertFlashRed 1s infinite;" />
            <text x="410" y="52" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="18" font-weight="900">⚠️ ADVERTENCIA: LECTURA DE STALL FALSA ACTIVADA</text>

            <!-- Grid de osciloscopio -->
            <g opacity="0.2" stroke="#38bdf8" stroke-width="1">
              <line x1="40" y1="140" x2="780" y2="140"/>
              <line x1="40" y1="200" x2="780" y2="200"/>
              <line x1="40" y1="260" x2="780" y2="260"/>
              <line x1="200" y1="100" x2="200" y2="300"/>
              <line x1="400" y1="100" x2="400" y2="300"/>
              <line x1="600" y1="100" x2="600" y2="300"/>
            </g>

            <!-- Onda Real (verde suave) -->
            <path d="M 40 200 Q 120 190 200 200 T 360 200 T 520 200 T 680 200 T 780 200" fill="none" stroke="#10b981" stroke-width="3" />
            <text x="50" y="185" fill="#10b981" font-family="'JetBrains Mono'" font-size="13">ÁNGULO REAL (VUELO RECTO: 4.2°)</text>

            <!-- Onda Sensor Roto (rojo en pico extremo animado) -->
            <path d="M 40 200 Q 120 130 200 110 T 360 110 T 520 110 T 680 110 T 780 110" fill="none" stroke="#f43f5e" stroke-width="4" stroke-dasharray="20 10" style="animation: hudWaveScan 1.5s linear infinite;" />
            <text x="500" y="130" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">ERROR: AOA REPORTA +32° (CRITICAL STALL)</text>

            <text x="40" y="315" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Decisión del Sistema: Activar compensador de morro abajo sin consultar la segunda veleta.</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 3: EL TORNILLO SINFÍN (JACKSCREW) Y LA ANULACIÓN MECÁNICA -->
    <div class="scene-card" id="card-3">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 03 • CINEMÁTICA DEL TRIM</div>
          <div class="card-title">EL TORNILLO SINFÍN: CONTROL TOTAL DE COLA</div>
        </div>
        <div class="card-tag" style="border-color:#a855f7; color:#a855f7;">AUTORIDAD 2.5°/CICLO</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#020713;">
          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">MECANISMO DE CONTROL: MOTOR ELÉCTRICO Y ESTABILIZADOR</text>

          <!-- SECCIÓN DE COLA (EMPENNAGE CUTAWAY) -->
          <path d="M 120 720 L 320 220 L 460 220 L 520 720 Z" fill="rgba(168, 85, 247, 0.08)" stroke="#a855f7" stroke-width="2.5" />
          <text x="270" y="270" fill="#a855f7" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">ESTABILIZADOR VERTICAL</text>

          <!-- MOTOR ELÉCTRICO DEL TRIM (ROTACIÓN CONTINUA) -->
          <g transform="translate(620, 480)">
            <rect width="180" height="110" rx="12" fill="#1e1b4b" stroke="#a855f7" stroke-width="3" />
            <text x="90" y="35" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="15" font-weight="bold">MOTOR ELÉCTRICO</text>
            <text x="90" y="60" text-anchor="middle" fill="#a855f7" font-family="'JetBrains Mono'" font-size="12">STAB TRIM ACTUATOR</text>

            <!-- Engranaje animado -->
            <g transform="translate(90, 85)" style="animation: turbineSpin 1s linear infinite;">
              <circle cx="0" cy="0" r="16" fill="none" stroke="#38bdf8" stroke-width="4" stroke-dasharray="6 4"/>
              <circle cx="0" cy="0" r="5" fill="#38bdf8"/>
            </g>
          </g>

          <!-- EL TORNILLO SINFÍN (JACKSCREW MECÁNICO MOVIÉNDOSE) -->
          <g transform="translate(480, 360)">
            <rect x="0" y="0" width="36" height="360" rx="6" fill="#0f172a" stroke="#fff" stroke-width="2" />
            <!-- Estrías helicoidales en movimiento vertical continuo -->
            <g style="animation: jackscrewTurn 0.8s linear infinite;">
              <line x1="0" y1="30" x2="36" y2="45" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="60" x2="36" y2="75" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="90" x2="36" y2="105" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="120" x2="36" y2="135" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="150" x2="36" y2="165" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="180" x2="36" y2="195" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="210" x2="36" y2="225" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="240" x2="36" y2="255" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="270" x2="36" y2="285" stroke="#a855f7" stroke-width="3"/>
              <line x1="0" y1="300" x2="36" y2="315" stroke="#a855f7" stroke-width="3"/>
            </g>
            <text x="-15" y="180" fill="#fff" font-family="'JetBrains Mono'" font-size="14" font-weight="bold" transform="rotate(-90 -15 180)">JACKSCREW ROTATIVO</text>
          </g>

          <!-- ESTABILIZADOR HORIZONTAL DEFLECTÁNDOSE HACIA ARRIBA -->
          <g transform="translate(500, 420)">
            <g style="animation: stabDeflect 2.5s ease-in-out infinite alternate; transform-origin: 0px 0px;">
              <polygon points="0,0 260,-40 240,20 0,15" fill="rgba(244, 63, 94, 0.4)" stroke="#f43f5e" stroke-width="3" />
              <text x="140" y="-10" fill="#fff" font-family="'Montserrat'" font-size="15" font-weight="bold">ESTABILIZADOR</text>
              <line x1="240" y1="-50" x2="240" y2="-100" stroke="#f43f5e" stroke-width="4" marker-end="url(#arrow)"/>
              <polygon points="240,-115 230,-95 250,-95" fill="#f43f5e" />
              <text x="210" y="-125" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">COLA SUBE ⬆️</text>
            </g>
          </g>

          <!-- FLECHA RESULTANTE: MORRO DEL AVIÓN AL SUELO -->
          <g transform="translate(140, 480)">
            <circle cx="0" cy="0" r="70" fill="rgba(244, 63, 94, 0.15)" stroke="#f43f5e" stroke-width="2" />
            <line x1="0" y1="-40" x2="0" y2="40" stroke="#f43f5e" stroke-width="6" />
            <polygon points="0,55 -15,35 15,35" fill="#f43f5e" />
            <text x="0" y="85" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="16" font-weight="900">MORRO AL PISO ⬇️</text>
          </g>

          <!-- PANEL TÉCNICO INFERIOR -->
          <g transform="translate(60, 780)">
            <rect width="820" height="340" rx="18" fill="rgba(15, 23, 42, 0.85)" stroke="#a855f7" stroke-width="2" />
            <text x="40" y="45" fill="#a855f7" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">FÍSICA DEL CONTROL DE CABUCEO (PITCH CONTROL)</text>
            <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <text x="40" y="110" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Límite Original de Diseño:</text>
            <text x="450" y="110" fill="#10b981" font-family="'JetBrains Mono'" font-size="17" font-weight="bold">0.6° de deflexión por activación</text>

            <text x="40" y="160" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Modificación Final del MCAS:</text>
            <text x="450" y="160" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="17" font-weight="bold">2.5° de deflexión por activación (4x)</text>

            <text x="40" y="210" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Consecuencia Mecánica:</text>
            <text x="450" y="210" fill="#f59e0b" font-family="'JetBrains Mono'" font-size="17" font-weight="bold">Fuerzas aerodinámicas congelan el tornillo</text>

            <rect x="40" y="245" width="740" height="70" rx="10" fill="rgba(244, 63, 94, 0.2)" stroke="#f43f5e" stroke-width="1.5" />
            <text x="410" y="275" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="15" font-weight="900">A ALTAS VELOCIDADES, EL ESFUERZO HUMANO NO PUEDE GIRAR EL TIMÓN</text>
            <text x="410" y="300" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">Los pilotos no pudieron mover la rueda de trim manual debido a la presión del aire.</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 4: LA BATALLA EN CABINA: EL LOOP DE 5 SEGUNDOS -->
    <div class="scene-card" id="card-4">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 04 • CONFLICTO HOMBRE-MÁQUINA</div>
          <div class="card-title">LA BATALLA EN CABINA: EL LOOP DE 5 SEGUNDOS</div>
        </div>
        <div class="card-tag" style="border-color:#eab308; color:#eab308;">21 RE-ACTIVACIONES</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#020713;">
          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">PERFIL DE PICADA Y LUCHA POR EL CONTROL</text>

          <!-- PALANCA DE CONTROL (YOKE) VIBRANDO POR STICK SHAKER -->
          <g transform="translate(180, 260)" style="animation: yokeShake 0.15s infinite;">
            <!-- Marco de la columna -->
            <rect x="-30" y="80" width="60" height="160" rx="12" fill="#1e293b" stroke="#94a3b8" stroke-width="3"/>
            <!-- Volante / Yoke -->
            <path d="M -110 30 C -110 -40, -40 -60, 0 -60 C 40 -60, 110 -40, 110 30 C 90 60, 50 30, 30 10 L -30 10 C -50 30, -90 60, -110 30 Z" fill="#0f172a" stroke="#eab308" stroke-width="4" />
            <circle cx="0" cy="-20" r="18" fill="#eab308" />
            <text x="0" y="140" text-anchor="middle" fill="#eab308" font-family="'Montserrat'" font-size="15" font-weight="900">STICK SHAKER</text>
            <text x="0" y="165" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13">VIBRACIÓN FORZADA</text>
            
            <!-- Flecha de fuerza humana hacia atrás -->
            <line x1="0" y1="20" x2="0" y2="-120" stroke="#10b981" stroke-width="5" />
            <polygon points="0,-135 -12,-115 12,-115" fill="#10b981"/>
            <text x="0" y="-150" text-anchor="middle" fill="#10b981" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">FUERZA HUMANA: 45 KG (99 LBS)</text>
          </g>

          <!-- RELOJ / CICLO DE 5 SEGUNDOS DEL MCAS -->
          <g transform="translate(680, 260)">
            <circle cx="0" cy="0" r="85" fill="#090d1a" stroke="#f43f5e" stroke-width="4" />
            <!-- Anillo de pulso infinito -->
            <circle cx="0" cy="0" r="85" fill="none" stroke="#f43f5e" stroke-width="3" style="animation: mcasPulseRing 1.5s infinite;" />
            <text x="0" y="-20" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="14">RESET AUTOMÁTICO</text>
            <text x="0" y="18" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="34" font-weight="900">5s</text>
            <text x="0" y="45" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13">LOOP CONTINUO</text>
            <rect x="-95" y="105" width="190" height="35" rx="8" fill="#f43f5e" />
            <text x="0" y="128" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="13" font-weight="900">ANULA AL PILOTO</text>
          </g>

          <!-- GRÁFICA DE PICADA (TRAYECTORIA DE VUELO EN TIEMPO REAL) -->
          <g transform="translate(60, 530)">
            <rect width="820" height="580" rx="18" fill="rgba(2, 6, 23, 0.95)" stroke="#eab308" stroke-width="2" />
            <text x="40" y="45" fill="#eab308" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">TRAYECTORIA TELEMÉTRICA DE VUELO (DIVE PROFILE)</text>
            <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <!-- Curva de altitud ondulada con cada ciclo de 5s perdiendo altura -->
            <path d="M 60 140 Q 140 120 180 180 T 280 230 T 380 290 T 480 370 T 580 430 T 700 520" fill="none" stroke="#f43f5e" stroke-width="5" />
            
            <!-- Puntos de intervención del piloto vs reactivación MCAS -->
            <circle cx="180" cy="180" r="7" fill="#10b981" />
            <text x="180" y="160" fill="#10b981" font-family="'JetBrains Mono'" font-size="11">Piloto nivela</text>

            <circle cx="280" cy="230" r="8" fill="#f43f5e" />
            <text x="290" y="220" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">MCAS #1</text>

            <circle cx="380" cy="290" r="8" fill="#f43f5e" />
            <text x="390" y="280" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">MCAS #5</text>

            <circle cx="480" cy="370" r="8" fill="#f43f5e" />
            <text x="490" y="360" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">MCAS #14</text>

            <circle cx="700" cy="520" r="10" fill="#f43f5e" />
            <text x="590" y="515" fill="#f43f5e" font-family="'Montserrat'" font-size="14" font-weight="900">IMPACTO EN TERRENO</text>

            <!-- Ticker de altímetro digital -->
            <g transform="translate(620, 100)">
              <rect width="160" height="130" rx="10" fill="#090d1a" stroke="#f43f5e" stroke-width="2"/>
              <text x="80" y="30" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="12">ALTITUD (MSL)</text>
              <text x="80" y="75" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="28" font-weight="900">1,200 FT</text>
              <text x="80" y="105" text-anchor="middle" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">-4,000 FPM</text>
            </g>

            <text x="40" y="555" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">La tripulación contrarrestó el software más de 20 veces antes de que el esfuerzo físico fuera insostenible.</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 5: EL MANUAL CENSURADO & LA VOTACIÓN COMUNITARIA -->
    <div class="scene-card" id="card-5">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 05 • AUTOPSIA & COMUNIDAD</div>
          <div class="card-title">MANUAL CENSURADO & TU VOTO</div>
        </div>
        <div class="card-tag" style="border-color:#10b981; color:#10b981;">ENCUESTA CAPÍTULO #12</div>
      </div>
      <div class="canvas-viewport" style="display:flex; flex-direction:column; padding:24px; gap:20px;">

        <!-- TARJETA SUPERIOR: EL DOCUMENTO CENSURADO -->
        <div style="background:#090d1a; border:1.5px solid rgba(255,255,255,0.15); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#f43f5e; letter-spacing:1px; font-weight:800;">FAA FLIGHT CREW OPERATIONS MANUAL (FCOM)</div>
            <div style="font-family:'Montserrat',sans-serif; font-size:22px; font-weight:900; color:#fff; margin-top:4px;">BOEING ELIMINÓ TODA MENCIÓN DEL MCAS</div>
            <div style="font-size:14px; color:#94a3b8; margin-top:4px;">Objetivo: Evitar costos de simulador ($1,000,000 USD por aerolínea) para vender el avión como 100% idéntico.</div>
          </div>
          <div style="background:#f43f5e; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900; font-size:16px; padding:10px 18px; border-radius:8px; transform:rotate(-5deg); box-shadow:0 0 20px rgba(244,63,94,0.5);">
            [CENSURADO]
          </div>
        </div>

        <!-- BOLETA DE VOTACIÓN COMUNITARIA PARA EL CAPÍTULO #12 -->
        <div style="flex:1; background:#020610; border:2px solid #10b981; border-radius:18px; padding:24px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 0 35px rgba(16,185,129,0.15);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="font-family:'Montserrat',sans-serif; font-size:24px; font-weight:900; color:#10b981; display:flex; align-items:center; gap:10px;">
                🗳️ ENCUESTA COMUNITARIA: CAPÍTULO #12
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:13px; background:rgba(16,185,129,0.15); color:#10b981; padding:4px 12px; border-radius:999px; font-weight:bold;">¡VOTA EN COMENTARIOS!</div>
            </div>
            <div style="font-size:16px; color:#94a3b8; margin-top:6px;">¿Qué historia de ingeniería, litigio o fraude técnico quieres que desarmemos?</div>
          </div>

          <div style="display:flex; flex-direction:column; gap:12px;">
            <!-- Opción 1 -->
            <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(56,189,248,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#38bdf8; color:#000; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">1</div>
                <div>
                  <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">🦍 NINTENDO VS UNIVERSAL (1982)</div>
                  <div style="font-size:13px; color:#94a3b8;">La batalla legal por Donkey Kong que salvó a Nintendo y bautizó a Kirby.</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#38bdf8; font-size:15px;">#NintendoKirby</div>
            </div>

            <!-- Opción 2 -->
            <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(244,63,94,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#f43f5e; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">2</div>
                <div>
                  <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">🩸 THERANOS & EL FRAUDE DE EDISON</div>
                  <div style="font-size:13px; color:#94a3b8;">La falsa microfluídica de Elizabeth Holmes y las máquinas comerciales escondidas.</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#f43f5e; font-size:15px;">#TheranosEdison</div>
            </div>

            <!-- Opción 3 -->
            <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(168,85,247,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#a855f7; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">3</div>
                <div>
                  <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">🧠 DEEPSEEK & REDES MOE</div>
                  <div style="font-size:13px; color:#94a3b8;">Arquitectura Mixture of Experts y cómo destronaron los clusters de millones de dólares.</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#a855f7; font-size:15px;">#DeepSeekMoE</div>
            </div>
          </div>

          <div style="text-align:center; font-family:'Space Grotesk',sans-serif; font-size:15px; color:#10b981; font-weight:bold; background:rgba(16,185,129,0.08); padding:10px; border-radius:8px;">
            💬 Déjanos tu opción favorita en los comentarios. El más votado será el próximo capítulo.
          </div>
        </div>

      </div>
    </div>

  </div>

  <!-- SUBTÍTULOS KINETIC PUNCH-PILL -->
  <div class="subtitles-container">
    {''.join(sub_items_html)}
  </div>

  <!-- FOOTER OMNICANAL -->
  <div class="omnichannel-footer">
    <div class="footer-left">
      <span>🚗</span>
      <span>¿En el coche? Escúchanos en Spotify: <strong>sIA Podcast</strong></span>
    </div>
    <div class="footer-right">
      <div class="footer-pill">TikTok: @escucha_sia</div>
      <div class="footer-pill">escucha-sia.github.io</div>
    </div>
  </div>
  </div>
</body>
</html>"""

# Write to file
target_path = Path("sia_tiktok_batch_engine/compositions/boeing_scene.html")
target_path.parent.mkdir(parents=True, exist_ok=True)
with open(target_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Escena generada exitosamente en {target_path}")
