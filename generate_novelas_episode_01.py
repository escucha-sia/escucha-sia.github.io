"""
sIA Novelas #01: Omniscient Reader's Viewpoint: La Novela que Salvó la Vida de un Lector Solitario en el Metro de Seúl
- Enfoque Humano y Técnico: La metaficción de las webnovels coreanas, el pacto invisible entre autor y lector, y la soledad urbana contemporánea.
- Diseño Sonoro de Estudio: Piano emocional (Kevin MacLeod - Isolated), acústica de sala y tecleo Keychron sutil.
- Masterización Broadcast EBU R128 (-16 LUFS) y compresión dinámica: volumen calibrado.
- Subtítulos Podcasting 2.0 (.vtt y .srt) sincronizados.
- Registro en podcast.xml, audio/podcast.xml, build_magazine.py y news_vault.json.
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
TEMP_DIR = BASE_DIR / "temp_chunks_novelas_01"
AUDIO_LIB = BASE_DIR / "assets" / "audio_library"
NEWS_VAULT = BASE_DIR / "news_vault.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

EPISODE_INFO = {
    "title": "sIA Novelas #01: Omniscient Reader's Viewpoint: La Novela que Salvó la Vida de un Lector Solitario en el Metro de Seúl",
    "filename": "sIA_Novelas_01_Omniscient_Reader_Viewpoint_2026-10-24.mp3",
    "description": "sIA Novelas #01: El fenómeno literario de las webnovels coreanas y la arquitectura de la metaficción. La historia de Kim Dokja, un oficinista anónimo que sobrevivió a la depresión leyendo cada noche en el metro un manuscrito ignorado por todos, el pacto íntimo entre quien escribe en soledad y quien lee para no rendirse, y cómo Omniscient Reader's Viewpoint se convirtió en la mayor carta de amor a la lectura de nuestra generación. | Leer artículo y análisis narrativo APA: https://escucha-sia.github.io/articulos/sia-novelas-01-omniscient-reader-viewpoint-metaficcion.html"
}

SCRIPT_NOVELAS_01 = """
[CHAPTER: 01. Cold Open: La Línea Tres del Metro de Seúl]
DALIA: Son las siete de la noche en la Línea Tres del metro de Seúl. El vagón va repleto de hombres y mujeres de traje oscuro con la mirada perdida en las pantallas de sus teléfonos, agotados tras jornadas de doce horas en oficinas corporativas. Entre ellos viaja Kim Dokja, un joven de veintiocho años con un contrato temporal en una empresa de videojuegos. Dokja no tiene amigos cercanos, no tiene ahorros ni una familia que lo espere en casa. En coreano, su nombre significa dos cosas: 'hijo único'... y también significa 'lector'. Durante diez años enteros, desde que era un adolescente acosado en la escuela, Dokja sobrevivió a la depresión gracias a un único ritual cotidiano: abrir una aplicación de novelas digitales a las siete en punto para leer una historia interminable titulada 'Tres formas de sobrevivir en un mundo en ruinas'. La novela tenía más de tres mil capítulos, una trama repetitiva y exactamente un solo lector activo en todo el planeta: él. Pero esa noche, tras publicar el epílogo final, el autor misterioso le envía un mensaje privado que cambiará la realidad: 'Gracias a ti, esta historia pudo llegar hasta el final'.

[CHAPTER: 02. Prólogo & Brújula: sIA Novelas]
JORGE: Hola, ¿cómo estás? Qué alegría saludarte. Mi nombre es Jorge...
DALIA: ... y yo soy Dalia. Te damos una cálida bienvenida a Sia.
JORGE: Hoy inauguramos una nueva estación en nuestro viaje: sIA Novelas, arquitectura de mundos. Si creías que las novelas ligeras y las webnovels digitales eran solo entretenimiento adolescente o clichés de reencarnación, en este espacio vamos a desmontar ese mito. En Sia exploramos la ingeniería de los sistemas narrativos: cómo se construyen universos fantásticos coherentes, la psicología del lector moderno y el impacto social de plataformas como Munpia, Kakao y Naver, que han revolucionado la literatura global desde los teléfonos móviles.
DALIA: Y para abrir esta puerta, no podíamos elegir otra obra que no fuera el hito más brillante y conmovedor de la narrativa coreana moderna: Omniscient Reader's Viewpoint, escrita por el dúo de autores anónimos sing N song. Una novela que no solo rompió récords con cientos de millones de lecturas, sino que construyó la declaración de amor más profunda jamás escrita hacia el acto solitario de leer.

[CHAPTER: 03. Los Tres Momentos de la Bitácora]
JORGE: Cuando analizas Omniscient Reader, descubres que su genialidad no está en los monstruos ni en los combates; está en cómo convierte la relación entre autor, protagonista y lector en un triángulo existencial. Para acompañarnos en esta travesía, fíjate en estos tres momentos clave: Primero: El auge de las webnovels coreanas y la soledad del oficinista. Cómo la literatura capitulada diaria sustituyó a las bibliotecas tradicionales en las metrópolis asiáticas. Segundo: La metaficción de la supervivencia. Por qué Kim Dokja no sobrevive al apocalipsis por ser el más fuerte, sino por ser el único que comprendió el dolor de los personajes leyendo hasta la última página. Y tercero: El pacto del autor y el lector. La revelación de por qué escribir una historia para una sola persona puede ser suficiente para salvar una vida en el mundo real.
DALIA: Ponte cómodo, ponte tus audífonos, respira profundo... y acompáñanos a subir al tren de Seúl.

[CHAPTER: 04. La Revolución de las Webnovels y la Soledad Urbana]
DALIA: Para entender el impacto de Omniscient Reader, primero hay que entender cómo lee la sociedad contemporánea. En Seúl, Tokio o Ciudad de México, el ritmo de vida moderno destruyó el hábito de sentarse durante horas con un libro pesado en la sala. La gente lee de pie, tambaleándose en el transporte público, esperando el cambio de semáforo o comiendo sola en una tienda de conveniencia.
JORGE: Las plataformas coreanas como Munpia entendieron esa realidad y crearon un modelo editorial radical: novelas serializadas que publican un capítulo diario de unas mil quinientas palabras a una hora fija. Cuesta apenas unos centavos desbloquear un capítulo. Pero lo revolucionario es la inmediatez: al final de cada texto hay una sección de comentarios en tiempo real donde los lectores debaten teorías, critican decisiones o simplemente le agradecen al autor por acompañarlos un día más.
DALIA: Los autores de Omniscient Reader —un matrimonio que firma bajo el seudónimo sing N song— vivieron esa realidad en carne propia. Escribían desde un modesto departamento, enfrentando el agotamiento y la ansiedad creativa. Y plasmaron esa vivencia en su protagonista: Kim Dokja es el reflejo de millones de jóvenes urbanos que sienten que la sociedad los ha dejado atrás, personas para quienes la ficción no es una simple distracción, sino el único refugio cálido donde pueden sentirse comprendidos.

[CHAPTER: 05. La Metaficción: El Lector como Protagonista]
JORGE: La premisa de la novela arranca cuando el mundo real colapsa y se convierte en el escenario apocalíptico de la novela que Dokja leía. Aparecen criaturas míticas y constelaciones estelares que transmiten el sufrimiento humano como si fuera un reality show cósmico. Pero aquí ocurre la gran subversión del género.
DALIA: En cualquier historia convencional, el héroe es un guerrero con fuerza sobrehumana o un genio mágico. En este universo, el personaje principal original se llama Yoo Joonghyuk: un hombre destinado a regresar en el tiempo cada vez que muere, acumulando siglos de traumas, pérdida y desesperación en un ciclo eterno. Pero Yoo Joonghyuk no es quien salva el mundo. Quien lo salva es Kim Dokja.
JORGE: ¿Y cuál es el superpoder de Kim Dokja? El Punto de Vista del Lector Omnisciente. Dokja no tiene fuerza física descomunal; tiene la memoria de haber leído cada tropiezo, cada lágrima y cada secreto de los personajes durante diez años. Es una metáfora literaria deslumbrante: el lector no es un observador pasivo que mira desde afuera; el lector es quien le da sentido a la historia. Sin alguien que lea las penurias de un personaje, el sufrimiento de ese héroe no existe en ninguna parte. Dokja sobrevive porque es el único que verdaderamente ama a los personajes más allá del texto.

[CHAPTER: 06. El Pacto Invisible: Salvar una Vida con una Historia]
DALIA: Hacia el tramo final de la obra, sing N song desvela el misterio más conmovedor de toda la trama: ¿quién era el autor anónimo que escribió más de tres mil capítulos sin cobrar un solo centavo y sin tener lectores?
JORGE: La respuesta es un nudo en la garganta. La historia fue escrita específicamente para Kim Dokja. En una paradoja temporal y emocional sublime, descubrimos que el autor continuó escribiendo noche tras noche porque sabía que si dejaba de publicar un solo día, aquel joven solitario en el metro de Seúl perdería la última razón que le quedaba para no quitarse la vida. El texto existía para mantenerlo con vida, y Dokja vivía para leer el texto.
DALIA: Esa es la tesis suprema de Omniscient Reader: el pacto invisible entre quien escribe y quien lee. Cuando un autor se sienta solo frente al teclado a las dos de la mañana, no sabe quién, al otro lado de una pantalla a miles de kilómetros de distancia, está encontrando consuelo en sus palabras. Una historia puede ser defectuosa, puede tener errores de ritmo o ser rechazada por los críticos literarios; pero si logró que una sola persona decidiera resistir hasta el día siguiente, esa historia ha cumplido el propósito más sagrado del arte humano.

[CHAPTER: 07. 🌌 Fuera de la Burbuja: La Arquitectura del Webtoon y la Progresión]
JORGE: Entremos a nuestra cápsula Fuera de la Burbuja para analizar cómo esta novela redefinió la narrativa transmedia global.
DALIA: Tras conquistar las plataformas de texto, Omniscient Reader fue adaptada al formato de webtoon vertical con arte del estudio Redice. El éxito fue tan descomunal que superó los trescientos millones de lecturas globales, demostrando que la estructura de niveles, habilidades cuantificadas y escenarios tipo videojuego no abaratan la literatura, sino que crean un nuevo lenguaje visual perfectamente adaptado a la psicología de la era digital.
JORGE: Sing N song demostró a los escritores de todo el mundo que se puede combinar la adrenalina de los sistemas mágicos de progresión con dilemas morales sobre el libre albedrío, la culpa del superviviente y el duelo. Hoy en día, la obra está en camino a convertirse en una superproducción cinematográfica de acción real y en serie de animación, llevando la voz de aquel lector solitario del metro a cada rincón del planeta.

[CHAPTER: 08. Cierre Íntimo & Comunidad]
DALIA: Omniscient Reader's Viewpoint nos recuerda que todos nosotros, en algún momento oscuro de nuestra vida, hemos sido Kim Dokja: buscando desesperadamente entre las páginas de un libro o los minutos de un podcast una voz que nos diga que nuestra existencia importa.
JORGE: Si deseas leer nuestro ensayo completo sobre la metaficción en las webnovels coreanas y revisar la bibliografía académica sobre narrativa digital en formato APA, visita nuestra revista en escucha guion sia punto github punto io.
DALIA: Muchísimas gracias por acompañarnos en esta inauguración de sIA Novelas. Cuéntanos en los comentarios qué historia o libro te salvó la vida en un momento difícil y qué otra gran novela te gustaría que desglosemos. Que tengas una noche reconfortante y serena... y nos escuchamos en la próxima entrega de Sia.
JORGE: Hasta la próxima.
"""

def clean_for_tts(text: str) -> str:
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    t = re.sub(r'\bsIA\b', 'Sia', t)
    t = re.sub(r'\bSIA\b', 'Sia', t)
    t = re.sub(r'\bKim Dokja\b', 'Kim Dok-ya', t)
    t = re.sub(r'\bDokja\b', 'Dok-ya', t)
    t = re.sub(r'\bYoo Joonghyuk\b', 'Yu Yung-jiuk', t)
    t = re.sub(r'\bsing N song\b', 'Sing and Song', t)
    t = re.sub(r'\bMunpia\b', 'Mun-pía', t)
    t = re.sub(r'\bNaver\b', 'Néiver', t)
    t = re.sub(r'\bwebtoons?\b', 'güebtún', t)
    t = re.sub(r'\bwebnovels?\b', 'güeb-nóvel', t)
    return t

def parse_script(raw_text: str):
    chapters = []
    dialogues = []
    lines = raw_text.strip().split('\n')
    current_chapter = "Introducción"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('[CHAPTER:'):
            current_chapter = line.replace('[CHAPTER:', '').rstrip(']').strip()
            chapters.append({
                "title": current_chapter,
                "dialogue_index": len(dialogues)
            })
            continue
        
        m_jorge = re.match(r'^JORGE:\s*(.+)$', line, re.IGNORECASE)
        m_dalia = re.match(r'^DALIA:\s*(.+)$', line, re.IGNORECASE)
        
        if m_jorge:
            dialogues.append({
                "speaker": "JORGE",
                "voice": VOICE_MALE,
                "text": m_jorge.group(1).strip(),
                "chapter": current_chapter
            })
        elif m_dalia:
            dialogues.append({
                "speaker": "DALIA",
                "voice": VOICE_FEMALE,
                "text": m_dalia.group(1).strip(),
                "chapter": current_chapter
            })
            
    return chapters, dialogues

def get_duration(audio_file: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def format_timestamp_vtt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"

def format_timestamp_srt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

async def synthesize_dialogue(dialogues):
    print(f"Sintetizando {len(dialogues)} bloques vocales con Edge-TTS...")
    raw_files = []
    for idx, item in enumerate(dialogues):
        out_file = TEMP_DIR / f"raw_{idx:03d}_{item['speaker'].lower()}.mp3"
        cleaned_text = clean_for_tts(item['text'])
        communicate = edge_tts.Communicate(cleaned_text, item['voice'], rate="+1%")
        await communicate.save(str(out_file))
        raw_files.append(out_file)
        print(f"  [{idx+1}/{len(dialogues)}] Voz generada ({item['speaker']}): {out_file.name}")
    return raw_files

def apply_sound_design_and_mix(raw_files, dialogues):
    print("\n🎛️ Aplicando capas de diseño sonoro de estudio (Música Kevin MacLeod, Tecleo Keychron & Sala)...")
    mixed_files = []
    
    music_tension = AUDIO_LIB / "music_isolated_tension.mp3"
    office_ambiance = AUDIO_LIB / "office_ambiance.mp3"
    typing_keychron = AUDIO_LIB / "typing_keychron.mp3"
    
    for idx, (raw_f, diag) in enumerate(zip(raw_files, dialogues)):
        dur = get_duration(raw_f)
        out_mixed = TEMP_DIR / f"mix_{idx:03d}.mp3"
        ch = diag.get("chapter", "")

        # 1. Cold Open, Pacto Invisible y Cierre: Piano emocional (Kevin MacLeod - Isolated)
        if any(k in ch for k in ["Cold Open", "Pacto Invisible", "Cierre"]):
            if music_tension.exists():
                cmd = [
                    "ffmpeg", "-y",
                    "-i", str(raw_f),
                    "-stream_loop", "-1", "-i", str(music_tension),
                    "-filter_complex",
                    f"[1:a]volume=0.035,afade=t=in:st=0:d=1.5,afade=t=out:st={max(0, dur-1.5):.2f}:d=1.5[bg];"
                    f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]",
                    "-map", "[aout]",
                    "-c:a", "libmp3lame", "-b:a", "192k",
                    str(out_mixed)
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                mixed_files.append(out_mixed)
                continue

        # 2. Análisis de autoría y publicación a las 7 PM: Tecleo acústico sutil
        if "Revolución de las Webnovels" in ch and typing_keychron.exists():
            cmd = [
                "ffmpeg", "-y",
                "-i", str(raw_f),
                "-stream_loop", "-1", "-i", str(typing_keychron),
                "-filter_complex",
                f"[1:a]volume=0.03,afade=t=in:st=0:d=1.0,afade=t=out:st={max(0, dur-1.0):.2f}:d=1.0[bg];"
                f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]",
                "-map", "[aout]",
                "-c:a", "libmp3lame", "-b:a", "192k",
                str(out_mixed)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            mixed_files.append(out_mixed)
            continue

        # 3. Metaficción y Webtoon: Ambiente sutil
        if ("Metaficción" in ch or "Fuera de la Burbuja" in ch) and office_ambiance.exists():
            cmd = [
                "ffmpeg", "-y",
                "-i", str(raw_f),
                "-stream_loop", "-1", "-i", str(office_ambiance),
                "-filter_complex",
                f"[1:a]volume=0.025,afade=t=in:st=0:d=1.0,afade=t=out:st={max(0, dur-1.0):.2f}:d=1.0[bg];"
                f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]",
                "-map", "[aout]",
                "-c:a", "libmp3lame", "-b:a", "192k",
                str(out_mixed)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            mixed_files.append(out_mixed)
            continue

        # 4. Voz limpia
        shutil.copy2(raw_f, out_mixed)
        mixed_files.append(out_mixed)
        
    return mixed_files

async def produce_episode():
    print("===========================================================================")
    print("🎙️ PRODUCCIÓN: sIA NOVELAS #01 (OMNISCIENT READER'S VIEWPOINT)")
    print("===========================================================================")
    
    chapters, dialogues = parse_script(SCRIPT_NOVELAS_01)
    
    # 1. Sintetizar bloques vocales
    raw_files = await synthesize_dialogue(dialogues)
    
    # 2. Aplicar diseño sonoro
    mixed_files = apply_sound_design_and_mix(raw_files, dialogues)
    
    # 3. Concatenación y subtítulos
    print("\nCalculando duraciones exactas y generando subtítulos WebVTT / SRT...")
    concat_list = TEMP_DIR / "concat_list.txt"
    vtt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.vtt"
    srt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.srt"
    
    vtt_lines = ["WEBVTT - sIA Novelas #01: Omniscient Reader's Viewpoint\n"]
    srt_lines = []
    
    current_time = 0.0
    with open(concat_list, "w", encoding="utf-8") as f_concat:
        for idx, (m_file, diag) in enumerate(zip(mixed_files, dialogues)):
            p = str(m_file).replace('\\', '/')
            f_concat.write(f"file '{p}'\n")
            
            dur = get_duration(m_file)
            start_t = current_time
            end_t = current_time + dur
            
            speaker = diag["speaker"]
            text = diag["text"]
            
            vtt_lines.append(f"{format_timestamp_vtt(start_t)} --> {format_timestamp_vtt(end_t)}")
            vtt_lines.append(f"<v {speaker}>{text}\n")
            
            srt_lines.append(f"{idx + 1}")
            srt_lines.append(f"{format_timestamp_srt(start_t)} --> {format_timestamp_srt(end_t)}")
            srt_lines.append(f"{speaker}: {text}\n")
            
            current_time = end_t
            
    vtt_path.write_text("\n".join(vtt_lines), encoding="utf-8")
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    shutil.copy2(vtt_path, SPOTIFY_DIR / vtt_path.name)
    shutil.copy2(srt_path, SPOTIFY_DIR / srt_path.name)
    print(f"✅ Subtítulos VTT y SRT generados y replicados en {SPOTIFY_DIR}")
    
    # 4. Masterización con Normalización EBU R128 (-16 LUFS)
    unmastered = TEMP_DIR / "unmastered.mp3"
    final_output = AUDIO_DIR / EPISODE_INFO["filename"]
    spotify_output = SPOTIFY_DIR / EPISODE_INFO["filename"]
    
    print("\n🎬 Ensamblando master final con Compresión Dinámica y Normalización EBU R128 (-16 LUFS)...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(unmastered)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    cover_path = BASE_DIR / "cover.jpg"
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(unmastered),
        "-i", str(cover_path),
        "-map", "0:a",
        "-map", "1:v?",
        "-id3v2_version", "3",
        "-metadata", f"title={EPISODE_INFO['title']}",
        "-metadata", "artist=sIA Media - Carlos Corona",
        "-metadata", "album=sIA Novelas",
        "-metadata", f"comment={EPISODE_INFO['description']}",
        "-map_metadata", "1",
        "-af", "acompressor=threshold=-20dB:ratio=2.5:attack=20:release=150,loudnorm=I=-16:TP=-1.5:LRA=9",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(final_output)
    ]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.copy2(final_output, spotify_output)
    
    total_sec = get_duration(final_output)
    size_bytes = final_output.stat().st_size
    print(f"✅ Master MP3 generado con éxito: {final_output}")
    print(f"   Duración total: {int(total_sec // 60)}m {int(total_sec % 60)}s | Tamaño: {size_bytes / (1024*1024):.2f} MB")
    print(f"   Replicado a Spotify: {spotify_output}")
    
    # 5. Actualizar RSS
    update_rss_feed(final_output, size_bytes, int(total_sec), vtt_path, srt_path)
    
    # 6. Registrar en news_vault.json
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
      <guid isPermaLink="false">sia-novelas-01-omniscient-reader-viewpoint</guid>
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
            "sIA Novelas #01: Omniscient Reader's Viewpoint y el fenómeno de las webnovels coreanas",
            "La sociología del metro de Seúl: soledad urbana y lectura capitulada en Munpia",
            "La metaficción del lector: Kim Dokja y la primacía de la empatía sobre la fuerza bruta",
            "El pacto supremo entre autor y lector: salvar una vida a través de una historia",
            "La expansión transmedia: de la webnovel al webtoon vertical de Redice y la gran pantalla"
        ],
        "cooldown_days": 45,
        "date": datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro de memoria añadido a news_vault.json.")

if __name__ == '__main__':
    asyncio.run(produce_episode())
