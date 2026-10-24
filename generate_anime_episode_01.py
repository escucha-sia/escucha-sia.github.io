"""
sIA Anime #01: Kyoto Animation y la Belleza de lo Cotidiano: Salarios Dignos, Sakuga y el Fuego de la Resiliencia
- Enfoque Humano y Técnico: De la mesa de cocina en Uji en 1981 al estudio que desafió el crunch y venció a la tragedia.
- Diseño Sonoro de Estudio: Piano emocional (Kevin MacLeod - Isolated) y acústica de sala.
- Masterización Broadcast EBU R128 (-16 LUFS) y compresión dinámica: volumen 100% calibrado.
- Subtítulos WebVTT y SRT sincronizados para Podcasting 2.0.
- Registro en podcast.xml, audio/podcast.xml y news_vault.json.
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
TEMP_DIR = BASE_DIR / "temp_chunks_anime_01"
AUDIO_LIB = BASE_DIR / "assets" / "audio_library"
NEWS_VAULT = BASE_DIR / "news_vault.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

EPISODE_INFO = {
    "title": "sIA Anime #01: Kyoto Animation y la Belleza de lo Cotidiano: Salarios Dignos, Sakuga y el Fuego de la Resiliencia",
    "filename": "sIA_Anime_01_Kyoto_Animation_Belleza_Cotidiano_2026-10-24.mp3",
    "description": "sIA Anime #01: La historia humana y técnica del estudio más querido del mundo de la animación. De la mesa de cocina en Uji donde amas de casa fundaron el estudio en 1981, al desafío radical contra el crunch mediante salarios fijos y escuela interna. La obsesión artesanal por las microexpresiones en K-On!, Hyouka y Violet Evergarden, el golpe devastador de 2019 y la resurrección colectiva demostrando que el arte nacido de la empatía no puede ser destruido. | Leer artículo y análisis técnico APA: https://escucha-sia.github.io/articulos/sia-anime-01-kyoto-animation-belleza-cotidiano-resiliencia.html"
}

SCRIPT_ANIME_01 = """
[CHAPTER: 01. Cold Open: La Mesa de Té en Uji]
DALIA: Primavera de mil novecientos ochenta y uno en Uji, una pequeña ciudad al sur de Kioto famosa por sus campos de té verde. Muy lejos de los rascacielos y el ritmo frenético de Tokio, una mujer llamada Yoko Hatta, antigua colorista de animación que se había mudado tras casarse, reúne a un grupo de vecinas y amas de casa alrededor de una mesa baja de madera. Sobre la mesa no hay computadoras ni contratos millonarios; hay pinceles finos, frascos de pintura acrílica y láminas transparentes de acetato. Aquellas mujeres coloreaban a mano, dibujo por dibujo, los fotogramas que los grandes estudios de Tokio les enviaban por correspondencia. Pero mientras sostenían sus pinceles, compartían una convicción silenciosa: que la animación no tenía por qué ser una trinchera de explotación donde los artistas se consumieran hasta enfermar, sino un oficio digno, humano y hecho con amor desde la comunidad. En esa humilde sala de estar nació Kyoto Animation.

[CHAPTER: 02. Prólogo & Brújula: sIA Anime]
JORGE: Hola, ¿cómo estás? Qué gusto coincidir contigo. Mi nombre es Jorge...
DALIA: ... y yo soy Dalia. Te damos una cálida bienvenida a Sia.
JORGE: Hoy inauguramos un territorio completamente nuevo en nuestra bitácora: sIA Anime, la física de la ilusión. Si llegas aquí esperando una lista superficial de recomendaciones de temporada o noticias rápidas, este no es ese tipo de espacio. En Sia nos sentamos a examinar el alma de la animación: la artesanía del movimiento conocida como sakuga, la psicología de la dirección visual y, sobre todo, el costo humano y emocional de quienes dejan parte de su vida en cada fotograma dibujado a mano.
DALIA: Y para abrir esta puerta, era imposible empezar con otro nombre que no fuera Kyoto Animation, conocido cariñosamente en todo el mundo como KyoAni. Un estudio que demostró que el mayor acto de rebeldía en una industria dominada por el agotamiento extremo no fue hacer escenas de batallas ruidosas, sino pagar sueldos justos y aprender a dibujar la belleza de lo cotidiano.

[CHAPTER: 03. Los Tres Momentos de la Bitácora]
JORGE: Cuando analizamos la trayectoria de KyoAni, descubrimos que su magia no viene de un software secreto ni de presupuestos ilimitados; viene de una filosofía de vida que desafió todas las reglas de Tokio. Para acompañarnos en esta travesía, fíjate en estos tres momentos clave: Primero: El modelo contracultural. Cómo decidieron pagar salarios mensuales fijos, fundar su propia escuela de arte y romper el sistema de pago por pieza que asfixia a los animadores japoneses. Segundo: La física de lo cotidiano. La técnica de animación de microexpresiones: cómo el peso de una taza de café, el parpadeo tímido de una mirada o la inercia de un cabello al viento pueden conmover más que cualquier explosión cósmica. Y tercero: El fuego del dieciocho de julio de dos mil diecinueve y el renacimiento de Violet Evergarden. La tragedia que desgarró al estudio y la respuesta de una comunidad que se negó a permitir que el dolor apagara su luz.
DALIA: Respira profundo, ponte cómodo, ajusta tus audífonos... y adentrémonos en el corazón de Kioto.

[CHAPTER: 04. La Rebelión Salarial contra el Crunch]
DALIA: Para entender por qué Kyoto Animation es un milagro, primero hay que entender la cruda realidad de la industria del anime en Tokio. Durante décadas, el estándar ha sido el trabajo a destajo: a los animadores novatos no se les paga un sueldo fijo; se les paga por dibujo terminado. En promedio, apenas doscientos yenes por lámina, lo que equivale a menos de dos dólares. Para poder pagar la renta y comer, un animador novato tiene que dibujar quince horas al día, durmiendo en sacos bajo su escritorio y alimentándose de fideos instantáneos. El resultado es una rotación brutal: más del ochenta por ciento abandona la profesión antes de cumplir tres años.
JORGE: Yoko Hatta y su esposo Hideaki vieron ese panorama y dijeron: 'Nosotros no vamos a operar así'. En lugar de contratar trabajadores independientes temporales para cada proyecto y desecharlos al terminar, Kyoto Animation tomó una decisión radical: contrataron a todos sus animadores como empleados permanentes de planta, con sueldo mensual garantizado, horarios regulares, beneficios médicos y apoyo para el cuidado de sus hijos.
DALIA: Y fueron todavía más lejos: crearon la KyoAni School, su propia academia interna donde formaban pacientemente a jóvenes talentos, enseñándoles no solo a dibujar rápido, sino a observar el comportamiento humano con sensibilidad. En una industria dominada históricamente por hombres directores, KyoAni se convirtió en un hogar donde las mujeres alcanzaron puestos de liderazgo histórico, como Naoko Yamada, la brillante directora detrás de obras maestras como K-On y Una Voz Silenciosa. No había competencia despiadada; había una familia que cenaba junta y que crecía junta proyecto tras proyecto.

[CHAPTER: 05. La Física de lo Cotidiano: Sakuga y Microexpresiones]
JORGE: Y esa estabilidad humana se reflejó de inmediato en la pantalla. Cuando un animador no tiene que apresurarse para entregar cien dibujos al día para sobrevivir, puede dedicar una semana entera a una sola escena de cinco segundos. Es ahí donde KyoAni inventó su sello inconfundible: la física de lo cotidiano.
DALIA: En series de acción tradicionales, el presupuesto y la energía se concentran en las batallas: espadas relucientes, rayos mágicos y cámaras giratorias. Pero en KyoAni, el milagro ocurre cuando no pasa aparentemente nada. En obras como Hyouka, K-On o Hibike Euphonium, ves a una adolescente ajustándose las gafas con una ligera vacilación en los nudillos; ves el peso exacto de la gravedad cuando alguien se sienta cansado en una banca de madera; ves la refracción sutil de la luz en la pupila antes de que caiga una lágrima.
JORGE: Técnicamente, eso se llama animación de actuación o acting animation. En lugar de usar poses estáticas donde solo se mueve la boca de los personajes, KyoAni anima el cuerpo entero en movimiento continuo a veinticuatro cuadros por segundo. Entendieron que los seres humanos nunca estamos completamente quietos: respiramos, cambiamos el peso de un pie a otro, apretamos los labios cuando dudamos. Esa atención obsesiva al detalle convierte la rutina más simple en un poema visual que conecta directamente con la memoria emocional del espectador.

[CHAPTER: 06. La Noche Más Oscura: Dieciocho de Julio de Dos Mil Diecinueve]
DALIA: Pero la pureza de esa obra comunitaria enfrentó la prueba más cruel y desgarradora que se recuerde en la historia del arte contemporáneo. La mañana del dieciocho de julio de dos mil diecinueve, un hombre perturbado entró al Estudio Uno de Kyoto Animation en Fushimi con gasolina y desató un incendio devastador.
JORGE: En cuestión de minutos, el edificio quedó envuelto en llamas. Treinta y seis personas perdieron la vida, y otras treinta y cuatro resultaron gravemente heridas. No eran simples trabajadores; eran directores legendarios como Yasuhiro Takemoto, diseñadores de personajes, animadores veteranos y jóvenes promesas recién egresadas de su escuela. Se perdió la mitad del equipo más talentoso y sensible que jamás haya existido en la animación mundial.
DALIA: El dolor en Kioto y en toda la comunidad internacional fue indescriptible. Millones de personas alrededor del planeta encendieron velas, donaron fondos y lloraron la pérdida de artistas cuyas obras les habían acompañado en momentos de depresión y soledad. Muchos analistas creyeron que aquel golpe mortal significaba el fin definitivo de Kyoto Animation. Era imposible reponerse de una herida tan profunda. Pero quienes pensaron eso, no conocían el espíritu de Uji.

[CHAPTER: 07. 🌌 Fuera de la Burbuja: La Resurrección de Violet Evergarden]
JORGE: Entremos a nuestra cápsula Fuera de la Burbuja, porque en el abismo más oscuro es donde el espíritu humano revela su verdadera estatura. Apenas unos días después de la tragedia, mientras los heridos aún luchaban por sus vidas en los hospitales, el presidente Hideaki Hatta habló ante los medios con voz quebrada pero firme. Dijo una frase que quedó grabada en la memoria colectiva: 'No nos rendiremos. El amor y la pasión de nuestros compañeros no terminarán en cenizas'.
DALIA: El estudio tenía a medio terminar la película más ambiciosa de su historia: Violet Evergarden, la película. La historia de una joven exsoldado que perdió los brazos en la guerra y que aprende a sanar su trauma escribiendo cartas para otras personas, intentando entender qué significa la frase 'Te amo'. Con manos vendadas y lágrimas en los ojos, los sobrevivientes regresaron poco a poco a los tableros de dibujo. No trabajaron por venganza ni por dinero; trabajaron para terminar la última obra de arte en la que habían trabajado sus amigos caídos.
JORGE: Cuando la película se estrenó en las salas de cine en septiembre de dos mil veinte, ocurrió un hecho sin precedentes en la industria japonesa. Tradicionalmente, si un animador no completa al menos un año de trabajo en una producción, su nombre no aparece en los créditos. Pero en Violet Evergarden, la dirección colocó en la pantalla grande los nombres de todos y cada uno de los treinta y seis compañeros que perdieron la vida en el incendio, honrando su talento y su memoria para la eternidad. La película fue un triunfo artístico colosal, recordándole al mundo entero que el odio puede derribar un edificio, pero jamás podrá extinguir el arte que nace de la empatía pura.

[CHAPTER: 08. Cierre Íntimo & Comunidad]
DALIA: Kyoto Animation nos enseñó que la verdadera maestría técnica no consiste en hacer alarde de virtuosismo vacío, sino en mirar al ser humano a los ojos, con sus fragilidades y sus silencios, y tratarlo con respeto tanto frente a la pantalla como detrás del tablero de dibujo.
JORGE: Si deseas profundizar en la anatomía técnica del sakuga de KyoAni, consultar los diagramas de acting animation y revisar la bibliografía académica sobre sociología del anime en formato APA, visita nuestra revista digital en escucha guion sia punto github punto io.
DALIA: Muchísimas gracias por acompañarnos en este primer viaje de sIA Anime. Cuéntanos en comentarios qué obra de KyoAni tocó tu vida y qué otro estudio o creador te gustaría que analicemos juntos. Que tengas una noche serena y reflexiva... y nos escuchamos en la próxima entrega de Sia.
JORGE: Hasta la próxima.
"""

def clean_for_tts(text: str) -> str:
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    # Pronunciación fonética de marca sIA -> 'Sia' (palabra corrida, no deletreada)
    t = re.sub(r'\bsIA\b', 'Sia', t)
    t = re.sub(r'\bSIA\b', 'Sia', t)
    t = re.sub(r'\bKyoAni\b', 'Kio-Ani', t)
    t = re.sub(r'\bsakuga\b', 'sákuga', t)
    t = re.sub(r'\bK-On\b', 'Kei-On', t)
    t = re.sub(r'\bHyouka\b', 'Jiouka', t)
    t = re.sub(r'\bHibike Euphonium\b', 'Jibike Eufónium', t)
    t = re.sub(r'\bIP\b', 'I P', t)
    t = re.sub(r'\bCGI\b', 'C G I', t)
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
    print("\n🎛️ Aplicando capas de diseño sonoro de estudio (Música Kevin MacLeod & Acústica de Sala)...")
    mixed_files = []
    
    music_tension = AUDIO_LIB / "music_isolated_tension.mp3"
    office_ambiance = AUDIO_LIB / "office_ambiance.mp3"
    
    for idx, (raw_f, diag) in enumerate(zip(raw_files, dialogues)):
        dur = get_duration(raw_f)
        out_mixed = TEMP_DIR / f"mix_{idx:03d}.mp3"
        ch = diag.get("chapter", "")

        # 1. Cold Open y Resurrección: Piano reflexivo emocional (Kevin MacLeod - Isolated)
        if "Cold Open" in ch or "Fuera de la Burbuja" in ch or "Cierre" in ch:
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

        # 2. Segmentos de estudio y escuela: Acústica suave de sala
        if ("Rebelión" in ch or "Sakuga" in ch) and office_ambiance.exists():
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

        # 3. Voz directa limpia
        shutil.copy2(raw_f, out_mixed)
        mixed_files.append(out_mixed)
        
    return mixed_files

async def produce_episode():
    print("===========================================================================")
    print("🎙️ PRODUCCIÓN: sIA ANIME #01 (KYOTO ANIMATION & RESILIENCIA)")
    print("===========================================================================")
    
    chapters, dialogues = parse_script(SCRIPT_ANIME_01)
    
    # 1. Sintetizar bloques vocales
    raw_files = await synthesize_dialogue(dialogues)
    
    # 2. Aplicar diseño sonoro
    mixed_files = apply_sound_design_and_mix(raw_files, dialogues)
    
    # 3. Concatenación, medición y generación de transcripciones
    print("\nCalculando duraciones exactas y generando subtítulos WebVTT / SRT...")
    concat_list = TEMP_DIR / "concat_list.txt"
    vtt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.vtt"
    srt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.srt"
    
    vtt_lines = ["WEBVTT - sIA Anime #01: Kyoto Animation y la Belleza de lo Cotidiano\n"]
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
    
    # 4. Ensamble de Master Final con Normalización EBU R128 (-16 LUFS)
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
        "-metadata", "album=sIA Anime",
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
      <guid isPermaLink="false">sia-anime-01-kyoto-animation-belleza-cotidiano</guid>
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
            "sIA Anime #01: Kyoto Animation y la fundación comunitaria en Uji en 1981",
            "La rebelión contra el crunch: salarios fijos, formación interna y liderazgo femenino",
            "La física de lo cotidiano: sakuga de microexpresiones y acting animation",
            "El atentado de 2019 en el Estudio 1 y la respuesta solidaria mundial",
            "La resurrección artística de Violet Evergarden: The Movie y el homenaje a los caídos"
        ],
        "cooldown_days": 45,
        "date": datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro de memoria añadido a news_vault.json.")

if __name__ == '__main__':
    asyncio.run(produce_episode())
