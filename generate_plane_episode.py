"""
sIA Deep Dive #48: Plane vs. Jira: La Rebelión Open Source contra Atlassian, la Fatiga de los Tickets y el Éxodo de Next.js
- Enfoque Humano y Técnico: La frustración global con Jira, el origen en Hyderabad de los hermanos Kurama, las confesiones de Reddit y la valiente migración de Next.js a Vite.
- Diseño Sonoro de Estudio: Piano reflexivo (Kevin MacLeod), tecleo Keychron V1 y acústica de sala.
- Masterización Broadcast EBU R128 (-16 LUFS) y compresión dinámica.
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
TEMP_DIR = BASE_DIR / "temp_chunks_plane"
AUDIO_LIB = BASE_DIR / "assets" / "audio_library"
NEWS_VAULT = BASE_DIR / "news_vault.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

EPISODE_INFO = {
    "title": "sIA #48: Plane vs. Jira: La Rebelión Open Source contra Atlassian, la Fatiga de los Tickets y el Éxodo de Next.js",
    "filename": "sIA_DeepDive_Plane_OpenSource_Jira_Alternative_2026-10-25.mp3",
    "description": "sIA Deep Dive #48: La historia detrás de Plane (github.com/makeplane/plane). Cómo los hermanos Vamsi y Vihar Kurama desafiaron el monopolio de Atlassian desde Hyderabad, el hartazgo de los desarrolladores en Reddit ante la lentitud de Jira, la seducción de Linear y la decisión técnica radical de eliminar Next.js para migrar más de 1,200 archivos a React Router y Vite. | Leer artículo y análisis de arquitectura APA: https://escucha-sia.github.io/articulos/sia-deepdive-plane-opensource-jira-alternative-atlassian.html"
}

SCRIPT_PLANE = """
[CHAPTER: 01. Cold Open: Ocho Segundos para Abrir un Ticket]
JORGE: Pregúntale a cualquier desarrollador de software en el planeta cuál es la herramienta que más drena su energía vital en el trabajo diario, y nueve de cada diez no dudarán en darte el mismo nombre: Jira. Hay un hilo legendario en Reddit, en la comunidad de programación, con miles de votos positivos titulado simplemente: 'Jira es el lugar donde el entusiasmo de programar va a morir'. La anécdota se repite en miles de oficinas: son las diez de la mañana, acabas de resolver un error complejo en el código, pero antes de hacer el commit tienes que documentarlo. Haces clic en un enlace de Jira... y la pantalla se queda en blanco. Dos segundos. Cuatro segundos. Ocho segundos enteros de ruleta girando mientras tu navegador descarga megabytes de scripts pesados, formularios infinitos de campos obligatorios y permisos bizantinos configurados por un departamento de recursos humanos que jamás ha escrito una línea de código. En noviembre de dos mil veintidós, dos hermanos en Hyderabad, India, dijeron: 'Basta. No podemos seguir viviendo así'. Y abrieron un repositorio en GitHub llamado Plane.

[CHAPTER: 02. Prólogo & Brújula: sIA Deep Dive]
DALIA: Hola, ¿cómo estás? Qué gusto saludarte. Mi nombre es Dalia...
JORGE: ... y yo soy Jorge. Te damos una cálida bienvenida a Sia.
DALIA: Hoy en sIA exploramos un caso fascinante de soberanía tecnológica y arquitectura de software: el fenómeno de Plane, el proyecto de código abierto alojado en makeplane barra plane que ha sacudido a la industria de la gestión de proyectos, acumulando más de treinta mil estrellas en GitHub y desafiando el imperio multimillonario de Atlassian.
JORGE: Este no es solo un episodio sobre administración de tareas; es una radiografía profunda sobre por qué las herramientas corporativas se vuelven lentas y alienantes, cómo la comunidad de Reddit impulsó una alternativa autoalojada y la valiente decisión de ingeniería que tomó el equipo de Plane cuando decidieron arrancar de raíz a Next punto j-s para migrar toda su plataforma a Vite.

[CHAPTER: 03. Los Tres Momentos de la Bitácora]
DALIA: Para desglosar este caso en toda su dimensión técnica y humana, Jorge y yo hemos dividido la bitácora en tres momentos clave: Primero: El fin de la era Jira Server y el hartazgo de la comunidad. Cómo Atlassian forzó a miles de empresas a migrar a su nube cerrada y por qué herramientas como Linear enamoraron a Silicon Valley pero dejaron desamparados a los defensores del software libre. Segundo: Los hermanos Kurama y el nacimiento de Plane. De un prototipo en Hyderabad a recibir cuatro millones de dólares de OSS Capital bajo licencia abierta A-G-P-L versión tres. Y tercero: La rebelión de los mil doscientos archivos. Por qué tiraron Next punto j-s a la basura tras sufrir tiempos de espera de treinta segundos en desarrollo y cómo Vite les devolvió la velocidad instantánea.
JORGE: Si eres desarrollador, líder técnico o simplemente estás cansado de la burocracia digital, ajusta tus audífonos, respira profundo... y acompáñanos a analizar este viaje.

[CHAPTER: 04. El Monopolio de Atlassian y la Tentación de Linear]
DALIA: Para comprender el éxito fulgurante de Plane, hay que entender la tormenta perfecta que desató Atlassian. Durante casi dos décadas, Jira fue el estándar indiscutible de la industria. Si una empresa crecía, instalaba Jira Server en sus propios centros de datos. Pero en dos mil veinte, Atlassian anunció una decisión comercial letal: la muerte definitiva de Jira Server.
JORGE: El mensaje para los clientes fue contundente: o migraban obligatoriamente a Jira Cloud, pagando suscripciones mensuales recurrentes por usuario donde Atlassian custodia todos tus datos en sus servidores, o pagaban licencias corporativas Data Center que costaban cientos de miles de dólares al año. Para equipos médicos, instituciones financieras, entidades gubernamentales y empresas con políticas estrictas de privacidad, esto fue una bofetada. No podían legalmente poner sus secretos industriales y fallos de seguridad en la nube pública de un tercero.
DALIA: Al mismo tiempo, en Silicon Valley surgió Linear: una herramienta deslumbrante diseñada con obsesión por la velocidad. Con atajos de teclado tipo comando K, transiciones a sesenta fotogramas por segundo y una interfaz limpia y minimalista, Linear demostró que registrar un bug podía sentirse tan ágil como escribir en un editor de texto. Pero Linear tenía un gran inconveniente: era un jardín vallado, cien por ciento propietario y exclusivamente disponible en la nube.
JORGE: Los desarrolladores en foros como r diagonal selfhosted se hacían la misma pregunta desesperada: '¿Por qué no podemos tener la belleza y agilidad de Linear, con la potencia de sprints y módulos de Jira, pero bajo código abierto que podamos correr en nuestro propio servidor con un simple comando de Docker Compose?'

[CHAPTER: 05. De Hyderabad al Mundo: La Apuesta de los Hermanos Kurama]
DALIA: Esa pregunta fue la chispa que encendió a Vamsi Kurama y su hermano Vihar Kurama en Hyderabad. No querían fundar otra consultora de software tradicional; querían construir una alternativa soberana desde el sur global para el resto del planeta.
JORGE: En noviembre de dos mil veintidós publicaron el código de Plane bajo la licencia A-G-P-L versión tres. Su propuesta era directa: una plataforma modular que combina problemas, ciclos de trabajo, hojas de ruta y páginas de documentación estilo Notion en un solo espacio unificado. Pero con una regla innegociable: la edición comunitaria debía ser completamente gratuita, sin límites artificiales de usuarios y desplegable en tu propia infraestructura con contenedores Docker.
DALIA: La respuesta en Reddit y Hacker News fue explosiva. En cuestión de meses, Plane se convirtió en uno de los repositorios con mayor crecimiento orgánico en GitHub. Ingenieros de todo el mundo comenzaron a contribuir con traducciones, integraciones con GitHub y GitLab, y adaptadores para bases de datos Postgres. El fondo estadounidense O-S-S Capital, especializado en respaldar empresas comerciales de código abierto, lideró una ronda semilla de cuatro millones de dólares, validando que el software libre no es una obra de caridad, sino el modelo de desarrollo más robusto del siglo veintiuno.

[CHAPTER: 06. La Batalla de los Mil Doscientos Archivos: El Éxodo de Next.js]
JORGE: Pero en el corazón de todo gran proyecto de software llega un momento donde las decisiones arquitectónicas del pasado se convierten en un ancla. Y para Plane, esa ancla se llamaba Next punto j-s.
DALIA: Cuando los hermanos Kurama comenzaron a programar Plane, eligieron el framework Next punto j-s porque era la opción por defecto en el ecosistema de React. Tenía gran popularidad y facilitaba el enrutamiento inicial. Sin embargo, conforme el código creció hasta superar miles de componentes, el equipo empezó a sufrir una pesadilla técnica interna.
JORGE: En publicaciones sumamente francas en su blog técnico y en Reddit, los ingenieros de Plane confesaron la cruda verdad: el servidor de desarrollo de Next tardaba entre veinte y treinta segundos en reflejar un cambio simple de código en pantalla. Cada vez que un desarrollador modificaba un botón o un estilo, tenía que esperar medio minuto para ver el resultado. Además, Plane es una aplicación interactiva que vive detrás de una pantalla de inicio de sesión; no es un periódico digital ni un blog de comercio electrónico que requiera renderizado en el servidor para posicionamiento en Google.
DALIA: Next punto j-s forzaba capas innecesarias de complejidad, hidratación en el cliente y contenedores de Docker pesados que consumían demasiada memoria en los servidores pequeños de los usuarios de self-hosting. Así que el equipo tomó una decisión que la mayoría de las empresas teme: en su versión uno punto cero, reescribieron más de mil doscientos archivos y veinte mil líneas de código para extirpar a Next punto j-s y migrar todo el frontend a React Router en modo framework junto a Vite.
JORGE: El cambio fue instantáneo: las recargas en caliente pasaron de treinta segundos a milisegundos imperceptibles. Los paquetes de despliegue para Docker se aligeraron drásticamente y la fluidez de navegación para el usuario final alcanzó la velocidad que los desarrolladores siempre habían soñado. Demostraron que la verdadera madurez técnica no es seguir la moda de los frameworks de moda, sino tener la valentía de elegir la herramienta correcta para el problema real.

[CHAPTER: 07. 🌌 Fuera de la Burbuja: La Tensión del Open-Core y la Soberanía]
DALIA: Entremos a nuestra cápsula Fuera de la Burbuja, porque no todo es idílico en el mundo del código abierto y es necesario hablar de las tensiones reales.
JORGE: En comunidades como r diagonal selfhosted, Plane ha sido celebrado como un héroe, pero también ha generado debates intensos sobre el modelo de negocio open-core. Algunos usuarios expresaron inquietud cuando ciertas funciones avanzadas de nivel corporativo se reservaron para la versión comercial de pago. Los fundadores tuvieron que ser muy transparentes: mantener a decenas de ingenieros de tiempo completo resolviendo errores y actualizando el software exige sostenibilidad financiera; de lo contrario, el proyecto muere abandonado como tantos repositorios de GitHub.
DALIA: A pesar de esos debates, el impacto de Plane es innegable: le ha devuelto a miles de equipos de tecnología la soberanía de sus propios datos. Saber que tus proyectos, tus discusiones internas y tus hojas de ruta están seguras en tu propio servidor, sin temor a que una corporación te duplique el precio de la noche a la mañana o te cierre el servicio, es una tranquilidad que el dinero de las suscripciones corporativas no puede comprar.

[CHAPTER: 08. Cierre Íntimo & Comunidad]
JORGE: Plane nos recuerda una lección fundamental de la ingeniería moderna: cuando una herramienta que usamos todos los días se vuelve lenta, arrogante y costosa, la respuesta de la comunidad de desarrolladores nunca es resignarse; la respuesta siempre es abrir una terminal, escribir código y construir algo mejor.
DALIA: Si deseas consultar los diagramas de arquitectura de la migración de Next a Vite de Plane, y revisar los enlaces al repositorio de GitHub con bibliografía técnica en formato APA, visita nuestra revista digital en escucha guion sia punto github punto io.
JORGE: Muchísimas gracias por acompañarnos en este viaje por las trincheras del software libre. Déjanos en los comentarios qué opinas de Jira, si has probado Plane o Linear, y qué otro gran proyecto de código abierto te gustaría que analicemos a fondo. Que tengas una excelente jornada... y nos escuchamos en el próximo episodio de Sia.
DALIA: Hasta la próxima.
"""

def clean_for_tts(text: str) -> str:
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    t = re.sub(r'\bsIA\b', 'Sia', t)
    t = re.sub(r'\bSIA\b', 'Sia', t)
    t = re.sub(r'\bJira\b', 'Yira', t)
    t = re.sub(r'\bLinear\b', 'Línear', t)
    t = re.sub(r'\bNext\.js\b', 'Next yei-es', t)
    t = re.sub(r'\bNext\b', 'Next', t)
    t = re.sub(r'\bVite\b', 'Vait', t)
    t = re.sub(r'\bVamsi Kurama\b', 'Vamsi Kuráma', t)
    t = re.sub(r'\bVihar Kurama\b', 'Vijar Kuráma', t)
    t = re.sub(r'\bKurama\b', 'Kuráma', t)
    t = re.sub(r'\bHyderabad\b', 'Jáiderabad', t)
    t = re.sub(r'\bAGPL\b', 'A G P L', t)
    t = re.sub(r'\bOSS Capital\b', 'O S S Capital', t)
    t = re.sub(r'\bDocker Compose\b', 'Dóker Compous', t)
    t = re.sub(r'\bDocker\b', 'Dóker', t)
    t = re.sub(r'\bPostgres\b', 'Póstgres', t)
    t = re.sub(r'\bSPA\b', 'S P A', t)
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

        # 1. Cold Open, Monopolio Atlassian y Cierre: Piano reflexivo emocional
        if any(k in ch for k in ["Cold Open", "Monopolio de Atlassian", "Cierre"]):
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

        # 2. La Batalla de los 1,200 Archivos (Ingeniería y Vite): Tecleo Keychron acústico
        if "Batalla de los Mil Doscientos Archivos" in ch and typing_keychron.exists():
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

        # 3. Hyderabad y Fuera de la Burbuja: Acústica suave de oficina
        if ("Hyderabad" in ch or "Fuera de la Burbuja" in ch) and office_ambiance.exists():
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
    print("🎙️ PRODUCCIÓN: sIA DEEP DIVE #48 (PLANE VS JIRA & VITE REVOLUTION)")
    print("===========================================================================")
    
    chapters, dialogues = parse_script(SCRIPT_PLANE)
    
    # 1. Sintetizar bloques vocales
    raw_files = await synthesize_dialogue(dialogues)
    
    # 2. Aplicar capas de diseño sonoro
    mixed_files = apply_sound_design_and_mix(raw_files, dialogues)
    
    # 3. Concatenación y subtítulos
    print("\nCalculando duraciones exactas y generando subtítulos WebVTT / SRT...")
    concat_list = TEMP_DIR / "concat_list.txt"
    vtt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.vtt"
    srt_path = AUDIO_DIR / f"{Path(EPISODE_INFO['filename']).stem}.srt"
    
    vtt_lines = ["WEBVTT - sIA #48: Plane vs Jira: La Rebelión Open Source\n"]
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
        "-metadata", "album=sIA Deep Dive",
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
      <guid isPermaLink="false">sia-deepdive-plane-opensource-jira-alternative</guid>
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
            "sIA Deep Dive #48: Plane (makeplane/plane) y la rebelión de código abierto contra Jira",
            "La muerte de Jira Server y el hartazgo de los desarrolladores en Reddit r/programming",
            "La tentación de Linear: elegancia estética versus el jardín vallado propietario",
            "Los hermanos Vamsi y Vihar Kurama: de Hyderabad a $4M con OSS Capital bajo AGPLv3",
            "La migración masiva de 1,200 archivos: por qué abandonaron Next.js para abrazar Vite y React Router"
        ],
        "cooldown_days": 45,
        "date": datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro de memoria añadido a news_vault.json.")

if __name__ == '__main__':
    asyncio.run(produce_episode())
