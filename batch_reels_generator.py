"""
Batch TikTok & Reels Video Generator using HyperFrames & FFmpeg
Iterates through sIA episode catalog, extracts audio teasers, compiles GSAP animated 9:16 scenes,
renders with local GPU-accelerated HyperFrames, generates posters, and registers in the web magazine.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
NODE_PATH = r"C:\Carlos\nodejs"

REELS_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)
ENGINE_DIR.mkdir(parents=True, exist_ok=True)

# Visual themes dictionary
THEMES = {
    "cyan": {
        "primary": "#06b6d4",
        "primary_glow": "rgba(6, 182, 212, 0.6)",
        "bg_radial_1": "rgba(6, 182, 212, 0.22)",
        "bg_radial_2": "rgba(139, 92, 246, 0.15)",
        "pill_border": "rgba(6, 182, 212, 0.5)",
        "pill_bg": "linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(0, 0, 0, 0.4))",
        "pill_text": "#67e8f9",
        "btn_bg": "#0891b2",
        "eq_gradient": "linear-gradient(180deg, #06b6d4, #0e7490)",
        "card_border": "rgba(6, 182, 212, 0.3)",
        "badge_brand_bg": "rgba(6, 182, 212, 0.12)",
        "badge_brand_border": "rgba(6, 182, 212, 0.4)",
        "badge_brand_text": "#a5f3fc",
        "highlight_color": "#22d3ee",
    },
    "purple": {
        "primary": "#a855f7",
        "primary_glow": "rgba(168, 85, 247, 0.6)",
        "bg_radial_1": "rgba(168, 85, 247, 0.22)",
        "bg_radial_2": "rgba(59, 130, 246, 0.15)",
        "pill_border": "rgba(168, 85, 247, 0.5)",
        "pill_bg": "linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(0, 0, 0, 0.4))",
        "pill_text": "#c084fc",
        "btn_bg": "#9333ea",
        "eq_gradient": "linear-gradient(180deg, #a855f7, #6b21a8)",
        "card_border": "rgba(168, 85, 247, 0.3)",
        "badge_brand_bg": "rgba(168, 85, 247, 0.12)",
        "badge_brand_border": "rgba(168, 85, 247, 0.4)",
        "badge_brand_text": "#e9d5ff",
        "highlight_color": "#c084fc",
    },
    "amber": {
        "primary": "#f59e0b",
        "primary_glow": "rgba(245, 158, 11, 0.6)",
        "bg_radial_1": "rgba(245, 158, 11, 0.22)",
        "bg_radial_2": "rgba(239, 68, 68, 0.15)",
        "pill_border": "rgba(245, 158, 11, 0.5)",
        "pill_bg": "linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(0, 0, 0, 0.4))",
        "pill_text": "#fcd34d",
        "btn_bg": "#d97706",
        "eq_gradient": "linear-gradient(180deg, #f59e0b, #b45309)",
        "card_border": "rgba(245, 158, 11, 0.3)",
        "badge_brand_bg": "rgba(245, 158, 11, 0.12)",
        "badge_brand_border": "rgba(245, 158, 11, 0.4)",
        "badge_brand_text": "#fef08a",
        "highlight_color": "#fbbf24",
    },
    "emerald": {
        "primary": "#10b981",
        "primary_glow": "rgba(16, 185, 129, 0.6)",
        "bg_radial_1": "rgba(16, 185, 129, 0.22)",
        "bg_radial_2": "rgba(6, 182, 212, 0.15)",
        "pill_border": "rgba(16, 185, 129, 0.5)",
        "pill_bg": "linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(0, 0, 0, 0.4))",
        "pill_text": "#6ee7b7",
        "btn_bg": "#059669",
        "eq_gradient": "linear-gradient(180deg, #10b981, #047857)",
        "card_border": "rgba(16, 185, 129, 0.3)",
        "badge_brand_bg": "rgba(16, 185, 129, 0.12)",
        "badge_brand_border": "rgba(16, 185, 129, 0.4)",
        "badge_brand_text": "#a7f3d0",
        "highlight_color": "#34d399",
    },
    "violet": {
        "primary": "#8b5cf6",
        "primary_glow": "rgba(139, 92, 246, 0.6)",
        "bg_radial_1": "rgba(139, 92, 246, 0.22)",
        "bg_radial_2": "rgba(236, 72, 153, 0.15)",
        "pill_border": "rgba(139, 92, 246, 0.5)",
        "pill_bg": "linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(0, 0, 0, 0.4))",
        "pill_text": "#d8b4fe",
        "btn_bg": "#7c3aed",
        "eq_gradient": "linear-gradient(180deg, #8b5cf6, #5b21b6)",
        "card_border": "rgba(139, 92, 246, 0.3)",
        "badge_brand_bg": "rgba(139, 92, 246, 0.12)",
        "badge_brand_border": "rgba(139, 92, 246, 0.4)",
        "badge_brand_text": "#ddd6fe",
        "highlight_color": "#a78bfa",
    },
    "red": {
        "primary": "#ef4444",
        "primary_glow": "rgba(239, 68, 68, 0.6)",
        "bg_radial_1": "rgba(239, 68, 68, 0.24)",
        "bg_radial_2": "rgba(153, 27, 27, 0.20)",
        "pill_border": "rgba(239, 68, 68, 0.5)",
        "pill_bg": "linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(0, 0, 0, 0.4))",
        "pill_text": "#fca5a5",
        "btn_bg": "#dc2626",
        "eq_gradient": "linear-gradient(180deg, #ef4444, #991b1b)",
        "card_border": "rgba(239, 68, 68, 0.3)",
        "badge_brand_bg": "rgba(239, 68, 68, 0.12)",
        "badge_brand_border": "rgba(239, 68, 68, 0.4)",
        "badge_brand_text": "#fca5a5",
        "highlight_color": "#f87171",
    }
}

# Catalog batch definition
REELS_CATALOG = [
    {
        "id": "reel_05",
        "audio_source": "sIA_Daily_S05_Geek_Horror_FullDive_VR_2026-10-12.mp3",
        "output_reel": "sIA_Reel_05_Horror_Psicologico_FullDive.mp4",
        "badge_tag": "sIA #38",
        "category_name": "CULTURA GEEK",
        "pill_text": "🧠 HORROR & VR • ANÁLISIS",
        "hook_title": "¿Puede una IA simular <span class=\"hl\">terror psicológico real</span> o nuestro cerebro sabe que finge?",
        "kinetic_1": "En Silent Hill y SAO, el miedo no es el monstruo... es la incertidumbre.",
        "sub_1": "🌌 NEUROCIENCIA FULL-DIVE",
        "kinetic_2": "Si la máquina induce pánico sensorial, ¿dónde termina el software?",
        "sub_2": "🎮 ANÁLISIS DE HARD SCI-FI",
        "theme": "violet",
        "start_time": "00:00:00.5",
        "duration": 18.5
    },
    {
        "id": "reel_06",
        "audio_source": "sIA_Daily_S04_Maker_3D_Bambu_Polimeros4D_2026-10-12.mp3",
        "output_reel": "sIA_Reel_06_Maker_Bambu_Lab_PETG.mp4",
        "badge_tag": "sIA #37",
        "category_name": "IMPRESIÓN 3D",
        "pill_text": "⚙️ BAMBU LAB X1C • MAKER",
        "hook_title": "¿Por qué tus piezas de PETG <span class=\"hl\">se deforman y fallan</span> en tolerancias críticas?",
        "kinetic_1": "Flujo volumétrico, retracción y compensación térmica del núcleo.",
        "sub_1": "🛠️ INGENIERÍA DE MATERIALES",
        "kinetic_2": "Y el salto a la impresión 4D: geometrías que mutan con temperatura.",
        "sub_2": "🚀 METAMATERIALES TÉRMICOS",
        "theme": "emerald",
        "start_time": "00:00:00.5",
        "duration": 18.5
    },
    {
        "id": "reel_07",
        "audio_source": "sIA_Daily_S03_Hardware_Calibre_DRM_Electroquimica_2026-10-12.mp3",
        "output_reel": "sIA_Reel_07_Hardware_DRM_EReaders.mp4",
        "badge_tag": "sIA #36",
        "category_name": "HARDWARE",
        "pill_text": "📖 SOBERANÍA DIGITAL • E-INK",
        "hook_title": "Compraste un libro digital... pero <span class=\"hl\">las corporaciones pueden borrarlo</span> cuando quieran.",
        "kinetic_1": "Cierre del DRM en e-readers y el escape hacia KOReader y Calibre.",
        "sub_1": "🔒 DEFENSA DE TU BIBLIOTECA",
        "kinetic_2": "Más pantallas electroquímicas reflectivas a 60 cuadros por segundo.",
        "sub_2": "⚡ EL FIN DE LA FATIGA VISUAL",
        "theme": "amber",
        "start_time": "00:00:00.5",
        "duration": 18.5
    },
    {
        "id": "reel_08",
        "audio_source": "sIA_Daily_S02_Data_Contratos_Semanticos_FHE_2026-10-12.mp3",
        "output_reel": "sIA_Reel_08_Data_Contratos_Semanticos.mp4",
        "badge_tag": "sIA #35",
        "category_name": "DATA & CLOUD",
        "pill_text": "📊 DATA ENGINEERING • SQL",
        "hook_title": "Tus pipelines de datos fallan porque nadie respeta un <span class=\"hl\">contrato semántico</span>.",
        "kinetic_1": "Validación estricta de esquemas en YAML antes de que toquen producción.",
        "sub_1": "🛡️ GOBERNANZA DE DATOS",
        "kinetic_2": "Y consultas SQL cifradas en memoria con criptografía homomórfica.",
        "sub_2": "🔐 CERO FUGAS EN BIGQUERY",
        "theme": "purple",
        "start_time": "00:00:00.5",
        "duration": 18.5
    },
    {
        "id": "reel_09",
        "audio_source": "sIA_DeepDive_Laya_OpenSource_CommandCenter.mp3",
        "output_reel": "sIA_Reel_09_Laya_OpenSource_Agentic.mp4",
        "badge_tag": "sIA DEEP DIVE",
        "category_name": "OPEN SOURCE AI",
        "pill_text": "⚡ ALTERNATIVA A JEV • AGENTES",
        "hook_title": "¿Cansado de depender de APIs caras? Laya es el <span class=\"hl\">centro de comando agéntico</span> local.",
        "kinetic_1": "Tauri v2, Svelte 5 y FastAPI corriendo en tu propia GPU sin telemetría.",
        "sub_1": "💻 LOCAL-FIRST ARCHITECTURE",
        "kinetic_2": "Orquestación multi-agente con n8n integrado y soberanía de datos.",
        "sub_2": "🤖 AGENTES AUTÓNOMOS REALES",
        "theme": "cyan",
        "start_time": "00:00:01.0",
        "duration": 18.5
    },
    {
        "id": "reel_10",
        "audio_source": "sIA_DeepDive_Jev_TypeSafe_Sistema1.mp3",
        "output_reel": "sIA_Reel_10_Jev_TypeSafe_Sistema1.mp4",
        "badge_tag": "sIA DEEP DIVE",
        "category_name": "IA & ARQUITECTURA",
        "pill_text": "🎯 DECISIONES DETERMINISTAS",
        "hook_title": "¿Por qué usar un LLM para tomar decisiones es el <span class=\"hl\">peor error de ingeniería</span>?",
        "kinetic_1": "Los LLMs sufren alucinación no acotada y varianza estocástica en producción.",
        "sub_1": "⚠️ EL DILEMA DEL SISTEMA 2",
        "kinetic_2": "Jev impone tipado estricto (choice, score, boolean) a velocidad de Sistema 1.",
        "sub_2": "⚡ LATENCIA SUB-10MS",
        "theme": "cyan",
        "start_time": "00:00:01.0",
        "duration": 18.5
    },
    {
        "id": "reel_11",
        "audio_source": "sIA_DeepDive_Bambu_Lab_Impresion_3D.mp3",
        "output_reel": "sIA_Reel_11_Bambu_Lab_LiDAR.mp4",
        "badge_tag": "sIA DEEP DIVE",
        "category_name": "IMPRESIÓN 3D",
        "pill_text": "🖨️ REVOLUCIÓN MAKER",
        "hook_title": "¿Cómo Bambu Lab humilló a la industria tradicional de <span class=\"hl\">impresión 3D</span>?",
        "kinetic_1": "Micro-LiDAR de doble haz para calibración de flujo en tiempo real.",
        "sub_1": "🔍 VISIÓN POR COMPUTADORA",
        "kinetic_2": "Compensación de resonancia activa y control térmico en cámara cerrada.",
        "sub_2": "🚀 500 MM/S SIN ERRORES",
        "theme": "emerald",
        "start_time": "00:00:01.0",
        "duration": 18.5
    },
    {
        "id": "reel_12",
        "audio_source": "sIA_DeepDive_Edge_AI_Galaxy_S25_Insta360.mp3",
        "output_reel": "sIA_Reel_12_Edge_AI_Galaxy_S25.mp4",
        "badge_tag": "sIA DEEP DIVE",
        "category_name": "EDGE COMPUTING",
        "pill_text": "📱 SILICIO LOCAL • NPU",
        "hook_title": "El verdadero poder de la IA no está en la nube... está en el <span class=\"hl\">silicio de tu bolsillo</span>.",
        "kinetic_1": "NPU del Galaxy S25 ejecutando modelos SLM de 7B parámetros sin internet.",
        "sub_1": "⚡ LATENCIA CERO EN EL BORDE",
        "kinetic_2": "Y visión computacional 8K en Insta360 X4 para stitching en tiempo real.",
        "sub_2": "👁️ FOTOGRAMETRÍA PORTÁTIL",
        "theme": "amber",
        "start_time": "00:00:01.0",
        "duration": 18.5
    },
    {
        "id": "reel_13",
        "audio_source": "sIA_DeepDive_MCP_Agentes_Produccion.mp3",
        "output_reel": "sIA_Reel_13_MCP_Agentes_Produccion.mp4",
        "badge_tag": "sIA DEEP DIVE",
        "category_name": "AGENTIC PROTOCOLS",
        "pill_text": "🌐 EL NUEVO ESTÁNDAR",
        "hook_title": "Las APIs REST están muriendo. El futuro de los agentes se llama <span class=\"hl\">Model Context Protocol</span>.",
        "kinetic_1": "Anthropic estandarizó cómo los LLMs se conectan a bases de datos y herramientas.",
        "sub_1": "🔌 BUS DE INTEROPERABILIDAD",
        "kinetic_2": "Arquitectura cliente-servidor con tipado estricto y contexto dinámico.",
        "sub_2": "🛠️ AGENTES EN PRODUCCIÓN",
        "theme": "cyan",
        "start_time": "00:00:01.0",
        "duration": 18.5
    },
    {
        "id": "reel_14",
        "audio_source": "sIA_Episodio_02_Arquitectos_de_Contexto.mp3",
        "output_reel": "sIA_Reel_14_Arquitectos_de_Contexto.mp4",
        "badge_tag": "sIA #02",
        "category_name": "CULTURA & CÓDIGO",
        "pill_text": "🧩 VIBE CODING TRAP",
        "hook_title": "¿Vibe coding te hace programador o solo un <span class=\"hl\">espectador de lo que genera la IA</span>?",
        "kinetic_1": "La ilusión de competencia: escribir sin entender vs vibe reviewing con criterio.",
        "sub_1": "⚠️ EL RIESGO DE DEUDA TÉCNICA",
        "kinetic_2": "De plomeros de datos a arquitectos de contexto con Google Antigravity.",
        "sub_2": "🏗️ SISTEMA CARDINAL MODERNO",
        "theme": "violet",
        "start_time": "00:00:01.0",
        "duration": 18.5
    }
]

def init_engine_scaffold():
    """Initializes the HyperFrames project scaffold inside ENGINE_DIR."""
    (ENGINE_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (ENGINE_DIR / "compositions").mkdir(parents=True, exist_ok=True)
    (ENGINE_DIR / "renders").mkdir(parents=True, exist_ok=True)

    # hyperframes.json
    hf_json = {
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {
            "blocks": "compositions",
            "components": "compositions/components",
            "assets": "assets"
        },
        "media": {
            "autoProxy": True
        }
    }
    with open(ENGINE_DIR / "hyperframes.json", "w", encoding="utf-8") as f:
        json.dump(hf_json, f, indent=2)

    # meta.json
    meta_json = {
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "defaultDuration": 18.5,
        "resolutions": ["portrait"]
    }
    with open(ENGINE_DIR / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta_json, f, indent=2)

    # package.json
    pkg_json = {
        "name": "sia-tiktok-batch-engine",
        "version": "1.0.0",
        "private": True,
        "type": "module"
    }
    with open(ENGINE_DIR / "package.json", "w", encoding="utf-8") as f:
        json.dump(pkg_json, f, indent=2)

def extract_audio_clip(source_mp3: Path, target_clip: Path, start_time: str, duration: float):
    """Extracts a high quality 192k audio clip from episode MP3 using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", str(source_mp3),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-af", "afade=t=out:st=17.5:d=1.0",
        str(target_clip)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_index_html(duration: float):
    return f"""<!doctype html>
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
        background: #030508;
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
    <div id="root" data-composition-id="sia_batch_reel" data-no-timeline data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{duration}"
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
        data-duration="{duration}"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>
"""

def generate_scene_html(reel_info: dict):
    theme_cfg = THEMES.get(reel_info["theme"], THEMES["cyan"])
    duration = reel_info["duration"]

    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #020408;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
      }}
      #scene-root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        background: radial-gradient(circle at 50% 25%, {theme_cfg['bg_radial_1']} 0%, transparent 65%),
                    radial-gradient(circle at 80% 80%, {theme_cfg['bg_radial_2']} 0%, transparent 55%),
                    #020408;
        overflow: hidden;
      }}

      /* Dynamic Atmospheric Grid */
      .grid-bg {{
        position: absolute;
        inset: 0;
        background-size: 80px 80px;
        background-image: 
          linear-gradient(to right, rgba(255, 255, 255, 0.04) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
        mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 40%, rgba(0,0,0,0) 85%);
      }}

      /* Top Header Elements */
      .header-wrap {{
        position: absolute;
        top: 100px;
        left: 70px;
        right: 70px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }}
      .badge-brand {{
        display: flex;
        align-items: center;
        gap: 16px;
        background: {theme_cfg['badge_brand_bg']};
        border: 1px solid {theme_cfg['badge_brand_border']};
        padding: 12px 24px;
        border-radius: 9999px;
        backdrop-filter: blur(12px);
      }}
      .badge-brand .dot {{
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: {theme_cfg['primary']};
        box-shadow: 0 0 18px {theme_cfg['primary_glow']};
      }}
      .badge-brand span {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: {theme_cfg['badge_brand_text']};
      }}
      .badge-category {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 600;
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.06);
        padding: 10px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.12);
      }}

      /* Topic Pill Badge */
      .topic-pill {{
        position: absolute;
        top: 240px;
        left: 70px;
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: {theme_cfg['pill_bg']};
        border: 1px solid {theme_cfg['pill_border']};
        padding: 10px 24px;
        border-radius: 9999px;
        font-size: 24px;
        font-weight: 700;
        color: {theme_cfg['pill_text']};
        backdrop-filter: blur(8px);
      }}

      /* Main Stage Card */
      .stage-card {{
        position: absolute;
        top: 340px;
        left: 70px;
        right: 70px;
        background: rgba(10, 14, 23, 0.88);
        border: 1px solid {theme_cfg['card_border']};
        border-radius: 36px;
        padding: 56px 48px;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(24px);
      }}
      .stage-card .post-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: {theme_cfg['primary']};
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 24px;
      }}
      .stage-card h1.main-hook {{
        font-size: 52px;
        line-height: 1.25;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
      }}
      .hl {{
        color: {theme_cfg['highlight_color']};
        text-decoration: underline;
        text-decoration-color: {theme_cfg['primary_glow']};
        text-underline-offset: 8px;
      }}

      /* Kinetic Takeaway Box */
      .kinetic-box {{
        position: absolute;
        top: 920px;
        left: 70px;
        right: 70px;
        background: linear-gradient(135deg, rgba(24, 24, 27, 0.9), rgba(9, 9, 11, 0.95));
        border: 1px solid {theme_cfg['card_border']};
        border-radius: 28px;
        padding: 44px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(16px);
      }}
      .kinetic-text {{
        font-size: 38px;
        font-weight: 700;
        line-height: 1.35;
        color: #f1f5f9;
        margin-bottom: 16px;
      }}
      .kinetic-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 600;
        color: {theme_cfg['primary']};
        display: flex;
        align-items: center;
        gap: 12px;
      }}

      /* Audio Visualizer Waveform */
      .eq-container {{
        position: absolute;
        bottom: 300px;
        left: 70px;
        right: 70px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 0 40px;
        backdrop-filter: blur(10px);
      }}
      .eq-bar {{
        width: 14px;
        height: 30px;
        background: {theme_cfg['eq_gradient']};
        border-radius: 9999px;
        box-shadow: 0 0 14px {theme_cfg['primary_glow']};
        transform-origin: center;
      }}

      /* Footer Branding & Spotify Pill */
      .footer-cta {{
        position: absolute;
        bottom: 120px;
        left: 70px;
        right: 70px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px 36px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid {theme_cfg['card_border']};
        border-radius: 9999px;
        backdrop-filter: blur(16px);
      }}
      .footer-left {{
        display: flex;
        align-items: center;
        gap: 20px;
      }}
      .spotify-icon {{
        width: 54px;
        height: 54px;
        border-radius: 50%;
        background: #1db954;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.4);
      }}
      .footer-text h4 {{
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
      }}
      .footer-text p {{
        font-size: 20px;
        font-weight: 500;
        color: #94a3b8;
      }}
      .listen-btn {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        background: {theme_cfg['btn_bg']};
        padding: 14px 28px;
        border-radius: 9999px;
        box-shadow: 0 0 25px {theme_cfg['primary_glow']};
      }}
    </style>
  </head>
  <body>
    <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920">
      <div class="grid-bg"></div>

      <!-- Top Header -->
      <div class="header-wrap" id="header">
        <div class="badge-brand">
          <div class="dot"></div>
          <span>{reel_info['badge_tag']}</span>
        </div>
        <div class="badge-category">{reel_info['category_name']}</div>
      </div>

      <!-- Topic Pill -->
      <div class="topic-pill" id="topic-tag">
        <span>{reel_info['pill_text']}</span>
      </div>

      <!-- Central Stage Card -->
      <div class="stage-card" id="main-card">
        <div class="post-tag">DEBATE EN PRODUCCIÓN</div>
        <h1 class="main-hook">
          "{reel_info['hook_title']}"
        </h1>
      </div>

      <!-- Kinetic Changing Text Box -->
      <div class="kinetic-box" id="kinetic-card">
        <div id="kinetic-phrase-1" style="display: block;">
          <p class="kinetic-text">{reel_info['kinetic_1']}</p>
          <p class="kinetic-sub">{reel_info['sub_1']}</p>
        </div>
        <div id="kinetic-phrase-2" style="display: none;">
          <p class="kinetic-text">{reel_info['kinetic_2']}</p>
          <p class="kinetic-sub">{reel_info['sub_2']}</p>
        </div>
      </div>

      <!-- Waveform Bars -->
      <div class="eq-container" id="eq-bars">
        <div class="eq-bar" id="b1"></div>
        <div class="eq-bar" id="b2"></div>
        <div class="eq-bar" id="b3"></div>
        <div class="eq-bar" id="b4"></div>
        <div class="eq-bar" id="b5"></div>
        <div class="eq-bar" id="b6"></div>
        <div class="eq-bar" id="b7"></div>
        <div class="eq-bar" id="b8"></div>
        <div class="eq-bar" id="b9"></div>
        <div class="eq-bar" id="b10"></div>
        <div class="eq-bar" id="b11"></div>
        <div class="eq-bar" id="b12"></div>
        <div class="eq-bar" id="b13"></div>
        <div class="eq-bar" id="b14"></div>
        <div class="eq-bar" id="b15"></div>
        <div class="eq-bar" id="b16"></div>
      </div>

      <!-- Footer CTA -->
      <div class="footer-cta" id="footer">
        <div class="footer-left">
          <div class="spotify-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="#000000">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.52 17.3c-.2.35-.68.46-1.03.25-2.82-1.72-6.37-2.11-10.55-1.16-.4.09-.81-.16-.9-.56-.09-.4.16-.81.56-.9 4.58-1.05 8.5-.61 11.66 1.34.36.21.47.68.26 1.03zm1.47-3.26c-.27.44-.85.59-1.3.31-3.22-1.98-8.14-2.56-11.95-1.4-.5.15-1.03-.13-1.18-.63-.15-.5.13-1.03.63-1.18 4.36-1.33 9.78-.68 13.48 1.6.45.27.59.85.32 1.3zm.13-3.41c-3.87-2.3-10.25-2.51-13.94-1.39-.6.18-1.22-.16-1.4-.75-.18-.6.16-1.22.75-1.4 4.24-1.29 11.29-1.04 15.73 1.6.54.32.71 1.01.39 1.55-.32.53-1.01.71-1.53.39z"/>
            </svg>
          </div>
          <div class="footer-text">
            <h4>sIA Podcast</h4>
            <p>escucha-sia.github.io</p>
          </div>
        </div>
        <div class="listen-btn">ESCUCHAR EN SPOTIFY</div>
      </div>
    </div>

    <!-- GSAP Master Animation Timeline -->
    <script>
      const tl = gsap.timeline({{ paused: true }});

      // 1. Entrance of Header & Card
      tl.fromTo("#header", {{ y: -50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, 0.2);
      tl.fromTo("#topic-tag", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, 0.5);
      tl.fromTo("#main-card", {{ y: 60, opacity: 0, scale: 0.95 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.8, ease: "power4.out" }}, 0.8);
      tl.fromTo("#footer", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, 1.0);

      // 2. Kinetic Card Entrance & Flip
      tl.fromTo("#kinetic-card", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, ease: "power3.out" }}, 5.5);

      // Switch phrase at 11.5s deterministically
      tl.to("#kinetic-phrase-1", {{ opacity: 0, y: -20, duration: 0.4 }}, 11.5);
      tl.set("#kinetic-phrase-1", {{ display: "none" }}, 11.9);
      tl.set("#kinetic-phrase-2", {{ display: "block" }}, 11.9);
      tl.fromTo("#kinetic-phrase-2", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 12.0);

      // 3. Audio Bars Animation (Waveform Simulation)
      const deterministicHeights = [90, 40, 100, 35, 70, 85, 45, 95, 60, 90, 40, 80, 50, 95, 35, 75];
      const bars = document.querySelectorAll(".eq-bar");
      bars.forEach((bar, i) => {{
        const targetH = deterministicHeights[i % deterministicHeights.length];
        tl.to(bar, {{
          height: targetH,
          repeat: 45,
          yoyo: true,
          duration: 0.25 + (i % 5) * 0.05,
          ease: "sine.inOut"
        }}, 0);
      }});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["scene"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

def render_reel(reel_info: dict):
    print(f"\n==================================================")
    print(f"🎬 RENDERIZANDO REEL: {reel_info['badge_tag']} - {reel_info['output_reel']}")
    print(f"==================================================")

    source_audio = AUDIO_DIR / reel_info["audio_source"]
    if not source_audio.exists():
        print(f"❌ Error: No existe el audio original {source_audio}")
        return False

    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    print(f"✂️ Extrayendo clip teaser de {reel_info['duration']}s desde {reel_info['start_time']}...")
    extract_audio_clip(source_audio, clip_audio, reel_info["start_time"], reel_info["duration"])

    # Write index.html and scene.html
    with open(ENGINE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(generate_index_html(reel_info["duration"]))

    with open(ENGINE_DIR / "compositions" / "scene.html", "w", encoding="utf-8") as f:
        f.write(generate_scene_html(reel_info))

    render_mp4 = ENGINE_DIR / "renders" / reel_info["output_reel"]
    if render_mp4.exists():
        render_mp4.unlink()

    # Render with HyperFrames CLI
    print(f"⚡ Ejecutando 'npx hyperframes render --gpu'...")
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    cmd = [
        "cmd.exe", "/c",
        f"npx hyperframes render --gpu --output renders/{reel_info['output_reel']}"
    ]
    proc = subprocess.run(cmd, cwd=str(ENGINE_DIR), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if proc.returncode != 0 or not render_mp4.exists():
        print(f"❌ Error al renderizar con HyperFrames:\n{proc.stderr}\n{proc.stdout}")
        return False

    # Extract poster
    poster_fn = Path(reel_info["output_reel"]).stem + "_poster.jpg"
    poster_path = REELS_DIR / poster_fn
    target_mp4 = REELS_DIR / reel_info["output_reel"]

    print(f"📸 Extrayendo poster frame a {poster_path}...")
    shutil.copy2(render_mp4, target_mp4)
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "00:00:02",
        "-i", str(target_mp4),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Sync to Spotify Reels folder
    spotify_mp4 = SPOTIFY_REELS_DIR / reel_info["output_reel"]
    spotify_poster = SPOTIFY_REELS_DIR / poster_fn
    shutil.copy2(target_mp4, spotify_mp4)
    shutil.copy2(poster_path, spotify_poster)

    file_size_mb = target_mp4.stat().st_size / (1024 * 1024)
    print(f"✅ Reel generado con éxito: {reel_info['output_reel']} ({file_size_mb:.2f} MB)")
    print(f"   -> Copiado a {target_mp4}")
    print(f"   -> Sincronizado a {spotify_mp4}")
    return True

def main():
    init_engine_scaffold()
    
    # Check if a specific reel ID was passed via CLI
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    rendered_count = 0
    for reel in REELS_CATALOG:
        if target_id and reel["id"] != target_id and reel["output_reel"] != target_id:
            continue
        success = render_reel(reel)
        if success:
            rendered_count += 1

    print(f"\n🎉 Batch Render Completado: {rendered_count} reels generados exitosamente.")

if __name__ == "__main__":
    main()
