"""
sIA Visual TikTok & Reels Infographic Generator (HyperFrames + GPU + Diagrams)
Genera videos verticales (1080x1920) de alto impacto visual con:
- Diagramas y esquemas técnicos reales generados en alta resolución en el Hero Stage.
- Línea láser animada de escaneo continuo (scanline) con GSAP.
- HUD holográfico con esquinas de calibración y badges de telemetría activa.
- Subtítulos cinemáticos con indicador de locutor (Jorge vs Dalia).
- Ecualizador reactivo y embudo directo a Spotify y al Blog con código y APA.
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
IMAGES_DIR = BASE_DIR / "assets" / "images"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
NODE_PATH = r"C:\Carlos\nodejs"

REELS_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)
ENGINE_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

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
        "card_border": "rgba(6, 182, 212, 0.4)",
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
        "card_border": "rgba(168, 85, 247, 0.4)",
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
        "card_border": "rgba(245, 158, 11, 0.4)",
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
        "card_border": "rgba(16, 185, 129, 0.4)",
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
        "card_border": "rgba(139, 92, 246, 0.4)",
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
        "card_border": "rgba(239, 68, 68, 0.4)",
        "badge_brand_bg": "rgba(239, 68, 68, 0.12)",
        "badge_brand_border": "rgba(239, 68, 68, 0.4)",
        "badge_brand_text": "#fca5a5",
        "highlight_color": "#f87171",
    }
}

REELS_CATALOG = [
    {
        "id": "reel_terror_01",
        "audio_source": "sIA_Terror_01_Las_Escaleras_del_Bosque_2026-10-15.mp3",
        "output_reel": "sIA_Terror_01_Las_Escaleras_Reel.mp4",
        "badge_tag": "sIA TERROR #01",
        "category_name": "RELATOS DE REDDIT",
        "pill_text": "💀 r/nosleep • TESTIMONIO SAR",
        "hook_title": "Si en mitad del bosque denso ves una <span class=\"hl\">escalera solitaria</span>... JAMÁS subas.",
        "diagram_image": "reel_visual_terror_stairs.jpg",
        "hud_tag": "ANOMALÍA SAR • BOSQUE PROFUNDO",
        "kinetic_1": "No hay cabañas ni cimientos. Solo escalones limpios hacia la nada.",
        "speaker_1": "OFICIAL DE BÚSQUEDA & RESCATE",
        "kinetic_2": "Regla no escrita del bosque: ignórala y no mires hacia arriba.",
        "speaker_2": "PROTOCOLO DE EMERGENCIA",
        "theme": "red",
        "start_time": "00:00:00.0",
        "duration": 18.5
    },
    {
        "id": "reel_15",
        "audio_source": "sIA_Daily_S01_IA_JEPA_Modelos_de_Mundo_2026-10-15.mp3",
        "output_reel": "sIA_Reel_15_Modelos_JEPA_Mundo.mp4",
        "badge_tag": "sIA #39",
        "category_name": "IA & AGENTES",
        "pill_text": "🧠 WORLD MODELS • JEPA",
        "hook_title": "¿Por qué predecir tokens de texto <span class=\"hl\">jamás entenderá el mundo físico</span>?",
        "diagram_image": "reel_visual_jepa_diagram.jpg",
        "hud_tag": "LATENT SPACE • ENCODING",
        "kinetic_1": "Los LLMs acumulan error exponencial: no tienen noción de inercia ni masa.",
        "speaker_1": "JORGE (INFRAESTRUCTURA)",
        "kinetic_2": "JEPA predice en espacio latente abstracto: causalidad física con latencia cero.",
        "speaker_2": "DALIA (ARQUITECTURA)",
        "theme": "cyan",
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
        "diagram_image": "reel_visual_bambu_lidar.jpg",
        "hud_tag": "COREXY • DUAL MICRO-LIDAR",
        "kinetic_1": "Flujo volumétrico y compensación activa de resonancia a 500 mm/s.",
        "speaker_1": "JORGE (FABRICACIÓN ADITIVA)",
        "kinetic_2": "El salto a la impresión 4D: metamateriales térmicos que mutan de forma.",
        "speaker_2": "DALIA (INGENIERÍA)",
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
        "diagram_image": "reel_visual_ereader_drm.jpg",
        "hud_tag": "CALIBRE vs CLOUD SILO",
        "kinetic_1": "Cierre del DRM en e-readers y el escape hacia KOReader y almacenamiento local.",
        "speaker_1": "JORGE (SOBERANÍA)",
        "kinetic_2": "Pantallas electroquímicas reflectivas a 60 fps bajo la luz solar directa.",
        "speaker_2": "DALIA (HARDWARE)",
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
        "diagram_image": "reel_visual_data_contracts.jpg",
        "hud_tag": "YAML GATE • SCHEMA ENGINE",
        "kinetic_1": "Validación estricta de esquemas en YAML antes de que toquen producción.",
        "speaker_1": "JORGE (DATA PIPELINES)",
        "kinetic_2": "Y consultas SQL sobre datos cifrados en memoria con criptografía homomórfica.",
        "speaker_2": "DALIA (CLOUD SECURITY)",
        "theme": "purple",
        "start_time": "00:00:00.5",
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
        "diagram_image": "reel_visual_jev_system1.jpg",
        "hud_tag": "SISTEMA 1 • LATENCIA 3.8ms",
        "kinetic_1": "Los LLMs sufren alucinación no acotada y varianza estocástica en producción.",
        "speaker_1": "JORGE (PRODUCCIÓN)",
        "kinetic_2": "Jev impone tipado estricto (choice, score, boolean) a velocidad de Sistema 1.",
        "speaker_2": "DALIA (DECISION MODELS)",
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
        "diagram_image": "reel_visual_bambu_lidar.jpg",
        "hud_tag": "MICRO-LIDAR • 500 MM/S",
        "kinetic_1": "Micro-LiDAR de doble haz para calibración de flujo en tiempo real.",
        "speaker_1": "JORGE (MAKER EXPERT)",
        "kinetic_2": "Compensación de resonancia activa y control térmico en cámara cerrada.",
        "speaker_2": "DALIA (INGENIERÍA)",
        "theme": "emerald",
        "start_time": "00:00:01.0",
        "duration": 18.5
    },
    {
        "id": "reel_05",
        "audio_source": "sIA_Daily_S05_Geek_Horror_FullDive_VR_2026-10-12.mp3",
        "output_reel": "sIA_Reel_05_Horror_Psicologico_FullDive.mp4",
        "badge_tag": "sIA #38",
        "category_name": "CULTURA GEEK",
        "pill_text": "🧠 HORROR & VR • ANÁLISIS",
        "hook_title": "¿Puede una IA simular <span class=\"hl\">terror psicológico real</span> o nuestro cerebro sabe que finge?",
        "diagram_image": "reel_visual_terror_stairs.jpg",
        "hud_tag": "FULL-DIVE VR • NEUROCIENCIA",
        "kinetic_1": "En Silent Hill y SAO, el miedo no es el monstruo... es la incertidumbre.",
        "speaker_1": "JORGE (CULTURA GEEK)",
        "kinetic_2": "Si la máquina induce pánico sensorial, ¿dónde termina el software?",
        "speaker_2": "DALIA (NEUROCIENCIA)",
        "theme": "violet",
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
        "diagram_image": "reel_visual_jepa_diagram.jpg",
        "hud_tag": "TAURI V2 • LOCAL-FIRST",
        "kinetic_1": "Tauri v2, Svelte 5 y FastAPI corriendo en tu propia GPU sin telemetría.",
        "speaker_1": "JORGE (DEVOPS)",
        "kinetic_2": "Orquestación multi-agente con n8n integrado y soberanía de datos.",
        "speaker_2": "DALIA (ARQUITECTURA)",
        "theme": "cyan",
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
        "diagram_image": "reel_visual_data_contracts.jpg",
        "hud_tag": "MCP PROTOCOL • ANTHROPIC",
        "kinetic_1": "Anthropic estandarizó cómo los LLMs se conectan a bases de datos y herramientas.",
        "speaker_1": "JORGE (BUS DE DATOS)",
        "kinetic_2": "Arquitectura cliente-servidor con tipado estricto y contexto dinámico.",
        "speaker_2": "DALIA (INGENIERÍA)",
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
        "diagram_image": "reel_visual_jepa_diagram.jpg",
        "hud_tag": "ANTIGRAVITY • VIBE REVIEWING",
        "kinetic_1": "La ilusión de competencia: escribir sin entender vs vibe reviewing con criterio.",
        "speaker_1": "JORGE (SENIOR ENGINEER)",
        "kinetic_2": "De plomeros de datos a arquitectos de contexto con Google Antigravity.",
        "speaker_2": "DALIA (ARQUITECTURA)",
        "theme": "violet",
        "start_time": "00:00:01.0",
        "duration": 18.5
    }
]

def init_engine_scaffold():
    (ENGINE_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (ENGINE_DIR / "compositions").mkdir(parents=True, exist_ok=True)
    (ENGINE_DIR / "renders").mkdir(parents=True, exist_ok=True)

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

    meta_json = {
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "defaultDuration": 18.5,
        "resolutions": ["portrait"]
    }
    with open(ENGINE_DIR / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta_json, f, indent=2)

    pkg_json = {
        "name": "sia-tiktok-batch-engine",
        "version": "1.0.0",
        "private": True,
        "type": "module"
    }
    with open(ENGINE_DIR / "package.json", "w", encoding="utf-8") as f:
        json.dump(pkg_json, f, indent=2)

def extract_audio_clip(source_mp3: Path, target_clip: Path, start_time: str, duration: float):
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
        background: #020408;
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
    hud_tag = reel_info.get("hud_tag", "TECHNICAL ARCHITECTURE")
    speaker_1 = reel_info.get("speaker_1", "JORGE")
    speaker_2 = reel_info.get("speaker_2", "DALIA")

    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
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
        background: radial-gradient(circle at 50% 15%, {theme_cfg['bg_radial_1']} 0%, transparent 60%),
                    radial-gradient(circle at 80% 85%, {theme_cfg['bg_radial_2']} 0%, transparent 55%),
                    #020408;
        overflow: hidden;
      }}

      /* Dynamic Atmospheric Grid */
      .grid-bg {{
        position: absolute;
        inset: 0;
        background-size: 80px 80px;
        background-image: 
          linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 40%, rgba(0,0,0,0) 85%);
      }}

      /* Top Header Elements */
      .header-wrap {{
        position: absolute;
        top: 60px;
        left: 60px;
        right: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 20;
      }}
      .badge-brand {{
        display: flex;
        align-items: center;
        gap: 14px;
        background: {theme_cfg['badge_brand_bg']};
        border: 1px solid {theme_cfg['badge_brand_border']};
        padding: 10px 22px;
        border-radius: 9999px;
        backdrop-filter: blur(12px);
      }}
      .badge-brand .dot {{
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: {theme_cfg['primary']};
        box-shadow: 0 0 16px {theme_cfg['primary_glow']};
      }}
      .badge-brand span {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: {theme_cfg['badge_brand_text']};
      }}
      .badge-category {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 700;
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.06);
        padding: 8px 18px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.12);
      }}

      /* Hook Question Card */
      .hook-card {{
        position: absolute;
        top: 150px;
        left: 60px;
        right: 60px;
        background: rgba(10, 14, 23, 0.90);
        border: 1px solid {theme_cfg['card_border']};
        border-radius: 28px;
        padding: 24px 32px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(20px);
        z-index: 15;
      }}
      .hook-card .topic-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: {theme_cfg['primary']};
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 10px;
      }}
      .hook-card h1.main-hook {{
        font-size: 34px;
        line-height: 1.25;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
      }}
      .hl {{
        color: {theme_cfg['highlight_color']};
        text-decoration: underline;
        text-decoration-color: {theme_cfg['primary_glow']};
        text-underline-offset: 6px;
      }}

      /* HERO VISUAL SCHEMATIC STAGE */
      .schematic-stage {{
        position: absolute;
        top: 360px;
        left: 60px;
        right: 60px;
        height: 1060px;
        background: rgba(8, 12, 20, 0.95);
        border: 2px solid {theme_cfg['card_border']};
        border-radius: 32px;
        padding: 14px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8),
                    0 0 35px {theme_cfg['primary_glow']};
        backdrop-filter: blur(24px);
        overflow: hidden;
        z-index: 10;
      }}
      .schematic-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        border-radius: 22px;
        overflow: hidden;
        background: #000;
      }}
      .schematic-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center top;
        display: block;
      }}
      .scanline {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, transparent, {theme_cfg['primary']}, #ffffff, {theme_cfg['primary']}, transparent);
        box-shadow: 0 0 25px {theme_cfg['primary']}, 0 0 12px #ffffff;
        opacity: 0.9;
        z-index: 12;
      }}
      .hud-overlay {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 14;
      }}
      .hud-badge {{
        position: absolute;
        top: 18px;
        right: 18px;
        background: rgba(0, 0, 0, 0.80);
        border: 1px solid {theme_cfg['primary']};
        padding: 8px 18px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 800;
        color: {theme_cfg['primary']};
        letter-spacing: 0.05em;
        backdrop-filter: blur(8px);
        box-shadow: 0 0 18px {theme_cfg['primary_glow']};
      }}
      .hud-corner {{
        position: absolute;
        width: 24px;
        height: 24px;
        border: 2px solid {theme_cfg['primary']};
      }}
      .hud-corner.top-left {{ top: 12px; left: 12px; border-right: none; border-bottom: none; }}
      .hud-corner.bottom-right {{ bottom: 12px; right: 12px; border-left: none; border-top: none; }}

      /* Kinetic Dialogue & Takeaway Box */
      .dialogue-box {{
        position: absolute;
        top: 1450px;
        left: 60px;
        right: 60px;
        height: 180px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(9, 9, 11, 0.96));
        border: 1px solid {theme_cfg['card_border']};
        border-radius: 24px;
        padding: 22px 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(16px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        z-index: 15;
      }}
      .speaker-pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 800;
        color: {theme_cfg['primary']};
        text-transform: uppercase;
        margin-bottom: 8px;
        letter-spacing: 0.05em;
      }}
      .dialogue-text {{
        font-size: 26px;
        font-weight: 700;
        line-height: 1.3;
        color: #f8fafc;
      }}

      /* Audio Visualizer Waveform */
      .eq-container {{
        position: absolute;
        top: 1650px;
        left: 60px;
        right: 60px;
        height: 85px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 0 30px;
        backdrop-filter: blur(10px);
        z-index: 15;
      }}
      .eq-bar {{
        width: 12px;
        height: 25px;
        background: {theme_cfg['eq_gradient']};
        border-radius: 9999px;
        box-shadow: 0 0 14px {theme_cfg['primary_glow']};
        transform-origin: center;
      }}

      /* Footer Branding & Spotify Pill */
      .footer-cta {{
        position: absolute;
        top: 1755px;
        left: 60px;
        right: 60px;
        height: 95px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 32px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid {theme_cfg['card_border']};
        border-radius: 9999px;
        backdrop-filter: blur(16px);
        z-index: 15;
      }}
      .footer-left {{
        display: flex;
        align-items: center;
        gap: 16px;
      }}
      .spotify-icon {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: #1db954;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 18px rgba(29, 185, 84, 0.4);
      }}
      .footer-text h4 {{
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
      }}
      .footer-text p {{
        font-size: 18px;
        font-weight: 500;
        color: #94a3b8;
      }}
      .listen-btn {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        background: {theme_cfg['btn_bg']};
        padding: 12px 24px;
        border-radius: 9999px;
        box-shadow: 0 0 20px {theme_cfg['primary_glow']};
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

      <!-- Hook Question Card -->
      <div class="hook-card" id="main-card">
        <div class="topic-tag">{reel_info['pill_text']}</div>
        <h1 class="main-hook">
          "{reel_info['hook_title']}"
        </h1>
      </div>

      <!-- HERO VISUAL SCHEMATIC / ARCHITECTURE DIAGRAM -->
      <div class="schematic-stage" id="diagram-stage">
        <div class="schematic-inner">
          <img src="assets/current_diagram.jpg" alt="Technical Diagram" class="schematic-img" />
          <div class="scanline" id="scanline"></div>
          <div class="hud-overlay">
            <div class="hud-corner top-left"></div>
            <div class="hud-corner bottom-right"></div>
            <div class="hud-badge" id="hud-badge">{hud_tag}</div>
          </div>
        </div>
      </div>

      <!-- Kinetic Takeaway / Dialogue Box -->
      <div class="dialogue-box" id="kinetic-card">
        <div id="kinetic-phrase-1" style="display: block;">
          <div class="speaker-pill">🎙️ {speaker_1}</div>
          <p class="dialogue-text">{reel_info['kinetic_1']}</p>
        </div>
        <div id="kinetic-phrase-2" style="display: none;">
          <div class="speaker-pill">🎙️ {speaker_2}</div>
          <p class="dialogue-text">{reel_info['kinetic_2']}</p>
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
            <svg width="28" height="28" viewBox="0 0 24 24" fill="#000000">
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

      // 1. Entrance of Header, Main Hook Card & Footer
      tl.fromTo("#header", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 0.2);
      tl.fromTo("#main-card", {{ y: 30, opacity: 0, scale: 0.97 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.6, ease: "power4.out" }}, 0.5);
      tl.fromTo("#footer", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 0.8);

      // 2. Entrance of Hero Schematic Stage & Laser Scanline
      tl.fromTo("#diagram-stage", {{ scale: 0.94, opacity: 0, y: 30 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, 0.6);
      tl.fromTo("#hud-badge", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, 1.0);
      
      // Continuous Laser Scanline Sweep down the diagram
      tl.fromTo("#scanline", {{ top: "0%" }}, {{ top: "100%", repeat: -1, duration: 2.6, ease: "linear" }}, 0);

      // 3. Kinetic Dialogue Box Entrance & Flip
      tl.fromTo("#kinetic-card", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, 1.2);

      // Switch phrase at 11.5s deterministically
      tl.to("#kinetic-phrase-1", {{ opacity: 0, y: -15, duration: 0.35 }}, 11.5);
      tl.set("#kinetic-phrase-1", {{ display: "none" }}, 11.85);
      tl.set("#kinetic-phrase-2", {{ display: "block" }}, 11.85);
      tl.fromTo("#kinetic-phrase-2", {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 11.9);

      // 4. Audio Bars Animation (Waveform Simulation)
      const deterministicHeights = [70, 30, 80, 25, 60, 75, 35, 75, 50, 70, 30, 65, 40, 75, 25, 60];
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
    print(f"🎬 RENDERIZANDO REEL CON ESQUEMA TÉCNICO: {reel_info['badge_tag']} - {reel_info['output_reel']}")
    print(f"==================================================")

    source_audio = AUDIO_DIR / reel_info["audio_source"]
    if not source_audio.exists():
        print(f"❌ Error: No existe el audio original {source_audio}")
        return False

    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    print(f"✂️ Extrayendo clip teaser de {reel_info['duration']}s desde {reel_info['start_time']}...")
    extract_audio_clip(source_audio, clip_audio, reel_info["start_time"], reel_info["duration"])

    # Copy technical diagram image
    diagram_fn = reel_info.get("diagram_image") or "reel_visual_jepa_diagram.jpg"
    diagram_src = IMAGES_DIR / diagram_fn
    diagram_dst = ENGINE_DIR / "assets" / "current_diagram.jpg"
    if diagram_src.exists():
        shutil.copy2(diagram_src, diagram_dst)
        print(f"🖼️ Esquema técnico cargado: {diagram_fn}")
    else:
        print(f"⚠️ Aviso: No se encontró {diagram_src}, buscando alternativo...")
        fallbacks = list(IMAGES_DIR.glob("*.jpg"))
        if fallbacks:
            shutil.copy2(fallbacks[0], diagram_dst)

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
    print(f"✅ Reel con diagrama generado con éxito: {reel_info['output_reel']} ({file_size_mb:.2f} MB)")
    print(f"   -> Copiado a {target_mp4}")
    print(f"   -> Sincronizado a {spotify_mp4}")
    return True

def main():
    init_engine_scaffold()
    
    target_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    rendered_count = 0
    for reel in REELS_CATALOG:
        if target_id and reel["id"] != target_id and reel["output_reel"] != target_id:
            continue
        success = render_reel(reel)
        if success:
            rendered_count += 1

    print(f"\n🎉 Renderizado con Diagramas Visuales Completado: {rendered_count} reels generados.")

if __name__ == "__main__":
    main()
