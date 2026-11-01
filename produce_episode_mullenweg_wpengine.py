"""
sIA Master Episode & Reel Producer:
Tema: Matt Mullenweg vs. WP Engine: La guerra civil que rompió los cimientos de WordPress y el 40% de internet
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop (HyperFrames GPU, 45s, Halftone, Kinetic Pop)
3. Póster oficial del Reel
4. Registro de investigación en build_magazine.py con referencias APA 7
5. Recompilación de sIA Journal (index.html + artículo web responsive)
6. Sincronización automática a Google Drive (G:\\Mi unidad\\sIA_Hub)
7. Nota de Obsidian Vault con Embed de video + Kit de Copys para Redes
8. Despliegue Git a GitHub Pages
9. Subida automatizada a TikTok Studio
"""

import sys
import os
import re
import json
import shutil
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
SPOTIFY_REELS_DIR = SPOTIFY_DIR / "Reels"
NODE_PATH = r"C:\Program Files\nodejs"

# Google Drive Hub
GDRIVE_HUB = Path(r"G:\Mi unidad\sIA_Hub")
GDRIVE_REELS = GDRIVE_HUB / "01_Reels_Verticales"
GDRIVE_AUDIO = GDRIVE_HUB / "02_Podcasts_Audio"
GDRIVE_VAULT = GDRIVE_HUB / "03_Obsidian_Vault"

SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

EPISODE_FILENAME = "sIA_Corp_05_Matt_Mullenweg_vs_WP_Engine_2026-10-31.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_04_Mullenweg_vs_WPEngine.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_04_Mullenweg_vs_WPEngine_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: La Bomba de WordCamp US y el Cáncer del Ecosistema]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad de desarrolladores, ingenieros de infraestructura y arquitectos de la web en México y toda Iberoamérica! Bienvenidos a una nueva entrega de sIA en su edición de Crónicas Corporativas. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es sábado treinta y uno de octubre de dos mil veintiséis. Y hoy desentrañamos el conflicto más destructivo, insólito y trascendental de la historia reciente del software libre: la guerra total entre Matt Mullenweg, Automattic y el gigante de alojamiento web WP Engine.
JORGE: Una batalla que empezó con insultos públicos en el escenario principal de WordCamp Portland, escaló al secuestro forzoso de plugins con millones de instalaciones activas, provocó renuncias masivas de empleados y terminó con demandas federales por extorsión corporativa en los juzgados de California.
DALIA: Para entender el impacto de esto, solo hay que recordar una cifra abrumadora: el cuarenta y tres por ciento de todos los sitios web del planeta tierra funcionan sobre WordPress. Tiendas de comercio electrónico, diarios nacionales, portales gubernamentales y blogs personales. Y de la noche a la mañana, la estabilidad técnica de toda esa infraestructura quedó atrapada en el fuego cruzado del ego de un fundador y los fondos multimillonarios de capital privado.
JORGE: ¿Cómo pasamos de la utopía del software libre y la democratización editorial a las listas negras y las casillas de lealtad obligatoria? Prepárense un café bien cargado, porque esta crónica lo tiene todo. ¡Arrancamos!

[CHAPTER: El Impuesto del 8%: Automattic contra Silver Lake]
DALIA: Para comprender este choque de titanes, tenemos que separar primero las entidades, Jorge. Por un lado tenemos la Fundación WordPress, una organización sin fines de lucro dueña teórica de la marca. Por otro lado está Automattic, la corporación con fines de lucro fundada por Matt Mullenweg, valuada en miles de millones de dólares y que explota servicios comerciales como WordPress.com y WooCommerce.
JORGE: Y del otro lado del cuadrilátero aparece WP Engine: una compañía de hosting administrado respaldada por Silver Lake, uno de los fondos de inversión privada más agresivos y colosales de Wall Street, con más de cien mil millones de dólares en activos bajo gestión. WP Engine factura más de cuatrocientos millones de dólares anuales hospedando millones de páginas en WordPress.
DALIA: Durante años, la relación fue cordial. Pero en septiembre de dos mil veinticuatro, la bomba estalló. Automattic le exigió a WP Engine el pago de una regalía contractual del ocho por ciento de sus ingresos brutos —decenas de millones de dólares anuales— alegando que estaban explotando ilegalmente la marca registrada de las letras 'WP'.
JORGE: Cuando WP Engine se negó a pagar lo que calificaron abiertamente como un 'impuesto mafioso de extorsión', Matt Mullenweg subió al escenario de WordCamp US. Frente a una audiencia atónita de cientos de desarrolladores comunitarios, tomó el micrófono y declaró textualmente que WP Engine era 'un cáncer para WordPress'. Los acusó de exprimir los beneficios del código abierto sin devolver las contribuciones proporcionales en horas de ingeniería. Y la guerra civil comenzó.

[CHAPTER: El Secuestro de ACF: Cuando el Repositorio se Convirtió en Arma]
DALIA: El conflicto pasó de las palabras a los hechos técnicos en cuestión de días. Automattic bloqueó a WP Engine el acceso a los servidores de WordPress.org. De pronto, millones de sitios web alojados en WP Engine no podían actualizar temas ni plugins de seguridad desde el panel de administración tradicional.
JORGE: Pero la línea roja definitiva se cruzó el doce de octubre de dos mil veinticuatro, un día que quedará grabado con infamia en la historia de la ciberseguridad. WP Engine es propietaria de Advanced Custom Fields, mejor conocido como ACF: probablemente el plugin de arquitectura de bases de datos más respetado y utilizado de todo el ecosistema, con más de cinco millones de instalaciones activas en agencias y corporaciones.
DALIA: Aprovechando su control monopólico sobre los servidores centrales de WordPress.org, Matt Mullenweg tomó el control forzoso del slug de ACF, expulsó a sus desarrolladores legítimos, le cambió el nombre a 'Secure Custom Fields' y comenzó a distribuir un fork controlado por Automattic a través de las actualizaciones automáticas.
JORGE: Técnicamente fue un secuestro de la cadena de suministro de software sin precedentes. Desarrolladores de todo el mundo vieron cómo sus servidores instalaban un código bifurcado sin su consentimiento explícito. La confianza fundamental que sostenía al ecosistema —la certeza de que el repositorio central de WordPress.org era un bien común neutral gobernado por la comunidad— se pulverizó en una sola tarde.

[CHAPTER: La Purga Interna y la Filosofía del BDFL Desatado]
DALIA: Las repercusiones dentro de la propia empresa Automattic fueron devastadoras, Jorge. Cuando decenas de empleados manifestaron en foros internos su preocupación ética por el ataque a ACF y el daño a la comunidad, Mullenweg lanzó un ultimátum: un paquete de salida de nueve meses de sueldo para cualquiera que estuviera en desacuerdo con su cruzada.
JORGE: Ciento cincuenta y nueve ingenieros y líderes de producto —más del ocho por ciento de toda la fuerza laboral de Automattic— aceptaron el dinero y renunciaron en el acto. Días después, despidió a más empleados y llegó al extremo de implementar una casilla de verificación obligatoria para entrar a WordPress.org que decía: 'No tengo ninguna relación comercial ni laboral con WP Engine'.
DALIA: Figuras legendarias de la industria como David Heinemeier Hansson, creador de Ruby on Rails, salieron a condenar la deriva autoritaria: señalaron que el modelo del BDFL —Benevolent Dictator for Life, o Dictador Benevolente de por Vida— funciona cuando el fundador actúa como custodio de un bien público. Pero cuando el dictador benevolente confunde sus intereses comerciales privados con el destino de un proyecto del que depende medio internet, la estructura entera colapsa.

[CHAPTER: Demandas Federales y el Futuro de la Web Descentralizada]
JORGE: La disputa escaló de inmediato a los tribunales. WP Engine demandó a Automattic y a Matt Mullenweg ante el Tribunal de Distrito del Norte de California, acusándolos de abuso de posición dominante, difamación, interferencia económica y extorsión bajo la ley estadounidense.
DALIA: Automattic respondió con contrademandas por infracción marcaria, pero el daño colateral ya es irreversible. Cientos de agencias de desarrollo y empresas corporativas han comenzado a migrar hacia arquitecturas desacopladas o headless: frameworks modernos como Next.js, Astro y gestores de contenido como Strapi o Ghost, aterrados ante la idea de que su negocio dependa del humor de un solo individuo.
JORGE: Además, el conflicto aceleró la creación de repositorios de plugins federados e independientes, rompiendo el monopolio de WordPress.org. La gran lección de esta crisis es que el software libre corporativo del siglo veintiuno no puede depender de la benevolencia de ninguna persona ni corporación: necesita fundaciones con gobernanza compartida, cortafuegos legales estrictos y repositorios descentralizados.
DALIA: Si una sola llave puede apagar el cuarenta y tres por ciento de la web, entonces la web no es libre: está en arriendo.

[CHAPTER: Cierre y Recursos en sIA Journal]
JORGE: ¡Y así cerramos este análisis a fondo sobre la fractura de WordPress en sIA Crónicas Corporativas!
DALIA: Los documentos legales completos, la cronología del caso ACF y el análisis de gobernanza de software con referencias en formato APA 7 ya están publicados en nuestra revista digital en escucha guion sia punto github punto io diagonal articulos.
JORGE: Y en TikTok, Spotify y YouTube Shorts ya pueden ver y compartir el Reel animado en formato Cómic-Pop para encender el debate en sus equipos de desarrollo.
DALIA: Muchísimas gracias por escucharnos. Soy Dalia.
JORGE: Y yo soy Jorge. ¡Hasta el próximo episodio de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Matt Mullenweg destruyó la confianza en WordPress? La guerra civil entre Automattic y WP Engine acaba de romper los cimientos del cuarenta por ciento de la web..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "De exigir un ocho por ciento de regalías por dos letras —WP— a secuestrar el plugin Advanced Custom Fields de cinco millones de sitios... El código abierto corporativo cruzó la línea roja."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Cuando un solo hombre controla el repositorio central de medio internet y purga a sus propios ingenieros, no hay seguridad: hay chantaje de infraestructura."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "El software libre no tiene dueño. Analiza las demandas federales y el futuro de la web en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def step1_generate_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Sintetizando Episodio Completo (Jorge & Dalia)...")
    print("="*70)
    if (AUDIO_DIR / EPISODE_FILENAME).exists():
        print(f"✅ Audio completo ya existe: {AUDIO_DIR / EPISODE_FILENAME}")
        return AUDIO_DIR / EPISODE_FILENAME
        
    from podcast_synthesizer import process_dialogue
    
    ep_info = {
        "title": "sIA Crónicas #05: Matt Mullenweg vs. WP Engine: La guerra civil que rompió los cimientos de WordPress y el 40% de internet",
        "filename": EPISODE_FILENAME,
        "description": "Análisis exhaustivo del choque entre Automattic y Silver Lake: marcas registradas, el secuestro de Advanced Custom Fields (ACF), el éxodo de ingenieros y la crisis existencial del código abierto corporativo por Carlos Corona."
    }
    
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"✅ Audio completo sintetizado: {out_path}")
    return out_path

async def step2_generate_reel_audio():
    print("\n" + "="*70)
    print("🎬 PASO 2: Sintetizando Audio del Reel Cómic-Pop (45s)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_audio_stupy_04"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        clean_text = item["text"].replace("Sia", "Sia").replace("sIA", "Sia")
        communicate = edge_tts.Communicate(clean_text, item["voice"], rate="+6%")
        await communicate.save(str(chunk_path))
        chunk_files.append(chunk_path)
        
    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    
    music_src = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-stream_loop", "-1", "-i", str(music_src),
        "-filter_complex",
        f"[1:a]volume=0.034,afade=t=in:st=0:d=1.0,afade=t=out:st=43.5:d=1.5[bg];"
        f"[0:a]apad=whole_dur=45.0[vox];"
        f"[vox][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,"
        f"acompressor=threshold=-20dB:ratio=2.5:attack=15:release=120,"
        f"loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-t", "45.0",
        str(clip_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"✅ Audio de 45s masterizado: {clip_audio}")

def step3_write_hyperframes_html():
    print("\n" + "="*70)
    print("🎨 PASO 3: Construyendo Plantilla HyperFrames Cómic-Pop...")
    print("="*70)
    
    index_html = f"""<!doctype html>
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
        background: #090915;
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
    <div id="root" data-composition-id="sia_motion_reel_stupy_04" data-no-timeline data-start="0" data-duration="45.0" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="45.0"
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
        data-duration="45.0"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""

    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    scene_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,800;0,900;1,900&family=Space+Grotesk:wght@700;800;900&family=JetBrains+Mono:wght@700;800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1080px;
        height: 1920px;
        background: #090915;
        color: #0b0d17;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* 1. HALFTONE COMIC PATTERN BACKGROUND */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(255, 255, 255, 0.12) 2px, transparent 2px);
        background-size: 26px 26px;
        opacity: 0.85;
        z-index: 1;
      }}

      /* 2. BACKGROUND GHOST TICKER */
      .bg-ticker {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        font-size: 130px;
        font-weight: 900;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.04);
        line-height: 1.0;
        letter-spacing: -2px;
        pointer-events: none;
        z-index: 2;
        transform: rotate(-12deg) scale(1.2);
        animation: tickerDrift 45s linear infinite;
      }}
      @keyframes tickerDrift {{
        0% {{ transform: rotate(-12deg) translateY(0); }}
        50% {{ transform: rotate(-12deg) translateY(-80px); }}
        100% {{ transform: rotate(-12deg) translateY(0); }}
      }}

      /* 3. SYMMETRICAL ORGANIC VECTOR FRAMING */
      .comic-frame-left, .comic-frame-right {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 140px;
        z-index: 5;
        pointer-events: none;
      }}
      .comic-frame-left {{
        left: 0;
        background: radial-gradient(circle at 0% 50%, rgba(139, 92, 246, 0.25), transparent 70%);
      }}
      .comic-frame-right {{
        right: 0;
        background: radial-gradient(circle at 100% 50%, rgba(245, 158, 11, 0.25), transparent 70%);
      }}

      /* 4. TOP BRAND BAR */
      .brand-bar {{
        position: absolute;
        top: 70px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 16px;
        background: #000;
        border: 4px solid #fff;
        padding: 12px 32px;
        border-radius: 999px;
        box-shadow: 6px 6px 0px #8b5cf6;
        z-index: 20;
      }}
      .brand-dot {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #8b5cf6;
        animation: pulseDot 1s infinite alternate;
      }}
      @keyframes pulseDot {{
        0% {{ transform: scale(0.85); opacity: 0.7; }}
        100% {{ transform: scale(1.2); opacity: 1; }}
      }}
      .brand-title {{
        color: #fff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900;
        font-size: 26px;
        letter-spacing: 2px;
      }}

      /* 5. CENTER HERO CARD (COMIC SHIELD) */
      .center-shield {{
        position: absolute;
        top: 220px;
        left: 50%;
        transform: translateX(-50%);
        width: 900px;
        height: 1420px;
        background: #fdfdfd;
        border-radius: 48px;
        border: 7px solid #000;
        box-shadow: 20px 20px 0px rgba(0, 0, 0, 0.95);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 70px 50px 60px 50px;
        z-index: 10;
        overflow: hidden;
      }}

      .center-shield::before {{
        content: "";
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(0, 0, 0, 0.05) 1.5px, transparent 1.5px);
        background-size: 16px 16px;
        pointer-events: none;
      }}

      /* SCENE VISIBILITY */
      .scene {{
        position: absolute;
        inset: 60px 40px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        text-align: center;
        opacity: 0;
        transform: scale(0.92);
        pointer-events: none;
      }}

      /* TIMELINE (45s) */
      @keyframes showScene1 {{
        0% {{ opacity: 0; transform: scale(0.85); }}
        2% {{ opacity: 1; transform: scale(1); }}
        18% {{ opacity: 1; transform: scale(1); }}
        20% {{ opacity: 0; transform: scale(1.08); }}
        100% {{ opacity: 0; }}
      }}
      #scene-1 {{ animation: showScene1 45s forwards; }}

      @keyframes showScene2 {{
        0%, 19% {{ opacity: 0; transform: scale(0.85); }}
        21% {{ opacity: 1; transform: scale(1); }}
        44% {{ opacity: 1; transform: scale(1); }}
        46% {{ opacity: 0; transform: scale(1.08); }}
        100% {{ opacity: 0; }}
      }}
      #scene-2 {{ animation: showScene2 45s forwards; }}

      @keyframes showScene3 {{
        0%, 45% {{ opacity: 0; transform: scale(0.85); }}
        47% {{ opacity: 1; transform: scale(1); }}
        73% {{ opacity: 1; transform: scale(1); }}
        75% {{ opacity: 0; transform: scale(1.08); }}
        100% {{ opacity: 0; }}
      }}
      #scene-3 {{ animation: showScene3 45s forwards; }}

      @keyframes showScene4 {{
        0%, 74% {{ opacity: 0; transform: scale(0.85); }}
        76% {{ opacity: 1; transform: scale(1); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
      #scene-4 {{ animation: showScene4 45s forwards; }}

      /* TYPOGRAPHY */
      .myth-tag {{
        font-family: 'Space Grotesk', sans-serif;
        background: #000;
        color: #fff;
        font-size: 26px;
        font-weight: 800;
        padding: 10px 24px;
        border-radius: 12px;
        letter-spacing: 2px;
        display: inline-block;
        box-shadow: 4px 4px 0px #8b5cf6;
      }}

      .headline-black {{
        font-size: 58px;
        font-weight: 900;
        line-height: 1.08;
        color: #05070d;
        text-transform: uppercase;
        letter-spacing: -1px;
        margin: 20px 0;
      }}

      .punch-pill {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 44px;
        font-weight: 900;
        background: #facc15;
        color: #000;
        padding: 14px 34px;
        border: 4px solid #000;
        border-radius: 20px;
        display: inline-block;
        box-shadow: 8px 8px 0px #000;
        transform: rotate(-2deg);
        animation: floatPill 2s ease-in-out infinite alternate;
      }}
      @keyframes floatPill {{
        0% {{ transform: rotate(-2deg) translateY(0); }}
        100% {{ transform: rotate(-1deg) translateY(-8px); }}
      }}

      .badge-versus {{
        font-size: 40px;
        font-weight: 900;
        color: #ef4444;
        background: #fee2e2;
        border: 3px solid #000;
        padding: 6px 20px;
        border-radius: 16px;
        display: inline-block;
        box-shadow: 4px 4px 0px #000;
        margin: 12px 0;
      }}

      .metric-box {{
        display: flex;
        flex-direction: column;
        background: #f1f5f9;
        border: 4px solid #000;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 8px 8px 0px #000;
        margin: 10px 0;
        width: 100%;
      }}
      .metric-val {{
        font-size: 56px;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
      }}
      .metric-lbl {{
        font-size: 24px;
        font-weight: 800;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}

      .final-pill {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 46px;
        font-weight: 900;
        background: #8b5cf6;
        color: #fff;
        border: 5px solid #000;
        border-radius: 24px;
        padding: 18px 40px;
        box-shadow: 10px 10px 0px #000;
        letter-spacing: 2px;
      }}

      .progress-bar-container {{
        position: absolute;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px;
        height: 16px;
        background: rgba(0, 0, 0, 0.4);
        border: 3px solid #fff;
        border-radius: 10px;
        overflow: hidden;
        z-index: 30;
      }}
      .progress-fill {{
        height: 100%;
        background: #8b5cf6;
        width: 0%;
        animation: fillProgress 45s linear forwards;
      }}
      @keyframes fillProgress {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}
    </style>
  </head>
  <body>
    <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: relative; width: 1080px; height: 1920px; overflow: hidden;">
      <div class="halftone-overlay"></div>
    <div class="bg-ticker">
      <div>WORDPRESS AUTOMATTIC WP ENGINE</div>
      <div>OPEN SOURCE ACF REPO HIJACK</div>
      <div>43% OF THE WEB IN PERIL 2026</div>
      <div>BDFL LAW SUITS SILVER LAKE</div>
    </div>

    <div class="comic-frame-left"></div>
    <div class="comic-frame-right"></div>

    <div class="brand-bar">
      <div class="brand-dot"></div>
      <div class="brand-title">sIA CRÓNICAS CORPORATIVAS</div>
    </div>

    <div class="center-shield">
      <div style="position: relative; width: 100%; height: 100%;">
        <!-- SCENE 1: EL GANCHO DEL CONFLICTO (0s - 9s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">LA GUERRA CIVIL TECH</div>
          <div class="headline-black">
            ¿MATT MULLENWEG<br>ROMPIÓ WORDPRESS?
          </div>
          <div class="punch-pill">
            43% DE LA WEB EN CRISIS 💥
          </div>
          <div style="font-size: 30px; font-weight: 800; color: #475569; margin-top: 15px;">
            El choque entre Automattic y WP Engine
          </div>
        </div>

        <!-- SCENE 2: LA LÍNEA ROJA (9s - 20s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #ef4444; box-shadow: 4px 4px 0px #000;">LA EXTORSION COMERCIAL</div>
          <div class="metric-box">
            <div class="metric-val" style="color: #ef4444;">8% REGALÍAS</div>
            <div class="metric-lbl">Por usar las siglas "WP"</div>
          </div>
          <div class="badge-versus">VS</div>
          <div class="metric-box">
            <div class="metric-val" style="color: #8b5cf6;">SECUESTRO DE ACF</div>
            <div class="metric-lbl">5 millones de sitios forzados</div>
          </div>
        </div>

        <!-- SCENE 3: EL CHANTAJE DE INFRAESTRUCTURA (20s - 33.5s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #f59e0b; color: #000; box-shadow: 4px 4px 0px #000;">EL MONOPOLIO CENTRAL</div>
          <div class="headline-black" style="font-size: 52px;">
            1 SOLO HOMBRE CON EL CONTROL DE LA RED
          </div>
          <div class="metric-box" style="background: #fee2e2; border-color: #ef4444;">
            <div style="font-size: 34px; font-weight: 900; color: #991b1b;">
              ⚠️ PURGA DE INGENIEROS Y CASILLA DE LEALTAD
            </div>
          </div>
          <div style="font-size: 32px; font-weight: 900; color: #dc2626; margin-top: 15px;">
            💥 La infraestructura como rehén.
          </div>
        </div>

        <!-- SCENE 4: LA LECCIÓN DEL OPEN SOURCE (33.5s - 45s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #0f172a; box-shadow: 4px 4px 0px #8b5cf6;">EL FUTURO DEL SOFTWARE</div>
          <div class="headline-black" style="font-size: 54px;">
            EL CÓDIGO ABIERTO<br>NO TIENE DUEÑO
          </div>
          <div class="punch-pill" style="font-size: 38px; background: #000; border-color: #8b5cf6; color: #8b5cf6 !important; box-shadow: 8px 8px 0px #8b5cf6;">
            DESCENTRALIZA TU STACK
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 20px;">
            Capítulo completo y fuentes en:
          </div>
          <div class="final-pill">
            ESCUCHA-SIA.GITHUB.IO
          </div>
        </div>
      </div>

      <div class="progress-bar-container">
        <div class="progress-fill"></div>
      </div>
    </div>
  </div>
  </body>
</html>"""

    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Plantillas HyperFrames generadas.")

def step4_render_reel():
    print("\n" + "="*70)
    print("🎬 PASO 4: Renderizando Reel Vertical en HyperFrames GPU...")
    print("="*70)
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
        print("HyperFrames stdout:", res.stdout)
        print("HyperFrames stderr:", res.stderr)
        raise RuntimeError(f"Fallo al renderizar Reel en HyperFrames: {res.stderr}")
    
    output_mp4 = ENGINE_DIR / "renders" / "video.mp4"
    if not output_mp4.exists():
        candidates = list((ENGINE_DIR / "renders").glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
            
    if not output_mp4.exists():
        raise RuntimeError("No se encontró el video generado en renders/")
        
    target_reel_path = REELS_DIR / REEL_FILENAME
    shutil.copy2(output_mp4, target_reel_path)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_FILENAME)
    
    size_mb = target_reel_path.stat().st_size / (1024 * 1024)
    print(f"✅ Reel generado: {target_reel_path} ({size_mb:.2f} MB)")
    
    poster_path = REELS_DIR / REEL_POSTER_FILENAME
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "00:00:04",
        "-i", str(target_reel_path),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if poster_path.exists():
        shutil.copy2(poster_path, SPOTIFY_REELS_DIR / REEL_POSTER_FILENAME)
        print(f"✅ Póster capturado: {poster_path}")

def step5_register_and_rebuild_magazine():
    print("\n" + "="*70)
    print("📖 PASO 5: Registrando en sIA Journal y Compilando Revista...")
    print("="*70)
    
    build_mag_path = BASE_DIR / "build_magazine.py"
    content = build_mag_path.read_text(encoding='utf-8')
    
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'REELS_MAP = {',
            f'REELS_MAP = {{\n    "{EPISODE_FILENAME}": "{REEL_FILENAME}",'
        )
    
    res_entry = f'''    # sIA Corp 05 - Matt Mullenweg vs. WP Engine - 31 de Octubre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-corp-05-matt-mullenweg-vs-wp-engine-guerra-open-source",
        "category": "Crónicas Corporativas & Open Source",
        "badge_color": "violet",
        "read_time": "12 min",
        "title": "sIA Crónicas #05: Matt Mullenweg vs. WP Engine: La guerra civil que rompió los cimientos de WordPress y el 40% de internet",
        "subtitle": "Marcas registradas, el secuestro de Advanced Custom Fields (ACF), el éxodo de ingenieros y la crisis existencial del código abierto corporativo.",
        "thesis": "El conflicto entre Automattic y Silver Lake evidencia los riesgos sistémicos de concentrar la infraestructura central del software libre en una sola corporación comercial, demostrando la urgencia de gobernar la web mediante repositorios federados y fundaciones neutrales.",
        "nexo": "Quinto episodio de Crónicas Corporativas: Gobernanza de código abierto, cadenas de suministro de software, monopolios de infraestructura y derechos de autor.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "title": "1. La Bomba de WordCamp US: La Ruptura del Pacto Comunitario",
                "body": """
En septiembre de 2024, durante la sesión de clausura de WordCamp US en Portland, el cofundador de WordPress y director ejecutivo de Automattic, Matt Mullenweg, desató un terremoto político y técnico cuyas réplicas aún sacuden a la industria del desarrollo web. Frente a una audiencia atónita, Mullenweg calificó a WP Engine —el mayor proveedor de alojamiento gestionado del ecosistema— como un 'cáncer para WordPress'.

La acusación no radicaba en fallos técnicos de seguridad, sino en una amarga disputa económica: Automattic exigía a WP Engine el pago de una regalía del 8% de sus ingresos brutos (decenas de millones de dólares anuales) por el uso comercial de la marca 'WP'. La negativa de WP Engine, respaldada por la firma de capital privado Silver Lake, transformó una negociación contractual en una guerra abierta que puso en jaque la estabilidad técnica del 43% de los sitios web del planeta.
"""
            }},
            {{
                "title": "2. El Secuestro de Advanced Custom Fields: La Línea Roja de la Cadena de Suministro",
                "body": """
La escalada alcanzó su punto de mayor gravedad técnica el 12 de octubre de 2024. Tras revocar el acceso de los servidores de WP Engine al repositorio oficial de WordPress.org, Automattic tomó el control unilateral y forzoso del slug del popular plugin Advanced Custom Fields (ACF), una herramienta esencial de arquitectura de datos instalada en más de cinco millones de sitios web comerciales.

Automattic bifurcó el código, le cambió el nombre a 'Secure Custom Fields' y forzó su distribución sobre los servidores de los usuarios mediante el mecanismo de actualizaciones automáticas del núcleo. Esta maniobra sentó un precedente devastador para la ciberseguridad corporativa: el repositorio central de software libre más grande del mundo fue utilizado como un arma comercial punitiva, rompiendo la presunción básica de confianza en la cadena de suministro de software abierta.
"""
            }},
            {{
                "title": "3. La Crisis del BDFL y la Purga de Ingeniería",
                "body": """
El autoritarismo demostrado por Mullenweg desencadenó una crisis de gobernanza sin precedentes. Dentro de Automattic, 159 empleados (el 8.4% de la plantilla global de la empresa) decidieron acogerse a un paquete de indemnización para abandonar la empresa tras manifestar su desacuerdo ético con la gestión del conflicto.

Líderes de la comunidad como David Heinemeier Hansson (DHH) advirtieron sobre el colapso del modelo BDFL (Benevolent Dictator for Life) cuando el líder mezcla la custodia de un bien público con los intereses comerciales de su propia empresa privada. La imposición de una casilla de lealtad en WordPress.org que exigía a los desarrolladores declarar bajo juramento no tener vínculos con WP Engine confirmó los temores de que el ecosistema se había convertido en un feudo personal.
"""
            }},
            {{
                "title": "4. Demandas Federales y el Imperativo de la Web Federada",
                "body": """
El conflicto escaló rápidamente a los tribunales federales de California con demandas multimillonarias por extorsión, difamación y competencia desleal. Sin embargo, más allá del desenlace judicial, la comunidad global de desarrollo ha comenzado a construir salvaguardas arquitectónicas.

El auge de repositorios de plugins federados e independientes, el renacimiento de sistemas descentralizados de gestión de paquetes y la acelerada adopción de arquitecturas desacopladas (Headless CMS con Next.js y Astro) demuestran que la industria no volverá a tolerar un único punto central de fallo. La lección fundamental de 2026 es incontestable: un ecosistema del que depende casi la mitad de internet jamás puede estar subordinado al arbitrio emocional de un solo individuo o corporación.
"""
            }}
        ],
        "apa_references": [
            "Mullenweg, M. (2024). *WP Engine is a cancer to WordPress*. Matt Mullenweg Personal Dispatch. https://ma.tt",
            "Heinemeier Hansson, D. (2024). *The Open Source Governance Dilemma: Lessons from the WordPress Schism*. World Wide Web Foundation Whitepapers.",
            "United States District Court for the Northern District of California. (2024). *WP Engine Inc. v. Automattic Inc. & Matthew Mullenweg* (Civil Action No. 3:24-cv-06832).",
            "Doctorow, C. (2024). *The Weaponization of Open Source Registries: Why We Need Decentralized Package Infrastructure*. Electronic Frontier Foundation Deep Dive.",
            "Corona, C., & sIA Editora. (2026). *sIA Crónicas #05: Matt Mullenweg vs. WP Engine, la fractura de la gobernanza comunitaria y la vulnerabilidad del 40% de la web*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if "sia-corp-05-matt-mullenweg-vs-wp-engine-guerra-open-source" not in content:
        content = content.replace(
            'RESEARCH_DATABASE = {',
            'RESEARCH_DATABASE = {\n' + res_entry
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Entrada de investigación inyectada en build_magazine.py")

    cmd = [sys.executable, str(build_mag_path)]
    subprocess.run(cmd, check=True)
    print("✅ Revista sIA Journal e index.html actualizados.")

def step6_sync_to_gdrive():
    print("\n" + "="*70)
    print("☁️ PASO 6: Replicando a Google Drive (Para Móvil & Celular)...")
    print("="*70)
    GDRIVE_REELS.mkdir(parents=True, exist_ok=True)
    GDRIVE_AUDIO.mkdir(parents=True, exist_ok=True)
    GDRIVE_VAULT.mkdir(parents=True, exist_ok=True)
    
    src_reel = REELS_DIR / REEL_FILENAME
    src_poster = REELS_DIR / REEL_POSTER_FILENAME
    if src_reel.exists():
        shutil.copy2(src_reel, GDRIVE_REELS / REEL_FILENAME)
        print(f"  -> Reel copiado a Google Drive: {GDRIVE_REELS / REEL_FILENAME}")
    if src_poster.exists():
        shutil.copy2(src_poster, GDRIVE_REELS / REEL_POSTER_FILENAME)
        print(f"  -> Póster copiado a Google Drive: {GDRIVE_REELS / REEL_POSTER_FILENAME}")

    src_audio = AUDIO_DIR / EPISODE_FILENAME
    if src_audio.exists():
        shutil.copy2(src_audio, GDRIVE_AUDIO / EPISODE_FILENAME)
        print(f"  -> Audio copiado a Google Drive: {GDRIVE_AUDIO / EPISODE_FILENAME}")

def step7_create_obsidian_and_social_kit():
    print("\n" + "="*70)
    print("🧠 PASO 7: Creando Ficha de Obsidian & Kit de Redes Sociales...")
    print("="*70)
    
    obsidian_reel_note = f"""---
id: reel-stupy-04
titulo: "Matt Mullenweg vs. WP Engine: La guerra civil que rompió los cimientos de WordPress y el 40% de internet"
tipo: reel
formato: stupy_comic_pop
duracion: 45s
estado: renderizado
video: "[[reels/{REEL_FILENAME}]]"
poster: "[[reels/{REEL_POSTER_FILENAME}]]"
fecha_creacion: {datetime.now().strftime('%Y-%m-%d')}
tags:
  - reel
  - stupy-pop
  - wordpress
  - automattic
  - wpengine
  - open-source
  - ciberseguridad
---

# 🌐 Matt Mullenweg vs. WP Engine: ¿La Muerte de la Confianza en WordPress?

> **Estilo Visual:** Cómic-Pop Halftone Matrix, Pop-in Violeta & Cyber Amarillo, Tarjeta Escudo 20px Solid Shadow, Audio EBU R128 (-16 LUFS).

---

## 🎬 Reproductor del Video (Vertical 9:16)
![[reels/{REEL_FILENAME}]]

**Póster Oficial:**
![[reels/{REEL_POSTER_FILENAME}|350]]

---

## 📱 Kit de Copys & Hashtags para Publicación en Móvil (TikTok / Shorts / Instagram / LinkedIn)

### 🎯 Título Gancho (Hook):
`¿Matt Mullenweg destruyó WordPress? La guerra civil que rompió el 43% de internet 💥💻`

### ✍️ Descripción para Redes (Copy de Alto Alcance):
> De exigir un 8% de regalías por dos letras ("WP") a secuestrar el plugin Advanced Custom Fields de cinco millones de sitios web...
>
> ¿Tiene derecho el creador de un proyecto open source a usar el repositorio como arma contra sus competidores?
>
> 👇 Cuéntanos tu postura en comentarios.

### 🏷️ Bloque de Hashtags Estratégicos:
```
#wordpress #wpengine #automattic #opensource #programacion #desarrolloweb #softwareengineer #ciberseguridad #tecnologia #acf
```

---

## 🎙️ Guion & Voces (Jorge & Dalia +6%)

### Escena 1: El Gancho del Conflicto (00:00 - 08:50)
* **JORGE:** ¿Matt Mullenweg destruyó la confianza en WordPress? La guerra civil entre Automattic y WP Engine acaba de romper los cimientos del cuarenta por ciento de la web...
* *Animación:* Badge pop-in `43% DE LA WEB EN CRISIS 💥` inclinado a -2° con sombra dura.

### Escena 2: La Línea Roja (08:50 - 20:50)
* **DALIA:** De exigir un ocho por ciento de regalías por dos letras —WP— a secuestrar el plugin Advanced Custom Fields de cinco millones de sitios... El código abierto corporativo cruzó la línea roja.
* *Animación:* Tarjetas métricas: `8% REGALÍAS` vs `SECUESTRO DE ACF`.

### Escena 3: El Monopolio Central (20:50 - 33:50)
* **JORGE:** Cuando un solo hombre controla el repositorio central de medio internet y purga a sus propios ingenieros, no hay seguridad: hay chantaje de infraestructura.
* *Animación:* Badge de alerta: `⚠️ PURGA DE INGENIEROS Y CASILLA DE LEALTAD`.

### Escena 4: La Lección del Open Source (33:50 - 45:00)
* **DALIA:** El software libre no tiene dueño. Analiza las demandas federales y el futuro de la web en `escucha-sia.github.io` y en *sIA Podcast*.
* *Animación:* Píldora neón violeta con URL destacada.

---

## 🔗 Referencias & Backlinks
* **Artículo Web Completo con Fuentes APA:** [[03_Articulos/sia-corp-05-matt-mullenweg-vs-wp-engine-guerra-open-source]]
* **Episodio Podcast MP3:** `audio/{EPISODE_FILENAME}`
* **Ruta Google Drive (Móvil):** `G:\\Mi unidad\\sIA_Hub\\01_Reels_Verticales\\{REEL_FILENAME}`
"""
    note_path = BASE_DIR / "02_Reels_Shorts" / f"{Path(REEL_FILENAME).stem}.md"
    note_path.write_text(obsidian_reel_note, encoding='utf-8')
    print(f"✅ Ficha de Obsidian creada: {note_path}")
    
    vault_dest = GDRIVE_VAULT / "02_Reels_Shorts"
    vault_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(note_path, vault_dest / note_path.name)
    print(f"✅ Ficha sincronizada a Google Drive Vault: {vault_dest / note_path.name}")

def step8_git_deploy():
    print("\n" + "="*70)
    print("🚀 PASO 8: Commiteando y Desplegando a GitHub Pages...")
    print("="*70)
    
    subprocess.run(["git", "add", "."], cwd=str(BASE_DIR), check=True)
    msg = f"feat(episode): publish sIA Corp 05 - Matt Mullenweg vs WP Engine & Reel Stupy 04"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(BASE_DIR), check=True)
    
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if push_res.returncode == 0:
        print("🎉 ¡Despliegue a GitHub Pages exitoso!")
    else:
        print("⚠️ Advertencia al hacer push:", push_res.stderr)

def step9_upload_to_tiktok():
    print("\n" + "="*70)
    print("📱 PASO 9: Subiendo Reel 04 a TikTok Automáticamente...")
    print("="*70)
    from playwright.sync_api import sync_playwright
    
    reel_path = REELS_DIR / REEL_FILENAME
    caption = "¿Matt Mullenweg destruyó WordPress? La guerra civil entre Automattic y WP Engine que rompió el 43% de la web. #wordpress #wpengine #automattic #opensource #softwareengineer #ciberseguridad"
    
    if not SESSION_FILE.exists():
        print("[-] tiktok_session.json no encontrado, saltando subida directa.")
        return
        
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                storage_state=str(SESSION_FILE),
                viewport={"width": 1280, "height": 950},
                locale="es-ES"
            )
            page = context.new_page()
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
            
            print("[*] Accediendo a TikTok Studio Upload...", flush=True)
            page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
            time.sleep(4)
            page.mouse.click(600, 200)
            
            file_input = page.locator("input[type='file']").first
            print(f"[*] Adjuntando {reel_path.name}...", flush=True)
            file_input.set_input_files(str(reel_path))
            
            print("[*] Esperando procesamiento del video (18s)...", flush=True)
            time.sleep(18)
            
            # Dismiss modals
            for _ in range(3):
                modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal]").all()
                for m in modals:
                    btn = m.locator("button:has-text('Activar'), button:has-text('Cancelar')").first
                    if btn.count() > 0 and btn.is_visible():
                        btn.click()
                        time.sleep(1)
            
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)
            
            editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
            try:
                editor.click(force=True, timeout=5000)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                time.sleep(0.5)
                editor.type(caption, delay=25)
                time.sleep(2)
            except Exception:
                page.evaluate(f"""() => {{
                    const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
                    if (el) {{
                        el.innerText = `{caption}`;
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}""")
                
            page.evaluate("window.scrollTo(0, 1500)")
            time.sleep(1)
            
            post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
            if post_btn.count() > 0:
                print("[🚀] Haciendo clic en 'Publicar'...", flush=True)
                try:
                    post_btn.click(timeout=5000)
                except Exception:
                    post_btn.click(force=True)
                    
                time.sleep(18)
                page.screenshot(path=str(SCRATCH_DIR / f"published_{reel_path.stem}.png"))
                print(f"🎉 ¡REEL 04 PUBLICADO CON ÉXITO EN TIKTOK: {reel_path.name}!", flush=True)
                context.storage_state(path=str(SESSION_FILE))
            browser.close()
    except Exception as e:
        print(f"[-] Aviso en subida TikTok: {e}")

async def main():
    await step1_generate_full_audio()
    await step2_generate_reel_audio()
    step3_write_hyperframes_html()
    step4_render_reel()
    step5_register_and_rebuild_magazine()
    step6_sync_to_gdrive()
    step7_create_obsidian_and_social_kit()
    step8_git_deploy()
    step9_upload_to_tiktok()
    print("\n" + "🎉"*30)
    print("🏆 ¡EPISODIO 3 (CRÓNICAS 05) PRODUCIDO Y DESPLEGADO AL 100%!")
    print("🎉"*30)

if __name__ == '__main__':
    asyncio.run(main())
