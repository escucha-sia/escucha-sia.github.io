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

    def commit_current_block():
        nonlocal chunk_index
        if current_speaker and current_text:
            combined_text = " ".join(current_text).strip()
            if combined_text:
                cleaned = clean_for_tts(combined_text)
                voice = VOICE_MALE if current_speaker == "JORGE" else VOICE_FEMALE
                chunk_file = TEMP_DIR / f"chunk_{chunk_index:03d}_{current_speaker.lower()}.mp3"
                chunks.append((chunk_file, cleaned, voice, current_speaker))
                chunk_index += 1

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
            
        if line_s.startswith('[SFX:') or line_s.startswith('[sfx:'):
            # Sound effect marker
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

    print(f"Generando {len(chunks)} intervenciones de voz para el dúo...")
    
    # Synthesize each chunk
    for idx, (chunk_file, text, voice, speaker) in enumerate(chunks, 1):
        print(f"  [{idx}/{len(chunks)}] Sintetizando {speaker} ({voice}): \"{text[:40]}...\"")
        await synthesize_chunk(text, voice, chunk_file)

    # Create concat list for ffmpeg
    concat_list_file = TEMP_DIR / "concat_list.txt"
    with open(concat_list_file, 'w', encoding='utf-8') as f:
        for chunk_file, _, _, _ in chunks:
            # Escape path for ffmpeg concat
            path_str = str(chunk_file).replace('\\', '/')
            f.write(f"file '{path_str}'\n")

    # Generate output filenames
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = custom_filename or f"sIA_{today_str}.mp3"
    final_output = AUDIO_DIR / output_filename
    spotify_output = SPOTIFY_DIR / output_filename

    print("\nEnsamblando audio con ffmpeg...")
    # Concat and add ID3 metadata
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-metadata", f"title={episode_title}",
        "-metadata", "artist=Jorge y Dalia (sIA)",
        "-metadata", "album=sIA",
        "-metadata", "genre=Podcast",
        "-metadata", f"date={datetime.now().strftime('%Y')}",
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
    
    new_item = f"""    <item>
      <title>{episode_title}</title>
      <description>{desc_text}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}" length="{file_size}" type="audio/mpeg"/>
      <guid isPermaLink="true">{audio_url}</guid>
      <itunes:author>Jorge y Dalia</itunes:author>
      <itunes:image href="{cover_url}"/>
      <itunes:explicit>no</itunes:explicit>
    </item>"""

    # Preserve existing items
    existing_items = []
    if rss_file.exists():
        try:
            content = rss_file.read_text(encoding='utf-8')
            items_found = re.findall(r'<item>.*?</item>', content, re.DOTALL)
            for it in items_found:
                if audio_url not in it:
                    existing_items.append(f"    {it.strip()}")
        except Exception as e:
            print(f"[WARN] Error leyendo items existentes de RSS: {e}")

    all_items = [new_item] + existing_items
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
    JORGE: ¡Hola Carlos! Bienvenidos a NoticIAs Dúo, tu dosis técnica diaria para el camino.
    DALIA: Hola a todos. Hoy tenemos noticias muy potentes en Google AI Studio, BigQuery y el despliegue de Android 17 en la serie S25 de Samsung.
    JORGE: Así es Dalia. En Google anunciaron la transición de los clásicos Gems hacia Skills modulares en Workspace y Gemini.
    DALIA: Y en el mundo geek, Reki Kawahara acaba de lanzar el tráiler de su nuevo anime y la próxima película de Sword Art Online. ¡Comencemos!
    """
    asyncio.run(process_dialogue(sample_script, "Piloto de Prueba - NoticIAs Dúo"))
