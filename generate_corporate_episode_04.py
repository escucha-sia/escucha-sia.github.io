"""
sIA Crónicas Corporativas #04: Marc Lore vs. Amazon: La Guerra de los Pañales y el Dilema del Fundador
- Enfoque Humano y Empático: De la angustia de un padre en una noche de nieve al choque de $100 millones con Jeff Bezos.
- Diseño Sonoro Real de Estudio: Piano emocional (Kevin MacLeod - Isolated), acústica de oficina y tecleo Keychron real.
- Masterización Broadcast EBU R128 (-16 LUFS) y compresión dinámica: volumen 100% estable.
- Sin términos informales: Crónicas Corporativas e Historia Empresarial.
- Volante tripartito omnicanal: Audio, Artículo con citas APA y Reel de 45 segundos.
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
TEMP_DIR = BASE_DIR / "temp_chunks_corp_04"
AUDIO_LIB = BASE_DIR / "assets" / "audio_library"
NEWS_VAULT = BASE_DIR / "news_vault.json"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

EPISODE_INFO = {
    "title": "sIA Corporativo #04: Marc Lore vs. Amazon: La Guerra de los Pañales y el Dilema del Fundador",
    "filename": "sIA_Corp_04_Marc_Lore_Amazon_Diapers_2026-10-23.mp3",
    "description": "sIA Crónicas Corporativas #04: El drama humano detrás de Diapers.com y Amazon. La noche de nieve en que un padre agotado concibió una empresa para ayudar a otras familias, la negativa a vender ante Jeff Bezos, la guerra de precios automatizada donde Amazon perdió $100 millones para destruirlos, el doloroso dilema moral de un fundador para proteger los empleos de su gente y el épico renacimiento con Jet.com y Walmart. | Leer artículo y cronología APA: https://escucha-sia.github.io/articulos/sia-corporativo-04-marc-lore-vs-amazon-guerra-panales.html"
}

SCRIPT_CORP_04 = """
[CHAPTER: 01. Cold Open: La Tormenta de Nieve y el Llanto de las Tres AM]
JORGE: Invierno de dos mil cinco en Montclair, Nueva Jersey. Afuera cae una tormenta de aguanieve que congela las ventanas. Adentro, en una recámara a media luz, un bebé de seis meses llora desconsolado con la piel irritada. Marc Lore, un padre joven de treinta y cuatro años, busca con desesperación en los cajones del cambiador. No queda ni un solo pañal limpio. Las farmacias están cerradas por el temporal. Y mientras sostiene a su hijo en brazos intentando calmarlo en la madrugada, siente una punzada de impotencia que todo padre o madre conoce de memoria. En ese preciso instante, con los ojos inyectados en sangre por el desvelo, nació una idea. No para construir un imperio multimillonario... sino para que ninguna otra familia tuviera que pasar por esa misma angustia a mitad de la noche.

[CHAPTER: 02. Prólogo & Brújula: sIA Crónicas Corporativas]
DALIA: Hola, ¿cómo estás? Qué gusto saludarte esta noche. Mi nombre es Dalia...
JORGE: ... y yo soy Jorge. Te damos una cálida bienvenida a Sia.
DALIA: Para quienes nos acompañan por primera vez o vienen de Spotify, YouTube o TikTok, te damos la bienvenida a nuestra casa. En Sia exploramos el impacto humano de la tecnología. Y hoy estás en sIA Crónicas Corporativas: el espacio donde abrimos los expedientes más íntimos de la historia empresarial. Aquí no venimos a recitar balances financieros ni comunicados de prensa; venimos a contar las batallas de supervivencia, los dilemas morales y las cicatrices personales de quienes arriesgaron todo por una idea.
JORGE: Y hoy abrimos uno de los capítulos más dramáticos y aleccionadores en la historia del comercio moderno: la guerra asimétrica entre un padre de familia y la corporación más implacable del planeta: Marc Lore contra Amazon y la Guerra de los Cien Millones de Dólares.

[CHAPTER: 03. Los Tres Momentos de la Bitácora]
DALIA: Jorge, cuando investigamos este caso, descubrimos que no fue una simple adquisición comercial; fue una tragedia humana en tres actos que marcó un antes y un después para cualquier persona que sueñe con emprender. Para que nos acompañes con los cinco sentidos, fíjate en estos tres momentos clave de la noche: Primero: Cómo dos amigos de la infancia crearon una empresa basada en la empatía pura hacia las madres trabajadoras, empacando cajas a mano en un almacén congelado. Segundo: La llamada telefónica de Seattle donde Jeff Bezos les ofreció comprar su empresa... y la venganza automatizada que desató cuando Marc se negó a vender su sueño. Y tercero: La madrugada en que Marc tuvo que sentarse solo en la sala de su casa a decidir entre su orgullo personal... o la supervivencia económica de las doscientas cincuenta familias que dependían de él.
JORGE: Presta mucha atención a cada detalle de este viaje. Ponte cómodo, ajusta tus audífonos, respira profundo... y acompáñanos a alcanzar el corazón de esta historia.

[CHAPTER: 04. El Almacén Congelado de Nueva Jersey]
DALIA: Marc Lore no venía del glamur de Silicon Valley ni tenía millones en el banco. Se asoció con su mejor amigo de la infancia, Vinit Bharara. Ambos sabían que ser padres primerizos es agotador: no tienes tiempo, estás cansado y cargar cajas de pañales de veinte kilos en el supermercado con un bebé en brazos es una pesadilla logística. Así fundaron Diapers punto com.
JORGE: Al principio no tenían dinero para camiones ni tecnología avanzada. Alquilaban una esquina en un almacén sin calefacción en las afueras de Jersey City. En los inviernos de dos mil cinco y dos mil seis, Marc y Vinit envolvían los pedidos con cinta adhesiva usando guantes de lana con los dedos cortados porque el frío les entumecía las manos. Pero tenían una obsesión: si una madre pedía pañales a las seis de la tarde, la caja tenía que estar en la puerta de su casa a la mañana siguiente sin falta.
DALIA: Incluían notas escritas a mano dentro de cada paquete deseándoles una noche de descanso a los padres. Ese trato humano y cálido detonó un fenómeno de recomendación descomunal: las comunidades de madres en foros de internet empezaron a recomendar el servicio como si fuera un salvavidas familiar. En menos de tres años, la empresa ya despachaba millones de pedidos al año y facturaba trescientos millones de dólares. Se habían ganado el cariño genuino de cientos de miles de hogares.

[CHAPTER: 05. La Invitación a Seattle y el Ultimátum]
JORGE: Pero en el mundo corporativo, cuando te vuelves indispensable para la gente, despiertas a los gigantes. Y en Seattle, Jeff Bezos vio con alarma cómo un porcentaje masivo de las madres estadounidenses ya no buscaban pañales en Amazon; iban directamente a Diapers punto com. En dos mil nueve, Bezos invitó a Marc Lore a las oficinas centrales de Amazon para un almuerzo privado.
DALIA: Ponte en el lugar de Marc: llegas a la torre de Amazon con tu carpeta bajo el brazo, sintiendo orgullo por lo que tú y tu amigo levantaron desde cero. Pero la reunión no fue una charla cordial de felicitaciones. Los ejecutivos de Bezos fueron cortantes y directos: 'Amazon va a entrar de lleno al negocio de bebés. Queremos comprar su empresa. Si aceptan, se integran a nosotros. Si no aceptan... vamos a competir'.
JORGE: Marc Lore miró la mesa y dijo con dignidad: 'No estamos en venta. Este es nuestro proyecto de vida, conocemos a nuestros clientes y creemos en lo que estamos construyendo'. Se levantó, estrechó manos y tomó el vuelo de regreso a Nueva Jersey creyendo que competirían en igualdad de condiciones, con mejor servicio y calidad humana. No tenía idea de la trampa letal que se estaba cerrando sobre él.

[CHAPTER: 06. La Guerra Suicida de los Cien Millones]
DALIA: Pocos meses después, los analistas de sistemas de Diapers punto com notaron algo insólito en sus paneles de tráfico. Un enjambre de bots automáticos rastreaba cada producto de su catálogo cada quince minutos. Y casi de inmediato, Amazon lanzó un servicio especial reduciendo el precio de los pañales en un treinta por ciento. Cada vez que Diapers punto com bajaba un centavo para no perder a sus clientes, el bot de Amazon bajaba dos centavos más.
JORGE: Marc Lore hizo los cálculos matemáticos en una hoja de cálculo y se le cayó el alma a los pies: Amazon estaba vendiendo cada paquete de pañales muy por debajo de su costo de fábrica y asumiendo los gastos de envío gratis. Documentos internos desclasificados años más tarde por el Congreso de los Estados Unidos revelaron que Amazon perdió deliberadamente cien millones de dólares en solo tres meses en esa categoría. Cien millones de dólares quemados a propósito, una cifra que para Amazon era una pequeña raspadura en su balance global, pero que para una empresa mediana independiente significaba la asfixia total de su flujo de caja.
DALIA: Los inversionistas de Diapers punto com entraron en pánico. Se negaron a inyectar más capital para sostener una guerra de desgaste contra un titán con reservas infinitas. El dinero en el banco de Marc se evaporaba día tras día. Las madres seguían amando el servicio, pero Amazon las estaba atrayendo con descuentos imposibles de igualar.

[CHAPTER: 07. La Madrugada del Dilema Moral]
JORGE: Octubre de dos mil diez. Marc Lore pasó noches enteras sin dormir, caminando en círculos por la sala de su casa mientras su familia dormía. Su socio Vinit y él sabían que podían resistir un par de meses más apelando al orgullo y pelear hasta el último centavo. Pero si la empresa quebraba, más de doscientas cincuenta personas —los empacadores del almacén, los desarrolladores que habían confiado en ellos, los empleados de atención a clientes— se quedarían sin empleo de la noche a la mañana con las manos vacías.
DALIA: Esa es la soledad invisible del líder de la que nadie habla en los libros de negocios: cuando el costo de tu orgullo personal lo van a pagar las familias de la gente que creyó en ti. Con el dolor más profundo de su carrera, Marc tragó saliva, descolgó el teléfono y aceptó la oferta de adquisición de Amazon por quinientos cuarenta y cinco millones de dólares.
JORGE: Para los periódicos financieros, fue una salida exitosa que convirtió a los fundadores en millonarios. Pero para Marc Lore fue un duelo devastador: vio cómo Amazon absorbió la infraestructura y años después cerró la marca que él había creado con tanto amor para su hijo.

[CHAPTER: 08. 🌌 Fuera de la Burbuja: La Dulce Venganza de Jet punto com]
DALIA: Entremos a nuestra cápsula Fuera de la Burbuja, porque la historia no termina en la derrota. La resiliencia humana tiene formas poéticas de manifestarse.
JORGE: Marc Lore cumplió los dos años de contrato obligatorio trabajando dentro de Amazon, aprendiendo desde adentro cada tuerca de su logística algorítmica y acumulando paciencia. El día que venció su cláusula de no competencia, renunció inmediatamente. Y en dos mil catorce fundó Jet punto com, una plataforma de comercio electrónico diseñada específicamente con algoritmos de optimización de cesta para desafiar el monopolio de Amazon.
DALIA: Apenas dos años después, en dos mil dieciséis, el gigante minorista Walmart compró Jet punto com por tres mil trescientos millones de dólares y nombró a Marc Lore como el máximo responsable de todo el comercio digital de Walmart en Estados Unidos. Desde esa posición, Marc lideró la transformación digital que por fin logró arrebatarle cuota de mercado a Amazon a escala global. Aquel padre que en dos mil cinco no tenía un pañal en una noche de nieve en Nueva Jersey demostró que una corporación puede quitarte una empresa con dinero sucio, pero jamás podrá quitarte el talento, la visión y la dignidad de volver a empezar.

[CHAPTER: 09. Cierre Íntimo & Comunidad]
JORGE: Si quieres consultar los documentos desclasificados del Congreso sobre la guerra de precios de Amazon y el análisis estratégico de este caso con bibliografía en formato APA, revisa nuestra revista digital en escucha guion sia punto github punto io. Y en nuestro TikTok y YouTube Shorts ya tienes disponible el Reel de cuarenta y cinco segundos con la reconstrucción de esta batalla.
DALIA: Gracias de corazón por acompañarnos y reflexionar con nosotros sobre el lado humano de las grandes leyendas tecnológicas. Que tengas una excelente noche... y nos escuchamos en la próxima crónica de Sia.
JORGE: Hasta la próxima.
"""

def clean_for_tts(text: str) -> str:
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    # Pronunciación fonética de marca sIA -> 'Sia' (palabra corrida, no deletreada)
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

def mix_background(voice_file: Path, bg_file: Path, output_file: Path, bg_volume: float = 0.03):
    # normalize=0 mantiene 100% de la ganancia vocal sin bajadas repentinas
    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_file),
        "-i", str(bg_file),
        "-filter_complex", f"[1:a]volume={bg_volume}[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[out]",
        "-map", "[out]",
        str(output_file)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

async def produce_episode():
    print("=" * 75)
    print("🎙️ PRODUCCIÓN: sIA CRÓNICAS CORPORATIVAS #04 (MARC LORE VS AMAZON)")
    print("=" * 75)

    # 1. Limpiar carpeta temporal
    for f in TEMP_DIR.glob("*"):
        try:
            f.unlink()
        except Exception:
            pass

    # 2. Parsear el guion
    lines = SCRIPT_CORP_04.strip().split('\n')
    dialogue_blocks = []
    current_chapter = "01. Cold Open: La Tormenta de Nieve y el Llanto de las Tres AM"
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

    # 3. Aplicar capas de diseño sonoro con audio real de estudio
    print("\n🎛️ Aplicando capas de diseño sonoro de estudio (Música Kevin MacLeod & Keychron Acústico)...")
    music_tension = AUDIO_LIB / "music_isolated_tension.mp3"
    typing_foley = AUDIO_LIB / "typing_keychron.mp3"
    office_room = AUDIO_LIB / "office_ambiance.mp3"

    timeline_items = []
    
    # Bloque 0: Cold Open con Piano Emocional tenue de fondo (Isolated de Kevin MacLeod a -28 dB / 0.035)
    b0 = dialogue_blocks[0]
    mixed_b0 = TEMP_DIR / "processed_000_cold_open.mp3"
    mix_background(b0["raw_audio"], music_tension, mixed_b0, bg_volume=0.035)
    timeline_items.append((mixed_b0, b0["raw_text"], b0["speaker"], b0["chapter"]))

    # Bloques 1 a 3: Presentación cálida, Brújula y Los 3 Momentos de la Bitácora
    # Con música de piano tenue de fondo (Isolated a -30 dB / 0.025)
    for i in range(1, 4):
        b = dialogue_blocks[i]
        mixed_b = TEMP_DIR / f"processed_{i:03d}_intro_bed.mp3"
        mix_background(b["raw_audio"], music_tension, mixed_b, bg_volume=0.025)
        timeline_items.append((mixed_b, b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 4 a 6: El Almacén congelado, la llamada de Bezos y la guerra de los $100M
    # Con ambiente de oficina acústica y tecleo real de fondo muy sutil
    for i in range(4, 7):
        b = dialogue_blocks[i]
        mixed_b = TEMP_DIR / f"processed_{i:03d}_warehouse.mp3"
        mix_background(b["raw_audio"], typing_foley, mixed_b, bg_volume=0.04)
        timeline_items.append((mixed_b, b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 7 a 9: El dilema moral (piano emocional de tensión íntima)
    for i in range(7, 10):
        b = dialogue_blocks[i]
        mixed_b = TEMP_DIR / f"processed_{i:03d}_dilemma.mp3"
        mix_background(b["raw_audio"], music_tension, mixed_b, bg_volume=0.03)
        timeline_items.append((mixed_b, b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 10 a 16: La capitulación, el renacimiento con Jet.com y Walmart
    for i in range(10, 17):
        b = dialogue_blocks[i]
        timeline_items.append((b["raw_audio"], b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 17 a 19: Cápsula Fuera de la Burbuja
    for i in range(17, 20):
        b = dialogue_blocks[i]
        timeline_items.append((b["raw_audio"], b["raw_text"], b["speaker"], b["chapter"]))

    # Bloques 20 a 22: Cierre reflexivo de comunidad y despedida
    for i in range(20, len(dialogue_blocks)):
        b = dialogue_blocks[i]
        mixed_cierre = TEMP_DIR / f"processed_{i:03d}_cierre.mp3"
        mix_background(b["raw_audio"], music_tension, mixed_cierre, bg_volume=0.025)
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
        "artist=Jorge y Dalia (sIA Crónicas Corporativas)\n",
        "album=sIA Crónicas Corporativas\n",
        "genre=Podcast\n",
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

    # Ensamble final con ffmpeg y Masterización Broadcast EBU R128 (-16 LUFS)
    final_output = AUDIO_DIR / EPISODE_INFO["filename"]
    spotify_output = SPOTIFY_DIR / EPISODE_INFO["filename"]

    print("\n🎬 Ensamblando master final con Compresión Dinámica y Normalización EBU R128 (-16 LUFS)...")
    raw_master = TEMP_DIR / "raw_concat_master.mp3"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:a", "libmp3lame",
        "-b:a", "256k",
        str(raw_master)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(raw_master),
        "-i", str(meta_file),
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
      <guid isPermaLink="false">sia-corp-04-marc-lore-amazon-diapers</guid>
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
            "sIA Crónicas Corporativas #04: Marc Lore vs Amazon y la génesis de Diapers.com",
            "La noche de nieve en Nueva Jersey y el origen humano del servicio",
            "La reunión con Jeff Bezos en Seattle y el rechazo a la oferta hostil",
            "La guerra de precios algorítmica: Amazon perdiendo $100 millones deliberadamente",
            "El dilema moral de Marc Lore: proteger el sustento de 250 empleados",
            "El renacimiento con Jet.com y la venta a Walmart por $3,300 millones"
        ],
        "cooldown_days": 45,
        "date": datetime.now().strftime("%a, %d %b %Y 21:00:00 GMT")
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro de memoria añadido a news_vault.json.")

if __name__ == '__main__':
    asyncio.run(produce_episode())
