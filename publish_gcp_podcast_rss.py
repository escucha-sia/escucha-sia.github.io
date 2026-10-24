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
    # Subprograma 01: Introducción a la Ingeniería de Datos
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
    # Subprograma 02: Obtén Estadísticas a partir de BigQuery
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
    # Subprograma 03: Preparar datos para paneles de Looker e informes
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
    },
    # Subprograma 04: Introducción a la IA y el Aprendizaje Automático en Google Cloud
    {
        "track_num": "04.01",
        "filename": "Pista_04_01_Fundamentos_de_IA_e_Infraestructura.mp3",
        "title": "#GCP-Data 04.01 - Fundamentos de IA e Infraestructura",
        "duration": "06:30",
        "pub_date": "Sat, 24 Oct 2026 11:20:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 04
Pista 04.01: Fundamentos de IA, Caso Coffee on Wheels, Arquitectura de 3 Capas y BigQuery ML.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con desacoplamiento compute/storage y optimización de costos de cómputo en r/googlecloud.

📌 Contenido del Episodio:
• [00:00] Apertura del Curso 4: Introducción a la IA y Machine Learning en Google Cloud.
• [01:10] Caso Coffee on Wheels y DataBeans: Rutas, inventario y marketing multimodal.
• [02:30] La Arquitectura de 3 capas: Infraestructura, Plataforma de desarrollo (Vertex AI) y Soluciones.
• [03:45] IA Predictiva (discriminativa) vs IA Generativa: El árbol de decisión.
• [05:00] Desacoplamiento de cómputo y almacenamiento con BigQuery ML en SQL.
• [06:15] Alerta de Examen 2026: Cuándo usar BigQuery ML vs Vertex AI Workbench.
• [07:05] Debrief Reddit: El desastre de la GPU olvidada y costos de cómputo inactivo.
• [07:55] Soundbite del Examen: 4 reglas de oro de fundamentos de IA."""
    },
    {
        "track_num": "04.02",
        "filename": "Pista_04_02_IA_Generativa_Modelos_y_Agentes.mp3",
        "title": "#GCP-Data 04.02 - IA Generativa, Modelos de Base y Agentes",
        "duration": "06:15",
        "pub_date": "Sat, 24 Oct 2026 11:25:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 04
Pista 04.02: Modelos de Base, Familia Gemini, Multimodalidad Nativa y Vertex AI Studio.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con Grounding en datos corporativos y prevención de alucinaciones.

📌 Contenido del Episodio:
• [00:00] Panorama de Modelos de Base: Parámetros y entrenamiento a escala.
• [01:10] Familia Gemini: Gemini Pro (razonamiento), Flash (baja latencia) y Flash-Lite (volumen).
• [02:30] Multimodalidad nativa: Texto, imagen, audio y video simultáneos.
• [03:45] Vertex AI Studio y Vertex AI Agent Builder con Function Calling.
• [05:00] Técnicas de adaptación: Prompt Engineering, RAG con Grounding y Fine-Tuning.
• [06:15] Alerta de Examen 2026: Grounding con Vertex AI Search vs Fine-Tuning innecesario.
• [07:05] Debrief Reddit: El error de hacer fine-tuning para datos dinámicos.
• [07:50] Soundbite del Examen: 4 reglas mnemotécnicas de IA generativa."""
    },
    {
        "track_num": "04.03",
        "filename": "Pista_04_03_Opciones_de_Desarrollo_y_Flujo_MLOps.mp3",
        "title": "#GCP-Data 04.03 - Opciones de Desarrollo y Flujo MLOps en Vertex AI",
        "duration": "06:20",
        "pub_date": "Sat, 24 Oct 2026 11:30:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 04
Pista 04.03: Cuadrante de Selección de ML, Ciclo de Vida del Modelo y Vertex AI Pipelines.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con MLOps, drift detection y análisis de costos en inferencia.

📌 Contenido del Episodio:
• [00:00] Las 4 opciones de desarrollo: Pretrained APIs, BigQuery ML, AutoML y Custom Training.
• [01:15] Las 3 etapas del flujo: Preparación de datos, Model Training & Evaluation, Model Serving.
• [02:40] Online Prediction Endpoints vs Vertex AI Batch Prediction.
• [04:00] MLOps: Data Drift, Concept Drift y orquestación con Vertex AI Pipelines (Kubeflow).
• [05:15] Alerta de Examen 2026: Criterios de examen para inferencia en línea vs por lotes.
• [06:05] Debrief Reddit: El costo desmedido de endpoints dedicados 24/7 sin tráfico.
• [06:50] Soundbite del Examen: 4 reglas de oro de desarrollo ML y MLOps."""
    },
    # Subprograma 05: Modelo de referencia: Infraestructura
    {
        "track_num": "05.01",
        "filename": "Pista_05_01_Almacenamiento_e_Identidad_IAM.mp3",
        "title": "#GCP-Data 05.01 - Almacenamiento en Cloud Storage e Identidad IAM",
        "duration": "06:10",
        "pub_date": "Sat, 24 Oct 2026 11:35:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 05
Pista 05.01: Cloud Storage (gcloud storage), Identidades IAM, Roles y Cloud Monitoring.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con principio de menor privilegio y gobernanza de accesos.

📌 Contenido del Episodio:
• [00:00] Apertura del Curso 5: Modelo de Referencia de Infraestructura.
• [01:05] Cloud Storage: Once nueves de durabilidad y la herramienta moderna gcloud storage.
• [02:20] El modelo IAM: Quién (Principals, Service Accounts), Qué (Roles) y Dónde (Recursos).
• [03:40] Observabilidad con Cloud Monitoring: Métricas, paneles y políticas de alertas.
• [04:55] Alerta de Examen 2026: Uniform Bucket-Level Access y prohibición de Roles Primitivos.
• [05:45] Debrief Reddit: El becario con rol Editor de proyecto y el borrado de tablas de producción.
• [06:30] Soundbite del Examen: 4 reglas de oro de infraestructura e IAM."""
    },
    {
        "track_num": "05.02",
        "filename": "Pista_05_02_Serverless_y_Mensajeria_con_PubSub.mp3",
        "title": "#GCP-Data 05.02 - Serverless y Mensajería Escalable con Pub/Sub",
        "duration": "06:25",
        "pub_date": "Sat, 24 Oct 2026 11:40:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 05
Pista 05.02: Cloud Run Functions, Arquitectura de Pub/Sub (Push vs Pull) y Dead-Lettering.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con resiliencia en eventos y prevención de bucles infinitos.

📌 Contenido del Episodio:
• [00:00] Computación Serverless reactiva con Cloud Run Functions (2da gen).
• [01:10] Arquitectura de Cloud Pub/Sub: Publicadores, Tópicos y Suscripciones.
• [02:30] Suscripción Push (endpoints HTTPS, autoscale) vs Suscripción Pull (Dataflow, VPC privada).
• [03:50] Resiliencia y Dead-Letter Topics para mensajes corruptos.
• [05:00] Alerta de Examen 2026: Push vs Pull y garantías de entrega At-Least-Once.
• [05:50] Debrief Reddit: El bucle infinito de reintentos en Cloud Run Functions sin Dead-Letter.
• [06:40] Soundbite del Examen: 4 reglas mnemotécnicas de serverless y mensajería."""
    },
    # Subprograma 06: Optimiza los costos con Google Cloud Storage
    {
        "track_num": "06.01",
        "filename": "Pista_06_01_Clases_de_Almacenamiento_Lifecycle_y_Autoclass.mp3",
        "title": "#GCP-Data 06.01 - Clases de Almacenamiento, Lifecycle y Autoclass",
        "duration": "06:40",
        "pub_date": "Sat, 24 Oct 2026 11:45:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 06
Pista 06.01: Optimización de Costos en Cloud Storage, Reglas OLM, Autoclass y Soft Delete.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con tarifas de recuperación y retención mínima.

📌 Contenido del Episodio:
• [00:00] Apertura del Curso 6: Optimiza los Costos con Google Cloud Storage.
• [01:05] Las 4 clases: Standard, Nearline (30d), Coldline (90d) y Archive (365d).
• [02:25] Object Lifecycle Management (OLM): Condiciones (Age) y Acciones (SetStorageClass, Delete).
• [03:45] Cloud Storage Autoclass: Transición inteligente sin tarifas de recuperación.
• [05:00] Protección contra ransomware con Soft Delete (retención de 7 días).
• [06:10] Alerta de Examen 2026: Tarifas de recuperación (Retrieval Fees) y penalizaciones de borrado temprano.
• [07:00] Debrief Reddit: La migración a Archive y la factura astronómica por auditoría de lectura.
• [07:50] Soundbite del Examen: 4 reglas de oro de costos de almacenamiento."""
    },
    # Subprograma 07: Implementa los aspectos básicos de seguridad
    {
        "track_num": "07.01",
        "filename": "Pista_07_01_IAM_Service_Accounts_y_VPC_Peering.mp3",
        "title": "#GCP-Data 07.01 - IAM, Service Accounts y VPC Network Peering",
        "duration": "06:15",
        "pub_date": "Sat, 24 Oct 2026 11:50:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 07
Pista 07.01: Implementa Seguridad en la Nube, Roles Personalizados, Workload Identity y Peering.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con interconexión privada de redes y no transitividad.

📌 Contenido del Episodio:
• [00:00] Apertura del Curso 7: Implementa los Aspectos Básicos de Seguridad en Google Cloud.
• [01:05] Creación quirúrgica de Roles Personalizados (Custom Roles) con gcloud iam roles create.
• [02:20] Seguridad en Cuentas de Servicio: Prohibición de claves JSON y Workload Identity Federation.
• [03:40] VPC Network Peering: Comunicación privada con IPs internas sin salir a internet.
• [04:55] Alerta de Examen 2026: No Transitividad de VPC Peering y gobernanza con Grupos.
• [05:45] Debrief Reddit: La fuga de Service Account Key en GitHub y la botnet de minería crypto.
• [06:30] Soundbite del Examen: 4 reglas mnemotécnicas de IAM y redes privadas."""
    },
    {
        "track_num": "07.02",
        "filename": "Pista_07_02_Cloud_KMS_IAP_GKE_Privado_y_Challenge_Lab.mp3",
        "title": "#GCP-Data 07.02 - Cloud KMS, IAP, GKE Privado y Challenge Lab",
        "duration": "06:35",
        "pub_date": "Sat, 24 Oct 2026 11:55:00 GMT",
        "description": """🎧 Certificación Google Cloud Associate Data Practitioner - Subprograma 07
Pista 07.02: Criptografía con Cloud KMS (CMEK), Identity-Aware Proxy, GKE Privado y Laboratorio de Desafío.

Voces: Jorge y Dalia (Español México).
Basado 100% en el curso oficial de Google Cloud Skills Boost con resolución paso a paso del Challenge Lab final.

📌 Contenido del Episodio:
• [00:00] Criptografía y Control Total de Claves con Cloud KMS y CMEK.
• [01:10] Paradigma Zero Trust con Identity-Aware Proxy (IAP) y túnel TCP para SSH sin IP pública.
• [02:30] Clústeres Privados de Google Kubernetes Engine (Private GKE) y Cloud NAT.
• [03:50] Estrategia de 4 Fases para resolver el Challenge Lab de Seguridad con 100 puntos.
• [05:10] Alerta de Examen 2026: gcloud compute ssh con tunnel-through-iap y rango CIDR de Google.
• [06:00] Debrief Reddit: El bastión SSH tradicional bombardeado por ataques de fuerza bruta vs IAP.
• [06:50] Soundbite del Examen: 4 reglas de oro para aprobar el Challenge Lab y la certificación."""
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

    # 2. Copiar archivos de audio a C:\Carlos\noticias_podcast\audio\
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    candidate_folders = [
        Path(r"C:\Users\c_a_c\Music\NoticIAs"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_01_Ingenieria_de_Datos"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_02_Estadisticas_en_BigQuery"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_03_Paneles_de_Looker_e_Informes"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_04_IA_y_Aprendizaje_Automatico_en_Google_Cloud"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_05_Modelo_de_Referencia_Infraestructura"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_06_Optimiza_los_Costos_con_Google_Cloud_Storage"),
        Path(r"C:\Users\c_a_c\Music\Associate_Data_Practitioner\Subprograma_07_Aspectos_Basicos_de_Seguridad")
    ]
    for ep in EPISODES:
        dst = AUDIO_DIR / ep["filename"]
        if not dst.exists() or dst.stat().st_size == 0:
            for c_folder in candidate_folders:
                src = c_folder / ep["filename"]
                if src.exists() and src.stat().st_size > 0:
                    print(f"[*] Copiando {ep['filename']} a audio/ desde {c_folder.name}...")
                    shutil.copy2(src, dst)
                    break
        if dst.exists():
            print(f"[OK] Audio presente: {ep['filename']} ({dst.stat().st_size / (1024*1024):.1f} MB)")

    # 3. Generar feed XML exclusivo
    feed_xml = build_feed_xml(EPISODES)
    FEED_PATH.write_text(feed_xml, encoding="utf-8")
    AUDIO_FEED_PATH.write_text(feed_xml, encoding="utf-8")
    print(f"✅ Feed RSS generado en: {FEED_PATH}")

    # 4. Git commit y Git push a GitHub Pages
    print("\nDesplegando nuevo programa a GitHub Pages...")
    try:
        subprocess.run(["git", "add", "."], cwd=str(NOTICIAS_DIR), check=True)
        commit_msg = "feat(podcast): publish complete 19 tracks for all 7 Google Cloud Associate Data Practitioner courses"
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
    print("Total de pistas publicadas en el feed:", len(EPISODES))
    print("=" * 70)

if __name__ == '__main__':
    main()
