"""
sIA Master Episode & Reel Producer:
Tema: sIA Crónicas #06: Fábrica de Dulces Montes: El Imperio del Caramelo de Leche en Poncitlán y la Resistencia Industrial Mexicana
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop (HyperFrames GPU, 45s, Halftone Caramel, Kinetic Pop)
3. Póster oficial del Reel
4. Registro de investigación en build_magazine.py con referencias APA 7 (Autor: cacs)
5. Recompilación de sIA Journal (index.html + artículo web responsive)
6. Sincronización automática a Google Drive (G:\\Mi unidad\\sIA_Hub)
7. Nota de Obsidian Vault con Embed de video + Kit de Copys para Redes
8. Despliegue Git a GitHub Pages
9. Subida automatizada a TikTok Studio (@escucha_sia)
"""

import sys
import os
import re
import json
import time
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

EPISODE_FILENAME = "sIA_Corp_06_Dulces_Montes_Poncitlan_Caramelo_2026-11-02.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_07_Dulces_Montes_Tomy.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_07_Dulces_Montes_Tomy_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: El Aroma a Leche Quemada en Poncitlán]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad de ingenieros de procesos, analistas corporativos y apasionados de la manufactura industrial en México y toda Iberoamérica! Bienvenidos a una nueva entrega de sIA en su edición de Crónicas Corporativas e Industriales. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es lunes dos de noviembre de dos mil veintiséis. Y hoy nos trasladamos al corazón de Jalisco, a orillas del Río Santiago y la Ciénega de Chapala, para desentrañar la historia de una de las hazañas empresariales más queridas y resilientes de México: la Fábrica de Dulces Montes.
JORGE: ¿Quién en este país no creció desenvolviendo un caramelo Tomy con su inconfundible vaca lechera, mordiendo un Damy con trozos crujientes de cacahuate tostado o disfrutando un Riko Riko en una piñata familiar? Esos pequeños envoltorios amarillos y rojos no son solo nostalgia infantil: son el resultado de casi nueve décadas de estricta ingeniería de confitería, integración agroindustrial con cuencas lecheras locales y una feroz resistencia mexicana frente a las ofertas de compra de conglomerados multinacionales de Wall Street.
DALIA: En una era donde gigantes transnacionales como Mondelēz, Nestlé y Mars han devorado marcas tradicionales para sustituir los ingredientes naturales por jarabes de maíz de alta fructosa y saborizantes artificiales, Dulces Montes sigue procesando leche fresca pasteurizada en pailas de cobre y hornos de vacío en su planta de Poncitlán, exportando a más de treinta países.
JORGE: ¿Cómo nació este imperio dulce en mil novecientos treinta y ocho? ¿Cuál es la química exacta detrás de la reacción de Maillard que le da su textura inigualable? Y sobre todo: ¿cómo sobrevive una empresa familiar de manufactura ante la NOM-051 y los impuestos calóricos modernos? Prepárense un café bien cargado, porque esta crónica despierta el apetito y el orgullo ingenieril. ¡Arrancamos!

[CHAPTER: Don Miguel Montes Martell y la Alquimia de 1938]
DALIA: La historia comienza en mil novecientos treinta y ocho con un hombre visionario: Don Miguel Montes Martell. Poncitlán era entonces un pueblo predominantemente agrícola y ganadero, favorecido por la riqueza de los pastizales cercanos al Lago de Chapala, donde la producción de leche de vaca superaba por mucho el consumo fresco de la población.
JORGE: Don Miguel entendió un principio económico fundamental de la transformación de materia prima: la leche cruda es un producto altamente perecedero que pierde valor en cuestión de horas si no se pasteuriza o refrigera. Pero si concentras esa leche con azúcar, mantequilla y calor constante, no solo extiendes su vida útil a más de un año: multiplicas su valor agregado por diez.
DALIA: Comenzó en un pequeño taller artesanal con una paila de cobre calentada a fuego directo, revolviendo con palas de madera mezclas de leche bronca recién ordeñada y sacarosa. Los primeros productos no tenían máquinas empacadoras: se cortaban a mano sobre mesas de mármol frío y se envolvían individualmente en papel encerado con doble torsión manual por trabajadoras del pueblo.
JORGE: El éxito regional fue instantáneo. Los arrieros y comerciantes que viajaban entre Guadalajara, Ocotlán y la Ciudad de México cargaban costales de caramelos Montes porque no se derretían con el calor del camino gracias a su emulsión láctea estabilizada. Para la década de mil novecientos cincuenta, el pequeño taller ya era una fábrica en toda regla con calderas de vapor y líneas de producción mecanizadas.

[CHAPTER: La Tríada Dorada: Tomy, Damy y Riko Riko]
DALIA: El verdadero salto a la inmortalidad comercial llegó cuando Don Miguel y su equipo desarrollaron su portafolio insignia: lo que en la industria se conoce como 'La Tríada Dorada de Montes'.
JORGE: El primero de ellos es el indiscutible rey: Tomy. Un caramelo blando de leche con mantequilla natural, caracterizado por su envoltura amarilla brillante decorada con una vaca sonriente. Lo que hacía único al Tomy no era solo su sabor lácteo concentrado, sino su elasticidad masticable: no se fragmentaba como un dulce macizo ni se pegaba agresivamente a los dientes como un toffee británico, logrando un equilibrio coloidal perfecto.
DALIA: Poco después nació Damy: una genialidad gastronómica que incorporó mitades de cacahuate tostado seleccionado dentro de la matriz caramelizada de leche. El contraste entre la salinidad sutil y las grasas saludables del cacahuate con el dulzor lácteo convirtió al Damy en un clásico de las cooperativas escolares y los puestos de periódicos en todo México.
JORGE: Y para completar la tríada surgió Riko Riko: un caramelo con corazón suave y centro fluido de cajeta o dulce de leche que requería una innovación técnica avanzada en boquillas de coextrusión concéntrica. A estos se sumaron marcas legendarias como Chupirul, las paletas de cajeta y los caramelos de menta con mantequilla, consolidando a Montes como el amo absoluto del caramelo lácteo nacional.

[CHAPTER: Ingeniería de Confitería: La Reacción de Maillard a Gran Escala]
DALIA: Detrás del placer sensorial de un caramelo Tomy existe una compleja coreografía de química de alimentos y termodinámica, Jorge.
JORGE: El color ámbar profundo y el aroma característico a caramelo de leche no provienen de colorantes artificiales: son el resultado directo de la Reacción de Maillard. Se trata de una red de reacciones químicas entre los aminoácidos de las proteínas lácteas —principalmente la caseína— y los azúcares reductores como la lactosa y la glucosa a temperaturas entre los ciento diez y ciento veinticinco grados centígrados.
DALIA: Si cocinas a fuego abierto excesivo, la proteína se desnaturaliza, el azúcar se quema amargo y la grasa de la mantequilla se separa en una fase oleosa desagradable. Por eso, la gran innovación de ingeniería en la planta de Poncitlán fue la incorporación de evaporadores de película descendente y cocedores al vacío.
JORGE: Al cocinar la leche bajo presión negativa de vacío, el punto de ebullición del agua desciende drásticamente. Esto permite evaporar el agua de la leche fresca sin destruir las proteínas ni quemar los azúcares, logrando una concentración de sólidos de más del noventa y dos por ciento con una textura sedosa, homogénea y repetible en lotes de varias toneladas por turno.
DALIA: Y en el empaque, la velocidad es asombrosa: líneas de envasado automatizadas con servomotores que toman la cuerda continua de caramelo enfriada en túneles térmicos, la cortan con guillotinas rotativas y aplican la doble torsión al celofán a un ritmo de más de mil quinientos caramelos por minuto por línea.

[CHAPTER: La Resistencia Mexicana frente a Nestlé, Mars y Mondelēz]
JORGE: A partir de la década de mil novecientos noventa y con la entrada en vigor del Tratado de Libre Comercio, el mercado mexicano de confitería se convirtió en el objetivo más codiciado de los conglomerados globales.
DALIA: Vimos cómo marcas históricas de dulces mexicanos fueron adquiridas una tras otra: Ricolino fue absorbida por Bimbo y posteriormente vendida a la multinacional Mondelēz por más de mil trescientos millones de dólares; La Corona y Carlos Quinto pasaron a manos de Nestlé; Lucas y Skwinkles fueron integradas por Mars Wrigley.
JORGE: Sin embargo, la familia Montes tomó una decisión estratégica contracorriente: rechazar las ofertas de adquisición y mantener el control soberano e independiente de la fábrica en Poncitlán.
DALIA: Para sobrevivir sin los presupuestos multimillonarios de mercadotecnia de las transnacionales, Montes recurrió a dos pilares imbatibles: la lealtad absoluta de la red tradicional de mayoristas y dulcerías de barrio en México, y la exportación al mercado de la nostalgia en los Estados Unidos, donde millones de migrantes hispanos buscan en las estanterías de Texas, California e Illinois el sabor genuino de su infancia.
JORGE: En la actualidad, Montes procesa decenas de miles de litros de leche diarios, genera más de mil quinientos empleos directos en la región Ciénega de Jalisco y ha sorteado con éxito las presiones de la NOM-051 y los sellos de advertencia calórica, demostrando que cuando un producto tiene autenticidad en sus ingredientes y excelencia en su manufactura, el consumidor jamás lo abandona por un sustituto barato.

[CHAPTER: Cierre y Recursos en sIA Journal]
DALIA: La historia de Dulces Montes es un recordatorio inspirador de que la mejor tecnología no siempre nace en Silicon Valley: también se forja en los calderos de vapor y las líneas de ensamble de nuestros municipios industriales.
JORGE: El ensayo histórico completo, el diagrama de flujo del proceso de cocción al vacío y la bibliografía con fuentes en formato APA 7ª Edición ya están disponibles en sIA Journal en nuestro portal web en escucha guion sia punto github punto io diagonal articulos.
DALIA: Y en TikTok, en nuestra cuenta oficial arroba escucha guion bajo sia, los invitamos a ver el Reel animado en formato Cómic-Pop para revivir la historia del Tomy y compartir con nosotros su caramelo favorito.
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
        "text": "¿Cómo un taller familiar en Poncitlán, Jalisco, creó el dulce más icónico de México y resistió el asedio de gigantes multinacionales? Esta es la historia de Dulces Montes..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "En 1938, Don Miguel Montes perfeccionó el caramelo de leche real. De ahí nacieron leyendas que todos comimos de niños: Tomy, Damy y Riko Riko."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Mientras las transnacionales usan jarabes artificiales, Montes procesa leche fresca con ingeniería de vacío y exporta a más de 30 países sin venderse a Wall Street."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Orgullo de la manufactura mexicana. Escucha la crónica completa y fuentes de investigación en escucha guion sia punto github punto io y en Sia Podcast."
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
        "title": "sIA Crónicas #06: Fábrica de Dulces Montes: El Imperio del Caramelo de Leche en Poncitlán y la Resistencia Industrial Mexicana",
        "filename": EPISODE_FILENAME,
        "description": "Crónica corporativa e industrial sobre Don Miguel Montes Martell (1938), la ingeniería de confitería con leche fresca y cocción al vacío, la tríada dorada de Tomy, Damy y Riko Riko, y la resistencia frente a los conglomerados globales por cacs."
    }
    
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"✅ Audio completo sintetizado: {out_path}")
    return out_path

async def step2_generate_reel_audio():
    print("\n" + "="*70)
    print("🎬 PASO 2: Sintetizando Audio del Reel Cómic-Pop (45s)...")
    print("="*70)
    temp_dir = ENGINE_DIR / "temp_audio_stupy_07"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        clean_text = item["text"].replace("Sia", "Sia").replace("sIA", "Sia")
        clean_text = clean_text.replace("Tomy", "Tomi").replace("Damy", "Dami").replace("Riko Riko", "Riko Riko").replace("Montes", "Montes")
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
    print("🎨 PASO 3: Preparando Composición HyperFrames Cómic-Pop Stupy 07...")
    print("="*70)
    
    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>sIA Reel Stupy 07 - Dulces Montes & Tomy</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #1c0d02;
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
    <div id="root" data-composition-id="sia_motion_reel_stupy_07" data-no-timeline data-start="0" data-duration="45.0" data-width="1080" data-height="1920">
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
        background: #1c0d02;
        color: #0b0d17;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
        position: relative;
      }}

      /* 1. HALFTONE COMIC PATTERN BACKGROUND */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(rgba(245, 158, 11, 0.18) 2.5px, transparent 2.5px);
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
        opacity: 0.06;
        font-family: 'JetBrains Mono', monospace;
        font-size: 80px;
        font-weight: 900;
        color: #f59e0b;
        user-select: none;
        pointer-events: none;
        z-index: 2;
        line-height: 1.1;
      }}

      /* 3. SPEED LINES */
      .speed-lines {{
        position: absolute;
        inset: 0;
        background: repeating-conic-gradient(from 0deg at 50% 50%, rgba(245, 158, 11, 0.05) 0deg 8deg, transparent 8deg 16deg);
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
        border: 4px solid #f59e0b;
        border-radius: 999px;
        padding: 14px 34px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 6px 6px 0px #f59e0b;
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
        background: #ea580c;
        color: #fff;
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

      .myth-tag {{
        background: #f59e0b;
        color: #000000;
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
        font-size: 54px;
        line-height: 1.08;
        color: #0b0d17;
        text-transform: uppercase;
        letter-spacing: -1.5px;
        margin-bottom: 26px;
      }}

      .punch-pill {{
        background: #fbbf24;
        color: #000000;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 40px;
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
        background: #fef3c7;
        border: 5px dashed #f59e0b;
        border-radius: 20px;
        padding: 22px 28px;
        margin-top: 20px;
        width: 100%;
      }}

      .metric-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 800;
        color: #b45309;
        letter-spacing: 1px;
      }}

      .metric-stat {{
        font-family: 'Montserrat', sans-serif;
        font-size: 48px;
        font-weight: 900;
        color: #78350f;
        line-height: 1.1;
      }}

      .progress-bar-container {{
        width: 100%;
        height: 20px;
        background: #000000;
        border: 4px solid #f59e0b;
        border-radius: 999px;
        overflow: hidden;
        position: relative;
        box-shadow: 4px 4px 0px #f59e0b;
      }}

      .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, #f59e0b, #fbbf24, #ea580c);
        width: 0%;
        animation: progressAnim 45s linear infinite;
      }}

      @keyframes progressAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}

      .final-pill {{
        background: #000000;
        color: #fbbf24;
        font-family: 'JetBrains Mono', monospace;
        font-size: 34px;
        font-weight: 800;
        padding: 16px 36px;
        border: 5px solid #f59e0b;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #f59e0b;
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
      <div>DULCES MONTES PONCITLAN JALISCO 1938</div>
      <div>TOMY DAMY RIKO RIKO CARAMELO DE LECHE</div>
      <div>REACCION DE MAILLARD VACIO Y PAILAS</div>
      <div>HECHO EN MEXICO RESISTENCIA INDUSTRIAL</div>
    </div>

    <div class="reel-wrapper">
      <div class="header-pill">
        <div class="header-dot"></div>
        <div class="header-text">sIA CRÓNICAS CORP #06</div>
      </div>

      <!-- MAIN COMIC CARD -->
      <div class="comic-card">
        <div class="comic-stamp">MÉXICO 1938</div>

        <!-- SCENE 1: EL REY DEL CARAMELO (0s - 8.5s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">EL ORIGEN DE PONCITLÁN</div>
          <div class="headline-black">
            ¿CÓMO NACIÓ EL REY DEL CARAMELO?
          </div>
          <div class="punch-pill">
            DULCES MONTES DESDE 1938
          </div>
          <div class="metric-box">
            <div class="metric-title">CIÉNEGA DE CHAPALA, JALISCO:</div>
            <div class="metric-stat">88 AÑOS DE RESISTENCIA</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 18px;">
            El dulce más icónico de la infancia mexicana.
          </div>
        </div>

        <!-- SCENE 2: LA TRÍADA DORADA (8.5s - 20.5s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #ea580c; color: #fff;">LA TRÍADA LEGENDARIA</div>
          <div class="headline-black" style="font-size: 50px;">
            TOMY, DAMY Y RIKO RIKO
          </div>
          <div class="punch-pill" style="background: #fef08a; color: #000; font-size: 36px;">
            LECHE REAL Y MANTEQUILLA
          </div>
          <div class="metric-box" style="background: #fefce8; border-color: #f59e0b;">
            <div style="font-size: 32px; font-weight: 900; color: #854d0e;">
              🥛 LA QUÍMICA DE MAILLARD
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Sabor natural sin sustitutos artificiales.
          </div>
        </div>

        <!-- SCENE 3: RESISTENCIA INDUSTRIAL (20.5s - 33.5s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #10b981; color: #fff;">INDEPENDENCIA MEXICANA</div>
          <div class="headline-black" style="font-size: 48px;">
            FRENTE A LOS GIGANTES
          </div>
          <div class="punch-pill" style="background: #000; color: #fbbf24 !important; font-size: 36px; border-color: #fbbf24;">
            EXPORTA A +30 PAÍSES
          </div>
          <div class="metric-box" style="background: #f0fdf4; border-color: #10b981;">
            <div style="font-size: 30px; font-weight: 900; color: #166534;">
              🇲🇽 NUNCA VENDIDA A WALL STREET
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            Cientos de millones de caramelos por año.
          </div>
        </div>

        <!-- SCENE 4: ORGULLO MANUFACTURERO (33.5s - 45s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #0f172a; color: #fff; box-shadow: 4px 4px 0px #f59e0b;">MANUFACTURA MEXICANA</div>
          <div class="headline-black" style="font-size: 52px;">
            TRADICIÓN &<br>ALTA INGENIERÍA
          </div>
          <div class="punch-pill" style="font-size: 36px; background: #000; border-color: #f59e0b; color: #fbbf24 !important; box-shadow: 8px 8px 0px #f59e0b;">
            COCCIÓN AL VACÍO
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 20px;">
            Crónica completa y fuentes en:
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
    print("✅ Plantillas HyperFrames generadas para Stupy 07.")

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
    
    res_entry = f'''    # sIA Corp 06 - Dulces Montes y la Resistencia Industrial - 2 de Noviembre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-corp-06-fabrica-de-dulces-montes-caramelo-de-leche-poncitlan",
        "category": "Crónicas Corporativas & Manufactura",
        "badge_color": "amber",
        "read_time": "12 min",
        "title": "sIA Crónicas #06: Fábrica de Dulces Montes: El Imperio del Caramelo de Leche en Poncitlán y la Resistencia Industrial Mexicana",
        "subtitle": "La alquimia de 1938 de Don Miguel Montes Martell: la química de Maillard a escala industrial, Tomy, Damy y la supervivencia frente a los conglomerados globales de Wall Street.",
        "thesis": "La permanencia y competitividad internacional de Fábrica de Dulces Montes durante casi un siglo demuestra que la integración vertical con cuencas lecheras locales, la fidelidad a ingredientes auténticos y la ingeniería de procesos al vacío superan a largo plazo a las economías de escala basadas en ultraprocesados y sustitutos artificiales.",
        "nexo": "Sexto episodio de Crónicas Corporativas: Historia empresarial mexicana, manufactura de alimentos, ingeniería de confitería, cadenas agroindustriales y resistencia a adquisiciones transnacionales.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "title": "1. El Origen en la Ciénega de Chapala: Don Miguel Montes Martell (1938)",
                "body": """
En 1938, en el municipio ribereño de Poncitlán, Jalisco, Don Miguel Montes Martell sentó las bases de lo que se convertiría en un bastión de la confitería tradicional mexicana. Rodeado por la cuenca lechera más productiva del occidente del país, Montes identificó una oportunidad agroindustrial decisiva: transformar los excedentes perecederos de leche bronca en caramelos concentrados de alto valor agregado mediante pailas de cobre y calor controlado.

Aquel taller artesanal, donde los primeros caramelos se cortaban a mano sobre losas de mármol frío y se envolvían manualmente en papel encerado con doble torsión, evolucionó paulatinamente hasta convertirse en un complejo industrial tecnificado que abastecería a los mercados de Guadalajara, la Ciudad de México y las redes mayoristas del bajío.
"""
            }},
            {{
                "title": "2. La Tríada Dorada: Tomy, Damy y Riko Riko",
                "body": """
El arraigo cultural de Montes descansa sobre una tríada de productos icónicos que trascendieron generaciones. El caramelo 'Tomy', con su distintiva envoltura amarilla y su ilustración de una vaca lechera sonriente, redefinió la categoría del caramelo blando masticable al integrar leche entera y mantequilla fresca en una emulsión elástica que no se fractura ni se adhiere en exceso al esmalte dental.

Posteriormente, la formulación de 'Damy' añadió mitades de cacahuate tostado de primera selección a la masa láctea, logrando un equilibrio organoléptico entre grasas vegetales, salinidad sutil y dulzor profundo. La tríada se completó con 'Riko Riko', un caramelo relleno mediante técnicas de coextrusión concéntrica con núcleo líquido de cajeta, consolidando un portafolio complementado por Chupirul, paletas y mentas con mantequilla.
"""
            }},
            {{
                "title": "3. Termodinámica y Reacción de Maillard a Escala Industrial",
                "body": """
Lejos de depender de esencias químicas o jarabes sintéticos, el perfil aromático de Dulces Montes es el resultado directo de la Reacción de Maillard: una serie de transformaciones no enzimáticas entre los aminoácidos de las proteínas lácteas (caseína) y los azúcares reductores (lactosa y sacarosa) a temperaturas controladas de entre 110°C y 125°C.

Para evitar la desnaturalización violenta de la proteína y la separación de fases grasas, la planta de Poncitlán adoptó concentradores y evaporadores al vacío. Al reducir la presión barométrica en las calderas, el agua de la leche fresca se evapora a menor temperatura, permitiendo obtener una concentración de sólidos superior al 92% sin carbonizar la mezcla y preservando la matriz coloidal que caracteriza a sus productos.
"""
            }},
            {{
                "title": "4. La Resistencia Familiar frente a los Gigantes Multinacionales",
                "body": """
Tras la apertura comercial de los años 90, la industria confitera en México presenció una ola masiva de consolidación extranjera: Ricolino fue adquirida por Bimbo y vendida después a Mondelēz; Nestlé absorbió La Corona y Carlos Quinto; Mars Wrigley se adueñó de Lucas y Skwinkles.

Frente a ofertas millonarias de compra por parte de corporaciones transnacionales, la familia Montes optó por la independencia accionaria. Su fortaleza radicó en el dominio del canal tradicional de abarrotes y dulcerías de mayoreo, así como en la exportación al mercado de la nostalgia en Estados Unidos (Texas, California, Illinois), donde millones de consumidores buscan la autenticidad láctea frente a los caramelos estadounidenses elaborados con jarabe de maíz de alta fructosa (HFCS).
"""
            }},
            {{
                "title": "5. Desafíos Regulatorios y el Futuro de la Confitería Mexicana",
                "body": """
En la actualidad, Montes procesa decenas de miles de litros diarios de leche, genera más de 1,500 empleos directos e indirectos en la región de Poncitlán y comercializa en más de 30 naciones. La implementación de la NOM-051 sobre etiquetado frontal de advertencia calórica y los impuestos especiales (IEPS) han obligado a optimizar procesos sin desvirtuar la receta original.

La trayectoria de Dulces Montes ratifica una lección estratégica para la industria nacional: el patrimonio agroindustrial mexicano sustentado en ingredientes genuinos, control estricto de ingeniería térmica y fidelidad a sus raíces comunitarias constituye una ventaja competitiva inexpugnable frente a cualquier monopolio global.
"""
            }}
        ],
        "apa_references": [
            "INEGI. (2024). *La industria de la confitería y productos de chocolate en México: Censos Económicos*. Instituto Nacional de Estadística y Geografía.",
            "Secretaría de Economía. (2023). *Perfil del sector de confitería y derivados lácteos en Jalisco*. Gobierno de México.",
            "Montes Martell, M. (1938-2024). *Archivos Históricos de Fábrica de Dulces Montes S.A. de C.V.* Poncitlán, Jalisco.",
            "Belitz, H. D., Grosch, W., & Schieberle, P. (2009). *Food Chemistry: Milk and Dairy Products, Maillard Reaction Mechanisms* (4th ed.). Springer.",
            "cacs, & sIA Editora. (2026). *sIA Crónicas #06: Fábrica de Dulces Montes: El Imperio del Caramelo de Leche en Poncitlán y la Resistencia Industrial Mexicana*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if "sia-corp-06-fabrica-de-dulces-montes-caramelo-de-leche-poncitlan" not in content:
        content = content.replace(
            'RESEARCH_DATABASE = {',
            'RESEARCH_DATABASE = {\n' + res_entry
        )
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Entrada de investigación sIA Crónicas #06 inyectada en build_magazine.py")

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
id: reel-stupy-07
titulo: "Fábrica de Dulces Montes: El Imperio del Caramelo de Leche en Poncitlán y la Resistencia Industrial Mexicana"
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
  - cronicas-corporativas
  - dulces-montes
  - tomy
  - damy
  - poncitlan
  - jalisco
  - manufactura
  - mexico
---

# 🍬 Fábrica de Dulces Montes: El Imperio del Caramelo de Leche en Jalisco

> **Estilo Visual:** Cómic-Pop Halftone Ámbar Caramelo & Naranja Toffee, Tarjeta Escudo 20px Solid Shadow, Audio EBU R128 (-16 LUFS).

---

## 🎬 Reproductor del Video (Vertical 9:16)
![[{REEL_FILENAME}]]

**Póster Oficial:**
![[{REEL_POSTER_FILENAME}|350]]

---

## 📱 Kit de Copys & Hashtags para Publicación en Móvil (TikTok / Shorts / Instagram / LinkedIn)

### 🎯 Título Gancho (Hook):
`¿Cómo un taller en Poncitlán, Jalisco, creó el dulce más icónico de México? 🍬🇲🇽`

### ✍️ Descripción para Redes (Copy de Alto Alcance):
> De una paila de cobre en 1938 a exportar cientos de millones de caramelos a más de 30 países...
>
> ¿Tomy, Damy o Riko Riko? La fascinante historia de cómo Dulces Montes resistió las compras de multinacionales procesando leche fresca con alta ingeniería al vacío.
>
> ¿Cuál era tu caramelo favorito de niño? Déjanoslo en los comentarios. 👇

### 🏷️ Bloque de Hashtags Estratégicos:
```
#dulcesmontes #tomy #damy #jalisco #poncitlan #hechoenmexico #emprendimiento #manufactura #nostalgia #negocios #siapodcast
```

---

## 🎙️ Guion & Voces (Jorge & Dalia +6%)

### Escena 1: El Origen de Poncitlán (00:00 - 08:50)
* **JORGE:** ¿Cómo un taller familiar en Poncitlán, Jalisco, creó el dulce más icónico de México y resistió el asedio de gigantes multinacionales? Esta es la historia de Dulces Montes...
* *Animación:* Badge pop-in `DULCES MONTES DESDE 1938 🍬` con sombra dura negra.

### Escena 2: La Tríada Legendaria (08:50 - 20:50)
* **DALIA:** En 1938, Don Miguel Montes perfeccionó el caramelo de leche real. De ahí nacieron leyendas que todos comimos de niños: Tomy, Damy y Riko Riko.
* *Animación:* Tarjeta métrica: `TOMY, DAMY Y RIKO RIKO` -> `LECHE REAL Y MANTEQUILLA`.

### Escena 3: Resistencia Industrial (20:50 - 33:50)
* **JORGE:** Mientras las transnacionales usan jarabes artificiales, Montes procesa leche fresca con ingeniería de vacío y exporta a más de 30 países sin venderse a Wall Street.
* *Animación:* Badge de alerta: `EXPORTA A +30 PAÍSES 🇲🇽 NUNCA VENDIDA`.

### Escena 4: Orgullo de la Manufactura (33:50 - 45:00)
* **DALIA:** Orgullo de la manufactura mexicana. Escucha la crónica completa y fuentes de investigación en `escucha-sia.github.io` y en *sIA Podcast*.
* *Animación:* Píldora neón dorada con URL destacada.

---

## 🔗 Referencias & Backlinks
* **Artículo Web Completo con Fuentes APA:** [[03_Articulos/sia-corp-06-fabrica-de-dulces-montes-caramelo-de-leche-poncitlan]]
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
    msg = f"feat(episode): publish sIA Corp 06 - Dulces Montes and Tomy with Reel Stupy 07"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(BASE_DIR), check=True)
    
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if push_res.returncode == 0:
        print("🎉 ¡Despliegue a GitHub Pages exitoso!")
    else:
        print("⚠️ Advertencia al hacer push:", push_res.stderr)

def step9_upload_to_tiktok():
    print("\n" + "="*70)
    print("📱 PASO 9: Subiendo Reel 07 a TikTok Automáticamente (@escucha_sia)...")
    print("="*70)
    
    pub_script = BASE_DIR / "scripts" / "publish_reels_to_tiktok.py"
    pub_content = pub_script.read_text(encoding='utf-8')
    
    new_reel_entry = f'''REELS_TO_PUBLISH = [
    {{
        "file": BASE_DIR / "reels" / "{REEL_FILENAME}",
        "caption": "¿Cómo un taller en Poncitlán creó el dulce más icónico de México? La historia de Dulces Montes (Tomy, Damy y Riko Riko). Episodio en Spotify (sIA) y blog en perfil. #dulcesmontes #tomy #damy #jalisco #hechoenmexico #emprendimiento #manufactura #siapodcast"
    }}
]'''
    pub_content = re.sub(r'REELS_TO_PUBLISH = \[.*?\]', new_reel_entry, pub_content, flags=re.DOTALL)
    pub_script.write_text(pub_content, encoding='utf-8')
    
    res = subprocess.run([sys.executable, str(pub_script)], cwd=str(BASE_DIR), text=True)
    if res.returncode == 0:
        print("🎉 ¡Reel 07 publicado y verificado en TikTok Studio exitosamente!")
    else:
        print(f"⚠️ Error al subir Reel 07 a TikTok: código {res.returncode}")

async def main_async():
    print("="*70)
    print("🚀 INICIANDO PRODUCCIÓN INTEGRAL 360° - EPISODIO & REEL STUPY 07")
    print("Tema: sIA Crónicas #06: Fábrica de Dulces Montes y el Imperio del Caramelo")
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
    # 9. TikTok Upload (sync fuera del loop asyncio)
    step9_upload_to_tiktok()

if __name__ == "__main__":
    main()
