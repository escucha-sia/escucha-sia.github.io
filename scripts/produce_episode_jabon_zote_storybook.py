import os
import sys
import math
import json
import shutil
import asyncio
import hashlib
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
ARTIFACT_DIR = Path(r"C:\Users\c_a_c\.gemini\antigravity\brain\3d3829e3-9423-4249-b4ec-672aaf684c20")
NODE_PATH = r"C:\Carlos\nodejs"

EPISODE_FILENAME = "sIA_Corp_08_Jabon_Zote_La_Corona_Ecatepec_2026-11-06.mp3"
REEL_FILENAME = "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"
REEL_POSTER_FILENAME = "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# Copy the 5 storybook illustrations into sia_tiktok_batch_engine/assets/
STORY_IMAGES = {
    "img1": ARTIFACT_DIR / "zote_scene1_banos_1920_1793967300165.jpg",
    "img2": ARTIFACT_DIR / "zote_scene2_ecatepec_plant_1793967309490.jpg",
    "img3": ARTIFACT_DIR / "zote_scene3_chemistry_bar_1793967319751.jpg",
    "img4": ARTIFACT_DIR / "zote_scene4_korea_fortress_1793967350896.jpg",
    "img5": ARTIFACT_DIR / "zote_scene5_omnicanal_car_1793967361709.jpg",
}

DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 1,
        "img": "assets/zote_img1.jpg",
        "tag": "CAPÍTULO 01 • PERALVILLO 1920",
        "headline": "LOS BAÑOS CORONA DE 1920",
        "pill": "DE TEPATITLÁN A LA CDMX",
        "caption_short": "En 1920, Don Esteban González Padilla y sus hermanos instalaron un cazo de cobre en unos viejos baños de vapor en Peralvillo.",
        "text": "¿Cómo una fábrica mexicana de jabón en Ecatepec logró derrotar a gigantes como Procter and Gamble y Unilever sin gastar un solo peso en publicidad televisiva? Bienvenidos a sIA Podcast. Hoy abrimos nuestro cuento ilustrado en 1920, cuando los hermanos Esteban, Loreto y Daniel González Padilla emigraron desde Tepatitlán, Jalisco, e instalaron su primer cazo de cobre dentro de unos antiguos baños públicos de vapor en el barrio de Peralvillo: los famosos Baños Corona."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 1,
        "img": "assets/zote_img1.jpg",
        "tag": "CAPÍTULO 01 • EL ORIGEN DEL NOMBRE",
        "headline": "EL BAUTIZO DEL BARRIO",
        "pill": "JABÓN DE MANTECA Y TEQUESQUITE",
        "caption_short": "La gente del barrio decía: 'Vamos a comprar jabón a La Corona', bautizando para siempre a la fábrica.",
        "text": "Así es, Jorge. En aquellos años postrevolucionarios escaseaban los productos básicos de higiene. Los hermanos cocinaban jabón artesanal mezclando sebo, manteca de cerdo y tequesquite. Como el taller no tenía letrero comercial y seguía pintado el rótulo de los antiguos baños, los vecinos decían: vamos a comprar jabón a La Corona. El propio pueblo bautizó uno de los imperios industriales más resilientes de América Latina."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 2,
        "img": "assets/zote_img2.jpg",
        "tag": "CAPÍTULO 02 • FORTALEZA ECATEPEC",
        "headline": "EL COLOSO DE XALOSTOC",
        "pill": "FERROCARRIL PROPIO + COGENERACIÓN",
        "caption_short": "Su megaplanta en Ecatepec tiene vías de tren propias, cogeneración eléctrica y refinería de glicerina farmacéutica.",
        "text": "Con las décadas, aquel taller se transformó en el coloso industrial de Xalostoc, en Ecatepec, Estado de México. A diferencia de las maquiladoras que dependen de proveedores externos, La Corona diseñó una fortaleza de integración vertical absoluta: espuelas de ferrocarril propias que entran directo a la planta, plantas de cogeneración eléctrica por turbinas de vapor y refinerías que extraen la glicerina de la saponificación para venderla con grado farmacéutico."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 2,
        "img": "assets/zote_img2.jpg",
        "tag": "CAPÍTULO 02 • ECONOMÍA CIRCULAR",
        "headline": "ROMA, FOCA Y ROSA VENUS",
        "pill": "AUTOSUFICIENCIA INDUSTRIAL",
        "caption_short": "Fabrican sus propios envases, procesan aceite 1-2-3 y producen detergentes biodegradables Roma y Foca.",
        "text": "Esa arquitectura industrial explica por qué sus costos son imposibles de igualar. Dentro del mismo complejo refinan el famoso aceite comestible Uno Dos Tres, soplan sus propios envases plásticos, imprimen sus envolturas y producen millones de bolsas de los detergentes biodegradables Roma y Foca, además del clásico jabón Rosa Venus."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 3,
        "img": "assets/zote_img3.jpg",
        "tag": "CAPÍTULO 03 • QUÍMICA DEL ZOTE (1970)",
        "headline": "LA FÓRMULA SECRETA ROSA",
        "pill": "400 GRAMOS • SEBO + ACEITE DE COCO",
        "caption_short": "Lanzado en 1970: un jabón-zote de 400g con 66% de ácidos grasos, aceite esencial de citronela y blanqueador óptico.",
        "text": "Pero la joya de la corona nació en 1970: el Jabón Zote. Un juego de palabras genial para describir un jabón grandote de cuatrocientos gramos. Su química es una obra maestra de formulación: sesenta y seis por ciento de ácidos grasos puros combinando sebo de res para dar dureza estructural y aceite de coco para generar espuma abundante incluso en aguas duras, perfumado con aceite esencial de citronela."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 3,
        "img": "assets/zote_img3.jpg",
        "tag": "CAPÍTULO 03 • BLANQUEADOR ÓPTICO",
        "headline": "FOTONES DE LUZ ULTRAVIOLETA",
        "pill": "EL SECRETO DEL BLANCO PERFECTO",
        "caption_short": "Sus blanqueadores ópticos absorben radiación UV invisible y la reemiten como luz azul, eliminando el tono amarillento.",
        "text": "Y tiene un truco óptico fascinante que casi nadie conoce: en lugar de usar cloro abrasivo que rompe las fibras de algodón, incorpora blanqueadores ópticos fluorescentes. Estas moléculas se adhieren a la tela, absorben la luz ultravioleta invisible del sol y la reflejan hacia el ojo humano como luz azul brillante, anulando el tono amarillento de la ropa blanca."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 4,
        "img": "assets/zote_img4.jpg",
        "tag": "CAPÍTULO 04 • DE MÉXICO A COREA DEL SUR",
        "headline": "0% MARKETING • 100% CULTO GLOBAL",
        "pill": "FUROR EN SEÚL Y RECHAZO A WALL STREET",
        "caption_short": "Sin comerciales en TV y sin deudas bancarias, Zote es artículo de culto en Corea del Sur y carnada de pesca en EE.UU.",
        "text": "Lo más sorprendente es su filosofía comercial: cero pesos en comerciales de televisión y cero deuda bancaria. Todo el ahorro publicitario se traslada directo al bolsillo de las familias mexicanas. Cuando gigantes de Wall Street intentaron comprar la fábrica con cheques en blanco, la familia respondió que una fuente de trabajo mexicana no está en venta. Y hoy, el Jabón Zote se vende como cosmético de culto en Corea del Sur para limpiar brochas de maquillaje y hasta como carnada de pesca para bagre en los ríos de Estados Unidos."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 5,
        "img": "assets/zote_img5.jpg",
        "tag": "CAPÍTULO 05 • ECOSISTEMA TRI-PLATAFORMA",
        "headline": "EN TU COCHE O EN VIDEO ILUSTRADO",
        "pill": "SPOTIFY • YOUTUBE • TIKTOK (@escucha_sia)",
        "caption_short": "🚗 Si vas en tu coche escúchanos en Spotify | 📱 Si quieres ver el cuento ilustrado míralo en YouTube y TikTok.",
        "text": "Recuerda que este episodio tiene el mismo formato completo en nuestras tres plataformas para acompañarte donde estés: si vas manejando en tu coche o en el tráfico, escúchanos manos libres en Spotify como sIA Podcast; y si quieres ver este cuento ilustrado con todas sus figuras y animaciones, míralo completo en YouTube y en TikTok en arroba escucha guion bajo sia."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 5,
        "img": "assets/zote_img5.jpg",
        "tag": "CAPÍTULO 05 • sIA JOURNAL",
        "headline": "INVESTIGACIÓN Y FUENTES APA",
        "pill": "ESCUCHA-SIA.GITHUB.IO",
        "caption_short": "Lee el análisis químico e industrial con referencias APA en escucha-sia.github.io. ¡Hasta la próxima!",
        "text": "Además, toda la investigación química e industrial con referencias académicas está disponible en nuestra revista digital escucha guion sia punto github punto io. Soy Jorge, junto a Dalia. ¡Gracias por escucharnos y vernos en sIA Podcast!"
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

def get_duration(file_path: Path) -> float:
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ], capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def get_audio_sha256(mp4_path: Path) -> str:
    res = subprocess.run([
        "ffmpeg", "-v", "error", "-i", str(mp4_path),
        "-map", "0:a:0", "-f", "wav", "-"
    ], capture_output=True, check=True)
    return hashlib.sha256(res.stdout).hexdigest()[:16]

def copy_storybook_images():
    assets_dir = ENGINE_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for idx, (k, src) in enumerate(STORY_IMAGES.items(), start=1):
        dst = assets_dir / f"zote_img{idx}.jpg"
        shutil.copy2(src, dst)
        print(f"  🖼️ Ilustración copiada: {dst.name}")

def step1_produce_unified_master_audio():
    print("\n" + "="*75)
    print("🎙️ PASO 1: Sintetizando Master Audio Unificado (Tamaño Estándar Spotify/TikTok/YouTube)...")
    print("="*75)

    temp_dir = BASE_DIR / "temp_audio_stupy_14_zote"
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_files = []
    durations = []
    for idx, item in enumerate(DIALOGUE):
        chunk_file = temp_dir / f"chunk_{idx:02d}_{item['speaker'].lower()}.mp3"
        if not (chunk_file.exists() and chunk_file.stat().st_size > 1000):
            print(f"  [{idx+1}/{len(DIALOGUE)}] Sintetizando voz de {item['speaker']}...")
            asyncio.run(synthesize_voice_segment(item["text"], item["voice"], chunk_file))
        chunk_files.append(chunk_file)
        dur = get_duration(chunk_file)
        durations.append(dur)
        print(f"    -> Segmento {idx+1} ({item['speaker']}): {dur:.2f}s")

    # Generate SRT and VTT subtitles
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
    scene_timings = []
    with open(srt_path, "w", encoding="utf-8") as fsrt, open(vtt_path, "w", encoding="utf-8") as fvtt:
        fvtt.write("WEBVTT\n\n")
        for i, (item, dur) in enumerate(zip(DIALOGUE, durations)):
            start_t = cur_time
            end_t = cur_time + dur
            fsrt.write(f"{i+1}\n{fmt_srt(start_t)} --> {fmt_srt(end_t)}\n{item['speaker']}: {item['text']}\n\n")
            fvtt.write(f"{i+1}\n{fmt_vtt(start_t)} --> {fmt_vtt(end_t)}\n{item['speaker']}: {item['text']}\n\n")
            scene_timings.append({
                "index": i,
                "start": round(start_t, 2),
                "end": round(end_t, 2),
                "speaker": item["speaker"],
                "chapter": item["chapter"],
                "img": item["img"],
                "tag": item["tag"],
                "headline": item["headline"],
                "pill": item["pill"],
                "caption": item["caption_short"]
            })
            cur_time = end_t

    concat_txt = temp_dir / "concat_master.txt"
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

    voice_dur = get_duration(raw_voice_master)
    total_dur = float(math.ceil(voice_dur + 2.0))
    fade_out_start = max(1.0, total_dur - 1.5)

    # Mix master audio with background music track and pad to total_dur
    final_master = AUDIO_DIR / EPISODE_FILENAME
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    music_track = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_voice_master),
        "-stream_loop", "-1", "-i", str(music_track),
        "-filter_complex",
        f"[1:a]volume=0.12,afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out_start:.1f}:d=1.5[bg];"
        f"[0:a]apad=whole_dur={total_dur:.1f}[vpad];"
        "[vpad][bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        f"[mixed]afade=t=out:st={fade_out_start:.1f}:d=1.5[faded];"
        "[faded]loudnorm=I=-16:LRA=10:TP=-1.5[norm]",
        "-map", "[norm]",
        "-ar", "44100", "-b:a", "192k",
        str(final_master)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Use the exact same master audio for the video engine!
    shutil.copy2(final_master, clip_audio)
    shutil.copy2(final_master, ENGINE_DIR / "assets" / "audio.mp3")
    SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
    if GDRIVE_AUDIO_DIR.exists():
        shutil.copy2(final_master, GDRIVE_AUDIO_DIR / EPISODE_FILENAME)

    print(f"✅ Master Audio Unificado listo: {final_master.name} | Duración={total_dur:.1f}s ({total_dur/60:.2f} min)")
    return total_dur, scene_timings

def step2_build_storybook_composition(total_dur: float, scene_timings: list):
    print("\n" + "="*75)
    print("🎨 PASO 2: Construyendo Composición de 'Cuento Ilustrado' (Storybook Motion)...")
    print("="*75)

    # Write engine index.html with full Spotify duration
    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>sIA Storybook #14 - Jabón Zote & La Corona</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #0f0514;
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
    <div id="root" data-composition-id="sia_storybook_14_zote" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
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

    # Build HTML cards for each of the 9 illustrated dialogue scenes
    scenes_html_parts = []
    for st in scene_timings:
        idx = st["index"]
        speaker_color = "#ec4899" if st["speaker"] == "DALIA" else "#06b6d4"
        speaker_badge = f"🎙️ {st['speaker']}"
        disp = "flex" if idx == 0 else "none"
        scenes_html_parts.append(f"""
        <div class="story-scene" id="scene-{idx}" style="display: {disp};">
          <div class="top-meta-row">
            <span class="chapter-tag">{st['tag']}</span>
            <span class="speaker-pill" style="background: {speaker_color};">{speaker_badge}</span>
          </div>

          <div class="illustration-frame">
            <img src="../{st['img']}" class="story-img" alt="Ilustración escena {idx+1}" />
            <div class="floating-badge">{st['pill']}</div>
          </div>

          <div class="story-text-box">
            <div class="story-headline">{st['headline']}</div>
            <div class="story-caption">“{st['caption']}”</div>
          </div>
        </div>""")

    scenes_joined = "\n".join(scenes_html_parts)
    timings_json = json.dumps(scene_timings, ensure_ascii=False)

    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Storybook 14 - Jabón Zote & Fábrica La Corona</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #0f0718;
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
        background-image: radial-gradient(#ec4899 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}

      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 76px;
        color: rgba(236, 72, 153, 0.06);
        text-transform: uppercase;
        transform: rotate(-10deg) scale(1.35);
        top: 22%;
        z-index: 0;
      }}

      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 64px 52px 84px 52px;
      }}

      .header-box {{
        display: flex;
        flex-direction: column;
        gap: 14px;
      }}

      .brand-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
      }}

      .brand-pill {{
        background: #ec4899;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 23px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.6);
        border: 2px solid #ffffff;
      }}

      .tag-pill {{
        background: rgba(6, 182, 212, 0.18);
        color: #22d3ee;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 20px;
        padding: 8px 18px;
        border-radius: 12px;
        border: 2px solid #06b6d4;
      }}

      .chapters-bar {{
        display: flex;
        gap: 8px;
        width: 100%;
      }}

      .chapter-pill {{
        flex: 1;
        padding: 10px 4px;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 13px;
        color: #94a3b8;
        text-transform: uppercase;
      }}

      .chapter-pill.active {{
        background: #ec4899;
        color: #ffffff;
        border-color: #f9a8d4;
        box-shadow: 0 0 18px rgba(236, 72, 153, 0.65);
        transform: scale(1.03);
      }}

      .storybook-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 34px 36px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.85), 0 0 40px rgba(236, 72, 153, 0.3);
        border: 6px solid #ec4899;
        min-height: 1280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      .story-scene {{
        display: none;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        gap: 20px;
      }}

      .top-meta-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
      }}

      .chapter-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 20px;
        color: #be185d;
        background: #fce7f3;
        padding: 8px 18px;
        border-radius: 10px;
        border: 2px solid #f472b6;
      }}

      .speaker-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 21px;
        color: #ffffff;
        padding: 8px 20px;
        border-radius: 999px;
      }}

      .illustration-frame {{
        position: relative;
        width: 100%;
        height: 760px;
        border-radius: 26px;
        overflow: hidden;
        border: 5px solid #0f172a;
        box-shadow: 0 18px 36px rgba(15, 23, 42, 0.25);
        background: #1e293b;
      }}

      .story-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        transform-origin: center center;
      }}

      .floating-badge {{
        position: absolute;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 23, 42, 0.92);
        color: #f472b6;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 10px 24px;
        border-radius: 14px;
        border: 2px solid #ec4899;
        white-space: nowrap;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
      }}

      .story-text-box {{
        background: #f8fafc;
        border: 3px solid #cbd5e1;
        border-radius: 24px;
        padding: 24px 28px;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }}

      .story-headline {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        color: #0f172a;
        line-height: 1.1;
        letter-spacing: -0.5px;
      }}

      .story-caption {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 27px;
        color: #334155;
        line-height: 1.32;
      }}

      .footer-badge {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
      }}

      .omnicanal-bar {{
        display: flex;
        gap: 16px;
        justify-content: center;
        width: 100%;
      }}

      .omni-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 18px;
        padding: 8px 16px;
        border-radius: 10px;
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

      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #ec4899 0%, #06b6d4 100%);
        width: 0%;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="bg-ticker">JABÓN ZOTE &bull; LA CORONA &bull; ECATEPEC &bull; 1920 &bull; MÉXICO</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🧼 sIA Crónicas #08</div>
          <div class="tag-pill">CUENTO ILUSTRADO</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill active" id="chap-1">01 Baños 1920</div>
          <div class="chapter-pill" id="chap-2">02 Ecatepec</div>
          <div class="chapter-pill" id="chap-3">03 Química Zote</div>
          <div class="chapter-pill" id="chap-4">04 Seúl & Wall St</div>
          <div class="chapter-pill" id="chap-5">05 Coche / Video</div>
        </div>
      </div>

      <div class="storybook-card">
        {scenes_joined}
      </div>

      <div class="footer-badge">
        <div class="omnicanal-bar">
          <span class="omni-pill">🚗 Coche: Spotify (sIA)</span>
          <span class="omni-pill">📱 Video: YouTube & TikTok (@escucha_sia)</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>

    <script>
      const SCENES = {timings_json};
      const TOTAL_DUR = {total_dur:.1f};

      function updateTimeline(time) {{
        let activeScene = SCENES[SCENES.length - 1];
        for (let i = 0; i < SCENES.length; i++) {{
          if (time >= SCENES[i].start && time < SCENES[i].end) {{
            activeScene = SCENES[i];
            break;
          }}
        }}

        for (let i = 0; i < SCENES.length; i++) {{
          const el = document.getElementById('scene-' + i);
          if (el) {{
            if (i === activeScene.index) {{
              el.style.display = 'flex';
              // Subtle Ken Burns zoom on the illustration
              const img = el.querySelector('.story-img');
              if (img) {{
                const segProgress = Math.min(1, Math.max(0, (time - activeScene.start) / Math.max(1, activeScene.end - activeScene.start)));
                const scale = 1.0 + (segProgress * 0.08);
                img.style.transform = 'scale(' + scale.toFixed(4) + ')';
              }}
            }} else {{
              el.style.display = 'none';
            }}
          }}
        }}

        for (let c = 1; c <= 5; c++) {{
          const chEl = document.getElementById('chap-' + c);
          if (chEl) {{
            if (c === activeScene.chapter) {{
              chEl.classList.add('active');
            }} else {{
              chEl.classList.remove('active');
            }}
          }}
        }}

        const pct = Math.min(100, Math.max(0, (time / TOTAL_DUR) * 100));
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
    scene_path.write_text(scene_html, encoding="utf-8")
    print(f"✅ Escena Storybook escrita en: {scene_path}")

def step3_render_hyperframes():
    print("\n" + "="*75)
    print("🎬 PASO 3: Renderizando Video Master Único (Cuento Ilustrado) con HyperFrames GPU...")
    print("="*75)

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
        raise RuntimeError(f"Error en HyperFrames: {res.stderr}")

    output_mp4 = renders_dir / "video.mp4"
    if not output_mp4.exists():
        candidates = list(renders_dir.glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)

    if not output_mp4.exists():
        raise RuntimeError("No se encontró video renderizado en renders/")

    target_reel = REELS_DIR / REEL_FILENAME
    shutil.copy2(output_mp4, target_reel)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_FILENAME)
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / REEL_FILENAME)

    dur = get_duration(target_reel)
    sha = get_audio_sha256(target_reel)
    size_mb = target_reel.stat().st_size / (1024 * 1024)
    print(f"✅ Video Master Único generado: {target_reel.name} | Duración={dur:.2f}s ({dur/60:.2f} min) | Tamaño={size_mb:.2f} MB | AudioSHA={sha}")

    poster_path = REELS_DIR / REEL_POSTER_FILENAME
    subprocess.run([
        "ffmpeg", "-y", "-ss", "00:00:05",
        "-i", str(target_reel),
        "-vframes", "1", "-q:v", "2",
        str(poster_path)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    copy_storybook_images()
    total_dur, scene_timings = step1_produce_unified_master_audio()
    step2_build_storybook_composition(total_dur, scene_timings)
    step3_render_hyperframes()
    print("\n🎉 ¡PRODUCCIÓN DEL PRIMER CUENTO ILUSTRADO TRI-PLATAFORMA COMPLETADA!")

if __name__ == "__main__":
    main()
