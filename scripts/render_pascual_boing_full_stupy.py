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
ARTIFACT_DIR = Path(r"C:\Users\c_a_c\.gemini\antigravity\brain\3d3829e3-9423-4249-b4ec-672aaf684c20")
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

def render_pascual_stupy():
    audio_src = AUDIO_DIR / "sIA_Corp_09_Pascual_Boing_Cooperativa_TetraPak_2026-11-08.mp3"
    reel_filename = "sIA_Storybook_15_Pascual_Boing_Cooperativa_TetraPak.mp4"
    total_dur = get_duration(audio_src)
    print(f"🎬 Iniciando render Full-Length Stupy de Pascual Boing: {total_dur:.2f}s ({int(total_dur//60):02d}:{int(total_dur%60):02d})")

    # Copiar audio e imágenes a la carpeta de assets del motor
    engine_assets = ENGINE_DIR / "assets"
    engine_assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(audio_src, engine_assets / "current_clip.mp3")
    shutil.copy2(audio_src, engine_assets / "audio.mp3")

    img_map = {
        "pascual_img1.jpg": ARTIFACT_DIR / "pascual_scene1_1982_strike_1794145992905.jpg",
        "pascual_img2.jpg": ARTIFACT_DIR / "pascual_scene2_tetrapak_cutaway_1794146010306.jpg",
        "pascual_img3.jpg": ARTIFACT_DIR / "pascual_scene3_pulp_factory_1794146026806.jpg",
        "pascual_img4.jpg": ARTIFACT_DIR / "pascual_scene4_cooperative_triumph_1794146045072.jpg",
        "pascual_img5.jpg": ARTIFACT_DIR / "pascual_scene5_omnicanal_car_1794146063838.jpg",
    }
    for dest_name, src_file in img_map.items():
        if src_file.exists():
            shutil.copy2(src_file, engine_assets / dest_name)
            print(f"   ✓ Copiado asset: {dest_name}")
        else:
            print(f"   ⚠️ No encontrado: {src_file}")

    # Configurar index.html del engine
    index_html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>sIA Crónicas #09 - Pascual Boing</title>
    <style>
      body {{
        margin: 0;
        padding: 0;
        background: #000;
        overflow: hidden;
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
    <div id="root" data-composition-id="sia_cronicas_09_pascual" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
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

    # Timestamps basados en los 5 capítulos de Pascual Boing:
    # Total: 228.12s
    # Acto 1: 0.0s -> 50.30s (Huelga de 1982 y Demetrio Vallejo)
    # Acto 2: 50.30s -> 108.62s (Ingeniería del Tetra Pak piramidal)
    # Acto 3: 108.62s -> 159.96s (Pulpa de Mango en San Juan del Río)
    # Acto 4: 159.96s -> 191.23s (Autogestión de la Cooperativa Pascual)
    # Acto 5: 191.23s -> 228.12s (Cierre Omnicanal: Spotify / YouTube / TikTok)
    t0, t1, t2, t3, t4, t5 = 0.0, 50.30, 108.62, 159.96, 191.23, total_dur

    kf_scene1 = build_css_keyframe_rule("scene1Anim", t0, t1, total_dur, is_first=True)
    kf_scene2 = build_css_keyframe_rule("scene2Anim", t1, t2, total_dur)
    kf_scene3 = build_css_keyframe_rule("scene3Anim", t2, t3, total_dur)
    kf_scene4 = build_css_keyframe_rule("scene4Anim", t3, t4, total_dur)
    kf_scene5 = build_css_keyframe_rule("scene5Anim", t4, t5, total_dur, is_last=True)

    kf_c1 = build_chapter_pill_keyframe("c1Anim", t0, t1, total_dur, "#ef4444", "#f87171", is_first=True)
    kf_c2 = build_chapter_pill_keyframe("c2Anim", t1, t2, total_dur, "#f59e0b", "#fbbf24")
    kf_c3 = build_chapter_pill_keyframe("c3Anim", t2, t3, total_dur, "#10b981", "#34d399")
    kf_c4 = build_chapter_pill_keyframe("c4Anim", t3, t4, total_dur, "#0284c7", "#38bdf8")
    kf_c5 = build_chapter_pill_keyframe("c5Anim", t4, t5, total_dur, "#8b5cf6", "#c4b5fd", is_last=True)

    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy - Pascual Boing</title>
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
        background-image: radial-gradient(#f59e0b 1.5px, transparent 1.5px);
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
          rgba(245, 158, 11, 0.04) 0px,
          rgba(245, 158, 11, 0.04) 2px,
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
        font-size: 74px;
        color: rgba(245, 158, 11, 0.06);
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
        background: #f59e0b;
        color: #000000;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.6);
        border: 2px solid #ffffff;
      }}
      .tag-pill {{
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 9999px;
        border: 1px solid rgba(245, 158, 11, 0.35);
      }}
      .title-hero {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 42px;
        line-height: 1.15;
        letter-spacing: -1.5px;
        color: #ffffff;
      }}
      .title-hero span {{ color: #fbbf24; }}

      .chapters-bar {{
        display: flex;
        gap: 8px;
        width: 100%;
        margin-top: 4px;
      }}
      .chapter-pill {{
        flex: 1;
        text-align: center;
        padding: 10px 4px;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 16px;
        text-transform: uppercase;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        transition: all 0.3s ease;
      }}

      #chap-1 {{ animation: c1Anim {total_dur:.1f}s linear forwards; }}
      #chap-2 {{ animation: c2Anim {total_dur:.1f}s linear forwards; }}
      #chap-3 {{ animation: c3Anim {total_dur:.1f}s linear forwards; }}
      #chap-4 {{ animation: c4Anim {total_dur:.1f}s linear forwards; }}
      #chap-5 {{ animation: c5Anim {total_dur:.1f}s linear forwards; }}

      .center-stage {{
        position: relative;
        width: 100%;
        height: 1220px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .card-layer {{
        position: absolute;
        inset: 0;
        background: #ffffff;
        border-radius: 36px;
        padding: 34px 34px 28px 34px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.85);
        border: 6px solid #f59e0b;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      #card-1 {{ animation: scene1Anim {total_dur:.1f}s linear forwards; border-color: #ef4444; }}
      #card-2 {{ animation: scene2Anim {total_dur:.1f}s linear forwards; border-color: #f59e0b; }}
      #card-3 {{ animation: scene3Anim {total_dur:.1f}s linear forwards; border-color: #10b981; }}
      #card-4 {{ animation: scene4Anim {total_dur:.1f}s linear forwards; border-color: #0284c7; }}
      #card-5 {{ animation: scene5Anim {total_dur:.1f}s linear forwards; border-color: #8b5cf6; }}

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
        font-size: 44px;
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
        font-size: 30px;
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
        padding: 18px;
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
        background: linear-gradient(90deg, #ef4444 0%, #f59e0b 35%, #10b981 70%, #0284c7 100%);
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
    <div class="bg-ticker">PASCUAL BOING &bull; TETRA PAK &bull; 1982 &bull; MANGO ATAULFO &bull; COOPERATIVA &bull; SOBERANÍA</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🥭 sIA Crónicas #09</div>
          <div class="tag-pill">INGENIERÍA & SOBERANÍA</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill" id="chap-1">01 HUELGA 1982</div>
          <div class="chapter-pill" id="chap-2">02 TETRA PAK</div>
          <div class="chapter-pill" id="chap-3">03 AGRO-PULPA</div>
          <div class="chapter-pill" id="chap-4">04 COOPERATIVA</div>
          <div class="chapter-pill" id="chap-5">05 OMNICANAL</div>
        </div>

        <div class="title-hero">
          Pascual Boing: <span>El Triángulo</span> que Derrotó a los Gigantes
        </div>
      </div>

      <div class="center-stage">
        <!-- ACTO 1: Huelga 1982 y Demetrio Vallejo -->
        <div class="card-layer" id="card-1">
          <div>
            <div class="myth-tag" style="background: #fee2e2; color: #991b1b;">01 • MAYO DE 1982: SAN RAFAEL</div>
            <div class="headline-black">La Guerra Patronal y el Nacimiento de la Lucha Obrera</div>
          </div>

          <div class="figure-container">
            <img src="../assets/pascual_img1.jpg" alt="Huelga Pascual 1982" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>

          <div class="punch-pill" style="background: #ef4444; color: #ffffff;">
            3 AÑOS DE PLANTÓN • DEVALUACIÓN 1982
          </div>

          <div class="metric-box">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #0f172a; font-weight: 800;">
              ⚖️ OBREROS VS PATRÓN: 2 Mártires, plantón en banquetas con apoyo de Rufino Tamayo y asesoría de Demetrio Vallejo.
            </div>
            <div style="font-size: 18px; color: #475569; font-weight: 700;">
              La Suprema Corte falló a favor de los obreros: el remate de bienes dio vida a la Sociedad Cooperativa.
            </div>
          </div>
        </div>

        <!-- ACTO 2: Ingeniería del Tetra Pak Triangular -->
        <div class="card-layer" id="card-2">
          <div>
            <div class="myth-tag" style="background: #fef3c7; color: #92400e;">02 • TETRA CLASSIC ASEPTIC</div>
            <div class="headline-black">La Pirámide de 6 Capas que Eliminó la Refrigeración</div>
          </div>

          <div class="figure-container">
            <img src="../assets/pascual_img2.jpg" alt="Tetra Pak Cutaway" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>

          <div class="punch-pill" style="background: #f59e0b; color: #000000;">
            CARTÓN + ALUMINIO UV + POLIETILENO
          </div>

          <div class="metric-box">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #0f172a; font-weight: 800;">
              📐 SELLADO TÉRMICO A 90°: Tubo continuo llenado con jugo y cortado con mordazas cruzadas.
            </div>
            <div style="font-size: 18px; color: #475569; font-weight: 700;">
              Barrera impenetrable contra oxígeno y luz ultravioleta: pulpa natural conservada por meses sin químicos.
            </div>
          </div>
        </div>

        <!-- ACTO 3: Agroindustria y Despulpado -->
        <div class="card-layer" id="card-3">
          <div>
            <div class="myth-tag" style="background: #dcfce7; color: #166534;">03 • PLANTA SAN JUAN DEL RÍO</div>
            <div class="headline-black">Integración Directa con Agricultores Mexicanos</div>
          </div>

          <div class="figure-container">
            <img src="../assets/pascual_img3.jpg" alt="Procesamiento de Fruta" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>

          <div class="punch-pill" style="background: #10b981; color: #ffffff;">
            MANGO ATAULFO Y GUAYABA 100% REAL
          </div>

          <div class="metric-box">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #0f172a; font-weight: 800;">
              🏭 PASTEURIZACIÓN FLASH >90°C: Bolsas asépticas de 200 litros con despalillado centrífugo.
            </div>
            <div style="font-size: 18px; color: #475569; font-weight: 700;">
              Frente a refrescos con jarabe de maíz, Boing procesa cosechas directas de Chiapas, Michoacán y Sinaloa.
            </div>
          </div>
        </div>

        <!-- ACTO 4: Autogestión y Demanda Disney -->
        <div class="card-layer" id="card-4">
          <div>
            <div class="myth-tag" style="background: #e0f2fe; color: #075985;">04 • DEMOCRACIA COOPERATIVA</div>
            <div class="headline-black">1 Obrero = 1 Voto • El Rediseño del Pato Boing</div>
          </div>

          <div class="figure-container">
            <img src="../assets/pascual_img4.jpg" alt="Cooperativa Triunfo" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>

          <div class="punch-pill" style="background: #0284c7; color: #ffffff;">
            CERO DEUDAS • CERO REGALÍAS A TRASNACIONALES
          </div>

          <div class="metric-box">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #0f172a; font-weight: 800;">
              🦆 LITIGIO DISNEY SUPERADO: Concurso nacional para rediseñar al pato con gorra deportiva.
            </div>
            <div style="font-size: 18px; color: #475569; font-weight: 700;">
              Flota logística propia y liderazgo absoluto en cooperativas escolares y taquerías mexicanas.
            </div>
          </div>
        </div>

        <!-- ACTO 5: Cierre Omnicanal sIA -->
        <div class="card-layer" id="card-5">
          <div>
            <div class="myth-tag" style="background: #ede9fe; color: #5b21b6;">05 • CIERRE OMNICANAL sIA</div>
            <div class="headline-black">Disponible en tu Coche y en Redes en Duración Completa</div>
          </div>

          <div class="figure-container">
            <img src="../assets/pascual_img5.jpg" alt="Omnicanal sIA Dashboard" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>

          <div class="punch-pill" style="background: #8b5cf6; color: #ffffff;">
            SPOTIFY • TIKTOK • YOUTUBE (@escucha_sia)
          </div>

          <div class="metric-box">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 19px; color: #0f172a; font-weight: 800;">
              🚗 ¿EN EL TRÁFICO? Escúchanos completo en Spotify manos libres (sIA Podcast).
            </div>
            <div style="font-size: 18px; color: #475569; font-weight: 700;">
              📱 ¿Prefieres ver los diagramas técnicos? Míralo en YouTube y TikTok (@escucha_sia).
            </div>
          </div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="omnicanal-bar">
          <div class="omni-pill">🟢 Spotify Show</div>
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
</html>"""
    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Composiciones index.html y scene.html configuradas con éxito.")

    # Generar poster oficial
    poster_dest = REELS_DIR / "sIA_Storybook_15_Pascual_Boing_Cooperativa_TetraPak_poster.jpg"
    shutil.copy2(img_map["pascual_img2.jpg"], poster_dest)
    print(f"✅ Poster guardado: {poster_dest}")

    # Ejecutar Render con HyperFrames CLI
    print("🚀 Ejecutando HyperFrames render GPU...")
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    renders_dir = ENGINE_DIR / "renders"
    if renders_dir.exists():
        for old_vid in renders_dir.glob("*.mp4"):
            try:
                old_vid.unlink()
            except Exception:
                pass

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

    target_reel = REELS_DIR / reel_filename
    shutil.copy2(output_mp4, target_reel)
    if SPOTIFY_REELS_DIR.exists():
        shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / reel_filename)
        print(f"   ✓ Respaldo local Spotify: {SPOTIFY_REELS_DIR / reel_filename}")
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / reel_filename)
        print(f"   ✓ Respaldo Google Drive: {GDRIVE_REELS_DIR / reel_filename}")

    dur = get_duration(target_reel)
    size_mb = target_reel.stat().st_size / (1024 * 1024)
    print(f"🎉 Video maestro vertical generado: {target_reel} ({dur:.2f}s, {size_mb:.2f} MB)")

if __name__ == "__main__":
    render_pascual_stupy()
