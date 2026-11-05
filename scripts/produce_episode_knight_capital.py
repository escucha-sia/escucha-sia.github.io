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

EPISODE_FILENAME = "sIA_Corp_07_Knight_Capital_440_Millones_Flag_Reutilizado_2026-11-04.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

PODCAST_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Bienvenidos a sIA Podcast. Hoy en Crónicas Corporativas y DevOps traemos uno de los casos de estudio más brutales en la historia de la ingeniería de software y Wall Street: cómo una sola empresa perdió cuatrocientos cuarenta millones de dólares en apenas cuarenta y cinco minutos por culpa de una variable booleana."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Ocurrió la mañana del primero de agosto de 2012. La protagonista era Knight Capital Group, en aquel entonces el mayor creador de mercado de acciones de todos los Estados Unidos. Manejaba el diecisiete por ciento de todo el volumen de la Bolsa de Nueva York y el diecisiete por ciento del NASDAQ. Eran los reyes indiscutibles de las finanzas algorítmicas de alta frecuencia."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Para entender cómo se gestó la catástrofe, tenemos que viajar a 2003, nueve años antes del desastre. En ese año, los desarrolladores de Knight crearon una función interna de pruebas llamada PowerPeg. Su único propósito era simular órdenes masivas a mercado para medir la velocidad de ejecución. Era código de prueba que nunca debió ejecutarse con dinero real."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Con los años, el sistema de enrutamiento de órdenes de Knight, conocido como SMARS, evolucionó a través de miles de líneas de código C++. Pero nadie borró PowerPeg. El código zombi permaneció dormido dentro de los binarios de producción durante casi una década, protegido por una bandera o flag de configuración apagada."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "En julio de 2012, la Bolsa de Nueva York anunció un nuevo programa de liquidez minorista, el Retail Liquidity Program. Los ingenieros de Knight tuvieron que actualizar SMARS con urgencia. Y aquí vino el primer pecado cardinal de arquitectura: en lugar de crear un nuevo flag limpio, decidieron reutilizar el viejo flag que antes controlaba la función PowerPeg."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Y aquí entró en juego el factor humano más destructivo: el despliegue manual. Knight no contaba con un pipeline automatizado de integración continua ni despliegues canary. La noche del 31 de julio, un técnico del equipo de operaciones se conectó manualmente vía consola a los ocho servidores de producción que componían el clúster de SMARS. Copió y reemplazó los binarios en siete de ellos... pero olvidó por completo el octavo servidor."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "A las nueve y media de la mañana, sonó la campana de apertura de Wall Street. Cientos de clientes enviaron órdenes para comprar acciones ordinarias. En los siete servidores actualizados, el nuevo código procesó las órdenes con normalidad. Pero en el octavo servidor, ocurrió la tormenta perfecta: el sistema tenía la nueva configuración con el flag activado, pero ejecutando el código viejo de 2003."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Para el código viejo, ese flag significaba: ejecuta PowerPeg a máxima potencia. PowerPeg entró en un bucle infinito destructivo: tomó una orden original de unas pocas miles de acciones y comenzó a emitir millones de micro-órdenes agresivas en el mercado abierto. Compraba al precio de venta más alto y vendía al precio de compra más bajo, perdiendo centavos por milisegundo a una escala monstruosa."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Durante cuarenta y cinco minutos de auténtico pánico en el centro de operaciones, mientras los teléfonos de la SEC ardían, el servidor fantasma ejecutó más de cuatro millones de transacciones, moviendo doscientos doce millones de acciones en ciento cincuenta y cuatro empresas diferentes. A las diez y cuarto de la mañana, cuando por fin lograron desconectar el servidor, la cuenta de pérdidas marcaba cuatrocientos cuarenta millones de dólares. Diez millones de dólares por minuto."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "El impacto fue fulminante. El valor de las acciones de Knight se desplomó un setenta y cinco por ciento en dos días. Incapaz de absorber el déficit de capital regulatorio, la junta directiva tuvo que vender la empresa de emergencia a su rival Getco a precio de liquidación, por un dólar con cincuenta centavos por acción cuando días antes valía más de diez."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Las lecciones técnicas que este desastre dejó a la industria del software son monumentales: nunca dejes código muerto en producción; los feature flags deben tener ciclo de vida estricto; los despliegues manuales en clústeres son inadmisibles; y todo sistema de alta velocidad necesita un interruptor de corte automático o circuit breaker cuando el volumen se dispara anomalamente."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Pueden leer el análisis forense con el informe oficial de la SEC y diagramas de arquitectura en escucha guion sia punto github punto io, y ver el desglose gráfico en TikTok en arroba escucha guion bajo sia."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Soy Jorge."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Y yo soy Dalia. ¡Hasta el próximo episodio de sIA Podcast!"
    }
]

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Cómo un desarrollador destruyó 440 millones de dólares en 45 minutos por reutilizar una sola variable booleana? Te presento la mayor pesadilla de DevOps en Wall Street..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "En 2012, Knight Capital manejaba el 17% de la Bolsa de Nueva York. Al actualizar su sistema de trading, reutilizaron un flag de código muerto de 2003 llamado PowerPeg."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Un técnico desplegó manualmente en 7 de los 8 servidores del clúster y olvidó el octavo. A las 9:30 AM, el servidor olvidado activó PowerPeg en bucle infinito: compraba caro y vendía barato sin parar."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "4 millones de operaciones y 10 millones de dólares perdidos por minuto. La firma quebró antes del mediodía y fue vendida en remate."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "El post-mortem completo de la SEC y las lecciones de CI/CD están en sIA Journal. Link en bio."
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
    print("🎙️ PASO 1: Generando Master Audio de Knight Capital...")
    print("="*70)
    
    final_master = AUDIO_DIR / EPISODE_FILENAME
    if final_master.exists() and final_master.stat().st_size > 1000000:
        print(f"ℹ️ Master de audio ya existe: {final_master} ({final_master.stat().st_size / (1024*1024):.2f} MB)")
        SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
        if GDRIVE_AUDIO_DIR.exists():
            shutil.copy2(final_master, GDRIVE_AUDIO_DIR / EPISODE_FILENAME)
        return

    temp_dir = BASE_DIR / "temp_audio_corp_07"
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
    
    temp_dir = BASE_DIR / "temp_audio_stupy_12"
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
    print("🎨 PASO 3: Generando Composición Stupy Wall Street Finance con Barra de Capítulos...")
    print("="*70)
    
    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 12 - Knight Capital $440M Bug</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #09090f;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}

      /* Matriz Halftone Dorada/Roja */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#f59e0b 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}

      .finance-grid {{
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
        font-size: 80px;
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
        background: #f59e0b;
        color: #000000;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 24px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.6);
        border: 2px solid #ffffff;
      }}

      .tag-pill {{
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 8px 20px;
        border-radius: 12px;
        border: 2px solid #ef4444;
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
        background: #f59e0b;
        color: #000000;
        border-color: #fbbf24;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.6);
        transform: scale(1.04);
      }}

      /* TARJETA DINÁMICA CENTRAL */
      .main-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 50px 45px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.8), 0 0 40px rgba(245, 158, 11, 0.25);
        border: 6px solid #f59e0b;
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
        background: #f59e0b;
        color: #000;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4);
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
        background: linear-gradient(90deg, #f59e0b 0%, #ef4444 100%);
        width: 0%;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="finance-grid"></div>
    <div class="bg-ticker">WALL STREET &bull; DEVOPS &bull; 440M &bull; POWERPEG &bull; BUG</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">📉 sIA Corp #07</div>
          <div class="tag-pill">DEVOPS DISASTER</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill active" id="chap-1">01 Wall Street</div>
          <div class="chapter-pill" id="chap-2">02 Código Zombi</div>
          <div class="chapter-pill" id="chap-3">03 Deploy Manual</div>
          <div class="chapter-pill" id="chap-4">04 $440 Millones</div>
        </div>
      </div>

      <div class="main-card">
        <!-- SCENE 1: WALL STREET (0.0s - 11.0s) -->
        <div class="scene" id="scene-1" style="display: flex;">
          <div class="myth-tag" style="background: #f59e0b; color: #000;">CATÁSTROFE FINANCIERA</div>
          <div class="headline-black">
            $440M EN 45 MINUTOS
          </div>
          <div class="punch-pill" style="background: #fef3c7; color: #92400e; border-color: #f59e0b;">
            1 VARIABLE BOOLEANA
          </div>
          <div class="metric-box">
            <div style="font-size: 32px; font-weight: 900; color: #b45309;">
              ⚡ 17% DE NYSE Y NASDAQ
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #64748b;">
              Knight Capital dominaba el trading algorítmico
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            La peor pesadilla de DevOps de la historia.
          </div>
        </div>

        <!-- SCENE 2: CÓDIGO ZOMBI (11.0s - 22.0s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">DEAD CODE DESASTRE</div>
          <div class="headline-black">
            FLAG POWERPEG (2003)
          </div>
          <div class="punch-pill" style="background: #000; color: #f87171; border-color: #ef4444;">
            REUTILIZACIÓN FATAL
          </div>
          <div class="metric-box" style="background: #fee2e2; border-color: #ef4444;">
            <div style="font-size: 30px; font-weight: 900; color: #b91c1c;">
              💀 CÓDIGO ZOMBI DE 9 AÑOS
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #991b1b;">
              Reutilizaron un flag viejo para una función nueva
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Nunca dejes código muerto en producción.
          </div>
        </div>

        <!-- SCENE 3: DESPLIEGUE MANUAL (22.0s - 34.0s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #7c3aed; color: #fff;">ERROR DE DEVOPS</div>
          <div class="headline-black">
            7 DE 8 SERVIDORES
          </div>
          <div class="punch-pill" style="background: #f3e8ff; color: #6b21a8; border-color: #7c3aed;">
            EL SERVIDOR OLVIDADO
          </div>
          <div class="metric-box" style="background: #faf5ff; border-color: #7c3aed;">
            <div style="font-size: 30px; font-weight: 900; color: #6b21a8;">
              🔄 BUCLE INFINITO A LAS 9:30 AM
            </div>
            <div style="font-size: 24px; font-weight: 700; color: #7c3aed;">
              Compraba al precio más alto y vendía al más bajo
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            4 millones de ejecuciones descontroladas.
          </div>
        </div>

        <!-- SCENE 4: 440 MILLONES (34.0s - 45.0s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">QUIEBRA EN 45 MINUTOS</div>
          <div class="headline-black">
            $10 MILLONES POR MINUTO
          </div>
          <div class="punch-pill" style="background: #fef2f2; color: #991b1b; font-size: 34px;">
            VENTA FORZOSA DE KNIGHT
          </div>
          <div class="final-pill">
            🎧 EPISODIO COMPLETO EN SPOTIFY
          </div>
          <div style="font-size: 26px; font-weight: 800; color: #b45309; margin-top: 14px;">
            Lee el reporte oficial de la SEC en sIA Journal
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
    print("📖 PASO 5: Registrando Knight Capital en sIA Journal...")
    print("="*70)
    
    build_mag_path = BASE_DIR / "build_magazine.py"
    content = build_mag_path.read_text(encoding='utf-8')
    
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'REELS_MAP = {',
            f'REELS_MAP = {{\n    "{EPISODE_FILENAME}": "{REEL_FILENAME}",'
        )
    
    res_entry = f'''    # sIA Corp 07 - Knight Capital $440M Bug - 4 de Noviembre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-corp-07-knight-capital-el-bug-de-440-millones-en-45-minutos",
        "category": "DevOps & Wall Street",
        "badge_color": "amber",
        "read_time": "14 min",
        "title": "sIA Corp #07: Knight Capital: $440 Millones Destruidos en 45 Minutos por Reutilizar un Flag Booleano",
        "subtitle": "El Mayor Desastre de DevOps en Wall Street: SMARS, Código Zombi PowerPeg, Despliegue Manual y la Caída de un Gigante Financiero.",
        "thesis": "La catástrofe de Knight Capital constituye el caso canónico de cómo la deuda técnica no gestionada, la reutilización imprudente de variables de configuración y la ausencia de despliegues automatizados e inmutables son capaces de aniquilar a un líder de mercado en menos de una hora, demostrando que la disciplina de entrega continua es un requisito existencial para la estabilidad financiera.",
        "nexo": "Séptimo episodio de Crónicas Corporativas: Alta frecuencia, DevOps, SEC, feature flags, arquitectura financiera y circuit breakers.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "type": "heading",
                "text": "1. 1 de Agosto de 2012: La Apertura del Abismo en Wall Street"
            }},
            {{
                "type": "paragraph",
                "text": "A las 9:30 AM del miércoles 1 de agosto de 2012, sonó la campana de apertura de la Bolsa de Valores de Nueva York (NYSE). En las pantallas de los operadores de Knight Capital Group —el principal creador de mercado de renta variable de Estados Unidos, responsable del 17% del volumen total del NYSE y del NASDAQ— comenzó una cascada incomprensible de alertas rojas."
            }},
            {{
                "type": "paragraph",
                "text": "En cuestión de segundos, los servidores del sistema SMARS (Smart Market Access Routing System) empezaron a emitir órdenes masivas a una velocidad inhumana. Para cuando los ingenieros lograron identificar la causa y apagar físicamente los servidores 45 minutos después, Knight había ejecutado más de 4 millones de transacciones por un total de 212 millones de acciones en 154 empresas cotizadas, acumulando una pérdida neta de 440 millones de dólares: casi 10 millones de dólares destruidos por cada minuto de operación."
            }},
            {{
                "type": "heading",
                "text": "2. PowerPeg: El Código Zombi que Nunca Murió"
            }},
            {{
                "type": "paragraph",
                "text": "Para comprender el origen de la falla, la Comisión de Bolsa y Valores de EE.UU. (SEC) tuvo que rastrear el árbol genealógico del software hasta 2003, nueve años atrás. En aquel entonces, los desarrolladores de Knight crearon una función de prueba interna denominada 'PowerPeg'. Su única finalidad era enviar órdenes acumuladas a mercado para medir la latencia y la capacidad de procesamiento de los enlaces de la bolsa sin verificar límites de precio."
            }},
            {{
                "type": "paragraph",
                "text": "PowerPeg fue diseñada como una herramienta temporal, pero nunca fue refactorizada ni eliminada de la base de código. Permaneció inerte dentro de los binarios en producción durante casi una década, silenciada únicamente por un flag de configuración booleano apagado. Este fenómeno, conocido en ingeniería de software como 'código muerto' o 'código zombi', representaba una bomba de tiempo lista para estallar ante cualquier colisión de configuración."
            }},
            {{
                "type": "heading",
                "text": "3. El Pecado de la Reutilización de Flags y el Despliegue Manual"
            }},
            {{
                "type": "paragraph",
                "text": "En julio de 2012, el NYSE anunció el lanzamiento del Retail Liquidity Program (RLP). Con una fecha límite estricta, el equipo de desarrollo de Knight modificó SMARS para adaptarse al nuevo protocolo de enrutamiento. En una decisión de diseño fatal, los ingenieros reutilizaron la variable de bandera interna que en 2003 controlaba la activación de PowerPeg, asignándole ahora el control del nuevo enrutador RLP."
            }},
            {{
                "type": "paragraph",
                "text": "El segundo fallo crítico ocurrió en el proceso de entrega. Knight no utilizaba pipelines automatizados de Integración y Despliegue Continuo (CI/CD), ni contenedores inmutables, ni políticas de verificación de firmas criptográficas. La noche previa al lanzamiento, un técnico de operaciones desplegó el software nuevo conectándose manualmente a cada uno de los ocho servidores del clúster de SMARS. Durante el proceso, el operador omitió involuntariamente el octavo servidor, dejándolo con la versión antigua del software de 2003."
            }},
            {{
                "type": "heading",
                "text": "4. La Tormenta Perfecta y el Bucle Infinito a Mercado"
            }},
            {{
                "type": "paragraph",
                "text": "A la apertura de la sesión, los ocho servidores recibieron la nueva configuración de producción con el flag habilitado. Los siete servidores que contaban con el nuevo código ejecutaron correctamente las órdenes de los clientes. Pero en el octavo servidor olvidado ocurrió el desastre: el código viejo interpretó el flag encendido como una instrucción imperativa de ejecutar PowerPeg al máximo rendimiento."
            }},
            {{
                "type": "paragraph",
                "text": "En lugar de verificar si la orden matriz ya había sido satisfecha, PowerPeg entró en un bucle recursivo infinito: fragmentaba cada orden de compra o venta en cientos de micro-órdenes a mercado, comprando al precio más alto disponible (Ask) y vendiendo al precio más bajo (Bid). Durante 45 minutos, el servidor absorbió vorazmente la liquidez de decenas de emisoras, provocando oscilaciones violentas en el mercado y vaciando el balance de capital regulatorio de la firma."
            }},
            {{
                "type": "heading",
                "text": "5. El Desplome, la Liquidación y las Leyes Sagradas de DevOps"
            }},
            {{
                "type": "paragraph",
                "text": "La pérdida de 440 millones de dólares evaporó las reservas de liquidez de Knight Capital. Sus acciones cayeron un 75% en dos días, pasando de 10.33 a menos de 2.50 dólares. Desesperada por evitar una quiebra forzosa que paralizara el mercado, la junta directiva aceptó una adquisición hostil de rescate por parte de Getco LLC a 1.50 dólares por acción, desmantelando la independencia de la mayor correduría de la época."
            }},
            {{
                "type": "paragraph",
                "text": "La investigación formal de la SEC (Release No. 70694) estableció precedentes regulatorios obligatorios para el sector tecnológico financiero que hoy rigen en toda la industria del software moderno: eliminación rigurosa de código muerto mediante herramientas de análisis estático, limitación temporal estricta para feature flags, automatización total e inmutable del despliegue (Infrastructure as Code), y la implementación obligatoria de interruptores de corte automático (Circuit Breakers) capaces de aislar nodos desbocados en milisegundos."
            }}
        ],
        "references": [
            "U.S. Securities and Exchange Commission (SEC). (2013). In the Matter of Knight Capital Americas LLC, Respondent (Administrative Proceeding File No. 3-15570, Release No. 70694). SEC Enforcement Publications.",
            "Popper, N. (2012). Knight Capital Says Trading Glitch Cost It $440 Million. The New York Times, DealBook.",
            "Phillips, M. (2012). The $440 Million Software Error at Knight Capital. Bloomberg Businessweek.",
            "Nygard, M. T. (2018). Release It!: Design and Deploy Production-Ready Software (2nd ed.). Pragmatic Bookshelf."
        ]
    }},'''
    
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'ARTICULOS_RESEARCH = {',
            f'ARTICULOS_RESEARCH = {{\n{res_entry}'
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print(f"✅ Registrado Knight Capital en build_magazine.py")
        
    cmd_build = ["python", "build_magazine.py"]
    subprocess.run(cmd_build, cwd=str(BASE_DIR), check=True)
    print("✅ Revista digital y artículos compilados con éxito.")

def main():
    print("="*70)
    print("🚀 PIPELINE COMPLETO DE PRODUCCIÓN: sIA Corp #07")
    print("   Knight Capital: $440 Millones en 45 Minutos por un Flag Reutilizado")
    print("="*70)
    
    step1_produce_full_audio()
    step2_produce_reel_audio()
    step3_prepare_stupy_composition()
    step4_render_hyperframes()
    step5_register_and_rebuild_magazine()
    
    print("\n" + "="*70)
    print("🎉 ¡PRODUCCIÓN 360° DE KNIGHT CAPITAL COMPLETADA CON ÉXITO!")
    print("="*70)

if __name__ == "__main__":
    main()
