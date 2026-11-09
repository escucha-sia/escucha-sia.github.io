import os
import sys
import math
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
SCRATCH_DIR = BASE_DIR / "scratch"
NODE_PATH = r"C:\Carlos\nodejs"

def get_duration(file_path: Path) -> float:
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ], capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def build_css_keyframe_rule(name: str, start_s: float, end_s: float, total_dur: float, is_first: bool = False, is_last: bool = False) -> str:
    p_start = max(0.0, (start_s / total_dur) * 100.0)
    p_in = min(100.0, ((start_s + 0.35) / total_dur) * 100.0)
    p_out = max(p_in + 0.1, ((end_s - 0.35) / total_dur) * 100.0)
    p_end = min(100.0, (end_s / total_dur) * 100.0)

    if is_first:
        return f"""
      @keyframes {name} {{
        0% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
        {p_out:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
        {p_end:.3f}% {{ opacity: 0; transform: scale(0.95); z-index: 0; pointer-events: none; }}
        100% {{ opacity: 0; transform: scale(0.95); z-index: 0; pointer-events: none; }}
      }}"""
    elif is_last:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ opacity: 0; transform: scale(0.95); z-index: 0; pointer-events: none; }}
        {p_in:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
        100% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
      }}"""
    else:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ opacity: 0; transform: scale(0.95); z-index: 0; pointer-events: none; }}
        {p_in:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
        {p_out:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; pointer-events: auto; }}
        {p_end:.3f}%, 100% {{ opacity: 0; transform: scale(0.95); z-index: 0; pointer-events: none; }}
      }}"""

def build_chapter_pill_keyframe(name: str, start_s: float, end_s: float, total_dur: float, active_bg: str, active_border: str, is_first: bool = False, is_last: bool = False) -> str:
    p_start = max(0.0, (start_s / total_dur) * 100.0)
    p_in = min(100.0, ((start_s + 0.1) / total_dur) * 100.0)
    p_out = max(p_in + 0.05, ((end_s - 0.1) / total_dur) * 100.0)
    p_end = min(100.0, (end_s / total_dur) * 100.0)
    inactive = "background: rgba(255, 255, 255, 0.08); color: #94a3b8; border-color: rgba(255, 255, 255, 0.15); transform: scale(1);"
    active = f"background: {active_bg}; color: #ffffff; border-color: {active_border}; box-shadow: 0 0 18px {active_bg}; transform: scale(1.04);"

    if is_first:
        return f"""
      @keyframes {name} {{
        0%, {p_out:.3f}% {{ {active} }}
        {p_end:.3f}%, 100% {{ {inactive} }}
      }}"""
    elif is_last:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ {inactive} }}
        {p_in:.3f}%, 100% {{ {active} }}
      }}"""
    else:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ {inactive} }}
        {p_in:.3f}%, {p_out:.3f}% {{ {active} }}
        {p_end:.3f}%, 100% {{ {inactive} }}
      }}"""

def render_zote_stupy():
    audio_src = AUDIO_DIR / "sIA_Corp_08_Jabon_Zote_La_Corona_Ecatepec_2026-11-06.mp3"
    reel_filename = "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"
    total_dur = get_duration(audio_src)
    print(f"🎬 Iniciando render Full-Length Stupy de Jabón Zote: {total_dur:.2f}s ({int(total_dur//60):02d}:{int(total_dur%60):02d})")

    # Copy audio to engine
    engine_assets = ENGINE_DIR / "assets"
    engine_assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(audio_src, engine_assets / "current_clip.mp3")
    shutil.copy2(audio_src, engine_assets / "audio.mp3")

    # Setup index.html
    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>sIA Crónicas 08 - Jabón Zote La Corona</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #090910;
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
    <div id="root" data-composition-id="sia_cronicas_08_zote" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{total_dur:.1f}"
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
        data-duration="{total_dur:.1f}"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""
    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # Timestamps for Jabón Zote:
    # Total: 215.04s
    # Cap 1: 0.0s -> 40.0s (Baños Corona 1920)
    # Cap 2: 40.0s -> 85.0s (Complejo Ecatepec)
    # Cap 3: 85.0s -> 135.0s (Química Zote)
    # Cap 4: 135.0s -> 185.0s (Seúl y Wall Street)
    # Cap 5: 185.0s -> 215.04s (Omnicanal: Spotify / YouTube / TikTok)
    t0, t1, t2, t3, t4, t5 = 0.0, 40.0, 85.0, 135.0, 185.0, total_dur

    kf_scene1 = build_css_keyframe_rule("scene1Anim", t0, t1, total_dur, is_first=True)
    kf_scene2 = build_css_keyframe_rule("scene2Anim", t1, t2, total_dur)
    kf_scene3 = build_css_keyframe_rule("scene3Anim", t2, t3, total_dur)
    kf_scene4 = build_css_keyframe_rule("scene4Anim", t3, t4, total_dur)
    kf_scene5 = build_css_keyframe_rule("scene5Anim", t4, t5, total_dur, is_last=True)

    kf_c1 = build_chapter_pill_keyframe("c1Anim", t0, t1, total_dur, "#db2777", "#f472b6", is_first=True)
    kf_c2 = build_chapter_pill_keyframe("c2Anim", t1, t2, total_dur, "#0284c7", "#38bdf8")
    kf_c3 = build_chapter_pill_keyframe("c3Anim", t2, t3, total_dur, "#e11d48", "#fb7185")
    kf_c4 = build_chapter_pill_keyframe("c4Anim", t3, t4, total_dur, "#8b5cf6", "#c4b5fd")
    kf_c5 = build_chapter_pill_keyframe("c5Anim", t4, t5, total_dur, "#10b981", "#34d399", is_last=True)

    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy - Jabón Zote</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #090910;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#ec4899 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.12;
        z-index: 1;
        pointer-events: none;
      }}
      .cyber-scanlines {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          0deg,
          rgba(236, 72, 153, 0.04) 0px,
          rgba(236, 72, 153, 0.04) 2px,
          transparent 2px,
          transparent 4px
        );
        z-index: 2;
        pointer-events: none;
      }}
      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 78px;
        color: rgba(236, 72, 153, 0.06);
        text-transform: uppercase;
        transform: rotate(-12deg) scale(1.4);
        top: 25%;
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
        padding: 70px 55px 85px 55px;
      }}
      .header-box {{ display: flex; flex-direction: column; gap: 14px; }}
      .brand-row {{ display: flex; align-items: center; justify-content: space-between; }}
      .brand-pill {{
        background: #db2777;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(219, 39, 119, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(236, 72, 153, 0.15);
        color: #f472b6;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #db2777;
      }}
      .chapters-bar {{ display: flex; gap: 8px; width: 100%; margin-top: 10px; }}
      .chapter-pill {{
        flex: 1;
        padding: 12px 4px;
        border-radius: 12px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 14px;
        text-transform: uppercase;
        border: 2px solid rgba(255, 255, 255, 0.15);
      }}

      #chap-1 {{ animation: c1Anim {total_dur:.1f}s linear forwards; }}
      #chap-2 {{ animation: c2Anim {total_dur:.1f}s linear forwards; }}
      #chap-3 {{ animation: c3Anim {total_dur:.1f}s linear forwards; }}
      #chap-4 {{ animation: c4Anim {total_dur:.1f}s linear forwards; }}
      #chap-5 {{ animation: c5Anim {total_dur:.1f}s linear forwards; }}

      .main-card-container {{
        position: relative;
        width: 100%;
        min-height: 1280px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}

      .scene-card {{
        position: absolute;
        inset: 0;
        background: #ffffff;
        border-radius: 36px;
        padding: 40px 36px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(219, 39, 119, 0.25);
        border: 6px solid #db2777;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      #card-1 {{ animation: scene1Anim {total_dur:.1f}s linear forwards; border-color: #db2777; }}
      #card-2 {{ animation: scene2Anim {total_dur:.1f}s linear forwards; border-color: #0284c7; }}
      #card-3 {{ animation: scene3Anim {total_dur:.1f}s linear forwards; border-color: #e11d48; }}
      #card-4 {{ animation: scene4Anim {total_dur:.1f}s linear forwards; border-color: #8b5cf6; }}
      #card-5 {{ animation: scene5Anim {total_dur:.1f}s linear forwards; border-color: #10b981; }}

      .myth-tag {{
        display: inline-block;
        align-self: flex-start;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 20px;
        padding: 6px 18px;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}
      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 46px;
        line-height: 1.1;
        letter-spacing: -1px;
        color: #09090f;
        margin-top: 8px;
      }}

      /* Illustrated Figure Box */
      .figure-container {{
        width: 100%;
        height: 520px;
        border-radius: 24px;
        background: #0f172a;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.6);
        border: 3px solid #e2e8f0;
      }}

      .punch-pill {{
        display: inline-block;
        align-self: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 32px;
        padding: 12px 28px;
        border-radius: 16px;
        line-height: 1.2;
        border: 3px solid #000;
        text-align: center;
      }}
      .metric-box {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: #f8fafc;
        border: 3px dashed #94a3b8;
        border-radius: 18px;
        padding: 20px;
      }}

      .footer-badge {{ display: flex; flex-direction: column; align-items: center; gap: 14px; }}
      .omnicanal-bar {{ display: flex; gap: 16px; justify-content: center; width: 100%; }}
      .omni-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 19px;
        padding: 10px 20px;
        border-radius: 12px;
        background: rgba(255,255,255,0.08);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.2);
      }}

      .progress-bar-container {{
        width: 100%;
        height: 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }}
      @keyframes progressFillAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}
      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #ec4899 0%, #06b6d4 50%, #10b981 100%);
        width: 0%;
        animation: progressFillAnim {total_dur:.1f}s linear forwards;
      }}

      {kf_scene1}
      {kf_scene2}
      {kf_scene3}
      {kf_scene4}
      {kf_scene5}

      {kf_c1}
      {kf_c2}
      {kf_c3}
      {kf_c4}
      {kf_c5}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="cyber-scanlines"></div>
    <div class="bg-ticker">JABÓN ZOTE &bull; LA CORONA &bull; ECATEPEC &bull; 1920 &bull; MÉXICO &bull; COREA</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🧼 sIA Crónicas #08</div>
          <div class="tag-pill">HISTORIA INDUSTRIAL</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill" id="chap-1">01 1920</div>
          <div class="chapter-pill" id="chap-2">02 Ecatepec</div>
          <div class="chapter-pill" id="chap-3">03 Química</div>
          <div class="chapter-pill" id="chap-4">04 Seúl / Wall St</div>
          <div class="chapter-pill" id="chap-5">05 Coche/Video</div>
        </div>
      </div>

      <div class="main-card-container">
        <!-- SCENE 1: BAÑOS CORONA 1920 -->
        <div class="scene-card" id="card-1">
          <div>
            <div class="myth-tag" style="background: #fce7f3; color: #be185d;">ORIGEN POPULAR MEXICANO</div>
            <div class="headline-black">DE PERALVILLO A TODO MÉXICO</div>
          </div>

          <!-- Figure 1: 1920 Peralta bathhouse & classic laundry cart -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #831843 0%, #2d0616 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Vintage Building facade -->
              <rect x="70" y="60" width="300" height="190" rx="8" fill="#1e293b" stroke="#f472b6" stroke-width="3"/>
              <polygon points="70,60 220,15 370,60" fill="#0f172a" stroke="#f472b6" stroke-width="3"/>
              <text x="220" y="48" font-family="Montserrat" font-weight="900" font-size="15" fill="#fbcfe8" text-anchor="middle">BAÑOS CORONA - 1920</text>
              <rect x="180" y="150" width="80" height="100" rx="4" fill="#334155"/>
              <text x="220" y="115" font-family="Montserrat" font-weight="900" font-size="16" fill="#fff" text-anchor="middle">PERALVILLO, CDMX</text>

              <!-- Classic Zote bar in front -->
              <rect x="110" y="240" width="220" height="75" rx="14" fill="#ec4899" stroke="#ffffff" stroke-width="3"/>
              <text x="220" y="288" font-family="Montserrat" font-weight="900" font-size="32" fill="#ffffff" text-anchor="middle" letter-spacing="4">ZOTE</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fbcfe8; letter-spacing: 1px;">FUNDADA POR ESTEBAN GONZÁLEZ PADILLA</div>
          </div>

          <div class="punch-pill" style="background: #fce7f3; color: #9d174d; border-color: #db2777;">CERO PESOS EN TELEVISIÓN</div>

          <div class="metric-box" style="border-color: #db2777; background: #fff1f2;">
            <div style="font-size: 26px; font-weight: 900; color: #be185d;">📦 DISTRIBUCIÓN DIRECTA</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Llegaron a cada tiendita de barrio sin intermediarios voraces.</div>
          </div>
        </div>

        <!-- SCENE 2: COMPLEJO ECATEPEC -->
        <div class="scene-card" id="card-2">
          <div>
            <div class="myth-tag" style="background: #e0f2fe; color: #0284c7;">INTEGRACIÓN INDUSTRIAL</div>
            <div class="headline-black">LA FORTALEZA DE 300,000 M²</div>
          </div>

          <!-- Figure 2: Ecatepec Factory & Railroad -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #0c4a6e 0%, #031e33 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Factory silos and buildings -->
              <rect x="60" y="70" width="90" height="180" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
              <text x="105" y="160" font-family="JetBrains Mono" font-weight="900" font-size="12" fill="#38bdf8" text-anchor="middle">SILO ACEITE</text>

              <rect x="170" y="90" width="100" height="160" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
              <text x="220" y="160" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffffff" text-anchor="middle">CALDERAS</text>
              <text x="220" y="180" font-family="JetBrains Mono" font-weight="700" font-size="11" fill="#7dd3fc" text-anchor="middle">200,000 L</text>

              <rect x="290" y="70" width="90" height="180" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
              <text x="335" y="160" font-family="JetBrains Mono" font-weight="900" font-size="12" fill="#38bdf8" text-anchor="middle">MOLDEADO</text>

              <!-- Railroad tracks -->
              <line x1="50" y1="280" x2="390" y2="280" stroke="#94a3b8" stroke-width="6"/>
              <line x1="50" y1="295" x2="390" y2="295" stroke="#94a3b8" stroke-width="6"/>
              <line x1="90" y1="275" x2="90" y2="300" stroke="#475569" stroke-width="4"/>
              <line x1="150" y1="275" x2="150" y2="300" stroke="#475569" stroke-width="4"/>
              <line x1="210" y1="275" x2="210" y2="300" stroke="#475569" stroke-width="4"/>
              <line x1="270" y1="275" x2="270" y2="300" stroke="#475569" stroke-width="4"/>
              <line x1="330" y1="275" x2="330" y2="300" stroke="#475569" stroke-width="4"/>

              <!-- Train badge -->
              <rect x="120" y="305" width="200" height="35" rx="6" fill="#0284c7"/>
              <text x="220" y="328" font-family="Montserrat" font-weight="900" font-size="13" fill="#ffffff" text-anchor="middle">ESPUELA DE TREN PROPIA</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #7dd3fc; letter-spacing: 1px;">ECATEPEC, ESTADO DE MÉXICO</div>
          </div>

          <div class="punch-pill" style="background: #e0f2fe; color: #0369a1; border-color: #0284c7;">FABRICAN HASTA SUS CAJAS</div>

          <div class="metric-box" style="border-color: #0284c7; background: #f0f9ff;">
            <div style="font-size: 26px; font-weight: 900; color: #0369a1;">🚂 CERO DEPENDENCIA EXTERNA</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Descargan carros de tren completos con materias primas en su patio.</div>
          </div>
        </div>

        <!-- SCENE 3: QUÍMICA ZOTE -->
        <div class="scene-card" id="card-3">
          <div>
            <div class="myth-tag" style="background: #fee2e2; color: #b91c1c;">FORMULACIÓN CIENTÍFICA</div>
            <div class="headline-black">SEBO, COCO, CITRONELA Y LUZ UV</div>
          </div>

          <!-- Figure 3: Chemistry of Zote -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #831843 0%, #200410 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Chemical component cards -->
              <rect x="50" y="30" width="160" height="75" rx="8" fill="#18181b" stroke="#f472b6" stroke-width="2"/>
              <text x="130" y="58" font-family="Montserrat" font-weight="900" font-size="14" fill="#fbcfe8" text-anchor="middle">SEBO VACUNO</text>
              <text x="130" y="82" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff" text-anchor="middle">Ácidos grasos puros</text>

              <rect x="230" y="30" width="160" height="75" rx="8" fill="#18181b" stroke="#f472b6" stroke-width="2"/>
              <text x="310" y="58" font-family="Montserrat" font-weight="900" font-size="14" fill="#fbcfe8" text-anchor="middle">ACEITE DE COCO</text>
              <text x="310" y="82" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff" text-anchor="middle">Espuma abundante</text>

              <rect x="50" y="125" width="160" height="75" rx="8" fill="#18181b" stroke="#f472b6" stroke-width="2"/>
              <text x="130" y="153" font-family="Montserrat" font-weight="900" font-size="14" fill="#fbcfe8" text-anchor="middle">CITRONELA</text>
              <text x="130" y="177" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff" text-anchor="middle">Aroma y repelente</text>

              <rect x="230" y="125" width="160" height="75" rx="8" fill="#18181b" stroke="#38bdf8" stroke-width="2"/>
              <text x="310" y="153" font-family="Montserrat" font-weight="900" font-size="14" fill="#38bdf8" text-anchor="middle">BLANQUEADOR UV</text>
              <text x="310" y="177" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff" text-anchor="middle">Brilla bajo el sol</text>

              <!-- Central Saponification Banner -->
              <rect x="50" y="225" width="340" height="85" rx="12" fill="#be185d" stroke="#fbcfe8" stroke-width="2"/>
              <text x="220" y="258" font-family="Montserrat" font-weight="900" font-size="16" fill="#ffffff" text-anchor="middle">SAPONIFICACIÓN DIRECTA</text>
              <text x="220" y="285" font-family="Space Grotesk" font-weight="700" font-size="13" fill="#fce7f3" text-anchor="middle">Barra densa que rinde semanas sin deshacerse en el agua</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #f472b6; letter-spacing: 1px;">EL SECRETO DEL BLANCO IMPECABLE</div>
          </div>

          <div class="punch-pill" style="background: #fee2e2; color: #9f1239; border-color: #e11d48;">EL SOL ACTIVA EL BLANQUEO</div>

          <div class="metric-box" style="border-color: #e11d48; background: #fff1f2;">
            <div style="font-size: 26px; font-weight: 900; color: #9f1239;">☀️ REACCIÓN FOTOQUÍMICA</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Absorbe rayos ultravioleta invisibles y emite luz azul blanca visible.</div>
          </div>
        </div>

        <!-- SCENE 4: SEÚL Y WALL STREET -->
        <div class="scene-card" id="card-4">
          <div>
            <div class="myth-tag" style="background: #ede9fe; color: #6d28d9;">CONQUISTA GLOBAL</div>
            <div class="headline-black">DE ECATEPEC A COREA DEL SUR</div>
          </div>

          <!-- Figure 4: Global map and K-Beauty / Laundry phenomenon -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #2e1065 0%, #12042b 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Globe line -->
              <circle cx="220" cy="140" r="100" stroke="#8b5cf6" stroke-width="3" fill="#1e1b4b"/>
              <path d="M140 140 Q 220 70 300 140 Q 220 210 140 140" stroke="#c4b5fd" stroke-width="2" fill="none"/>
              <line x1="220" y1="40" x2="220" y2="240" stroke="#c4b5fd" stroke-width="2"/>

              <!-- Markers -->
              <circle cx="170" cy="145" r="8" fill="#ec4899"/>
              <text x="170" y="170" font-family="Montserrat" font-weight="900" font-size="12" fill="#fbcfe8" text-anchor="middle">MÉXICO</text>

              <circle cx="270" cy="115" r="8" fill="#38bdf8"/>
              <text x="270" y="105" font-family="Montserrat" font-weight="900" font-size="12" fill="#7dd3fc" text-anchor="middle">SEÚL (COREA)</text>

              <!-- Flight arc -->
              <path d="M170 145 Q 220 80 270 115" stroke="#f472b6" stroke-width="3" stroke-dasharray="6 3" fill="none"/>

              <!-- Triumph badge -->
              <rect x="50" y="260" width="340" height="65" rx="12" fill="#4c1d95" stroke="#a855f7" stroke-width="2"/>
              <text x="220" y="288" font-family="Montserrat" font-weight="900" font-size="15" fill="#ffffff" text-anchor="middle">VIRAL EN ASIA POR SU PUREZA</text>
              <text x="220" y="310" font-family="Space Grotesk" font-weight="700" font-size="13" fill="#e9d5ff" text-anchor="middle">Preferido para prendas delicadas y piel sensible.</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #c4b5fd; letter-spacing: 1px;">DERROTANDO A MULTINACIONALES EN SU TERRENO</div>
          </div>

          <div class="punch-pill" style="background: #ede9fe; color: #5b21b6; border-color: #8b5cf6;">UN ÉXITO SIN GASTAR EN PUBLICIDAD</div>

          <div class="metric-box" style="border-color: #8b5cf6; background: #faf5ff;">
            <div style="font-size: 26px; font-weight: 900; color: #6d28d9;">🌏 FENÓMENO CULTURAL</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Demostró que la excelencia de producto vence al marketing agresivo.</div>
          </div>
        </div>

        <!-- SCENE 5: OMNICANAL SPOTIFY + YOUTUBE & TIKTOK -->
        <div class="scene-card" id="card-5">
          <div>
            <div class="myth-tag" style="background: #d1fae5; color: #047857;">DISPONIBLE EN 3 PLATAFORMAS</div>
            <div class="headline-black">sIA PODCAST OMNICANAL</div>
          </div>

          <!-- Figure 5: Car Dashboard & Mobile Screens -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #064e3b 0%, #022c22 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Car Dashboard Console -->
              <rect x="30" y="30" width="380" height="180" rx="16" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
              <!-- Car Screen: Spotify -->
              <rect x="50" y="50" width="220" height="140" rx="10" fill="#121212" stroke="#22c55e" stroke-width="2"/>
              <circle cx="85" cy="85" r="18" fill="#22c55e"/>
              <text x="85" y="92" font-family="Montserrat" font-weight="900" font-size="16" fill="#000" text-anchor="middle">sIA</text>
              <text x="115" y="80" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffffff">sIA Podcast</text>
              <text x="115" y="100" font-family="Space Grotesk" font-weight="700" font-size="12" fill="#22c55e">sIA Crónicas #08 Jabón Zote</text>
              <!-- Play progress -->
              <rect x="65" y="130" width="190" height="6" rx="3" fill="#334155"/>
              <rect x="65" y="130" width="115" height="6" rx="3" fill="#22c55e"/>
              <text x="160" y="160" font-family="Montserrat" font-weight="900" font-size="13" fill="#a7f3d0" text-anchor="middle">🚗 MODO COCHE: SPOTIFY</text>

              <!-- Steering wheel hint -->
              <circle cx="330" cy="120" r="45" stroke="#475569" stroke-width="8" fill="none"/>

              <!-- Mobile Phones for YouTube and TikTok -->
              <!-- Phone 1: TikTok -->
              <rect x="60" y="230" width="140" height="100" rx="12" fill="#000" stroke="#06b6d4" stroke-width="2"/>
              <text x="130" y="265" font-family="Montserrat" font-weight="900" font-size="14" fill="#38bdf8" text-anchor="middle">📱 TIKTOK</text>
              <text x="130" y="290" font-family="JetBrains Mono" font-weight="800" font-size="11" fill="#fff" text-anchor="middle">@escucha_sia</text>
              <text x="130" y="312" font-family="Space Grotesk" font-weight="700" font-size="10" fill="#94a3b8" text-anchor="middle">Video + Diagramas</text>

              <!-- Phone 2: YouTube -->
              <rect x="240" y="230" width="140" height="100" rx="12" fill="#000" stroke="#ef4444" stroke-width="2"/>
              <text x="310" y="265" font-family="Montserrat" font-weight="900" font-size="14" fill="#f87171" text-anchor="middle">▶️ YOUTUBE</text>
              <text x="310" y="290" font-family="JetBrains Mono" font-weight="800" font-size="11" fill="#fff" text-anchor="middle">sIA Hub</text>
              <text x="310" y="312" font-family="Space Grotesk" font-weight="700" font-size="10" fill="#94a3b8" text-anchor="middle">Shorts & Full Video</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #34d399; letter-spacing: 1px;">EL MISMO CONTENIDO EN TODAS PARTES</div>
          </div>

          <div class="punch-pill" style="background: #10b981; color: #fff; border-color: #047857;">COCHE = SPOTIFY | VIDEO = YOUTUBE & TIKTOK</div>

          <div class="metric-box" style="border-color: #10b981; background: #ecfdf5;">
            <div style="font-size: 26px; font-weight: 900; color: #047857;">🌐 PORTAL OFICIAL DE ARTÍCULOS</div>
            <div style="font-size: 20px; font-weight: 700; color: #1e293b;">Lee la historia completa en: <b>escucha-sia.github.io</b></div>
          </div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="omnicanal-bar">
          <span class="omni-pill">🚗 Coche: Spotify</span>
          <span class="omni-pill">📱 Video: YouTube & TikTok (@escucha_sia)</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>
  </div>
  </body>
</html>"""

    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("  ✅ scene.html generado con 5 Actos Stupy Ilustrados y CSS Keyframes nativos.")

    # Render via HyperFrames GPU
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    renders_dir = ENGINE_DIR / "renders"
    if renders_dir.exists():
        for old_vid in renders_dir.glob("*.mp4"):
            try:
                old_vid.unlink()
            except Exception:
                pass

    print("  🚀 Lanzando render con GPU...")
    cmd = ["cmd.exe", "/c", f"set PATH={NODE_PATH};%PATH% && cd /d {ENGINE_DIR} && npx hyperframes render --gpu"]
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"HyperFrames render error: {res.stderr}\nStdout: {res.stdout}")

    output_mp4 = renders_dir / "video.mp4"
    if not output_mp4.exists():
        candidates = list(renders_dir.glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)

    if not output_mp4.exists():
        raise RuntimeError("No se encontró el video generado en renders/")

    # Copy to target destinations
    target_reel = REELS_DIR / reel_filename
    shutil.copy2(output_mp4, target_reel)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / reel_filename)
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / reel_filename)

    dur = get_duration(target_reel)
    size_mb = target_reel.stat().st_size / (1024 * 1024)
    print(f"  🎉 Render finalizado con éxito: {target_reel.name} ({dur:.2f}s, {size_mb:.2f} MB)")

    # Extract verification frames across all 5 acts
    audit_dir = SCRATCH_DIR / "zote_stupy_frames"
    audit_dir.mkdir(parents=True, exist_ok=True)
    for sec in [15, 60, 110, 160, 200]:
        fp = audit_dir / f"zote_act_{sec}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sec), "-i", str(target_reel),
            "-vframes", "1", "-q:v", "2", str(fp)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    📸 Frame verificado {sec}s: {fp.name} ({fp.stat().st_size} bytes)")

if __name__ == "__main__":
    render_zote_stupy()
