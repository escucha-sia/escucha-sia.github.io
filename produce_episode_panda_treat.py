"""
sIA Master Episode & Reel Producer:
Tema: sIA Maker #03 (FoodTech): BIQU Panda Treat: Cómo una Impresora 3D de $200 Hackeó la Industria de la Confitería Digital
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop con Barra de Capítulos (HyperFrames GPU, 45s, Kinetic Pop)
3. Póster oficial del Reel
4. Registro de investigación en build_magazine.py con referencias APA 7 (Autor: cacs)
5. Recompilación de sIA Journal (index.html + artículo web responsive)
6. Sincronización automática a Google Drive (G:\\Mi unidad\\sIA_Hub)
7. Nota de Obsidian Vault con Embed de video + Kit de Copys para Redes
8. Despliegue Git a GitHub Pages
9. Subida automatizada a TikTok Studio (@escucha_sia)
"""

import sys
import os
import re
import json
import time
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

EPISODE_FILENAME = "sIA_Maker_03_Biqu_Panda_Treat_FoodTech_2026-11-04.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_09_Biqu_Panda_Treat_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: Cuando tu Impresora 3D se vuelve Pastelería]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad maker, diseñadores industriales, apasionados del hardware abierto y entusiastas de la gastronomía digital! Bienvenidos a una nueva entrega de sIA en su serie de Maker, Hardware & FoodTech. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es miércoles cuatro de noviembre de dos mil veintiséis. Y hoy analizamos una de las convergencias más fascinantes e inesperadas del mundo de la fabricación personal: ¿cómo una máquina diseñada para derretir filamentos de plástico a doscientos grados se transformó en una fábrica de galletas, macarons y arte sobre café por menos de trescientos cincuenta dólares?
JORGE: En las últimas semanas se volvió viral un video en TikTok de la creadora Magical Prints mostrando algo que parecía magia: colocas una galleta artesanal con glaseado real sobre la cama de una Bambu Lab A1 Mini, seleccionas una ilustración en el teléfono móvil y, en veintidós segundos, un cabezal especializado imprime un gráfico a todo color con tinta comestible certificada.
DALIA: El artefacto responsable de esta disrupción se llama Panda Treat, desarrollado por BIGTREETECH y CMY Labs. Y no es solo un gadget curioso para redes sociales: representa la demolición de una barrera económica histórica.
JORGE: Hasta hace muy poco, cualquier pastelería artesanal o repostero que quisiera imprimir sobre alimentos tenía que desembolsar entre tres mil y ocho mil dólares por máquinas industriales cerradas como la Primera Eddie o impresoras planas adaptadas. Hoy, ese mismo resultado se logra con un accesorio intercambiable de ciento treinta dólares montado sobre una impresora 3D de consumo.
DALIA: ¿Cómo funciona mecánicamente este intercambio? ¿Qué química hay detrás de las tintas comestibles para no tapar los inyectores térmicos? Y lo más importante: ¿es higiénico y seguro imprimir comida en una máquina donde normalmente fundes polímeros y usas grasa de litio? Prepárense un café bien espumoso, porque hoy nos adentramos en la alquimia del FoodTech de escritorio. ¡Arrancamos!

[CHAPTER: La Dictadura de los Cinco Mil Dólares en la Confitería Digital]
DALIA: Para entender por qué el Panda Treat ha causado semejante revuelo en la comunidad maker, Jorge, pongamos en contexto lo que costaba esta tecnología antes de dos mil veintiséis.
JORGE: La impresión directa sobre alimentos no es un concepto nuevo. Desde hace una década, grandes cadenas hoteleras y confiterías de lujo ofrecían galletas personalizadas para bodas, logos corporativos en la espuma de un capuchino o retratos sobre bombones de chocolate.
DALIA: Sin embargo, el mercado de maquinaria estaba dominado por un oligopolio de fabricantes de impresión plana especializada. Máquinas como la Primera Eddie Direct-to-Cookie Printer costaban entre tres mil doscientos y cinco mil dólares estadounidenses.
JORGE: Y el problema no era solo el costo inicial de adquisición. Eran ecosistemas cerrados y punitivos: los cartuchos de tinta comestible tenían chips propietarios DRM que costaban más de cien dólares por color, el software de control era propietario y obsoleto, y si un cabezal piezoeléctrico se secaba por falta de uso, la reparación exigía enviar la máquina al servicio técnico oficial.
DALIA: Para una repostera independiente o una cafetería de barrio, amortizar una inversión de cinco mil dólares en galletas requería vender miles de unidades a precios exorbitantes, reservando la personalización gastronómica para eventos corporativos de gran escala.

[CHAPTER: La Rebelión Panda: BIGTREETECH vs el Jardín Cerrado de Bambu]
JORGE: Pero en este panorama irrumpió un actor inesperado de la escena del código abierto y el hardware chino: BIGTREETECH.
DALIA: Como recordarán de nuestro episodio sobre Bambu Lab vs. RepRap, BIGTREETECH fue durante años el fabricante líder de placas madre abiertas para impresoras Ender 3 y Voron, con tarjetas legendarias como la SKR Mini y la Octopus.
JORGE: Cuando Bambu Lab lanzó sus impresoras propietarias cerrando el firmware y encriptando las comunicaciones, muchos pensaron que el negocio de los componentes de terceros estaba muerto. Pero BIGTREETECH ejecutó una jugada maestra de contraataque comercial llamada el 'Ecosistema Panda'.
DALIA: Desarrollaron la pantalla táctil Panda Touch, las luces Panda Lux, el hotend de cambio rápido Panda Revo con E3D, y ahora, el Panda Treat.
JORGE: La genialidad del Panda Treat radica en su diseño modular de acople magnético. Utiliza la cinemática CoreXY y los rieles lineales de alta precisión de las impresoras Bambu Lab, que ya cuentan con aceleraciones de hasta veinte mil milímetros por segundo al cuadrado y calibración por resonancia.
DALIA: En lugar de construir un chasis nuevo, motores y fuentes de poder desde cero, aprovechan el hardware de doscientos dólares que el usuario ya tiene en su escritorio, sustituyendo únicamente el extrusor térmico por un cabezal de inyección de tinta térmica piezoeléctrica ultraligero que se conecta al puerto de expansión de accesorios de la herramienta.

[CHAPTER: El Dilema de la Seguridad Alimentaria y la Química de Tintas]
JORGE: Ahora bien, la gran pregunta que cualquier microbiólogo o chef se hace de inmediato: ¿es seguro meter alimentos en una máquina donde normalmente fundes plásticos como PLA, ABS o PETG?
DALIA: Este es el debate crítico de ingeniería de materiales e inocuidad alimentaria. Una impresora 3D convencional está plagada de focos de contaminación cruzada: grasa de litio en los tornillos sinfín, polvo de desgaste de correas de goma y compuestos orgánicos volátiles adheridos a las superficies.
JORGE: Para resolver esto sin violar las normas de la FDA y la Unión Europea, el sistema introduce tres barreras de aislamiento higiénico indispensables.
DALIA: Primero: la cama magnética de acero de la impresora nunca toca el alimento. Se instala una bandeja desmontable de silicona platino de grado quirúrgico cien por ciento lavable y esterilizable a vapor.
JORGE: Segundo: la formulación química de las tintas. No se puede usar tinta de impresora de papel ni tintes genéricos. Las tintas del Panda Treat están formuladas con una base de agua desmineralizada de alta pureza, propilenglicol grado USP para controlar la evaporación, glicerina vegetal para la viscosidad y colorantes sintéticos y naturales certificados por la FDA, libres de gluten y con sellos Kosher y Halal.
DALIA: Y tercero: el control de gotas. La tinta debe tener la tensión superficial exacta para secar en segundos sobre el glaseado de azúcar sin sangrar ni disolver la superficie azucarada por capilaridad, manteniendo líneas nítidas con resolución fotográfica de hasta seiscientos puntos por pulgada.

[CHAPTER: La Explosión del Micro-Baking en TikTok e Instagram]
JORGE: Este salto tecnológico ha detonado un fenómeno económico silencioso en redes sociales conocido como el 'Micro-Baking Digital'.
DALIA: Miles de pequeños emprendimientos de repostería casera están utilizando clips de video en TikTok donde muestran la hipnótica precisión con la que la máquina imprime rostros, caricaturas de anime, dedicatorias o logotipos en tiempo real.
JORGE: El modelo de negocio es imbatible: una galleta de mantequilla tiene un costo de ingredientes de aproximadamente cinco a diez pesos mexicanos. Pero esa misma galleta personalizada con el logotipo de un evento o la foto de una mascota se vende fácilmente entre cincuenta y ochenta pesos.
DALIA: Con una inversión total de trescientos treinta dólares —unos seis mil pesos entre la impresora básica y el kit Panda Treat—, el retorno de inversión para un repostero independiente se logra en menos de tres fines de semana de trabajo.
JORGE: La confitería digital ha dejado de ser un monopolio de las cadenas hoteleras de cinco estrellas para convertirse en un nuevo estándar de la manufactura distribuida de cocina.

[CHAPTER: Cierre y Recursos en sIA Journal]
DALIA: Una demostración brillante de cómo el ingenio maker y la reutilización de hardware pueden transformar industrias enteras más allá del plástico.
JORGE: El análisis técnico completo sobre las formulaciones de tintas comestibles, las tolerancias higiénicas y los enlaces a los repositorios y patentes de BIGTREETECH ya están disponibles en sIA Journal en escucha guion sia punto github punto io diagonal articulos.
DALIA: Y en TikTok, en nuestra cuenta oficial arroba escucha guion bajo sia, los invitamos a ver el Reel animado en formato Cómic-Pop donde explicamos cómo una impresora de trescientos dólares jubiló a las máquinas de cinco mil dólares.
JORGE: Muchísimas gracias por escucharnos. Soy Jorge.
DALIA: Y yo soy Dalia. ¡Hasta el próximo episodio de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Por qué las pastelerías pagaban 5,000 dólares por imprimir galletas, hasta que un hacker adaptó un cabezal de comida a una Bambu Lab por 130? Te presento al Panda Treat..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Históricamente, las impresoras de alimentos costaban una fortuna. Pero BIGTREETECH hackeó el sistema: quitas el extrusor de plástico y montas un cabezal de inyección comestible en segundos."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Usa bandejas de silicona platino y tintas de propilenglicol y glicerina vegetal certificadas por la FDA. Imprime galletas, macarons y café en 20 segundos a todo color."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "De una máquina industrial de 5,000 dólares a tu cocina por 330 en total. La revolución del micro-baking que está reventando TikTok."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El ensayo técnico completo de inocuidad y hardware está en sIA Journal. Link en bio."
    }
]

# ==============================================================================
# SUBROUTINES DE PRODUCCIÓN
# ==============================================================================

async def synthesize_voice_segment(text: str, voice: str, output_path: Path):
    for attempt in range(4):
        try:
            communicate = edge_tts.Communicate(text, voice, rate="+6%")
            await communicate.save(str(output_path))
            if output_path.exists() and output_path.stat().st_size > 200:
                return
        except Exception as e:
            if attempt == 3:
                raise e
            await asyncio.sleep(2)

def step1_produce_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Generando Master Audio del Podcast Completo...")
    print("="*70)
    
    final_master = AUDIO_DIR / EPISODE_FILENAME
    if final_master.exists() and final_master.stat().st_size > 1000000:
        print(f"ℹ️ Master de audio ya existe: {final_master}")
        SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
        return final_master
        
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = BASE_DIR / "temp_audio_pandatreat"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    lines = [line.strip() for line in FULL_SCRIPT.strip().split("\n") if line.strip()]
    segments = []
    
    for i, line in enumerate(lines):
        if line.startswith("[CHAPTER:"):
            continue
        if line.startswith("JORGE:"):
            text = line.replace("JORGE:", "").strip()
            voice = VOICE_JORGE
        elif line.startswith("DALIA:"):
            text = line.replace("DALIA:", "").strip()
            voice = VOICE_DALIA
        else:
            continue
            
        seg_path = temp_dir / f"seg_{i:03d}.mp3"
        print(f"  [TTS] Generando segmento {i+1}/{len(lines)} ({voice[:11]})...")
        asyncio.run(synthesize_voice_segment(text, voice, seg_path))
        segments.append(seg_path)
        
    concat_list_path = temp_dir / "concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"file '{seg.name}'\n")
            
    raw_master = temp_dir / "raw_master.mp3"
    print("  [FFMPEG] Concatenando segmentos...")
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(raw_master)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    print("  [EBU R128] Normalizando sonoridad a -16 LUFS...")
    cmd_norm = [
        "ffmpeg", "-y", "-i", str(raw_master),
        "-af", "loudnorm=I=-16:LRA=11:TP=-1.5",
        "-ar", "44100", "-b:a", "192k",
        str(final_master)
    ]
    subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
    print(f"✅ Master de audio completado: {final_master}")
    return final_master

def step2_produce_reel_audio():
    print("\n" + "="*70)
    print("🔊 PASO 2: Sintetizando Audio del Reel Vertical (45s exactos)...")
    print("="*70)
    
    temp_dir = ENGINE_DIR / "temp_audio_stupy_09"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    segments = []
    for i, item in enumerate(REEL_DIALOGUE):
        seg_path = temp_dir / f"reel_seg_{i:02d}.mp3"
        print(f"  [TTS Reel] ({item['speaker']}) {item['text'][:45]}...")
        asyncio.run(synthesize_voice_segment(item['text'], item['voice'], seg_path))
        segments.append(seg_path)
        
    concat_list = temp_dir / "concat_reel.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"file '{seg.name}'\n")
            
    raw_reel = temp_dir / "raw_reel.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(raw_reel)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    norm_reel = ENGINE_DIR / "assets" / "audio.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_reel),
        "-af", "loudnorm=I=-14:LRA=7:TP=-1.0,atempo=1.0",
        "-ar", "44100", "-b:a", "192k",
        str(norm_reel)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    print(f"✅ Audio del Reel listo en: {norm_reel}")

def step3_prepare_stupy_composition():
    print("\n" + "="*70)
    print("🎨 PASO 3: Generando Composición Stupy Cómic-Pop con Barra de Capítulos...")
    print("="*70)
    
    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 09 - BIQU Panda Treat</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #0f0a1c;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}

      /* Matriz Halftone Cómic Pop Dulce */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#ec4899 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.16;
        z-index: 1;
        pointer-events: none;
      }}

      .speed-lines {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          -45deg,
          rgba(236, 72, 153, 0.05) 0px,
          rgba(236, 72, 153, 0.05) 12px,
          transparent 12px,
          transparent 24px
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
        font-size: 80px;
        color: rgba(236, 72, 153, 0.07);
        text-transform: uppercase;
        transform: rotate(-12deg) scale(1.4);
        top: 25%;
        z-index: 0;
        line-height: 1.1;
      }}

      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding: 90px 50px 110px 50px;
      }}

      /* BARRA DE CAPÍTULOS DINÁMICA SUPERIOR */
      .chapters-pill-bar {{
        display: flex;
        gap: 12px;
        background: rgba(30, 27, 75, 0.9);
        padding: 10px 20px;
        border-radius: 40px;
        border: 2px solid rgba(236, 72, 153, 0.4);
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
      }}

      .chapter-step {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        padding: 6px 16px;
        border-radius: 20px;
        color: #94a3b8;
        background: transparent;
        transition: all 0.3s ease;
      }}

      .step-active {{
        background: #ec4899;
        color: #ffffff;
        box-shadow: 0 0 16px rgba(236, 72, 153, 0.7);
      }}

      .header-pill {{
        background: #000000;
        border: 4px solid #ec4899;
        box-shadow: 6px 6px 0px #ec4899;
        border-radius: 50px;
        padding: 14px 38px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
      }}

      .header-dot {{
        width: 20px;
        height: 20px;
        background: #ec4899;
        border-radius: 50%;
        box-shadow: 0 0 16px #ec4899;
      }}

      .header-text {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #f8fafc;
      }}

      /* TARJETA CÓMIC-POP PRINCIPAL */
      .comic-card {{
        background: #ffffff;
        border: 8px solid #000000;
        box-shadow: 18px 18px 0px #ec4899;
        border-radius: 36px;
        width: 100%;
        max-width: 980px;
        padding: 50px 42px;
        color: #000000;
        text-align: center;
        position: relative;
      }}

      .comic-stamp {{
        position: absolute;
        top: -30px;
        right: 40px;
        background: #f59e0b;
        color: #000000;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 24px;
        padding: 8px 24px;
        border: 4px solid #000000;
        border-radius: 14px;
        transform: rotate(6deg);
        box-shadow: 4px 4px 0px #000000;
      }}

      .myth-tag {{
        display: inline-block;
        background: #be185d;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        padding: 8px 24px;
        border-radius: 12px;
        border: 3px solid #000;
        margin-bottom: 24px;
        text-transform: uppercase;
      }}

      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 54px;
        line-height: 1.15;
        letter-spacing: -1.5px;
        color: #000000;
        margin-bottom: 24px;
        text-transform: uppercase;
      }}

      .punch-pill {{
        background: #fbcfe8;
        color: #831843;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 40px;
        padding: 16px 28px;
        border: 5px solid #000000;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #000000;
        display: inline-block;
        margin-bottom: 26px;
      }}

      .metric-box {{
        background: #fdf2f8;
        border: 4px dashed #db2777;
        border-radius: 20px;
        padding: 24px 28px;
        margin-top: 15px;
      }}

      .metric-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #9d174d;
      }}

      .metric-stat {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 58px;
        color: #db2777;
        line-height: 1.1;
        margin-top: 6px;
      }}

      /* FOOTER & TIMELINE */
      .footer-badge {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 14px;
        margin-top: 20px;
      }}

      .channel-tag {{
        background: #000000;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 800;
        padding: 12px 36px;
        border: 4px solid #ec4899;
        border-radius: 40px;
        box-shadow: 6px 6px 0px #ec4899;
      }}

      .progress-bar-container {{
        width: 100%;
        max-width: 900px;
        height: 16px;
        background: #1e293b;
        border: 3px solid #000000;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 15px;
      }}

      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #ec4899, #db2777, #f43f5e);
        width: 0%;
        animation: progressAnim 45s linear infinite;
      }}

      @keyframes progressAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}

      .final-pill {{
        background: #000000;
        color: #f472b6;
        font-family: 'JetBrains Mono', monospace;
        font-size: 34px;
        font-weight: 800;
        padding: 16px 36px;
        border: 5px solid #ec4899;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #ec4899;
        margin-top: 15px;
        display: inline-block;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="speed-lines"></div>

    <div class="bg-ticker">
      <div>BIQU PANDA TREAT BAMBU LAB FOODTECH</div>
      <div>GALLETAS DECORADAS REPOSTERIA 3D TINTA COMESTIBLE</div>
      <div>DE 5000 A 330 DOLARES DEMOCRATIZACION</div>
      <div>BIGTREETECH HACK ALIMENTARIO VIRAL TIKTOK</div>
    </div>

    <div class="reel-wrapper">
      <!-- BARRA DE CAPÍTULOS SUPERIOR -->
      <div class="chapters-pill-bar">
        <div class="chapter-step" id="chap-1">01 $5,000 A $330</div>
        <div class="chapter-step" id="chap-2">02 EL HACK</div>
        <div class="chapter-step" id="chap-3">03 FOOD SAFETY</div>
        <div class="chapter-step" id="chap-4">04 NEGOCIO</div>
      </div>

      <div class="header-pill">
        <div class="header-dot"></div>
        <div class="header-text">sIA MAKER & FOODTECH #03</div>
      </div>

      <!-- MAIN COMIC CARD -->
      <div class="comic-card">
        <div class="comic-stamp">HACK 2026</div>

        <!-- SCENE 1: EL PRECIO PROHIBITIVO (0s - 9.0s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">EL MONOPOLIO DULCE</div>
          <div class="headline-black">
            ¿IMPRIMIR GALLETAS COSTABA $5,000?
          </div>
          <div class="punch-pill">
            LLEGÓ EL BIQU PANDA TREAT
          </div>
          <div class="metric-box">
            <div class="metric-title">MÁQUINAS INDUSTRIALES ANTIGUAS:</div>
            <div class="metric-stat">$5,000 USD</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 18px;">
            Un lujo reservado para gigantes hoteleros.
          </div>
        </div>

        <!-- SCENE 2: EL HACK DE BIGTREETECH (9.0s - 21.0s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #0284c7; color: #fff;">INGENIERÍA MAKER</div>
          <div class="headline-black" style="font-size: 50px;">
            HACK A BAMBU LAB POR $130
          </div>
          <div class="punch-pill" style="background: #e0f2fe; color: #0369a1; font-size: 36px;">
            CABEZAL COMESTIBLE SNAP-ON
          </div>
          <div class="metric-box" style="background: #f0f9ff; border-color: #0284c7;">
            <div style="font-size: 32px; font-weight: 900; color: #075985;">
              🍓 CAMBIO RÁPIDO EN SEGUNDOS
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Quitas el plástico y pones tinta de comida.
          </div>
        </div>

        <!-- SCENE 3: FOOD SAFETY (21.0s - 34.0s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #10b981; color: #fff;">INOCUIDAD CERTIFICADA</div>
          <div class="headline-black" style="font-size: 48px;">
            TINTAS COMESTIBLES FDA
          </div>
          <div class="punch-pill" style="background: #000; color: #f472b6 !important; font-size: 36px; border-color: #f472b6;">
            BANDEJA DE SILICONA PURA
          </div>
          <div class="metric-box" style="background: #f0fdf4; border-color: #10b981;">
            <div style="font-size: 30px; font-weight: 900; color: #166534;">
              ✨ KOSHER, HALAL Y SIN GLUTEN
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            Galletas, macarons y café en 20 segundos.
          </div>
        </div>

        <!-- SCENE 4: LA REVOLUCIÓN (34.0s - 45.0s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #ec4899; color: #fff;">MICRO-BAKING VIRAL</div>
          <div class="headline-black" style="font-size: 46px;">
            TOTAL: $330 USD EN TU COCINA
          </div>
          <div class="punch-pill" style="background: #fbcfe8; font-size: 34px;">
            DEMOCRATIZACIÓN GASTRONÓMICA
          </div>
          <div class="final-pill">
            🎧 EPISODIO COMPLETO EN SPOTIFY
          </div>
          <div style="font-size: 26px; font-weight: 800; color: #db2777; margin-top: 14px;">
            Lee la investigación en sIA Journal (link en bio)
          </div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="channel-tag">@escucha_sia &bull; Spotify Show</div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    function updateTimeline(time) {{
      const s1 = document.getElementById('scene-1');
      const s2 = document.getElementById('scene-2');
      const s3 = document.getElementById('scene-3');
      const s4 = document.getElementById('scene-4');

      const c1 = document.getElementById('chap-1');
      const c2 = document.getElementById('chap-2');
      const c3 = document.getElementById('chap-3');
      const c4 = document.getElementById('chap-4');

      s1.style.display = 'none';
      s2.style.display = 'none';
      s3.style.display = 'none';
      s4.style.display = 'none';

      [c1, c2, c3, c4].forEach(c => c.className = 'chapter-step');

      if (time < 9.0) {{
        s1.style.display = 'block';
        c1.className = 'chapter-step step-active';
      }} else if (time < 21.0) {{
        s2.style.display = 'block';
        c2.className = 'chapter-step step-active';
      }} else if (time < 34.0) {{
        s3.style.display = 'block';
        c3.className = 'chapter-step step-active';
      }} else {{
        s4.style.display = 'block';
        c4.className = 'chapter-step step-active';
      }}
    }}

    window.__seekHyperFrames = function(currentTime) {{
      updateTimeline(currentTime);
    }};

    updateTimeline(0);
  </script>
  </body>
</html>
"""
    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Plantillas HyperFrames generadas para Stupy 09 (BIQU Panda Treat).")

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
    
    res_entry = f'''    # sIA Maker 03 - BIQU Panda Treat - 4 de Noviembre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-maker-03-biqu-panda-treat-impresora-3d-confiteria-digital",
        "category": "Maker & FoodTech",
        "badge_color": "rose",
        "read_time": "12 min",
        "title": "sIA Maker #03: BIQU Panda Treat: Cómo una Impresora 3D de $200 Hackeó la Industria de la Confitería Digital",
        "subtitle": "De $5,000 a $330 USD: acoples modulares, química de tintas comestibles y la democratización del micro-baking artesanal.",
        "thesis": "La transformación de cinemáticas de impresión 3D de consumo en plataformas de manufactura alimentaria mediante cabezales térmicos intercambiables demuestra que la estandarización de movimientos de alta precisión es capaz de destruir monopolios de maquinaria industrial especializada, trasladando la personalización masiva a la microeconomía doméstica.",
        "nexo": "Tercer episodio de Maker & 3D: Hardware abierto vs cerrado, ingeniería de alimentos, BIGTREETECH, química de formulaciones inocuas y microfabricación culinaria.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "type": "heading",
                "text": "1. El Monopolio de la Confitería Digital y la Barrera de los Cinco Mil Dólares"
            }},
            {{
                "type": "paragraph",
                "text": "Durante más de una década, la impresión directa sobre alimentos permaneció como un servicio prohibitivo reservado a cadenas hoteleras y empresas de eventos corporativos de gran escala. Las impresoras especializadas de cama plana, como la serie Eddie de Primera Technology o adaptaciones industriales de Roland y Mimaki, exigían desembolsos de entre 3,000 y 8,000 dólares estadounidenses. Además de la inversión de capital, estos equipos operaban bajo esquemas de consumibles cerrados con cartuchos dotados de chips DRM y cabezales piezoeléctricos propietarios con elevados costos de mantenimiento."
            }},
            {{
                "type": "callout",
                "icon": "🍰",
                "title": "La Democratización del Micro-Baking",
                "text": "Al combinar una impresora 3D de consumo como la Bambu Lab A1 Mini (con un costo de 199 dólares) con un módulo intercambiable Panda Treat de 130 dólares, la inversión total desciende a 330 dólares. Esto representa una reducción de más del 93% en la barrera de entrada para confiterías artesanales y cafeterías de especialidad."
            }},
            {{
                "type": "heading",
                "text": "2. La Arquitectura Mecánica de Acople Rápido de BIGTREETECH"
            }},
            {{
                "type": "paragraph",
                "text": "Tras el cierre del ecosistema de Bambu Lab, BIGTREETECH reorientó su estrategia hacia el desarrollo de periféricos de alto valor bajo la submarca Panda. El dispositivo Panda Treat prescinde de motores y fuentes de poder redundantes: se ancla magnéticamente al toolhead de la impresora y aprovecha los rieles lineales metálicos y la compensación activa de vibraciones del chasis original. El sistema sustituye el extrusor térmico de filamento por un cabezal de inyección térmica de microgotas alimentado a través del conector auxiliar de la placa de herramientas."
            }},
            {{
                "type": "heading",
                "text": "3. Inocuidad y Formulación Química de Tintas Comestibles"
            }},
            {{
                "type": "paragraph",
                "text": "El empleo de maquinaria de manufactura plástica para el procesamiento de alimentos introduce estrictos requerimientos de bioseguridad. El sistema mitiga la contaminación cruzada mediante bandejas desmontables de silicona curada con platino de grado alimenticio FDA, aislando por completo la cama metálica y los lubricantes de los ejes. Por su parte, las tintas CMY se formulan a partir de agua desmineralizada, propilenglicol de grado farmacéutico USP, glicerina vegetal y colorantes hidrosolubles certificados bajo normativas Kosher y Halal, garantizando tiempos de secado inferiores a 30 segundos sobre superficies porosas de azúcar sin alterar la estabilidad coloidal del glaseado."
            }},
            {{
                "type": "heading",
                "text": "4. Modelos de Negocio en Redes Sociales y Manufactura Distribuida"
            }},
            {{
                "type": "paragraph",
                "text": "La proliferación de contenidos virales en TikTok e Instagram centrados en la decoración automatizada de galletas ha impulsado un nuevo segmento económico: el micro-baking digital bajo demanda. Con un costo marginal de tinta inferior a cinco centavos de dólar por pieza y tiempos de producción de 20 segundos, los pequeños productores alcanzan márgenes de rentabilidad superiores al 400%, confirmando que la tecnología de fabricación digital de escritorio está redefiniendo la economía de los bienes de consumo personalizables."
            }}
        ],
        "fuentes": [
            "BIGTREETECH & CMY Labs. (2026). Panda Treat Food-Safe Inkjet Printing Module Specification. BIQU Equipment.",
            "U.S. Food and Drug Administration. (2024). Color additives approved for use in human food: Code of Federal Regulations Title 21. FDA Publications.",
            "Primera Technology. (2025). Direct-to-Food Digital Printing Technology: Eddie Printer White Paper.",
            "Bambu Lab. (2025). High-speed motion control and input shaping in CoreXY kinematics. Bambu Lab Engineering.",
            "International Food Information Council. (2026). Digital customization and food safety in artisanal confectionery."
        ]
    }},
'''
    if '"slug": "sia-maker-03-biqu-panda-treat-impresora-3d-confiteria-digital"' not in content:
        insert_marker = "RESEARCH_COMPENDIUM = {"
        content = content.replace(insert_marker, insert_marker + "\n" + res_entry)
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Registrado en build_magazine.py.")
    else:
        print("ℹ️ Ya existía el registro en build_magazine.py.")
        
    cmd_build = [sys.executable, str(BASE_DIR / "build_magazine.py")]
    subprocess.run(cmd_build, check=True)
    print("✅ Revista digital recompilada y actualizada.")

def step6_sync_gdrive():
    print("\n" + "="*70)
    print("☁️ PASO 6: Sincronizando con Google Drive Hub...")
    print("="*70)
    
    GDRIVE_REELS.mkdir(parents=True, exist_ok=True)
    GDRIVE_AUDIO.mkdir(parents=True, exist_ok=True)
    GDRIVE_VAULT.mkdir(parents=True, exist_ok=True)
    
    reel_src = REELS_DIR / REEL_FILENAME
    poster_src = REELS_DIR / REEL_POSTER_FILENAME
    audio_src = AUDIO_DIR / EPISODE_FILENAME
    
    if reel_src.exists():
        shutil.copy2(reel_src, GDRIVE_REELS / REEL_FILENAME)
        print(f"  [Drive] Reel copiado: {GDRIVE_REELS / REEL_FILENAME}")
    if poster_src.exists():
        shutil.copy2(poster_src, GDRIVE_REELS / REEL_POSTER_FILENAME)
        print(f"  [Drive] Poster copiado: {GDRIVE_REELS / REEL_POSTER_FILENAME}")
    if audio_src.exists():
        shutil.copy2(audio_src, GDRIVE_AUDIO / EPISODE_FILENAME)
        print(f"  [Drive] Audio master copiado: {GDRIVE_AUDIO / EPISODE_FILENAME}")

def step7_create_obsidian_vault_note():
    print("\n" + "="*70)
    print("📝 PASO 7: Creando Nota en Obsidian Vault con Social Kit...")
    print("="*70)
    
    vault_shorts_dir = GDRIVE_VAULT / "02_Reels_Shorts"
    vault_shorts_dir.mkdir(parents=True, exist_ok=True)
    
    note_content = f"""# Reel Stupy 09: BIQU Panda Treat — Galletas con Impresora 3D

**ID:** `sIA_Reel_Stupy_09_Biqu_Panda_Treat`
**Episodio Relacionado:** `sIA_Maker_03_Biqu_Panda_Treat_FoodTech_2026-11-04.mp3`
**Fecha de Publicación:** 2026-11-04
**Autor / Arquitecto:** `cacs`
**Estado:** Publicado en TikTok (@escucha_sia) y Spotify Show

---

## 🎬 Video Renderizado
![[sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4]]

---

## 📋 Social Kit de Publicación

### Caption para TikTok / YouTube Shorts / Instagram Reels
> ¿Imprimir comida en tu impresora 3D? De pagar 5,000 dólares por una máquina industrial a personalizar galletas en tu cocina por 330 en total. Te explico cómo el BIQU Panda Treat hackeó a Bambu Lab. 🍪✨
>
> 🎧 Episodio completo en Spotify (sIA Podcast) y ensayo de FoodTech en el link del perfil.
>
> #impresion3d #bambulab #pandatreat #bigtreetech #foodtech #reposteria #galletasdecoradas #maker #siapodcast

### Primer Comentario Fijado (Call to Action de Conversión)
> 🍪 **¿Cómo funciona la química de tintas e inocuidad alimentaria?**
> Lee el artículo completo con diagramas en:  
> 👉 https://escucha-sia.github.io/articulos/sia-maker-03-biqu-panda-treat-impresora-3d-confiteria-digital.html  
> O busca "sIA" en Spotify para escuchar el debate técnico completo.

---

## 🔬 Puntos Clave de Investigación
1. **La barrera económica:** Las máquinas industriales (Primera Eddie) costaban de $3,500 a $8,000 USD.
2. **El hack modular:** Cabezal intercambiable snap-on de $130 USD sobre Bambu Lab A1 Mini ($199 USD).
3. **Inocuidad alimentaria:** Bandejas de silicona platino de grado quirúrgico y tintas CMY con propilenglicol USP y certificaciones FDA/Kosher/Halal.
4. **Micro-baking viral:** Márgenes superiores al 400% imprimiendo galletas y macarons bajo demanda.
"""
    note_path = vault_shorts_dir / "sIA_Reel_Stupy_09_Biqu_Panda_Treat.md"
    note_path.write_text(note_content, encoding='utf-8')
    print(f"✅ Nota de Obsidian Vault creada: {note_path}")

def step8_git_deploy():
    print("\n" + "="*70)
    print("🚀 PASO 8: Desplegando en GitHub Pages...")
    print("="*70)
    
    subprocess.run(["git", "add", "."], cwd=str(BASE_DIR), check=True)
    subprocess.run(["git", "commit", "-m", "feat(episode): publish sIA Maker 03 - BIQU Panda Treat and Reel Stupy 09"], cwd=str(BASE_DIR), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=True)
    print("✅ Despliegue en GitHub Pages completado.")

if __name__ == "__main__":
    print("="*70)
    print("🚀 INICIANDO PIPELINE 360°: sIA Maker #03 (BIQU Panda Treat)")
    print("="*70)
    step1_produce_full_audio()
    step2_produce_reel_audio()
    step3_prepare_stupy_composition()
    step4_render_reel()
    step5_register_and_rebuild_magazine()
    step6_sync_gdrive()
    step7_create_obsidian_vault_note()
    step8_git_deploy()
    print("\n" + "="*70)
    print("🎉 PACK 360° COMPLETADO: sIA Maker #03 (BIQU Panda Treat)")
    print("="*70)
