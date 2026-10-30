"""
sIA Master Episode & Reel Producer:
Tema: El Síndrome de la Niñera de Prompts (AI Burnout & Code Review Crisis)
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop (HyperFrames GPU, 45s, Halftone, Kinetic Pop)
3. Póster oficial del Reel
4. Registro de investigación en build_magazine.py con referencias APA 7
5. Recompilación de sIA Journal (index.html + artículo web responsive)
6. Sincronización automática a Google Drive (G:\Mi unidad\sIA_Hub)
7. Nota de Obsidian Vault con Embed de video + Kit de Copys para Redes
8. Despliegue Git a GitHub Pages
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

EPISODE_FILENAME = "sIA_Dev_01_Ninera_de_Prompts_AI_Burnout_2026-10-30.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_02_Ninera_Prompts.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_02_Ninera_Prompts_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: El Confesionario de Reddit y la Fatiga de los Desarrolladores]
JORGE: ¡Muy buenos días a toda nuestra comunidad de ingenieros, arquitectos de software y mentes curiosas en México y toda Latinoamérica! Bienvenidos a una entrega especial de sIA. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es viernes treinta de octubre de dos mil veintiséis. Y hoy tenemos que hablar de una conversación que está ardiendo con miles de comentarios en Reddit, en r diagonal programming y en los canales más respetados de ingeniería de software en YouTube.
JORGE: Así es, Dalia. Durante los últimos dos años nos vendieron la promesa dorada de que la Inteligencia Artificial eliminaría las tareas aburridas y el código repetitivo, liberándonos para dedicarnos a la pura creatividad arquitectónica. Pero la realidad en las trincheras de producción en este dos mil veintiséis es completamente opuesta.
DALIA: Cientos de desarrolladores senior con diez y quince años de experiencia están confesando un agotamiento existencial brutal: lo que la comunidad ha bautizado como el síndrome de la niñera de prompts. Ingenieros que antes diseñaban sistemas elegantes y hoy pasan doce horas al día sentados frente a la terminal solo presionando la tecla Enter para aprobar sugerencias automatizadas que apenas comprenden.
JORGE: Es la transformación del artesano del software en un burócrata de validación. Y lo peor de todo es que este fenómeno ha desatado una crisis estructural sin precedentes en la revisión de código y en la cultura de los equipos de desarrollo.
DALIA: En este episodio vamos a desarmar la anatomía de este burnout, los datos duros de la caída de confianza en la IA y la regla arquitectónica para recuperar el control técnico de nuestros sistemas. ¡Arrancamos!

[CHAPTER: La Crisis del Code Review y el Colapso del 'LGTM']
JORGE: Entremos de lleno al núcleo del problema: el colapso del proceso de revisión de código. Tradicionalmente, un Pull Request bien diseñado contenía entre cincuenta y doscientas líneas de código cuidadosamente pensadas, con pruebas unitarias y una descripción clara de la intención del desarrollador.
DALIA: Hoy en día, con agentes de codificación autónomos capaces de modificar quince archivos en tres segundos, los repositorios se están inundando de Pull Requests gigantescos de mil quinientas o dos mil líneas generadas casi instantáneamente.
JORGE: ¿Y cuál ha sido la respuesta humana ante semejante avalancha de texto sintético? La indiferencia y la pereza institucional. Ningún ingeniero de un equipo tiene el tiempo ni el ancho de banda cognitivo para auditar línea por línea dos mil renglones de lógica generada por una máquina.
DALIA: Exactamente, Jorge. Y lo más irónico y peligroso es lo que documentan en los foros: los revisores le piden a otra Inteligencia Artificial que resuma el Pull Request y terminan estampando un sello superficial de 'LGTM' —Looks Good To Me— sin haber leído ni un solo caso de borde. Se ha creado una cámara de eco donde una IA escribe el código, otra IA escribe la justificación del cambio, un humano aprieta un botón sin entenderlo, y el código se despliega directamente a los servidores de producción.
JORGE: Es la receta perfecta para la catástrofe silenciosa: vulnerabilidades de seguridad sutiles, inyecciones de dependencias innecesarias, fugas de memoria y una deuda técnica invisible que nadie sabe cómo depurar cuando los sistemas colapsan a las tres de la mañana.

[CHAPTER: La Paradoja de la Confianza: 80% de Adopción, 0% de Fe]
DALIA: Y esto nos lleva a una paradoja estadística fascinante que revelan las encuestas más recientes de la industria tecnológica: mientras la tasa de adopción de herramientas de IA entre programadores supera el ochenta y cinco por ciento, el índice de confianza real en la exactitud del código generado ha caído a su punto más bajo en cuatro años.
JORGE: ¡Es el fenómeno del código 'casi correcto', Dalia! Una alucinación burda es fácil de detectar porque el compilador o el intérprete arrojan un error en rojo de inmediato. Pero los agentes modernos son extremadamente elocuentes: generan código que luce impecable a simple vista, con nombres de variables elegantes y comentarios estructurados, pero que oculta una falla de concurrencia o una suposición errónea sobre el estado de la base de datos.
DALIA: Y aquí es donde radica el origen del agotamiento mental: depurar un error sutil en quinientas líneas de código que tú no escribiste ni razonaste mentalmente requiere hasta cuatro veces más esfuerzo cognitivo que escribir la solución desde cero. El desarrollador pasa de un estado de flujo creativo a un estado permanente de sospecha y paranoia técnica.
JORGE: Por eso los bootcamps que prometían crear 'orquestadores de IA en tres meses' están sufriendo una crisis terminal. En la era de la inteligencia artificial, lo que las organizaciones maduras buscan desesperadamente no son personas que sepan redactar prompts bonitos, sino veteranos de arquitectura con el criterio técnico suficiente para detectar cuándo una máquina está mintiendo con elegancia.

[CHAPTER: La Regla de Verificación: De Niñera de Prompts a Ingeniero de Sistemas]
DALIA: Entonces, Jorge, ¿cómo rompemos esta trampa? ¿Cómo evitamos convertirnos en meros cuidadores de modelos probabilísticos?
JORGE: La respuesta no es renunciar a la tecnología, sino invertir la jerarquía de control. El principio fundamental de la ingeniería de software moderna debe ser: nunca permitas que un modelo de lenguaje escriba código antes de que tú hayas definido formalmente el contrato determinista del sistema.
DALIA: Esto significa que el ingeniero diseña primero las interfaces estrictas, los esquemas de validación con TypeSafe o Pydantic, y las pruebas de integración que definen exactamente lo que es aceptable y lo que no. El agente de IA puede generar la implementación interna, pero está estrictamente confinado dentro de una caja de arena donde el código no se acepta si no pasa una suite de pruebas automatizadas locales.
JORGE: Y la segunda regla de oro para la salud mental de los equipos es el límite estricto de contexto: jamás permitas que un asistente modifique más de dos o tres archivos en un solo ciclo sin una revisión humana reflexiva. La velocidad bruta de generación no es productividad si destruye la soberanía técnica del programador sobre su propio producto.
DALIA: La verdadera maestría tecnológica en dos mil veintiséis no se mide por la cantidad de líneas que un modelo escribe por ti, sino por tu capacidad de entender cada engranaje del sistema cuando todo lo demás falla.

[CHAPTER: Cierre y Recursos en sIA Journal]
JORGE: Y con esta reflexión cerramos este análisis urgente sobre la psicología y el futuro del desarrollo de software.
DALIA: Recuerden que el artículo completo con diagramas de arquitectura de verificación, análisis sociotécnico y todas las fuentes bibliográficas en formato APA ya está publicado en nuestra revista digital en escucha guion sia punto github punto io diagonal articulos.
JORGE: Y en nuestras redes sociales y en su canal de Spotify ya pueden disfrutar del Reel vertical en formato Cómic-Pop con la síntesis animada de cuarenta y cinco segundos para compartir con sus colegas de equipo.
DALIA: Muchísimas gracias por escucharnos. Soy Dalia.
JORGE: Y yo soy Jorge. ¡Nos escuchamos en el próximo episodio de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Creías que usar agentes de Inteligencia Artificial te haría un programador diez veces más rápido? En Reddit y Silicon Valley los desarrolladores senior están confesando la verdad..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Bienvenido al síndrome de la niñera de prompts: pasas doce horas al día solo apretando la tecla Enter para validar código que tú no escribiste... ¡y que tu equipo aprueba con un 'LGTM' sin leerlo!"
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Generar mil líneas toma treinta segundos. Pero encontrar la alucinación silenciosa que tumba la base de datos te cuesta tu salud mental, tu fin de semana y la caída de producción."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Si no entiendes la arquitectura, no eres un ingeniero: eres un capturista de prompts. Recupera tu criterio técnico en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def step1_generate_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Sintetizando Episodio Completo (Jorge & Dalia)...")
    print("="*70)
    from podcast_synthesizer import process_dialogue
    
    ep_info = {
        "title": "sIA Dev #01: El Síndrome de la Niñera de Prompts: AI Burnout y la Crisis del Code Review",
        "filename": EPISODE_FILENAME,
        "description": "Análisis sobre la fatiga del desarrollador moderno, el colapso del 'LGTM' en Pull Requests masivos generados por IA, la pérdida de soberanía técnica y el nuevo paradigma de verificación arquitectónica por Carlos Corona."
    }
    
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"✅ Audio completo sintetizado: {out_path}")
    return out_path

async def step2_generate_reel_audio():
    print("\n" + "="*70)
    print("🎬 PASO 2: Sintetizando Audio del Reel Cómic-Pop (45s)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_audio_stupy_02"
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
        background: #080a12;
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
    <div id="root" data-composition-id="sia_motion_reel_stupy_02" data-no-timeline data-start="0" data-duration="45.0" data-width="1080" data-height="1920">
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
        background: #090b14;
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

      /* 2. GIANT BACKGROUND GHOST WATERMARK TICKER */
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
        background: radial-gradient(circle at 0% 50%, rgba(255, 69, 0, 0.15), transparent 70%);
      }}
      .comic-frame-right {{
        right: 0;
        background: radial-gradient(circle at 100% 50%, rgba(255, 69, 0, 0.15), transparent 70%);
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
        box-shadow: 6px 6px 0px #ff4500;
        z-index: 20;
      }}
      .brand-dot {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #ff4500;
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
        background: #f8fafc;
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
        box-shadow: 4px 4px 0px #ff4500;
      }}

      .headline-black {{
        font-size: 60px;
        font-weight: 900;
        line-height: 1.08;
        color: #05070d;
        text-transform: uppercase;
        letter-spacing: -1px;
        margin: 20px 0;
      }}

      .punch-pill {{
        background: #ff4500;
        color: #fff !important;
        font-size: 72px;
        font-weight: 900;
        padding: 16px 40px;
        border-radius: 16px;
        display: inline-block;
        border: 5px solid #000;
        box-shadow: 8px 8px 0px #000;
        transform: rotate(-3deg);
        animation: popPunch 0.8s infinite alternate ease-in-out;
      }}
      @keyframes popPunch {{
        0% {{ transform: rotate(-3deg) scale(0.98); }}
        100% {{ transform: rotate(-3deg) scale(1.04); }}
      }}

      .metric-grid {{
        display: flex;
        flex-direction: column;
        gap: 20px;
        width: 100%;
        margin-top: 10px;
      }}
      .metric-card {{
        background: #fff;
        border: 5px solid #000;
        border-radius: 24px;
        padding: 20px 26px;
        box-shadow: 8px 8px 0px #000;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }}
      .metric-card.danger {{
        border-color: #dc2626;
        box-shadow: 8px 8px 0px #dc2626;
      }}
      .metric-val {{
        font-size: 64px;
        font-weight: 900;
      }}
      .metric-val.red {{ color: #dc2626; }}
      .metric-desc {{
        font-size: 30px;
        font-weight: 800;
        text-align: right;
        color: #000;
        line-height: 1.15;
      }}

      .compare-box {{
        background: #000;
        color: #fff;
        border-radius: 24px;
        padding: 30px 36px;
        width: 100%;
        text-align: left;
        box-shadow: 10px 10px 0px #ff4500;
        border: 4px solid #fff;
        font-family: 'JetBrains Mono', monospace;
      }}
      .code-line {{
        font-size: 26px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 16px;
      }}
      .tag-fast {{
        background: #10b981;
        color: #000;
        padding: 4px 14px;
        border-radius: 6px;
        font-weight: 900;
        font-size: 22px;
      }}
      .tag-slow {{
        background: #ef4444;
        color: #fff;
        padding: 4px 14px;
        border-radius: 6px;
        font-weight: 900;
        font-size: 22px;
      }}

      .final-pill {{
        background: #000;
        color: #00f0ff;
        border: 5px solid #00f0ff;
        padding: 20px 40px;
        border-radius: 20px;
        font-size: 34px;
        font-weight: 900;
        box-shadow: 8px 8px 0px #00f0ff;
        margin-top: 20px;
        letter-spacing: 1px;
      }}

      .progress-bar-container {{
        position: absolute;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 860px;
        height: 14px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 999px;
        overflow: hidden;
        z-index: 20;
      }}
      .progress-fill {{
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #ff4500, #00f0ff);
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
        <div>BURNOUT DEL PROGRAMADOR</div>
        <div>BOTÓN ENTER 500 VECES</div>
        <div>EL COLAPSO DEL LGTM</div>
        <div>NIÑERA DE PROMPTS</div>
        <div>SIA TECH MEDIA</div>
      </div>

      <div class="comic-frame-left"></div>
      <div class="comic-frame-right"></div>

      <div class="brand-bar">
        <div class="brand-dot"></div>
        <div class="brand-title">SIA • REALIDAD DE SOFTWARE</div>
      </div>

      <div class="center-shield">
        <!-- SCENE 1: EL GANCHO (0s - 8.5s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">EL CONFESIONARIO DE REDDIT</div>
          <div class="headline-black">
            ¿PROGRAMADOR 10X<br>CON IA?<br>LOS SENIORS DICEN...
          </div>
          <div class="punch-pill">¡ES BURNOUT! 🤯</div>
          <div style="font-size: 32px; font-weight: 800; color: #64748b; margin-top: 20px;">
            La trampa del botón Enter
          </div>
        </div>

        <!-- SCENE 2: LA PESADILLA DEL DÍA A DÍA (8.5s - 20.5s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #991b1b; box-shadow: 4px 4px 0px #ef4444;">SÍNDROME DE LA NIÑERA</div>
          <div class="headline-black" style="font-size: 52px;">
            12 HORAS APRETANDO<br>'ENTER' EN LA TERMINAL
          </div>
          <div class="metric-grid">
            <div class="metric-card danger">
              <span class="metric-val red">+2,000</span>
              <span class="metric-desc">LÍNEAS POR PR<br>SIN LEER</span>
            </div>
            <div class="metric-card danger">
              <span class="metric-val red">"LGTM"</span>
              <span class="metric-desc">APROBADO POR<br>OTRA IA</span>
            </div>
          </div>
          <div style="background: #fee2e2; border: 3px solid #ef4444; color: #b91c1c; padding: 10px 20px; border-radius: 12px; font-weight: 900; font-size: 24px; margin-top: 10px;">
            ⚠️ DEUDA TÉCNICA EXPLOSIVA
          </div>
        </div>

        <!-- SCENE 3: EL COSTE COGNITIVO (20.5s - 33.5s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #7c2d12; box-shadow: 4px 4px 0px #ea580c;">FATIGA COGNITIVA</div>
          <div class="headline-black" style="font-size: 52px;">
            CÓDIGO QUE 'CASI'<br>FUNCIONA
          </div>
          <div class="compare-box">
            <div class="code-line">
              <span class="tag-fast">30 SEG</span>
              <span>Generar 1,000 líneas con agente</span>
            </div>
            <div style="border-top: 2px dashed #475569; margin: 16px 0;"></div>
            <div class="code-line">
              <span class="tag-slow">3 DÍAS</span>
              <span>Depurar la fuga de memoria</span>
            </div>
          </div>
          <div style="font-size: 32px; font-weight: 900; color: #dc2626; margin-top: 15px;">
            💥 Adiós a tu fin de semana.
          </div>
        </div>

        <!-- SCENE 4: LA VERDAD Y REGLA DE ORO (33.5s - 45s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #0f172a; box-shadow: 4px 4px 0px #06b6d4;">CRITERIO ARQUITECTÓNICO</div>
          <div class="headline-black" style="font-size: 56px;">
            NO SEAS UN<br>CAPTURISTA DE PROMPTS
          </div>
          <div class="punch-pill" style="font-size: 38px; background: #000; border-color: #ff4500; color: #ff4500 !important; box-shadow: 8px 8px 0px #ff4500;">
            RECUPERA TU ARQUITECTURA
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 20px;">
            Episodio completo y APA en:
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
    
    # 1. Update build_magazine.py with RESEARCH_DATABASE entry and REELS_MAP
    build_mag_path = BASE_DIR / "build_magazine.py"
    content = build_mag_path.read_text(encoding='utf-8')
    
    # Check if REELS_MAP has the new reel
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'REELS_MAP = {',
            f'REELS_MAP = {{\n    "{EPISODE_FILENAME}": "{REEL_FILENAME}",'
        )
    
    # Research database entry
    res_entry = f'''    # sIA Dev 01 - El Síndrome de la Niñera de Prompts (AI Burnout) - 30 de Octubre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-dev-01-el-sindrome-de-la-ninera-de-prompts-ai-burnout",
        "category": "sIA Tech & Dev",
        "badge_color": "purple",
        "read_time": "10 min",
        "title": "sIA Dev #01: El Síndrome de la Niñera de Prompts: AI Burnout y la Crisis del Code Review",
        "subtitle": "Cuando programar se convirtió en presionar 'Enter' 500 veces al día: El colapso del 'LGTM', los Pull Requests masivos sin auditar, la pérdida de soberanía técnica y el nuevo paradigma de verificación arquitectónica.",
        "thesis": "La Inteligencia Artificial generativa no elimina el trabajo intelectual del programador; cuando se adopta sin rigor arquitectónico, degrada al ingeniero en un burócrata de validación superficial ('niñera de prompts'), acumulando deuda técnica silenciosa que cuadruplica el tiempo de depuración en producción.",
        "nexo": "Primer capítulo de sIA Dev: Análisis sociotécnico, ingeniería de software contemporánea, psicología del desarrollador y verificación determinista.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "title": "1. El Confesionario de Reddit y la Fatiga del 'Botón Enter'",
                "body": """
Durante el último trimestre de 2026, foros de ingeniería como r/programming y r/softwareengineer han registrado una oleada de testimonios de desarrolladores senior con más de una década de experiencia manifestando un agotamiento existencial inédito. El discurso corporativo prometía que la IA liberaría a los programadores del código repetitivo ('boilerplate') para enfocarse en la creatividad arquitectónica. Sin embargo, la experiencia cotidiana en las trincheras de software se ha transformado en lo que la comunidad denomina el 'síndrome de la niñera de prompts'.

En lugar de razonar estructuras de datos complejas o modelar dominios de negocio, los ingenieros pasan entre 10 y 12 horas diarias frente a sus terminales aprobando sugerencias predictivas, aceptando 'diffs' multilínea y supervisando bucles de agentes autónomos. Esta pérdida de autoría directa sobre el código fragmenta la concentración profunda y genera un estado constante de sospecha: el profesional deja de ser un creador para convertirse en un inspector burocrático de lógica ajena que no escribió ni internalizó mentalmente.
"""
            }},
            {{
                "title": "2. La Crisis del Code Review y el Colapso Institucional del 'LGTM'",
                "body": """
El síntoma más peligroso de esta transformación es la degradación del proceso de revisión de código (Code Review). Tradicionalmente, un Pull Request bien estructurado contenía entre 50 y 200 líneas de código con intención clara y trazabilidad de pruebas. Con agentes capaces de modificar docenas de archivos en segundos, los repositorios de las empresas se inundan a diario de Pull Requests gigantescos de 1,500 a 3,000 líneas generadas mecánicamente.

Ante la imposibilidad física y cognitiva de auditar semejante volumen de texto sintético, los equipos caen en la pereza sistémica: los revisores le piden a otra IA que resuma los cambios y responden con el clásico 'LGTM' ('Looks Good To Me') sin verificar condiciones de carrera, inyecciones de dependencias ni supuestos de escalabilidad. Se institucionaliza así un circuito cerrado donde el código lo genera una máquina, lo valida otra máquina de forma superficial y se despliega en producción sin que ningún cerebro humano haya comprendido integralmente su comportamiento en casos extremos.
"""
            }},
            {{
                "title": "3. La Paradoja de la Confianza: 85% de Adopción, Mínimos Históricos de Fe",
                "body": """
Las métricas recientes de la industria reflejan una paradoja contundente: mientras la adopción de herramientas de IA entre ingenieros de software supera el 85%, la confianza en la corrección matemática y lógica del código generado se sitúa en mínimos históricos. Esto se debe a la naturaleza de las fallas contemporáneas: ya no se trata de errores sintácticos burdos que el compilador detiene al instante, sino de código 'casi correcto'.

Un agente moderno redacta funciones con excelente formato visual, variables descriptivas y comentarios convincentes, pero oculta suposiciones erróneas sobre el estado transaccional o filtraciones de memoria en concurrencia. Investigaciones empíricas demuestran que localizar y corregir una alucinación silenciosa en 500 líneas de código generado toma entre tres y cinco veces más tiempo y desgaste cognitivo que escribir el componente desde cero con pruebas de diseño guiadas por el dominio (TDD).
"""
            }},
            {{
                "title": "4. La Solución Arquitectónica: Inversión del Control y Verificación Determinista",
                "body": """
Para rescatar la dignidad del trabajo técnico y blindar la confiabilidad de los sistemas, la ingeniería de software debe invertir la jerarquía de control. La regla de oro en producción establece que jamás debe permitirse a un modelo probabilístico escribir una sola línea de código antes de que el ingeniero humano haya definido formalmente el contrato determinista del componente.

Esto implica diseñar primero interfaces estrictamente tipadas (TypeSafe, Pydantic, Zod), contratos semánticos y una suite de pruebas de integración inmutables que actúen como árbitros inviolables. El agente de IA puede proponer la implementación dentro de un entorno aislado, pero su trabajo se rechaza automáticamente si falla un solo test. Recuperar la soberanía del desarrollador exige entender que la velocidad no reside en la cantidad de líneas vomitadas por segundo, sino en la solidez del diseño arquitectónico que evita colapsos a las tres de la madrugada.
"""
            }}
        ],
        "apa_references": [
            "Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps: Building and Scaling High Performing Technology Organizations*. IT Revolution Press.",
            "Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.",
            "Stack Overflow. (2025). *Developer Survey 2025: AI Tools, Trust Deficits, and the Evolving Role of Code Review*. Stack Overflow Research.",
            "GitHub & Stanford University. (2024). *The Impact of Generative AI on Developer Velocity and Software Quality: A Longitudinal Case Study*. ACM Transactions on Software Engineering.",
            "Corona, C., & sIA Editora. (2026). *sIA Dev #01: El síndrome de la niñera de prompts, el colapso del LGTM y la soberanía del software en la era de los agentes*. sIA Technology Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if "sia-dev-01-el-sindrome-de-la-ninera-de-prompts-ai-burnout" not in content:
        content = content.replace(
            'RESEARCH_DATABASE = {',
            'RESEARCH_DATABASE = {\n' + res_entry
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Entrada de investigación inyectada en build_magazine.py")

    # Run build_magazine.py
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
    
    # 1. Copiar Reels
    src_reel = REELS_DIR / REEL_FILENAME
    src_poster = REELS_DIR / REEL_POSTER_FILENAME
    if src_reel.exists():
        shutil.copy2(src_reel, GDRIVE_REELS / REEL_FILENAME)
        print(f"  -> Reel copiado a Google Drive: {GDRIVE_REELS / REEL_FILENAME}")
    if src_poster.exists():
        shutil.copy2(src_poster, GDRIVE_REELS / REEL_POSTER_FILENAME)
        print(f"  -> Póster copiado a Google Drive: {GDRIVE_REELS / REEL_POSTER_FILENAME}")

    # 2. Copiar Audio Completo
    src_audio = AUDIO_DIR / EPISODE_FILENAME
    if src_audio.exists():
        shutil.copy2(src_audio, GDRIVE_AUDIO / EPISODE_FILENAME)
        print(f"  -> Audio copiado a Google Drive: {GDRIVE_AUDIO / EPISODE_FILENAME}")

def step7_create_obsidian_and_social_kit():
    print("\n" + "="*70)
    print("🧠 PASO 7: Creando Ficha de Obsidian & Kit de Redes Sociales...")
    print("="*70)
    
    obsidian_reel_note = f"""---
id: reel-stupy-02
titulo: "El Síndrome de la Niñera de Prompts: Cuando Programar se Convirtió en Presionar 'Enter' 500 Veces al Día"
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
  - dev-burnout
  - code-review
  - prompt-babysitting
---

# 🤖 El Síndrome de la Niñera de Prompts (AI Burnout)

> **Estilo Visual:** Cómic-Pop Halftone Matrix, Pop-in Neón Coral, Tarjeta Escudo 20px Solid Shadow, Audio EBU R128 (-16 LUFS).

---

## 🎬 Reproductor del Video (Vertical 9:16)
![[reels/{REEL_FILENAME}]]

**Póster Oficial:**
![[reels/{REEL_POSTER_FILENAME}|350]]

---

## 📱 Kit de Copys & Hashtags para Publicación en Móvil (TikTok / Shorts / Instagram / LinkedIn)

### 🎯 Título Gancho (Hook):
`¿Desarrollador 10X o niñera de prompts? La verdad del AI Burnout 🤯`

### ✍️ Descripción para Redes (Copy de Alto Alcance):
> Cientos de desarrolladores senior están confesando en Reddit lo que nadie se atreve a decir: la IA no los hizo más libres, los convirtió en validadores de alucinaciones apretando "Enter" 12 horas al día.
>
> Pull Requests de 2,000 líneas que nadie lee y todo el equipo aprueba con un "LGTM". ¿Te ha pasado en tu empresa? 👇 Cuéntanos en los comentarios.

### 🏷️ Bloque de Hashtags Estratégicos:
```
#programacion #softwareengineer #inteligenciaartificial #devlife #tecnologia #aprendeentiktok #codereview #burnout #desarrolloweb #podcasttech
```

---

## 🎙️ Guion & Voces (Jorge & Dalia +6%)

### Escena 1: El Gancho del Mito (00:00 - 08:50)
* **JORGE:** ¿Creías que usar agentes de Inteligencia Artificial te haría un programador diez veces más rápido? En Reddit y Silicon Valley los desarrolladores senior están confesando la verdad...
* *Animación:* Badge pop-in `¡ES BURNOUT! 🤯` inclinado a -3° con sombra dura.

### Escena 2: La Pesadilla del Día a Día (08:50 - 20:50)
* **DALIA:** Bienvenido al síndrome de la niñera de prompts: pasas doce horas al día solo apretando la tecla Enter para validar código que tú no escribiste... ¡y que tu equipo aprueba con un 'LGTM' sin leerlo!
* *Animación:* Tarjetas métricas rojas: `+2,000 LÍNEAS POR PR` y `"LGTM" APROBADO POR OTRA IA`.

### Escena 3: El Coste Cognitivo (20:50 - 33:50)
* **JORGE:** Generar mil líneas toma treinta segundos. Pero encontrar la alucinación silenciosa que tumba la base de datos te cuesta tu salud mental, tu fin de semana y la caída de producción.
* *Animación:* Terminal negra de código comparativo `30 SEG Generar` vs `3 DÍAS Buscar el leak`.

### Escena 4: La Verdad y Regla de Oro (33:50 - 45:00)
* **DALIA:** Si no entiendes la arquitectura, no eres un ingeniero: eres un capturista de prompts. Recupera tu criterio técnico en `escucha-sia.github.io` y en *sIA Podcast*.
* *Animación:* Píldora cian neón con URL destacada.

---

## 🔗 Referencias & Backlinks
* **Artículo Web Completo con Fuentes APA:** [[03_Articulos/sia-dev-01-el-sindrome-de-la-ninera-de-prompts-ai-burnout]]
* **Episodio Podcast MP3:** `audio/{EPISODE_FILENAME}`
* **Ruta Google Drive (Móvil):** `G:\\Mi unidad\\sIA_Hub\\01_Reels_Verticales\\{REEL_FILENAME}`
"""
    note_path = BASE_DIR / "02_Reels_Shorts" / f"{Path(REEL_FILENAME).stem}.md"
    note_path.write_text(obsidian_reel_note, encoding='utf-8')
    print(f"✅ Ficha de Obsidian creada: {note_path}")
    
    # Replicar ficha al Vault de Google Drive
    vault_dest = GDRIVE_VAULT / "02_Reels_Shorts"
    vault_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(note_path, vault_dest / note_path.name)
    print(f"✅ Ficha sincronizada a Google Drive Vault: {vault_dest / note_path.name}")

def step8_git_deploy():
    print("\n" + "="*70)
    print("🚀 PASO 8: Commiteando y Desplegando a GitHub Pages...")
    print("="*70)
    
    subprocess.run(["git", "add", "."], cwd=str(BASE_DIR), check=True)
    msg = f"feat(episode): publish sIA Dev 01 - El Sindrome de la Ninera de Prompts & Reel Stupy 02"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(BASE_DIR), check=True)
    
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if push_res.returncode == 0:
        print("🎉 ¡Despliegue a GitHub Pages exitoso!")
    else:
        print("⚠️ Advertencia al hacer push:", push_res.stderr)

async def main():
    await step1_generate_full_audio()
    await step2_generate_reel_audio()
    step3_write_hyperframes_html()
    step4_render_reel()
    step5_register_and_rebuild_magazine()
    step6_sync_to_gdrive()
    step7_create_obsidian_and_social_kit()
    step8_git_deploy()
    print("\n" + "🎉"*30)
    print("🏆 ¡EPISODIO 1 PRODUCIDO Y DESPLEGADO AL 100%!")
    print("🎉"*30)

if __name__ == '__main__':
    asyncio.run(main())
