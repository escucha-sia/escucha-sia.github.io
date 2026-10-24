import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

NOTICIAS_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = NOTICIAS_DIR / "audio"
MUSIC_SRC_DIR = Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_01_Ingenieria_de_Datos")
COVER_PATH = NOTICIAS_DIR / "cover_gcp_podcast.jpg"
FEED_PATH = NOTICIAS_DIR / "gcp-data-practitioner.xml"
AUDIO_FEED_PATH = AUDIO_DIR / "gcp-data-practitioner.xml"

BASE_URL = "https://escucha-sia.github.io"
COVER_URL = f"{BASE_URL}/cover_gcp_podcast.jpg"

def generate_podcast_show_cover():
    """Genera una portada cuadrada de 1400x1400 px que cumple con los estándares de Spotify y Apple Podcasts"""
    size = 1400
    img = Image.new("RGB", (size, size), color=(15, 23, 42)) # Slate oscuro
    draw = ImageDraw.Draw(img)

    # Borde corporativo Google Cloud en la parte superior
    draw.rectangle([0, 0, size, 24], fill=(66, 133, 244))      # Google Blue
    draw.rectangle([0, 24, size, 36], fill=(52, 168, 83))      # Google Green
    draw.rectangle([0, size-24, size, size], fill=(234, 67, 53)) # Google Red

    fonts_dir = Path("C:/Windows/Fonts")
    font_bold_path = str(fonts_dir / "calibrib.ttf" if (fonts_dir / "calibrib.ttf").exists() else fonts_dir / "arialbd.ttf")
    font_reg_path = str(fonts_dir / "calibri.ttf" if (fonts_dir / "calibri.ttf").exists() else fonts_dir / "arial.ttf")

    try:
        font_sub = ImageFont.truetype(font_bold_path, 40)
        font_title = ImageFont.truetype(font_bold_path, 84)
        font_role = ImageFont.truetype(font_bold_path, 60)
        font_badge = ImageFont.truetype(font_bold_path, 38)
        font_meta = ImageFont.truetype(font_reg_path, 34)
    except Exception:
        font_sub = font_title = font_role = font_badge = font_meta = ImageFont.load_default()

    # 1. Google Cloud Certified
    draw.text((100, 100), "GOOGLE CLOUD CERTIFIED", fill=(148, 163, 184), font=font_sub)
    draw.text((100, 160), "ASSOCIATE DATA PRACTITIONER", fill=(255, 255, 255), font=font_role)

    # 2. Caja central destacada
    draw.rounded_rectangle([100, 270, 1300, 950], radius=30, fill=(30, 41, 59), outline=(59, 130, 246), width=4)
    draw.text((150, 330), "AUDIO CURSO OFICIAL", fill=(245, 158, 11), font=font_title)
    draw.text((150, 440), "INGENIERÍA DE DATOS & BIG DATA", fill=(255, 255, 255), font=font_sub)
    
    # Lista de temas destacados
    topics = [
        "• BigQuery, Dataform, BigLake & Storage Write API",
        "• Cloud Storage, Datastream & CDC en Tiempo Real",
        "• Dataproc, Spark Serverless, Dataflow & Apache Beam",
        "• Orquestación con Cloud Composer, Scheduler & Eventarc",
        "• Casos Reales y Trampas de Producción de Reddit"
    ]
    y_pos = 530
    for t in topics:
        draw.text((150, y_pos), t, fill=(203, 213, 225), font=font_meta)
        y_pos += 70

    # 3. Badge inferior
    draw.rounded_rectangle([100, 1020, 1300, 1140], radius=20, fill=(15, 118, 110), outline=(20, 184, 166), width=2)
    draw.text((140, 1055), "FORMATO EN AUTO • ESPAÑOL MÉXICO • JORGE & DALIA", fill=(240, 253, 250), font=font_badge)

    # 4. Firma
    draw.text((100, 1200), "sIA Academy • Master Cloud Series • Carlos Corona", fill=(100, 116, 139), font=font_meta)

    img.save(COVER_PATH, quality=95)
    print(f"✅ Carátula oficial del programa generada en: {COVER_PATH} (1400x1400 px)")

EPISODES = [
    {
        "track_num": "01.01",
        "filename": "Pista_01_01_Fundamentos_y_Componentes.mp3",
        "title": "#GCP-Data 01.01 - Fundamentos y Componentes de Ingeniería de Datos",
        "duration": "08:47",
        "pub_date": "Sat, 24 Oct 2026 09:45:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 01
Pista 01.01: Introducción a la Ingeniería de Datos y Componentes del Ecosistema GCP.

Voces: Jorge y Dalia (Español México).
Basado 100% en el currículo oficial de Google Cloud Skills Boost con enriquecimiento técnico, pronunciación fonética y anécdotas de producción de r/googlecloud.

📌 Contenido del Episodio:
• [00:00] Bienvenida y Blueprint Oficial del Associate Data Practitioner.
• [01:20] Ciclo de vida del dato: Ingestión, Almacenamiento, Procesamiento y Analítica.
• [03:45] Arquitectura visual: De Data Source a Data Sink paso a paso.
• [05:15] Interrupción Reddit: El error de novato entre Cloud Storage Multi-Regional vs Regional.
• [06:40] Alerta de Examen 2026: Dataplex y gobierno unificado de datos.
• [07:45] Soundbite del Examen: 3 reglas nemotécnicas para aprobar a la primera."""
    },
    {
        "track_num": "01.02",
        "filename": "Pista_01_02_Replicacion_y_Migracion_de_Datos.mp3",
        "title": "#GCP-Data 01.02 - Replicación y Migración de Datos (Datastream, STS y DMS)",
        "duration": "11:15",
        "pub_date": "Sat, 24 Oct 2026 09:58:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 01
Pista 01.02: Replicación y Migración de Datos, Datastream, Storage Transfer Service y Database Migration Service.

Voces: Jorge y Dalia (Español México).
Basado 100% en el currículo oficial de Google Cloud Skills Boost con enriquecimiento técnico, pronunciación fonética y desastres de producción de Reddit.

📌 Contenido del Episodio:
• [00:00] Bienvenida y Panorama de Replicación y Migración.
• [01:15] Arquitectura visual y regla de ancho de banda: ¿Cuándo mover por red y cuándo con hardware?
• [03:00] La herramienta moderna gcloud storage y reemplazo de gsutil.
• [04:10] Mover grandes conjuntos: Storage Transfer Service vs Transfer Appliance (>20 TB).
• [05:45] Datastream y Captura de Datos Modificados (CDC): Lectura de WAL y tipos de datos unificados.
• [07:20] Debrief Reddit: El desastre de saturación de disco por ranuras de replicación en PostgreSQL.
• [08:30] Alerta de Examen 2026: Datastream directo a BigQuery y DMS a AlloyDB.
• [09:15] Soundbite del Examen: 4 reglas nemotécnicas para preguntas de migración."""
    },
    {
        "track_num": "01.04",
        "filename": "Pista_01_04_Patron_EL_Extraccion_y_Carga.mp3",
        "title": "#GCP-Data 01.04 - Patrón EL: Extracción y Carga en BigQuery",
        "duration": "08:03",
        "pub_date": "Sat, 24 Oct 2026 10:00:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 01
Pista 01.04: Patrón Extract and Load (EL), BigQuery Storage Write API y Cloud Storage.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con análisis de costos y casos reales de r/dataengineering.

📌 Contenido del Episodio:
• [00:00] Introducción al Patrón EL y Filosofía Schema-on-Read.
• [01:30] BigQuery Load Jobs vs Streaming Inserts: ¿Cuándo pagar y cuándo es gratis?
• [03:15] BigQuery Storage Write API: Modo Committed vs Pending y Exactly-Once Semantics.
• [05:00] Debate Reddit: Por qué las cargas por lotes en BigQuery son gratuitas y cómo evitar facturas sorpresa.
• [06:30] Alerta de Examen 2026: Formatos columnar Parquet/ORC y compresión Snappy.
• [07:15] Soundbite del Examen: Reglas de oro para preguntas capciosas de carga de datos."""
    },
    {
        "track_num": "01.05",
        "filename": "Pista_01_05_Patron_ELT_y_Dataform_en_BigQuery.mp3",
        "title": "#GCP-Data 01.05 - Patrón ELT y Dataform en BigQuery",
        "duration": "07:49",
        "pub_date": "Sat, 24 Oct 2026 10:10:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 01
Pista 01.05: Patrón Extract, Load and Transform (ELT), SQL Procedural, UDFs, Spark y Dataform.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con lecciones de producción y reglas de oro de r/dataengineering.

📌 Contenido del Episodio:
• [00:00] Introducción al Patrón ELT y ahorro de clústeres dedicados.
• [01:05] Arquitectura visual: Staging tables y transformaciones dentro de BigQuery.
• [02:10] Extensiones de BigQuery: SQL Procedural, UDFs, Spark sin Dataproc y Remote Functions.
• [04:15] Dataform: Framework declarativo con SQLX, pruebas de aserción y control Git.
• [05:35] Alerta de Examen 2026: Dataform y BigQuery DataFrames (bigframes).
• [06:15] Debrief Reddit: El peligro de las consultas programadas ciegas vs DAGs de Dataform.
• [07:05] Soundbite del Examen: 4 reglas mnemotécnicas para preguntas de ELT."""
    },
    {
        "track_num": "01.06",
        "filename": "Pista_01_06_Patron_ETL_y_Procesamiento_Distribuido.mp3",
        "title": "#GCP-Data 01.06 - Patrón ETL y Procesamiento Distribuido (Dataproc, Beam, Bigtable)",
        "duration": "08:47",
        "pub_date": "Sat, 24 Oct 2026 10:18:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 01
Pista 01.06: Patrón Extract, Transform and Load (ETL), Dataprep, Data Fusion, Dataproc, Apache Beam en Dataflow y Cloud Bigtable.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con anécdotas de costos de r/googlecloud y diseño de clave de fila NoSQL.

📌 Contenido del Episodio:
• [00:00] Introducción al Patrón ETL y transformación en vuelo.
• [01:10] Herramientas visuales sin código: Dataprep by Trifacta y Cloud Data Fusion (CDAP).
• [02:40] Procesamiento por lotes: Clústeres efímeros de Dataproc y Dataproc Serverless para Spark.
• [04:20] Streaming en tiempo real: Pub/Sub como buffer global y Dataflow con Apache Beam.
• [05:55] Cloud Bigtable: Almacenamiento NoSQL de columnas anchas para series temporales y latencia sub-10ms.
• [06:50] Alerta de Examen 2026: Dataproc Serverless y Dataflow Streaming Engine.
• [07:30] Debrief Reddit: El clúster olvidado del fin de semana y hotspotting en Bigtable.
• [08:05] Soundbite del Examen: 4 reglas de oro de procesamiento distribuido."""
    },
    {
        "track_num": "01.07",
        "filename": "Pista_01_07_Automatizacion_y_Orquestacion_en_GCP.mp3",
        "title": "#GCP-Data 01.07 - Automatización y Orquestación en GCP (Scheduler, Composer, Eventarc)",
        "duration": "08:31",
        "pub_date": "Sat, 24 Oct 2026 10:21:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 01
Pista 01.07: Automatización y Orquestación, Cloud Scheduler, Cloud Workflows, Cloud Composer (Airflow), Cloud Run Functions y Eventarc.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con la gran síntesis de los 4 patrones de ingeniería de datos.

📌 Contenido del Episodio:
• [00:00] Introducción a la Automatización: Por tiempo vs Dirigida por eventos.
• [01:05] Automatización ágil serverless: Cloud Scheduler (cron) y Cloud Workflows.
• [02:20] Orquestación empresarial: Cloud Composer y DAGs en Python con Apache Airflow.
• [03:45] Flujos reactivos: Cloud Run Functions y enrutamiento global con Eventarc (CloudEvents).
• [05:00] Gran Síntesis del Subprograma 1: Los 4 patrones arquitectónicos del examen.
• [06:35] Alerta de Examen 2026: Cloud Run Functions de 2da gen y Composer 3.
• [07:15] Debrief Reddit: El costo de usar Composer para crons simples vs Workflows.
• [07:50] Soundbite del Examen: 4 reglas de oro de automatización."""
    },
    {
        "track_num": "02.01",
        "filename": "Pista_02_01_Fundamentos_SQL_y_Paradigma_BigQuery.mp3",
        "title": "#GCP-Data 02.01 - Fundamentos de SQL y el Paradigma de BigQuery",
        "duration": "06:44",
        "pub_date": "Sat, 24 Oct 2026 10:53:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 02
Pista 02.01: Fundamentos de SQL y el Paradigma de Almacenamiento de BigQuery.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con arquitectura OLTP vs OLAP y optimización de costos.

📌 Contenido del Episodio:
• [00:00] Apertura del Curso 2: BigQuery y Blueprint Oficial.
• [01:10] Paradigma BigQuery vs Cloud SQL: Almacenamiento columnar Capacitor y Validador de consultas.
• [02:30] Sintaxis SQL Esencial y automatización con Cloud SDK: bq query, bq mk y bq extract.
• [03:45] Alerta de Examen 2026: BigQuery Studio, Gemini in BigQuery y BigQuery Editions.
• [04:35] Debrief Reddit: El mito del comando LIMIT y la factura de los 10 Terabytes.
• [05:50] Soundbite del Examen: 4 reglas de oro de BigQuery SQL."""
    },
    {
        "track_num": "02.02",
        "filename": "Pista_02_02_SQL_Analitico_Deduplicacion_y_Depuracion.mp3",
        "title": "#GCP-Data 02.02 - SQL Analítico, Deduplicación y Depuración",
        "duration": "06:17",
        "pub_date": "Sat, 24 Oct 2026 10:54:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 02
Pista 02.02: SQL Analítico, Patrones de Deduplicación y Depuración de Errores de Consulta.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con datos de e-commerce y lecciones de r/dataengineering.

📌 Contenido del Episodio:
• [00:00] Introducción al SQL Analítico y conjuntos de datos de comercio electrónico.
• [01:10] Deduplicación con funciones analíticas de ventana: ROW_NUMBER() OVER(PARTITION BY... ORDER BY... DESC).
• [02:25] Depuración de errores: La diferencia vital entre WHERE y HAVING, y prevención con SAFE_DIVIDE.
• [03:40] Alerta de Examen 2026: BigQuery Search Index y Vector Search.
• [04:30] Debrief Reddit: El peligro de los JOINs sobre campos NULL y el error de memoria de shuffle.
• [05:40] Soundbite del Examen: 4 reglas nemotécnicas de SQL Analítico."""
    },
    {
        "track_num": "02.03",
        "filename": "Pista_02_03_Visualizacion_Looker_Studio_y_Challenge_Lab.mp3",
        "title": "#GCP-Data 02.03 - Visualización con Looker Studio y Challenge Lab",
        "duration": "06:09",
        "pub_date": "Sat, 24 Oct 2026 10:56:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 02
Pista 02.03: Visualización de Informes de Negocio con Looker Studio, BI Engine y Challenge Lab.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con aceleración en memoria y resolución de examen práctico.

📌 Contenido del Episodio:
• [00:00] Introducción a la Visualización de Negocio y conectores de datos.
• [01:05] Arquitectura de Looker Studio y aceleración en memoria RAM con BigQuery BI Engine.
• [02:30] Estrategia de resolución de 4 fases para el Laboratorio de Desafío (Challenge Lab).
• [03:45] Alerta de Examen 2026: Diferencia entre Looker Studio y Looker Enterprise (LookML).
• [04:35] Debrief Reddit: El desastre de facturación por dashboards sin caché en producción.
• [05:40] Soundbite del Examen: 4 reglas de oro de visualización y Challenge Labs."""
    },
    {
        "track_num": "03.01",
        "filename": "Pista_03_01_Exploracion_y_Filtrado_en_Looker.mp3",
        "title": "#GCP-Data 03.01 - Exploración y Filtrado en Looker",
        "duration": "06:00",
        "pub_date": "Sat, 24 Oct 2026 11:10:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 03
Pista 03.01: Exploración y Filtrado en Looker, Dimensiones, Medidas y Merged Results.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con capa semántica, Looker Modeler y trampas de rendimiento en r/looker.

📌 Contenido del Episodio:
• [00:00] Apertura del Curso 3: Preparar datos para paneles de Looker e informes.
• [01:05] Dimensiones vs Medidas y pivotes en Looker Explores.
• [02:30] Combinar resultados (Merged Results) entre exploraciones sin JOIN en LookML.
• [03:45] Alerta de Examen 2026: Capa semántica universal y Looker Modeler.
• [04:30] Debrief Reddit: El abuso de Merged Results y el colapso de memoria en el navegador.
• [05:20] Soundbite del Examen: 4 reglas mnemotécnicas de Looker Explores."""
    },
    {
        "track_num": "03.02",
        "filename": "Pista_03_02_Calculos_de_Tabla_y_Challenge_Lab.mp3",
        "title": "#GCP-Data 03.02 - Cálculos de Tabla y Challenge Lab de Looker",
        "duration": "06:00",
        "pub_date": "Sat, 24 Oct 2026 11:15:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 03
Pista 03.02: Cálculos de Tabla, Expresiones de Looker y Estrategia del Challenge Lab.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con funciones de offset, percentiles y resolución de laboratorio.

📌 Contenido del Episodio:
• [00:00] Introducción a los Table Calculations y Looker Expressions (Lexp).
• [01:05] Diferencia vital de arquitectura: Consulta SQL vs Cálculos en memoria del navegador.
• [02:25] Funciones avanzadas: offset, pivot_index, percentiles y formateo condicional.
• [03:40] Alerta de Examen 2026: Cuándo usar Table Calculations vs Métricas en LookML.
• [04:30] Debrief Reddit: El peligro de aplicar cálculos de tabla a consultas sin ordenar.
• [05:20] Soundbite del Examen: 4 reglas de oro para el Challenge Lab de Looker."""
    }
]

def build_feed_xml(episodes):
    items_xml = []
    for ep in episodes:
        audio_file = AUDIO_DIR / ep["filename"]
        file_size = audio_file.stat().st_size if audio_file.exists() else 12000000
        audio_url = f"{BASE_URL}/audio/{ep['filename']}"

        item_str = f"""    <item>
      <title>{ep['title']}</title>
      <description><![CDATA[{ep['description']}]]></description>
      <pubDate>{ep['pub_date']}</pubDate>
      <enclosure url="{audio_url}" length="{file_size}" type="audio/mpeg"/>
      <guid isPermaLink="true">{audio_url}</guid>
      <itunes:duration>{ep['duration']}</itunes:duration>
      <itunes:author>Jorge y Dalia • Carlos Corona</itunes:author>
      <itunes:image href="{COVER_URL}"/>
      <itunes:explicit>no</itunes:explicit>
    </item>"""
        items_xml.append(item_str)

    items_block = "\n".join(items_xml)

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podcast="https://podcastindex.org/namespace/1.0">
  <channel>
    <title>Google Cloud Certified: Associate Data Practitioner (Audio Curso Oficial)</title>
    <link>{BASE_URL}/gcp-data-practitioner.xml</link>
    <language>es-mx</language>
    <itunes:author>Jorge y Dalia • Carlos Corona</itunes:author>
    <itunes:image href="{COVER_URL}"/>
    <itunes:category text="Education">
      <itunes:category text="Courses"/>
    </itunes:category>
    <itunes:category text="Technology"/>
    <itunes:owner>
      <itunes:name>Carlos Corona</itunes:name>
      <itunes:email>escucha.sia@gmail.com</itunes:email>
    </itunes:owner>
    <description>Audio curso oficial y debriefs de ingeniería de datos para la certificación Google Cloud Certified: Associate Data Practitioner. Presentado por Jorge y Dalia en español de México. Incluye análisis teórico 1:1, descripción oral de arquitecturas para estudio en el auto, anécdotas reales y trampas de examen de r/googlecloud y r/dataengineering, y soundbites mnemotécnicos de 60 segundos.</description>
{items_block}
  </channel>
</rss>"""
    return xml_content

def main():
    print("=" * 70)
    print("🚀 PUBLICANDO PROGRAMA DEDICADO DE SPOTIFY VÍA RSS GITHUB PAGES")
    print("=" * 70)

    # 1. Carátula oficial 1400x1400
    if not COVER_PATH.exists():
        generate_podcast_show_cover()

    # 2. Copiar archivos de audio a C:\\Carlos\\noticias_podcast\\audio\\
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    candidate_folders = [
        Path(r"C:\Users\c_a_c\Music\NoticIAs"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_01_Ingenieria_de_Datos"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_02_Estadisticas_en_BigQuery"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_03_Paneles_de_Looker_e_Informes")
    ]
    for ep in EPISODES:
        dst = AUDIO_DIR / ep["filename"]
        if not dst.exists():
            for c_folder in candidate_folders:
                src = c_folder / ep["filename"]
                if src.exists():
                    print(f"[*] Copiando {ep['filename']} a audio/ desde {c_folder.name}...")
                    shutil.copy2(src, dst)
                    break
        if dst.exists():
            print(f"[OK] Audio presente: {ep['filename']}")

    # 3. Generar feed XML exclusivo
    feed_xml = build_feed_xml(EPISODES)
    FEED_PATH.write_text(feed_xml, encoding="utf-8")
    AUDIO_FEED_PATH.write_text(feed_xml, encoding="utf-8")
    print(f"✅ Feed RSS generado en: {FEED_PATH}")

    # 4. Limpiar el feed principal de sIA (quitar cualquier item de prueba GCP)
    sia_feed_path = NOTICIAS_DIR / "podcast.xml"
    if sia_feed_path.exists():
        sia_content = sia_feed_path.read_text(encoding="utf-8")
        if "#GCP-Data-01" in sia_content:
            print("[*] Limpiando podcast.xml principal de sIA para mantenerlo separado...")
            # Remover el item de GCP
            import re
            cleaned_sia = re.sub(r'\s*<item>\s*<title>#GCP-Data-01.*?</item>', '', sia_content, flags=re.DOTALL)
            sia_feed_path.write_text(cleaned_sia, encoding="utf-8")
            (AUDIO_DIR / "podcast.xml").write_text(cleaned_sia, encoding="utf-8")
            print("✅ Feed sIA principal restaurado 100% a noticias y geek.")

    # 5. Git commit y Git push a GitHub Pages
    print("\nDesplegando nuevo programa a GitHub Pages...")
    try:
        subprocess.run(["git", "add", "."], cwd=str(NOTICIAS_DIR), check=True)
        commit_msg = "feat(podcast): launch dedicated Google Cloud Associate Data Practitioner podcast feed"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(NOTICIAS_DIR), capture_output=True)
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(NOTICIAS_DIR), capture_output=True, text=True)
        if push_res.returncode == 0:
            print("🎉 ¡Despliegue a GitHub Pages exitoso!")
        else:
            print(f"Aviso git push: {push_res.stderr}")
    except Exception as e:
        print(f"Error git: {e}")

    print("\n" + "=" * 70)
    print("📻 URL DEL FEED RSS PARA SPOTIFY FOR CREATORS:")
    print(f"👉 {BASE_URL}/gcp-data-practitioner.xml")
    print("=" * 70)
    print("Pasos para Spotify for Creators:")
    print("1. Abre https://creators.spotify.com")
    print("2. Haz clic en 'Configuración / Tu cuenta' o 'Añadir nuevo podcast'")
    print("3. Selecciona 'Ya tengo un feed RSS'")
    print(f"4. Pega la URL: {BASE_URL}/gcp-data-practitioner.xml")
    print("5. ¡Listo! Spotify creará automáticamente el nuevo programa independiente.")
    print("=" * 70)

if __name__ == '__main__':
    main()
