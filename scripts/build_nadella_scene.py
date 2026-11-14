import json
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
TIMESTAMPS_FILE = ROOT_DIR / "scratch" / "nadella_timestamps.json"
OUT_HTML = ROOT_DIR / "sia_tiktok_batch_engine" / "compositions" / "nadella_layoffs_scene.html"

with open(TIMESTAMPS_FILE, "r", encoding="utf-8") as f:
    segments = json.load(f)

TOTAL_DUR = 274.25

# 5 Actos definidos
acts = [
    {"num": 1, "title": "LA PARADOJA DE NADELLA", "start": 0.0, "end": 60.77},
    {"num": 2, "title": "LA PURGA DE QA Y SREs", "start": 60.77, "end": 122.30},
    {"num": 3, "title": "EL CASTILLO DE NAIPES", "start": 122.30, "end": 179.26},
    {"num": 4, "title": "LA ADVERTENCIA SILENCIADA", "start": 179.26, "end": 223.70},
    {"num": 5, "title": "EL APAGÓN INMINENTE (12 NOV)", "start": 223.70, "end": 274.25}
]

# Generar CSS para visibilidad opaca de tarjetas por acto
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

# Generar CSS para la barra de capítulos superior
chap_css = []
for act in acts:
    num = act["num"]
    s_pct = (act["start"] / TOTAL_DUR) * 100
    e_pct = (act["end"] / TOTAL_DUR) * 100
    chap_css.append(f"""
    #pill-{num} {{ animation: c{num}Anim {TOTAL_DUR}s linear infinite; }}
    @keyframes c{num}Anim {{
      0%, {max(0, s_pct - 0.05):.3f}% {{ background: rgba(255, 255, 255, 0.06); color: #94a3b8; border-color: rgba(255, 255, 255, 0.12); }}
      {s_pct:.3f}%, {e_pct - 0.05:.3f}% {{ background: #38bdf8; color: #000; border-color: #38bdf8; font-weight: 900; }}
      {e_pct:.3f}%, 100% {{ background: rgba(255, 255, 255, 0.06); color: #94a3b8; border-color: rgba(255, 255, 255, 0.12); }}
    }}""")

# Subtítulos punchy kinetic
sub_items = []
sub_css = []
for idx, seg in enumerate(segments):
    s_pct = (seg["start"] / TOTAL_DUR) * 100
    e_pct = (seg["end"] / TOTAL_DUR) * 100
    is_jorge = seg["voice"] == "Jorge"
    badge_col = "#38bdf8" if is_jorge else "#ec4899"
    badge_text = "JORGE" if is_jorge else "DALIA"

    sub_items.append(f"""
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

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>sIA Crónicas #13 - La Paradoja de Nadella: Despidos Masivos y Fiebre de IA</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@600;700;800&family=JetBrains+Mono:wght@700;800;900&display=swap');

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      width: 1080px;
      height: 1920px;
      background: #030712;
      color: #fff;
      font-family: 'Space Grotesk', sans-serif;
      overflow: hidden;
      position: relative;
    }}

    .cyber-grid {{
      position: absolute;
      inset: 0;
      background-image: 
        radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.07) 0%, transparent 80%),
        linear-gradient(rgba(56, 189, 248, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.07) 1px, transparent 1px),
        linear-gradient(rgba(244, 63, 94, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(244, 63, 94, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 60px 60px, 60px 60px, 15px 15px, 15px 15px;
      z-index: 1;
    }}

    .scanlines {{
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.18), rgba(0, 0, 0, 0.18) 2px, transparent 2px, transparent 4px);
      pointer-events: none;
      z-index: 2;
    }}

    /* HEADER TÁCTICO (y=24px a 140px) */
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

    .brand-pill {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(15, 23, 42, 0.85);
      border: 1.5px solid #38bdf8;
      border-radius: 999px;
      padding: 8px 24px;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    }}

    .brand-dot {{
      width: 14px;
      height: 14px;
      background: #38bdf8;
      border-radius: 50%;
      box-shadow: 0 0 10px #38bdf8;
      animation: pulseDot 1s infinite alternate;
    }}
    @keyframes pulseDot {{
      from {{ transform: scale(0.85); opacity: 0.6; }}
      to {{ transform: scale(1.25); opacity: 1; }}
    }}

    .brand-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 24px;
      font-weight: 900;
      letter-spacing: 1.5px;
      color: #fff;
    }}

    .header-handles {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 16px;
      color: #94a3b8;
      background: rgba(15, 23, 42, 0.7);
      padding: 6px 18px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}

    /* CAPÍTULOS TÁCTICOS */
    .chapters-track {{
      display: flex;
      gap: 10px;
      width: 100%;
      margin-top: 10px;
    }}

    .chapter-pill {{
      flex: 1;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      border-radius: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: rgba(255, 255, 255, 0.04);
      color: #94a3b8;
      transition: all 0.3s;
    }}

    {"".join(chap_css)}

    /* TIMELINE PROGRESS */
    .timeline-bar {{
      position: absolute;
      top: 142px;
      left: 40px;
      right: 40px;
      height: 4px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 2px;
      overflow: hidden;
      z-index: 10;
    }}
    .timeline-progress {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #38bdf8, #f43f5e, #eab308);
      animation: progressAnim {TOTAL_DUR}s linear infinite;
    }}
    @keyframes progressAnim {{
      0% {{ width: 0%; }}
      100% {{ width: 100%; }}
    }}

    /* EL ÁREA CENTRAL 75% EXCLUSIVA PARA DIAGRAMAS TÉCNICOS (1080x1400px) */
    .scene-container {{
      position: absolute;
      top: 154px;
      left: 40px;
      right: 40px;
      height: 1400px;
      z-index: 5;
    }}

    .scene-card {{
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      background: #040714;
      border-radius: 24px;
      border: 2px solid rgba(56, 189, 248, 0.35);
      padding: 24px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
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
      color: #38bdf8;
      font-weight: 800;
      letter-spacing: 2px;
    }}

    .card-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 26px;
      font-weight: 900;
      color: #fff;
      letter-spacing: 0.5px;
    }}

    .card-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
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
      background: #02050e;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    /* REGLAS CLAVE SVG TRANSFORM */
    svg circle, svg rect, svg polygon {{
      transform-box: fill-box;
      transform-origin: center;
    }}

    /* ANIMACIONES PROCEDURALES KINÉTICAS */
    @keyframes flowDollar {{
      0% {{ stroke-dashoffset: 400; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    @keyframes rackBurnPulse {{
      0%, 100% {{ filter: drop-shadow(0 0 10px #f43f5e); opacity: 0.85; }}
      50% {{ filter: drop-shadow(0 0 30px #ef4444); opacity: 1; }}
    }}

    @keyframes alertBlink {{
      0%, 100% {{ opacity: 0.25; }}
      50% {{ opacity: 1; }}
    }}

    @keyframes radarSweep {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}

    @keyframes cardShake {{
      0%, 100% {{ transform: translate(0, 0); }}
      25% {{ transform: translate(-2px, 1px); }}
      75% {{ transform: translate(2px, -1px); }}
    }}

    /* SUBTÍTULOS KINETIC PUNCH-PILL (y=1570px a 1810px) */
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
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: rgba(15, 23, 42, 0.95);
      border: 2px solid rgba(56, 189, 248, 0.4);
      border-radius: 20px;
      padding: 20px 28px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(12px);
    }}

    .speaker-tag {{
      align-self: flex-start;
      font-family: 'Montserrat', sans-serif;
      font-size: 15px;
      font-weight: 900;
      padding: 4px 14px;
      border-radius: 999px;
      letter-spacing: 1px;
    }}

    .sub-text {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 26px;
      font-weight: 700;
      line-height: 1.35;
      color: #f8fafc;
    }}

    {"".join(sub_css)}

    /* FOOTER TÁCTICO INFERIOR (y=1820px a 1890px) */
    .tactical-footer {{
      position: absolute;
      bottom: 24px;
      left: 40px;
      right: 40px;
      height: 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      color: #64748b;
      z-index: 10;
    }}
  </style>
</head>
<body>
  <div class="cyber-grid"></div>
  <div class="scanlines"></div>

  <!-- CONTENEDOR RAÍZ CON ATRIBUTO DATA-COMPOSITION-ID REQUERIDO POR HYPERFRAMES -->
  <div id="scene-root" data-composition-id="nadella_layoffs_scene" data-width="1080" data-height="1920" style="position:relative; width:1080px; height:1920px;">
    
    <!-- HEADER -->
    <div class="tactical-header">
      <div class="header-top">
        <div class="brand-pill">
          <div class="brand-dot"></div>
          <div class="brand-title">sIA CRÓNICAS #13</div>
        </div>
        <div class="header-handles">
          <span>@escucha_sia</span>
          <span>&bull;</span>
          <span>DILOGÍA MICROSOFT • PARTE 1</span>
        </div>
      </div>
      <div class="chapters-track">
        <div class="chapter-pill" id="pill-1">1. Paradoja</div>
        <div class="chapter-pill" id="pill-2">2. Purga QA</div>
        <div class="chapter-pill" id="pill-3">3. Fragilidad</div>
        <div class="chapter-pill" id="pill-4">4. Alerta</div>
        <div class="chapter-pill" id="pill-5">5. Apagón 12-Nov</div>
      </div>
    </div>

    <!-- LÍNEA DE PROGRESO -->
    <div class="timeline-bar">
      <div class="timeline-progress"></div>
    </div>

    <!-- EL 75% CENTRAL: LAS 5 ESCENAS CINÉTICAS (SIN AVATARES) -->
    <div class="scene-container">
      
      <!-- ACTO 1: LA PARADOJA DE NADELLA (20,000 DESPIDOS VS $50B SILICIO IA) -->
      <div class="scene-card" id="card-1">
        <div class="card-topbar">
          <div class="card-title-group">
            <div class="card-act-num">ACTO 01 • LA PARADOJA CORPORATIVA</div>
            <div class="card-title">EL ENIGMA DEL ÉXITO: SILICIO VS SALARIOS</div>
          </div>
          <div class="card-tag" style="border-color:#f43f5e; color:#f43f5e;">+20,000 DESPIDOS</div>
        </div>
        <div class="canvas-viewport">
          <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
            <defs>
              <linearGradient id="fireGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ef4444"/>
                <stop offset="100%" stop-color="#f43f5e"/>
              </linearGradient>
              <linearGradient id="moneyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8"/>
                <stop offset="100%" stop-color="#10b981"/>
              </linearGradient>
            </defs>

            <text x="470" y="55" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">REASIGNACIÓN BRUTAL DE CAPITAL EN MICROSOFT (2023 - 2026)</text>

            <!-- LA BALANZA ASIMÉTRICA DE CAPITAL -->
            <!-- LADO IZQUIERDO: DESPIDOS MASIVOS DE INGENIEROS -->
            <g transform="translate(60, 100)">
              <rect width="380" height="360" rx="18" fill="rgba(244, 63, 94, 0.08)" stroke="#f43f5e" stroke-width="2.5"/>
              <text x="190" y="45" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="20" font-weight="900">📉 PURGA DE PERSONAL</text>
              <text x="190" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">"El Enigma del Éxito"</text>

              <rect x="35" y="110" width="310" height="150" rx="10" fill="#090d1a" stroke="#f43f5e" stroke-width="1.5"/>
              <text x="190" y="160" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="14">TALENTO HUMANO RECORTADO</text>
              <text x="190" y="205" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="38" font-weight="900">-22,500</text>
              <text x="190" y="240" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="12">INGENIEROS Y ESPECIALISTAS</text>

              <rect x="35" y="285" width="310" height="45" rx="8" fill="#f43f5e"/>
              <text x="190" y="313" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="13" font-weight="900">REDUCCIÓN MASIVA DE OPEX</text>
            </g>

            <!-- TUBERÍA DE DINERO EN TRASLACIÓN CONTINUA (LÁSER DE $ A CLUSTERS) -->
            <g transform="translate(470, 280)">
              <line x1="-30" y1="0" x2="30" y2="0" stroke="#eab308" stroke-width="6" stroke-dasharray="15 8" style="animation: flowDollar 0.8s linear infinite;"/>
              <text x="0" y="-18" text-anchor="middle" fill="#eab308" font-family="'Montserrat'" font-size="13" font-weight="900">TRANSFER</text>
              <text x="0" y="28" text-anchor="middle" fill="#eab308" font-family="'JetBrains Mono'" font-size="12">CAPEX</text>
            </g>

            <!-- LADO DERECHO: COMPRA MASIVA DE CLUSTERS IA Y OPENAI -->
            <g transform="translate(500, 100)">
              <rect width="380" height="360" rx="18" fill="rgba(56, 189, 248, 0.08)" stroke="#38bdf8" stroke-width="2.5"/>
              <text x="190" y="45" text-anchor="middle" fill="#38bdf8" font-family="'Montserrat'" font-size="20" font-weight="900">⚡ GASTO EN SILICIO IA</text>
              <text x="190" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">OpenAI, Maia & Nvidia H100</text>

              <rect x="35" y="110" width="310" height="150" rx="10" fill="#090d1a" stroke="#38bdf8" stroke-width="1.5"/>
              <text x="190" y="160" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="14">CAPEX ANUAL ESTIMADO</text>
              <text x="190" y="205" text-anchor="middle" fill="#38bdf8" font-family="'Montserrat'" font-size="38" font-weight="900">$50,000M</text>
              <text x="190" y="240" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="12">CENTROS DE DATOS & ENERGÍA</text>

              <rect x="35" y="285" width="310" height="45" rx="8" fill="#38bdf8"/>
              <text x="190" y="313" text-anchor="middle" fill="#000" font-family="'Montserrat'" font-size="13" font-weight="900">EXPANSIÓN HIPERESCALAR</text>
            </g>

            <!-- PANEL INFERIOR: LA TESIS DE WALL STREET -->
            <g transform="translate(60, 500)">
              <rect width="820" height="630" rx="20" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="2"/>
              <text x="40" y="45" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">LA FÓRMULA CORPORATIVA DE SATYA NADELLA</text>
              <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

              <!-- Card 1: Valoración Bursátil de $3.2 Trillones -->
              <g transform="translate(40, 95)">
                <rect width="740" height="110" rx="12" fill="#090d1a" stroke="#10b981" stroke-width="1.5"/>
                <text x="25" y="36" fill="#10b981" font-family="'Montserrat'" font-size="18" font-weight="bold">WALL STREET PREMIA EL RECORTE: $3,200,000,000,000 USD</text>
                <text x="25" y="66" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Cada ola de despidos era recibida con aplausos en la bolsa: el mercado premiaba sustituir</text>
                <text x="25" y="90" fill="#fff" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">salarios humanos fijos por infraestructura escalable de inteligencia artificial.</text>
              </g>

              <!-- Card 2: La Falacia de la Productividad Sintética -->
              <g transform="translate(40, 235)">
                <rect width="740" height="110" rx="12" fill="#090d1a" stroke="#f43f5e" stroke-width="1.5"/>
                <text x="25" y="36" fill="#f43f5e" font-family="'Montserrat'" font-size="18" font-weight="bold">LA PROMESA DE COPILOT: "HACER MÁS CON MENOS"</text>
                <text x="25" y="66" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">La narrativa oficial sostenía que los ingenieros restantes serían 50% más productivos</text>
                <text x="25" y="90" fill="#f87171" font-family="'JetBrains Mono'" font-size="14">gracias a Copilot escribiendo código y autogenerando pruebas unitarias en bucle.</text>
              </g>

              <!-- Card 3: El Vaciamiento Invisible -->
              <g transform="translate(40, 375)">
                <rect width="740" height="210" rx="14" fill="rgba(244, 63, 94, 0.12)" stroke="#f43f5e" stroke-width="2"/>
                <text x="370" y="45" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="900">EL VERDADERO COSTO OCULTO</text>
                <text x="370" y="85" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">No se despidió a personal prescindible: se cortaron las arterias operativas</text>
                <text x="370" y="115" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">que sabían cómo levantar Exchange y Azure cuando las máquinas fallan.</text>
                <rect x="50" y="145" width="640" height="42" rx="8" fill="#f43f5e"/>
                <text x="370" y="172" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="14" font-weight="900">SE CAMBIÓ LA MEMORIA INSTITUCIONAL POR ASISTENTES DE CÓDIGO</text>
              </g>
            </g>
          </svg>
        </div>
      </div>

      <!-- ACTO 2: LA PURGA DE QA Y SREs (LA MUERTE DEL TESTING MANUAL) -->
      <div class="scene-card" id="card-2">
        <div class="card-topbar">
          <div class="card-title-group">
            <div class="card-act-num">ACTO 02 • DESMANTELAMIENTO OPERATIVO</div>
            <div class="card-title">LA MUERTE DEL CONTROL DE CALIDAD (QA)</div>
          </div>
          <div class="card-tag" style="border-color:#eab308; color:#eab308;">30% CÓDIGO IA</div>
        </div>
        <div class="canvas-viewport">
          <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
            <text x="470" y="55" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">DE BRIGADAS DESTRUCTIVAS A PIPELINES CIEGOS</text>

            <!-- ANTES VS DESPUÉS DEL DESMANTELAMIENTO -->
            <!-- ANTES: INGENIERÍA RESILIENTE -->
            <g transform="translate(60, 100)">
              <rect width="380" height="360" rx="18" fill="rgba(16, 185, 129, 0.08)" stroke="#10b981" stroke-width="2"/>
              <text x="190" y="45" text-anchor="middle" fill="#10b981" font-family="'Montserrat'" font-size="18" font-weight="900">EL MODELO HISTÓRICO</text>
              <text x="190" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">Pruebas Destructivas Reales</text>

              <rect x="35" y="110" width="310" height="150" rx="10" fill="#061f18" stroke="#10b981" stroke-width="1.5"/>
              <text x="190" y="150" text-anchor="middle" fill="#10b981" font-family="'Montserrat'" font-size="16" font-weight="bold">🛡️ BRIGADAS QA & SRE</text>
              <text x="190" y="180" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="12">&bull; Simulacros de Cold Start</text>
              <text x="190" y="205" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="12">&bull; Caída forzada de centros de datos</text>
              <text x="190" y="230" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="12">&bull; Validación manual de dependencias</text>

              <rect x="35" y="285" width="310" height="45" rx="8" fill="#10b981"/>
              <text x="190" y="313" text-anchor="middle" fill="#000" font-family="'Montserrat'" font-size="13" font-weight="900">HUMAN-IN-THE-LOOP CRÍTICO</text>
            </g>

            <!-- DESPUÉS: LA PURGA POR IA -->
            <g transform="translate(500, 100)">
              <rect width="380" height="360" rx="18" fill="rgba(244, 63, 94, 0.08)" stroke="#f43f5e" stroke-width="2.5"/>
              <text x="190" y="45" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="18" font-weight="900">EL NUEVO DOGMA IA</text>
              <text x="190" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">Automatización Desatendida</text>

              <rect x="35" y="110" width="310" height="150" rx="10" fill="#090d1a" stroke="#f43f5e" stroke-width="1.5"/>
              <text x="190" y="150" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="16" font-weight="bold">🤖 PIPELINE SINTÉTICO</text>
              <text x="190" y="180" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="12">&bull; Test Slop: cobertura sin lógica</text>
              <text x="190" y="205" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="12">&bull; 30% del código escrito por IA</text>
              <text x="190" y="230" text-anchor="middle" fill="#f87171" font-family="'JetBrains Mono'" font-size="12">&bull; Health checks automatizados ciegos</text>

              <rect x="35" y="285" width="310" height="45" rx="8" fill="#f43f5e"/>
              <text x="190" y="313" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="13" font-weight="900">CERO VIGILANCIA HUMANA</text>
            </g>

            <!-- PIPELINE ANIMADO: CÓMO SE INFILTRAN LOS BUGS -->
            <g transform="translate(60, 500)">
              <rect width="820" height="630" rx="20" fill="rgba(15, 23, 42, 0.95)" stroke="#eab308" stroke-width="2"/>
              <text x="40" y="45" fill="#eab308" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">LA FRACTURA DEL CICLO CI/CD EN AZURE</text>
              <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

              <!-- El flujo de código sin filtro -->
              <g transform="translate(40, 100)">
                <rect width="740" height="120" rx="12" fill="#090d1a" stroke="#38bdf8" stroke-width="1.5"/>
                <text x="25" y="36" fill="#38bdf8" font-family="'Montserrat'" font-size="17" font-weight="bold">1. GENERACIÓN VELOZ, AUDITORÍA NULA</text>
                <text x="25" y="66" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Los desarrolladores bajo presión usan Copilot para despachar miles de líneas de código.</text>
                <text x="25" y="92" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Nadie revisa el comportamiento en condiciones de carrera porque no hay tiempo asignado.</text>
              </g>

              <g transform="translate(40, 245)">
                <rect width="740" height="120" rx="12" fill="#090d1a" stroke="#f43f5e" stroke-width="1.5"/>
                <text x="25" y="36" fill="#f43f5e" font-family="'Montserrat'" font-size="17" font-weight="bold">2. LA TRAMPA DEL "TEST SLOP"</text>
                <text x="25" y="66" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Las pruebas sintéticas creadas por IA devuelven 100% de éxito en cobertura superficial,</text>
                <text x="25" y="92" fill="#f87171" font-family="'Space Grotesk'" font-size="15">pero omiten comprobar qué sucede si un balanceador satura la memoria de los nodos.</text>
              </g>

              <rect x="40" y="390" width="740" height="195" rx="14" fill="rgba(234, 179, 8, 0.12)" stroke="#eab308" stroke-width="2"/>
              <text x="410" y="440" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="900">LA DESAPARICIÓN DE LOS VETERANOS</text>
              <text x="410" y="480" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">Al despedir a ingenieros con 15 o 20 años en la arquitectura de Exchange,</text>
              <text x="410" y="510" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">Microsoft perdió la intuición para responder ante un apagón imprevisto.</text>
              <text x="410" y="545" text-anchor="middle" fill="#eab308" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">UN SISTEMA DE $3B ADMINISTRADO POR PILOTO AUTOMÁTICO CIEGO</text>
            </g>
          </svg>
        </div>
      </div>

      <!-- ACTO 3: EL CASTILLO DE NAIPES (ANSIEDAD Y FRAGILIDAD EN AZURE) -->
      <div class="scene-card" id="card-3">
        <div class="card-topbar">
          <div class="card-title-group">
            <div class="card-act-num">ACTO 03 • MONOCULTIVO HIPERFRÁGIL</div>
            <div class="card-title">EL CASTILLO DE NAIPES DE LA NUBE</div>
          </div>
          <div class="card-tag" style="border-color:#ec4899; color:#ec4899;">80% DEL PLANETA</div>
        </div>
        <div class="canvas-viewport">
          <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
            <text x="470" y="55" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">DEPENDENCIAS GLOBALES ATADAS A UNA SOLA EMPRESA</text>

            <!-- LA PIRÁMIDE DE FRAGILIDAD (ANIMADA) -->
            <g transform="translate(470, 240)">
              <!-- Nivel 1 (Base): Azure & Red HyperScale -->
              <polygon points="-380,120 380,120 280,30 -280,30" fill="rgba(56, 189, 248, 0.15)" stroke="#38bdf8" stroke-width="2"/>
              <text x="0" y="85" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="18" font-weight="bold">INFRAESTRUCTURA BASE AZURE (CAPACIDAD RECORTADA)</text>

              <!-- Nivel 2: Exchange, Teams, SharePoint -->
              <polygon points="-260,20 260,20 180,-60 -180,-60" fill="rgba(168, 85, 247, 0.18)" stroke="#a855f7" stroke-width="2"/>
              <text x="0" y="-12" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="17" font-weight="bold">MICROSOFT 365, TEAMS & EXCHANGE ONLINE</text>

              <!-- Nivel 3 (Cúspide inestable): Millones de Clientes -->
              <polygon points="-160,-70 160,-70 0,-160" fill="rgba(244, 63, 94, 0.25)" stroke="#f43f5e" stroke-width="2.5" style="animation: cardShake 3s ease-in-out infinite;"/>
              <text x="0" y="-105" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="15" font-weight="900">74 PAÍSES, BANCOS Y HOSPITALES</text>
            </g>

            <!-- CUADROS DE ALERTA: LA CARTA DE LOS INGENIEROS DE AZURE -->
            <g transform="translate(60, 480)">
              <rect width="820" height="650" rx="20" fill="rgba(15, 23, 42, 0.95)" stroke="#ec4899" stroke-width="2"/>
              <text x="40" y="45" fill="#ec4899" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">TESTIMONIOS INTERNOS EN FOROS DE REDMOND (BLIND)</text>
              <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

              <!-- Testimonio 1 -->
              <g transform="translate(40, 95)">
                <rect width="740" height="135" rx="12" fill="#090d1a" stroke="#ec4899" stroke-width="1.5"/>
                <text x="25" y="34" fill="#ec4899" font-family="'Montserrat'" font-size="16" font-weight="bold">"VOLAMOS UN AVIÓN SUPERSÓNICO SIN MECÁNICOS"</text>
                <text x="25" y="65" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">"La directiva cree que la IA puede autogestionar la topología de red. Pero cuando los</text>
                <text x="25" y="90" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">balanceadores entran en bucle, un modelo de lenguaje no sabe qué switch desconectar."</text>
                <text x="25" y="118" fill="#fff" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">&mdash; Ingeniero Principal de Azure (Enero 2026)</text>
              </g>

              <!-- Testimonio 2: La carga insostenible de guardias -->
              <g transform="translate(40, 255)">
                <rect width="740" height="135" rx="12" fill="#090d1a" stroke="#38bdf8" stroke-width="1.5"/>
                <text x="25" y="34" fill="#38bdf8" font-family="'Montserrat'" font-size="16" font-weight="bold">GUARDÍAS EN CRISIS: ON-CALL FATIGUE</text>
                <text x="25" y="65" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">"Un solo ingeniero en turno ahora atiende lo que antes cubría un equipo de cinco personas.</text>
                <text x="25" y="90" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Si ocurre un incidente masivo, la respuesta humana se demorará horas en organizarse."</text>
                <text x="25" y="118" fill="#fff" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">&mdash; Reporte interno de fiabilidad</text>
              </g>

              <rect x="40" y="420" width="740" height="185" rx="14" fill="rgba(244, 63, 94, 0.12)" stroke="#f43f5e" stroke-width="2"/>
              <text x="410" y="465" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="900">EL EFECTO MONOCULTIVO</text>
              <text x="410" y="505" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">Gobiernos, bancos centrales y sanidad pública consolidaron todo en una misma cuenta.</text>
              <text x="410" y="535" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">Si Microsoft pestañeaba, el planeta entero perdía la comunicación.</text>
              <text x="410" y="570" text-anchor="middle" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">Y EL PESTAÑEO ESTABA A DÍAS DE SUCEDER</text>
            </g>
          </svg>
        </div>
      </div>

      <!-- ACTO 4: LA ADVERTENCIA SILENCIADA (EL COMITÉ DE AUDITORÍA) -->
      <div class="scene-card" id="card-4">
        <div class="card-topbar">
          <div class="card-title-group">
            <div class="card-act-num">ACTO 04 • LA CRÓNICA ANUNCIADA</div>
            <div class="card-title">LA ADVERTENCIA QUE NADIE ESCUCHÓ</div>
          </div>
          <div class="card-tag" style="border-color:#f43f5e; color:#f43f5e;">RIESGO CRÍTICO</div>
        </div>
        <div class="canvas-viewport">
          <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
            <text x="470" y="55" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">EL EXPEDIENTE DE RIESGO OPERACIONAL OCULTO</text>

            <!-- MEMO DE AUDITORÍA CON SELLO ROJO -->
            <g transform="translate(60, 100)">
              <rect width="820" height="380" rx="18" fill="rgba(244, 63, 94, 0.08)" stroke="#f43f5e" stroke-width="2.5"/>
              <text x="40" y="45" fill="#f43f5e" font-family="'Montserrat'" font-size="20" font-weight="900">⚠️ MEMORANDO DE RIESGO DE INFRAESTRUCTURA (OCTUBRE 2026)</text>
              <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

              <g transform="translate(40, 90)">
                <text x="0" y="25" fill="#fff" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">HALLAZGOS CLAVE ELEVADOS A LA JUNTA DIRECTIVA:</text>
                <text x="0" y="60" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">&bull; 1. Reducción del 45% en personal senior con experiencia en resolución de emergencias.</text>
                <text x="0" y="95" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">&bull; 2. Dependencia excesiva de algoritmos de conmutación por error (failover) no probados.</text>
                <text x="0" y="130" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">&bull; 3. Ausencia de simulacros de recuperación ante estampidas de tráfico (Thundering Herd).</text>
                <text x="0" y="165" fill="#f87171" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">&bull; CONCLUSI&Oacute;N: La infraestructura colapsar&aacute;</text>
                <text x="18" y="190" fill="#f87171" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">ante una reconfiguraci&oacute;n rutinaria de red.</text>
              </g>

              <!-- Sello de Censura Corporativa -->
              <g transform="translate(560, 240) rotate(-10)">
                <rect width="210" height="70" rx="8" fill="none" stroke="#ef4444" stroke-width="4"/>
                <text x="105" y="42" text-anchor="middle" fill="#ef4444" font-family="'Montserrat'" font-size="22" font-weight="900">DESESTIMADO</text>
                <text x="105" y="60" text-anchor="middle" fill="#ef4444" font-family="'JetBrains Mono'" font-size="11" font-weight="bold">PRIORIDAD: CRECIMIENTO IA</text>
              </g>
            </g>

            <!-- COMPARATIVA: COSTE DE GUARDIA VS COSTE DE PARADA -->
            <g transform="translate(60, 520)">
              <rect width="820" height="590" rx="20" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="2"/>
              <text x="40" y="45" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">LA MIOPÍA DEL AHORRO FINANCIERO A CORTO PLAZO</text>
              <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

              <!-- Ahorro en ingenieros -->
              <g transform="translate(40, 100)">
                <rect width="740" height="110" rx="12" fill="#090d1a" stroke="#10b981" stroke-width="1.5"/>
                <text x="25" y="36" fill="#10b981" font-family="'Montserrat'" font-size="17" font-weight="bold">AHORRO TEÓRICO EN SALARIOS: ~$1,800M USD</text>
                <text x="25" y="66" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Dinero ahorrado al recortar puestos de ingeniería senior y soporte operativo,</text>
                <text x="25" y="92" fill="#fff" font-family="'JetBrains Mono'" font-size="14">celebrado en reportes trimestrales para inflar el flujo libre de caja.</text>
              </g>

              <!-- Costo del colapso -->
              <g transform="translate(40, 240)">
                <rect width="740" height="110" rx="12" fill="#090d1a" stroke="#f43f5e" stroke-width="1.5"/>
                <text x="25" y="36" fill="#f43f5e" font-family="'Montserrat'" font-size="17" font-weight="bold">COSTO POTENCIAL DE UN APAGÓN GLOBAL: +$10,000M USD</text>
                <text x="25" y="66" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Sanciones regulatorias, acuerdos de nivel de servicio (SLAs) rotos con bancos,</text>
                <text x="25" y="92" fill="#f87171" font-family="'JetBrains Mono'" font-size="14">pérdida irrecuperable de confianza y daño reputacional en la nube.</text>
              </g>

              <rect x="40" y="380" width="740" height="175" rx="14" fill="rgba(244, 63, 94, 0.12)" stroke="#f43f5e" stroke-width="2"/>
              <text x="410" y="425" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="900">EL RELOJ DE ARENA LLEGABA A CERO</text>
              <text x="410" y="465" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">Las condiciones estaban dadas: un sistema sin defensas humanas veteranas</text>
              <text x="410" y="495" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">esperando únicamente el chispazo de una actualización rutinaria.</text>
              <text x="410" y="530" text-anchor="middle" fill="#f43f5e" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">ESE CHISPAZO OCURRIÓ EL 12 DE NOVIEMBRE</text>
            </g>
          </svg>
        </div>
      </div>

      <!-- ACTO 5: EL GANCHO A LA PARTE 2 Y LLAMADO A LA COMUNIDAD -->
      <div class="scene-card" id="card-5">
        <div class="card-topbar">
          <div class="card-title-group">
            <div class="card-act-num">ACTO 05 • EL DESENLACE INEVITABLE</div>
            <div class="card-title">PARTE 2: LA AUTOPSIA DEL 12 DE NOVIEMBRE</div>
          </div>
          <div class="card-tag" style="border-color:#38bdf8; color:#38bdf8;">CONTINUARÁ...</div>
        </div>
        <div class="canvas-viewport" style="display:flex; flex-direction:column; padding:24px; gap:20px;">

          <!-- TARJETA SUPERIOR: EL IMPACTO DEL APAGÓN DEL 12 DE NOVIEMBRE -->
          <div style="background:#090d1a; border:2px solid #f43f5e; border-radius:16px; padding:20px 24px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 0 30px rgba(244,63,94,0.2);">
            <div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#f43f5e; letter-spacing:1.5px; font-weight:800;">JUEVES 12 DE NOVIEMBRE DE 2026 &bull; 13:26 ET</div>
              <div style="font-family:'Montserrat',sans-serif; font-size:24px; font-weight:900; color:#fff; margin-top:4px;">EL DÍA QUE MICROSOFT COLAPSÓ</div>
              <div style="font-size:15px; color:#94a3b8; margin-top:4px;">74 países a oscuras, el Banco de Inglaterra incomunicado y 20 horas de parálisis global.</div>
            </div>
            <div style="background:#f43f5e; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; padding:12px 22px; border-radius:10px; box-shadow:0 0 20px rgba(244,63,94,0.6);">
              18h CAÍDA
            </div>
          </div>

          <!-- BUZÓN Y PREGUNTA PARA LA COMUNIDAD -->
          <div style="flex:1; background:#020610; border:2px solid #38bdf8; border-radius:18px; padding:24px; display:flex; flex-direction:column; justify-content:space-evenly; box-shadow:0 0 35px rgba(56,189,248,0.15);">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-family:'Montserrat',sans-serif; font-size:24px; font-weight:900; color:#38bdf8; display:flex; align-items:center; gap:10px;">
                  🗳️ DEBATE DE INGENIERÍA: ¿GENIALIDAD O NEGLIGENCIA?
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:13px; background:rgba(56,189,248,0.15); color:#38bdf8; padding:4px 12px; border-radius:999px; font-weight:bold;">¡COMENTA AQUÍ!</div>
              </div>
              <div style="font-size:16px; color:#94a3b8; margin-top:6px;">¿Fue inteligente recortar miles de ingenieros para financiar clusters de IA, o desató el apagón?</div>
            </div>

            <div style="display:flex; flex-direction:column; gap:14px;">
              <!-- Opción A -->
              <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(56,189,248,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:16px;">
                  <div style="width:36px; height:36px; border-radius:8px; background:#38bdf8; color:#000; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">1</div>
                  <div>
                    <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">NEGLIGENCIA HISTÓRICA</div>
                    <div style="font-size:13px; color:#94a3b8;">La nube no puede operar sin intuición humana; la IA no sabe resolver emergencias.</div>
                  </div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#38bdf8; font-size:14px;">#HumanFirst</div>
              </div>

              <!-- Opción B -->
              <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(16,185,129,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:16px;">
                  <div style="width:36px; height:36px; border-radius:8px; background:#10b981; color:#000; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">2</div>
                  <div>
                    <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">TRANSICIÓN INEVITABLE</div>
                    <div style="font-size:13px; color:#94a3b8;">El silicio y los agentes son el futuro; los fallos son solo dolores de crecimiento.</div>
                  </div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#10b981; font-size:14px;">#AIFuture</div>
              </div>
            </div>

            <!-- Avance de la Parte 2 -->
            <div style="text-align:center; font-family:'Space Grotesk',sans-serif; font-size:16px; color:#38bdf8; font-weight:bold; background:rgba(56,189,248,0.08); padding:14px; border-radius:10px; border:1px solid rgba(56,189,248,0.3);">
              ⚡ PARTE 2 DISPONIBLE MAÑANA: La autopsia técnica del Thundering Herd y el fallo en cascada de los Health Checks de Microsoft.
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- SUBTÍTULOS KINETIC PUNCH-PILL -->
    <div class="subtitles-container">
      {"".join(sub_items)}
    </div>

    <!-- FOOTER TÁCTICO -->
    <div class="tactical-footer">
      <div>🚗 ¿En el coche? Escúchanos en Spotify: sIA Podcast</div>
      <div>TikTok: @escucha_sia &bull; escucha-sia.github.io</div>
    </div>

  </div>
</body>
</html>"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Escena compilada exitosamente en {OUT_HTML}")
