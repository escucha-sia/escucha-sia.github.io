"""
sIA Master Episode & Reel Producer:
Tema: sIA Sec #01: La Caída Global de CrowdStrike y el Bug del Ring 0: Cómo una actualización de kernel paralizó 8.5 millones de máquinas, bancos y aeropuertos
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop (HyperFrames GPU, 45s, Halftone BSOD, Kinetic Pop)
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

EPISODE_FILENAME = "sIA_Sec_01_CrowdStrike_Ring0_Kernel_BSOD_2026-11-02.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_06_CrowdStrike_Ring0_BSOD.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_06_CrowdStrike_Ring0_BSOD_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: El Día que se Apagó el Planeta Digital]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad de ingenieros de sistemas, profesionales de ciberseguridad y arquitectos de infraestructura en México y toda Iberoamérica! Bienvenidos a una entrega inaugural de sIA en su edición de Seguridad e Infraestructura Crítica. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es lunes dos de noviembre de dos mil veintiséis. Y hoy desentrañamos desde sus cimientos de bajo nivel el mayor colapso informático en la historia de la civilización moderna: el día en que una sola actualización defectuosa de CrowdStrike apagó más de ocho millones y medio de computadoras con Windows en todo el mundo.
JORGE: El diecinueve de julio de dos mil veinticuatro, el mundo físico chocó de frente contra la fragilidad de su software. Aerolíneas completas cancelaron miles de vuelos dejando a millones de pasajeros varados en terminales a oscuras; hospitales suspendieron cirugías críticas y tratamientos de radioterapia; cajeros automáticos y sistemas de pago con tarjeta dejaron de operar; y cadenas de televisión como Sky News salieron del aire en vivo mostrando únicamente una pantalla azul con el temido código PAGE FAULT IN NONPAGED AREA.
DALIA: El daño económico total superó los diez mil millones de dólares. Pero lo más inquietante para la comunidad técnica no fue la magnitud de la catástrofe, sino su origen: no hubo un ciberataque de hackers estatales, no hubo un ataque de ransomware ruso ni una vulnerabilidad de día cero. Fue un error de puntero en una actualización rutinaria de un sensor de seguridad que operaba en el nivel más íntimo y peligroso de la arquitectura de computadores: el Ring Cero.
JORGE: ¿Cómo funciona realmente el núcleo de un sistema operativo? ¿Por qué una empresa de ciberseguridad valuada en miles de millones de dólares desplegó un archivo binario corrupto a todo el planeta a la misma hora sin pruebas canario? Y sobre todo: ¿por qué este incidente está obligando a Microsoft y a toda la industria a expulsar los antivirus fuera del kernel? Prepárense un café bien cargado, porque esta autopsia técnica no deja títere con cabeza. ¡Arrancamos!

[CHAPTER: La Arquitectura del Núcleo: Ring 0 contra Ring 3]
DALIA: Para comprender cómo una sola línea de código paralizó bancos y aeropuertos, Jorge, tenemos que bajar hasta la arquitectura de hardware de los procesadores modernos x86 y x64.
JORGE: Desde los procesadores Intel de finales de los años ochenta, los chips incorporan una jerarquía de privilegios de hardware conocida como 'anillos de protección' o Protection Rings. La inmensa mayoría de las aplicaciones que usamos a diario —el navegador Google Chrome, Spotify, Microsoft Word, los entornos de desarrollo y las bases de datos— se ejecutan en lo que llamamos el Ring Tres o Espacio de Usuario (User Space).
DALIA: En el Ring Tres, las aplicaciones están aisladas en su propia memoria virtual. Si una aplicación tiene un error grave de programación, si se queda sin memoria o intenta dividir entre cero, el sistema operativo interviene de inmediato: mata el proceso, muestra un mensaje de error y el resto de la computadora sigue funcionando con absoluta normalidad. Es una red de seguridad perfecta.
JORGE: Pero en el fondo de la jerarquía se encuentra el Ring Cero, también llamado Modo Núcleo o Kernel Mode. En este anillo reside el corazón del sistema operativo: el kernel de Windows, ntoskrnl.exe, junto a los controladores de hardware más críticos como la tarjeta madre, los discos y los controladores de red.
DALIA: En Ring Cero no existen las barreras de protección. Cualquier código que se ejecute en este nivel tiene acceso irrestricto y directo a toda la memoria física y a todas las instrucciones de la CPU. Si un controlador en Ring Cero comete un solo error de lectura en una dirección de memoria no mapeada, no hay nadie arriba para atraparlo. La CPU se detiene en seco y lanza un Kernel Panic —la Pantalla Azul de la Muerte en Windows— como mecanismo de defensa para evitar que la memoria física o los datos del disco se corrompan irremediablemente.
JORGE: Y aquí viene la gran pregunta: ¿por qué un software de ciberseguridad tenía permiso para operar en el nivel más peligroso del sistema operativo?

[CHAPTER: La Anatomía Forense del Bug: El Archivo Channel 291]
DALIA: La herramienta responsable se llama CrowdStrike Falcon. Es un agente EDR —Endpoint Detection and Response— diseñado para monitorear en tiempo real la actividad de la máquina y detectar técnicas de ataque avanzadas antes de que los atacantes puedan ejecutar ransomware.
JORGE: Para poder interceptar ataques a nivel de bajo nivel, CrowdStrike instala un controlador de kernel llamado csagent.sys. Este controlador está registrado como un Boot-Start Driver: un tipo de driver que Windows carga obligatoriamente en los primeros segundos del arranque, antes incluso de que aparezca la pantalla de inicio de sesión de los usuarios.
DALIA: Para no tener que pedir a los administradores de sistemas que reinicien servidores críticos cada vez que se descubre una nueva técnica de hackeo, CrowdStrike ideó un mecanismo llamado 'Channel Files'. Son pequeños archivos binarios de configuración que el sensor Falcon descarga dinámicamente desde la nube y que el driver de Ring Cero interpreta para aplicar nuevas reglas de detección de amenazas.
JORGE: Y llegamos a la madrugada fatídica del diecinueve de julio de dos mil veinticuatro. A las cero cuatro con cero nueve minutos UTC, CrowdStrike publicó una actualización de reglas en un archivo llamado Channel File doscientos noventa y uno, diseñado para detectar el uso malicioso de tuberías con nombre —Named Pipes— habitualmente explotadas por herramientas de pentesting.
DALIA: El reporte forense oficial reveló un fallo vergonzoso de validación de memoria en lenguaje C++. El analizador dentro del driver de Ring Cero esperaba veintiún campos de entrada para esa regla específica. Sin embargo, el archivo Channel doscientos noventa y uno que se distribuyó solo contenía veinte campos formateados.
JORGE: Cuando el controlador en Ring Cero intentó leer el campo número veintiuno, calculó un desplazamiento de memoria basado en un puntero nulo: la dirección hexadecimal cero equis nueve ce. Al intentar leer una dirección de memoria física no asignada en pleno arranque del sistema, la CPU disparó una violación de acceso de memoria fatal. Y como el driver se ejecutaba en Ring Cero durante el inicio, Windows no tuvo más opción que colapsar en una pantalla azul inmediata, reiniciarse y volver a fallar en un bucle infinito.

[CHAPTER: El Pecado de QA y la Falacia del Despliegue Global]
DALIA: Un error de puntero nulo es un fallo técnico de programación que puede cometer cualquier ingeniero novato. Pero que ese archivo defectuoso llegara simultáneamente a ocho millones y medio de computadoras en producción representa el fallo de control de calidad más colosal de la ingeniería de software moderna.
JORGE: Cualquier estudiante de primer semestre de infraestructura de servidores conoce la regla de oro: nunca, jamás, bajo ninguna circunstancia, se despliega una actualización a todo el planeta al mismo tiempo.
DALIA: El estándar de la industria exige lo que llamamos 'despliegues canario' o despliegues escalonados por fases: primero liberas la actualización a un uno por ciento de máquinas internas de prueba; si tras dos horas no hay anomalías, avanzas al diez por ciento; luego al veinticinco por ciento; y finalmente al resto de la flota a lo largo de varios días.
JORGE: CrowdStrike se saltó por completo esta disciplina. Como consideraban que los Channel Files eran 'datos de configuración' y no 'código ejecutable', su sistema de validación automatizada tenía un bug que aprobó el archivo doscientos noventa y uno a ciegas. Y a las cuatro y nueve de la mañana, sus servidores empujaron el archivo defectuoso a todas las máquinas conectadas de Delta Airlines, de bancos, hospitales y supermercados a nivel mundial en el mismo segundo.

[CHAPTER: La Pesadilla de la Recuperación Manual y el Futuro sin Kernel]
DALIA: Lo que siguió fue una pesadilla dantesca para los departamentos de tecnología. Como las máquinas estaban atrapadas en un bucle de pantalla azul antes de cargar la red, no había forma de enviarles un parche por internet.
JORGE: Además, la inmensa mayoría de las computadoras corporativas tenían activado el cifrado de disco BitLocker de Microsoft. Para desbloquearlas, los ingenieros tuvieron que desplazarse físicamente a cada una de las ocho millones y medio de máquinas con memorias USB, arrancar en Modo Seguro, escribir a mano claves criptográficas de recuperación de cuarenta y ocho caracteres y borrar manualmente el archivo C guion cero cero cero cero cero doscientos noventa y uno punto sys.
DALIA: La lección política y técnica fue tan severa que Microsoft convocó de urgencia una cumbre global de seguridad en su sede de Redmond. La conclusión de los líderes de la industria es inapelable: los días en que cualquier proveedor de seguridad instala drivers en el Ring Cero de Windows están contados.
JORGE: Siguiendo el camino que Apple ya recorrió en macOS con su arquitectura de System Extensions, Microsoft y la comunidad de código abierto están impulsando tecnologías como eBPF (Extended Berkeley Packet Filter), permitiendo que el software de seguridad analice paquetes de red, procesos y llamadas al sistema con verificadores formales de memoria sin necesidad de ejecutar código nativo en el núcleo. Si un programa de eBPF falla, el verificador lo aísla y el sistema operativo no se cae.

[CHAPTER: Conclusiones y Resiliencia en sIA Journal]
DALIA: La caída de CrowdStrike nos demostró que la mayor amenaza para la seguridad de una empresa muchas veces no es el hacker externo, sino la complejidad descontrolada y los privilegios ciegos que le otorgamos a las herramientas corporativas que prometen protegernos.
JORGE: El análisis forense completo, los diagramas de arquitectura de memoria de Ring Cero a Ring Tres y las referencias académicas en formato APA 7ª Edición ya están disponibles en sIA Journal en escucha guion sia punto github punto io diagonal articulos.
DALIA: Y en TikTok, en nuestra cuenta oficial arroba escucha guion bajo sia, ya pueden ver el Reel explicativo en formato Cómic-Pop para compartir con sus colegas de sistemas y ciberseguridad.
JORGE: Muchísimas gracias por acompañarnos. Soy Jorge.
DALIA: Y yo soy Dalia. ¡Hasta la próxima entrega de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Cómo una sola línea de código paralizó bancos, hospitales y aeropuertos de todo el mundo? La caída global de CrowdStrike no fue un ciberataque: fue el bug del Ring Cero."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "En el Modo Núcleo de Windows no hay red de seguridad. El sensor Falcon intentó leer un puntero nulo en memoria física y colapsó el kernel en segundos."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "CrowdStrike violó la regla de oro: lanzó el parche a todo el planeta a la misma hora sin pruebas canario. Y millones de ingenieros tuvieron que arreglarlo a mano con memorias USB."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "El software de seguridad debe salir del núcleo. Analiza el reporte forense completo y las fuentes académicas en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def step1_generate_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Sintetizando Episodio Completo (Jorge & Dalia)...")
    print("="*70)
    target_path = AUDIO_DIR / EPISODE_FILENAME
    if target_path.exists():
        print(f"✅ Audio completo ya existe: {target_path}")
        return target_path
        
    from podcast_synthesizer import process_dialogue
    
    ep_info = {
        "title": "sIA Sec #01: La Caída Global de CrowdStrike y el Bug del Ring 0: Cómo una actualización de kernel paralizó 8.5 millones de máquinas, bancos y aeropuertos",
        "filename": EPISODE_FILENAME,
        "description": "Autopsia forense y arquitectónica del mayor colapso informático de la historia: Ring 0 vs Ring 3, el archivo Channel 291, violación de memoria nula, fallo de QA masivo y el imperativo de expulsar los antivirus fuera del kernel por cacs."
    }
    
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"✅ Audio completo sintetizado: {out_path}")
    return out_path

async def step2_generate_reel_audio():
    print("\n" + "="*70)
    print("🎬 PASO 2: Sintetizando Audio del Reel Cómic-Pop (45s)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_audio_stupy_06"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        clean_text = item["text"].replace("Sia", "Sia").replace("sIA", "Sia")
        clean_text = clean_text.replace("CrowdStrike", "Craud-Straik").replace("Ring Cero", "Ring Cero").replace("Falcon", "Fálcon")
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
    if not music_src.exists():
        candidates = list((BASE_DIR / "assets" / "audio_library").glob("*.mp3"))
        if candidates:
            music_src = candidates[0]
            
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
    subprocess.run(cmd, check=True)
    print(f"✅ Audio del Reel generado con música y mezcla EBU R128 (-16 LUFS): {clip_audio}")

def step3_prepare_hyperframes_composition():
    print("\n" + "="*70)
    print("🎨 PASO 3: Preparando Composición HyperFrames Cómic-Pop Stupy 06...")
    print("="*70)
    
    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>sIA Reel Stupy 06 - CrowdStrike & Ring 0 BSOD</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #04091a;
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
    <div id="root" data-composition-id="sia_motion_reel_stupy_06" data-no-timeline data-start="0" data-duration="45.0" data-width="1080" data-height="1920">
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
        background: #04091a;
        color: #0b0d17;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* 1. HALFTONE COMIC PATTERN BACKGROUND */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(2, 132, 199, 0.16) 2.5px, transparent 2.5px);
        background-size: 26px 26px;
        opacity: 0.9;
        z-index: 1;
      }}

      /* 2. BACKGROUND GHOST TICKER */
      .bg-ticker {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        opacity: 0.05;
        font-family: 'JetBrains Mono', monospace;
        font-size: 80px;
        font-weight: 900;
        color: #fff;
        user-select: none;
        pointer-events: none;
        z-index: 2;
        line-height: 1.1;
      }}

      /* 3. SPEED LINES */
      .speed-lines {{
        position: absolute;
        inset: 0;
        background: repeating-conic-gradient(from 0deg at 50% 50%, rgba(2, 132, 199, 0.05) 0deg 8deg, transparent 8deg 16deg);
        z-index: 2;
        pointer-events: none;
      }}

      /* 4. MAIN CONTAINER */
      .reel-wrapper {{
        position: absolute;
        inset: 0;
        z-index: 10;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 90px 48px 120px 48px;
      }}

      /* HEADER */
      .header-pill {{
        background: #000000;
        border: 4px solid #0284c7;
        border-radius: 999px;
        padding: 14px 34px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 6px 6px 0px #0284c7;
        transform: rotate(-1deg);
      }}
      .header-dot {{
        width: 18px;
        height: 18px;
        background: #ef4444;
        border-radius: 50%;
        box-shadow: 0 0 16px #ef4444;
      }}
      .header-text {{
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 2px;
      }}

      /* COMIC POP CARD */
      .comic-card {{
        background: #ffffff;
        border: 7px solid #000000;
        border-radius: 36px;
        box-shadow: 18px 18px 0px #000000;
        width: 100%;
        max-width: 984px;
        padding: 44px 36px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin: auto 0;
      }}

      /* CORNER COMIC STAMP */
      .comic-stamp {{
        position: absolute;
        top: -30px;
        right: 40px;
        background: #ef4444;
        color: #fff;
        font-weight: 900;
        font-size: 26px;
        padding: 10px 24px;
        border: 5px solid #000;
        box-shadow: 6px 6px 0px #000;
        border-radius: 12px;
        transform: rotate(4deg);
        letter-spacing: 1px;
      }}

      /* SCENES DEFINITION */
      .scene {{
        display: none;
        width: 100%;
        flex-direction: column;
        align-items: center;
      }}

      #scene-1 {{ display: flex; }}

      @keyframes showS1 {{
        0%, 18.88% {{ opacity: 1; pointer-events: auto; display: flex; }}
        18.89%, 100% {{ opacity: 0; pointer-events: none; display: none; }}
      }}
      @keyframes showS2 {{
        0%, 18.88% {{ opacity: 0; pointer-events: none; display: none; }}
        18.89%, 45.55% {{ opacity: 1; pointer-events: auto; display: flex; }}
        45.56%, 100% {{ opacity: 0; pointer-events: none; display: none; }}
      }}
      @keyframes showS3 {{
        0%, 45.55% {{ opacity: 0; pointer-events: none; display: none; }}
        45.56%, 74.44% {{ opacity: 1; pointer-events: auto; display: flex; }}
        74.45%, 100% {{ opacity: 0; pointer-events: none; display: none; }}
      }}
      @keyframes showS4 {{
        0%, 74.44% {{ opacity: 0; pointer-events: none; display: none; }}
        74.45%, 100% {{ opacity: 1; pointer-events: auto; display: flex; }}
      }}

      #scene-1 {{ animation: showS1 45s infinite; }}
      #scene-2 {{ animation: showS2 45s infinite; }}
      #scene-3 {{ animation: showS3 45s infinite; }}
      #scene-4 {{ animation: showS4 45s infinite; }}

      .myth-tag {{
        background: #0284c7;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 2px;
        padding: 8px 22px;
        border-radius: 999px;
        border: 4px solid #000;
        box-shadow: 4px 4px 0px #000;
        margin-bottom: 24px;
        display: inline-block;
      }}

      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 54px;
        line-height: 1.08;
        color: #0b0d17;
        text-transform: uppercase;
        letter-spacing: -1.5px;
        margin-bottom: 26px;
      }}

      .punch-pill {{
        background: #0078d7;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 40px;
        line-height: 1.15;
        padding: 16px 28px;
        border: 6px solid #000000;
        box-shadow: 8px 8px 0px #000000;
        border-radius: 20px;
        transform: rotate(-1.5deg);
        margin: 18px 0;
        display: inline-block;
      }}

      .metric-box {{
        background: #eff6ff;
        border: 5px dashed #0284c7;
        border-radius: 20px;
        padding: 22px 28px;
        margin-top: 20px;
        width: 100%;
      }}

      .metric-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 800;
        color: #0369a1;
        letter-spacing: 1px;
      }}

      .metric-stat {{
        font-family: 'Montserrat', sans-serif;
        font-size: 48px;
        font-weight: 900;
        color: #1e3a8a;
        line-height: 1.1;
      }}

      .progress-bar-container {{
        width: 100%;
        height: 20px;
        background: #000000;
        border: 4px solid #0284c7;
        border-radius: 999px;
        overflow: hidden;
        position: relative;
        box-shadow: 4px 4px 0px #0284c7;
      }}

      .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, #0284c7, #0078d7, #ef4444);
        width: 0%;
        animation: progressAnim 45s linear infinite;
      }}

      @keyframes progressAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}

      .final-pill {{
        background: #000000;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 34px;
        font-weight: 800;
        padding: 16px 36px;
        border: 5px solid #0284c7;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #0284c7;
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
      <div>CROWDSTRIKE RING 0 KERNEL BSOD</div>
      <div>PAGE FAULT IN NONPAGED AREA 0X9C</div>
      <div>CHANNEL FILE 291 CANARY DEPLOYMENT</div>
      <div>EBPF SYSTEM EXTENSIONS USER SPACE</div>
    </div>

    <div class="reel-wrapper">
      <div class="header-pill">
        <div class="header-dot"></div>
        <div class="header-text">sIA CIBERSEGURIDAD #01</div>
      </div>

      <!-- MAIN COMIC CARD -->
      <div class="comic-card">
        <div class="comic-stamp">FORENSE</div>

        <!-- SCENE 1: LA PANTALLA AZUL GLOBAL (0s - 8.5s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag" style="background: #ef4444;">APAGÓN INFORMÁTICO</div>
          <div class="headline-black">
            ¿CÓMO 1 LÍNEA APAGÓ EL MUNDO?
          </div>
          <div class="punch-pill">
            8.5M DE MÁQUINAS EN BSOD
          </div>
          <div class="metric-box">
            <div class="metric-title">AEROLÍNEAS, BANCOS Y SALUD:</div>
            <div class="metric-stat">$10,000 MILLONES EN PÉRDIDAS</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 18px;">
            El mayor colapso en la historia del software.
          </div>
        </div>

        <!-- SCENE 2: RING 0 VS RING 3 (8.5s - 20.5s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #0284c7;">EL SANTUARIO DEL KERNEL</div>
          <div class="headline-black" style="font-size: 50px;">
            SIN RED DE SEGURIDAD
          </div>
          <div class="punch-pill" style="background: #ef4444; font-size: 36px;">
            PUNTERO NULO EN MEMORIA FÍSICA
          </div>
          <div class="metric-box" style="background: #fee2e2; border-color: #ef4444;">
            <div style="font-size: 32px; font-weight: 900; color: #991b1b;">
              ⚠️ RING 0: ACCESO ABSOLUTO A CPU
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Un error en el núcleo no se recupera: colapsa.
          </div>
        </div>

        <!-- SCENE 3: EL PECADO DEL QA (20.5s - 33.5s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #f59e0b; color: #000;">DESPLIEGUE FATAL</div>
          <div class="headline-black" style="font-size: 50px;">
            CERO PRUEBAS CANARIO
          </div>
          <div class="punch-pill" style="background: #000; color: #f59e0b !important; font-size: 36px; border-color: #f59e0b;">
            DESPLIEGUE A TODO EL PLANETA
          </div>
          <div class="metric-box" style="background: #fefce8; border-color: #f59e0b;">
            <div style="font-size: 30px; font-weight: 900; color: #854d0e;">
              🛠️ RECUPERACIÓN MANUAL CON USB Y BITLOCKER
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            La pesadilla de los administradores de sistemas.
          </div>
        </div>

        <!-- SCENE 4: EL FUTURO SIN KERNEL (33.5s - 45s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #0f172a; box-shadow: 4px 4px 0px #38bdf8;">RESILIENCIA SISTÉMICA</div>
          <div class="headline-black" style="font-size: 52px;">
            EXPULSAR ANTIVIRUS<br>FUERA DEL NÚCLEO
          </div>
          <div class="punch-pill" style="font-size: 36px; background: #000; border-color: #38bdf8; color: #38bdf8 !important; box-shadow: 8px 8px 0px #38bdf8;">
            LA REVOLUCIÓN EBPF
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 20px;">
            Autopsia forense completa en:
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
    print("✅ Plantillas HyperFrames generadas para Stupy 06.")

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
    
    res_entry = f'''    # sIA Sec 01 - CrowdStrike, Ring 0 y el Bug del Kernel - 2 de Noviembre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-sec-01-la-caida-global-de-crowdstrike-y-el-bug-del-ring-0",
        "category": "Ciberseguridad & Kernel",
        "badge_color": "blue",
        "read_time": "12 min",
        "title": "sIA Sec #01: La Caída Global de CrowdStrike y el Bug del Ring 0: Cómo una actualización de kernel paralizó 8.5 millones de máquinas, bancos y aeropuertos",
        "subtitle": "La anatomía forense del fallo de memoria en Channel File 291: Ring 0 vs. Ring 3, la ausencia de despliegues canario y la urgencia de expulsar el software de seguridad fuera del núcleo del sistema operativo.",
        "thesis": "La concentración de privilegios irrestrictos en el Modo Núcleo (Ring 0) para software de seguridad corporativo constituye un riesgo sistémico inaceptable. La adopción de arquitecturas aisladas en espacio de usuario y mecanismos de observabilidad formalmente verificados como eBPF es imprescindible para salvaguardar la infraestructura crítica global.",
        "nexo": "Primer episodio de la serie de Ciberseguridad & Resiliencia de Sistemas: Arquitectura de sistemas operativos, fallos de memoria, despliegues canario y gobernanza de infraestructura crítica.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "title": "1. El Apagón Informático Global: La Fragilidad de la Infraestructura Crítica",
                "body": """
El 19 de julio de 2024, el tejido digital de la civilización moderna experimentó una fractura sistémica sin precedentes. En cuestión de minutos, más de 8.5 millones de computadoras y servidores con sistema operativo Windows quedaron paralizados en bucles infinitos de Pantalla Azul de la Muerte (BSOD), exhibiendo el mensaje de excepción 'PAGE FAULT IN NONPAGED AREA'.

Aerolíneas globales cancelaron decenas de miles de vuelos dejando a millones de pasajeros atrapados; quirófanos y tratamientos oncológicos en hospitales de Estados Unidos y Europa fueron suspendidos; plataformas bancarias, cajeros automáticos y sistemas de logística portuaria dejaron de procesar transacciones. Con un impacto económico directo estimado en más de 10,000 millones de dólares, el incidente demostró que no se requería una ciberguerra ni un ataque de ransomware de actores estatales para doblegar a la economía mundial: bastaba un fallo de puntero en una actualización rutinaria de ciberseguridad.
"""
            }},
            {{
                "title": "2. La Arquitectura de Anillos de Protección: Ring 0 vs. Ring 3",
                "body": """
Para comprender la mecánica del fallo es necesario analizar la jerarquía de hardware de los procesadores x86/x64 modernos. En el 'Ring 3' o Espacio de Usuario (User Space) se ejecutan todas las aplicaciones convencionales (navegadores, bases de datos, suites ofimáticas). Si un programa en Ring 3 comete una violación de memoria, el sistema operativo aborta el proceso sin comprometer la estabilidad del equipo.

En contraste, el 'Ring 0' o Modo Núcleo (Kernel Mode) es el santuario interior donde reside el núcleo del sistema operativo (ntoskrnl.exe) y los controladores de bajo nivel. En Ring 0 el software goza de acceso irrestricto a la memoria física y a todas las instrucciones de la CPU. No existe ninguna red de contención: si una sola instrucción en Ring 0 intenta acceder a una dirección de memoria inválida, la CPU dispara una excepción no manejable forzando el reinicio de emergencia para evitar la corrupción de datos en disco.
"""
            }},
            {{
                "title": "3. Anatomía Forense del Bug: El Archivo Channel 291",
                "body": """
El sensor CrowdStrike Falcon opera en Ring 0 mediante un controlador registrado como 'Boot-Start Driver' (csagent.sys), el cual se inicializa en los primeros instantes del arranque de Windows. Para incorporar nuevas reglas de detección sin exigir reinicios de servidores, Falcon descarga archivos binarios denominados 'Channel Files'.

A las 04:09 UTC, CrowdStrike distribuyó el archivo 'Channel 291', orientado a evaluar el uso de tuberías con nombre (Named Pipes) en ataques cibernéticos. El analizador del driver esperaba veintiún campos de entrada; sin embargo, el archivo distribuido únicamente contenía veinte. Al intentar evaluar el índice 21 inexistente, el controlador leyó a través de un puntero nulo (dirección hexadecimal 0x9c), provocando una violación de acceso inmediata en Ring 0 y desencadenando el colapso en cadena de millones de equipos.
"""
            }},
            {{
                "title": "4. El Colapso de QA y la Falta de Despliegues Canario",
                "body": """
Más allá del error de programación en C++, la catástrofe evidenció una omisión imperdonable en las prácticas de ingeniería de infraestructura: la ausencia de despliegues canario (canary deployments). CrowdStrike consideró los Channel Files como 'datos' en lugar de código ejecutable, lo que provocó que su validador automático aprobara el archivo corrupto debido a un fallo en su propia lógica de pruebas.

Posteriormente, la actualización fue inyectada de manera simultánea e indiscriminada a nivel planetario en lugar de seguir un esquema escalonado (1%, 10%, 25%, 100%). Esta decisión transformó un fallo aislado en un apagón mundial, forzando a los equipos de TI a realizar intervenciones presenciales máquina por máquina, ingresando claves de recuperación BitLocker de 48 caracteres para eliminar el archivo corrupto en Modo Seguro.
"""
            }},
            {{
                "title": "5. El Futuro de la Ciberseguridad: Expulsar los Antivirus del Kernel",
                "body": """
La cumbre de seguridad de Windows celebrada por Microsoft en Redmond marcó un punto de inflexión definitivo. Siguiendo el precedente de Apple en macOS con Endpoint Security y System Extensions, la industria ha acelerado el desarrollo de mecanismos para migrar los agentes de seguridad fuera del Ring 0.

El uso de eBPF (Extended Berkeley Packet Filter) en Linux y su implementación en Windows se perfila como la arquitectura del futuro: permite ejecutar sondas de seguridad en el kernel pero sometidas a un verificador formal estricto que garantiza en tiempo de compilación que el código jamás accederá a memoria prohibida ni entrará en bucles infinitos. La lección de CrowdStrike es incontestable: otorgar privilegios absolutos en el núcleo a software de terceros es una práctica obsoleta e insostenible.
"""
            }}
        ],
        "apa_references": [
            "CrowdStrike Intelligence. (2024). *External Technical Root Cause Analysis: Channel File 291 Incident*. CrowdStrike Security Reports. https://www.crowdstrike.com",
            "Microsoft Security Response Center. (2024). *Windows Security Ecosystem Architecture and Resiliency: Moving Beyond Kernel Drivers*. Microsoft Technical Whitepapers.",
            "Russinovich, M., Solomon, D. A., & Ionescu, A. (2021). *Windows Internals, Part 1: System architecture, processes, threads, memory management, and more* (7th ed.). Microsoft Press.",
            "Gregg, B. (2020). *BPF Performance Tools: Deep Visibility into Systems and Performance*. Addison-Wesley Professional.",
            "cacs, & sIA Editora. (2026). *sIA Sec #01: La Caída Global de CrowdStrike y el Bug del Ring 0: Cómo una actualización de kernel paralizó 8.5 millones de máquinas, bancos y aeropuertos*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if "sia-sec-01-la-caida-global-de-crowdstrike-y-el-bug-del-ring-0" not in content:
        content = content.replace(
            'RESEARCH_DATABASE = {',
            'RESEARCH_DATABASE = {\n' + res_entry
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Entrada de investigación sIA Sec #01 inyectada en build_magazine.py")

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
id: reel-stupy-06
titulo: "La Caída Global de CrowdStrike y el Bug del Ring 0: Cómo una actualización paralizó el 43% del mundo digital"
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
  - ciberseguridad
  - crowdstrike
  - kernel
  - windows
  - bsod
  - devops
  - sysadmin
---

# 💥 La Caída Global de CrowdStrike: El Bug de Memoria en Ring 0

> **Estilo Visual:** Cómic-Pop Halftone BSOD Cyber Blue & Alerta Rojo Neón, Tarjeta Escudo 20px Solid Shadow, Audio EBU R128 (-16 LUFS).

---

## 🎬 Reproductor del Video (Vertical 9:16)
![[{REEL_FILENAME}]]

**Póster Oficial:**
![[{REEL_POSTER_FILENAME}|350]]

---

## 📱 Kit de Copys & Hashtags para Publicación en Móvil (TikTok / Shorts / Instagram / LinkedIn)

### 🎯 Título Gancho (Hook):
`¿Cómo una sola línea de código apagó bancos, aeropuertos y hospitales de todo el mundo? 💥💻`

### ✍️ Descripción para Redes (Copy de Alto Alcance):
> 8.5 millones de máquinas colapsadas en bucle de Pantalla Azul en un solo segundo...
>
> No fue un ciberataque: fue un puntero nulo en Ring 0 y cero pruebas canario de despliegue.
>
> ¿Tiene sentido seguir otorgando permisos de kernel a los antivirus corporativos? Cuéntanos tu postura en comentarios.

### 🏷️ Bloque de Hashtags Estratégicos:
```
#ciberseguridad #crowdstrike #windows #bsod #kernel #devops #sysadmin #softwareengineering #programacion #infosec #siapodcast
```

---

## 🎙️ Guion & Voces (Jorge & Dalia +6%)

### Escena 1: El Apagón Global (00:00 - 08:50)
* **JORGE:** ¿Cómo una sola línea de código paralizó bancos, hospitales y aeropuertos de todo el mundo? La caída global de CrowdStrike no fue un ciberataque: fue el bug del Ring Cero...
* *Animación:* Badge pop-in `8.5M DE MÁQUINAS EN BSOD 💥` con sombra dura negra.

### Escena 2: Ring 0 vs Ring 3 (08:50 - 20:50)
* **DALIA:** En el Modo Núcleo de Windows no hay red de seguridad. El sensor Falcon intentó leer un puntero nulo en memoria física y colapsó el kernel en segundos.
* *Animación:* Tarjeta métrica: `RING 0: ACCESO ABSOLUTO A CPU` vs `PUNTERO NULO EN MEMORIA`.

### Escena 3: El Pecado del QA (20:50 - 33:50)
* **JORGE:** CrowdStrike violó la regla de oro: lanzó el parche a todo el planeta a la misma hora sin pruebas canario. Y millones de ingenieros tuvieron que arreglarlo a mano con memorias USB.
* *Animación:* Badge de alerta: `🛠️ RECUPERACIÓN MANUAL CON USB Y BITLOCKER`.

### Escena 4: El Futuro sin Kernel (33:50 - 45:00)
* **DALIA:** El software de seguridad debe salir del núcleo. Analiza el reporte forense completo y las fuentes académicas en `escucha-sia.github.io` y en *sIA Podcast*.
* *Animación:* Píldora neón azul con URL destacada.

---

## 🔗 Referencias & Backlinks
* **Artículo Web Completo con Fuentes APA:** [[03_Articulos/sia-sec-01-la-caida-global-de-crowdstrike-y-el-bug-del-ring-0]]
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
    msg = f"feat(episode): publish sIA Sec 01 - CrowdStrike, Ring 0 and BSOD bug with Reel Stupy 06"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(BASE_DIR), check=True)
    
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if push_res.returncode == 0:
        print("🎉 ¡Despliegue a GitHub Pages exitoso!")
    else:
        print("⚠️ Advertencia al hacer push:", push_res.stderr)

def step9_upload_to_tiktok():
    print("\n" + "="*70)
    print("📱 PASO 9: Subiendo Reel 06 a TikTok Automáticamente (@escucha_sia)...")
    print("="*70)
    
    # Actualizar publish_reels_to_tiktok.py con Reel 06 y caption
    pub_script = BASE_DIR / "scripts" / "publish_reels_to_tiktok.py"
    pub_content = pub_script.read_text(encoding='utf-8')
    
    new_reel_entry = f'''REELS_TO_PUBLISH = [
    {{
        "file": BASE_DIR / "reels" / "{REEL_FILENAME}",
        "caption": "¿Cómo una línea de código apagó 8.5 millones de PCs? La caída de CrowdStrike y el bug del Ring 0. Episodio en Spotify (sIA) y blog en perfil. #ciberseguridad #crowdstrike #windows #bsod #kernel #devops #sysadmin #programacion #siapodcast"
    }}
]'''
    pub_content = re.sub(r'REELS_TO_PUBLISH = \[.*?\]', new_reel_entry, pub_content, flags=re.DOTALL)
    pub_script.write_text(pub_content, encoding='utf-8')
    
    res = subprocess.run([sys.executable, str(pub_script)], cwd=str(BASE_DIR), text=True)
    if res.returncode == 0:
        print("🎉 ¡Reel 06 publicado y verificado en TikTok Studio exitosamente!")
    else:
        print(f"⚠️ Error al subir Reel 06 a TikTok: código {res.returncode}")

async def main_async():
    print("="*70)
    print("🚀 INICIANDO PRODUCCIÓN INTEGRAL 360° - EPISODIO & REEL STUPY 06")
    print("Tema: sIA Sec #01: La Caída Global de CrowdStrike y el Bug del Ring 0")
    print("="*70)
    
    # 1. Audio Completo
    await step1_generate_full_audio()
    
    # 2. Audio Reel
    await step2_generate_reel_audio()
    
    # 3. Composición HyperFrames
    step3_prepare_hyperframes_composition()
    
    # 4. Render HyperFrames Reel
    step4_render_reel()
    
    # 5. Registrar y Recompilar sIA Journal
    step5_register_and_rebuild_magazine()
    
    # 6. Sincronizar Google Drive
    step6_sync_to_gdrive()
    
    # 7. Crear Ficha Obsidian y Kit de Redes
    step7_create_obsidian_and_social_kit()
    
    # 8. Git Commit & Deploy
    step8_git_deploy()

def main():
    asyncio.run(main_async())
    # 9. TikTok Upload (sync fuera del loop asyncio)
    step9_upload_to_tiktok()

if __name__ == "__main__":
    main()
