import sys
import os
import re
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VOICE_MALE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

AUDIO_DIR = Path(r"C:\Carlos\noticias_podcast\audio")
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
TEMP_DIR = Path(r"C:\Carlos\noticias_podcast\temp_chunks")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

async def synthesize_chunk(text: str, voice: str, output_path: Path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))

def clean_for_tts(text: str) -> str:
    # Phonetic cleanups for TTS fluency
    t = text.strip()
    t = re.sub(r'[*_#`]', '', t)
    # Expand acronyms for clean Spanish TTS reading
    t = re.sub(r'\bGCP\b', 'G C P', t)
    t = re.sub(r'\bAI Studio\b', 'A I Studio', t)
    t = re.sub(r'\bGoogle AI\b', 'Google A I', t)
    t = re.sub(r'\bdbt\b', 'd b t', t)
    t = re.sub(r'\bBigQuery\b', 'Big-Kueri', t)
    t = re.sub(r'\bSoC\b', 'S o C', t)
    t = re.sub(r'\bSAO\b', 'S A O', t)
    t = re.sub(r'\bTTS\b', 'T T S', t)
    t = re.sub(r'\bAPI\b', 'A P I', t)
    t = re.sub(r'\bOne UI\b', 'Uan U I', t)
    # Impresión 3D y Bambu Lab
    t = re.sub(r'\bAMS\b', 'A M S', t)
    t = re.sub(r'\bLiDAR\b', 'Láidar', t)
    t = re.sub(r'\bX1-Carbon\b', 'X uno Carbón', t)
    t = re.sub(r'\bX1C\b', 'X uno C', t)
    t = re.sub(r'\bP1S\b', 'P uno S', t)
    t = re.sub(r'\bA1\b', 'A uno', t)
    t = re.sub(r'\bOrcaSlicer\b', 'Orca Slaiser', t)
    t = re.sub(r'\bMakerWorld\b', 'Meiker-güorld', t)
    t = re.sub(r'\bFDM\b', 'F D M', t)
    t = re.sub(r'\bPLA\b', 'P L A', t)
    t = re.sub(r'\bPETG\b', 'P E T G', t)
    t = re.sub(r'\bTPU\b', 'T P U', t)
    # Modelos de Decisión y JEPA / Jev
    t = re.sub(r'\bJEPA\b', 'Yepa', t)
    t = re.sub(r'\bI-JEPA\b', 'I-Yepa', t)
    t = re.sub(r'\bV-JEPA\b', 'V-Yepa', t)
    t = re.sub(r'\bLeCun\b', 'LeCún', t)
    t = re.sub(r'\bJev\b', 'Yeb', t, flags=re.IGNORECASE)
    t = re.sub(r'\bYev\b', 'Yeb', t, flags=re.IGNORECASE)
    t = re.sub(r'\bTypeSafe AI\b', 'Taip-Seif A I', t)
    t = re.sub(r'\bTypeSafe\b', 'Taip-Seif', t)
    t = re.sub(r'\bDotCSV\b', 'Dot C S V', t)
    t = re.sub(r'\bDOOM\b', 'Dum', t)
    # Laya y Stack Agéntico Open Source
    t = re.sub(r'\bn8n\b', 'ene ocho ene', t)
    t = re.sub(r'\bChromaDB\b', 'Croma D B', t)
    t = re.sub(r'\bSQLite\b', 'Es-Kiu-Lait', t)
    t = re.sub(r'\bFTS5\b', 'F T S cinco', t)
    t = re.sub(r'\bSvelte\b', 'Esvelt', t)
    t = re.sub(r'\bLiteLLM\b', 'Lait L L M', t)
    t = re.sub(r'\bBYOK\b', 'B Y O K', t)
    # Ecosistema Cloud, Datos y Modelos
    t = re.sub(r'\bPostgreSQL\b', 'Postgres', t, flags=re.IGNORECASE)
    t = re.sub(r'\bPostgres\b', 'Postgres', t, flags=re.IGNORECASE)
    t = re.sub(r'\bMySQL\b', 'Mai-Es-Kiu-El', t)
    t = re.sub(r'\bDocker\b', 'Dóquer', t)
    t = re.sub(r'\bK8s\b', 'Ka ocho ese', t)
    t = re.sub(r'\bPyTorch\b', 'Pai-Torch', t)
    t = re.sub(r'\bHugging Face\b', 'Jaguíng Feis', t, flags=re.IGNORECASE)
    t = re.sub(r'\bLangChain\b', 'Lang-Chein', t, flags=re.IGNORECASE)
    t = re.sub(r'\bDatabricks\b', 'Data-briks', t, flags=re.IGNORECASE)
    t = re.sub(r'\bSnowflake\b', 'Snou-fleik', t, flags=re.IGNORECASE)
    t = re.sub(r'\bGitHub\b', 'Git-Jab', t, flags=re.IGNORECASE)
    t = re.sub(r'\bOpenAI\b', 'Open A I', t, flags=re.IGNORECASE)
    t = re.sub(r'\bFastAPI\b', 'Fast A P I', t)
    t = re.sub(r'\bAirflow\b', 'Eir-flou', t, flags=re.IGNORECASE)
    t = re.sub(r'\bDagster\b', 'Dags-ter', t, flags=re.IGNORECASE)
    t = re.sub(r'\bLLMs\b', 'L L Ms', t)
    t = re.sub(r'\bLLM\b', 'L L M', t)
    t = re.sub(r'\bRAG\b', 'Rag', t)
    t = re.sub(r'\bMCP\b', 'M C P', t)
    # Hardware, E-Ink y Serendipia
    t = re.sub(r'\bACeP\b', 'A C E P', t)
    t = re.sub(r'\bGallery 3\b', 'Gálery tres', t)
    t = re.sub(r'\bKaleido 3\b', 'Caleido tres', t)
    t = re.sub(r'\bppi\b', 'P P I', t, flags=re.IGNORECASE)
    t = re.sub(r'\bADN\b', 'A D N', t)
    t = re.sub(r'\bDNA\b', 'D N A', t)
    t = re.sub(r'\bKOReader\b', 'Kei-Ou-Ríder', t)
    t = re.sub(r'\bCalibre\b', 'Cálibre', t)
    t = re.sub(r'\bgVisor\b', 'Yi-Váisor', t)
    t = re.sub(r'\bFirecracker\b', 'Fáier-cráquer', t)
    t = re.sub(r'\bAnthropic\b', 'Antrópic', t)
    t = re.sub(r'\bClaude\b', 'Clod', t)
    t = re.sub(r'\bCTE\b', 'C T E', t)
    t = re.sub(r'\bCTEs\b', 'C T Es', t)
    t = re.sub(r'\bEXPLAIN\b', 'Expléin', t)
    return t



async def process_dialogue(script_text: str, episode_title: str, custom_filename: str = None, episode_description: str = None) -> Path:
    lines = script_text.strip().split('\n')
    chunks = []
    chunk_index = 0
    
    # Clean temp dir
    for f in TEMP_DIR.glob("*.mp3"):
        try:
            f.unlink()
        except Exception:
            pass

    current_speaker = None
    current_text = []
    current_chapter = "Introducción"

    def commit_current_block():
        nonlocal chunk_index
        if current_speaker and current_text:
            combined_text = " ".join(current_text).strip()
            if combined_text:
                cleaned = clean_for_tts(combined_text)
                voice = VOICE_MALE if current_speaker == "JORGE" else VOICE_FEMALE
                chunk_file = TEMP_DIR / f"chunk_{chunk_index:04d}_{current_speaker.lower()}.mp3"
                chunks.append((chunk_file, cleaned, voice, current_speaker, current_chapter))
                chunk_index += 1

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
            
        if line_s.startswith('[SFX:') or line_s.startswith('[sfx:'):
            continue

        # Check for chapter marker
        ch_match = re.match(r'^\[(?:CHAPTER|BLOQUE|ACTO)\s*:\s*(.*?)\]', line_s, re.IGNORECASE)
        if ch_match:
            commit_current_block()
            current_chapter = ch_match.group(1).strip()
            continue
            
        # Detect speaker
        jorge_match = re.match(r'^(JORGE|HOST 1|LOCUTOR 1|CARLOS)\s*:\s*(.*)$', line_s, re.IGNORECASE)
        dalia_match = re.match(r'^(DALIA|HOST 2|LOCUTOR 2|SOFIA|ELENA)\s*:\s*(.*)$', line_s, re.IGNORECASE)
        
        if jorge_match:
            commit_current_block()
            current_speaker = "JORGE"
            current_text = [jorge_match.group(2)]
        elif dalia_match:
            commit_current_block()
            current_speaker = "DALIA"
            current_text = [dalia_match.group(2)]
        else:
            if current_speaker:
                current_text.append(line_s)

    commit_current_block()

    if not chunks:
        raise ValueError("No se encontraron intervenciones con formato 'JORGE:' o 'DALIA:' en el guion.")

    print(f"Generando {len(chunks)} intervenciones de voz para el dúo con concurrencia...")
    
    # Synthesize chunks with concurrency limit
    sem = asyncio.Semaphore(6)
    completed_count = 0
    total_chunks = len(chunks)

    async def worker(chunk_file, text, voice, speaker):
        nonlocal completed_count
        async with sem:
            await synthesize_chunk(text, voice, chunk_file)
            completed_count += 1
            if completed_count % 10 == 0 or completed_count == total_chunks:
                print(f"  [{completed_count}/{total_chunks}] Sintetizado con éxito...")

    tasks = [worker(cf, txt, v, spk) for cf, txt, v, spk, ch in chunks]
    await asyncio.gather(*tasks)

    # Calculate chunk durations and chapters
    print("Calculando duración exacta y marcadores de capítulos...")
    chapter_spans = []
    current_ch_name = None
    ch_start_ms = 0
    current_time_ms = 0

    concat_list_file = TEMP_DIR / "concat_list.txt"
    with open(concat_list_file, 'w', encoding='utf-8') as f:
        for chunk_file, _, _, _, ch_name in chunks:
            path_str = str(chunk_file).replace('\\', '/')
            f.write(f"file '{path_str}'\n")

            dur_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(chunk_file)]
            dur_res = subprocess.run(dur_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                dur_sec = float(dur_res.stdout.strip())
            except Exception:
                dur_sec = 2.0
            dur_ms = int(dur_sec * 1000)

            if ch_name != current_ch_name:
                if current_ch_name is not None:
                    chapter_spans.append((current_ch_name, ch_start_ms, current_time_ms))
                current_ch_name = ch_name
                ch_start_ms = current_time_ms

            current_time_ms += dur_ms

    if current_ch_name is not None:
        chapter_spans.append((current_ch_name, ch_start_ms, current_time_ms))

    # Generate FFMETADATA file with ID3v2 chapters
    meta_lines = [
        ";FFMETADATA1\n",
        f"title={episode_title}\n",
        "artist=Jorge y Dalia (sIA)\n",
        "album=sIA\n",
        "genre=Podcast\n",
        f"date={datetime.now().strftime('%Y')}\n\n"
    ]
    if chapter_spans:
        for ch_title, s_ms, e_ms in chapter_spans:
            meta_lines.append(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={s_ms}\nEND={e_ms}\ntitle={ch_title}\n\n")

    meta_file = TEMP_DIR / "chapters_metadata.txt"
    meta_file.write_text("".join(meta_lines), encoding='utf-8')

    # Generate output filenames
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = custom_filename or f"sIA_{today_str}.mp3"
    final_output = AUDIO_DIR / output_filename
    spotify_output = SPOTIFY_DIR / output_filename

    print("\nEnsamblando audio final con capítulos ID3v2 en ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-i", str(meta_file),
        "-map_metadata", "1",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-id3v2_version", "3",
        str(final_output)
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error en ffmpeg:", res.stderr)
        raise RuntimeError("Fallo al ensamblar con ffmpeg")

    # Copy to Spotify local directory
    import shutil
    shutil.copy2(final_output, spotify_output)
    print(f"\n[OK] Episodio master generado en: {final_output}")
    print(f"[OK] Sincronizado en carpeta de Spotify: {spotify_output}")

    # Generate/Update RSS
    update_podcast_rss(episode_title, output_filename, final_output, description=episode_description)
    return final_output

CONFIG_FILE = Path(r"C:\Carlos\noticias_podcast\podcast_config.json")

def get_podcast_email() -> str:
    if CONFIG_FILE.exists():
        try:
            import json
            data = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
            return data.get("owner_email", "")
        except Exception:
            pass
    return ""

def get_audio_duration_str(filepath: Path) -> str:
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(filepath)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        secs = float(res.stdout.strip())
        m, s = divmod(int(secs), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
    except Exception:
        return "05:00"

def update_podcast_rss(episode_title: str, filename: str, filepath: Path, email_address: str = None, description: str = None):
    if not email_address:
        email_address = get_podcast_email() or "charly.corona@gmail.com"
    rss_file = AUDIO_DIR / "podcast.xml"
    file_size = filepath.stat().st_size
    pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    base_url = "https://escucha-sia.github.io"
    audio_url = f"{base_url}/audio/{filename}"
    cover_url = f"{base_url}/cover.jpg"
    desc_text = description or "sIA: Análisis técnico y estratégico de Inteligencia Artificial, Cloud, Data Engineering, Gadgets y Cultura Geek con Jorge y Dalia."
    dur_str = get_audio_duration_str(filepath)
    
    new_item = f"""    <item>
      <title>{episode_title}</title>
      <description>{desc_text}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}" length="{file_size}" type="audio/mpeg"/>
      <guid isPermaLink="true">{audio_url}</guid>
      <itunes:duration>{dur_str}</itunes:duration>
      <itunes:author>Jorge y Dalia</itunes:author>
      <itunes:image href="{cover_url}"/>
      <itunes:explicit>no</itunes:explicit>
    </item>"""

    # Preserve existing items and position if updating
    found_and_replaced = False
    new_items_list = []
    if rss_file.exists():
        try:
            content = rss_file.read_text(encoding='utf-8')
            items_found = re.findall(r'<item>.*?</item>', content, re.DOTALL)
            for it in items_found:
                if audio_url in it:
                    # Update in place, preserving existing pubDate and link
                    m_date = re.search(r'<pubDate>(.*?)</pubDate>', it)
                    orig_date = m_date.group(1) if m_date else pub_date
                    m_link = re.search(r'<link>(.*?)</link>', it)
                    link_line = f"\n      <link>{m_link.group(1)}</link>" if m_link else ""
                    
                    updated_it = f"""    <item>
      <title>{episode_title}</title>{link_line}
      <description>{desc_text}</description>
      <pubDate>{orig_date}</pubDate>
      <enclosure url="{audio_url}" length="{file_size}" type="audio/mpeg"/>
      <guid isPermaLink="true">{audio_url}</guid>
      <itunes:duration>{dur_str}</itunes:duration>
      <itunes:author>Jorge y Dalia</itunes:author>
      <itunes:image href="{cover_url}"/>
      <itunes:explicit>no</itunes:explicit>
    </item>"""
                    new_items_list.append(updated_it)
                    found_and_replaced = True
                else:
                    new_items_list.append(f"    {it.strip()}")
        except Exception as e:
            print(f"[WARN] Error leyendo items existentes de RSS: {e}")

    if not found_and_replaced:
        new_items_list.insert(0, new_item)

    all_items = new_items_list
    items_block = "\n".join(all_items)

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>sIA</title>
    <link>{base_url}</link>
    <language>es-mx</language>
    <itunes:author>Jorge y Dalia</itunes:author>
    <itunes:image href="{cover_url}"/>
    <itunes:category text="Technology"/>
    <itunes:owner>
      <itunes:name>Carlos Corona</itunes:name>
      <itunes:email>{email_address}</itunes:email>
    </itunes:owner>
    <description>sIA: El podcast diario de Inteligencia Artificial, Cloud, Big Data, Gadgets y Cultura Geek presentado por Jorge y Dalia.</description>
{items_block}
  </channel>
</rss>"""
    rss_file.write_text(rss_content, encoding='utf-8')
    root_rss = Path(r"C:\Carlos\noticias_podcast\podcast.xml")
    root_rss.write_text(rss_content, encoding='utf-8')
    print(f"[OK] Feed RSS actualizado con {len(all_items)} episodios: {rss_file}")
    
    # Auto-rebuild digital magazine and APA research articles
    try:
        from build_magazine import build_all_articles
        build_all_articles()
    except Exception as e:
        print(f"[WARN] Error al regenerar revista digital: {e}")

if __name__ == '__main__':
    # Test script if executed directly
    sample_script = """
    JORGE: ¡Hola a toda nuestra audiencia! Bienvenidos a sIA, tu dosis técnica diaria para el camino.
    DALIA: Hola a todos. Hoy tenemos noticias muy potentes en Google AI Studio, BigQuery y el despliegue de Android 17 en la serie S25 de Samsung.
    JORGE: Así es Dalia. En Google anunciaron la transición de los clásicos Gems hacia Skills modulares en Workspace y Gemini.
    DALIA: Y en el mundo geek, Reki Kawahara acaba de lanzar el tráiler de su nuevo anime y la próxima película de Sword Art Online. ¡Comencemos!
    """
    asyncio.run(process_dialogue(sample_script, "Piloto de Prueba - NoticIAs Dúo"))
