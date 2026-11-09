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

def render_xz_backdoor_stupy():
    audio_src = AUDIO_DIR / "sIA_Sec_03_XZ_Utils_Backdoor_Andres_Freund_SSH_2026-11-04.mp3"
    reel_filename = "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4"
    total_dur = get_duration(audio_src)
    print(f"🎬 Iniciando render Full-Length Stupy de XZ Utils: {total_dur:.2f}s ({int(total_dur//60):02d}:{int(total_dur%60):02d})")

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
    <title>sIA Sec 03 - XZ Utils Backdoor</title>
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
    <div id="root" data-composition-id="sia_sec_03_xz_backdoor" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
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

    # Timestamps (exact SRT):
    # Total: 236.43s
    # Cap 1: 0.0s -> 35.9s (El Objetivo: liblzma)
    # Cap 2: 35.9s -> 82.7s (Ingeniería Social: Jia Tan)
    # Cap 3: 82.7s -> 136.0s (El Backdoor: IFUNC + OpenSSH)
    # Cap 4: 136.0s -> 213.6s (El Héroe: Andrés Freund y los 500ms)
    # Cap 5: 213.6s -> 236.43s (Omnicanal: Spotify / YouTube / TikTok)
    t0, t1, t2, t3, t4, t5 = 0.0, 35.9, 82.7, 136.0, 213.6, total_dur

    kf_scene1 = build_css_keyframe_rule("scene1Anim", t0, t1, total_dur, is_first=True)
    kf_scene2 = build_css_keyframe_rule("scene2Anim", t1, t2, total_dur)
    kf_scene3 = build_css_keyframe_rule("scene3Anim", t2, t3, total_dur)
    kf_scene4 = build_css_keyframe_rule("scene4Anim", t3, t4, total_dur)
    kf_scene5 = build_css_keyframe_rule("scene5Anim", t4, t5, total_dur, is_last=True)

    kf_c1 = build_chapter_pill_keyframe("c1Anim", t0, t1, total_dur, "#0284c7", "#38bdf8", is_first=True)
    kf_c2 = build_chapter_pill_keyframe("c2Anim", t1, t2, total_dur, "#f59e0b", "#fbbf24")
    kf_c3 = build_chapter_pill_keyframe("c3Anim", t2, t3, total_dur, "#ef4444", "#f87171")
    kf_c4 = build_chapter_pill_keyframe("c4Anim", t3, t4, total_dur, "#06b6d4", "#22d3ee")
    kf_c5 = build_chapter_pill_keyframe("c5Anim", t4, t5, total_dur, "#10b981", "#34d399", is_last=True)

    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy - XZ Utils Backdoor</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #020617;
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
        background-image: radial-gradient(#06b6d4 1.5px, transparent 1.5px);
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
          rgba(6, 182, 212, 0.04) 0px,
          rgba(6, 182, 212, 0.04) 2px,
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
        color: rgba(6, 182, 212, 0.06);
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
        background: #0284c7;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(2, 132, 199, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(6, 182, 212, 0.15);
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #0284c7;
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
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(6, 182, 212, 0.25);
        border: 6px solid #0284c7;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      #card-1 {{ animation: scene1Anim {total_dur:.1f}s linear forwards; border-color: #0284c7; }}
      #card-2 {{ animation: scene2Anim {total_dur:.1f}s linear forwards; border-color: #f59e0b; }}
      #card-3 {{ animation: scene3Anim {total_dur:.1f}s linear forwards; border-color: #ef4444; }}
      #card-4 {{ animation: scene4Anim {total_dur:.1f}s linear forwards; border-color: #06b6d4; }}
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
        background: linear-gradient(90deg, #0284c7 0%, #06b6d4 50%, #10b981 100%);
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
    <div class="bg-ticker">XZ UTILS &bull; LIBLZMA &bull; OPENSSH &bull; ANDRES FREUND &bull; 500MS BUG</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🛡️ sIA Sec #03</div>
          <div class="tag-pill">CIBERSEGURIDAD FORENSE</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill" id="chap-1">01 Objetivo</div>
          <div class="chapter-pill" id="chap-2">02 Infiltración</div>
          <div class="chapter-pill" id="chap-3">03 Backdoor</div>
          <div class="chapter-pill" id="chap-4">04 Andrés Freund</div>
          <div class="chapter-pill" id="chap-5">05 Coche/Video</div>
        </div>
      </div>

      <div class="main-card-container">
        <!-- SCENE 1: EL OBJETIVO: LIBLZMA -->
        <div class="scene-card" id="card-1">
          <div>
            <div class="myth-tag" style="background: #e0f2fe; color: #0284c7;">INFRAESTRUCTURA MUNDIAL</div>
            <div class="headline-black">LA LIBRERÍA INSTALADA EN TODO LINUX</div>
          </div>

          <!-- Figure 1: Linux Server Rack & liblzma compression -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #0c4a6e 0%, #031e33 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Server rack -->
              <rect x="70" y="40" width="300" height="230" rx="14" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
              <!-- Rack units -->
              <rect x="90" y="60" width="260" height="40" rx="6" fill="#1e293b"/>
              <circle cx="115" cy="80" r="5" fill="#22c55e"/>
              <text x="135" y="86" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#ffffff">DEBIAN &bull; RED HAT &bull; UBUNTU</text>

              <rect x="90" y="115" width="260" height="40" rx="6" fill="#1e293b"/>
              <circle cx="115" cy="135" r="5" fill="#22c55e"/>
              <text x="135" y="141" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#38bdf8">NUBES GUBERNAMENTALES</text>

              <rect x="90" y="170" width="260" height="40" rx="6" fill="#1e293b"/>
              <circle cx="115" cy="190" r="5" fill="#22c55e"/>
              <text x="135" y="196" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#ffffff">CENTROS DE DATOS BANCARIOS</text>

              <!-- Central library chip -->
              <rect x="90" y="225" width="260" height="35" rx="6" fill="#0284c7"/>
              <text x="220" y="248" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffffff" text-anchor="middle">📦 XZ UTILS / LIBLZMA (.tar.xz)</text>

              <!-- Bottom badge -->
              <rect x="70" y="285" width="300" height="45" rx="10" fill="#0369a1"/>
              <text x="220" y="313" font-family="Montserrat" font-weight="900" font-size="15" fill="#fff" text-anchor="middle">99% DE LOS SERVIDORES EN LA RED</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #7dd3fc; letter-spacing: 1px;">UBICUO EN SATÉLITES, NUBES Y ROUTERS</div>
          </div>

          <div class="punch-pill" style="background: #e0f2fe; color: #0284c7; border-color: #0284c7;">UN COMPONENTE VITAL INVISIBLE</div>

          <div class="metric-box" style="border-color: #0284c7; background: #f0f9ff;">
            <div style="font-size: 26px; font-weight: 900; color: #0369a1;">☕ MANTENIDO POR UN VOLUNTARIO</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Lasse Collin sostenía solo el proyecto desde su hogar en Finlandia.</div>
          </div>
        </div>

        <!-- SCENE 2: INGENIERÍA SOCIAL (JIA TAN) -->
        <div class="scene-card" id="card-2">
          <div>
            <div class="myth-tag" style="background: #fef3c7; color: #b45309;">PACIENCIA DE INTELIGENCIA ESTATAL</div>
            <div class="headline-black">JIA TAN: 2 AÑOS GANANDO CONFIANZA</div>
          </div>

          <!-- Figure 2: Social Engineering Timeline -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #451a03 0%, #1c0a00 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Timeline nodes -->
              <line x1="70" y1="60" x2="70" y2="280" stroke="#f59e0b" stroke-width="4"/>

              <!-- Step 1 -->
              <circle cx="70" cy="70" r="14" fill="#f59e0b"/>
              <rect x="100" y="45" width="295" height="50" rx="8" fill="#292524" stroke="#f59e0b" stroke-width="2"/>
              <text x="115" y="70" font-family="Montserrat" font-weight="900" font-size="13" fill="#fef08a">2021-2022: COMMITS INOFENSIVOS</text>
              <text x="115" y="87" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff">Arregló bugs menores y ayudó en el repo.</text>

              <!-- Step 2 -->
              <circle cx="70" cy="150" r="14" fill="#f59e0b"/>
              <rect x="100" y="125" width="295" height="50" rx="8" fill="#292524" stroke="#f59e0b" stroke-width="2"/>
              <text x="115" y="150" font-family="Montserrat" font-weight="900" font-size="13" fill="#f87171">CUENTAS TÍTERE PRESIONANDO</text>
              <text x="115" y="167" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff">Exigían a Lasse ceder el mantenimiento.</text>

              <!-- Step 3 -->
              <circle cx="70" cy="230" r="14" fill="#ef4444"/>
              <rect x="100" y="205" width="295" height="55" rx="8" fill="#7f1d1d" stroke="#ef4444" stroke-width="3"/>
              <text x="115" y="230" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffedd5">CONTROL TOTAL DE RELEASES</text>
              <text x="115" y="248" font-family="Space Grotesk" font-weight="700" font-size="11" fill="#fff">Jia Tan lanza xz 5.6.0 y 5.6.1 troyanizadas.</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fbbf24; letter-spacing: 1px;">EL CABALLO DE TROYA PERFECTO EN OPEN SOURCE</div>
          </div>

          <div class="punch-pill" style="background: #fef3c7; color: #78350f; border-color: #f59e0b;">DESGASTE PSICOLÓGICO Y CONTROL</div>

          <div class="metric-box" style="border-color: #f59e0b; background: #fffbeb;">
            <div style="font-size: 26px; font-weight: 900; color: #b45309;">🎭 OPERACIÓN QUIRÚRGICA</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">El código malicioso no estaba en C, sino en tests de compresión corruptos.</div>
          </div>
        </div>

        <!-- SCENE 3: EL BACKDOOR EN OPENSSH -->
        <div class="scene-card" id="card-3">
          <div>
            <div class="myth-tag" style="background: #fee2e2; color: #b91c1c;">INGENIERÍA MALICIOSA MILITAR</div>
            <div class="headline-black">IFUNC Y EL HOOK SILENCIOSO EN SSHD</div>
          </div>

          <!-- Figure 3: Exploit chain diagram -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #450a0a 0%, #1a0505 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Exploit chain boxes -->
              <rect x="40" y="30" width="360" height="55" rx="8" fill="#18181b" stroke="#94a3b8" stroke-width="2"/>
              <text x="60" y="55" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#38bdf8">1. M4 Build Script</text>
              <text x="60" y="73" font-family="Space Grotesk" font-weight="700" font-size="12" fill="#e2e8f0">Extrae payload precompilado en el build</text>

              <path d="M220 85 L220 105" stroke="#ef4444" stroke-width="4"/>

              <rect x="40" y="105" width="360" height="55" rx="8" fill="#18181b" stroke="#f59e0b" stroke-width="2"/>
              <text x="60" y="130" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#fbbf24">2. GNU IFUNC (Funciones Indirectas)</text>
              <text x="60" y="148" font-family="Space Grotesk" font-weight="700" font-size="12" fill="#e2e8f0">Resuelve símbolos dinámicos antes del arranque</text>

              <path d="M220 160 L220 180" stroke="#ef4444" stroke-width="4"/>

              <rect x="40" y="180" width="360" height="55" rx="8" fill="#7f1d1d" stroke="#ef4444" stroke-width="3"/>
              <text x="60" y="205" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffedd5">3. OpenSSH Interceptado</text>
              <text x="60" y="223" font-family="Space Grotesk" font-weight="700" font-size="12" fill="#fff">Modifica RSA_public_decrypt en libcrypto</text>

              <!-- Master Key Badge -->
              <rect x="40" y="260" width="360" height="65" rx="12" fill="#991b1b" stroke="#fca5a5" stroke-width="2"/>
              <text x="220" y="288" font-family="Montserrat" font-weight="900" font-size="15" fill="#fff" text-anchor="middle">🗝️ LLAVE MAESTRA UNIVERSAL</text>
              <text x="220" y="310" font-family="Space Grotesk" font-weight="700" font-size="13" fill="#ffedd5" text-anchor="middle">Root en cualquier servidor sin dejar un solo log.</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #f87171; letter-spacing: 1px;">EL MAYOR ATAQUE DE LA HISTORIA A INTERNET</div>
          </div>

          <div class="punch-pill" style="background: #000; color: #ef4444; border-color: #ef4444;">ROOT TOTAL CON UNA FIRMA PRIVADA</div>

          <div class="metric-box" style="border-color: #ef4444; background: #fff5f5;">
            <div style="font-size: 26px; font-weight: 900; color: #b91c1c;">💥 A DÍAS DE LLEGAR A PRODUCCIÓN</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Habría infectado las versiones estables de Debian, Ubuntu y Red Hat.</div>
          </div>
        </div>

        <!-- SCENE 4: ANDRÉS FREUND Y LOS 500MS -->
        <div class="scene-card" id="card-4">
          <div>
            <div class="myth-tag" style="background: #cffafe; color: #0891b2;">EL INGENIERO QUE NOTÓ EL RETRASO</div>
            <div class="headline-black">500 MILISEGUNDOS SALVARON EL MUNDO</div>
          </div>

          <!-- Figure 4: Andres Freund Valgrind & 500ms Terminal Trace -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #083344 0%, #021a24 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Terminal Box -->
              <rect x="40" y="30" width="360" height="180" rx="10" fill="#020617" stroke="#06b6d4" stroke-width="2"/>
              <circle cx="65" cy="50" r="5" fill="#ef4444"/>
              <circle cx="80" cy="50" r="5" fill="#f59e0b"/>
              <circle cx="95" cy="50" r="5" fill="#22c55e"/>
              <text x="120" y="55" font-family="JetBrains Mono" font-weight="900" font-size="12" fill="#94a3b8">andres@freedesktop:~$ valgrind</text>

              <!-- Valgrind output -->
              <text x="55" y="85" font-family="JetBrains Mono" font-weight="700" font-size="12" fill="#22d3ee">== Valgrind: Memory errors in liblzma.so</text>
              <text x="55" y="110" font-family="JetBrains Mono" font-weight="700" font-size="12" fill="#f87171">== sshd login: CPU usage anomalously high</text>
              <text x="55" y="140" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#fef08a">⏱️ Latency spike: +500 ms (0.5s lag)</text>
              <text x="55" y="170" font-family="JetBrains Mono" font-weight="700" font-size="12" fill="#a5f3fc">Andrés Freund: "No voy a ignorar esto."</text>

              <!-- Alert badge -->
              <rect x="40" y="235" width="360" height="85" rx="12" fill="#155e75" stroke="#22d3ee" stroke-width="2"/>
              <text x="220" y="265" font-family="Montserrat" font-weight="900" font-size="16" fill="#cffafe" text-anchor="middle">🚨 29 DE MARZO DE 2024</text>
              <text x="220" y="290" font-family="Space Grotesk" font-weight="700" font-size="13" fill="#ffffff" text-anchor="middle">Andrés desensambló el binario y frenó la pesadilla.</text>
              <text x="220" y="308" font-family="JetBrains Mono" font-weight="800" font-size="11" fill="#a5f3fc" text-anchor="middle">Alerta enviada a la lista oss-security</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #67e8f9; letter-spacing: 1px;">EL PODER DE LA CURIOSIDAD DE UN DESARROLLADOR</div>
          </div>

          <div class="punch-pill" style="background: #cffafe; color: #0e7490; border-color: #06b6d4;">UN MICRO-LAG EVITÓ EL COLAPSO</div>

          <div class="metric-box" style="border-color: #06b6d4; background: #ecfeff;">
            <div style="font-size: 26px; font-weight: 900; color: #0891b2;">🌟 HÉROE INESPERADO</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Optimizaba PostgreSQL en Microsoft cuando notó la lentitud en SSH.</div>
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
              <text x="115" y="100" font-family="Space Grotesk" font-weight="700" font-size="12" fill="#22c55e">sIA Sec #03 XZ Utils</text>
              <!-- Play progress -->
              <rect x="65" y="130" width="190" height="6" rx="3" fill="#334155"/>
              <rect x="65" y="130" width="130" height="6" rx="3" fill="#22c55e"/>
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
            <div style="font-size: 20px; font-weight: 700; color: #1e293b;">Lee la cadena forense completa en: <b>escucha-sia.github.io</b></div>
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
    audit_dir = SCRATCH_DIR / "xz_backdoor_stupy_frames"
    audit_dir.mkdir(parents=True, exist_ok=True)
    for sec in [15, 60, 110, 175, 225]:
        fp = audit_dir / f"xz_act_{sec}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sec), "-i", str(target_reel),
            "-vframes", "1", "-q:v", "2", str(fp)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    📸 Frame verificado {sec}s: {fp.name} ({fp.stat().st_size} bytes)")

if __name__ == "__main__":
    render_xz_backdoor_stupy()
