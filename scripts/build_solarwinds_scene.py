import json

with open("scratch/solarwinds_timestamps.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

TOTAL_DUR = 271.66

# Acts definition
ACTS = [
    {"num": 1, "start": 0.0, "end": 43.4, "title": "EL CABALLO DE TROYA", "tag": "ORION PLATFORM 2020.2.1"},
    {"num": 2, "start": 43.4, "end": 108.6, "title": "INYECCIÓN EN RAM", "tag": "MSBUILD & SOLORIGATE"},
    {"num": 3, "start": 108.6, "end": 166.0, "title": "DNS FANTASMA Y TEARDROP", "tag": "14 DÍAS DE HIBERNACIÓN"},
    {"num": 4, "start": 166.0, "end": 217.0, "title": "EL DETALLE HUMANO", "tag": "ALERTA 2FA FIREEYE"},
    {"num": 5, "start": 217.0, "end": 271.66, "title": "TÚ DECIDES EL CAPÍTULO #11", "tag": "ENCUESTA COMUNITARIA"}
]

# Generate card keyframe CSS
cards_css = []
for act in ACTS:
    s_pct = (act["start"] / TOTAL_DUR) * 100
    e_pct = (act["end"] / TOTAL_DUR) * 100
    num = act["num"]
    fade_in = max(0.0, s_pct - 0.2)
    fade_out = min(100.0, e_pct + 0.2)
    
    if num == 1:
        css = f"""
        @keyframes scene1Anim {{
          0% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
          {e_pct - 0.1:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
          {e_pct:.3f}%, 100% {{ opacity: 0; transform: scale(0.96); z-index: 0; pointer-events: none; }}
        }}"""
    elif num == 5:
        css = f"""
        @keyframes scene5Anim {{
          0%, {s_pct - 0.1:.3f}% {{ opacity: 0; transform: scale(0.96); z-index: 0; pointer-events: none; }}
          {s_pct:.3f}%, 100% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
        }}"""
    else:
        css = f"""
        @keyframes scene{num}Anim {{
          0%, {s_pct - 0.1:.3f}% {{ opacity: 0; transform: scale(0.96); z-index: 0; pointer-events: none; }}
          {s_pct:.3f}%, {e_pct - 0.1:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
          {e_pct:.3f}%, 100% {{ opacity: 0; transform: scale(0.96); z-index: 0; pointer-events: none; }}
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
          {s_pct:.3f}%, 100% {{ background: {col}; color: #000; border-color: #fff; box-shadow: 0 0 20px {col}; transform: scale(1.08); animation: c5Pulse 1.2s infinite alternate; }}
        }}"""
    else:
        css = f"""
        @keyframes c{num}Anim {{
          0%, {s_pct - 0.1:.3f}% {{ background: rgba(255,255,255,0.06); color: #94a3b8; border-color: rgba(255,255,255,0.12); transform: scale(1); }}
          {s_pct:.3f}%, {e_pct - 0.1:.3f}% {{ background: {col}; color: #000; border-color: #fff; box-shadow: 0 0 16px {col}; transform: scale(1.05); }}
          {e_pct:.3f}%, 100% {{ background: rgba(255,255,255,0.06); color: #94a3b8; border-color: rgba(255,255,255,0.12); transform: scale(1); }}
        }}"""
    chap_css.append(css)

# Generate subtitle segments HTML & CSS
sub_html = []
sub_css = []
for idx, s in enumerate(segments):
    s_pct = (s["start"] / TOTAL_DUR) * 100
    e_pct = (s["end"] / TOTAL_DUR) * 100
    voice = s["voice"]
    pill_color = "#38bdf8" if voice == "Jorge" else "#10b981"
    
    # Subtitle HTML
    sub_html.append(f"""
    <div class="sub-line" id="sub-{idx}">
      <span class="sub-speaker" style="color: {pill_color};">[{voice.upper()}]</span>
      <span class="sub-text">{s['text']}</span>
    </div>""")
    
    # Subtitle CSS
    sub_css.append(f"""
    #sub-{idx} {{ animation: subAnim_{idx} {TOTAL_DUR}s linear forwards; }}
    @keyframes subAnim_{idx} {{
      0%, {max(0, s_pct - 0.08):.3f}% {{ opacity: 0; transform: translateY(6px); display: none; }}
      {s_pct:.3f}%, {max(0, e_pct - 0.08):.3f}% {{ opacity: 1; transform: translateY(0); display: block; }}
      {e_pct:.3f}%, 100% {{ opacity: 0; transform: translateY(-6px); display: none; }}
    }}""")

# Generate Avatar active/inactive spotlight CSS
# When Jorge speaks, Jorge is 1.0, Dalia is 0.55. When Dalia speaks, Dalia is 1.0, Jorge is 0.55.
# Let's create keyframe for Jorge and Dalia
jorge_keyframes = []
dalia_keyframes = []

# We calculate keyframe intervals for avatar spotlight
for s in segments:
    s_pct = (s["start"] / TOTAL_DUR) * 100
    e_pct = (s["end"] / TOTAL_DUR) * 100
    if s["voice"] == "Jorge":
        jorge_keyframes.append(f"{s_pct:.3f}% {{ opacity: 1; transform: scale(1) translateY(0); filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.6)); }}")
        jorge_keyframes.append(f"{e_pct - 0.05:.3f}% {{ opacity: 1; transform: scale(1) translateY(0); filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.6)); }}")
        dalia_keyframes.append(f"{s_pct:.3f}% {{ opacity: 0.55; transform: scale(0.94) translateY(12px); filter: grayscale(40%); }}")
        dalia_keyframes.append(f"{e_pct - 0.05:.3f}% {{ opacity: 0.55; transform: scale(0.94) translateY(12px); filter: grayscale(40%); }}")
    else:
        dalia_keyframes.append(f"{s_pct:.3f}% {{ opacity: 1; transform: scale(1) translateY(0); filter: drop-shadow(0 0 20px rgba(16, 185, 129, 0.6)); }}")
        dalia_keyframes.append(f"{e_pct - 0.05:.3f}% {{ opacity: 1; transform: scale(1) translateY(0); filter: drop-shadow(0 0 20px rgba(16, 185, 129, 0.6)); }}")
        jorge_keyframes.append(f"{s_pct:.3f}% {{ opacity: 0.55; transform: scale(0.94) translateY(12px); filter: grayscale(40%); }}")
        jorge_keyframes.append(f"{e_pct - 0.05:.3f}% {{ opacity: 0.55; transform: scale(0.94) translateY(12px); filter: grayscale(40%); }}")

jorge_spotlight_css = f"""
@keyframes jorgeSpotlight {{
  {" ".join(jorge_keyframes)}
}}
"""
dalia_spotlight_css = f"""
@keyframes daliaSpotlight {{
  {" ".join(dalia_keyframes)}
}}
"""

html_content = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Crónicas #10 - SolarWinds SUNBURST</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@600;700;800&family=JetBrains+Mono:wght@700;800;900&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #060911;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}
      .cyber-grid {{
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(56, 189, 248, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(56, 189, 248, 0.06) 1px, transparent 1px);
        background-size: 40px 40px;
        z-index: 1;
        pointer-events: none;
      }}
      .cyber-scanlines {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          0deg,
          rgba(0, 0, 0, 0.15) 0px,
          rgba(0, 0, 0, 0.15) 2px,
          transparent 2px,
          transparent 4px
        );
        z-index: 2;
        pointer-events: none;
      }}
      .bg-ticker {{
        position: absolute;
        width: 120%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 78px;
        color: rgba(56, 189, 248, 0.04);
        text-transform: uppercase;
        transform: rotate(-10deg) scale(1.3);
        top: 20%;
        left: -10%;
        z-index: 0;
        line-height: 1.1;
      }}
      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 60px 48px 45px 48px;
      }}
      
      /* HEADER */
      .header-box {{ display: flex; flex-direction: column; gap: 12px; }}
      .brand-row {{ display: flex; align-items: center; justify-content: space-between; }}
      .brand-pill {{
        background: #38bdf8;
        color: #030712;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 23px;
        padding: 8px 22px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(56, 189, 248, 0.12);
        color: #7dd3fc;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 20px;
        padding: 6px 18px;
        border-radius: 9999px;
        border: 1px solid rgba(56, 189, 248, 0.35);
      }}
      .title-hero {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 40px;
        line-height: 1.12;
        letter-spacing: -1.2px;
        color: #ffffff;
      }}
      .title-hero span {{ color: #38bdf8; }}
      
      .chapters-bar {{
        display: flex;
        gap: 6px;
        width: 100%;
        margin-top: 4px;
      }}
      .chapter-pill {{
        flex: 1;
        text-align: center;
        padding: 8px 2px;
        border-radius: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 15px;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.06);
        color: #94a3b8;
      }}
      
      #chap-1 {{ animation: c1Anim {TOTAL_DUR}s linear forwards; }}
      #chap-2 {{ animation: c2Anim {TOTAL_DUR}s linear forwards; }}
      #chap-3 {{ animation: c3Anim {TOTAL_DUR}s linear forwards; }}
      #chap-4 {{ animation: c4Anim {TOTAL_DUR}s linear forwards; }}
      #chap-5 {{ animation: c5Anim {TOTAL_DUR}s linear forwards; }}
      
      {' '.join(chap_css)}
      
      @keyframes c5Pulse {{
        0% {{ box-shadow: 0 0 10px #10b981; transform: scale(1.05); }}
        100% {{ box-shadow: 0 0 25px #34d399; transform: scale(1.1); }}
      }}
      
      /* TOP SHOWCASE WINDOW (UPPER 50%) */
      .showcase-stage {{
        position: relative;
        width: 100%;
        height: 980px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
      }}
      .card-layer {{
        position: absolute;
        inset: 0;
        background: #0b1120;
        border-radius: 30px;
        padding: 28px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.85);
        border: 4px solid #38bdf8;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}
      
      #card-1 {{ animation: scene1Anim {TOTAL_DUR}s linear forwards; border-color: #38bdf8; }}
      #card-2 {{ animation: scene2Anim {TOTAL_DUR}s linear forwards; border-color: #f43f5e; }}
      #card-3 {{ animation: scene3Anim {TOTAL_DUR}s linear forwards; border-color: #a855f7; }}
      #card-4 {{ animation: scene4Anim {TOTAL_DUR}s linear forwards; border-color: #eab308; }}
      #card-5 {{ animation: scene5Anim {TOTAL_DUR}s linear forwards; border-color: #10b981; }}
      
      {' '.join(cards_css)}
      
      .myth-tag {{
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 18px;
        padding: 6px 16px;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}
      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 36px;
        line-height: 1.15;
        letter-spacing: -0.8px;
        color: #f8fafc;
        margin-top: 8px;
      }}
      
      .canvas-graphic-box {{
        width: 100%;
        height: 480px;
        border-radius: 20px;
        background: #030712;
        border: 2px solid #1e293b;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 16px;
      }}
      
      .punch-pill {{
        display: inline-block;
        align-self: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 12px;
        line-height: 1.2;
        border: 2px solid #fff;
        text-align: center;
      }}
      .metric-box {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        background: #0f172a;
        border: 2px dashed #334155;
        border-radius: 16px;
        padding: 14px 18px;
      }}
      
      /* SUBTITLES ZONE (MIDDLE 12%) */
      .subtitles-box {{
        position: relative;
        width: 100%;
        min-height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(15, 23, 42, 0.75);
        border: 2px solid rgba(56, 189, 248, 0.3);
        border-radius: 18px;
        padding: 12px 24px;
        margin: 8px 0;
        backdrop-filter: blur(10px);
      }}
      .sub-line {{
        position: absolute;
        width: 92%;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 28px;
        line-height: 1.25;
        color: #ffffff;
      }}
      .sub-speaker {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        margin-right: 8px;
      }}
      
      {' '.join(sub_css)}
      
      /* BOTTOM STAGE: HOST AVATARS (LOWER 28%) */
      .hosts-stage {{
        position: relative;
        width: 100%;
        height: 380px;
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
        padding: 0 40px;
      }}
      
      .host-card {{
        position: relative;
        width: 320px;
        height: 380px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        transition: all 0.3s ease;
      }}
      
      .host-img {{
        width: 300px;
        height: auto;
        max-height: 360px;
        object-fit: contain;
        display: block;
        animation: idleBreathe 3s ease-in-out infinite alternate;
      }}
      
      @keyframes idleBreathe {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-7px); }}
      }}
      
      #host-jorge {{
        animation: jorgeSpotlight {TOTAL_DUR}s linear forwards;
      }}
      #host-dalia {{
        animation: daliaSpotlight {TOTAL_DUR}s linear forwards;
      }}
      
      {jorge_spotlight_css}
      {dalia_spotlight_css}
      
      /* FOOTER PROGRESS */
      .footer-box {{
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 8px;
      }}
      .omnicanal-bar {{ display: flex; gap: 14px; justify-content: center; width: 100%; }}
      .omni-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 17px;
        padding: 8px 16px;
        border-radius: 10px;
        background: rgba(255,255,255,0.06);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.18);
      }}
      .progress-bar-container {{
        width: 100%;
        height: 14px;
        background: rgba(255, 255, 255, 0.12);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.25);
      }}
      @keyframes progressFillAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}
      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #f43f5e 35%, #a855f7 65%, #eab308 85%, #10b981 100%);
        width: 0%;
        animation: progressFillAnim {TOTAL_DUR}s linear forwards;
      }}
    </style>
  </head>
  <body>
    <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
      <div class="cyber-grid"></div>
      <div class="cyber-scanlines"></div>
      <div class="bg-ticker">SOLARWINDS &bull; SUNBURST &bull; MSBUILD &bull; PENTÁGONO &bull; TEARDROP &bull; ZERO TRUST</div>

      <div class="reel-wrapper">
        <!-- HEADER -->
        <div class="header-box">
          <div class="brand-row">
            <div class="brand-pill">🛡️ sIA Crónicas #10</div>
            <div class="tag-pill">CIBERESPIONAJE & INGENIERÍA</div>
          </div>

          <div class="chapters-bar">
            <div class="chapter-pill" id="chap-1">01 ORION 2020</div>
            <div class="chapter-pill" id="chap-2">02 COMPILADOR</div>
            <div class="chapter-pill" id="chap-3">03 DNS FANTASMA</div>
            <div class="chapter-pill" id="chap-4">04 FIREEYE</div>
            <div class="chapter-pill" id="chap-5">05 TÚ DECIDES</div>
          </div>

          <div class="title-hero">
            SolarWinds SUNBURST: <span>El Fantasma</span> en el Compilador
          </div>
        </div>

        <!-- TOP SHOWCASE WINDOW (UPPER 50%) -->
        <div class="showcase-stage">
          <!-- ACTO 1: El Caballo de Troya Perfecto -->
          <div class="card-layer" id="card-1">
            <div>
              <div class="myth-tag" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #38bdf8;">01 • MARZO 2020: ACTUALIZACIÓN ORION</div>
              <div class="headline-black">18,000 Redes Infectadas con Certificado Oficial Válido</div>
            </div>

            <!-- Procedural SVG Diagram: Orion Network & Victims -->
            <div class="canvas-graphic-box">
              <svg width="680" height="420" viewBox="0 0 680 420" style="overflow: visible;">
                <defs>
                  <linearGradient id="cyberGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#38bdf8" />
                    <stop offset="100%" stop-color="#0284c7" />
                  </linearGradient>
                  <filter id="glowEffect">
                    <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                    <feMerge>
                      <feMergeNode in="coloredBlur"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
                <!-- Central Node: SolarWinds Orion -->
                <circle cx="340" cy="180" r="65" fill="#0f172a" stroke="#38bdf8" stroke-width="4" filter="url(#glowEffect)" />
                <text x="340" y="165" font-family="Space Grotesk" font-weight="800" font-size="18" fill="#38bdf8" text-anchor="middle">SOLARWINDS</text>
                <text x="340" y="188" font-family="JetBrains Mono" font-weight="900" font-size="15" fill="#f8fafc" text-anchor="middle">ORION 2020.2.1</text>
                <text x="340" y="208" font-family="JetBrains Mono" font-weight="700" font-size="12" fill="#22c55e" text-anchor="middle">✓ SHA-256 SIGNED</text>

                <!-- Connecting Branches -->
                <line x1="340" y1="115" x2="160" y2="60" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4" />
                <line x1="340" y1="115" x2="520" y2="60" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4" />
                <line x1="340" y1="245" x2="140" y2="330" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4" />
                <line x1="340" y1="245" x2="340" y2="340" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4" />
                <line x1="340" y1="245" x2="540" y2="330" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4" />

                <!-- Nodes -->
                <!-- Pentagon -->
                <rect x="80" y="30" width="160" height="60" rx="10" fill="#0f172a" stroke="#f43f5e" stroke-width="2" />
                <text x="160" y="55" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#fff" text-anchor="middle">🏛️ EL PENTÁGONO</text>
                <text x="160" y="75" font-family="JetBrains Mono" font-size="12" fill="#fda4af" text-anchor="middle">Dept. Defensa EE.UU.</text>

                <!-- Los Alamos -->
                <rect x="440" y="30" width="160" height="60" rx="10" fill="#0f172a" stroke="#eab308" stroke-width="2" />
                <text x="520" y="55" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#fff" text-anchor="middle">☢️ LOS ÁLAMOS</text>
                <text x="520" y="75" font-family="JetBrains Mono" font-size="12" fill="#fde047" text-anchor="middle">Laboratorio Nuclear</text>

                <!-- Fortune 500 -->
                <rect x="50" y="300" width="180" height="60" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
                <text x="140" y="325" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#fff" text-anchor="middle">🏢 425 FORTUNE 500</text>
                <text x="140" y="345" font-family="JetBrains Mono" font-size="12" fill="#7dd3fc" text-anchor="middle">Banca y Telecom</text>

                <!-- Dept Estado -->
                <rect x="250" y="315" width="180" height="60" rx="10" fill="#0f172a" stroke="#a855f7" stroke-width="2" />
                <text x="340" y="340" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#fff" text-anchor="middle">🌐 DEPT. ESTADO</text>
                <text x="340" y="360" font-family="JetBrains Mono" font-size="12" fill="#d8b4fe" text-anchor="middle">Comunicaciones</text>

                <!-- Microsoft -->
                <rect x="460" y="300" width="160" height="60" rx="10" fill="#0f172a" stroke="#22c55e" stroke-width="2" />
                <text x="540" y="325" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#fff" text-anchor="middle">☁️ MICROSOFT</text>
                <text x="540" y="345" font-family="JetBrains Mono" font-size="12" fill="#86efac" text-anchor="middle">Azure Cloud Ops</text>
              </svg>
            </div>

            <div class="punch-pill" style="background: #38bdf8; color: #030712;">
              EL CABALLO DE TROYA MÁS GRANDE DE LA HISTORIA
            </div>

            <div class="metric-box">
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #38bdf8; font-weight: 800;">
                🔒 FIRMADO DIGITALMENTE: Certificado oficial de DigiCert/Symantec 100% válido.
              </div>
              <div style="font-size: 18px; color: #94a3b8; font-weight: 700;">
                Ningún antivirus generó alertas. La actualización entró por el canal corporativo legítimo.
              </div>
            </div>
          </div>

          <!-- ACTO 2: La Inyección en el Compilador -->
          <div class="card-layer" id="card-2">
            <div>
              <div class="myth-tag" style="background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid #f43f5e;">02 • INYECCIÓN EN MSBUILD.EXE</div>
              <div class="headline-black">El Código en Git Estaba Limpio: El Malware Nació en la RAM</div>
            </div>

            <!-- Procedural Architecture Diagram: Compiler Injection -->
            <div class="canvas-graphic-box">
              <svg width="680" height="420" viewBox="0 0 680 420">
                <!-- Step 1: GitHub Clean Code -->
                <rect x="30" y="50" width="180" height="110" rx="14" fill="#0f172a" stroke="#22c55e" stroke-width="2" />
                <text x="120" y="85" font-family="Space Grotesk" font-weight="800" font-size="17" fill="#22c55e" text-anchor="middle">1. REPO GITHUB</text>
                <text x="120" y="110" font-family="JetBrains Mono" font-size="13" fill="#86efac" text-anchor="middle">CÓDIGO 100% LIMPIO</text>
                <text x="120" y="135" font-family="JetBrains Mono" font-size="11" fill="#64748b" text-anchor="middle">BusinessLayer.cs</text>

                <!-- Arrow 1 to Compiler -->
                <line x1="210" y1="105" x2="260" y2="105" stroke="#fff" stroke-width="3" marker-end="url(#arrow)" />

                <!-- Step 2: MSBuild in RAM -->
                <rect x="260" y="30" width="200" height="150" rx="14" fill="#0f172a" stroke="#38bdf8" stroke-width="3" />
                <text x="360" y="65" font-family="Space Grotesk" font-weight="800" font-size="17" fill="#38bdf8" text-anchor="middle">2. MSBUILD.EXE</text>
                <text x="360" y="90" font-family="JetBrains Mono" font-size="13" fill="#cbd5e1" text-anchor="middle">Compilación en RAM</text>
                
                <!-- Red Hacker Hook Solorigate -->
                <rect x="280" y="115" width="160" height="50" rx="8" fill="#f43f5e" />
                <text x="360" y="137" font-family="JetBrains Mono" font-weight="900" font-size="12" fill="#fff" text-anchor="middle">⚡ SOLORIGATE HOOK</text>
                <text x="360" y="153" font-family="JetBrains Mono" font-size="10" fill="#fff" text-anchor="middle">+4,000 líneas maliciosas</text>

                <!-- Arrow 2 to Output -->
                <line x1="460" y1="105" x2="510" y2="105" stroke="#fff" stroke-width="3" />

                <!-- Step 3: Envenenado y Firmado -->
                <rect x="510" y="50" width="150" height="110" rx="14" fill="#0f172a" stroke="#f43f5e" stroke-width="2" />
                <text x="585" y="85" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#f43f5e" text-anchor="middle">3. DLL FIRMADA</text>
                <text x="585" y="110" font-family="JetBrains Mono" font-size="12" fill="#fda4af" text-anchor="middle">SUNBURST BACKDOOR</text>
                <text x="585" y="135" font-family="JetBrains Mono" font-size="11" fill="#22c55e" text-anchor="middle">✓ Firma Válida</text>

                <!-- Code Comparison Snippet Box -->
                <rect x="50" y="220" width="580" height="150" rx="12" fill="#090d16" stroke="#334155" stroke-width="2" />
                <text x="70" y="250" font-family="JetBrains Mono" font-weight="900" font-size="15" fill="#f43f5e">💻 SolarWinds.Orion.Core.BusinessLayer.dll:</text>
                <text x="70" y="280" font-family="JetBrains Mono" font-size="13" fill="#64748b">// Función manipulada en tiempo de compilación</text>
                <text x="70" y="305" font-family="JetBrains Mono" font-size="13" fill="#38bdf8">void Update() {{{{ if (CheckTimer() &gt; 14_DAYS) {{{{</text>
                <text x="90" y="330" font-family="JetBrains Mono" font-size="13" fill="#f43f5e">  SpawnThread(DnsBeacon.Resolve()); // Cozy Bear (APT29)</text>
                <text x="70" y="355" font-family="JetBrains Mono" font-size="13" fill="#38bdf8">}}}}}}}}</text>
              </svg>
            </div>

            <div class="punch-pill" style="background: #f43f5e; color: #ffffff;">
              EL CÓDIGO FUENTE NO DEJÓ HUELLA EN EL DISCO
            </div>

            <div class="metric-box">
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #f43f5e; font-weight: 800;">
                🧠 HACKEO AL PROCESO DE COMPILACIÓN: Solorigate vigilaba MSBuild.exe en memoria.
              </div>
              <div style="font-size: 18px; color: #94a3b8; font-weight: 700;">
                Cero modificaciones en Git. El binario salía envenenado y se firmaba automáticamente.
              </div>
            </div>
          </div>

          <!-- ACTO 3: La Hibernación de 14 Días y el DNS Fantasma -->
          <div class="card-layer" id="card-3">
            <div>
              <div class="myth-tag" style="background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid #a855f7;">03 • EVASIÓN DE SANDBOX & STEGANOGRAFÍA</div>
              <div class="headline-black">14 Días de Silencio y Tráfico Camuflado en AWS</div>
            </div>

            <!-- Procedural Diagram: 14 Days & DNS Tunneling -->
            <div class="canvas-graphic-box">
              <svg width="680" height="420" viewBox="0 0 680 420">
                <!-- 14 Day Dormancy Calendar Box -->
                <rect x="40" y="30" width="260" height="140" rx="16" fill="#0f172a" stroke="#a855f7" stroke-width="2" />
                <text x="170" y="65" font-family="Space Grotesk" font-weight="900" font-size="18" fill="#a855f7" text-anchor="middle">⏳ HIBERNACIÓN TOTAL</text>
                <text x="170" y="105" font-family="Montserrat" font-weight="900" font-size="34" fill="#ffffff" text-anchor="middle">14 DÍAS</text>
                <text x="170" y="145" font-family="JetBrains Mono" font-size="12" fill="#94a3b8" text-anchor="middle">Burló análisis de Sandbox</text>

                <!-- DNS Tunneling Visual -->
                <rect x="340" y="30" width="300" height="140" rx="16" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
                <text x="490" y="65" font-family="Space Grotesk" font-weight="800" font-size="17" fill="#38bdf8" text-anchor="middle">📡 ESTEGANOGRAFÍA DNS</text>
                <text x="490" y="98" font-family="JetBrains Mono" font-weight="800" font-size="13" fill="#cbd5e1" text-anchor="middle">Base32 DGA Queries:</text>
                <text x="490" y="125" font-family="JetBrains Mono" font-size="12" fill="#22c55e" text-anchor="middle">*.avsvmcloud.com</text>
                <text x="490" y="150" font-family="JetBrains Mono" font-size="11" fill="#64748b" text-anchor="middle">Camuflado como Amazon AWS</text>

                <!-- Decision Branch: Target Filter -->
                <rect x="50" y="210" width="580" height="160" rx="14" fill="#090d16" stroke="#475569" stroke-width="2" />
                <text x="340" y="245" font-family="Space Grotesk" font-weight="800" font-size="18" fill="#fff" text-anchor="middle">FILTRO DE OBJETIVOS ESTRATÉGICOS</text>
                
                <!-- Path A: Common Target -->
                <rect x="80" y="270" width="220" height="80" rx="10" fill="#1e293b" />
                <text x="190" y="300" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#94a3b8" text-anchor="middle">Empresa Común</text>
                <text x="190" y="330" font-family="JetBrains Mono" font-size="13" fill="#ef4444" text-anchor="middle">💣 Auto-destrucción</text>

                <!-- Path B: Pentagon/Microsoft -->
                <rect x="380" y="270" width="220" height="80" rx="10" fill="#2e1065" stroke="#a855f7" stroke-width="2" />
                <text x="490" y="300" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#d8b4fe" text-anchor="middle">Pentágono / Tesoro</text>
                <text x="490" y="330" font-family="JetBrains Mono" font-size="13" fill="#a855f7" text-anchor="middle">💀 Inyección TEARDROP</text>
              </svg>
            </div>

            <div class="punch-pill" style="background: #a855f7; color: #ffffff;">
              TEARDROP: LA SEGUNDA FASE SÓLO EN OBJETIVOS CLAVE
            </div>

            <div class="metric-box">
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #a855f7; font-weight: 800;">
                🛰️ TRÁFICO CAMUFLADO: Peticiones DNS a dominios controlados por AWS.
              </div>
              <div style="font-size: 18px; color: #94a3b8; font-weight: 700;">
                El malware permaneció 9 meses invisible en los servidores más custodiados de la Tierra.
              </div>
            </div>
          </div>

          <!-- ACTO 4: El Error de los 2FA y la Cacería de FireEye -->
          <div class="card-layer" id="card-4">
            <div>
              <div class="myth-tag" style="background: rgba(234, 179, 8, 0.15); color: #eab308; border: 1px solid #eab308;">04 • DICIEMBRE 2020: LA CAÍDA</div>
              <div class="headline-black">Un Teléfono Duplicado en el 2FA Reveló el Secreto</div>
            </div>

            <!-- Procedural Diagram: FireEye Discovery -->
            <div class="canvas-graphic-box">
              <svg width="680" height="420" viewBox="0 0 680 420">
                <!-- 2FA Alert Box -->
                <rect x="50" y="40" width="580" height="140" rx="16" fill="#1c1917" stroke="#eab308" stroke-width="3" />
                <text x="340" y="80" font-family="Space Grotesk" font-weight="900" font-size="22" fill="#eab308" text-anchor="middle">⚠️ ALERTA DE SEGURIDAD INTERNA FIREEYE</text>
                <text x="340" y="115" font-family="JetBrains Mono" font-size="16" fill="#fff" text-anchor="middle">Nuevo teléfono móvil registrado para autenticación de empleado</text>
                <text x="340" y="145" font-family="JetBrains Mono" font-weight="800" font-size="14" fill="#22c55e" text-anchor="middle">¿Fue el empleado? -> RESPUESTA: NO</text>

                <!-- Forensic Investigation Steps -->
                <rect x="60" y="210" width="160" height="120" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2" />
                <text x="140" y="245" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#38bdf8" text-anchor="middle">1. RASTREO</text>
                <text x="140" y="280" font-family="JetBrains Mono" font-size="12" fill="#cbd5e1" text-anchor="middle">Cero malware externo</text>
                <text x="140" y="305" font-family="JetBrains Mono" font-size="12" fill="#94a3b8" text-anchor="middle">Credenciales ilesas</text>

                <line x1="220" y1="270" x2="260" y2="270" stroke="#fff" stroke-width="2" />

                <rect x="260" y="210" width="160" height="120" rx="12" fill="#0f172a" stroke="#eab308" stroke-width="2" />
                <text x="340" y="245" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#eab308" text-anchor="middle">2. SOLARWINDS</text>
                <text x="340" y="280" font-family="JetBrains Mono" font-size="12" fill="#cbd5e1" text-anchor="middle">La actualización oficial</text>
                <text x="340" y="305" font-family="JetBrains Mono" font-size="12" fill="#eab308" text-anchor="middle">es el vector</text>

                <line x1="420" y1="270" x2="460" y2="270" stroke="#fff" stroke-width="2" />

                <rect x="460" y="210" width="160" height="120" rx="12" fill="#0f172a" stroke="#f43f5e" stroke-width="2" />
                <text x="540" y="245" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#f43f5e" text-anchor="middle">3. CRISIS NACIONAL</text>
                <text x="540" y="280" font-family="JetBrains Mono" font-size="12" fill="#cbd5e1" text-anchor="middle">Casa Blanca y Azure</text>
                <text x="540" y="305" font-family="JetBrains Mono" font-size="12" fill="#f43f5e" text-anchor="middle">en alerta roja</text>
              </svg>
            </div>

            <div class="punch-pill" style="background: #eab308; color: #000000;">
              EL MEJOR MALWARE DEL MUNDO CAYÓ POR UN SMS
            </div>

            <div class="metric-box">
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #eab308; font-weight: 800;">
                🔍 CACERÍA INVERSA DE KEVIN MANDIA: FireEye alertó al mundo entero.
              </div>
              <div style="font-size: 18px; color: #94a3b8; font-weight: 700;">
                Los atacantes accedieron a los repositorios secretos de Azure y correos de seguridad nacional.
              </div>
            </div>
          </div>

          <!-- ACTO 5: Cierre Omnicanal & Votación Comunitaria -->
          <div class="card-layer" id="card-5">
            <div>
              <div class="myth-tag" style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 2px solid #10b981;">05 • DECISIÓN DE LA COMUNIDAD</div>
              <div class="headline-black">¿Qué Historia Analizamos en el Capítulo #11?</div>
            </div>

            <!-- Interactive Voting Ballot UI -->
            <div class="canvas-graphic-box" style="justify-content: space-around;">
              <!-- Option 1: Boeing 737 MAX -->
              <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: #0f172a; padding: 14px 22px; border-radius: 14px; border: 2px solid #38bdf8;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <span style="background: #38bdf8; color: #000; font-family: 'JetBrains Mono'; font-weight: 900; font-size: 20px; padding: 4px 12px; border-radius: 8px;">1</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 800; font-size: 20px; color: #fff;">✈️ BOEING 737 MAX & MCAS</div>
                    <div style="font-size: 15px; color: #94a3b8;">El sensor de $1,000 y el código oculto que costó 346 vidas</div>
                  </div>
                </div>
                <span style="font-family: 'JetBrains Mono'; color: #38bdf8; font-weight: 800; font-size: 17px;">COMENTA 1</span>
              </div>

              <!-- Option 2: Nintendo vs Universal -->
              <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: #0f172a; padding: 14px 22px; border-radius: 14px; border: 2px solid #f43f5e;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <span style="background: #f43f5e; color: #fff; font-family: 'JetBrains Mono'; font-weight: 900; font-size: 20px; padding: 4px 12px; border-radius: 8px;">2</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 800; font-size: 20px; color: #fff;">🎮 NINTENDO VS UNIVERSAL</div>
                    <div style="font-size: 15px; color: #94a3b8;">El abogado de Donkey Kong que bautizó al personaje Kirby</div>
                  </div>
                </div>
                <span style="font-family: 'JetBrains Mono'; color: #f43f5e; font-weight: 800; font-size: 17px;">COMENTA 2</span>
              </div>

              <!-- Option 3: Theranos & Elizabeth Holmes -->
              <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: #0f172a; padding: 14px 22px; border-radius: 14px; border: 2px solid #eab308;">
                <div style="display: flex; align-items: center; gap: 14px;">
                  <span style="background: #eab308; color: #000; font-family: 'JetBrains Mono'; font-weight: 900; font-size: 20px; padding: 4px 12px; border-radius: 8px;">3</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 800; font-size: 20px; color: #fff;">🩸 THERANOS & LA FALSA MÁQUINA</div>
                    <div style="font-size: 15px; color: #94a3b8;">La ilusión de la gota de sangre y el búnker secreto de Siemens</div>
                  </div>
                </div>
                <span style="font-family: 'JetBrains Mono'; color: #eab308; font-weight: 800; font-size: 17px;">COMENTA 3</span>
              </div>
            </div>

            <div class="punch-pill" style="background: #10b981; color: #000000; font-size: 26px;">
              👇 DEJA EN LOS COMENTARIOS CUÁL QUIERES VER 👇
            </div>

            <div class="metric-box">
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #10b981; font-weight: 800;">
                🏆 EL COMENTARIO MÁS VOTADO SERÁ EL PRÓXIMO CAPÍTULO COMPLETO
              </div>
              <div style="font-size: 18px; color: #94a3b8; font-weight: 700;">
                O déjanos tu caso corporativo o colapso tecnológico favorito. ¡Los leemos todos!
              </div>
            </div>
          </div>
        </div>

        <!-- SUBTITLES ZONE (MIDDLE 12%) -->
        <div class="subtitles-box">
          {' '.join(sub_html)}
        </div>

        <!-- BOTTOM STAGE: HOST AVATARS (LOWER 28%) -->
        <div class="hosts-stage">
          <!-- Jorge -->
          <div class="host-card" id="host-jorge">
            <img class="host-img" src="../assets/jorge_host.png" alt="Jorge Presentador" />
          </div>

          <!-- Dalia -->
          <div class="host-card" id="host-dalia">
            <img class="host-img" src="../assets/dalia_host.png" alt="Dalia Presentadora" />
          </div>
        </div>

        <!-- FOOTER PROGRESS -->
        <div class="footer-box">
          <div class="omnicanal-bar">
            <div class="omni-pill">🟢 Spotify Show (sIA)</div>
            <div class="omni-pill">🎵 TikTok @escucha_sia</div>
            <div class="omni-pill">🌐 escucha-sia.github.io</div>
          </div>

          <div class="progress-bar-container">
            <div class="progress-bar-fill"></div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""

with open("sia_tiktok_batch_engine/compositions/scene.html", "w", encoding="utf-8") as f_out:
    f_out.write(html_content)

print("✨ sia_tiktok_batch_engine/compositions/scene.html generado exitosamente con 100% código!")
