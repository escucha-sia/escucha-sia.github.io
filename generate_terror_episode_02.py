"""
sIA Terror #02: El Moderador del Turno Nocturno: Anomalías en la Cola de Revisión #7
- Cold Open inmersivo con tecleo mecánico de oficina vacía y estática digital.
- Presentación cálida y brújula de sIA (Jorge y Dalia) con drone nocturno.
- Opción 1: Los 3 Detalles Inquietantes de la Bitácora (Storytelling orgánico).
- Efectos de sonido (SFX): office_typing, digital_static, dark_drone, terminal_alert.
- Cápsula Fuera de la Burbuja: La realidad psicológica y algorítmica de la moderación.
- Cierre íntimo con comunidad nocturna ("Dulces pesadillas") y volante tripartito.
"""

import sys
import os
import re
import json
import asyncio
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = BASE_DIR / "audio"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
TEMP_DIR = BASE_DIR / "temp_chunks_terror_02"
SFX_DIR = BASE_DIR / "assets" / "sfx"
NEWS_VAULT = BASE_DIR / "news_vault.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
SFX_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

EPISODE_INFO = {
    "title": "sIA Terror #02: El Moderador del Turno Nocturno: Anomalías en la Cola de Revisión #7",
    "filename": "sIA_Terror_02_El_Moderador_Nocturno_Cola_7_2026-10-23.mp3",
    "description": "sIA Terror #02: El testimonio perturbador de un analista nocturno en Austin, Texas, asignado a la 'Cola 7' de moderación algorítmica. Un archivo sin origen clasificado con confianza cero y topología no humana, una cámara apuntando a su propia espalda, el reloj que corría en reversa y la entidad que aprendió a imitar sus parpadeos. Incluye diseño sonoro cinemático con SFX y análisis psicológico de la moderación digital. | Leer artículo y análisis técnico: https://escucha-sia.github.io/articulos/sia-terror-02-el-moderador-del-turno-nocturno.html"
}

SCRIPT_TERROR_02 = """
[CHAPTER: 01. Cold Open: La Señal de las 3:14 AM]
JORGE: Son las tres y catorce de la madrugada en un complejo corporativo en Austin, Texas. La planta de quinientos metros cuadrados está completamente a oscuras, salvo por el resplandor azul de una pantalla solitaria. En el monitor de un analista nocturno aparece una alerta que el sistema jamás debió generar: 'Archivo huérfano. Confianza del modelo: cero por ciento. Topología: no humana'. El video dura apenas seis segundos. Y cuando le da reproducir... la cámara está apuntando exactamente a su espalda.

[CHAPTER: 02. Prólogo & Brújula: sIA Terror]
DALIA: Hola, ¿cómo estás? Qué gusto saludarte esta noche. Mi nombre es Dalia...
JORGE: ... y yo soy Jorge. Te damos una cálida bienvenida a sIA.
DALIA: Para quienes se unen por primera vez o vienen de Spotify, YouTube o TikTok, te damos la bienvenida a nuestra casa. En sIA tenemos varias frecuencias: en nuestras Ediciones Diarias analizamos inteligencia artificial y código; en Crónicas Corporativas destapamos las guerras secretas de Silicon Valley... Pero hoy... hoy estás en sIA Terror: Crónicas de lo Inexplicable y Creepypastas del Mundo Digital.
JORGE: Aquí cerramos el laboratorio y nos adentramos en esos relatos que habitan en las esquinas más oscuras de internet: foros olvidados, servidores huérfanos y anomalías tecnológicas que la lógica formal no puede explicar.

[CHAPTER: 03. Los Tres Detalles de la Bitácora]
DALIA: El episodio de hoy se titula: 'El Moderador del Turno Nocturno: Anomalías en la Cola de Revisión Número Siete'. Jorge, cuando leí por primera vez este expediente rescatado de un foro de ciberseguridad, creí que era una simple leyenda urbana de programadores desvelados. Pero hay tres detalles en la bitácora de esa noche que hacen que se te hiele la sangre...
JORGE: El primero es la regla no escrita del contrato: si la pantalla parpadea en rojo a las tres de la mañana, sal de la sala y no mires atrás. El segundo, ese video huérfano donde el reloj de pared avanza al revés... mientras una sombra en el fondo empieza a copiar tus propios parpadeos. Y lo más perturbador, Dalia: lo que el equipo de limpieza encontró a la mañana siguiente frente al monitor.
DALIA: Exacto. Presta mucha atención a cómo se va cerrando el círculo...
JORGE: Ahora sí. Tómate un momento: apaga las luces de tu habitación. Si vas en el auto, mantén la vista en el camino. Ajusta bien tus audífonos, respira profundo... y acompáñanos a alcanzar lo que no existe en las sombras de la red.

[CHAPTER: 04. El Contrato de Austin y la Cola Número Siete]
DALIA: Octubre de dos mil veintidós. Carlos era un analista de datos de veintisiete años que aceptó un contrato de emergencia para una firma subcontratista de moderación en Texas. El sueldo duplicaba el promedio del mercado, pero el horario era demoledor: de once de la noche a siete de la mañana, en un edificio vidriado a las afueras de la ciudad.
JORGE: En esos centros trabajan cientos de personas de día revisando contenido reportado en redes sociales. Pero en el turno de la madrugada solo quedaban tres personas en todo el piso, separadas por mamparas aislantes. A Carlos le asignaron la 'Cola Siete'. En la jerga de la empresa, la Cola Siete era el pozo ciego del sistema: videos marcados por los algoritmos de visión computacional con un coeficiente de incertidumbre total. Metraje sin origen, sin cuenta de usuario asociada y sin metadatos de compresión.
DALIA: El supervisor le dio solo dos indicaciones antes de marcharse: 'Usa audífonos de diadema, pero jamás subas el volumen por encima del nivel cinco. Y si una transmisión tarda más de veinte segundos en cargar... dale al botón de purga y no intentes refrescar la memoria caché'.

[CHAPTER: 05. El Archivo Huérfano y el Ángulo Imposible]
JORGE: Durante las primeras tres semanas, la rutina fue tediosa: cámaras de seguridad de estacionamientos desiertos, transmisiones de televisores con estática y errores de sincronización de audio. Pero la madrugada del dieciocho de octubre, a las tres y catorce, el sistema emitió un pitido sordo y la pantalla parpadeó en un tono violeta oscuro.
DALIA: El archivo no tenía nombre; solo una cadena hexadecimal: 'cero equis siete f f'. La etiqueta decía: 'Confianza del modelo: cero punto cero cero por ciento. Clasificación: Topología no humana'. Carlos sintió un escalofrío en la nuca. Ajustó los audífonos y presionó la barra espaciadora para reproducir.
JORGE: El metraje duraba apenas seis segundos y se reproducía en bucle infinito. Mostraba una sala corporativa en penumbra, iluminada únicamente por la luz fría de un monitor de computadora. La toma estaba hecha desde lo alto de una mampara divisoria, en un ángulo picado... apuntando a la espalda de un hombre joven con sudadera gris y audífonos negros, sentado en una silla ergonómica.
DALIA: Carlos se quedó paralizado. La sudadera gris. Los audífonos negros. La botella de agua metálica en la esquina derecha del escritorio. No era un video de archivo: la cámara lo estaba enfocando a él, desde la mampara que estaba a sus espaldas, en ese preciso segundo.

[CHAPTER: 06. La Anomalía Temporal y el Reflejo que no Parpadea]
JORGE: Su primer instinto fue que se trataba de una novatada pesada de los otros dos operadores del turno. Se quitó los audífonos y volteó bruscamente hacia la mampara detrás de él. No había nadie. El pasillo estaba completamente oscuro y vacío. Solo el zumbido distante de los conductos de ventilación.
DALIA: Carlos volvió a mirar la pantalla... y fue ahí donde notó la primera anomalía imposible. En la esquina superior izquierda del video había un reloj digital de pared. Mientras que el reloj de su computadora marcaba las tres y quince con dieciocho segundos... el reloj en el video corría hacia atrás: quince, catorce, trece, doce...
JORGE: Quiso presionar la tecla de escape para purgar el búfer, pero el teclado no respondía. En los audífonos, a pesar de estar sobre el escritorio, comenzó a filtrarse un sonido de respiración pausada, lenta, casi congelada. Y en la pantalla, la figura en el video... dejó de seguir sus movimientos. Carlos estaba inmóvil, petrificado del pavor. Pero la figura en el monitor giró lentamente la cabeza ciento ochenta grados... mirándolo directamente a través del cristal.

[CHAPTER: 07. La Puerta Bloqueada y la Huella Térmica]
DALIA: El pánico se apoderó de él. Carlos tiró la silla hacia atrás, corrió hacia la salida de emergencia del piso y tecleó su código de cuatro dígitos en el panel de control. La cerradura magnética emitió un zumbido agudo y la pantalla LED mostró una sola palabra en letras rojas: 'BLOQUEO DE CUARENTENA: USUARIO NO LOCALIZADO'.
JORGE: La temperatura en la sala bajó abruptamente. El termostato digital marcaba ocho grados centígrados, y el vaho de su propia respiración se hacía visible en el aire. Desde la oscuridad del cubículo que acababa de abandonar, se escuchó el 'clic, clic, clic' pausado de las teclas mecánicas... alguien estaba escribiendo en su terminal.
DALIA: A las siete de la mañana, cuando llegó el relevo del turno diurno junto con el personal de limpieza, encontraron la puerta de seguridad entreabierta. La silla de Carlos estaba en el suelo. Su teléfono celular, su cartera y sus llaves estaban ordenados sobre el escritorio.
JORGE: Pero Carlos no estaba en el edificio. Los guardias revisaron las cámaras del perímetro: nadie había salido por ninguna de las puertas exteriores. En la terminal de la Cola Siete había una sola línea de comandos abierta con un mensaje parpadeante: 'Revisión completada. Entidad indexada en el núcleo del clúster'.

[CHAPTER: 08. 🌌 Fuera de la Burbuja: La Frontera entre la IA y el Aislamiento]
DALIA: Entremos a nuestra cápsula Fuera de la Burbuja, porque este testimonio, más allá del estremecimiento que provoca, toca una herida muy real de la tecnología moderna: la invisibilidad de la moderación algorítmica.
JORGE: Miles de personas en todo el mundo trabajan de madrugada en condiciones de privación sensorial extrema, expuestas a lo peor del comportamiento humano y a fallos de visión computacional. Cuando un modelo convolucional se enfrenta a ruido puro o artefactos de compresión, sufre lo que los investigadores llaman pareidolia artificial: inventa geometrías, busca rostros donde solo hay estática y genera bucles de retroalimentación que pueden alterar la percepción psicológica del observador.
DALIA: La policía de Austin cerró el caso meses después catalogándolo como desaparición voluntaria. Sin embargo, los operadores que ocuparon esa sala en las semanas siguientes reportaron un detalle que la empresa nunca pudo desmentir: cada vez que el reloj marca las tres y catorce de la madrugada, los monitores de la Cola Siete reflejan en el cristal negro la silueta de alguien con sudadera gris... que jamás parpadea.

[CHAPTER: 09. Cierre Íntimo & Dulces Pesadillas]
JORGE: Si quieres consultar los reportes técnicos sobre alucinaciones de visión artificial y el análisis completo de este caso, entra a nuestra revista digital en escucha guion sia punto github punto io. Y en nuestro TikTok y YouTube Shorts ya tienes disponible el Reel de cuarenta y cinco segundos con la reconstrucción visual de la Cola Siete.
DALIA: Gracias por acompañarnos y ser parte de nuestra comunidad nocturna en este segundo episodio de sIA Terror. Te deseamos una noche tranquila... apaga tus pantallas con cuidado. Buenas noches...
JORGE: ... y dulces pesadillas.
"""

def clean_for_tts(text: str) -> str:
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    # Pronunciación fonética de la marca sIA -> 'Sia' (una sola palabra fluida)
    t = re.sub(r'\bsIA\b', 'Sia', t)
    t = re.sub(r'\bSIA\b', 'Sia', t)
    t = re.sub(r'\bIP\b', 'I P', t)
    t = re.sub(r'\bLED\b', 'L E D', t)
    t = re.sub(r'\bAI\b', 'A I', t)
    t = re.sub(r'\bIA\b', 'I A', t)
    return t

async def synthesize_chunk(text: str, voice: str, output_path: Path):
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_path))
            return
        except Exception as e:
            if attempt == 4:
                raise e
            await asyncio.sleep(1.0 + attempt * 1.5)

def get_duration(audio_file: Path) -> float:
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_file)]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 2.0

def mix_background(voice_file: Path, bg_file: Path, output_file: Path, bg_volume: float = 0.20):
    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_file),
        "-i", str(bg_file),
        "-filter_complex", f"[1:a]volume={bg_volume}[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=1[out]",
        "-map", "[out]",
        str(output_file)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

async def produce_episode():
    print("=" * 75)
    print("🎙️ PRODUCCIÓN CINEMÁTICA: sIA TERROR #02 (CON EFECTOS DE SONIDO SFX)")
    print("=" * 75)

    # 1. Limpiar carpeta temporal
    for f in TEMP_DIR.glob("*"):
        try:
            f.unlink()
        except Exception:
            pass

    # 2. Parsear el guion
    lines = SCRIPT_TERROR_02.strip().split('\n')
    dialogue_blocks = []
    current_chapter = "01. Cold Open: La Señal de las 3:14 AM"
    current_speaker = None
    current_text = []

    def commit_block():
        nonlocal current_speaker, current_text
        if current_speaker and current_text:
            text_str = " ".join(current_text).strip()
            if text_str:
                voice = VOICE_MALE if current_speaker == "JORGE" else VOICE_FEMALE
                dialogue_blocks.append({
                    "speaker": current_speaker,
                    "text": clean_for_tts(text_str),
                    "raw_text": text_str,
                    "voice": voice,
                    "chapter": current_chapter
                })
            current_speaker = None
            current_text = []

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        ch_match = re.match(r'^\[CHAPTER:\s*(.*?)\]', line_s, re.IGNORECASE)
        if ch_match:
            commit_block()
            current_chapter = ch_match.group(1).strip()
            continue
        j_match = re.match(r'^JORGE\s*:\s*(.*)$', line_s, re.IGNORECASE)
        d_match = re.match(r'^DALIA\s*:\s*(.*)$', line_s, re.IGNORECASE)
        if j_match:
            commit_block()
            current_speaker = "JORGE"
            current_text = [j_match.group(1)]
        elif d_match:
            commit_block()
            current_speaker = "DALIA"
            current_text = [d_match.group(1)]
        else:
            if current_speaker:
                current_text.append(line_s)

    commit_block()

    print(f"Sintetizando {len(dialogue_blocks)} bloques vocales con Edge-TTS...")
    for idx, block in enumerate(dialogue_blocks):
        raw_p = TEMP_DIR / f"raw_{idx:03d}_{block['speaker'].lower()}.mp3"
        await synthesize_chunk(block["text"], block["voice"], raw_p)
        block["raw_audio"] = raw_p
        print(f"  [{idx+1}/{len(dialogue_blocks)}] Voz generada ({block['speaker']}): {raw_p.name}")

    # 3. Aplicar capas de diseño sonoro y SFX
    print("\n🎛️ Aplicando capas de diseño sonoro cinemático (SFX & Ambient Beds)...")
    sfx_typing = SFX_DIR / "office_typing.mp3"
    sfx_static = SFX_DIR / "digital_static.mp3"
    sfx_drone = SFX_DIR / "dark_drone.mp3"
    sfx_alert = SFX_DIR / "terminal_alert.mp3"

    timeline_items = []
    
    # Bloque 0: Cold Open con Teclado de oficina y zumbido de fondo
    b0 = dialogue_blocks[0]
    mixed_b0 = TEMP_DIR / "processed_000_cold_open.mp3"
    mix_background(b0["raw_audio"], sfx_typing, mixed_b0, bg_volume=0.25)
    timeline_items.append((mixed_b0, b0["raw_text"], b0["speaker"], b0["chapter"]))

    # Transición SFX: Estática digital entre Cold Open y Presentación
    static_chunk = TEMP_DIR / "sfx_transition_static.mp3"
    shutil.copy2(sfx_static, static_chunk)
    timeline_items.append((static_chunk, None, None, b0["chapter"]))

    # Bloques 1 a 4: Presentación cálida, Brújula y Los 3 Detalles de la Bitácora
    # Mezclados sutilmente con dark_drone de fondo (-22 dB / 0.08 vol)
    for i in range(1, 5):
        b = dialogue_blocks[i]
        mixed_b = TEMP_DIR / f"processed_{i:03d}_intro_bed.mp3"
        mix_background(b["raw_audio"], sfx_drone, mixed_b, bg_volume=0.08)
        timeline_items.append((mixed_b, b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 5 a 7: El Contrato de Austin y el inicio de la historia
    for i in range(5, 8):
        b = dialogue_blocks[i]
        timeline_items.append((b["raw_audio"], b["raw_text"], b["speaker"], b["chapter"]))

    # SFX: Terminal Alert justo antes de la llegada del archivo huérfano (bloque 8)
    alert_chunk = TEMP_DIR / "sfx_alert_terminal.mp3"
    shutil.copy2(sfx_alert, alert_chunk)
    timeline_items.append((alert_chunk, None, None, dialogue_blocks[8]["chapter"]))

    # Bloques 8 a 17: Relato inmersivo y Clímax
    for i in range(8, 18):
        b = dialogue_blocks[i]
        timeline_items.append((b["raw_audio"], b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 18 a 20: Cápsula Fuera de la Burbuja
    for i in range(18, 21):
        b = dialogue_blocks[i]
        timeline_items.append((b["raw_audio"], b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 21 a 23: Cierre íntimo con comunidad y drone sutil de despedida
    for i in range(21, len(dialogue_blocks)):
        b = dialogue_blocks[i]
        mixed_cierre = TEMP_DIR / f"processed_{i:03d}_cierre_bed.mp3"
        mix_background(b["raw_audio"], sfx_drone, mixed_cierre, bg_volume=0.08)
        timeline_items.append((mixed_cierre, b["raw_text"], b["speaker"], b["chapter"]))

    # 4. Construir concatenación y subtítulos sincronizados
    print("\nCalculando duraciones exactas y generando subtítulos WebVTT / SRT...")
    vtt_lines = ["WEBVTT\nKind: captions\nLanguage: es\n\n"]
    srt_lines = []
    srt_idx = 1
    chapter_spans = []
    current_ch = None
    ch_start_ms = 0
    current_time_ms = 0

    def fmt_vtt(ms: int) -> str:
        h, rem = divmod(ms, 3600000)
        m, rem = divmod(rem, 60000)
        s, millis = divmod(rem, 1000)
        return f"{h:02d}:{m:02d}:{s:02d}.{millis:03d}"

    def fmt_srt(ms: int) -> str:
        h, rem = divmod(ms, 3600000)
        m, rem = divmod(rem, 60000)
        s, millis = divmod(rem, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{millis:03d}"

    concat_file = TEMP_DIR / "concat_list.txt"
    with open(concat_file, 'w', encoding='utf-8') as f:
        for audio_path, text, speaker, ch_name in timeline_items:
            path_str = str(audio_path).replace('\\', '/')
            f.write(f"file '{path_str}'\n")

            dur_sec = get_duration(audio_path)
            dur_ms = int(dur_sec * 1000)

            chunk_s = current_time_ms
            chunk_e = current_time_ms + dur_ms

            if text and speaker:
                vtt_lines.append(f"{fmt_vtt(chunk_s)} --> {fmt_vtt(chunk_e)}\n{speaker}: {text}\n\n")
                srt_lines.append(f"{srt_idx}\n{fmt_srt(chunk_s)} --> {fmt_srt(chunk_e)}\n{speaker}: {text}\n\n")
                srt_idx += 1

            if ch_name != current_ch:
                if current_ch is not None:
                    chapter_spans.append((current_ch, ch_start_ms, current_time_ms))
                current_ch = ch_name
                ch_start_ms = current_time_ms

            current_time_ms += dur_ms

    if current_ch is not None:
        chapter_spans.append((current_ch, ch_start_ms, current_time_ms))

    # Guardar metadatos de capítulos
    meta_lines = [
        ";FFMETADATA1\n",
        f"title={EPISODE_INFO['title']}\n",
        "artist=Jorge y Dalia (sIA Terror)\n",
        "album=sIA Terror\n",
        "genre=Horror Podcast\n",
        f"date={datetime.now().strftime('%Y')}\n\n"
    ]
    for ch_title, s_ms, e_ms in chapter_spans:
        meta_lines.append(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={s_ms}\nEND={e_ms}\ntitle={ch_title}\n\n")

    meta_file = TEMP_DIR / "chapters_metadata.txt"
    meta_file.write_text("".join(meta_lines), encoding='utf-8')

    # Subtítulos
    base_stem = Path(EPISODE_INFO["filename"]).stem
    vtt_path = AUDIO_DIR / f"{base_stem}.vtt"
    srt_path = AUDIO_DIR / f"{base_stem}.srt"
    vtt_path.write_text("".join(vtt_lines), encoding='utf-8')
    srt_path.write_text("".join(srt_lines), encoding='utf-8')

    shutil.copy2(vtt_path, SPOTIFY_DIR / f"{base_stem}.vtt")
    shutil.copy2(srt_path, SPOTIFY_DIR / f"{base_stem}.srt")
    print(f"✅ Subtítulos VTT y SRT generados y replicados en {SPOTIFY_DIR}")

    # Ensamble final con ffmpeg
    final_output = AUDIO_DIR / EPISODE_INFO["filename"]
    spotify_output = SPOTIFY_DIR / EPISODE_INFO["filename"]

    print("\n🎬 Ensamblando master final de audio con ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-i", str(meta_file),
        "-map_metadata", "1",
        "-c:a", "libmp3lame",
        "-q:a", "2",
        str(final_output)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.copy2(final_output, spotify_output)

    total_sec = get_duration(final_output)
    size_bytes = final_output.stat().st_size
    print(f"✅ Master MP3 generado con éxito: {final_output}")
    print(f"   Duración total: {int(total_sec // 60)}m {int(total_sec % 60)}s | Tamaño: {size_bytes / (1024*1024):.2f} MB")
    print(f"   Replicado a Spotify: {spotify_output}")

    # 5. Actualizar RSS podcast.xml y audio/podcast.xml
    update_rss_feed(final_output, size_bytes, int(total_sec), vtt_path, srt_path)

    # 6. Registrar en el archivo de memoria news_vault.json
    log_to_news_vault()

def update_rss_feed(audio_file: Path, size_bytes: int, duration_sec: int, vtt_file: Path, srt_file: Path):
    print("\nActualizando feed RSS podcast.xml...")
    pub_date = datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    m, s = divmod(duration_sec, 60)
    dur_str = f"{m:02d}:{s:02d}"

    audio_url = f"https://escucha-sia.github.io/audio/{audio_file.name}"
    vtt_url = f"https://escucha-sia.github.io/audio/{vtt_file.name}"
    srt_url = f"https://escucha-sia.github.io/audio/{srt_file.name}"

    item_xml = f"""    <item>
      <title>{EPISODE_INFO['title']}</title>
      <description><![CDATA[{EPISODE_INFO['description']}]]></description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}" length="{size_bytes}" type="audio/mpeg"/>
      <guid isPermaLink="false">sia-terror-02-moderador-nocturno-cola-7</guid>
      <itunes:duration>{dur_str}</itunes:duration>
      <itunes:explicit>no</itunes:explicit>
      <itunes:episodeType>full</itunes:episodeType>
      <podcast:transcript url="{vtt_url}" type="text/vtt" language="es"/>
      <podcast:transcript url="{srt_url}" type="application/x-subrip" language="es"/>
    </item>
"""
    for feed_path in [BASE_DIR / "podcast.xml", BASE_DIR / "audio" / "podcast.xml"]:
        if feed_path.exists():
            content = feed_path.read_text(encoding='utf-8')
            if EPISODE_INFO['title'] not in content:
                # Insertar como el primer item después de <channel>
                pos = content.find("<item>")
                if pos != -1:
                    new_content = content[:pos] + item_xml + content[pos:]
                    feed_path.write_text(new_content, encoding='utf-8')
                    print(f"  -> Añadido a {feed_path}")

def log_to_news_vault():
    vault_data = {"covered_items": []}
    if NEWS_VAULT.exists():
        try:
            vault_data = json.loads(NEWS_VAULT.read_text(encoding='utf-8'))
        except Exception:
            pass
    vault_data["covered_items"].append({
        "title": EPISODE_INFO["title"],
        "filename": EPISODE_INFO["filename"],
        "topics": [
            "sIA Terror #02: El moderador del turno nocturno en Austin Texas",
            "La Cola 7 de moderación: archivos huérfanos con topología no humana",
            "Anomalía temporal: el reloj que avanza en reversa y la copia de movimientos",
            "Puerta de cuarentena magnética y la terminal activa en la sala vacía",
            "Fuera de la Burbuja: La realidad del aislamiento de moderadores y pareidolia algorítmica"
        ],
        "cooldown_days": 45,
        "date": datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro de memoria añadido a news_vault.json.")

if __name__ == '__main__':
    asyncio.run(produce_episode())
