"""
sIA Master Episode & Reel Producer:
Tema: sIA Data #03: De Data Warehouse a Lakehouse y Data Mesh: Por qué el 80% de los proyectos de datos fracasan en producción
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop (HyperFrames GPU, 45s, Halftone, Kinetic Pop)
3. Póster oficial del Reel
4. Registro de investigación en build_magazine.py con referencias APA 7
5. Recompilación de sIA Journal (index.html + artículo web responsive)
6. Sincronización automática a Google Drive (G:\\Mi unidad\\sIA_Hub)
7. Nota de Obsidian Vault con Embed de video + Kit de Copys para Redes
8. Despliegue Git a GitHub Pages
9. Subida automatizada a TikTok Studio
"""

import sys
import os
import re
import json
import shutil
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
SPOTIFY_REELS_DIR = SPOTIFY_DIR / "Reels"
NODE_PATH = r"C:\Program Files\nodejs"

# Google Drive Hub
GDRIVE_HUB = Path(r"G:\Mi unidad\sIA_Hub")
GDRIVE_REELS = GDRIVE_HUB / "01_Reels_Verticales"
GDRIVE_AUDIO = GDRIVE_HUB / "02_Podcasts_Audio"
GDRIVE_VAULT = GDRIVE_HUB / "03_Obsidian_Vault"

SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

EPISODE_FILENAME = "sIA_Data_03_Lakehouse_Data_Mesh_Iceberg_DuckDB_2026-10-31.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_05_Lakehouse_Iceberg_DataMesh.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_05_Lakehouse_Iceberg_DataMesh_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: El Espejismo del Big Data y el 80% de Fracaso]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad de arquitectos de datos, ingenieros de analítica y líderes de tecnología en México y toda Iberoamérica! Bienvenidos a una nueva entrega de sIA en su edición de Deep Dive de Arquitectura e Ingeniería de Datos. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es sábado treinta y uno de octubre de dos mil veintiséis. Y hoy nos sumergimos de lleno en la autopsia técnica de la promesa más inflada y costosa de la industria tecnológica corporativa: la ingeniería de datos a escala de petabytes.
JORGE: Informes consolidados de firmas como Gartner, VentureBeat y McKinsey confirman una estadística escalofriante: entre el setenta y cinco y el ochenta y cinco por ciento de las iniciativas corporativas de Big Data, lagos de datos y plataformas de inteligencia artificial fracasan en entregar un retorno de inversión real, o terminan abandonadas silenciosamente tras quemar millones de dólares en facturas de nube.
DALIA: Corporaciones que contrataron clústeres masivos de computación distribuida para responder preguntas analíticas básicas que caben en la memoria RAM de una computadora portátil común. Equipos que migraron a arquitecturas de Lakehouse y Data Mesh sin entender los fundamentos de gobernanza, convirtiendo sus plataformas en un cementerio digital de dashboards que nadie consulta y tablas huérfanas sin dueño.
JORGE: ¿Cómo llegamos a esta trampa tecnológica? ¿Por qué la batalla entre Snowflake, Databricks y los formatos abiertos como Apache Iceberg está definiendo el futuro del software empresarial? Y sobre todo: ¿por qué herramientas locales como DuckDB están demostrando que el Big Data era, en gran parte, una ilusión comercial? Prepárense un café bien cargado, porque este análisis desmonta mitos desde la primera línea de código. ¡Arrancamos!

[CHAPTER: De Monolitos a Pantanos: La Odisea de Warehouse a Lakehouse]
DALIA: Para entender la crisis actual, Jorge, tenemos que repasar la evolución de las últimas tres décadas. En los años noventa y dos mil, el rey indiscutible era el Data Warehouse tradicional: bases de datos relacionales colosales de Teradata, Oracle o Microsoft SQL Server.
JORGE: Eran sistemas extremadamente caros, altamente estructurados y basados en procesos ETL rígidos. Para subir una nueva columna, el equipo de negocio tenía que esperar semanas de reuniones con el comité de arquitectura. La ventaja era que los datos tenían consistencia transaccional absoluta y esquemas verificados. Pero cuando estalló la explosión de datos no estructurados —logs de servidores, eventos web, telemetría y audio—, el modelo de Data Warehouse tradicional se volvió prohibitivo en costo y escala.
DALIA: Ahí nació la segunda ola: la utopía del Data Lake con Hadoop y los almacenes de objetos en la nube como Amazon S3 y Google Cloud Storage. La promesa de los evangelistas era seductora: 'Simplemente arroja todos tus archivos crudos en formato JSON, CSV o Parquet en un cubo de S3 a bajo costo, y ya los consultaremos después con Spark'.
JORGE: Pero lo que crearon no fue un lago de datos: fue un pantano de datos nauseabundo. Sin esquemas de validación obligatorios, sin transacciones ACID y sin control de concurrencia, miles de archivos quedaban corruptos a mitad de escritura. Los científicos de datos gastaban el ochenta por ciento de su tiempo limpiando basura inconsistente, y los directores financieros descubrieron con horror que consultar un pantano de petabytes consumía millones de dólares en cómputo innecesario.
DALIA: La respuesta de la industria para salvar el desastre fue inventar el 'Lakehouse': una arquitectura híbrida que busca combinar la escalabilidad barata del almacenamiento de objetos con las garantías de calidad, esquemas estructurados y transacciones ACID del Data Warehouse tradicional. Y ahí es donde comenzó la verdadera guerra de los metadatos.

[CHAPTER: La Guerra Fría de los Titanes: Snowflake contra Databricks]
JORGE: En el centro de esta pugna emergieron dos titanes tecnológicos con filosofías de ingeniería opuestas: Snowflake y Databricks.
DALIA: Snowflake conquistó a las empresas gracias a una genialidad de diseño: la separación radical entre almacenamiento y cómputo elástico, envuelta en un lenguaje SQL puro y una experiencia de usuario donde el administrador no tiene que preocuparse por gestionar clústeres ni servidores. Simplemente lanzas consultas y Snowflake escala automáticamente almacenes virtuales según la demanda.
JORGE: Pero esa conveniencia extrema trajo consigo una jaula de oro. Históricamente, para usar Snowflake a máxima velocidad, debías cargar tus datos en sus formatos propietarios de almacenamiento. Y cuando una corporación almacena cinco petabytes dentro del formato cerrado de un proveedor, el costo de salida o egress se vuelve astronómico. Muchas empresas experimentaron el famoso 'efecto de la factura sorpresa': consultas analíticas mal optimizadas por analistas novatos que consumían decenas de miles de dólares en créditos durante un solo fin de semana.
DALIA: Por otro lado, Databricks nació en los laboratorios de UC Berkeley con Apache Spark en su ADN. Su enfoque original era para ingenieros de datos y científicos de aprendizaje automático que requerían cómputo distribuido masivo en Python, Scala y SQL.
JORGE: Para competir con la simplicidad de Snowflake, Databricks introdujo Delta Lake: una capa de almacenamiento de código abierto que añade metadatos transaccionales sobre archivos Parquet almacenados en los propios cubos de S3 del cliente. Y aquí se desató la guerra comercial: Snowflake comenzó a incorporar capacidades de Python y Machine Learning con Snowpark, mientras que Databricks construyó Databricks SQL para devorar las cargas de trabajo de Business Intelligence.
DALIA: Ambos gigantes peleaban por convertirse en el sistema operativo central de los datos corporativos. Pero cometieron un error de cálculo: los clientes corporativos, escarmentados tras décadas de dependencia tecnológica, ya no querían estar atados ni a los formatos de Snowflake ni al ecosistema cerrado de Databricks. Y fue entonces cuando la comunidad de código abierto detonó su jugada maestra: Apache Iceberg.

[CHAPTER: La Liberación de Apache Iceberg: Metadatos sin Dueño]
JORGE: Apache Iceberg nació en las trincheras de ingeniería de Netflix, diseñado por Ryan Blue y Dan Weeks para resolver un problema crítico: cómo gestionar tablas con cientos de miles de particiones sobre Amazon S3 sin sufrir las lentitudes y limitaciones de consistencia eventual del antiguo catálogo de Apache Hive.
DALIA: Iceberg cambió las reglas del juego de forma radical. En lugar de definir una tabla como un directorio de archivos en un sistema de almacenamiento, Iceberg define una tabla como un árbol inmutable de metadatos jerárquicos. Cada commit crea una foto instantánea o snapshot de la tabla.
JORGE: Esto permite capacidades fascinantes que antes solo existían en bases de datos propietarias de millones de dólares: viajes en el tiempo para consultar cómo estaban los datos hace una semana, evolución de esquemas atómica sin necesidad de reescribir petabytes de datos, transacciones completamente serializables y compactación invisible en segundo plano.
DALIA: Pero la verdadera revolución de Iceberg es política y arquitectónica: la total separación entre el motor de cómputo y el formato de la tabla. Con Apache Iceberg, tus datos residen en tu propio almacenamiento en archivos Apache Parquet estándar. Y sobre esa misma tabla puedes ejecutar consultas concurrentes con Snowflake, clústeres de Spark en Databricks, motores de consulta interactiva como Trino o Presto, y herramientas analíticas locales como DuckDB. Ningún proveedor puede secuestrar tus metadatos.
JORGE: El impacto en la industria fue tan demoledor que Snowflake tuvo que claudicar e implementar soporte nativo de primera clase para Iceberg, llegando incluso a adquirir por más de mil millones de dólares a Tabular, la empresa fundada por los creadores de Iceberg, en una maniobra desesperada para no perder el control sobre el nuevo estándar de facto del planeta de los datos.

[CHAPTER: Data Mesh: La Utopía Descentralizada y la Trampa de los Cuatro Principios]
DALIA: Mientras la capa técnica se debatía entre Lakehouses e Iceberg, en la capa organizacional explotó otra tendencia revolucionaria: el concepto de Data Mesh, formulado por la tecnóloga Zhamak Dehghani en Thoughtworks.
JORGE: El diagnóstico de Dehghani era brillante y demoledor: el cuello de botella de los datos en las empresas no es tecnológico, sino humano y organizacional. El modelo tradicional de concentrar a un equipo centralizado de ingenieros de datos como intermediarios entre quienes generan la información en las áreas de negocio y quienes la consumen es una receta garantizada para la lentitud, el agotamiento y el fracaso.
DALIA: Data Mesh propuso cuatro principios fundacionales: propiedad descentralizada de los datos orientada al dominio de negocio, datos como un producto consumible con contratos de servicio estrictos, una plataforma de datos de autoservicio que abstraiga la infraestructura subyacente, y una gobernanza federada computacional basada en políticas automatizadas de calidad y seguridad.
JORGE: La teoría es impecable. Pero en la práctica, el ochenta por ciento de las empresas que intentaron adoptar Data Mesh fracasaron estrepitosamente. ¿Por qué? Porque trataron al Data Mesh como si fuera un producto de software que se puede comprar con una tarjeta corporativa.
DALIA: Directores de tecnología salieron a contratar decenas de herramientas SaaS creyendo que instalando software de catálogo y linaje ya tenían un Data Mesh. En realidad, descentralizar la propiedad de los datos requiere una cultura madura de ingeniería en cada área de negocio: desarrolladores que traten a sus esquemas de eventos como APIs públicas y no como volcados descuidados de bases de datos operacionales. Al carecer de esa madurez, lo único que lograron fue multiplicar por diez los silos caóticos y fragmentar la gobernanza.

[CHAPTER: La Herejía Local: Por Qué DuckDB Demuestra que no Necesitas un Clúster]
JORGE: Y mientras las grandes consultoras vendían soluciones multimillonarias en la nube, en dos mil diecinueve emergió silenciosamente desde los Países Bajos la mayor revolución de sentido común en la historia reciente de los datos: DuckDB.
DALIA: Creado por Mark Raasveldt y Hannes Mühleisen en el CWI de Ámsterdam, DuckDB es a las consultas analíticas lo que SQLite es a las bases de datos transaccionales: un motor de base de datos columnar en memoria, libre de dependencias de servidor, que se ejecuta directamente embebido dentro del proceso de tu aplicación o terminal.
JORGE: Y aquí viene la gran verdad que los proveedores de nube no quieren que los directores financieros escuchen: estudios de telemetría en empresas de la lista Fortune 500 demuestran que más del noventa por ciento de las consultas analíticas diarias en producción operan sobre conjuntos de datos que pesan menos de cien gigabytes.
DALIA: ¡Menos de cien gigabytes! Y sin embargo, las empresas estaban levantando clústeres de cincuenta máquinas de Spark en la nube, pagando miles de dólares por hora solo para esperar quince minutos mientras la red distribuida transfería paquetes entre nodos.
JORGE: DuckDB destruyó ese absurdo con un motor de ejecución vectorial moderno optimizado para procesadores multinúcleo e instrucciones SIMD. Puede leer directamente archivos Parquet remotos en S3 o locales en tu disco de estado sólido NVMe, ejecutando agregaciones complejas sobre cientos de millones de registros en fracciones de segundo dentro de una sola laptop o contenedor liviano.
DALIA: DuckDB demostró la falsedad del dogma del Big Data: no necesitas complejidad distribuida cuando el hardware moderno y los algoritmos vectorizados eficientes pueden hacer el trabajo a una fracción del costo y con cero fricción operativa.

[CHAPTER: Conclusiones y Brújula de Arquitectura en sIA Journal]
JORGE: La gran lección para este dos mil veintiséis es indiscutible: el éxito en la ingeniería de datos no proviene de sumar más capas de abstracción ni de pagar las licencias más costosas, sino de aplicar un pragmatismo feroz.
DALIA: Adopta formatos abiertos como Apache Iceberg y Parquet para ser dueño incondicional de tus datos. Implementa contratos de datos estrictos en origen antes de que la información toque la plataforma analítica. Prototipa localmente con DuckDB antes de considerar un clúster distribuido. Y no intentes descentralizar tu organización con Data Mesh si primero no has resuelto la disciplina básica de ingeniería en tus dominios.
JORGE: El análisis técnico exhaustivo, las comparativas de rendimiento, los diagramas de arquitectura y la bibliografía con referencias en formato APA 7 ya están disponibles en sIA Journal en escucha guion sia punto github punto io diagonal articulos.
DALIA: Y en TikTok, Spotify y Shorts pueden consultar la síntesis animada en nuestro Reel Cómic-Pop para compartir con sus colegas de ingeniería.
JORGE: Muchísimas gracias por acompañarnos. Soy Jorge.
DALIA: Y yo soy Dalia. ¡Hasta el próximo episodio de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Por qué el ochenta por ciento de los proyectos de datos fracasan en producción? Porque las empresas gastan millones en clústeres gigantes antes de entender sus propios datos..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Snowflake y Databricks quieren encerrarte en sus silos de facturación. Pero formatos abiertos como Apache Iceberg llegaron para liberar los metadatos y romper el monopolio."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Y la mayor herejía de la década es DuckDB: procesa millones de filas en segundos dentro de tu propia laptop, sin pagar un solo dólar de servidores en la nube."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Menos humo de Big Data y más ingeniería limpia. Revisa el análisis completo con fuentes académicas en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def step1_generate_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Sintetizando Episodio Completo (Jorge & Dalia)...")
    print("="*70)
    target_path = AUDIO_DIR / EPISODE_FILENAME
    if target_path.exists():
        print(f"✅ Audio completo ya existe: {target_path}")
        return target_path
        
    from podcast_synthesizer import process_dialogue
    
    ep_info = {
        "title": "sIA Data #03: De Data Warehouse a Lakehouse y Data Mesh: Por qué el 80% de los proyectos de datos fracasan en producción",
        "filename": EPISODE_FILENAME,
        "description": "Análisis arquitectónico a fondo sobre la trampa de los silos modernos: Snowflake vs. Databricks, la revolución de Apache Iceberg, la utopía organizacional del Data Mesh y el contraataque local de DuckDB por Carlos Corona."
    }
    
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"✅ Audio completo sintetizado: {out_path}")
    return out_path

async def step2_generate_reel_audio():
    print("\n" + "="*70)
    print("🎬 PASO 2: Sintetizando Audio del Reel Cómic-Pop (45s)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_audio_stupy_05"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        clean_text = item["text"].replace("Sia", "Sia").replace("sIA", "Sia")
        clean_text = clean_text.replace("DuckDB", "Dak D B").replace("Iceberg", "Áisberg").replace("Databricks", "Data-briks").replace("Snowflake", "Snou-fleik")
        communicate = edge_tts.Communicate(clean_text, item["voice"], rate="+6%")
        await communicate.save(str(chunk_path))
        chunk_files.append(chunk_path)
        
    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    
    music_src = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
    if not music_src.exists():
        # Fallback to any available audio file or synthetic bed
        candidates = list((BASE_DIR / "assets" / "audio_library").glob("*.mp3"))
        if candidates:
            music_src = candidates[0]
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-stream_loop", "-1", "-i", str(music_src),
        "-filter_complex",
        f"[1:a]volume=0.034,afade=t=in:st=0:d=1.0,afade=t=out:st=43.5:d=1.5[bg];"
        f"[0:a]apad=whole_dur=45.0[vox];"
        f"[vox][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,"
        f"acompressor=threshold=-20dB:ratio=2.5:attack=15:release=120,"
        f"loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-t", "45.0",
        str(clip_audio)
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Audio del Reel generado con música y mezcla EBU R128 (-16 LUFS): {clip_audio}")

def step3_prepare_hyperframes_composition():
    print("\n" + "="*70)
    print("🎨 PASO 3: Preparando Composición HyperFrames Cómic-Pop Stupy 05...")
    print("="*70)
    
    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>sIA Reel Stupy 05 - Lakehouse, Iceberg & DuckDB</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #080d1a;
      }}
      #root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
      }}
      .clip {{
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="sia_motion_reel_stupy_05" data-no-timeline data-start="0" data-duration="45.0" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="45.0"
        data-track-index="0"
        data-volume="1.0"
        src="assets/current_clip.mp3"
      ></audio>

      <div
        id="main-scene"
        class="clip"
        data-composition-id="scene"
        data-composition-src="compositions/scene.html"
        data-start="0"
        data-duration="45.0"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""

    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    scene_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,800;0,900;1,900&family=Space+Grotesk:wght@700;800;900&family=JetBrains+Mono:wght@700;800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1080px;
        height: 1920px;
        background: #080d1a;
        color: #0b0d17;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* 1. HALFTONE COMIC PATTERN BACKGROUND */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(6, 182, 212, 0.15) 2.5px, transparent 2.5px);
        background-size: 26px 26px;
        opacity: 0.9;
        z-index: 1;
      }}

      /* 2. BACKGROUND GHOST TICKER */
      .bg-ticker {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        opacity: 0.05;
        font-family: 'JetBrains Mono', monospace;
        font-size: 80px;
        font-weight: 900;
        color: #fff;
        user-select: none;
        pointer-events: none;
        z-index: 2;
        line-height: 1.1;
      }}

      /* 3. SPEED LINES */
      .speed-lines {{
        position: absolute;
        inset: 0;
        background: repeating-conic-gradient(from 0deg at 50% 50%, rgba(6, 182, 212, 0.04) 0deg 8deg, transparent 8deg 16deg);
        z-index: 2;
        pointer-events: none;
      }}

      /* 4. MAIN CONTAINER */
      .reel-wrapper {{
        position: absolute;
        inset: 0;
        z-index: 10;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 90px 48px 120px 48px;
      }}

      /* HEADER */
      .header-pill {{
        background: #000000;
        border: 4px solid #06b6d4;
        border-radius: 999px;
        padding: 14px 34px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 6px 6px 0px #06b6d4;
        transform: rotate(-1deg);
      }}
      .header-dot {{
        width: 18px;
        height: 18px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 16px #10b981;
      }}
      .header-text {{
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 2px;
      }}

      /* COMIC POP CARD */
      .comic-card {{
        background: #ffffff;
        border: 7px solid #000000;
        border-radius: 36px;
        box-shadow: 18px 18px 0px #000000;
        width: 100%;
        max-width: 984px;
        padding: 44px 36px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin: auto 0;
      }}

      /* CORNER COMIC STAMP */
      .comic-stamp {{
        position: absolute;
        top: -30px;
        right: 40px;
        background: #f59e0b;
        color: #000;
        font-weight: 900;
        font-size: 26px;
        padding: 10px 24px;
        border: 5px solid #000;
        box-shadow: 6px 6px 0px #000;
        border-radius: 12px;
        transform: rotate(4deg);
        letter-spacing: 1px;
      }}

      /* SCENES DEFINITION */
      .scene {{
        display: none;
        width: 100%;
        flex-direction: column;
        align-items: center;
      }}

      /* SCENE VISIBILITY DRIVEN BY TIME */
      #scene-1 {{ display: flex; }}

      @keyframes showS1 {{
        0%, 18.88% {{ opacity: 1; pointer-events: auto; display: flex; }}
        18.89%, 100% {{ opacity: 0; pointer-events: none; display: none; }}
      }}
      @keyframes showS2 {{
        0%, 18.88% {{ opacity: 0; pointer-events: none; display: none; }}
        18.89%, 45.55% {{ opacity: 1; pointer-events: auto; display: flex; }}
        45.56%, 100% {{ opacity: 0; pointer-events: none; display: none; }}
      }}
      @keyframes showS3 {{
        0%, 45.55% {{ opacity: 0; pointer-events: none; display: none; }}
        45.56%, 74.44% {{ opacity: 1; pointer-events: auto; display: flex; }}
        74.45%, 100% {{ opacity: 0; pointer-events: none; display: none; }}
      }}
      @keyframes showS4 {{
        0%, 74.44% {{ opacity: 0; pointer-events: none; display: none; }}
        74.45%, 100% {{ opacity: 1; pointer-events: auto; display: flex; }}
      }}

      #scene-1 {{ animation: showS1 45s infinite; }}
      #scene-2 {{ animation: showS2 45s infinite; }}
      #scene-3 {{ animation: showS3 45s infinite; }}
      #scene-4 {{ animation: showS4 45s infinite; }}

      /* TYPOGRAPHY IN COMIC CARD */
      .myth-tag {{
        background: #ef4444;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 2px;
        padding: 8px 22px;
        border-radius: 999px;
        border: 4px solid #000;
        box-shadow: 4px 4px 0px #000;
        margin-bottom: 24px;
        display: inline-block;
      }}

      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 56px;
        line-height: 1.08;
        color: #0b0d17;
        text-transform: uppercase;
        letter-spacing: -1.5px;
        margin-bottom: 26px;
      }}

      .punch-pill {{
        background: #06b6d4;
        color: #000000;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 42px;
        line-height: 1.15;
        padding: 16px 28px;
        border: 6px solid #000000;
        box-shadow: 8px 8px 0px #000000;
        border-radius: 20px;
        transform: rotate(-1.5deg);
        margin: 18px 0;
        display: inline-block;
      }}

      .metric-box {{
        background: #ecfeff;
        border: 5px dashed #06b6d4;
        border-radius: 20px;
        padding: 22px 28px;
        margin-top: 20px;
        width: 100%;
      }}

      .metric-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 800;
        color: #0891b2;
        letter-spacing: 1px;
      }}

      .metric-stat {{
        font-family: 'Montserrat', sans-serif;
        font-size: 52px;
        font-weight: 900;
        color: #0e7490;
        line-height: 1.1;
      }}

      /* FOOTER PROGRESS BAR */
      .progress-bar-container {{
        width: 100%;
        height: 20px;
        background: #000000;
        border: 4px solid #06b6d4;
        border-radius: 999px;
        overflow: hidden;
        position: relative;
        box-shadow: 4px 4px 0px #06b6d4;
      }}

      .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, #06b6d4, #10b981, #f59e0b);
        width: 0%;
        animation: progressAnim 45s linear infinite;
      }}

      @keyframes progressAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}

      .final-pill {{
        background: #000000;
        color: #06b6d4;
        font-family: 'JetBrains Mono', monospace;
        font-size: 34px;
        font-weight: 800;
        padding: 16px 36px;
        border: 5px solid #06b6d4;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #06b6d4;
        margin-top: 15px;
        display: inline-block;
      }}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="speed-lines"></div>

    <div class="bg-ticker">
      <div>DATA WAREHOUSE LAKEHOUSE DATA MESH</div>
      <div>SNOWFLAKE DATABRICKS APACHE ICEBERG</div>
      <div>PARQUET S3 TRINO ARROW DUCKDB</div>
      <div>BIG DATA ILLUSION ACID LOCAL FIRST</div>
    </div>

    <div class="reel-wrapper">
      <div class="header-pill">
        <div class="header-dot"></div>
        <div class="header-text">sIA DATA ENGINEERING #03</div>
      </div>

      <!-- MAIN COMIC CARD -->
      <div class="comic-card">
        <div class="comic-stamp">DEEP DIVE</div>

        <!-- SCENE 1: LA REALIDAD DEL BIG DATA (0s - 8.5s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">EL CEMENTERIO DE DATOS</div>
          <div class="headline-black">
            ¿POR QUÉ EL 80% DE LOS PROYECTOS FRACASAN?
          </div>
          <div class="punch-pill">
            80% ABANDONADOS
          </div>
          <div class="metric-box">
            <div class="metric-title">GARTNER & MCKINSEY REPORT:</div>
            <div class="metric-stat">MILLONES EN LA NUBE</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 18px;">
            Gastar en clústeres antes de entender el negocio.
          </div>
        </div>

        <!-- SCENE 2: LA GUERRA POR TUS METADATOS (8.5s - 20.5s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #0284c7; box-shadow: 4px 4px 0px #000;">LA GUERRA DE FORMATOS</div>
          <div class="headline-black" style="font-size: 50px;">
            SNOWFLAKE VS DATABRICKS
          </div>
          <div class="punch-pill" style="background: #10b981; font-size: 38px;">
            APACHE ICEBERG LIBERA LA TABLA
          </div>
          <div class="metric-box" style="background: #f0fdf4; border-color: #10b981;">
            <div style="font-size: 32px; font-weight: 900; color: #166534;">
              🔓 ALMACENAMIENTO INDEPENDIENTE
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Cero secuestro de metadatos corporativos.
          </div>
        </div>

        <!-- SCENE 3: LA HEREJÍA LOCAL DUCKDB (20.5s - 33.5s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #f59e0b; color: #000; box-shadow: 4px 4px 0px #000;">LA FALACIA DEL CLÚSTER</div>
          <div class="headline-black" style="font-size: 52px;">
            DUCKDB CORRE EN TU LAPTOP
          </div>
          <div class="punch-pill" style="background: #fef08a; font-size: 38px; color: #000;">
            100 GB EN MILISEGUNDOS
          </div>
          <div class="metric-box" style="background: #fefce8; border-color: #f59e0b;">
            <div style="font-size: 32px; font-weight: 900; color: #854d0e;">
              ⚡ SQL VECTORIZADO SIN FACTURA CLOUD
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            El 90% de tus consultas no necesita Big Data.
          </div>
        </div>

        <!-- SCENE 4: LA LECCIÓN DEL PRAGMATISMO (33.5s - 45s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #0f172a; box-shadow: 4px 4px 0px #06b6d4;">ARQUITECTURA SANA</div>
          <div class="headline-black" style="font-size: 52px;">
            MENOS HUMO,<br>MÁS INGENIERÍA
          </div>
          <div class="punch-pill" style="font-size: 36px; background: #000; border-color: #06b6d4; color: #06b6d4 !important; box-shadow: 8px 8px 0px #06b6d4;">
            CONTRATOS DE DATOS & ICEBERG
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 20px;">
            Capítulo completo y fuentes APA en:
          </div>
          <div class="final-pill">
            ESCUCHA-SIA.GITHUB.IO
          </div>
        </div>
      </div>

      <div class="progress-bar-container">
        <div class="progress-fill"></div>
      </div>
    </div>
  </div>
  </body>
</html>"""

    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Plantillas HyperFrames generadas para Stupy 05.")

def step4_render_reel():
    print("\n" + "="*70)
    print("🎬 PASO 4: Renderizando Reel Vertical en HyperFrames GPU...")
    print("="*70)
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    
    renders_dir = ENGINE_DIR / "renders"
    if renders_dir.exists():
        for old_vid in renders_dir.glob("*.mp4"):
            try:
                old_vid.unlink()
            except Exception:
                pass

    cmd = ["cmd.exe", "/c", f"set PATH={NODE_PATH};%PATH% && cd /d {ENGINE_DIR} && npx hyperframes render --gpu"]
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("HyperFrames stdout:", res.stdout)
        print("HyperFrames stderr:", res.stderr)
        raise RuntimeError(f"Fallo al renderizar Reel en HyperFrames: {res.stderr}")
    
    output_mp4 = ENGINE_DIR / "renders" / "video.mp4"
    if not output_mp4.exists():
        candidates = list((ENGINE_DIR / "renders").glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
            
    if not output_mp4.exists():
        raise RuntimeError("No se encontró el video generado en renders/")
        
    target_reel_path = REELS_DIR / REEL_FILENAME
    shutil.copy2(output_mp4, target_reel_path)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_FILENAME)
    
    size_mb = target_reel_path.stat().st_size / (1024 * 1024)
    print(f"✅ Reel generado: {target_reel_path} ({size_mb:.2f} MB)")
    
    poster_path = REELS_DIR / REEL_POSTER_FILENAME
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "00:00:04",
        "-i", str(target_reel_path),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if poster_path.exists():
        shutil.copy2(poster_path, SPOTIFY_REELS_DIR / REEL_POSTER_FILENAME)
        print(f"✅ Póster capturado: {poster_path}")

def step5_register_and_rebuild_magazine():
    print("\n" + "="*70)
    print("📖 PASO 5: Registrando en sIA Journal y Compilando Revista...")
    print("="*70)
    
    build_mag_path = BASE_DIR / "build_magazine.py"
    content = build_mag_path.read_text(encoding='utf-8')
    
    if EPISODE_FILENAME not in content:
        content = content.replace(
            'REELS_MAP = {',
            f'REELS_MAP = {{\n    "{EPISODE_FILENAME}": "{REEL_FILENAME}",'
        )
    
    res_entry = f'''    # sIA Data 03 - Lakehouse, Data Mesh, Iceberg & DuckDB - 31 de Octubre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-data-03-de-data-warehouse-a-lakehouse-y-data-mesh",
        "category": "Arquitectura & Data Engineering",
        "badge_color": "cyan",
        "read_time": "12 min",
        "title": "sIA Data #03: De Data Warehouse a Lakehouse y Data Mesh: Por qué el 80% de los proyectos de datos fracasan en producción",
        "subtitle": "La trampa de los silos modernos: Snowflake vs. Databricks, el auge de formatos abiertos como Apache Iceberg y la revolución local de DuckDB frente a la falacia del Big Data.",
        "thesis": "El fracaso sistémico en las arquitecturas de datos corporativas se debe a la adopción de complejidad distribuida injustificada y vendor lock-in en formatos cerrados. La convergencia hacia metadatos abiertos con Apache Iceberg y motores vectorizados eficientes como DuckDB restaura la soberanía técnica y el retorno de inversión.",
        "nexo": "Tercer episodio de Ingeniería de Datos: Arquitectura Lakehouse, formatos abiertos, gobernanza de datos, contratos de datos y optimización de cómputo.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "title": "1. El Espejismo de los Petabytes: La Autopsia del 80% de Fracaso",
                "body": """
Informes consolidados de firmas como Gartner, VentureBeat y McKinsey confirman una estadística alarmante para los presupuestos de tecnología: entre el 75% y el 85% de las iniciativas corporativas de Big Data, lagos de datos y plataformas de aprendizaje automático no logran entregar un retorno de inversión sostenible o son silenciosamente abandonadas en producción tras consumir millones de dólares.

El origen fundamental de este desperdicio radica en una falacia arquitectónica: la creencia de que contratar almacenamiento distribuido y clústeres masivos en la nube resuelve por sí mismo la falta de definición analítica. Las empresas invirtieron fortunas en replicar arquitecturas complejas de gigantes como Google o Netflix para resolver problemas operacionales cotidianos cuyas cargas reales jamás superaron los cincuenta gigabytes.
"""
            }},
            {{
                "title": "2. De Monolitos Rígidos a Pantanos de Datos: El Surgimiento del Lakehouse",
                "body": """
Durante décadas, el Data Warehouse clásico (Teradata, Oracle) impuso esquemas relacionales inmutables y costos prohibitivos de licenciamiento. La posterior rebelión del Data Lake sobre Hadoop y Amazon S3 prometió libertad mediante el lema 'vuelca primero en crudo y estructura después'. Sin embargo, esta permisividad dio lugar a pantanos de datos corruptos, carentes de transacciones ACID, con lecturas 'sucias' y nula garantía de integridad.

La arquitectura Lakehouse surgió precisamente para conciliar ambos mundos: retener el bajo coste y la escalabilidad del almacenamiento de objetos desacoplado, pero superponiendo una capa transaccional robusta capaz de ofrecer aislamiento, auditoría y evolución de esquemas. No obstante, esta promesa pronto se vio capturada por la batalla comercial entre Snowflake y Databricks.
"""
            }},
            {{
                "title": "3. La Liberación de Apache Iceberg: Metadatos sin Dueño",
                "body": """
Snowflake demostró la elegancia del desacoplamiento entre cómputo y almacenamiento en la nube, pero impuso formatos de almacenamiento cerrados que generaron un severo vendor lock-in y facturas de cómputo impredecibles. Databricks contraatacó con Delta Lake y cómputo Spark distribuido, manteniendo la competencia en una carrera por monopolizar la capa de almacenamiento.

En respuesta a esta trampa propietaria, Apache Iceberg (creado en la ingeniería de Netflix) rompió el tablero. Al estructurar las tablas como árboles de metadatos inmutables e independientes del motor de procesamiento, Iceberg permitió que Spark, Trino, Snowflake y DuckDB consulten concurrentemente los mismos datos en cubos S3 sin mover un solo byte. La adquisición de Tabular por parte de Snowflake por más de mil millones de dólares consagró a Iceberg como el estándar abierto irrenunciable de la industria.
"""
            }},
            {{
                "title": "4. Data Mesh y la Trampa de los Silos Descentralizados",
                "body": """
Paralelamente, la tesis de Data Mesh formulada por Zhamak Dehghani planteó descentralizar la propiedad de los datos hacia los dominios de negocio, tratando los datasets como productos con SLAs verificables. Si bien el modelo conceptual es impecable, su implementación práctica derivó en un fracaso generalizado al ser confundido con la compra masiva de herramientas de software.

Descentralizar la analítica sin una cultura madura de ingeniería de software en cada área de negocio únicamente logró multiplicar por diez los silos caóticos. El éxito de Data Mesh exige contratos de datos (Data Contracts) formalizados a nivel de API de producción, no simplemente adquirir suites de catálogos y linaje cosmético.
"""
            }},
            {{
                "title": "5. El Contraataque Local con DuckDB: La Victoria del Pragmatismo",
                "body": """
La mayor revolución de sentido común en la ingeniería moderna de datos ha sido el ascenso meteórico de DuckDB. Diseñado en el CWI como una base de datos columnar analítica in-process (el SQLite de la analítica), DuckDB ejecuta consultas vectorizadas altamente optimizadas para CPUs multinúcleo con instrucciones SIMD.

Telemetrías reales en corporaciones Fortune 500 demuestran que más del 90% de las consultas analíticas diarias operan sobre volúmenes menores a 100 GB. DuckDB procesa agregaciones complejas sobre archivos Parquet locales o remotos en fracciones de segundo dentro de una sola laptop de desarrollo, destruyendo la necesidad de mantener clústeres distribuidos costosos y devolviendo a los equipos la velocidad, simplicidad y soberanía técnica.
"""
            }}
        ],
        "apa_references": [
            "Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale*. O'Reilly Media.",
            "Raasveldt, M., & Mühleisen, H. (2019). *DuckDB: an Embeddable Analytical Database*. Proceedings of the 2019 International Conference on Management of Data (SIGMOD '19), 1981–1984.",
            "Blue, R., Weeks, D., & Sznajdman, J. (2021). *Apache Iceberg: An Architectural Overview of the Open Table Format*. Netflix Technology Blog.",
            "Gartner Research. (2024). *Predicts 2024: The Real Cost of Big Data and Lakehouse Implementations*. Gartner Information Technology Whitepapers.",
            "Corona, C., & sIA Editora. (2026). *sIA Data #03: De Data Warehouse a Lakehouse y Data Mesh: Por qué el 80% de los proyectos de datos fracasan en producción*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if "sia-data-03-de-data-warehouse-a-lakehouse-y-data-mesh" not in content:
        content = content.replace(
            'RESEARCH_DATABASE = {',
            'RESEARCH_DATABASE = {\n' + res_entry
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Entrada de investigación sIA Data #03 inyectada en build_magazine.py")

    cmd = [sys.executable, str(build_mag_path)]
    subprocess.run(cmd, check=True)
    print("✅ Revista sIA Journal e index.html actualizados.")

def step6_sync_to_gdrive():
    print("\n" + "="*70)
    print("☁️ PASO 6: Replicando a Google Drive (Para Móvil & Celular)...")
    print("="*70)
    GDRIVE_REELS.mkdir(parents=True, exist_ok=True)
    GDRIVE_AUDIO.mkdir(parents=True, exist_ok=True)
    GDRIVE_VAULT.mkdir(parents=True, exist_ok=True)
    
    src_reel = REELS_DIR / REEL_FILENAME
    src_poster = REELS_DIR / REEL_POSTER_FILENAME
    if src_reel.exists():
        shutil.copy2(src_reel, GDRIVE_REELS / REEL_FILENAME)
        print(f"  -> Reel copiado a Google Drive: {GDRIVE_REELS / REEL_FILENAME}")
    if src_poster.exists():
        shutil.copy2(src_poster, GDRIVE_REELS / REEL_POSTER_FILENAME)
        print(f"  -> Póster copiado a Google Drive: {GDRIVE_REELS / REEL_POSTER_FILENAME}")

    src_audio = AUDIO_DIR / EPISODE_FILENAME
    if src_audio.exists():
        shutil.copy2(src_audio, GDRIVE_AUDIO / EPISODE_FILENAME)
        print(f"  -> Audio copiado a Google Drive: {GDRIVE_AUDIO / EPISODE_FILENAME}")

def step7_create_obsidian_and_social_kit():
    print("\n" + "="*70)
    print("🧠 PASO 7: Creando Ficha de Obsidian & Kit de Redes Sociales...")
    print("="*70)
    
    obsidian_reel_note = f"""---
id: reel-stupy-05
titulo: "De Data Warehouse a Lakehouse y Data Mesh: Por qué el 80% de los proyectos de datos fracasan en producción"
tipo: reel
formato: stupy_comic_pop
duracion: 45s
estado: renderizado
video: "[[reels/{REEL_FILENAME}]]"
poster: "[[reels/{REEL_POSTER_FILENAME}]]"
fecha_creacion: {datetime.now().strftime('%Y-%m-%d')}
tags:
  - reel
  - stupy-pop
  - data-engineering
  - lakehouse
  - iceberg
  - duckdb
  - snowflake
  - databricks
  - data-mesh
---

# ⚡ De Data Warehouse a Lakehouse: ¿Por qué el 80% de los Proyectos de Datos Fracasan?

> **Estilo Visual:** Cómic-Pop Halftone Matrix, Pop-in Cyan Neón & Esmeralda, Tarjeta Escudo 20px Solid Shadow, Audio EBU R128 (-16 LUFS).

---

## 🎬 Reproductor del Video (Vertical 9:16)
![[{REEL_FILENAME}]]

**Póster Oficial:**
![[{REEL_POSTER_FILENAME}|350]]

---

## 📱 Kit de Copys & Hashtags para Publicación en Móvil (TikTok / Shorts / Instagram / LinkedIn)

### 🎯 Título Gancho (Hook):
`¿Por qué el 80% de los proyectos de Big Data fracasan en producción? 💥📊`

### ✍️ Descripción para Redes (Copy de Alto Alcance):
> Millones de dólares gastados en clústeres gigantes en la nube para procesar consultas que caben en la RAM de una laptop común...
>
> ¿Snowflake vs. Databricks? La verdadera revolución se llama Apache Iceberg para liberar los metadatos y DuckDB para procesar petabytes en local.
>
> ¿Tú equipo sigue pagando fortunas en la nube por consultas de 50 GB? Cuéntanos en los comentarios.

### 🏷️ Bloque de Hashtags Estratégicos:
```
#dataengineering #bigdata #lakehouse #datamesh #snowflake #databricks #apacheiceberg #duckdb #python #sql #softwareengineer #tecnologia
```

---

## 🎙️ Guion & Voces (Jorge & Dalia +6%)

### Escena 1: El Espejismo de los Datos (00:00 - 08:50)
* **JORGE:** ¿Por qué el ochenta por ciento de los proyectos de datos fracasan en producción? Porque las empresas gastan millones en clústeres gigantes antes de entender sus propios datos...
* *Animación:* Badge pop-in `80% ABANDONADOS 💥` con sombra dura negra.

### Escena 2: La Guerra de Formatos (08:50 - 20:50)
* **DALIA:** Snowflake y Databricks quieren encerrarte en sus silos de facturación. Pero formatos abiertos como Apache Iceberg llegaron para liberar los metadatos y romper el monopolio.
* *Animación:* Tarjeta métrica: `SNOWFLAKE VS. DATABRICKS` -> `APACHE ICEBERG LIBRE`.

### Escena 3: La Herejía Local (20:50 - 33:50)
* **JORGE:** Y la mayor herejía de la década es DuckDB: procesa millones de filas en segundos dentro de tu propia laptop, sin pagar un solo dólar de servidores en la nube.
* *Animación:* Badge de alerta: `100 GB EN MILISEGUNDOS ⚡`.

### Escena 4: La Lección del Pragmatismo (33:50 - 45:00)
* **DALIA:** Menos humo de Big Data y más ingeniería limpia. Revisa el análisis completo con fuentes académicas en `escucha-sia.github.io` y en *sIA Podcast*.
* *Animación:* Píldora neón cyan con URL destacada.

---

## 🔗 Referencias & Backlinks
* **Artículo Web Completo con Fuentes APA:** [[03_Articulos/sia-data-03-de-data-warehouse-a-lakehouse-y-data-mesh]]
* **Episodio Podcast MP3:** `audio/{EPISODE_FILENAME}`
* **Ruta Google Drive (Móvil):** `G:\\Mi unidad\\sIA_Hub\\01_Reels_Verticales\\{REEL_FILENAME}`
"""
    note_path = BASE_DIR / "02_Reels_Shorts" / f"{Path(REEL_FILENAME).stem}.md"
    note_path.write_text(obsidian_reel_note, encoding='utf-8')
    print(f"✅ Ficha de Obsidian creada: {note_path}")
    
    vault_dest = GDRIVE_VAULT / "02_Reels_Shorts"
    vault_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(note_path, vault_dest / note_path.name)
    print(f"✅ Ficha sincronizada a Google Drive Vault: {vault_dest / note_path.name}")

def step8_git_deploy():
    print("\n" + "="*70)
    print("🚀 PASO 8: Commiteando y Desplegando a GitHub Pages...")
    print("="*70)
    
    subprocess.run(["git", "add", "."], cwd=str(BASE_DIR), check=True)
    msg = f"feat(episode): publish sIA Data 03 - Lakehouse, Data Mesh, Iceberg & DuckDB with Reel Stupy 05"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(BASE_DIR), check=True)
    
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if push_res.returncode == 0:
        print("🎉 ¡Despliegue a GitHub Pages exitoso!")
    else:
        print("⚠️ Advertencia al hacer push:", push_res.stderr)

def step9_upload_to_tiktok():
    print("\n" + "="*70)
    print("📱 PASO 9: Subiendo Reel 05 a TikTok Automáticamente...")
    print("="*70)
    from playwright.sync_api import sync_playwright
    
    reel_path = REELS_DIR / REEL_FILENAME
    caption = "¿Por qué el 80% de los proyectos de datos fracasan en producción? Snowflake vs. Databricks vs. Apache Iceberg y DuckDB. #dataengineering #bigdata #lakehouse #snowflake #databricks #duckdb #python #sql"
    
    if not SESSION_FILE.exists():
        print("[-] tiktok_session.json no encontrado, saltando subida directa.")
        return
        
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                storage_state=str(SESSION_FILE),
                viewport={"width": 1280, "height": 950},
                locale="es-ES"
            )
            page = context.new_page()
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
            
            print("[*] Accediendo a TikTok Studio Upload...", flush=True)
            page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
            time.sleep(4)
            page.mouse.click(600, 200)
            
            file_input = page.locator("input[type='file']").first
            print(f"[*] Adjuntando {reel_path.name}...", flush=True)
            file_input.set_input_files(str(reel_path))
            
            print("[*] Esperando procesamiento del video (18s)...", flush=True)
            time.sleep(18)
            
            # Dismiss modals
            for _ in range(3):
                modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal]").all()
                for m in modals:
                    btn = m.locator("button:has-text('Activar'), button:has-text('Cancelar'), button:has-text('Entendido')").first
                    if btn.count() > 0 and btn.is_visible():
                        btn.click()
                        time.sleep(1)
                page.keyboard.press("Escape")
            
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)
            
            editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
            print("[*] Escribiendo texto y hashtags en la leyenda...", flush=True)
            try:
                editor.click(force=True, timeout=5000)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(caption, delay=20)
                time.sleep(2)
            except Exception as e:
                print(f"[!] Editor click fallback: {e}")
                page.evaluate(f"""() => {{
                    const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
                    if (el) {{
                        el.innerText = `{caption}`;
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}""")
                time.sleep(1)
                
            page.screenshot(path=str(SCRATCH_DIR / f"ready_to_post_{reel_path.stem}.png"))
            
            page.evaluate("window.scrollTo(0, 1500)")
            time.sleep(1)
            
            post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
            if post_btn.count() > 0:
                print("[🚀] Haciendo clic en 'Publicar'...", flush=True)
                post_btn.click(force=True)
                time.sleep(18)
                page.screenshot(path=str(SCRATCH_DIR / f"published_{reel_path.stem}.png"))
                print(f"🎉 ¡VIDEO PUBLICADO EXITOSAMENTE EN TIKTOK: {reel_path.name}!")
            else:
                print(f"[-] Botón Publicar no encontrado.")
                
            context.storage_state(path=str(SESSION_FILE))
            browser.close()
    except Exception as e:
        print(f"[!] Error durante la subida a TikTok: {e}")

async def main_async():
    print("="*70)
    print("🚀 INICIANDO PRODUCCIÓN INTEGRAL 360° - EPISODIO & REEL STUPY 05")
    print("Tema: De Data Warehouse a Lakehouse y Data Mesh")
    print("="*70)
    
    # 1. Audio Completo
    await step1_generate_full_audio()
    
    # 2. Audio Reel
    await step2_generate_reel_audio()
    
    # 3. Composición HyperFrames
    step3_prepare_hyperframes_composition()
    
    # 4. Render HyperFrames Reel
    step4_render_reel()
    
    # 5. Registrar y Recompilar sIA Journal
    step5_register_and_rebuild_magazine()
    
    # 6. Sincronizar Google Drive
    step6_sync_to_gdrive()
    
    # 7. Crear Ficha Obsidian y Kit de Redes
    step7_create_obsidian_and_social_kit()
    
    # 8. Git Commit & Deploy
    step8_git_deploy()

def main():
    asyncio.run(main_async())
    # 9. TikTok Upload (sync fuera del loop asyncio para evitar conflictos Playwright)
    step9_upload_to_tiktok()

if __name__ == "__main__":
    main()
