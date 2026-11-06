import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = BASE_DIR / "audio"
XML_FILE = BASE_DIR / "podcast.xml"
BUILD_MAG = BASE_DIR / "build_magazine.py"

def get_audio_meta(mp3_name: str):
    p = AUDIO_DIR / mp3_name
    if not p.exists():
        return 5500000, "05:30"
    size_bytes = p.stat().st_size
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p)
    ], capture_output=True, text=True)
    try:
        secs = int(float(res.stdout.strip()))
        mm = secs // 60
        ss = secs % 60
        dur_str = f"{mm:02d}:{ss:02d}"
    except Exception:
        dur_str = "05:30"
    return size_bytes, dur_str

NEW_EPISODES = [
    {
        "mp3": "sIA_Sec_03_XZ_Utils_Backdoor_Andres_Freund_SSH_2026-11-04.mp3",
        "title": "sIA Sec #03: El Backdoor de XZ Utils: Cómo 500 Milisegundos de Lag Salvaron al Internet Entero",
        "slug": "sia-sec-03-el-backdoor-de-xz-utils-y-los-500ms-que-salvaron-internet",
        "desc": "Crónica forense de la mayor operación de espionaje en código abierto: los dos años de ingeniería social de Jia Tan sobre Lasse Collin, los hooks IFUNC en liblzma para secuestrar OpenSSH, y cómo el ingeniero Andrés Freund salvó internet al investigar 500ms de latencia en PostgreSQL por cacs.",
        "pubDate": "Wed, 04 Nov 2026 22:30:00 GMT"
    },
    {
        "mp3": "sIA_Corp_07_Knight_Capital_440_Millones_Flag_Reutilizado_2026-11-04.mp3",
        "title": "sIA Corp #07: Knight Capital: $440 Millones Destruidos en 45 Minutos por Reutilizar un Flag Booleano",
        "slug": "sia-corp-07-knight-capital-el-bug-de-440-millones-en-45-minutos",
        "desc": "El mayor desastre de DevOps en la historia de Wall Street: cómo el sistema SMARS de Knight Capital despertó código muerto de 2003 (PowerPeg) en un octavo servidor olvidado durante un despliegue manual, perdiendo 10 millones de dólares por minuto por cacs.",
        "pubDate": "Wed, 04 Nov 2026 21:00:00 GMT"
    },
    {
        "mp3": "sIA_Sec_02_TV_Boxes_Malware_Fabrica_Videostrong_2026-11-04.mp3",
        "title": "sIA Sec #02: El Caballo de Troya en tu Sala: Cómo 1.3 Millones de TV Boxes Android Venían con Malware de Fábrica",
        "slug": "sia-sec-02-el-caballo-de-troya-en-tu-sala-tv-boxes-android-malware-de-fabrica",
        "desc": "Análisis de la operación del Grupo de Inteligencia de Amenazas de Google contra la botnet XCPE: cómo el fabricante chino Videostrong (MECOOL, T95) inyectó el rootkit x.cpe en la partición de sistema con persistencia en bootloader, MQTT y proxies residenciales, y su expulsión definitiva de Android por cacs.",
        "pubDate": "Wed, 04 Nov 2026 19:30:00 GMT"
    },
    {
        "mp3": "sIA_Terror_01_Las_Escaleras_En_El_Bosque_2026-11-04.mp3",
        "title": "sIA Terror #01: Las Escaleras Perdidas en el Bosque Profundo: El Secreto de los Guardabosques",
        "slug": "sia-terror-01-las-escaleras-en-el-bosque-nacional",
        "desc": "Especial inmersivo de terror analógico y misterio: los testimonios de oficiales de Búsqueda y Rescate en parques nacionales sobre estructuras arquitectónicas imposibles a kilómetros de la civilización y la orden estricta de jamás subir sus escalones por cacs.",
        "pubDate": "Wed, 04 Nov 2026 17:00:00 GMT"
    },
    {
        "mp3": "sIA_Maker_03_Biqu_Panda_Treat_FoodTech_2026-11-04.mp3",
        "title": "sIA Maker #03: BIQU Panda Treat: Cómo una Impresora 3D de $200 Hackeó la Industria de la Confitería Digital",
        "slug": "sia-maker-03-biqu-panda-treat-impresora-3d-confiteria-digital",
        "desc": "De $5,000 a $330 USD: cómo el cabezal modular de inyección térmica de tintas comestibles BIQU Panda Treat transforma la cinemática de una Bambu Lab A1 Mini en una plataforma de repostería digital certificada por la FDA por cacs.",
        "pubDate": "Wed, 04 Nov 2026 14:00:00 GMT"
    },
    {
        "mp3": "sIA_Dev_02_Code_Mode_vs_MCP_Cloudflare_Anthropic_2026-11-04.mp3",
        "title": "sIA Dev #02: La Muerte del Function Calling: Cómo Code Mode de Cloudflare y Anthropic Redujo MCP de 1.17M a 1,000 Tokens",
        "slug": "sia-dev-02-la-muerte-del-function-calling-code-mode-vs-mcp",
        "desc": "Por qué los LLMs son ineficientes invocando herramientas JSON secuenciales y cómo el paradigma Code Mode sobre Dynamic Worker V8 Isolates reduce el consumo de contexto en servidores MCP masivos en un 99.9% por cacs.",
        "pubDate": "Wed, 04 Nov 2026 11:00:00 GMT"
    }
]

def main():
    # 1. Also ensure sIA_Terror_01 is in RESEARCH_DATABASE in build_magazine.py
    mag_text = BUILD_MAG.read_text(encoding="utf-8")
    if "sIA_Terror_01_Las_Escaleras_En_El_Bosque_2026-11-04.mp3" not in mag_text:
        mag_text = mag_text.replace(
            "REELS_MAP = {",
            'REELS_MAP = {\n    "sIA_Terror_01_Las_Escaleras_En_El_Bosque_2026-11-04.mp3": "sIA_Terror_01_Las_Escaleras_Reel.mp4",'
        )
        terror_entry = '''    # sIA Terror 01 - Las Escaleras en el Bosque - 4 de Noviembre de 2026
    "sIA_Terror_01_Las_Escaleras_En_El_Bosque_2026-11-04.mp3": {
        "slug": "sia-terror-01-las-escaleras-en-el-bosque-nacional",
        "category": "sIA Terror & Misterio",
        "badge_color": "rose",
        "read_time": "10 min",
        "title": "sIA Terror #01: Las Escaleras Perdidas en el Bosque Profundo: El Secreto de los Guardabosques",
        "subtitle": "Crónicas de Búsqueda y Rescate (SAR): Anomalías Arquitectónicas, Silencio Acústico (The Oz Factor) y el Protocolo No Escrito.",
        "thesis": "El fenómeno cultural y testimonial de las escaleras aisladas en reservas forestales combina la psicología de la desorientación sensorial en espacios liminales con la tradición oral de los equipos de Búsqueda y Rescate en Norteamérica.",
        "nexo": "Primer episodio de nuestra serie sIA Terror: Narrativa inmersiva nocturna, diseño sonoro binaural y misterios de guardabosques.",
        "reel_video": "sIA_Terror_01_Las_Escaleras_Reel.mp4",
        "content_blocks": [
            {
                "title": "1. El Protocolo No Escrito de los Oficiales de Búsqueda y Rescate",
                "body": """
En las profundidades de los bosques nacionales, a treinta o cuarenta kilómetros del camino pavimentado más cercano, los oficiales veteranos de Búsqueda y Rescate (SAR) comparten una advertencia constante con los reclutas: si durante un operativo encuentras una escalera intacta en medio de los árboles que no conduce a ninguna parte, no te acerques y jamás subas sus peldaños.
"""
            },
            {
                "title": "2. El Factor Oz y la Ruptura Acústica del Bosque",
                "body": """
Quienes han ignorado la advertencia describen una transición sensorial abrupta conocida como el 'Factor Oz': el viento en las copas de los pinos, el canto de las aves y el zumbido de los insectos se apagan de golpe, sumiendo al observador en un vacío acústico opresivo mientras los sensores GPS pierden toda señal satelital.
"""
            }
        ],
        "apa_references": [
            "Paulides, D. (2012). *Missing 411: North America and Beyond*. CanAm Missing Project.",
            "Vallee, J. (1988). *Dimensions: A Casebook of Alien Contact* (The Oz Factor sensory analysis). Contemporary Books.",
            "cacs, & sIA Editora. (2026). *sIA Terror #01: Las Escaleras Perdidas en el Bosque Profundo*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    },'''
        mag_text = mag_text.replace("RESEARCH_DATABASE = {", "RESEARCH_DATABASE = {\n" + terror_entry)
        BUILD_MAG.write_text(mag_text, encoding="utf-8")
        print("[OK] Added sIA_Terror_01 to build_magazine.py")

    # 2. Update podcast.xml with strict privacy (cacs instead of personal name) and new <item> blocks
    xml_text = XML_FILE.read_text(encoding="utf-8")
    xml_text = xml_text.replace("<itunes:name>Carlos Corona</itunes:name>", "<itunes:name>cacs</itunes:name>")

    items_to_insert = []
    for ep in NEW_EPISODES:
        if ep["mp3"] in xml_text:
            print(f"[INFO] {ep['mp3']} already in podcast.xml")
            continue
        size_bytes, dur_str = get_audio_meta(ep["mp3"])
        base_stem = ep["mp3"].replace(".mp3", "")
        art_url = f"https://escucha-sia.github.io/articulos/{ep['slug']}.html"
        item_xml = f"""    <item>
      <title>{ep['title']}</title>
      <link>{art_url}</link>
      <description>{ep['desc']} | Leer artículo y referencias APA: {art_url}</description>
      <pubDate>{ep['pubDate']}</pubDate>
      <enclosure url="https://escucha-sia.github.io/audio/{ep['mp3']}" length="{size_bytes}" type="audio/mpeg"/>
      <guid isPermaLink="true">https://escucha-sia.github.io/audio/{ep['mp3']}</guid>
      <itunes:duration>{dur_str}</itunes:duration>
      <itunes:author>Jorge y Dalia</itunes:author>
      <itunes:image href="https://escucha-sia.github.io/cover.jpg"/>
      <itunes:explicit>no</itunes:explicit>
      <podcast:transcript url="https://escucha-sia.github.io/audio/{base_stem}.vtt" type="text/vtt" language="es"/>
      <podcast:transcript url="https://escucha-sia.github.io/audio/{base_stem}.srt" type="application/x-subrip" language="es"/>
    </item>"""
        items_to_insert.append(item_xml)

    if items_to_insert:
        joined_items = "\n".join(items_to_insert) + "\n    <item>"
        xml_text = xml_text.replace("    <item>", joined_items, 1)
        XML_FILE.write_text(xml_text, encoding="utf-8")
        print(f"[OK] Inserted {len(items_to_insert)} new <item> blocks into podcast.xml")

    # 3. Run build_magazine.py
    subprocess.run([sys.executable, str(BUILD_MAG)], cwd=str(BASE_DIR), check=True)

    # 4. Verify generated HTML files
    for ep in NEW_EPISODES:
        html_path = BASE_DIR / "articulos" / f"{ep['slug']}.html"
        print(f"  -> {html_path.name}: exists={html_path.exists()} ({html_path.stat().st_size if html_path.exists() else 0} bytes)")

if __name__ == "__main__":
    main()
