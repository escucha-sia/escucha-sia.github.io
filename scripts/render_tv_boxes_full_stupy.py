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

def render_tv_boxes_stupy():
    audio_src = AUDIO_DIR / "sIA_Sec_02_TV_Boxes_Malware_Fabrica_Videostrong_2026-11-04.mp3"
    reel_filename = "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4"
    total_dur = get_duration(audio_src)
    print(f"🎬 Iniciando render Full-Length Stupy de TV Boxes: {total_dur:.2f}s ({int(total_dur//60):02d}:{int(total_dur%60):02d})")

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
    <title>sIA Sec 02 - TV Boxes Malware</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #060913;
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
    <div id="root" data-composition-id="sia_sec_02_tv_boxes" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
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

    # Define Chapter Boundaries (based on exact SRT)
    # Total duration: 230.14s
    # Cap 1: 0.0s -> 42.6s (La Botnet en tu Sala: 1.3M decodificadores)
    # Cap 2: 42.6s -> 109.0s (Ingeniería del Rootkit: x.cpe y superusuario)
    # Cap 3: 109.0s -> 161.0s (Comando y Control MQTT sobre TLS)
    # Cap 4: 161.0s -> 204.5s (Tu Wi-Fi como Escudo Criminal y Veto de Google)
    # Cap 5: 204.5s -> 230.14s (Omnicanal: Spotify en Coche + Video YouTube/TikTok)
    t0, t1, t2, t3, t4, t5 = 0.0, 42.6, 109.0, 161.0, 204.5, total_dur

    kf_scene1 = build_css_keyframe_rule("scene1Anim", t0, t1, total_dur, is_first=True)
    kf_scene2 = build_css_keyframe_rule("scene2Anim", t1, t2, total_dur)
    kf_scene3 = build_css_keyframe_rule("scene3Anim", t2, t3, total_dur)
    kf_scene4 = build_css_keyframe_rule("scene4Anim", t3, t4, total_dur)
    kf_scene5 = build_css_keyframe_rule("scene5Anim", t4, t5, total_dur, is_last=True)

    kf_c1 = build_chapter_pill_keyframe("c1Anim", t0, t1, total_dur, "#ef4444", "#f87171", is_first=True)
    kf_c2 = build_chapter_pill_keyframe("c2Anim", t1, t2, total_dur, "#0284c7", "#38bdf8")
    kf_c3 = build_chapter_pill_keyframe("c3Anim", t2, t3, total_dur, "#7c3aed", "#c084fc")
    kf_c4 = build_chapter_pill_keyframe("c4Anim", t3, t4, total_dur, "#f59e0b", "#fbbf24")
    kf_c5 = build_chapter_pill_keyframe("c5Anim", t4, t5, total_dur, "#10b981", "#34d399", is_last=True)

    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy - TV Boxes Malware</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #060913;
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
        opacity: 0.14;
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
        color: rgba(239, 68, 68, 0.06);
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
        background: #ef4444;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.6);
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
        border: 6px solid #ef4444;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      #card-1 {{ animation: scene1Anim {total_dur:.1f}s linear forwards; border-color: #ef4444; }}
      #card-2 {{ animation: scene2Anim {total_dur:.1f}s linear forwards; border-color: #0284c7; }}
      #card-3 {{ animation: scene3Anim {total_dur:.1f}s linear forwards; border-color: #7c3aed; }}
      #card-4 {{ animation: scene4Anim {total_dur:.1f}s linear forwards; border-color: #f59e0b; }}
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
        background: linear-gradient(90deg, #ef4444 0%, #06b6d4 50%, #10b981 100%);
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
    <div class="bg-ticker">VIDEOSTRONG &bull; MECOOL &bull; T95 &bull; ROOTKIT &bull; X.CPE &bull; MALWARE</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🚨 sIA Sec #02</div>
          <div class="tag-pill">INVESTIGACIÓN FORENSE</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill" id="chap-1">01 Fábrica</div>
          <div class="chapter-pill" id="chap-2">02 Rootkit</div>
          <div class="chapter-pill" id="chap-3">03 MQTT</div>
          <div class="chapter-pill" id="chap-4">04 Proxy Wi-Fi</div>
          <div class="chapter-pill" id="chap-5">05 Coche/Video</div>
        </div>
      </div>

      <div class="main-card-container">
        <!-- SCENE 1: LA BOTNET DE FÁBRICA -->
        <div class="scene-card" id="card-1">
          <div>
            <div class="myth-tag" style="background: #fee2e2; color: #dc2626;">ATAQUE A LA CADENA DE SUMINISTRO</div>
            <div class="headline-black">1.3 MILLONES DE TV BOXES TROYANIZADAS</div>
          </div>

          <!-- Illustrated Figure 1: TV Box & Smart TV with Rogue Red Signal -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #1e293b 0%, #090d16 100%);">
            <svg width="420" height="360" viewBox="0 0 420 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Smart TV screen -->
              <rect x="40" y="30" width="340" height="200" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
              <rect x="55" y="45" width="310" height="170" rx="6" fill="#020617"/>
              <text x="210" y="110" font-family="Montserrat" font-weight="900" font-size="22" fill="#ef4444" text-anchor="middle">⚠️ SMART TV 4K ANDROID</text>
              <text x="210" y="145" font-family="JetBrains Mono" font-weight="800" font-size="16" fill="#94a3b8" text-anchor="middle">MECOOL / T95 (Videostrong)</text>
              <rect x="90" y="170" width="240" height="26" rx="6" fill="#7f1d1d"/>
              <text x="210" y="188" font-family="JetBrains Mono" font-weight="900" font-size="13" fill="#fca5a5" text-anchor="middle">BACKDOOR X.CPE PREINSTALADO</text>
              <!-- TV Stand -->
              <path d="M180 230 L160 270 L260 270 L240 230 Z" fill="#334155"/>
              <!-- TV Box Hardware Unit -->
              <rect x="130" y="275" width="160" height="50" rx="10" fill="#18181b" stroke="#ef4444" stroke-width="3"/>
              <circle cx="155" cy="300" r="6" fill="#ef4444"/>
              <text x="175" y="305" font-family="JetBrains Mono" font-weight="900" font-size="14" fill="#ffffff">TV BOX 4K</text>
              <!-- HDMI Cable -->
              <path d="M210 275 L210 240" stroke="#f59e0b" stroke-width="4" stroke-dasharray="4 2"/>
              <!-- Malicious WiFi Radiation Waves -->
              <path d="M290 280 A 20 20 0 0 1 320 310" stroke="#ef4444" stroke-width="3" fill="none"/>
              <path d="M300 270 A 35 35 0 0 1 345 315" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 3" fill="none"/>
              <path d="M310 260 A 50 50 0 0 1 370 320" stroke="#ef4444" stroke-width="4" fill="none"/>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #f87171; letter-spacing: 1px;">PRECIO: $25 USD EN AMAZON Y ALIEXPRESS</div>
          </div>

          <div class="punch-pill" style="background: #fee2e2; color: #991b1b; border-color: #ef4444;">EL VIRUS VENÍA DENTRO DEL HARDWARE</div>

          <div class="metric-box" style="border-color: #ef4444; background: #fff5f5;">
            <div style="font-size: 26px; font-weight: 900; color: #b91c1c;">🏢 FABRICANTE: VIDEOSTRONG TECHNOLOGY</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Desmantelado por Google GTIG, HUMAN Security y Policía de Japón.</div>
          </div>
        </div>

        <!-- SCENE 2: INGENIERÍA DEL ROOTKIT -->
        <div class="scene-card" id="card-2">
          <div>
            <div class="myth-tag" style="background: #e0f2fe; color: #0284c7;">PERSISTENCIA EN BOOTLOADER</div>
            <div class="headline-black">x.cpe / com.oemservice</div>
          </div>

          <!-- Illustrated Figure 2: Android Rootkit System Tree -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #0c4a6e 0%, #031e33 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Partition boxes -->
              <rect x="40" y="30" width="360" height="70" rx="10" fill="#0369a1" stroke="#38bdf8" stroke-width="2"/>
              <text x="60" y="60" font-family="JetBrains Mono" font-weight="900" font-size="16" fill="#e0f2fe">/system (Partición de Solo Lectura)</text>
              <text x="60" y="85" font-family="JetBrains Mono" font-weight="700" font-size="13" fill="#bae6fd">android.uid.system (Superusuario Root)</text>

              <!-- Connection arrow -->
              <path d="M220 100 L220 140" stroke="#38bdf8" stroke-width="4" marker-end="url(#arrow)"/>

              <rect x="40" y="140" width="360" height="90" rx="10" fill="#082f49" stroke="#ef4444" stroke-width="3"/>
              <text x="60" y="170" font-family="Montserrat" font-weight="900" font-size="18" fill="#f87171">⚡ MALWARE RE-INSPECTOR</text>
              <text x="60" y="195" font-family="JetBrains Mono" font-weight="700" font-size="14" fill="#ffffff">Paquete: com.oemservice</text>
              <text x="60" y="218" font-family="Space Grotesk" font-weight="700" font-size="13" fill="#fca5a5">Inmune al Restablecimiento de Fábrica</text>

              <!-- Bootloader base -->
              <rect x="40" y="255" width="360" height="75" rx="10" fill="#1e1b4b" stroke="#a855f7" stroke-width="2"/>
              <text x="220" y="285" font-family="Montserrat" font-weight="900" font-size="17" fill="#e9d5ff" text-anchor="middle">BOOTLOADER COMPROMETIDO</text>
              <text x="220" y="312" font-family="JetBrains Mono" font-weight="700" font-size="13" fill="#c084fc" text-anchor="middle">Recompila el troyano en cada inicio</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #38bdf8; letter-spacing: 1px;">CONTROL ABSOLUTO A NIVEL DE KERNEL</div>
          </div>

          <div class="punch-pill" style="background: #000; color: #38bdf8; border-color: #38bdf8;">AL FORMATEAR, EL CHIP LO REINSTALA</div>

          <div class="metric-box" style="border-color: #0284c7; background: #f0f9ff;">
            <div style="font-size: 26px; font-weight: 900; color: #0369a1;">🔒 PLAY PROTECT DESACTIVADO</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Ciega todas las defensas nativas de seguridad de Android.</div>
          </div>
        </div>

        <!-- SCENE 3: COMANDO Y CONTROL MQTT -->
        <div class="scene-card" id="card-3">
          <div>
            <div class="myth-tag" style="background: #f3e8ff; color: #7c3aed;">TELEMETRÍA SILENCIOSA</div>
            <div class="headline-black">MQTT SOBRE TLS (PUERTO 8883)</div>
          </div>

          <!-- Illustrated Figure 3: MQTT C2 Telemetry Diagram -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #3b0764 0%, #170326 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Router Icon -->
              <rect x="40" y="130" width="100" height="70" rx="10" fill="#312e81" stroke="#818cf8" stroke-width="3"/>
              <text x="90" y="165" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffffff" text-anchor="middle">MÓDEM</text>
              <text x="90" y="185" font-family="JetBrains Mono" font-weight="700" font-size="11" fill="#c7d2fe" text-anchor="middle">DOMÉSTICO</text>
              <!-- Antennas -->
              <line x1="65" y1="130" x2="55" y2="90" stroke="#818cf8" stroke-width="4"/>
              <line x1="115" y1="130" x2="125" y2="90" stroke="#818cf8" stroke-width="4"/>

              <!-- Packet flow -->
              <path d="M140 165 L300 165" stroke="#c084fc" stroke-width="4" stroke-dasharray="8 4"/>
              <circle cx="220" cy="165" r="14" fill="#a855f7"/>
              <text x="220" y="170" font-family="JetBrains Mono" font-weight="900" font-size="12" fill="#fff" text-anchor="middle">TLS</text>

              <!-- Cloud C2 -->
              <rect x="300" y="110" width="110" height="110" rx="16" fill="#4c1d95" stroke="#c084fc" stroke-width="3"/>
              <text x="355" y="150" font-family="Montserrat" font-weight="900" font-size="15" fill="#f5d0fe" text-anchor="middle">SERVIDOR</text>
              <text x="355" y="172" font-family="Montserrat" font-weight="900" font-size="15" fill="#ef4444" text-anchor="middle">C2 HACKER</text>
              <text x="355" y="195" font-family="JetBrains Mono" font-weight="800" font-size="11" fill="#ddd6fe" text-anchor="middle">MQTT Botnet</text>

              <!-- Description badge -->
              <rect x="40" y="260" width="370" height="60" rx="12" fill="#2e1065"/>
              <text x="225" y="286" font-family="Space Grotesk" font-weight="800" font-size="15" fill="#e9d5ff" text-anchor="middle">Disfrazado de foco o termostato inteligente</text>
              <text x="225" y="306" font-family="JetBrains Mono" font-weight="700" font-size="13" fill="#a855f7" text-anchor="middle">Los firewalls caseros no lo bloquean</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #c084fc; letter-spacing: 1px;">TRÁFICO LIGERO Y COMPLETAMENTE CIFRADO</div>
          </div>

          <div class="punch-pill" style="background: #f3e8ff; color: #6b21a8; border-color: #7c3aed;">CERO ALERTAS EN TU ROUTER</div>

          <div class="metric-box" style="border-color: #7c3aed; background: #faf5ff;">
            <div style="font-size: 26px; font-weight: 900; color: #6b21a8;">📡 MONETIZACIÓN CLANDESTINA</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Fraude publicitario invisible y captura de tráfico LAN.</div>
          </div>
        </div>

        <!-- SCENE 4: PROXY RESIDENCIAL Y VETO -->
        <div class="scene-card" id="card-4">
          <div>
            <div class="myth-tag" style="background: #fef3c7; color: #b45309;">EL VERDADERO PELIGRO</div>
            <div class="headline-black">TU WI-FI COMO ESCUDO CRIMINAL</div>
          </div>

          <!-- Illustrated Figure 4: Residential Proxy Attack Scheme -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #451a03 0%, #1c0a00 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Criminal -->
              <circle cx="80" cy="90" r="30" fill="#7f1d1d" stroke="#ef4444" stroke-width="2"/>
              <text x="80" y="96" font-family="Montserrat" font-weight="900" font-size="20" fill="#fff" text-anchor="middle">🥷</text>
              <text x="80" y="140" font-family="JetBrains Mono" font-weight="800" font-size="12" fill="#fca5a5" text-anchor="middle">CIBERCRIMINAL</text>

              <!-- Arrow through home -->
              <path d="M120 90 L200 90" stroke="#f59e0b" stroke-width="4" stroke-dasharray="6 3"/>

              <!-- Home IP -->
              <rect x="200" y="55" width="130" height="70" rx="10" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
              <text x="265" y="85" font-family="Montserrat" font-weight="900" font-size="13" fill="#ffffff" text-anchor="middle">TU MÓDEM FAMILIAR</text>
              <text x="265" y="108" font-family="JetBrains Mono" font-weight="900" font-size="12" fill="#38bdf8" text-anchor="middle">IP: 189.140.X.X</text>

              <!-- Arrow to target bank -->
              <path d="M330 90 L380 90" stroke="#ef4444" stroke-width="4"/>
              <rect x="350" y="140" width="75" height="40" rx="6" fill="#991b1b"/>
              <text x="387" y="165" font-family="Montserrat" font-weight="900" font-size="11" fill="#fff" text-anchor="middle">BANCO</text>

              <!-- Police Investigation Badge -->
              <rect x="60" y="210" width="320" height="80" rx="14" fill="#78350f" stroke="#fbbf24" stroke-width="2"/>
              <text x="220" y="240" font-family="Montserrat" font-weight="900" font-size="16" fill="#fef08a" text-anchor="middle">🚨 INVESTIGACIÓN POLICIAL</text>
              <text x="220" y="268" font-family="Space Grotesk" font-weight="700" font-size="14" fill="#fff" text-anchor="middle">La policía tocaba a la puerta de una familia inocente.</text>

              <!-- Google BAN stamp -->
              <rect x="140" y="300" width="160" height="35" rx="6" fill="#dc2626"/>
              <text x="220" y="324" font-family="Montserrat" font-weight="900" font-size="14" fill="#fff" text-anchor="middle">GOOGLE: VETO TOTAL</text>
            </svg>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #fbbf24; letter-spacing: 1px;">EXPULSIÓN DEFINITIVA A VIDEOSTRONG</div>
          </div>

          <div class="punch-pill" style="background: #fef3c7; color: #78350f; border-color: #f59e0b;">ALQUILABAN TU CONEXIÓN A HACKERS</div>

          <div class="metric-box" style="border-color: #f59e0b; background: #fffbeb;">
            <div style="font-size: 26px; font-weight: 900; color: #b45309;">🛡️ MIGRACIÓN RECOMENDADA</div>
            <div style="font-size: 20px; font-weight: 700; color: #475569;">Usa dispositivos certificados: Chromecast, Fire TV o Apple TV.</div>
          </div>
        </div>

        <!-- SCENE 5: OMNICANAL SPOTIFY + YOUTUBE & TIKTOK -->
        <div class="scene-card" id="card-5">
          <div>
            <div class="myth-tag" style="background: #d1fae5; color: #047857;">DISPONIBLE EN 3 PLATAFORMAS</div>
            <div class="headline-black">sIA PODCAST OMNICANAL</div>
          </div>

          <!-- Illustrated Figure 5: Car Dashboard & Mobile Screens -->
          <div class="figure-container" style="background: radial-gradient(circle at center, #064e3b 0%, #022c22 100%);">
            <svg width="440" height="360" viewBox="0 0 440 360" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Car Dashboard Wheel & Center Console -->
              <rect x="30" y="30" width="380" height="180" rx="16" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
              <!-- Car Screen: Spotify -->
              <rect x="50" y="50" width="220" height="140" rx="10" fill="#121212" stroke="#22c55e" stroke-width="2"/>
              <circle cx="85" cy="85" r="18" fill="#22c55e"/>
              <text x="85" y="92" font-family="Montserrat" font-weight="900" font-size="16" fill="#000" text-anchor="middle">sIA</text>
              <text x="115" y="80" font-family="Montserrat" font-weight="900" font-size="14" fill="#ffffff">sIA Podcast</text>
              <text x="115" y="100" font-family="Space Grotesk" font-weight="700" font-size="12" fill="#22c55e">sIA Sec #02 TV Boxes</text>
              <!-- Play progress -->
              <rect x="65" y="130" width="190" height="6" rx="3" fill="#334155"/>
              <rect x="65" y="130" width="120" height="6" rx="3" fill="#22c55e"/>
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
            <div style="font-size: 20px; font-weight: 700; color: #1e293b;">Lee los indicadores de red en: <b>escucha-sia.github.io</b></div>
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
    audit_dir = SCRATCH_DIR / "tv_boxes_stupy_frames"
    audit_dir.mkdir(parents=True, exist_ok=True)
    for sec in [10, 60, 130, 180, 215]:
        fp = audit_dir / f"tvboxes_act_{sec}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sec), "-i", str(target_reel),
            "-vframes", "1", "-q:v", "2", str(fp)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    📸 Frame verificado {sec}s: {fp.name} ({fp.stat().st_size} bytes)")

if __name__ == "__main__":
    render_tv_boxes_stupy()
