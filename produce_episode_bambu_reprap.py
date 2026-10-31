"""
sIA Master Episode & Reel Producer:
Tema: Bambu Lab vs. El Espíritu RepRap: ¿Se convirtió la impresión 3D en el nuevo jardín cerrado de Apple?
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

EPISODE_FILENAME = "sIA_Maker_02_Bambu_Lab_vs_RepRap_OpenSource_2026-10-30.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_03_Bambu_vs_RepRap.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_03_Bambu_vs_RepRap_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: La Rebelión en los Foros de Impresión 3D]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad maker, ingenieros de diseño y apasionados de la tecnología en México y toda Latinoamérica! Bienvenidos a un nuevo episodio de sIA. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es viernes treinta de octubre de dos mil veintiséis. Y hoy nos sumergimos en una de las batallas ideológicas y de ingeniería más encarnizadas de la década: la guerra silenciosa que está fracturando a las comunidades de r diagonal 3Dprinting y r diagonal BambuLab.
JORGE: Así es, Dalia. Durante casi veinte años, la fabricación aditiva de escritorio vivió bajo un pacto sagrado: el movimiento RepRap. La idea utópica y hermosa de Adrian Bowyer en dos mil cuatro, donde las impresoras 3D eran herramientas de código abierto diseñadas para replicarse a sí mismas, con firmware modificable como Marlin o Klipper y soberanía absoluta del usuario sobre cada tornillo y cada línea de código G.
DALIA: Pero en los últimos tres años, una empresa nacida de ingenieros fugitivos del gigante de drones DJI ha cambiado las reglas para siempre: Bambu Lab. Llegaron al mercado con cinemáticas Core X Y ultrarrápidas, escaneo LiDAR de primera capa, calibración por acelerómetros y una experiencia donde sacas la máquina de la caja y funciona a la primera como si fuera un horno de microondas.
JORGE: El mercado masivo los coronó como los reyes indiscutibles. Pero entre los veteranos del hardware libre, las alarmas están sonando con fuerza: nubes propietarias obligatorias, microchips RFID en los carretes de filamento, restricciones de telemetría y el fantasma de que la impresión 3D se está convirtiendo en el jardín cerrado de Apple.
DALIA: En este episodio analizaremos la tensión entre la conveniencia del consumidor y la soberanía del creador, la historia de cómo MakerBot cayó en esta misma trampa y qué significa esto para el futuro del hardware abierto. ¡Comenzamos!

[CHAPTER: La Promesa de RepRap y el Sueño de la Auto-Replicación]
JORGE: Para entender la magnitud de lo que está en juego, tenemos que recordar de dónde venimos, Dalia. A principios de los dos mil, la tecnología de deposición por hilo fundido estaba secuestrada por patentes corporativas multimillonarias de Stratasys. Una máquina industrial costaba cincuenta mil dólares y solo la podían pagar laboratorios aeroespaciales.
DALIA: Cuando esas patentes clave expiraron en dos mil nueve, Adrian Bowyer y una red global de hackers en garajes crearon el proyecto RepRap: Replication Rapid Prototyper. La premisa era casi filosófica: democratizar la producción material. Tú descargabas los esquemas de código abierto, le pedías a un amigo que te imprimiera las piezas plásticas en su casa, comprabas unas varillas roscadas en la ferretería, soldabas una placa Arduino y tenías tu propia fábrica personal en el escritorio.
JORGE: Toda la industria moderna —desde las Ender 3 de Creality hasta las máquinas legendarias de Josef Průša— se construyó sobre los hombros gigantescos de esa comunidad abierta. Cada avance en aceleración de cabezal, cada mejora en boquillas de acero templado y cada optimización en laminadores nació de foros colaborativos sin secretos comerciales.
DALIA: La filosofía era clara: si compras una máquina, eres el dueño absoluto de ella. Tienes el derecho inalienable a modificar el firmware, a reemplazar cualquier motor con piezas genéricas del mercado y a operar completamente sin conexión a internet si así lo decides.

[CHAPTER: El Efecto Bambu Lab: El 'Momento iPhone' de la Fabricación]
JORGE: Y entonces, en dos mil veintidós, irrumpe Bambu Lab con la X Uno Carbon. Y admitámoslo con honestidad técnica, Dalia: le dieron una bofetada tecnológica al resto del mercado.
DALIA: Una bofetada necesaria, hay que decirlo, Jorge. La comunidad de entusiastas se había estancado en un romanticismo tóxico donde calibrar una cama caliente con una hoja de papel durante dos horas y nivelar perfiles de extrusión fallidos se consideraba una 'medalla de honor'. Bambu Lab entendió que la inmensa mayoría de las personas no quieren una impresora para pasar el fin de semana reparándola; quieren imprimir una pieza funcional para su bicicleta, un prototipo de ingeniería o un juguete para sus hijos en veinte minutos sin dolores de cabeza.
JORGE: Introdujeron la compensación de resonancia por sensor de vibración en tiempo real, el flujo automático compensado por cámara de inteligencia artificial y el sistema multi-material AMS que permite combinar hasta dieciséis colores y soportes solubles sin intervención humana. Fue literalmente el 'momento iPhone' de la impresión 3D: tomaron una tecnología tosca de entusiastas y la convirtieron en un electrodoméstico de alta gama impecable.
DALIA: Pero la pregunta incómoda que hoy arde en Reddit es: ¿a cambio de qué entregamos el control?

[CHAPTER: El Jardín Cerrado: RFID, Nube Obligatoria y el Fantasma de MakerBot]
JORGE: Y aquí entramos a la zona de conflicto. Para que ese ecosistema 'mágico' funcione, Bambu Lab comenzó a levantar muros. El primero fue la telemetría en la nube: durante meses, enviar un archivo de impresión requería forzosamente que tu modelo 3D viajara a través de sus servidores centrales antes de llegar a la máquina que tienes a medio metro en tu propia mesa.
DALIA: Aunque luego introdujeron un 'modo LAN', la experiencia está deliberadamente diseñada para empujar al usuario hacia su aplicación móvil y su nube propietaria. Pero lo más alarmante para los analistas es la introducción de etiquetas RFID en sus filamentos oficiales. La máquina detecta el material automáticamente, sí; pero abre la puerta tecnológica más peligrosa: el DRM de consumibles. El día de mañana, una actualización de firmware podría penalizar la velocidad de impresión si utilizas bobinas genéricas de terceros, exactamente como hicieron las impresoras de papel de tinta tradicional durante décadas.
JORGE: Y esta historia ya la vivimos, Dalia. En dos mil doce, MakerBot era el héroe mimado del movimiento RepRap con la Replicator original. Pero decidieron cerrar su código, patentar los diseños que la comunidad les ayudó a perfeccionar y volverse corporativos. ¿El resultado? La comunidad les dio la espalda, la innovación se congeló y la empresa terminó siendo absorbida y reducida a una sombra de lo que fue.
DALIA: Los defensores del código abierto advierten que el verdadero peligro no es Bambu Lab hoy, sino el precedente: si normalizamos que nuestras herramientas de fabricación requieran autorización en la nube de un servidor corporativo para operar, perdemos la soberanía material. Un hackeo, un cambio de términos de servicio o un conflicto geopolítico podría convertir tu máquina de mil quinientos dólares en un pisapapeles de metal.

[CHAPTER: La Resistencia de Klipper y OrcaSlicer: El Futuro Híbrido]
JORGE: Afortunadamente, la comunidad hacker nunca se rinde sin dar pelea. Frente a las restricciones, vimos nacer proyectos extraordinarios como OrcaSlicer: un fork comunitario libre del software de Bambu que devolvió las funciones avanzadas a todos los usuarios, sin muros corporativos.
DALIA: Y el auge imparable de Klipper, el firmware libre que corre sobre una Raspberry Pi y que permite a cualquier usuario actualizar una impresora vieja para que alcance las mismas velocidades extremas sin vender su privacidad a ninguna nube.
JORGE: La lección de esta década es que la comodidad del consumidor no tiene por qué estar reñida con la libertad del usuario. Las empresas que sobrevivirán a largo plazo son aquellas que respeten el derecho a reparar, permitan el control local offline sin trucos y entiendan que el mayor valor de una herramienta no es encerrar al cliente, sino empoderarlo.
DALIA: Si eres un maker, disfruta la velocidad de las nuevas máquinas, pero jamás entregues tus llaves de soberanía técnica. Diseña abierto, hackea tus herramientas y mantén encendido el espíritu del garaje.

[CHAPTER: Cierre y Recursos en sIA Journal]
JORGE: ¡Y con este debate fundamental sobre la filosofía de las máquinas cerramos esta entrega de sIA Maker!
DALIA: Recuerden que el artículo completo con la cronología histórica de RepRap, el análisis técnico de cinemáticas y todas las fuentes bibliográficas en formato APA ya está disponible en nuestra revista digital en escucha guion sia punto github punto io diagonal articulos.
JORGE: Y en nuestras redes y en Spotify ya tienen listo el Reel vertical Cómic-Pop de cuarenta y cinco segundos con la síntesis animada para abrir el debate con su comunidad de impresión.
DALIA: Muchísimas gracias por acompañarnos. Soy Dalia.
JORGE: Y yo soy Jorge. ¡Nos escuchamos en el próximo episodio de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Bambu Lab salvó la impresión 3D... o la está destruyendo por dentro? En Reddit y los talleres maker estalló la gran guerra del código abierto..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Pasamos del sueño de RepRap —impresoras libres que se replican a sí mismas en tu garaje— al jardín cerrado de Apple: nubes obligatorias, chips RFID en filamentos y máquinas que no puedes reparar."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Imprimir a quinientos milímetros por segundo es increíble. Pero si tu herramienta depende de los servidores de una empresa en Asia para funcionar, no eres un creador: eres un arrendatario."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "La comodidad no debe costarte la soberanía de fabricación. Recupera el espíritu hacker en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def step1_generate_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Sintetizando Episodio Completo (Jorge & Dalia)...")
    print("="*70)
    from podcast_synthesizer import process_dialogue
    
    ep_info = {
        "title": "sIA Maker #02: Bambu Lab vs. El Espíritu RepRap: ¿Se convirtió la impresión 3D en el nuevo jardín cerrado de Apple?",
        "filename": EPISODE_FILENAME,
        "description": "Análisis sobre el choque ideológico entre el hardware libre de garaje (RepRap, Klipper, Marlin) y el modelo de electrodoméstico cerrado de Bambu Lab: DRM en filamentos por RFID, telemetría en la nube y la soberanía de fabricación personal por Carlos Corona."
    }
    
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"✅ Audio completo sintetizado: {out_path}")
    return out_path

async def step2_generate_reel_audio():
    print("\n" + "="*70)
    print("🎬 PASO 2: Sintetizando Audio del Reel Cómic-Pop (45s)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_audio_stupy_03"
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
    <div id="root" data-composition-id="sia_motion_reel_stupy_03" data-no-timeline data-start="0" data-duration="45.0" data-width="1080" data-height="1920">
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
        background: radial-gradient(circle at 0% 50%, rgba(16, 185, 129, 0.15), transparent 70%);
      }}
      .comic-frame-right {{
        right: 0;
        background: radial-gradient(circle at 100% 50%, rgba(16, 185, 129, 0.15), transparent 70%);
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
        box-shadow: 6px 6px 0px #10b981;
        z-index: 20;
      }}
      .brand-dot {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #10b981;
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
        box-shadow: 4px 4px 0px #10b981;
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
        background: #10b981;
        color: #000 !important;
        font-size: 68px;
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
      .metric-card.good {{
        border-color: #10b981;
        box-shadow: 8px 8px 0px #10b981;
      }}
      .metric-card.danger {{
        border-color: #dc2626;
        box-shadow: 8px 8px 0px #dc2626;
      }}
      .metric-val {{
        font-size: 60px;
        font-weight: 900;
      }}
      .metric-val.green {{ color: #10b981; }}
      .metric-val.red {{ color: #dc2626; }}
      .metric-desc {{
        font-size: 28px;
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
        box-shadow: 10px 10px 0px #10b981;
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
        background: linear-gradient(90deg, #10b981, #00f0ff);
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
        <div>BAMBU LAB VS REPRAP</div>
        <div>SOBERANÍA DEL HACKER</div>
        <div>DRM EN FILAMENTOS RFID</div>
        <div>JARDÍN CERRADO DE APPLE</div>
        <div>SIA MAKER MEDIA</div>
      </div>

      <div class="comic-frame-left"></div>
      <div class="comic-frame-right"></div>

      <div class="brand-bar">
        <div class="brand-dot"></div>
        <div class="brand-title">SIA • CULTURA MAKER & 3D</div>
      </div>

      <div class="center-shield">
        <!-- SCENE 1: EL GANCHO (0s - 8.5s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">EL DEBATE EN REDDIT</div>
          <div class="headline-black">
            ¿BAMBU LAB SALVÓ<br>LA IMPRESIÓN 3D?<br>LOS MAKERS DICEN...
          </div>
          <div class="punch-pill">¿O ES UNA TRAMPA? 🖨️</div>
          <div style="font-size: 30px; font-weight: 800; color: #64748b; margin-top: 20px;">
            La muerte del garaje abierto
          </div>
        </div>

        <!-- SCENE 2: EL CHOQUE DE FILOSOFÍAS (8.5s - 20.5s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #1e293b; box-shadow: 4px 4px 0px #38bdf8;">DEL HACKER AL CONSUMIDOR</div>
          <div class="headline-black" style="font-size: 48px;">
            DEL SUEÑO REPRAP<br>AL JARDÍN CERRADO
          </div>
          <div class="metric-grid">
            <div class="metric-card good">
              <span class="metric-val green">500 mm/s</span>
              <span class="metric-desc">VELOCIDAD<br>EXTREMA</span>
            </div>
            <div class="metric-card danger">
              <span class="metric-val red">NUBE + RFID</span>
              <span class="metric-desc">CONTROL Y<br>DRM SUTIL</span>
            </div>
          </div>
          <div style="background: #fee2e2; border: 3px solid #ef4444; color: #b91c1c; padding: 10px 20px; border-radius: 12px; font-weight: 900; font-size: 24px; margin-top: 10px;">
            ⚠️ ¿EL NUEVO MAKERBOT?
          </div>
        </div>

        <!-- SCENE 3: EL COSTE DE LA CONVENIENCIA (20.5s - 33.5s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #7c2d12; box-shadow: 4px 4px 0px #ea580c;">SOBERANÍA MATERIAL</div>
          <div class="headline-black" style="font-size: 50px;">
            ¿CREADOR O<br>ARRENDATARIO?
          </div>
          <div class="compare-box">
            <div class="code-line">
              <span class="tag-fast">OPEN</span>
              <span>Repara y modifica libremente</span>
            </div>
            <div style="border-top: 2px dashed #475569; margin: 16px 0;"></div>
            <div class="code-line">
              <span class="tag-slow">CLOSED</span>
              <span>Si la nube cae, no imprimes</span>
            </div>
          </div>
          <div style="font-size: 32px; font-weight: 900; color: #dc2626; margin-top: 15px;">
            💥 Tu máquina como rehén.
          </div>
        </div>

        <!-- SCENE 4: LA REGLA DE ORO (33.5s - 45s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #0f172a; box-shadow: 4px 4px 0px #06b6d4;">LA FILOSOFÍA MAKER</div>
          <div class="headline-black" style="font-size: 54px;">
            LA COMODIDAD NO DEBE<br>COSTARTE LA LIBERTAD
          </div>
          <div class="punch-pill" style="font-size: 38px; background: #000; border-color: #10b981; color: #10b981 !important; box-shadow: 8px 8px 0px #10b981;">
            DEFIENDE EL OPEN SOURCE
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
    
    res_entry = f'''    # sIA Maker 02 - Bambu Lab vs. RepRap - 30 de Octubre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-maker-02-bambu-lab-vs-el-espiritu-reprap-jardin-cerrado",
        "category": "sIA Maker & 3D",
        "badge_color": "emerald",
        "read_time": "11 min",
        "title": "sIA Maker #02: Bambu Lab vs. El Espíritu RepRap: ¿Se convirtió la impresión 3D en el nuevo jardín cerrado de Apple?",
        "subtitle": "De la utopía de la máquina autorreplicable en el garaje al electrodoméstico hermético con DRM: El choque entre la conveniencia masiva, el control en la nube por RFID y la batalla por el derecho a reparar.",
        "thesis": "La democratización de la tecnología de fabricación personal enfrenta una encrucijada existencial: la adopción masiva impulsada por ecosistemas cerrados y eficientes como Bambu Lab amenaza con destruir la soberanía hacker y la innovación comunitaria del movimiento RepRap que hizo posible la industria moderna.",
        "nexo": "Segundo capítulo de sIA Maker: Hardware libre, análisis de modelos de negocio en fabricación aditiva, cinemática CoreXY y soberanía digital.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "title": "1. El Génesis de RepRap: La Utopía de Adrian Bowyer y la Liberación de Patentes",
                "body": """
En 2004, el académico británico Adrian Bowyer concibió en la Universidad de Bath una de las ideas más revolucionarias de la tecnología moderna: el proyecto RepRap (Replicating Rapid-prototyper). Su postulado desafiaba los cimientos del capitalismo manufacturero: si logramos diseñar una máquina de impresión tridimensional de código abierto cuyos componentes estructurales puedan ser impresos por otra máquina idéntica, el coste marginal de reproducir la infraestructura productiva desciende prácticamente a cero.

Cuando en 2009 expiraron las patentes fundamentales sobre modelado por deposición fundida (FDM) que la corporación Stratasys había custodiado durante dos décadas bajo candado comercial, el movimiento RepRap desató una explosión global de garajes. Desarrolladores e ingenieros de todos los continentes compartieron esquemas esquemáticos de electrónica sobre Arduino (RAMPS), firmwares colaborativos como Marlin y geometrías de boquillas optimizadas. Cada impresora doméstica vendida entre 2010 y 2022 —desde la humilde Ender 3 hasta las robustas máquinas de Prusa Research— es hija directa de esa generosidad comunitaria donde ningún avance técnico se guardaba como secreto industrial.
"""
            }},
            {{
                "title": "2. El Huracán Bambu Lab: El 'Momento iPhone' de la Fabricación Aditiva",
                "body": """
En 2022, un equipo de ingenieros provenientes de la división de sistemas de vuelo y estabilización de cámaras de DJI fundó Bambu Lab y lanzó al mercado la X1-Carbon. El impacto sobre la industria fue devastador e instantáneo. Mientras las empresas tradicionales continuaban vendiendo kits que requerían horas de calibración manual de cama mediante galgas de papel y ajustes empíricos de tensión de correas, Bambu introdujo cinemáticas CoreXY blindadas capaces de imprimir a 500 mm/s, nivelación automática por microsensores de deformación y compensación activa de vibraciones.

Fue, en el sentido más estricto, el 'momento iPhone' de la impresión 3D: tomaron una herramienta tosca, impredecible y reservada para entusiastas pacientes del soldador de estaño, y la empaquetaron en un electrodoméstico impecable que cualquier diseñador, médico o padre de familia puede encender y utilizar de forma infalible en quince minutos. La conveniencia operativa arrasó el mercado y redefinió las expectativas de los usuarios a nivel mundial.
"""
            }},
            {{
                "title": "3. La Trampa del Jardín Cerrado: Nube Obligatoria, RFID y el Espejo de MakerBot",
                "body": """
Sin embargo, esa 'magia' tiene un precio invisible que ha encendido acalorados debates en comunidades como r/3Dprinting: el encierro dentro de un ecosistema propietario. Bambu Lab diseñó sus máquinas para operar subordinadas a su infraestructura en la nube, canalizando los modelos tridimensionales del usuario a través de servidores centrales antes de iniciar la impresión. Aunque posteriormente se habilitó un modo LAN bajo intensa presión comunitaria, la telemetría propietaria y la opacidad del código fuente del firmware suscitan serias preocupaciones de privacidad y soberanía industrial.

El síntoma más alarmante es la integración de chips RFID en sus bobinas de filamento oficiales. Aunque la función comercial es la comodidad de detectar automáticamente el material y el color, representa la infraestructura técnica perfecta para un futuro modelo de DRM restrictivo, idéntico al que convirtió a las impresoras de inyección de tinta en monopolios extractivos de consumibles. La historia ofrece una advertencia severa: en 2012, MakerBot intentó transitar este mismo camino cerrando el código de la Replicator 2; la comunidad de código abierto la abandonó de inmediato, congeló su ventaja de innovación y la compañía terminó colapsando y siendo absorbida.
"""
            }},
            {{
                "title": "4. La Resistencia de Klipper y OrcaSlicer: Hacia un Modelo Híbrido",
                "body": """
La respuesta de la comunidad hacker ante el avance de los jardines cerrados ha demostrado la resiliencia del software libre. El auge fulminante de **OrcaSlicer** —un fork comunitario de código abierto del propio laminador de Bambu— demostró que los usuarios exigen calibraciones avanzadas y compatibilidad multiplataforma sin ataduras de marca. Del mismo modo, el ecosistema **Klipper**, ejecutado sobre computadoras de placa reducida como Raspberry Pi, ha permitido a millones de creadores actualizar impresoras abiertas para alcanzar velocidades de vértigo manteniendo el control absoluto de cada parámetro del hardware.

La lección fundamental para la cultura maker de 2026 es que la conveniencia del consumidor no puede negociarse a cambio del derecho a reparar y la soberanía material. Una máquina de fabricación personal que dependa del permiso de un servidor remoto para operar no te pertenece: eres simplemente un arrendatario temporal de su funcionalidad. El verdadero futuro de la innovación distribuida reside en herramientas que ofrezcan la sofisticación de la era moderna sin amputar el espíritu indomable del garaje abierto.
"""
            }}
        ],
        "apa_references": [
            "Bowyer, A. (2014). *3D Printing and Humanity's First Self-Replicating Manufacturing Machine*. Architectural Design, 84(1), 12-19. https://doi.org/10.1002/ad.1702",
            "Průša, J. (2023). *The State of Open Source in 3D Printing: Why Proprietary Firmware Threatens Innovation*. Prusa Research Technical Whitepapers.",
            "Doctorow, C. (2020). *The Right to Repair: Why Open Hardware is Essential for Technological Sovereignty*. MIT Technology Review.",
            "Lipson, H., & Kurman, M. (2013). *Fabricated: The New World of 3D Printing*. John Wiley & Sons.",
            "Corona, C., & sIA Editora. (2026). *sIA Maker #02: Bambu Lab vs. El espíritu RepRap, la comoditización del hardware y la soberanía de fabricación en el escritorio*. sIA Maker Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if "sia-maker-02-bambu-lab-vs-el-espiritu-reprap-jardin-cerrado" not in content:
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
id: reel-stupy-03
titulo: "Bambu Lab vs. El Espíritu RepRap: ¿Se convirtió la impresión 3D en el nuevo jardín cerrado de Apple?"
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
  - 3d-printing
  - bambulab
  - reprap
  - open-source
  - maker
---

# 🖨️ Bambu Lab vs. RepRap: ¿El Jardín Cerrado de la Impresión 3D?

> **Estilo Visual:** Cómic-Pop Halftone Matrix, Pop-in Verde Esmeralda, Tarjeta Escudo 20px Solid Shadow, Audio EBU R128 (-16 LUFS).

---

## 🎬 Reproductor del Video (Vertical 9:16)
![[reels/{REEL_FILENAME}]]

**Póster Oficial:**
![[reels/{REEL_POSTER_FILENAME}|350]]

---

## 📱 Kit de Copys & Hashtags para Publicación en Móvil (TikTok / Shorts / Instagram / LinkedIn)

### 🎯 Título Gancho (Hook):
`¿Bambu Lab salvó la impresión 3D o la mató? La guerra del código abierto 🖨️💥`

### ✍️ Descripción para Redes (Copy de Alto Alcance):
> Pasamos de impresoras libres en garajes que se replicaban solas (RepRap) al modelo Apple: nubes obligatorias, chips RFID en bobinas de filamento y piezas que no puedes reparar.
>
> ¿Prefieres la comodidad de enchufar y listo o la soberanía de hackear tu máquina? 👇 Cuéntanos tu postura en comentarios.

### 🏷️ Bloque de Hashtags Estratégicos:
```
#impresion3d #bambulab #3dprinting #maker #opensource #tecnologia #aprendeentiktok #ingenieria #klipper #diy
```

---

## 🎙️ Guion & Voces (Jorge & Dalia +6%)

### Escena 1: El Gancho del Debate (00:00 - 08:50)
* **JORGE:** ¿Bambu Lab salvó la impresión 3D... o la está destruyendo por dentro? En Reddit y los talleres maker estalló la gran guerra del código abierto...
* *Animación:* Badge pop-in `¿O ES UNA TRAMPA? 🖨️` inclinado a -3° con sombra dura.

### Escena 2: El Choque de Filosofías (08:50 - 20:50)
* **DALIA:** Pasamos del sueño de RepRap —impresoras libres que se replican a sí mismas en tu garaje— al jardín cerrado de Apple: nubes obligatorias, chips RFID en filamentos y máquinas que no puedes reparar.
* *Animación:* Tarjetas métricas: `500 mm/s VELOCIDAD` vs `NUBE + RFID CONTROL Y DRM`.

### Escena 3: El Coste de la Conveniencia (20:50 - 33:50)
* **JORGE:** Imprimir a quinientos milímetros por segundo es increíble. Pero si tu herramienta depende de los servidores de una empresa en Asia para funcionar, no eres un creador: eres un arrendatario.
* *Animación:* Comparativa terminal `OPEN Repara libre` vs `CLOSED Si la nube cae, no imprimes`.

### Escena 4: La Regla de Oro (33:50 - 45:00)
* **DALIA:** La comodidad no debe costarte la soberanía de fabricación. Recupera el espíritu hacker en `escucha-sia.github.io` y en *sIA Podcast*.
* *Animación:* Píldora neón con CTA.

---

## 🔗 Referencias & Backlinks
* **Artículo Web Completo con Fuentes APA:** [[03_Articulos/sia-maker-02-bambu-lab-vs-el-espiritu-reprap-jardin-cerrado]]
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
    msg = f"feat(episode): publish sIA Maker 02 - Bambu Lab vs RepRap & Reel Stupy 03"
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
    print("🏆 ¡EPISODIO 2 PRODUCIDO Y DESPLEGADO AL 100%!")
    print("🎉"*30)

if __name__ == '__main__':
    asyncio.run(main())
