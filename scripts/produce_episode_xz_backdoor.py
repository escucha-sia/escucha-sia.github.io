import os
import sys
import shutil
import asyncio
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
ARTICULOS_DIR = BASE_DIR / "articulos"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
SPOTIFY_REELS_DIR = SPOTIFY_DIR / "Reels"
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
GDRIVE_AUDIO_DIR = Path(r"G:\Mi unidad\sIA_Hub\03_Audios_Completos")
NODE_PATH = r"C:\Carlos\nodejs"

EPISODE_FILENAME = "sIA_Sec_03_XZ_Utils_Backdoor_Andres_Freund_SSH_2026-11-04.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

PODCAST_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Bienvenidos a sIA Podcast. Hoy en sIA Sec analizamos la que es, sin exagerar, la historia de espionaje cibernético y paranoia técnica más impresionante del siglo veintiuno: cómo un retraso de medio segundo en una terminal de Linux evitó el mayor colapso de seguridad en la historia de Internet."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Ocurrió a finales de marzo de 2024. El objetivo era xz utils y su librería liblzma, un paquete de compresión de datos ubicuo que está instalado por defecto en prácticamente todos los servidores Linux del mundo, desde centros de datos bancarios hasta satélites y nubes gubernamentales."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Lo aterrador de este ataque no fue la sofisticación técnica, sino la paciencia infinita de los atacantes. Durante más de dos años, un perfil anónimo bajo el seudónimo de Jia Tan se dedicó a construir una identidad impecable en el mundo del código abierto. Ayudó a corregir bugs menores, limpió código y se ganó la confianza del único y agotado mantenedor de xz, Lasse Collin."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Junto a Jia Tan, una red de cuentas títere comenzó a presionar a Lasse con mensajes agresivos exigiendo que cediera el mantenimiento del proyecto. Agotado por la carga mental, Lasse le entregó las llaves del repositorio. Una vez con control total de los lanzamientos oficiales, Jia Tan preparó las versiones 5.6.0 y 5.6.1 con un caballo de Troya invisible a simple vista."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El código malicioso no estaba en los archivos de código C, donde cualquier auditor lo habría detectado. Estaba oculto dentro de archivos binarios de prueba aparentemente corruptos, utilizados para comprobar algoritmos de descompresión. Durante el proceso de compilación con M4, el script extraía un archivo objeto precompilado que utilizaba una característica avanzada de Linux llamada funciones indirectas de GNU, o IFUNC."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "¿Y contra qué apuntaba? Contra OpenSSH, el servicio que permite la administración remota de cualquier servidor. A través de una cadena de dependencias complejas, systemd enlazaba con liblzma, lo que permitía al malware interceptar la función de desencriptación de claves públicas de SSH. Cualquier persona con la clave privada de los atacantes podía enviar una firma que ejecutaba comandos remotos con privilegios de root sin dejar un solo rastro en los registros."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Era la llave maestra para abrir cualquier servidor del planeta. Y habría llegado a las versiones estables de Debian, Red Hat y Ubuntu de no ser por un héroe inesperado: Andrés Freund, un ingeniero de software alemán que trabajaba en Microsoft optimizando PostgreSQL."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Andrés estaba ejecutando micro-benchmarks de rendimiento en Debian sid. Al hacer pruebas de estrés, notó tres anomalías diminutas: el inicio de sesión por SSH consumía demasiada CPU, la herramienta Valgrind arrojaba errores extraños de memoria en liblzma, y los logins tardaban exactamente quinientos milisegundos más de lo habitual."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Cualquier otro desarrollador habría atribuido ese medio segundo a congestión de red o un fallo pasajero. Pero Andrés se negó a ignorarlo. Empezó a desensamblar el binario, rastreó las llamadas al linker y descubrió la inyección maliciosa en los archivos M4. Cuando publicó la alerta el 29 de marzo, la comunidad de ciberseguridad entró en estado de emergencia global."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "El descubrimiento de Andrés Freund salvó literalmente los cimientos de la economía digital. Pero dejó al descubierto la fragilidad más profunda del software moderno: que infraestructuras críticas que mueven billones de dólares dependen de proyectos de código abierto mantenidos por voluntarios solitarios y agotados en su tiempo libre."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El análisis técnico completo, la cadena de explotación de IFUNC y el post-mortem paso a paso están disponibles en sIA Journal en escucha guion sia punto github punto io. Y en TikTok pueden ver la animación visual en arroba escucha guion bajo sia."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Gracias por escucharnos en este fascinante episodio de sIA Sec. Soy Dalia."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Y yo soy Jorge. ¡Hasta el próximo episodio de sIA Podcast!"
    }
]

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Cómo un retraso de medio segundo en una pantalla de Linux salvó al internet entero del mayor ciberataque de la historia? Te presento el caso XZ Utils..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Durante dos años, un espía con el alias Jia Tan se ganó la confianza del agotado mantenedor de xz e inyectó un backdoor indetectable en OpenSSH usando funciones IFUNC."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Era una llave maestra para ejecutar root en cualquier servidor del mundo. Pero un ingeniero de PostgreSQL, Andrés Freund, notó que SSH tardaba 500 milisegundos más de lo normal."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Desensambló el binario, descubrió el ataque patrocinado por un estado y lo frenó horas antes de llegar a los servidores de bancos y gobiernos."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El post-mortem técnico de ingeniería inversa está en sIA Journal. Link en bio."
    }
]

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
    print("🎙️ PASO 1: Generando Master Audio de XZ Utils Backdoor...")
    print("="*70)
    
    final_master = AUDIO_DIR / EPISODE_FILENAME
    if final_master.exists() and final_master.stat().st_size > 1000000:
        print(f"ℹ️ Master de audio ya existe: {final_master} ({final_master.stat().st_size / (1024*1024):.2f} MB)")
        SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
        if GDRIVE_AUDIO_DIR.exists():
            shutil.copy2(final_master, GDRIVE_AUDIO_DIR / EPISODE_FILENAME)
        return

    temp_dir = BASE_DIR / "temp_audio_sec_03"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    durations = []
    for idx, item in enumerate(PODCAST_DIALOGUE):
        chunk_file = temp_dir / f"chunk_{idx:03d}_{item['speaker'].lower()}.mp3"
        print(f"  [{idx+1}/{len(PODCAST_DIALOGUE)}] Sintetizando voz de {item['speaker']}...")
        asyncio.run(synthesize_voice_segment(item["text"], item["voice"], chunk_file))
        chunk_files.append(chunk_file)
        
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(chunk_file)
        ], capture_output=True, text=True, check=True)
        durations.append(float(probe.stdout.strip()))

    srt_path = AUDIO_DIR / EPISODE_FILENAME.replace(".mp3", ".srt")
    vtt_path = AUDIO_DIR / EPISODE_FILENAME.replace(".mp3", ".vtt")
    
    def fmt_srt(s):
        hrs = int(s // 3600)
        mins = int((s % 3600) // 60)
        secs = int(s % 60)
        millis = int((s - int(s)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"
        
    def fmt_vtt(s):
        hrs = int(s // 3600)
        mins = int((s % 3600) // 60)
        secs = int(s % 60)
        millis = int((s - int(s)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"
        
    cur_time = 0.0
    with open(srt_path, "w", encoding="utf-8") as fsrt, open(vtt_path, "w", encoding="utf-8") as fvtt:
        fvtt.write("WEBVTT\n\n")
        for i, (item, dur) in enumerate(zip(PODCAST_DIALOGUE, durations)):
            start_t = cur_time
            end_t = cur_time + dur
            fsrt.write(f"{i+1}\n{fmt_srt(start_t)} --> {fmt_srt(end_t)}\n{item['speaker']}: {item['text']}\n\n")
            fvtt.write(f"{i+1}\n{fmt_vtt(start_t)} --> {fmt_vtt(end_t)}\n{item['speaker']}: {item['text']}\n\n")
            cur_time = end_t + 0.35

    concat_txt = temp_dir / "concat_full.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")

    raw_voice_master = temp_dir / "raw_voice_master.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy", str(raw_voice_master)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    music_track = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_voice_master),
        "-stream_loop", "-1", "-i", str(music_track),
        "-filter_complex",
        "[1:a]volume=0.10,afade=t=in:st=0:d=2.0[bg];"
        "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-16:LRA=11:TP=-1.5[norm]",
        "-map", "[norm]",
        "-ar", "44100", "-b:a", "192k",
        str(final_master)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
    if GDRIVE_AUDIO_DIR.exists():
        shutil.copy2(final_master, GDRIVE_AUDIO_DIR / EPISODE_FILENAME)
        
    print(f"✅ Master Full Audio creado: {final_master} ({final_master.stat().st_size / (1024*1024):.2f} MB)")

def step2_produce_reel_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 2: Generando Audio del Reel Vertical (45s Cerrados EBU R128)...")
    print("="*70)
    
    temp_dir = BASE_DIR / "temp_audio_stupy_13"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_file = temp_dir / f"chunk_{idx}_{item['speaker'].lower()}.mp3"
        print(f"  [Reel {idx+1}/{len(REEL_DIALOGUE)}] {item['speaker']}...")
        asyncio.run(synthesize_voice_segment(item["text"], item["voice"], chunk_file))
        chunk_files.append(chunk_file)
        
    concat_list = temp_dir / "concat_reel.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    raw_reel = temp_dir / "raw_reel_voice.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(raw_reel)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    music_track = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_reel),
        "-stream_loop", "-1", "-i", str(music_track),
        "-filter_complex",
        "[1:a]volume=0.14,afade=t=in:st=0:d=1.5,afade=t=out:st=43.5:d=1.5[bg];"
        "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        f"[mixed]apad=whole_dur=45.0,afade=t=out:st=44.0:d=1.0[padded];"
        "[padded]loudnorm=I=-16:LRA=10:TP=-1.5[norm]",
        "-map", "[norm]",
        "-ar", "44100", "-b:a", "192k",
        str(clip_audio)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    shutil.copy2(clip_audio, ENGINE_DIR / "assets" / "audio.mp3")
    print(f"✅ Audio del Reel verificado y mezclado en: {clip_audio}")

def step3_prepare_stupy_composition():
    print("\n" + "="*70)
    print("🎨 PASO 3: Generando Composición Stupy Cyber-Espionage con Barra de Capítulos...")
    print("="*70)
    
    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 13 - XZ Utils Backdoor 500ms</title>
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

      /* Matriz Halftone Hacker Emerald/Slate */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#10b981 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}

      .matrix-grid {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          0deg,
          rgba(16, 185, 129, 0.04) 0px,
          rgba(16, 185, 129, 0.04) 2px,
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
        font-size: 80px;
        color: rgba(16, 185, 129, 0.06);
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
        padding: 80px 60px 100px 60px;
      }}

      /* HEADER TÁCTICO CON CAPÍTULOS */
      .header-box {{
        display: flex;
        flex-direction: column;
        gap: 16px;
      }}

      .brand-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
      }}

      .brand-pill {{
        background: #10b981;
        color: #000000;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.6);
        border: 2px solid #ffffff;
      }}

      .tag-pill {{
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #059669;
      }}

      /* BARRA DE CAPÍTULOS */
      .chapters-bar {{
        display: flex;
        gap: 10px;
        width: 100%;
        margin-top: 10px;
      }}

      .chapter-pill {{
        flex: 1;
        padding: 12px 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 15px;
        color: #94a3b8;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }}

      .chapter-pill.active {{
        background: #059669;
        color: #ffffff;
        border-color: #34d399;
        box-shadow: 0 0 20px rgba(52, 211, 153, 0.6);
        transform: scale(1.04);
      }}

      /* TARJETA DINÁMICA CENTRAL */
      .main-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 50px 45px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(16, 185, 129, 0.25);
        border: 6px solid #10b981;
        position: relative;
        min-height: 820px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }}

      .scene {{
        display: none;
        flex-direction: column;
        gap: 24px;
        text-align: center;
        animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
      }}

      @keyframes popIn {{
        0% {{ opacity: 0; transform: scale(0.92); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}

      .myth-tag {{
        display: inline-block;
        align-self: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 26px;
        padding: 8px 24px;
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }}

      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 52px;
        line-height: 1.1;
        letter-spacing: -1px;
        color: #09090f;
      }}

      .punch-pill {{
        display: inline-block;
        align-self: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 38px;
        padding: 16px 36px;
        border-radius: 20px;
        line-height: 1.2;
        border: 3px solid #000;
      }}

      .metric-box {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: #f8fafc;
        border: 4px dashed #94a3b8;
        border-radius: 20px;
        padding: 24px;
        margin-top: 10px;
      }}

      .final-pill {{
        background: #059669;
        color: #fff;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(5, 150, 105, 0.4);
      }}

      /* FOOTER */
      .footer-badge {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
      }}

      .channel-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 26px;
        color: #94a3b8;
        letter-spacing: 1px;
      }}

      .progress-bar-container {{
        width: 100%;
        height: 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }}

      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        width: 0%;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="matrix-grid"></div>
    <div class="bg-ticker">XZ UTILS &bull; SSH BACKDOOR &bull; JIA TAN &bull; 500MS &bull; FREUND</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🛡️ sIA Sec #03</div>
          <div class="tag-pill">CYBER ESPIONAGE</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill active" id="chap-1">01 El Enigma 500ms</div>
          <div class="chapter-pill" id="chap-2">02 Infiltración 2 Años</div>
          <div class="chapter-pill" id="chap-3">03 Llave Maestra SSH</div>
          <div class="chapter-pill" id="chap-4">04 El Héroe Andrés</div>
        </div>
      </div>

      <div class="main-card">
        <!-- SCENE 1: EL ENIGMA (0.0s - 11.0s) -->
        <div class="scene" id="scene-1" style="display: flex;">
          <div class="myth-tag" style="background: #10b981; color: #000;">EL DÍA QUE INTERNET CASI CAE</div>
          <div class="headline-black">
            500 MILISEGUNDOS DE LAG
          </div>
          <div class="punch-pill" style="background: #d1fae5; color: #065f46; border-color: #10b981;">
            EL BACKDOOR DE XZ UTILS
          </div>
          <div class="metric-box">
            <div style="font-size: 32px; font-weight: 900; color: #047857;">
              ⚡ AFECTABA A TODO LINUX
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #64748b;">
              Servidores bancarios, nubes y gobiernos en jaque
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            La mayor conspiración en código abierto.
          </div>
        </div>

        <!-- SCENE 2: INFILTRACIÓN (11.0s - 22.0s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #6366f1; color: #fff;">INGENIERÍA SOCIAL</div>
          <div class="headline-black">
            JIA TAN: 2 AÑOS DE PACIENCIA
          </div>
          <div class="punch-pill" style="background: #000; color: #818cf8; border-color: #6366f1;">
            GANÁNDOSE AL MANTENEDOR
          </div>
          <div class="metric-box" style="background: #eef2ff; border-color: #6366f1;">
            <div style="font-size: 30px; font-weight: 900; color: #4338ca;">
              🕵️ PRESIÓN CON CUENTAS TÍTERE
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #6366f1;">
              Inyectó el código en archivos de prueba corruptos
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Compilación oculta mediante macros M4.
          </div>
        </div>

        <!-- SCENE 3: LLAVE MAESTRA (22.0s - 34.0s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">EXPLOIT DE KERNEL</div>
          <div class="headline-black">
            BYPASS ROOT EN OPENSSH
          </div>
          <div class="punch-pill" style="background: #fee2e2; color: #b91c1c; border-color: #ef4444;">
            HOOK IFUNC EN LIBLZMA
          </div>
          <div class="metric-box" style="background: #fef2f2; border-color: #ef4444;">
            <div style="font-size: 30px; font-weight: 900; color: #b91c1c;">
              🔑 CONTROL TOTAL SIN REGISTROS
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #ef4444;">
              Una clave privada podía mandar órdenes a cualquier servidor
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            A horas de entrar a Debian y Red Hat estables.
          </div>
        </div>

        <!-- SCENE 4: EL HÉROE (34.0s - 45.0s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #10b981; color: #000;">EL INGENIERO OBSERVADOR</div>
          <div class="headline-black">
            ANDRÉS FREUND
          </div>
          <div class="punch-pill" style="background: #d1fae5; color: #065f46; font-size: 34px;">
            MICRO-BENCHMARK DE POSTGRESQL
          </div>
          <div class="final-pill">
            🎧 EPISODIO COMPLETO EN SPOTIFY
          </div>
          <div style="font-size: 26px; font-weight: 800; color: #059669; margin-top: 14px;">
            Lee el post-mortem en sIA Journal (link en bio)
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

        c1.classList.remove('active');
        c2.classList.remove('active');
        c3.classList.remove('active');
        c4.classList.remove('active');

        if (time < 11.0) {{
          s1.style.display = 'flex';
          c1.classList.add('active');
        }} else if (time < 22.0) {{
          s2.style.display = 'flex';
          c2.classList.add('active');
        }} else if (time < 34.0) {{
          s3.style.display = 'flex';
          c3.classList.add('active');
        }} else {{
          s4.style.display = 'flex';
          c4.classList.add('active');
        }}

        const pct = Math.min(100, Math.max(0, (time / 45.0) * 100));
        document.querySelector('.progress-bar-fill').style.width = pct + '%';
      }}

      window.__hyperframes = {{
        seek: function(t) {{
          updateTimeline(t);
        }}
      }};
    </script>
  </div>
  </body>
</html>"""

    scene_path = ENGINE_DIR / "compositions" / "scene.html"
    scene_path.parent.mkdir(parents=True, exist_ok=True)
    scene_path.write_text(scene_html, encoding='utf-8')
    print(f"✅ Escena HTML escrita en: {scene_path}")

def step4_render_hyperframes():
    print("\n" + "="*70)
    print("🎬 PASO 4: Renderizando Reel Vertical 1080x1920 con HyperFrames GPU...")
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
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / REEL_FILENAME)
        
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
    print("📖 PASO 5: Registrando XZ Utils en sIA Journal...")
    print("="*70)
    
    build_mag_path = BASE_DIR / "build_magazine.py"
    content = build_mag_path.read_text(encoding='utf-8')
    
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'REELS_MAP = {',
            f'REELS_MAP = {{\n    "{EPISODE_FILENAME}": "{REEL_FILENAME}",'
        )
    
    res_entry = f'''    # sIA Sec 03 - XZ Utils Backdoor Andres Freund - 4 de Noviembre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-sec-03-el-backdoor-de-xz-utils-y-los-500ms-que-salvaron-internet",
        "category": "Ciberseguridad & Open Source",
        "badge_color": "emerald",
        "read_time": "15 min",
        "title": "sIA Sec #03: El Backdoor de XZ Utils: Cómo 500 Milisegundos de Lag Salvaron al Internet Entero",
        "subtitle": "Ingeniería Social de 2 Años, IFUNC Hooks en liblzma, Infiltración de OpenSSH y el Descubrimiento de Andrés Freund.",
        "thesis": "La crisis de seguridad de XZ Utils expone la vulnerabilidad estructural más crítica del ecosistema digital moderno: cómo actores estatales pueden invertir años de ingeniería social sobre mantenedores comunitarios agotados para inyectar vectores de ataque criptográficos indetectables que comprometen la totalidad de la infraestructura de servidores de producción de la civilización contemporánea.",
        "nexo": "Tercer episodio de Ciberseguridad: Espionaje cibernético tras CrowdStrike y Videostrong, arquitectura de OpenSSH, GNU IFUNC, micro-benchmarks y gobernanza de código abierto.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "type": "heading",
                "text": "1. 29 de Marzo de 2024: La Alerta que Paralizó al Mundo Tecnológico"
            }},
            {{
                "type": "paragraph",
                "text": "El viernes 29 de marzo de 2024, un mensaje publicado en la lista de correo de seguridad de código abierto oss-security hizo que los equipos de infraestructura de las principales empresas y gobiernos del planeta declararan estado de emergencia inmediata. Andrés Freund, un ingeniero de software de Microsoft especializado en bases de datos PostgreSQL, notificó la detección de un backdoor malicioso de ejecución remota de código inyectado en las versiones oficiales 5.6.0 y 5.6.1 de xz utils y liblzma, la librería estándar de compresión de datos del núcleo de Linux."
            }},
            {{
                "type": "paragraph",
                "text": "A diferencia de vulnerabilidades accidentales originadas por desbordamiento de búfer o punteros nulos, este incidente representaba la operación de espionaje e infiltración en la cadena de suministro más sofisticada y paciente jamás documentada en la historia de la informática."
            }},
            {{
                "type": "heading",
                "text": "2. La Operación Jia Tan: Dos Años Cultivando una Falsa Identidad"
            }},
            {{
                "type": "paragraph",
                "text": "La infiltración comenzó a finales de 2021. Un perfil bajo el seudónimo de 'Jia Tan' (JiaT75) comenzó a enviar parches menores y mejoras de compresión al repositorio de xz. El proyecto estaba mantenido por una sola persona: Lasse Collin, un voluntario finlandés que llevaba más de una década sosteniendo el software en su tiempo libre bajo un severo agotamiento mental y quejas constantes de usuarios."
            }},
            {{
                "type": "paragraph",
                "text": "Para acelerar la entrega de privilegios, una red coordinada de cuentas títere (sockpuppets con nombres como Jigar Kumar y Dennis Ens) comenzó a presionar a Collin en foros públicos, recriminándole demoras en la integración de parches y sugiriendo agresivamente que cediera la gobernanza del código a Jia Tan. Agotado y confiando en la impecable trayectoria de Tan durante dos años, Collin le otorgó permisos de commit y control sobre los tarballs de distribución."
            }},
            {{
                "type": "heading",
                "text": "3. El Mecanismo Técnico: IFUNC Hooks y el Secuestro de OpenSSH"
            }},
            {{
                "type": "paragraph",
                "text": "Una vez al mando, Jia Tan diseñó un vector de inyección criptográfico de extraordinaria sofisticación. El código malicioso no se encontraba en el repositorio Git público, sino camuflado dentro de archivos binarios de prueba aparentemente corruptos ('bad-3-corrupt_lzma2.xz'). Durante el proceso de construcción mediante el sistema autotools (M4), scripts ofuscados extraían un archivo objeto (.o) que se vinculaba durante la compilación."
            }},
            {{
                "type": "paragraph",
                "text": "El payload aprovechaba las funciones indirectas de GNU (IFUNC) para resolver dinámicamente símbolos de bajo nivel antes de que el ejecutable terminara de cargarse en memoria. El objetivo final era el demonio del servidor SSH (sshd): en distribuciones como Debian y Ubuntu, systemd incluye soporte para compresión mediante liblzma, lo que provocaba que sshd cargara indirectamente la librería infectada en su espacio de memoria privilegiada."
            }},
            {{
                "type": "paragraph",
                "text": "Allí, el backdoor interceptaba la función 'RSA_public_decrypt'. Si un atacante enviaba un certificado SSH especialmente firmado con una clave privada de curva elíptica Ed448 predeterminada, el malware ejecutaba una orden arbitraria con privilegios de root antes de la fase de autenticación, sin activar registros del sistema ni levantar alertas en herramientas de auditoría."
            }},
            {{
                "type": "heading",
                "text": "4. El Descubrimiento: 500 Milisegundos de Rigor Técnico"
            }},
            {{
                "type": "paragraph",
                "text": "La introducción del malware en las ramas estables de Debian, Red Hat Enterprise Linux y SUSE era cuestión de semanas. De haberse consolidado, casi la totalidad de los servidores de internet habrían quedado expuestos a una puerta trasera indetectable. El plan fue frustrado por la obsesión técnica de Andrés Freund."
            }},
            {{
                "type": "paragraph",
                "text": "Mientras realizaba pruebas de rendimiento y micro-benchmarks para medir la latencia de conexiones PostgreSQL en Debian sid, Freund detectó que los inicios de sesión por SSH consumían un porcentaje anómalo de ciclos de reloj de la CPU y tardaban exactamente 500 milisegundos más de lo habitual. Asimismo, la herramienta de depuración Valgrind reportaba accesos inválidos a memoria dentro de liblzma."
            }},
            {{
                "type": "paragraph",
                "text": "En lugar de atribuir la lentitud a una sobrecarga de red o ignorar la advertencia, Freund comenzó a desensamblar el binario de sshd con gdb y objdump, identificó las tablas de reubicación manipuladas y desentrañó los scripts ofuscados en las macros M4. Su informe detallado permitió revocar de inmediato las versiones infectadas antes de su despliegue en entornos corporativos masivos."
            }},
            {{
                "type": "heading",
                "text": "5. Lecciones para la Seguridad y la Gobernanza del Software Libre"
            }},
            {{
                "type": "paragraph",
                "text": "El caso XZ Utils forzó una reevaluación global sobre la sostenibilidad del código abierto. Demostró que el modelo actual, donde dependencias críticas de las que depende el producto interno bruto del planeta están bajo la custodia de programadores individuales no remunerados, constituye un riesgo para la seguridad nacional de cualquier país."
            }},
            {{
                "type": "paragraph",
                "text": "Las medidas posteriores aceleraron la adopción de compilaciones reproducibles (Reproducible Builds), la eliminación de dependencias innecesarias en demonios de sistema críticos (como la desvinculación de liblzma de systemd en OpenSSH), y el financiamiento directo a mantenedores clave mediante consorcios como la OpenSSF."
            }}
        ],
        "references": [
            "Freund, A. (2024). Backdoor in upstream xz/liblzma leading to ssh server compromise. Open Source Security (oss-security) Mailing List.",
            "Goodin, D. (2024). What we know about the xz-utils backdoor that almost infected the world. Ars Technica.",
            "Cybersecurity and Infrastructure Security Agency (CISA). (2024). Alert: Supply Chain Compromise in XZ Utils (CVE-2024-3094). CISA Publications.",
            "OpenSSF. (2024). Analysis of the XZ Utils Social Engineering and Supply Chain Attack. Open Source Security Foundation Technical Brief."
        ]
    }},'''
    
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'ARTICULOS_RESEARCH = {',
            f'ARTICULOS_RESEARCH = {{\n{res_entry}'
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print(f"✅ Registrado XZ Utils en build_magazine.py")
        
    cmd_build = ["python", "build_magazine.py"]
    subprocess.run(cmd_build, cwd=str(BASE_DIR), check=True)
    print("✅ Revista digital y artículos compilados con éxito.")

def main():
    print("="*70)
    print("🚀 PIPELINE COMPLETO DE PRODUCCIÓN: sIA Sec #03")
    print("   XZ Utils Backdoor: 500ms que Salvaron Internet")
    print("="*70)
    
    step1_produce_full_audio()
    step2_produce_reel_audio()
    step3_prepare_stupy_composition()
    step4_render_hyperframes()
    step5_register_and_rebuild_magazine()
    
    print("\n" + "="*70)
    print("🎉 ¡PRODUCCIÓN 360° DE XZ UTILS COMPLETADA CON ÉXITO!")
    print("="*70)

if __name__ == "__main__":
    main()
