import json
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Load timestamps
with open("scratch/moe_timestamps.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

TOTAL_DUR = 253.22

ACTS = [
    {"num": 1, "start": 0.0, "end": 57.4, "title": "EL MONOLITO DENSO", "tag": "600B ENERGÍA & VRAM"},
    {"num": 2, "start": 57.4, "end": 112.2, "title": "GATING ROUTER & MOE", "tag": "37B ACTIVOS / 671B TOTAL"},
    {"num": 3, "start": 112.2, "end": 164.5, "title": "LATENT ATTENTION (MLA)", "tag": "-93% MEMORIA KV CACHE"},
    {"num": 4, "start": 164.5, "end": 213.9, "title": "PRECISIÓN FP8 & DUALPIPE", "tag": "SHOCKWAVE EN WALL STREET"},
    {"num": 5, "start": 213.9, "end": 253.22, "title": "COMUNIDAD & TU PROPUESTA", "tag": "TÚ DECIDES EL PRÓXIMO TEMA"}
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
colors = ["#38bdf8", "#a855f7", "#10b981", "#f43f5e", "#eab308"]
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

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>sIA Crónicas #12: DeepSeek, Mixture of Experts (MoE) y la Rebelión del Hardware</title>
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
        radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.07) 0%, transparent 80%),
        linear-gradient(rgba(56, 189, 248, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.07) 1px, transparent 1px),
        linear-gradient(rgba(168, 85, 247, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(168, 85, 247, 0.03) 1px, transparent 1px);
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
      background: rgba(168, 85, 247, 0.2);
      border: 1.5px solid #a855f7;
      padding: 8px 18px;
      border-radius: 999px;
      box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }}

    .brand-dot {{
      width: 14px;
      height: 14px;
      background: #c084fc;
      border-radius: 50%;
      box-shadow: 0 0 12px #c084fc;
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
      background: linear-gradient(90deg, #38bdf8, #a855f7, #10b981, #f43f5e, #eab308);
      animation: progressAnim {TOTAL_DUR}s linear infinite;
    }}
    @keyframes progressAnim {{ 0% {{ width: 0%; }} 100% {{ width: 100%; }} }}

    /* MAIN STAGE (75% ALTURA CENTRAL - CERO AVATARES) */
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
      background: #040714;
      border: 1.5px solid rgba(168, 85, 247, 0.3);
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), inset 0 0 40px rgba(168, 85, 247, 0.08);
      padding: 32px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

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
      color: #a855f7;
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
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid #a855f7;
      color: #c084fc;
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

    /* ANIMACIONES PROCEDURALES CONTINUAS */
    svg circle {{
      transform-box: fill-box;
      transform-origin: center;
    }}

    @keyframes tokenStream {{
      0% {{ stroke-dashoffset: 400; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    @keyframes routerPulse {{
      0% {{ transform: scale(1); filter: drop-shadow(0 0 10px #a855f7); }}
      50% {{ transform: scale(1.08); filter: drop-shadow(0 0 25px #c084fc); }}
      100% {{ transform: scale(1); filter: drop-shadow(0 0 10px #a855f7); }}
    }}

    @keyframes nodeActiveGlow {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.95); }}
      50% {{ opacity: 1; transform: scale(1.1); fill: #38bdf8; }}
    }}

    @keyframes funnelSqueeze {{
      0% {{ stroke-dashoffset: 300; transform: scaleX(1); }}
      50% {{ transform: scaleX(0.96); }}
      100% {{ stroke-dashoffset: 0; transform: scaleX(1); }}
    }}

    @keyframes marketCrashLine {{
      0% {{ stroke-dashoffset: 500; }}
      100% {{ stroke-dashoffset: 0; }}
    }}

    @keyframes dualPipeLoop {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-160px); }}
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
      height: 100%;
      background: rgba(6, 11, 24, 0.94);
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

    /* FOOTER OMNICANAL */
    .omnichannel-footer {{
      position: absolute;
      bottom: 24px;
      left: 40px;
      right: 40px;
      height: 70px;
      background: rgba(15, 23, 42, 0.85);
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
  <div id="scene-root" data-composition-id="moe_scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
  <div class="cyber-grid"></div>
  <div class="scanlines"></div>
  <div class="watermark">sIA CRÓNICAS #12 • DEEPSEEK & MOE</div>

  <!-- HEADER TÁCTICO -->
  <div class="tactical-header">
    <div class="header-top">
      <div class="brand-badge">
        <div class="brand-dot"></div>
        <div class="brand-name">sIA CRÓNICAS #12</div>
      </div>
      <div class="channel-tag">@escucha_sia • SPOTIFY & TIKTOK</div>
    </div>
    <div class="chapter-pills">
      <div class="chap-pill" id="pill-1">1. MONOLITO</div>
      <div class="chap-pill" id="pill-2">2. GATING MOE</div>
      <div class="chap-pill" id="pill-3">3. LATENT MLA</div>
      <div class="chap-pill" id="pill-4">4. FP8 & CRASH</div>
      <div class="chap-pill" id="pill-5">5. TU TEMA</div>
    </div>
  </div>

  <div class="progress-bar-container">
    <div class="progress-bar"></div>
  </div>

  <!-- MAIN STAGE (CERO AVATARES: 100% ESPACIO TÉCNICO VIVO) -->
  <div class="main-stage">

    <!-- ACTO 1: EL MITO DEL MONOLITO DENSO -->
    <div class="scene-card" id="card-1">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 01 • INEFICIENCIA BRUTA</div>
          <div class="card-title">EL FRAUDE DEL MONOLITO DENSO</div>
        </div>
        <div class="card-tag">MODELO DENSO VS SPARSE</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
          <defs>
            <linearGradient id="fireGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#ef4444"/>
              <stop offset="100%" stop-color="#f97316"/>
            </linearGradient>
            <linearGradient id="coolGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#38bdf8"/>
              <stop offset="100%" stop-color="#0284c7"/>
            </linearGradient>
          </defs>

          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">ANATOMÍA DE EJECUCIÓN: DENSE TRANSFORMER</text>

          <!-- MATRIZ DE PARÁMETROS DENSOS (TODOS ENCENDIDOS EN ROJO FUEGO) -->
          <g transform="translate(70, 120)">
            <rect width="800" height="420" rx="16" fill="rgba(239, 68, 68, 0.08)" stroke="#ef4444" stroke-width="2.5" />
            <text x="30" y="45" fill="#ef4444" font-family="'Montserrat'" font-size="20" font-weight="900">🔥 TRANSFORMER DENSO: 100% PARÁMETROS ACTIVOS</text>
            <text x="30" y="75" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="14">Cada token despierta la totalidad de la matriz de pesos (Full FLOP Burn)</text>

            <!-- Grid de 48 nodos neuronales interconectados encendiéndose en bucle -->
            <g transform="translate(40, 100)">
              <!-- Capa 1 -->
              <circle cx="60" cy="50" r="14" fill="#ef4444" style="animation: nodeActiveGlow 0.8s infinite alternate;" />
              <circle cx="60" cy="120" r="14" fill="#ef4444" style="animation: nodeActiveGlow 0.9s infinite alternate;" />
              <circle cx="60" cy="190" r="14" fill="#ef4444" style="animation: nodeActiveGlow 0.7s infinite alternate;" />
              <circle cx="60" cy="260" r="14" fill="#ef4444" style="animation: nodeActiveGlow 1.0s infinite alternate;" />

              <!-- Capa 2 -->
              <circle cx="260" cy="50" r="14" fill="#f97316" style="animation: nodeActiveGlow 0.9s infinite alternate;" />
              <circle cx="260" cy="120" r="14" fill="#f97316" style="animation: nodeActiveGlow 0.7s infinite alternate;" />
              <circle cx="260" cy="190" r="14" fill="#f97316" style="animation: nodeActiveGlow 1.1s infinite alternate;" />
              <circle cx="260" cy="260" r="14" fill="#f97316" style="animation: nodeActiveGlow 0.8s infinite alternate;" />

              <!-- Capa 3 -->
              <circle cx="460" cy="50" r="14" fill="#ef4444" style="animation: nodeActiveGlow 1.0s infinite alternate;" />
              <circle cx="460" cy="120" r="14" fill="#ef4444" style="animation: nodeActiveGlow 0.8s infinite alternate;" />
              <circle cx="460" cy="190" r="14" fill="#ef4444" style="animation: nodeActiveGlow 0.9s infinite alternate;" />
              <circle cx="460" cy="260" r="14" fill="#ef4444" style="animation: nodeActiveGlow 0.7s infinite alternate;" />

              <!-- Capa 4 -->
              <circle cx="660" cy="50" r="14" fill="#f97316" style="animation: nodeActiveGlow 0.7s infinite alternate;" />
              <circle cx="660" cy="120" r="14" fill="#f97316" style="animation: nodeActiveGlow 1.1s infinite alternate;" />
              <circle cx="660" cy="190" r="14" fill="#f97316" style="animation: nodeActiveGlow 0.8s infinite alternate;" />
              <circle cx="660" cy="260" r="14" fill="#f97316" style="animation: nodeActiveGlow 0.9s infinite alternate;" />

              <!-- Líneas sinápticas que arden con pulsos de datos continuos -->
              <g stroke="#f97316" stroke-width="1.5" opacity="0.4" stroke-dasharray="10 5" style="animation: tokenStream 1s linear infinite;">
                <line x1="60" y1="50" x2="260" y2="50"/>
                <line x1="60" y1="50" x2="260" y2="120"/>
                <line x1="60" y1="120" x2="260" y2="190"/>
                <line x1="60" y1="190" x2="260" y2="260"/>
                <line x1="260" y1="50" x2="460" y2="120"/>
                <line x1="260" y1="120" x2="460" y2="190"/>
                <line x1="260" y1="190" x2="460" y2="260"/>
                <line x1="460" y1="50" x2="660" y2="50"/>
                <line x1="460" y1="120" x2="660" y2="120"/>
                <line x1="460" y1="190" x2="660" y2="190"/>
                <line x1="460" y1="260" x2="660" y2="260"/>
              </g>
            </g>
          </g>

          <!-- GAUGES TELEMÉTRICOS DE GASTO ENERGÉTICO -->
          <g transform="translate(70, 580)">
            <rect width="800" height="210" rx="16" fill="rgba(15, 23, 42, 0.85)" stroke="#38bdf8" stroke-width="1.5" />
            <text x="35" y="40" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="16" font-weight="bold">MÉTRICAS DE CARGA POR TOKEN (GPT-4 DENSE)</text>
            <line x1="35" y1="55" x2="765" y2="55" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <!-- Barra VRAM -->
            <text x="35" y="95" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Consumo VRAM / Token:</text>
            <rect x="260" y="78" width="380" height="24" rx="6" fill="#1e293b"/>
            <rect x="260" y="78" width="365" height="24" rx="6" fill="url(#fireGrad)"/>
            <text x="655" y="96" fill="#fff" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">96% CRITICAL</text>

            <!-- Barra Energía -->
            <text x="35" y="145" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Gasto Térmico / Nodo:</text>
            <rect x="260" y="128" width="380" height="24" rx="6" fill="#1e293b"/>
            <rect x="260" y="128" width="350" height="24" rx="6" fill="url(#fireGrad)"/>
            <text x="655" y="146" fill="#fff" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">700W / H100</text>

            <text x="35" y="188" fill="#f87171" font-family="'JetBrains Mono'" font-size="14">Analogía: Encender todas las luces de un rascacielos para leer una sola línea.</text>
          </g>

          <!-- TARJETA INFERIOR: LA SOLUCIÓN DE DEEPSEEK -->
          <g transform="translate(70, 830)">
            <rect width="800" height="300" rx="16" fill="rgba(16, 185, 129, 0.08)" stroke="#10b981" stroke-width="2" />
            <text x="35" y="45" fill="#10b981" font-family="'Montserrat'" font-size="22" font-weight="900">⚡ LA RUPTURA: ARQUITECTURA ESCASA (SPARSE MOE)</text>
            <text x="35" y="80" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">En lugar de quemar 600,000 millones de parámetros por palabra:</text>

            <g transform="translate(35, 110)">
              <rect width="340" height="75" rx="10" fill="#090d1a" stroke="#ef4444" stroke-width="1.5"/>
              <text x="20" y="30" fill="#ef4444" font-family="'JetBrains Mono'" font-size="14">MODELO DENSO TRADICIONAL</text>
              <text x="20" y="58" fill="#fff" font-family="'Montserrat'" font-size="18" font-weight="bold">100% Parámetros Activos</text>
            </g>

            <g transform="translate(420, 110)">
              <rect width="340" height="75" rx="10" fill="#090d1a" stroke="#10b981" stroke-width="2"/>
              <text x="20" y="30" fill="#10b981" font-family="'JetBrains Mono'" font-size="14">DEEPSEEK-V3 SPARSE MOE</text>
              <text x="20" y="58" fill="#fff" font-family="'Montserrat'" font-size="18" font-weight="bold">Solo 5.5% Activo (37B / 671B)</text>
            </g>

            <rect x="35" y="215" width="730" height="60" rx="10" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" stroke-width="1.5"/>
            <text x="400" y="251" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="14" font-weight="900">COSTO DE ENTRENAMIENTO: MENOS DE $6 MILLONES USD (VS $100M+ SILICON VALLEY)</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 2: GATING ROUTER & TOP-K ENRUTAMIENTO DINÁMICO -->
    <div class="scene-card" id="card-2">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 02 • ALGORITMO DE ENRUTAMIENTO</div>
          <div class="card-title">EL GATING ROUTER Y LOS 256 EXPERTOS</div>
        </div>
        <div class="card-tag" style="border-color:#a855f7; color:#a855f7;">TOP-8 DYNAMIC DISPATCH</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">FLUJO DE TOKEN A TRAVÉS DEL ENRUTADOR DINÁMICO</text>

          <!-- TOKEN ENTRANTE (PARTÍCULA ANIMADA) -->
          <g transform="translate(470, 150)">
            <rect x="-135" y="-30" width="270" height="60" rx="14" fill="#1e1b4b" stroke="#38bdf8" stroke-width="3"/>
            <text x="0" y="8" text-anchor="middle" fill="#38bdf8" font-family="'Montserrat'" font-size="20" font-weight="900">TOKEN: "def solve()"</text>
            <!-- Línea de flujo hacia el Router -->
            <line x1="0" y1="30" x2="0" y2="120" stroke="#38bdf8" stroke-width="4" stroke-dasharray="10 5" style="animation: tokenStream 1s linear infinite;" />
          </g>

          <!-- RÁFAGAS LÁSER HACIA LOS EXPERTOS ACTIVADOS -->
          <!-- Línea a Experto 1 (Python) -> ACTIVO -->
          <line x1="405" y1="350" x2="260" y2="350" stroke="#10b981" stroke-width="5" stroke-dasharray="20 10" style="animation: tokenStream 0.6s linear infinite;"/>
          
          <!-- Línea a Experto 2 (Lógica Math) -> ACTIVO -->
          <line x1="440" y1="410" x2="260" y2="560" stroke="#10b981" stroke-width="5" stroke-dasharray="20 10" style="animation: tokenStream 0.7s linear infinite;"/>

          <!-- Líneas a Expertos Inactivos (apagadas/punteadas) -->
          <line x1="535" y1="350" x2="680" y2="350" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5 5" opacity="0.35"/>
          <line x1="500" y1="410" x2="680" y2="560" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5 5" opacity="0.35"/>

          <!-- NÚCLEO CENTRAL DEL GATING ROUTER (HEXÁGONO PULSANTE CENTRADO) -->
          <g transform="translate(470, 350)">
            <g style="animation: routerPulse 2s ease-in-out infinite; transform-box: fill-box; transform-origin: center;">
              <polygon points="0,-75 65,-37 65,37 0,75 -65,37 -65,-37" fill="#090d1a" stroke="#a855f7" stroke-width="4" />
              <circle cx="0" cy="0" r="30" fill="#a855f7" opacity="0.3"/>
              <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="16" font-weight="900">GATING</text>
              <text x="0" y="16" text-anchor="middle" fill="#c084fc" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">ROUTER</text>
              <text x="0" y="36" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="11">SOFTMAX</text>
            </g>
          </g>

          <!-- PODS DE EXPERTOS ESPECIALIZADOS -->
          <!-- EXPERTO 1: PYTHON & CODE (ENCENDIDO EN VERDE) -->
          <g transform="translate(60, 300)">
            <rect width="200" height="100" rx="14" fill="#061f18" stroke="#10b981" stroke-width="3" style="filter: drop-shadow(0 0 16px rgba(16, 185, 129, 0.4));"/>
            <text x="100" y="38" text-anchor="middle" fill="#10b981" font-family="'Montserrat'" font-size="16" font-weight="900">🐍 EXPERT #14</text>
            <text x="100" y="62" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13">PYTHON SYNTAX</text>
            <rect x="25" y="74" width="150" height="16" rx="4" fill="#10b981"/>
            <text x="100" y="86" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="10" font-weight="bold">WEIGHT: 0.84 (TOP-1)</text>
          </g>

          <!-- EXPERTO 2: MATH & LOGIC (ENCENDIDO EN CYAN) -->
          <g transform="translate(160, 560)">
            <rect width="200" height="100" rx="14" fill="#031d2e" stroke="#38bdf8" stroke-width="3" style="filter: drop-shadow(0 0 16px rgba(56, 189, 248, 0.4));"/>
            <text x="100" y="38" text-anchor="middle" fill="#38bdf8" font-family="'Montserrat'" font-size="16" font-weight="900">📐 EXPERT #89</text>
            <text x="100" y="62" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13">ALGORITHMIC LOGIC</text>
            <rect x="25" y="74" width="150" height="16" rx="4" fill="#38bdf8"/>
            <text x="100" y="86" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="10" font-weight="bold">WEIGHT: 0.14 (TOP-2)</text>
          </g>

          <!-- EXPERTO 3: MEDICINA (DURMIENDO) -->
          <g transform="translate(680, 300)" opacity="0.35">
            <rect width="200" height="100" rx="14" fill="#0f172a" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6 4"/>
            <text x="100" y="42" text-anchor="middle" fill="#94a3b8" font-family="'Montserrat'" font-size="16">🧬 EXPERT #03</text>
            <text x="100" y="68" text-anchor="middle" fill="#64748b" font-family="'JetBrains Mono'" font-size="12">BIOMEDICAL (SLEEP)</text>
          </g>

          <!-- EXPERTO 4: HISTORIA (DURMIENDO) -->
          <g transform="translate(580, 560)" opacity="0.35">
            <rect width="200" height="100" rx="14" fill="#0f172a" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6 4"/>
            <text x="100" y="42" text-anchor="middle" fill="#94a3b8" font-family="'Montserrat'" font-size="16">📜 EXPERT #42</text>
            <text x="100" y="68" text-anchor="middle" fill="#64748b" font-family="'JetBrains Mono'" font-size="12">HISTORY (SLEEP)</text>
          </g>

          <!-- PANEL TÉCNICO INFERIOR -->
          <g transform="translate(70, 780)">
            <rect width="800" height="340" rx="18" fill="rgba(15, 23, 42, 0.9)" stroke="#a855f7" stroke-width="2" />
            <text x="40" y="45" fill="#a855f7" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">ARQUITECTURA DE ENRUTAMIENTO DEEPSEEK-V3</text>
            <line x1="40" y1="65" x2="760" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <text x="40" y="110" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Total de Expertos Ruteados:</text>
            <text x="450" y="110" fill="#c084fc" font-family="'JetBrains Mono'" font-size="17" font-weight="bold">256 Expertos Discretos</text>

            <text x="40" y="160" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Expertos Compartidos (Shared):</text>
            <text x="450" y="160" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="17" font-weight="bold">1 Experto Base Siempre Activo</text>

            <text x="40" y="210" fill="#94a3b8" font-family="'Space Grotesk'" font-size="17">Activación Dinámica por Token:</text>
            <text x="450" y="210" fill="#10b981" font-family="'JetBrains Mono'" font-size="17" font-weight="bold">Top-8 Expertos Seleccionados</text>

            <rect x="40" y="245" width="720" height="70" rx="10" fill="rgba(168, 85, 247, 0.15)" stroke="#a855f7" stroke-width="1.5" />
            <text x="400" y="275" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="15" font-weight="900">BALANCEO DE CARGA SIN PÉRDIDA AUXILIAR (AUX-LOSS-FREE)</text>
            <text x="400" y="300" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">Ningún experto sufre cuellos de botella; la carga se reparte con sesgo dinámico.</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 3: MULTI-HEAD LATENT ATTENTION (MLA) Y COMPRESIÓN KV -->
    <div class="scene-card" id="card-3">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 03 • EFICIENCIA EN MEMORIA</div>
          <div class="card-title">LATENT ATTENTION (MLA) Y COMPRESIÓN KV</div>
        </div>
        <div class="card-tag" style="border-color:#10b981; color:#10b981;">-93.3% VRAM FOOTPRINT</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">PROYECCIÓN DE MATRIZ DE ATENCIÓN LATENTE</text>

          <!-- COMPARATIVA: TRADICIONAL MHA (GIGANTE) VS MLA COMPRIMIDO -->
          <!-- MATRIZ TRADICIONAL (128 GB) -->
          <g transform="translate(60, 120)">
            <rect width="350" height="340" rx="16" fill="rgba(239, 68, 68, 0.08)" stroke="#ef4444" stroke-width="2"/>
            <text x="175" y="45" text-anchor="middle" fill="#ef4444" font-family="'Montserrat'" font-size="18" font-weight="900">MHA TRADICIONAL</text>
            <text x="175" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">Multi-Head Attention Clásico</text>
            
            <rect x="30" y="105" width="290" height="160" rx="8" fill="#1e1b4b" stroke="#f87171" stroke-width="1.5" stroke-dasharray="4 4"/>
            <text x="175" y="160" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="14">KV CACHE COMPLETO</text>
            <text x="175" y="190" text-anchor="middle" fill="#ef4444" font-family="'Montserrat'" font-size="32" font-weight="900">128 GB</text>
            <text x="175" y="220" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="12">DESBORDA MEMORIA HBM</text>

            <rect x="30" y="285" width="290" height="35" rx="6" fill="#ef4444"/>
            <text x="175" y="308" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="12" font-weight="bold">REQUIERE 8+ SERVIDORES H100</text>
          </g>

          <!-- EMBUDO DE COMPRESIÓN VECTORIAL (ANIMADO) -->
          <g transform="translate(470, 290)">
            <!-- Embudo SVG -->
            <polygon points="-25,-70 25,-70 12,50 -12,50" fill="rgba(56, 189, 248, 0.2)" stroke="#38bdf8" stroke-width="3" style="animation: funnelSqueeze 1.5s ease-in-out infinite; transform-origin: 0px 0px;"/>
            <text x="0" y="90" text-anchor="middle" fill="#38bdf8" font-family="'Montserrat'" font-size="13" font-weight="900">PROYECCIÓN</text>
            <text x="0" y="110" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="11">LATENTE MLA</text>
          </g>

          <!-- MATRIZ COMPRIMIDA MLA DEEPSEEK (8.5 GB) -->
          <g transform="translate(530, 120)">
            <rect width="350" height="340" rx="16" fill="rgba(16, 185, 129, 0.08)" stroke="#10b981" stroke-width="2.5"/>
            <text x="175" y="45" text-anchor="middle" fill="#10b981" font-family="'Montserrat'" font-size="18" font-weight="900">DEEPSEEK MLA</text>
            <text x="175" y="75" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="13">Multi-Head Latent Attention</text>

            <rect x="65" y="125" width="220" height="120" rx="8" fill="#061f18" stroke="#10b981" stroke-width="2"/>
            <text x="175" y="160" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="13">VECTOR LATENTE (c_t)</text>
            <text x="175" y="195" text-anchor="middle" fill="#10b981" font-family="'Montserrat'" font-size="34" font-weight="900">8.5 GB</text>
            <text x="175" y="225" text-anchor="middle" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="12">REDUCCIÓN DEL 93.3%</text>

            <rect x="30" y="285" width="290" height="35" rx="6" fill="#10b981"/>
            <text x="175" y="308" text-anchor="middle" fill="#000" font-family="'Montserrat'" font-size="12" font-weight="900">CABE EN TARJETAS COMERCIALES</text>
          </g>

          <!-- MATRIZ DE DECODIFICACIÓN EN VIVO (CÓDIGO PROCEDURAL FLOTANTE) -->
          <g transform="translate(60, 520)">
            <rect width="820" height="580" rx="18" fill="rgba(15, 23, 42, 0.95)" stroke="#10b981" stroke-width="2" />
            <text x="40" y="45" fill="#10b981" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">DESCOMPRESIÓN ON-THE-FLY Y RoPE DESACOPLADO</text>
            <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <!-- Explicación visual de RoPE desacoplado -->
            <g transform="translate(40, 100)">
              <rect width="740" height="105" rx="10" fill="#090d1a" stroke="#38bdf8" stroke-width="1.5"/>
              <text x="25" y="34" fill="#38bdf8" font-family="'Montserrat'" font-size="16" font-weight="bold">DESACOPLAMIENTO DE POSICIÓN ROTACIONAL (RoPE)</text>
              <text x="25" y="62" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">La posición de los tokens se procesa en un canal independiente de baja dimensión,</text>
              <text x="25" y="86" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">comprimiendo el contenido semántico sin perder la noción del orden de las palabras.</text>
            </g>

            <!-- Ticker de Ahorro VRAM en Concurrencia -->
            <g transform="translate(40, 235)">
              <text x="0" y="30" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="bold">Ahorro para 100 Usuarios Simultáneos:</text>
              <text x="0" y="70" fill="#f87171" font-family="'JetBrains Mono'" font-size="16">MHA Estándar: 1,280 GB VRAM (16 GPUs H100)</text>
              <text x="0" y="105" fill="#10b981" font-family="'JetBrains Mono'" font-size="16" font-weight="bold">DeepSeek MLA: 85 GB VRAM (1 Sola GPU H100 / A100)</text>
            </g>

            <rect x="40" y="380" width="740" height="150" rx="12" fill="rgba(16, 185, 129, 0.12)" stroke="#10b981" stroke-width="2"/>
            <text x="410" y="425" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="900">DEMOCRATIZACIÓN TOTAL DE LA INFERENCIA</text>
            <text x="410" y="465" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">El costo por millón de tokens en DeepSeek se desplomó a menos de $0.27 USD,</text>
            <text x="410" y="495" text-anchor="middle" fill="#10b981" font-family="'JetBrains Mono'" font-size="13.5" font-weight="bold">frente a los $5.00 a $15.00 USD cobrados por las APIs propietarias estadounidenses.</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 4: PRECISIÓN FP8, DUALPIPE Y EL COLAPSO EN WALL STREET -->
    <div class="scene-card" id="card-4">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 04 • HARDWARE & ECONOMÍA</div>
          <div class="card-title">PRECISIÓN FP8 Y EL COLAPSO EN WALL STREET</div>
        </div>
        <div class="card-tag" style="border-color:#f43f5e; color:#f43f5e;">-$600 BILLONES NVIDIA</div>
      </div>
      <div class="canvas-viewport">
        <svg viewBox="0 0 940 1180" width="940" height="1180" style="background:#02050e;">
          <defs>
            <clipPath id="dualPipeClip">
              <rect x="0" y="0" width="740" height="45" rx="8"/>
            </clipPath>
          </defs>
          <text x="470" y="65" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="16" letter-spacing="3">EL EFECTO DEEPSEEK EN LOS MERCADOS GLOBALES</text>

          <!-- GRÁFICA DE COLAPSO BURSÁTIL DE NVIDIA (ENERO 2025) -->
          <g transform="translate(60, 110)">
            <rect width="820" height="380" rx="18" fill="rgba(2, 6, 23, 0.95)" stroke="#f43f5e" stroke-width="2" />
            <text x="35" y="45" fill="#f43f5e" font-family="'Montserrat'" font-size="22" font-weight="900">📉 NVDA (NVIDIA CORP): -$600,000,000,000 USD (24 HORAS)</text>
            <line x1="35" y1="65" x2="785" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <!-- Curva de colapso bursátil animada -->
            <path d="M 60 140 Q 200 130 320 145 T 440 150 L 520 220 L 620 310 L 740 330" fill="none" stroke="#f43f5e" stroke-width="5" stroke-dasharray="20 10" style="animation: marketCrashLine 2s linear infinite;" />

            <!-- Puntos de caída -->
            <circle cx="440" cy="150" r="8" fill="#eab308" />
            <text x="360" y="130" fill="#eab308" font-family="'JetBrains Mono'" font-size="13" font-weight="bold">LANZAMIENTO R1 / V3</text>

            <circle cx="620" cy="310" r="10" fill="#f43f5e" />
            <text x="540" y="300" fill="#f43f5e" font-family="'Montserrat'" font-size="14" font-weight="900">CAÍDA HISTÓRICA -17%</text>

            <!-- Ticker digital Wall Street -->
            <g transform="translate(560, 95)">
              <rect width="220" height="70" rx="10" fill="#090d1a" stroke="#f43f5e" stroke-width="2"/>
              <text x="110" y="28" text-anchor="middle" fill="#94a3b8" font-family="'JetBrains Mono'" font-size="12">MARKET CAP WIPEOUT</text>
              <text x="110" y="55" text-anchor="middle" fill="#f43f5e" font-family="'Montserrat'" font-size="22" font-weight="900">-$590B USD</text>
            </g>
          </g>

          <!-- DUALPIPE: SOLAPAMIENTO DE CÓMPUTO Y COMUNICACIÓN -->
          <g transform="translate(60, 520)">
            <rect width="820" height="580" rx="18" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" stroke-width="2" />
            <text x="40" y="45" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="18" font-weight="bold">DUALPIPE Y OPTIMIZACIÓN EN HARDWARE (FP8)</text>
            <line x1="40" y1="65" x2="780" y2="65" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>

            <!-- Bloques DualPipe en traslación continua -->
            <text x="40" y="105" fill="#fff" font-family="'Montserrat'" font-size="17" font-weight="bold">Solapamiento Total (Cero Burbujas de Espera):</text>
            
            <g transform="translate(40, 130)">
              <!-- Timeline Forward (Compute) -->
              <rect x="0" y="0" width="740" height="45" rx="8" fill="#090d1a" stroke="#38bdf8" stroke-width="1.5"/>
              <g clip-path="url(#dualPipeClip)">
                <g style="animation: dualPipeLoop 2s linear infinite;">
                  <rect x="20" y="6" width="130" height="33" rx="6" fill="#38bdf8"/>
                  <text x="85" y="27" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">COMPUTE FWD</text>

                  <rect x="180" y="6" width="130" height="33" rx="6" fill="#a855f7"/>
                  <text x="245" y="27" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">ALL-TO-ALL</text>

                  <rect x="340" y="6" width="130" height="33" rx="6" fill="#38bdf8"/>
                  <text x="405" y="27" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">COMPUTE FWD</text>

                  <rect x="500" y="6" width="130" height="33" rx="6" fill="#a855f7"/>
                  <text x="565" y="27" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">ALL-TO-ALL</text>

                  <rect x="660" y="6" width="130" height="33" rx="6" fill="#38bdf8"/>
                  <text x="725" y="27" text-anchor="middle" fill="#000" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">COMPUTE FWD</text>

                  <rect x="820" y="6" width="130" height="33" rx="6" fill="#a855f7"/>
                  <text x="885" y="27" text-anchor="middle" fill="#fff" font-family="'JetBrains Mono'" font-size="12" font-weight="bold">ALL-TO-ALL</text>
                </g>
              </g>
            </g>

            <!-- Comparativa FP8 vs FP16 -->
            <g transform="translate(40, 210)">
              <rect width="740" height="135" rx="12" fill="#090d1a" stroke="#10b981" stroke-width="1.5"/>
              <text x="25" y="34" fill="#10b981" font-family="'Montserrat'" font-size="17" font-weight="bold">FORMATO NATIVO FP8 (E4M3): 2X DE ANCHO DE BANDA</text>
              <text x="25" y="62" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">Los pesos se calculan en 8 bits usando factores de escala por bloque de 1x128,</text>
              <text x="25" y="86" fill="#94a3b8" font-family="'Space Grotesk'" font-size="15">reduciendo a la mitad el tráfico de red sin perder precisión matemática.</text>
              <text x="25" y="116" fill="#fff" font-family="'JetBrains Mono'" font-size="14" font-weight="bold">Infraestructura: 2,048 GPUs H800 &bull; Costo total: $5.58M USD</text>
            </g>

            <rect x="40" y="375" width="740" height="160" rx="12" fill="rgba(244, 63, 94, 0.12)" stroke="#f43f5e" stroke-width="2"/>
            <text x="410" y="420" text-anchor="middle" fill="#fff" font-family="'Montserrat'" font-size="20" font-weight="900">EL FIN DE LA BURBUJA DE FUERZA BRUTA</text>
            <text x="410" y="460" text-anchor="middle" fill="#94a3b8" font-family="'Space Grotesk'" font-size="16">DeepSeek demostró que los algoritmos ingeniosos superan a la compra masiva de silicio.</text>
            <text x="410" y="495" text-anchor="middle" fill="#38bdf8" font-family="'JetBrains Mono'" font-size="15" font-weight="bold">La soberanía de la IA regresó a los desarrolladores y al software libre.</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ACTO 5: COMUNIDAD ABIERTA Y TU PROPUESTA DE TEMA -->
    <div class="scene-card" id="card-5">
      <div class="card-topbar">
        <div class="card-title-group">
          <div class="card-act-num">ACTO 05 • COMUNIDAD ABIERTA</div>
          <div class="card-title">TÚ PROPONES EL PRÓXIMO CAPÍTULO</div>
        </div>
        <div class="card-tag" style="border-color:#eab308; color:#eab308;">BUZÓN 100% ABIERTO</div>
      </div>
      <div class="canvas-viewport" style="display:flex; flex-direction:column; padding:24px; gap:20px;">

        <!-- TARJETA SUPERIOR: EL TRIUNFO DEL SOFTWARE LIBRE -->
        <div style="background:#090d1a; border:1.5px solid #10b981; border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:13px; color:#10b981; letter-spacing:1px; font-weight:800;">DEEPSEEK-R1 & V3 LICENCIA MIT OPEN SOURCE</div>
            <div style="font-family:'Montserrat',sans-serif; font-size:22px; font-weight:900; color:#fff; margin-top:4px;">CÓDIGO, PESOS Y ARQUITECTURA PÚBLICOS</div>
            <div style="font-size:14px; color:#94a3b8; margin-top:4px;">Cualquiera puede descargarlo, ejecutarlo y auditarlo en hardware local sin permisos de Silicon Valley.</div>
          </div>
          <div style="background:#10b981; color:#000; font-family:'Montserrat',sans-serif; font-weight:900; font-size:16px; padding:10px 18px; border-radius:8px; box-shadow:0 0 20px rgba(16,185,129,0.5);">
            LIBRE / LOCAL
          </div>
        </div>

        <!-- BUZÓN COMUNITARIO 100% ABIERTO -->
        <div style="flex:1; background:#020610; border:2px solid #eab308; border-radius:18px; padding:24px; display:flex; flex-direction:column; justify-content:space-evenly; box-shadow:0 0 35px rgba(234,179,8,0.15);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="font-family:'Montserrat',sans-serif; font-size:24px; font-weight:900; color:#eab308; display:flex; align-items:center; gap:10px;">
                🎙️ LA MESA ESTÁ ABIERTA: ¿QUÉ CASO INVESTIGAMOS?
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:13px; background:rgba(234,179,8,0.15); color:#eab308; padding:4px 12px; border-radius:999px; font-weight:bold;">¡COMENTA AQUÍ!</div>
            </div>
            <div style="font-size:16px; color:#94a3b8; margin-top:6px;">No importa qué tan complejo, oscuro o disruptivo sea: tú lo propones y nosotros lo creamos en código animado.</div>
          </div>

          <div style="display:flex; flex-direction:column; gap:12px;">
            <!-- Categoría 1 -->
            <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(56,189,248,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#38bdf8; color:#000; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">💻</div>
                <div>
                  <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">UN FALLO DE CÓDIGO O BUG CATASTRÓFICO</div>
                  <div style="font-size:13px; color:#94a3b8;">Sistemas críticos, desbordamientos de enteros, desastres espaciales o colapsos de trading.</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#38bdf8; font-size:14px;">#SoftwareFail</div>
            </div>

            <!-- Categoría 2 -->
            <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(244,63,94,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#f43f5e; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">🏢</div>
                <div>
                  <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">UNA GUERRA CORPORATIVA O FRAUDE INDUSTRIAL</div>
                  <div style="font-size:13px; color:#94a3b8;">Litigios épicos (Nintendo vs Universal, Theranos, espionaje corporativo de chips).</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#f43f5e; font-size:14px;">#TechDrama</div>
            </div>

            <!-- Categoría 3 -->
            <div style="background:rgba(255,255,255,0.04); border:1.5px solid rgba(168,85,247,0.4); border-radius:12px; padding:14px 20px; display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#a855f7; color:#fff; font-family:'Montserrat',sans-serif; font-weight:900; font-size:18px; display:flex; align-items:center; justify-content:center;">🧠</div>
                <div>
                  <div style="font-family:'Montserrat',sans-serif; font-weight:800; font-size:18px; color:#fff;">UN AVANCE CIENTÍFICO O REVOLUCIÓN DE HARDWARE</div>
                  <div style="font-size:13px; color:#94a3b8;">Computación cuántica, chips fotónicos, robótica o nuevas arquitecturas de frontera.</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-weight:bold; color:#a855f7; font-size:14px;">#DeepTech</div>
            </div>
          </div>

          <div style="text-align:center; font-family:'Space Grotesk',sans-serif; font-size:16px; color:#eab308; font-weight:bold; background:rgba(234,179,8,0.08); padding:12px; border-radius:8px;">
            💬 Déjanos en los comentarios tu propuesta. El comentario con más apoyo será el próximo capítulo maestro.
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

target_path = Path("sia_tiktok_batch_engine/compositions/moe_scene.html")
target_path.parent.mkdir(parents=True, exist_ok=True)
with open(target_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Escena MoE generada exitosamente en {target_path}")
