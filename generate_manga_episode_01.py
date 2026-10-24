"""
sIA Manga #01: Kentaro Miura y la Tumba de Tinta de Berserk: El Sacrificio Físico del Mangaka y la Filosofía del Dolor
- Enfoque Humano y Técnico: La soledad física del tablero de dibujo, la obsesión microscópica con la plumilla G-Pen y la figura de Guts como símbolo existencialista.
- Diseño Sonoro de Estudio: Piano reflexivo (Kevin MacLeod - Isolated) y acústica de sala.
- Masterización Broadcast EBU R128 (-16 LUFS) y compresión dinámica: volumen 100% uniforme.
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
TEMP_DIR = BASE_DIR / "temp_chunks_manga_01"
AUDIO_LIB = BASE_DIR / "assets" / "audio_library"
NEWS_VAULT = BASE_DIR / "news_vault.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

EPISODE_INFO = {
    "title": "sIA Manga #01: Kentaro Miura y la Tumba de Tinta de Berserk: El Sacrificio Físico del Mangaka y la Filosofía del Dolor",
    "filename": "sIA_Manga_01_Kentaro_Miura_Berserk_Tumba_Tinta_2026-10-24.mp3",
    "description": "sIA Manga #01: La devoción, el dolor físico y la maestría visual detrás de la obra magna del manga oscuro. Treinta y dos años dibujando cada eslabón a mano con plumilla G-Pen, la soledad extrema frente al tablero, la deconstrucción de Guts como arquetipo de la resistencia humana ante el destino y el legado inmortal de Kentaro Miura continuado por la hermandad de Studio Gaga. | Leer artículo y análisis visual APA: https://escucha-sia.github.io/articulos/sia-manga-01-kentaro-miura-berserk-tumba-tinta.html"
}

SCRIPT_MANGA_01 = """
[CHAPTER: 01. Cold Open: La Habitación a las Cuatro AM]
JORGE: Madrugada en Tokio. Afuera la ciudad duerme bajo un silencio pesado. Adentro de un pequeño apartamento, una lámpara de flexo ilumina una hoja de papel blanco de cien gramos. El único sonido en la habitación es el rasguño metálico, rítmico y casi obsesivo de una plumilla G-Pen contra el papel. Un hombre de cuarenta años sostiene el mango de madera con los dedos vendados para amortiguar la tendinitis crónica que le quema la muñeca. Se llama Kentaro Miura. Lleva dieciséis horas continuas inclinado sobre el tablero. Con una lupa de relojero y tinta china negra, dibuja a mano alzada, uno por uno, los miles de eslabones de una cota de malla y las sombras microscópicas en el rostro de un guerrero que se niega a morir. No utiliza asistentes para los personajes principales. No utiliza filtros digitales para acelerar el proceso. Cuando sus amigos le suplicaban que descansara y saliera a ver el sol, Miura sonreía con timidez y respondía: 'Si no lo dibujo yo mismo con cada gota de mi energía, los lectores sentirán que les estoy mintiendo'.

[CHAPTER: 02. Prólogo & Brújula: sIA Manga]
DALIA: Hola, ¿cómo estás? Qué placer saludarte. Mi nombre es Dalia...
JORGE: ... y yo soy Jorge. Te damos una cálida bienvenida a Sia.
DALIA: Hoy abrimos una nueva coordenada en nuestra bitácora cultural: sIA Manga, la gramática de la tinta. Si buscas debates superficiales sobre niveles de poder o resúmenes apresurados de capítulos, este no es ese rincón. En Sia nos detenemos a examinar la arquitectura visual del cómic japonés: el control del ritmo cardíaco del lector a través de las viñetas, el uso sagrado del espacio en blanco conocido como Ma, y la batalla solitaria de los mangakas que entregan su salud física por dejar una huella en el mundo.
JORGE: Y para inaugurar este espacio, era un deber de honor comenzar con el monumento más imponente, doloroso y conmovedor en la historia de la historieta universal: Kentaro Miura y los treinta y dos años de vida que fundió en las páginas de Berserk.

[CHAPTER: 03. Los Tres Momentos de la Bitácora]
DALIA: Cuando te asomas a las páginas de Berserk, no estás viendo simples dibujos de fantasía oscura; estás presenciando un testamento de resistencia humana. Para que nos acompañes en esta inmersión, presta atención a estos tres momentos clave: Primero: La gramática de la tinta y la plumilla G-Pen. Cómo Miura dominó la física del papel, el tramado manual y el choque psicológico del giro de página para manipular la respiración del lector. Segundo: La filosofía de Guts y la deconstrucción del héroe. Por qué Berserk no trata sobre la violencia, sino sobre la soledad, el trauma y la decisión heroica de levantarse un segundo más frente a un destino aplastante. Y tercero: El seis de mayo de dos mil veintiuno y la promesa de Kouji Mori. La partida repentina del maestro a los cincuenta y cuatro años y cómo la hermandad salvó su obra del olvido.
JORGE: Prepárate un café caliente, ajusta tus audífonos y acompáñanos a descubrir la verdad detrás de la tinta.

[CHAPTER: 04. La Gramática de la Tinta y el Giro de Página]
JORGE: El manga es un medio artístico silencioso. No tiene música de fondo, no tiene actores de voz ni efectos de sonido grabados. El autor depende exclusivamente de dos cosas: tinta negra y papel blanco. Y en ese territorio minimalista, Kentaro Miura fue un científico de la percepción humana.
DALIA: Jorge, fíjate en cómo estructuraba sus páginas. En Japón se lee de derecha a izquierda. Miura diseñaba las viñetas guiando los ojos del lector a través de una coreografía geométrica invisible: colocaba líneas cinéticas que empujaban tu mirada de la esquina superior derecha hacia la esquina inferior izquierda. Y justo cuando tu ojo llegaba al final de la hoja impar, ocultaba el clímax dramático o la revelación aterradora al otro lado.
JORGE: Eso en la teoría del manga se conoce como el page-turn effect o el impacto del giro de página. Miura sabía que para ver la siguiente viñeta tenías que hacer un movimiento físico con tus dedos: voltear la hoja. Y en esa fracción de segundo de incertidumbre en blanco, tu cerebro experimentaba un golpe de dopamina o de terror. Al voltear, te encontrabas con una doble página monumental que te dejaba sin aliento: castillos góticos dibujados hasta el último ladrillo, ejércitos enteros donde cada soldado tenía un rostro distinto, o criaturas nacidas de una pesadilla renacentista.
DALIA: Mientras la mayoría de los autores utilizaban tramas adhesivas precortadas para ahorrar tiempo, Miura hacía el sombreado con micro-líneas cruzadas trazadas a mano con plumilla. Llegó a pasar semanas enteras en una sola página doble. Esa obsesión extrema le costó caro: sus descansos se volvieron legendarios y el manga se publicaba a cuentagotas. Pero los lectores sabían que cada entrega era una pieza de museo que desafiaba los límites de lo que un ser humano puede plasmar con sus manos.

[CHAPTER: 05. Guts: La Filosofía del Dolor y el Luchador]
JORGE: Pero toda esa técnica virtuosa habría sido un cascarón vacío sin un corazón que la sostuviera. Y el corazón de Berserk es su protagonista: Guts, conocido como el Luchador o the Struggler.
DALIA: Quien no ha leído la obra suele cometer el error de pensar que Guts es el típico arquetipo de guerrero musculoso e insensible que resuelve todo con una espada gigante. Pero cuando lees el arco de la Edad de Oro, descubres a uno de los personajes más vulnerables y tridimensionales de la literatura contemporánea. Guts nace literalmente debajo del cadáver ahorcado de su madre; crece en un mundo medieval brutal donde sufre abusos indecibles, rechazo y traición. No tiene poderes divinos, no es el elegido de ninguna profecía.
JORGE: Es ahí donde Berserk se convierte en una obra profundamente existencialista. En el universo de Miura existe la Causalidad: una fuerza cósmica determinista donde los dioses y los apóstoles deciden que los humanos son ganado indefenso destinado a sufrir. Griffith, su mejor amigo y comandante, encarna la rendición absoluta al destino: sacrifica a todos sus seres queridos para alcanzar un castillo brillante y convertirse en un dios. Pero Guts elige el camino contrario: el rechazo a la resignación.
DALIA: A pesar de estar mutilado, ciego de un ojo y con el cuerpo cubierto de cicatrices, Guts empuña su espada pesada no para conquistar el mundo, sino para proteger a las personas que ama y reclamar su derecho a existir. La frase del Caballero de la Calavera resume toda la filosofía de Miura: 'Lucha, desafía, resiste... pues esa es la única espada con la que el hombre puede hendir el destino'. Guts representa a cualquier ser humano que, tras ser destrozado por la vida, decide ponerse de pie una mañana más y seguir luchando.

[CHAPTER: 06. La Partida del Maestro y el Pacto de Kouji Mori]
JORGE: Esa entrega física total, sin embargo, cobró la factura definitiva. El seis de mayo de dos mil veintiuno, a la temprana edad de cincuenta y cuatro años, Kentaro Miura falleció de manera súbita debido a una disección aórtica aguda. La noticia conmocionó al mundo entero: desde mangakas rivales hasta millones de lectores que sintieron la pérdida de un mentor espiritual. El final de la obra más influyente de la fantasía oscura parecía haber muerto con su creador.
DALIA: Pero aquí surge el acto de amor fraternal más noble de la industria. Su mejor amigo desde la preparatoria, el también mangaka Kouji Mori, reveló que durante más de treinta años, Miura lo invitaba a cenar a su casa para contarle, escena por escena y final por final, cómo terminaría la historia de Guts y Griffith. Miura no le dejó notas escritas a su editorial, pero le confió la memoria de su historia a su hermano del alma.
JORGE: Kouji Mori reunió a los asistentes de Miura en Studio Gaga —jóvenes artistas que fueron entrenados personalmente por él— y les hizo una promesa: 'No inventaremos nada nuevo. No alargaremos la historia por dinero. Solo dibujaremos exactamente lo que Miura me contó antes de partir'. Y así, con lágrimas en los ojos pero con una devoción inquebrantable, Berserk continuó su publicación, demostrando que cuando el arte se construye con verdad, ni la muerte misma puede romper el lazo entre un creador y su legado.

[CHAPTER: 07. 🌌 Fuera de la Burbuja: La Huella de Berserk en la Cultura Global]
DALIA: Entremos a nuestra cápsula Fuera de la Burbuja para entender por qué la tinta de Miura trascendió al papel y transformó la cultura pop global.
JORGE: Si has jugado videojuegos como Dark Souls, Bloodborne o Elden Ring, has caminado dentro del cerebro de Kentaro Miura. El legendario director Hidetaka Miyazaki ha declarado abiertamente que sin Berserk, el género Soulslike jamás habría existido: la atmósfera opresiva, el caballero solitario que enfrenta monstruos colosales con una voluntad inquebrantable y la melancolía de un mundo en ruinas nacieron directamente de los trazos de Miura.
DALIA: Desde las espadas descomunales en Final Fantasy hasta series de fantasía occidentales, Berserk redefinió lo que significa crear arte oscuro: no la glorificación de la violencia gratuita, sino la exploración de la belleza que solo se puede apreciar cuando estás rodeado de sombras absolutas.

[CHAPTER: 08. Cierre Íntimo & Comunidad]
JORGE: Kentaro Miura no dibujó un cómic; esculpió una catedral de papel y tinta que nos enseñó que la mayor valentía humana no es no tener miedo, sino avanzar temblando con una espada rota en la mano.
DALIA: Si deseas analizar los diagramas de paneling y composición visual de Miura, y revisar la bibliografía académica sobre narrativa gráfica y existencialismo en formato APA, visita nuestra revista digital en escucha guion sia punto github punto io.
JORGE: Gracias por acompañarnos en este primer capítulo de sIA Manga. Déjanos en los comentarios qué escena de Berserk marcó tu vida y qué otro maestro del dibujo te gustaría que exploremos juntos. Que tengas una noche reflexiva y llena de fuerza... y nos escuchamos en la próxima entrega de Sia.
DALIA: Hasta la próxima.
"""

def clean_for_tts(text: str) -> str:
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    t = re.sub(r'\bsIA\b', 'Sia', t)
    t = re.sub(r'\bSIA\b', 'Sia', t)
    t = re.sub(r'\bG-Pen\b', 'G-Pen', t)
    t = re.sub(r'\bKouji Mori\b', 'Kouyi Mori', t)
    t = re.sub(r'\bGriffith\b', 'Grifis', t)
    t = re.sub(r'\bSoulslike\b', 'Souls like', t)
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
    print("\n🎛️ Aplicando capas de diseño sonoro de estudio (Música Kevin MacLeod & Acústica de Estudio)...")
    mixed_files = []
    
    music_tension = AUDIO_LIB / "music_isolated_tension.mp3"
    office_ambiance = AUDIO_LIB / "office_ambiance.mp3"
    
    for idx, (raw_f, diag) in enumerate(zip(raw_files, dialogues)):
        dur = get_duration(raw_f)
        out_mixed = TEMP_DIR / f"mix_{idx:03d}.mp3"
        ch = diag.get("chapter", "")

        # 1. Cold Open, Filosofía de Guts, Partida y Cierre: Piano emocional (Kevin MacLeod - Isolated)
        if any(k in ch for k in ["Cold Open", "Filosofía del Dolor", "Partida del Maestro", "Cierre"]):
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

        # 2. Análisis de técnica gráfica: Ambiente sutil
        if ("Gramática de la Tinta" in ch or "Fuera de la Burbuja" in ch) and office_ambiance.exists():
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

        # 3. Voz limpia
        shutil.copy2(raw_f, out_mixed)
        mixed_files.append(out_mixed)
        
    return mixed_files

async def produce_episode():
    print("===========================================================================")
    print("🎙️ PRODUCCIÓN: sIA MANGA #01 (KENTARO MIURA & BERSERK)")
    print("===========================================================================")
    
    chapters, dialogues = parse_script(SCRIPT_MANGA_01)
    
    # 1. Sintetizar bloques vocales
    raw_files = await synthesize_dialogue(dialogues)
    
    # 2. Aplicar diseño sonoro
    mixed_files = apply_sound_design_and_mix(raw_files, dialogues)
    
    # 3. Concatenación y subtítulos
    print("\nCalculando duraciones exactas y generando subtítulos WebVTT / SRT...")
    concat_list = TEMP_DIR / "concat_list.txt"
    vtt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.vtt"
    srt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.srt"
    
    vtt_lines = ["WEBVTT - sIA Manga #01: Kentaro Miura y la Tumba de Tinta de Berserk\n"]
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
        "-metadata", "album=sIA Manga",
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
      <guid isPermaLink="false">sia-manga-01-kentaro-miura-berserk-tumba-tinta</guid>
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
            "sIA Manga #01: Kentaro Miura y la génesis física de Berserk en 1989",
            "La gramática de la tinta: plumilla G-Pen, tramado manual y el page-turn shock",
            "La filosofía de Guts: la deconstrucción del dolor, el trauma y la rebelión existencial",
            "El fallecimiento en 2021 y la hermandad de Kouji Mori y Studio Gaga",
            "La huella monumental en la cultura pop: del manga a Dark Souls y Elden Ring"
        ],
        "cooldown_days": 45,
        "date": datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro de memoria añadido a news_vault.json.")

if __name__ == '__main__':
    asyncio.run(produce_episode())
