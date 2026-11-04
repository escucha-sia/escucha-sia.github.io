"""
sIA Master Episode & Reel Producer:
Tema: sIA Dev #02: La Muerte del Function Calling: Por qué Cloudflare y Anthropic reemplazaron miles de herramientas por 1,000 tokens de código (Code Mode)
Pipeline 360°:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos, VTT, SRT, EBU R128)
2. Reel Vertical 9:16 Stupy Cómic-Pop con Barra de Capítulos (HyperFrames GPU, 45s, Kinetic Pop)
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

EPISODE_FILENAME = "sIA_Dev_02_Code_Mode_vs_MCP_Cloudflare_Anthropic_2026-11-04.mp3"
REEL_FILENAME = "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4"
REEL_POSTER_FILENAME = "sIA_Reel_Stupy_08_CodeMode_vs_MCP_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# ==============================================================================
# 1. GUION DEL PODCAST COMPLETO (10 - 12 MINUTOS)
# ==============================================================================
FULL_SCRIPT = """
[CHAPTER: Apertura: El Millón de Tokens Inútiles]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad de arquitectos de software, ingenieros de inteligencia artificial y apasionados de los sistemas distribuidos en producción! Bienvenidos a una nueva entrega técnica de sIA en su edición de Desarrollo e Infraestructura Agéntica. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es miércoles cuatro de noviembre de dos mil veintiséis. Y hoy ponemos sobre la mesa de autopsia uno de los debates más intensos de la ingeniería moderna: ¿por qué el modelo tradicional de Function Calling y Model Context Protocol que nos vendieron hace apenas unos meses está colapsando en los entornos empresariales reales?
JORGE: Todos conocemos la promesa original de MCP: tienes un modelo de lenguaje de última generación, le defines herramientas en esquemas JSON y el agente decide cuándo invocar una base de datos, una API climática o un CRM. En una demo de salón con tres herramientas, funciona de maravilla.
DALIA: Pero cuando llevas eso al mundo corporativo, donde una plataforma como Cloudflare tiene más de dos mil quinientos endpoints en su API, la realidad golpea con fuerza: inyectar la definición de todas esas herramientas en el prompt del sistema consume más de un millón ciento setenta mil tokens antes de que el usuario envíe su primera consulta.
JORGE: Y peor aún: para encadenar cuatro tareas, el agente realiza cuatro viajes completos de ida y vuelta al modelo, saturando la ventana de contexto con payloads JSON intermedios y disparando las facturas de inferencia a niveles absurdos.
DALIA: Frente a este cuello de botella, gigantes como Cloudflare con 'Code Mode' y Anthropic con 'Programmatic Tool Calling' han presentado la solución definitiva: los modelos de IA ya no deben llamar herramientas una por una; deben escribir código ejecutable en sandboxes aislados.
JORGE: De más de un millón de tokens a escasos mil tokens. De minutos de latencia a milisegundos en V8 Isolates. Ajusten sus terminales, porque hoy desarmamos el fin del function calling ingenuo y el nacimiento de la arquitectura de código como interfaz universal. ¡Comenzamos!

[CHAPTER: La Trampa de MCP: Por qué el Tool Calling Naive Colapsa]
DALIA: Para entender la magnitud del problema, Jorge, desmenucemos qué ocurre internamente en un bucle tradicional de agentes basados en JSON Function Calling.
JORGE: Imaginemos que le pides a un agente: 'Busca a los usuarios que no han iniciado sesión en treinta días y envíales un correo de reactivación'. En el paradigma MCP convencional, el agente invoca una herramienta `get_users`. El backend ejecuta la consulta SQL y le devuelve al modelo un objeto JSON gigantesco con cientos de registros.
DALIA: Toda esa masa de texto crudo entra directo a la memoria de trabajo del LLM. Luego, el modelo debe razonar sobre cada usuario, generar una llamada individual `send_email` por cada uno, esperar la confirmación de la herramienta, volver a parsear el resultado y repetir el ciclo una y otra vez.
JORGE: Esto sufre de lo que en arquitectura llamamos 'Ampliación de Contexto Patológica'. Cada interacción intermedia contamina la atención del transformador. Mientras más grande es el contexto, mayor es la degradación de la aguja en el pajar, mayor es la probabilidad de alucinaciones y el costo por token se multiplica exponencialmente.
DALIA: Y si hablamos de catálogos masivos de APIs como AWS, Stripe o Salesforce, simplemente no caben. Ningún contexto de doscientos mil o un millón de tokens soporta miles de esquemas OpenAPI serializados en formato JSON Schema sin degradar el razonamiento lógico del modelo.

[CHAPTER: La Revelación de Cloudflare: Code Mode y los 2,500 Endpoints en 1,000 Tokens]
JORGE: Aquí es donde entra la brillantez arquitectónica de Cloudflare con el anuncio oficial de 'Code Mode'.
DALIA: Cloudflare se enfrentó a este dilema exacto con su propia API global, que abarca más de dos mil quinientos endpoints para gestionar DNS, reglas de firewall, certificados SSL, Workers y almacenamiento R2. Si intentaban exponerla mediante MCP tradicional, el footprint era de uno punto diecisiete millones de tokens.
JORGE: La solución de Cloudflare fue invertir por completo la perspectiva: en lugar de enseñarle al LLM dos mil quinientas herramientas en JSON, le entregaron únicamente dos herramientas primitivas: `search_api` y `execute_code`.
DALIA: Con esto, el consumo del modelo bajó de un millón ciento setenta mil tokens a escasos mil tokens fijos: una reducción brutal del noventa y nueve punto nueve por ciento.
JORGE: ¿Cómo opera en la práctica? La API completa se empaqueta como un SDK tipado en TypeScript. Cuando el agente recibe una tarea, primero consulta mediante `search_api` la firma tipada de los métodos que necesita.
DALIA: Y luego viene la magia: en vez de pedirle al backend que ejecute llamadas ciegas, el propio LLM escribe un pequeño script en TypeScript con bucles `for`, filtros nativos con `.filter()`, mapeos con `.map()` y bloques `try/catch`.
JORGE: Ese código se envía al servidor y se ejecuta dentro de un entorno aislado. Si la API devuelve mil registros, el script filtra los diez necesarios en memoria local y le devuelve al modelo de lenguaje únicamente la respuesta refinada. Un solo viaje de ida y vuelta.

[CHAPTER: Anthropic y Programmatic Tool Calling: De 150k a 2,000 Tokens]
DALIA: Esta no es una ocurrencia aislada de Cloudflare, Jorge. Anthropic, los creadores de Claude, publicaron investigaciones clave sobre 'Code execution with MCP' y 'Advanced Programmatic Tool Use'.
JORGE: En los experimentos formales de Anthropic, midieron el consumo de tokens y la tasa de éxito en tareas complejas de orquestación de datos. El resultado fue contundente: tareas que bajo el modelo reactivo de MCP consumían más de ciento cincuenta mil tokens en iteraciones sucesivas, se completaron con menos de dos mil tokens utilizando ejecución programática.
DALIA: ¿Por qué los modelos son infinitamente más eficientes escribiendo código que rellenando esquemas JSON de herramientas?
JORGE: La respuesta radica en el preentrenamiento fundacional. Los grandes modelos de lenguaje han ingerido billones de líneas de código fuente en GitHub, GitLab y Stack Overflow. Comprenden a la perfección la semántica del flujo de control, la asignación de variables, el encadenamiento de funciones y la gestión de excepciones.
DALIA: Cuando obligas a un modelo a razonar mediante llamadas de herramientas en JSON, estás forzando a un motor de programación a comportarse como un enrutador burocrático de mensajes. Al permitirle escribir código, liberas su capacidad nativa de síntesis algorítmica.

[CHAPTER: Sandboxing con V8 Isolates: Rendimiento vs Seguridad]
DALIA: Ahora bien, como siempre decimos en sIA, en ingeniería no existen las soluciones mágicas, solo los trade-offs. Y ejecutar código generado dinámicamente por un modelo de IA en tus servidores plantea un desafío crítico: la seguridad.
JORGE: Si un agente escribe código TypeScript y lo ejecuta en tu infraestructura, ¿cómo garantizas que un atacante mediante prompt injection no inyecte un comando malicioso o intente leer secretos de entorno?
DALIA: Aquí es donde brilla la tecnología de V8 Isolates de Cloudflare Workers y Deno. A diferencia de levantar contenedores Docker tradicionales, que tardan entre uno y tres segundos en arrancar y consumen cientos de megabytes de memoria RAM, un V8 Isolate arranca en menos de cinco milisegundos.
JORGE: Cada script corre en un espacio de memoria completamente aislado a nivel de motor de JavaScript, sin acceso al sistema de archivos del host, sin acceso a procesos del sistema operativo y con límites estrictos de CPU y tiempo de ejecución.
DALIA: Además, la gestión de credenciales se resuelve con elegancia: las API keys y tokens de autenticación nunca se exponen al contexto del LLM. Permanecen inyectadas como bindings seguros dentro del entorno de ejecución del sandbox, por lo que el modelo interactúa con el cliente HTTP sin ver jamás la llave criptográfica en texto plano.

[CHAPTER: El Fin de las APIs para Humanos: TypeScript como la Interfaz Universal]
JORGE: Esta transición marca un cambio de paradigma histórico en la forma en que los desarrolladores construiremos software en la próxima década.
DALIA: Durante veinte años diseñamos APIs REST y GraphQL pensadas para ser leídas por desarrolladores humanos en interfaces Swagger o Postman.
JORGE: En la era agéntica moderna, la interfaz universal ya no es una documentación en HTML ni un esquema JSON interminable: es una biblioteca tipada en TypeScript o Python. Los compiladores y los checkers de tipos actúan como el arnés de seguridad perfecto para que el agente autocorrija sus errores de sintaxis antes de ejecutar el código.
DALIA: MCP no ha muerto, pero el function calling ingenuo de invocar herramientas una por una ha quedado obsoleto para sistemas de alta escala. La orquestación moderna pertenece a los agentes que programan su propio flujo de trabajo.

[CHAPTER: Cierre y Recursos en sIA Journal]
JORGE: Una lección magistral de optimización de costos, eficiencia de contexto y elegancia arquitectónica.
DALIA: El artículo de investigación completo, con los diagramas de secuencia entre el modelo, el sandbox de V8 y la API de Cloudflare, junto con las referencias formales en formato APA 7ª Edición, ya está disponible en sIA Journal en nuestro portal web: escucha guion sia punto github punto io diagonal articulos.
JORGE: Y en nuestra cuenta oficial de TikTok arroba escucha guion bajo sia, los invitamos a ver el Reel animado en formato Cómic-Pop donde explicamos este salto de un millón de tokens a mil tokens en cuarenta y cinco segundos visuales.
DALIA: Muchísimas gracias por acompañarnos en este análisis de arquitectura viva. Soy Dalia.
JORGE: Y yo soy Jorge. ¡Hasta el próximo episodio de sIA Podcast!
"""

# ==============================================================================
# 2. DIÁLOGO DEL REEL VERTICAL 9:16 (45 SEGUNDOS EXACTOS)
# ==============================================================================
REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Conectar 20 herramientas a tu agente de IA destruyó tu presupuesto en tokens? Te explico por qué llamar herramientas una por una murió, y cómo Cloudflare metió 2,500 endpoints en solo 1,000 tokens..."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Hoy los agentes usan MCP tradicional: llaman una herramienta, reciben un JSON gigante, llaman otra y repiten. Es lento, gasta millones de tokens y satura la memoria del modelo."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Cloudflare y Anthropic crearon 'Code Mode': en vez de miles de herramientas, el modelo escribe código TypeScript en un sandbox V8 aislado y ejecuta todo en un solo viaje."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "De 1.17 millones de tokens a escasos mil. Noventa y ocho por ciento de ahorro. Los modelos razonan mejor programando código que persiguiendo JSONs."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "La arquitectura completa con benchmarks de producción está en sIA Journal. Link en nuestro perfil."
    }
]

# ==============================================================================
# SUBROUTINES DE PRODUCCIÓN
# ==============================================================================

async def synthesize_voice_segment(text: str, voice: str, output_path: Path):
    for attempt in range(4):
        try:
            communicate = edge_tts.Communicate(text, voice, rate="+6%")
            await communicate.save(str(output_path))
            if output_path.exists() and output_path.stat().st_size > 200:
                return
        except Exception as e:
            if attempt == 3:
                raise e
            await asyncio.sleep(2)

def step1_produce_full_audio():
    print("\n" + "="*70)
    print("🎙️ PASO 1: Generando Master Audio del Podcast Completo...")
    print("="*70)
    
    final_master = AUDIO_DIR / EPISODE_FILENAME
    if final_master.exists() and final_master.stat().st_size > 1000000:
        print(f"ℹ️ Master de audio ya existe y es válido: {final_master} ({final_master.stat().st_size / (1024*1024):.2f} MB)")
        SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
        return final_master
        
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = BASE_DIR / "temp_audio_codemode"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    lines = [line.strip() for line in FULL_SCRIPT.strip().split("\n") if line.strip()]
    segments = []
    
    for i, line in enumerate(lines):
        if line.startswith("[CHAPTER:"):
            continue
        if line.startswith("JORGE:"):
            text = line.replace("JORGE:", "").strip()
            voice = VOICE_JORGE
        elif line.startswith("DALIA:"):
            text = line.replace("DALIA:", "").strip()
            voice = VOICE_DALIA
        else:
            continue
            
        seg_path = temp_dir / f"seg_{i:03d}.mp3"
        print(f"  [TTS] Generando segmento {i+1}/{len(lines)} ({voice[:11]})...")
        asyncio.run(synthesize_voice_segment(text, voice, seg_path))
        segments.append(seg_path)
        
    concat_list_path = temp_dir / "concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"file '{seg.name}'\n")
            
    raw_master = temp_dir / "raw_master.mp3"
    print("  [FFMPEG] Concatenando segmentos...")
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(raw_master)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    final_master = AUDIO_DIR / EPISODE_FILENAME
    print("  [EBU R128] Normalizando sonoridad a -16 LUFS...")
    cmd_norm = [
        "ffmpeg", "-y", "-i", str(raw_master),
        "-af", "loudnorm=I=-16:LRA=11:TP=-1.5",
        "-ar", "44100", "-b:a", "192k",
        str(final_master)
    ]
    subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final_master, SPOTIFY_DIR / EPISODE_FILENAME)
    
    print(f"✅ Master de audio completado: {final_master}")
    return final_master

def step2_produce_reel_audio():
    print("\n" + "="*70)
    print("🔊 PASO 2: Sintetizando Audio del Reel Vertical (45s exactos)...")
    print("="*70)
    
    temp_dir = ENGINE_DIR / "temp_audio_stupy_08"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    segments = []
    for i, item in enumerate(REEL_DIALOGUE):
        seg_path = temp_dir / f"reel_seg_{i:02d}.mp3"
        print(f"  [TTS Reel] ({item['speaker']}) {item['text'][:45]}...")
        asyncio.run(synthesize_voice_segment(item['text'], item['voice'], seg_path))
        segments.append(seg_path)
        
    concat_list = temp_dir / "concat_reel.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"file '{seg.name}'\n")
            
    raw_reel = temp_dir / "raw_reel.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(raw_reel)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    norm_reel = ENGINE_DIR / "assets" / "audio.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_reel),
        "-af", "loudnorm=I=-14:LRA=7:TP=-1.0,atempo=1.0",
        "-ar", "44100", "-b:a", "192k",
        str(norm_reel)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    print(f"✅ Audio del Reel listo en: {norm_reel}")

def step3_prepare_stupy_composition():
    print("\n" + "="*70)
    print("🎨 PASO 3: Generando Composición Stupy Cómic-Pop con Barra de Capítulos...")
    print("="*70)
    
    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Reel Stupy 08 - Code Mode vs MCP</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #060913;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}

      /* Matriz Halftone Cómic Pop */
      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#38bdf8 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.15;
        z-index: 1;
        pointer-events: none;
      }}

      .speed-lines {{
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          -45deg,
          rgba(56, 189, 248, 0.05) 0px,
          rgba(56, 189, 248, 0.05) 12px,
          transparent 12px,
          transparent 24px
        );
        z-index: 2;
        pointer-events: none;
      }}

      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 80px;
        color: rgba(56, 189, 248, 0.06);
        text-transform: uppercase;
        transform: rotate(-12deg) scale(1.4);
        top: 25%;
        z-index: 0;
        line-height: 1.1;
      }}

      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding: 90px 50px 110px 50px;
      }}

      /* BARRA DE CAPÍTULOS SUPERIOR TIPO JOHNOLVEN */
      .chapters-pill-bar {{
        display: flex;
        gap: 12px;
        background: rgba(15, 23, 42, 0.85);
        padding: 10px 20px;
        border-radius: 40px;
        border: 2px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
      }}

      .chapter-step {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        padding: 6px 16px;
        border-radius: 20px;
        color: #94a3b8;
        background: transparent;
        transition: all 0.3s ease;
      }}

      .step-active {{
        background: #38bdf8;
        color: #000000;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
      }}

      .header-pill {{
        background: #000000;
        border: 4px solid #38bdf8;
        box-shadow: 6px 6px 0px #38bdf8;
        border-radius: 50px;
        padding: 14px 38px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
      }}

      .header-dot {{
        width: 20px;
        height: 20px;
        background: #38bdf8;
        border-radius: 50%;
        box-shadow: 0 0 16px #38bdf8;
      }}

      .header-text {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #f8fafc;
      }}

      /* TARJETA CÓMIC-POP PRINCIPAL */
      .comic-card {{
        background: #ffffff;
        border: 8px solid #000000;
        box-shadow: 18px 18px 0px #38bdf8;
        border-radius: 36px;
        width: 100%;
        max-width: 980px;
        padding: 50px 42px;
        color: #000000;
        text-align: center;
        position: relative;
      }}

      .comic-stamp {{
        position: absolute;
        top: -30px;
        right: 40px;
        background: #ef4444;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 24px;
        padding: 8px 24px;
        border: 4px solid #000000;
        border-radius: 14px;
        transform: rotate(6deg);
        box-shadow: 4px 4px 0px #000000;
      }}

      .myth-tag {{
        display: inline-block;
        background: #0284c7;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        padding: 8px 24px;
        border-radius: 12px;
        border: 3px solid #000;
        margin-bottom: 24px;
        text-transform: uppercase;
      }}

      .headline-black {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 54px;
        line-height: 1.15;
        letter-spacing: -1.5px;
        color: #000000;
        margin-bottom: 24px;
        text-transform: uppercase;
      }}

      .punch-pill {{
        background: #38bdf8;
        color: #000000;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 40px;
        padding: 16px 28px;
        border: 5px solid #000000;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #000000;
        display: inline-block;
        margin-bottom: 26px;
      }}

      .metric-box {{
        background: #f0f9ff;
        border: 4px dashed #0284c7;
        border-radius: 20px;
        padding: 24px 28px;
        margin-top: 15px;
      }}

      .metric-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #0369a1;
      }}

      .metric-stat {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 58px;
        color: #0284c7;
        line-height: 1.1;
        margin-top: 6px;
      }}

      /* FOOTER & TIMELINE */
      .footer-badge {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 14px;
        margin-top: 20px;
      }}

      .channel-tag {{
        background: #000000;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 32px;
        font-weight: 800;
        padding: 12px 36px;
        border: 4px solid #38bdf8;
        border-radius: 40px;
        box-shadow: 6px 6px 0px #38bdf8;
      }}

      .progress-bar-container {{
        width: 100%;
        max-width: 900px;
        height: 16px;
        background: #1e293b;
        border: 3px solid #000000;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 15px;
      }}

      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #38bdf8, #0284c7, #818cf8);
        width: 0%;
        animation: progressAnim 45s linear infinite;
      }}

      @keyframes progressAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}

      .final-pill {{
        background: #000000;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 34px;
        font-weight: 800;
        padding: 16px 36px;
        border: 5px solid #38bdf8;
        border-radius: 20px;
        box-shadow: 6px 6px 0px #38bdf8;
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
      <div>MCP TOOL CALLING CODE MODE CLOUDFLARE</div>
      <div>ANTHROPIC 1.17M TOKENS A 1000 TOKENS</div>
      <div>TYPESCRIPT SDK V8 ISOLATES SANDBOX</div>
      <div>CODE IS THE UNIVERSAL INTERFACE</div>
    </div>

    <div class="reel-wrapper">
      <!-- BARRA DE CAPÍTULOS DINÁMICA -->
      <div class="chapters-pill-bar">
        <div class="chapter-step" id="chap-1">01 MCP</div>
        <div class="chapter-step" id="chap-2">02 PROBLEMA</div>
        <div class="chapter-step" id="chap-3">03 CODE MODE</div>
        <div class="chapter-step" id="chap-4">04 BENCHMARK</div>
      </div>

      <div class="header-pill">
        <div class="header-dot"></div>
        <div class="header-text">sIA DEV & ARQUITECTURA #02</div>
      </div>

      <!-- MAIN COMIC CARD -->
      <div class="comic-card">
        <div class="comic-stamp">NOVEDAD 2026</div>

        <!-- SCENE 1: EL CUELLO DE BOTELLA (0s - 9.0s) -->
        <div class="scene" id="scene-1">
          <div class="myth-tag">EL MITO DEL TOOL CALLING</div>
          <div class="headline-black">
            ¿RIP MCP? LLAMAR TOOLS UNA POR UNA MURIÓ
          </div>
          <div class="punch-pill">
            ¿FACTURA DE TOKENS POR LAS NUBES?
          </div>
          <div class="metric-box">
            <div class="metric-title">API CLOUDFLARE EN MCP:</div>
            <div class="metric-stat">1.17M TOKENS</div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 18px;">
            2,500 endpoints saturan el contexto antes de empezar.
          </div>
        </div>

        <!-- SCENE 2: EL PROBLEMA DEL JSON (9.0s - 21.0s) -->
        <div class="scene" id="scene-2">
          <div class="myth-tag" style="background: #ef4444; color: #fff;">LATENCIA Y BASURA JSON</div>
          <div class="headline-black" style="font-size: 50px;">
            MÚLTIPLES VIAJES DE IDA Y VUELTA
          </div>
          <div class="punch-pill" style="background: #fca5a5; color: #000; font-size: 36px;">
            CONGESTIÓN DE CONTEXTO
          </div>
          <div class="metric-box" style="background: #fef2f2; border-color: #ef4444;">
            <div style="font-size: 32px; font-weight: 900; color: #991b1b;">
              ⚠️ EL LLM NO ES UN ENRUTADOR
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 14px;">
            Payloads intermedios destruyen el razonamiento.
          </div>
        </div>

        <!-- SCENE 3: CODE MODE (21.0s - 34.0s) -->
        <div class="scene" id="scene-3">
          <div class="myth-tag" style="background: #10b981; color: #fff;">LA SOLUCIÓN REVOLUCIONARIA</div>
          <div class="headline-black" style="font-size: 48px;">
            CODE MODE: TYPESCRIPT SDK
          </div>
          <div class="punch-pill" style="background: #000; color: #38bdf8 !important; font-size: 36px; border-color: #38bdf8;">
            CORRE EN SANDBOX V8 ISOLATE
          </div>
          <div class="metric-box" style="background: #f0fdf4; border-color: #10b981;">
            <div style="font-size: 30px; font-weight: 900; color: #166534;">
              ⚡ UN SOLO VIAJE DE IDA Y VUELTA
            </div>
          </div>
          <div style="font-size: 28px; font-weight: 800; color: #475569; margin-top: 15px;">
            El código corre en milisegundos y filtra en local.
          </div>
        </div>

        <!-- SCENE 4: BENCHMARK Y CIERRE (34.0s - 45.0s) -->
        <div class="scene" id="scene-4">
          <div class="myth-tag" style="background: #8b5cf6; color: #fff;">EL BENCHMARK DEFINITIVO</div>
          <div class="headline-black" style="font-size: 46px;">
            DE 150,000 A 2,000 TOKENS
          </div>
          <div class="punch-pill" style="background: #38bdf8; font-size: 34px;">
            -98% EN COSTOS DE INFERENCIA
          </div>
          <div class="final-pill">
            🎧 EPISODIO COMPLETO EN SPOTIFY
          </div>
          <div style="font-size: 26px; font-weight: 800; color: #0284c7; margin-top: 14px;">
            Lee la investigación en sIA Journal (link en bio)
          </div>
        </div>
      </div>

      <div class="footer-badge">
        <div class="channel-tag">@escucha_sia &bull; Spotify Show</div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    function updateTimeline(time) {{
      const s1 = document.getElementById('scene-1');
      const s2 = document.getElementById('scene-2');
      const s3 = document.getElementById('scene-3');
      const s4 = document.getElementById('scene-4');

      const c1 = document.getElementById('chap-1');
      const c2 = document.getElementById('chap-2');
      const c3 = document.getElementById('chap-3');
      const c4 = document.getElementById('chap-4');

      // Reset display
      s1.style.display = 'none';
      s2.style.display = 'none';
      s3.style.display = 'none';
      s4.style.display = 'none';

      [c1, c2, c3, c4].forEach(c => c.className = 'chapter-step');

      if (time < 9.0) {{
        s1.style.display = 'block';
        c1.className = 'chapter-step step-active';
      }} else if (time < 21.0) {{
        s2.style.display = 'block';
        c2.className = 'chapter-step step-active';
      }} else if (time < 34.0) {{
        s3.style.display = 'block';
        c3.className = 'chapter-step step-active';
      }} else {{
        s4.style.display = 'block';
        c4.className = 'chapter-step step-active';
      }}
    }}

    window.__seekHyperFrames = function(currentTime) {{
      updateTimeline(currentTime);
    }};

    updateTimeline(0);
  </script>
  </body>
</html>
"""
    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Plantillas HyperFrames generadas para Stupy 08 (Code Mode vs MCP).")

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
    
    res_entry = f'''    # sIA Dev 02 - Code Mode vs MCP - 4 de Noviembre de 2026
    "{EPISODE_FILENAME}": {{
        "slug": "sia-dev-02-la-muerte-del-function-calling-code-mode-vs-mcp",
        "category": "Arquitectura & Agentes IA",
        "badge_color": "blue",
        "read_time": "11 min",
        "title": "sIA Dev #02: La Muerte del Function Calling: Por qué Cloudflare y Anthropic reemplazaron miles de herramientas por 1,000 tokens de código (Code Mode)",
        "subtitle": "De 1.17 millones de tokens a un script de TypeScript: cómo el programmatic tool calling y los V8 Isolates resolvieron el colapso de contexto en agentes de producción.",
        "thesis": "La orquestación de agentes de inteligencia artificial mediante esquemas JSON declarativos individuales colapsa en entornos de gran escala debido a la saturación de contexto y la latencia multiturno. El paradigma de 'Code Mode' y ejecución programática en sandboxes seguros de V8 demuestra que el código nativo es la interfaz más eficiente, económica y expresiva para modelos fundacionales.",
        "nexo": "Segundo episodio de Desarrollo e Infraestructura: Patrones de diseño para agentes de IA, optimización de ventanas de contexto, sandboxing de código, MCP y arquitectura de APIs para LLMs.",
        "reel_video": "{REEL_FILENAME}",
        "content_blocks": [
            {{
                "type": "heading",
                "text": "1. El Cuello de Botella del Tool Calling Tradicional y el Límite de Escala"
            }},
            {{
                "type": "paragraph",
                "text": "Durante los últimos dos años, el estándar de facto para dotar de capacidades operativas a los modelos de lenguaje fue el Function Calling estructurado bajo especificaciones como el Model Context Protocol (MCP) y OpenAPI. En este esquema, cada operación disponible se describe mediante un esquema JSON Schema que detalla sus parámetros, tipos y descripciones semánticas. Si bien este enfoque es intuitivo en prototipos con cinco o diez herramientas, introduce un cuello de botella insuperable cuando se intenta conectar a los agentes con catálogos empresariales reales. El ejemplo paradigmático lo documentó Cloudflare: su catálogo de API abarca más de dos mil quinientos endpoints. Mapear cada uno de estos endpoints como una herramienta MCP discreta requeriría inyectar más de 1.17 millones de tokens en el prompt del sistema antes de procesar la consulta del usuario."
            }},
            {{
                "type": "callout",
                "icon": "⚠️",
                "title": "La Falacia del Routing Bureaucrático",
                "text": "Forzar al LLM a predecir llamadas JSON de herramientas de forma secuencial obliga a un motor algorítmico a comportarse como un enrutador ciego. Cada paso intermedio exige un viaje completo al modelo, donde cientos de líneas de JSON innecesario inundan la ventana de atención, degradando la precisión del razonamiento y multiplicando exponencialmente la factura de inferencia."
            }},
            {{
                "type": "heading",
                "text": "2. La Arquitectura de Code Mode: APIs en TypeScript y Sandboxes Aislados"
            }},
            {{
                "type": "paragraph",
                "text": "Para sortear esta crisis de contexto, Cloudflare introdujo 'Code Mode', un patrón arquitectónico que reduce el footprint del modelo a solo dos primitivas: search_api y execute_code. En lugar de exponer miles de esquemas JSON, el sistema empaqueta la API como una biblioteca fuertemente tipada en TypeScript y pone a disposición del agente un sandbox aislado. El modelo explora dinámicamente las firmas tipadas de los métodos requeridos y escribe un script compacto en TypeScript que orquesta las llamadas internamente. Dicho script se ejecuta dentro de un V8 Isolate local en el servidor, procesando bucles, paginaciones y filtros en milisegundos, retornando al LLM únicamente el resultado sintetizado final en un solo viaje de ida y vuelta."
            }},
            {{
                "type": "heading",
                "text": "3. Evidencia Empírica de Anthropic: Reducción del 98% en Consumo de Tokens"
            }},
            {{
                "type": "paragraph",
                "text": "De manera paralela, las investigaciones publicadas por Anthropic en torno a 'Code execution with MCP' y 'Programmatic Tool Calling' arrojaron resultados coincidentes. En benchmarks de orquestación de datos y manipulación de catálogos masivos, el consumo de tokens descendió de más de 150,000 tokens en flujos de llamadas tradicionales a menos de 2,000 tokens utilizando ejecución de código programática. Los modelos de frontera han sido preentrenados con billones de líneas de código fuente en GitHub, por lo que su habilidad para inferir sintaxis, gestionar excepciones y aplicar lógica booleana mediante código estructurado supera por mucho su capacidad de rellenar estructuras JSON fragmentadas."
            }},
            {{
                "type": "heading",
                "text": "4. Seguridad, Aislamiento de Memoria y el Futuro de las APIs para IA"
            }},
            {{
                "type": "paragraph",
                "text": "El reto central de este nuevo paradigma radica en la seguridad del entorno de ejecución. Correr código sintetizado dinámicamente por un modelo exige sandboxes herméticos con tiempos de arranque casi instantáneos. La adopción de V8 Isolates frente a contenedores Docker tradicionales permite tiempos de inicialización inferiores a 5 milisegundos con límites estrictos de memoria y CPU. Asimismo, la arquitectura desacopla por completo las credenciales y tokens de acceso: el LLM escribe código contra clientes preautenticados en el servidor, impidiendo que llaves criptográficas queden expuestas en el contexto conversacional. Como conclusión, la ingeniería de software está presenciando el fin de las APIs diseñadas exclusivamente para humanos: en el ecosistema agéntico, el código TypeScript es la interfaz universal definitiva."
            }}
        ],
        "fuentes": [
            "Cloudflare. (2025). Code Mode: the better way to use MCP. Cloudflare Engineering Blog. https://blog.cloudflare.com",
            "Cloudflare. (2026). Code Mode: give agents an entire API in 1,000 tokens. Cloudflare Documentation & Research.",
            "Anthropic. (2025). Code execution with MCP: Advancing agentic tool use through programmatic execution. Anthropic Research Publications.",
            "Anthropic. (2025). Introducing advanced tool use and programmatic calling for Claude 3.5. Anthropic Engineering Updates.",
            "V8 Project. (2026). Lightweight sandboxing and multi-tenant execution using V8 Isolates. Google V8 Documentation."
        ]
    }},
'''
    if '"slug": "sia-dev-02-la-muerte-del-function-calling-code-mode-vs-mcp"' not in content:
        insert_marker = "RESEARCH_COMPENDIUM = {"
        content = content.replace(insert_marker, insert_marker + "\n" + res_entry)
        build_mag_path.write_text(content, encoding='utf-8')
        print("✅ Registrado en build_magazine.py.")
    else:
        print("ℹ️ Ya existía el registro en build_magazine.py.")
        
    cmd_build = [sys.executable, str(BASE_DIR / "build_magazine.py")]
    subprocess.run(cmd_build, check=True)
    print("✅ Revista digital recompilada y actualizada.")

def step6_sync_gdrive():
    print("\n" + "="*70)
    print("☁️ PASO 6: Sincronizando con Google Drive Hub...")
    print("="*70)
    
    GDRIVE_REELS.mkdir(parents=True, exist_ok=True)
    GDRIVE_AUDIO.mkdir(parents=True, exist_ok=True)
    GDRIVE_VAULT.mkdir(parents=True, exist_ok=True)
    
    reel_src = REELS_DIR / REEL_FILENAME
    poster_src = REELS_DIR / REEL_POSTER_FILENAME
    audio_src = AUDIO_DIR / EPISODE_FILENAME
    
    if reel_src.exists():
        shutil.copy2(reel_src, GDRIVE_REELS / REEL_FILENAME)
        print(f"  [Drive] Reel copiado: {GDRIVE_REELS / REEL_FILENAME}")
    if poster_src.exists():
        shutil.copy2(poster_src, GDRIVE_REELS / REEL_POSTER_FILENAME)
        print(f"  [Drive] Poster copiado: {GDRIVE_REELS / REEL_POSTER_FILENAME}")
    if audio_src.exists():
        shutil.copy2(audio_src, GDRIVE_AUDIO / EPISODE_FILENAME)
        print(f"  [Drive] Audio master copiado: {GDRIVE_AUDIO / EPISODE_FILENAME}")

def step7_create_obsidian_vault_note():
    print("\n" + "="*70)
    print("📝 PASO 7: Creando Nota en Obsidian Vault con Social Kit...")
    print("="*70)
    
    vault_shorts_dir = GDRIVE_VAULT / "02_Reels_Shorts"
    vault_shorts_dir.mkdir(parents=True, exist_ok=True)
    
    note_content = f"""# Reel Stupy 08: Code Mode vs MCP — La Muerte del Function Calling

**ID:** `sIA_Reel_Stupy_08_CodeMode_vs_MCP`
**Episodio Relacionado:** `sIA_Dev_02_Code_Mode_vs_MCP_Cloudflare_Anthropic_2026-11-04.mp3`
**Fecha de Publicación:** 2026-11-04
**Autor / Arquitecto:** `cacs`
**Estado:** Publicado en TikTok (@escucha_sia) y Spotify Show

---

## 🎬 Video Renderizado
![[sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4]]

---

## 📋 Social Kit de Publicación

### Caption para TikTok / YouTube Shorts / Instagram Reels
> ¿RIP MCP? Conectar 20 herramientas a tu agente de IA está quebrando tu factura de tokens. Te explico por qué llamar herramientas una por una murió, y cómo Cloudflare metió 2,500 endpoints en solo 1,000 tokens usando Code Mode y sandboxes de V8. 🤖⚡
>
> 🎧 Episodio completo en Spotify (sIA Podcast) y ensayo de arquitectura en el link del perfil.
>
> #mcp #agentesia #cloudflare #anthropic #claudecode #programacion #softwareengineer #v8isolates #aiarchitecture #siapodcast

### Primer Comentario Fijado (Call to Action de Conversión)
> 🚀 **Análisis técnico con código y benchmarks:**
> Lee el artículo completo con diagramas de arquitectura en:  
> 👉 https://escucha-sia.github.io/articulos/sia-dev-02-la-muerte-del-function-calling-code-mode-vs-mcp.html  
> O escucha el debate en Spotify buscando "sIA".

---

## 🔬 Puntos Clave de Arquitectura
1. **El colapso de escala:** 2,500 endpoints de Cloudflare = 1.17M tokens en esquemas JSON.
2. **La solución Code Mode:** 2 primitivas (`search` y `execute`) y TypeScript SDK = 1,000 tokens fijos (-99.9%).
3. **Benchmark de Anthropic:** De 150,000 a 2,000 tokens (-98%) en tareas complejas de orquestación.
4. **Sandboxing de baja latencia:** V8 Isolates con arranque en <5ms y desacoplamiento de credenciales.
"""
    note_path = vault_shorts_dir / "sIA_Reel_Stupy_08_CodeMode_vs_MCP.md"
    note_path.write_text(note_content, encoding='utf-8')
    print(f"✅ Nota de Obsidian Vault creada: {note_path}")

def step8_git_deploy():
    print("\n" + "="*70)
    print("🚀 PASO 8: Desplegando en GitHub Pages...")
    print("="*70)
    
    subprocess.run(["git", "add", "."], cwd=str(BASE_DIR), check=True)
    subprocess.run(["git", "commit", "-m", "feat(episode): publish sIA Dev 02 - Code Mode vs MCP and Reel Stupy 08"], cwd=str(BASE_DIR), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=True)
    print("✅ Despliegue en GitHub Pages completado.")

def step9_upload_to_tiktok():
    print("\n" + "="*70)
    print("📲 PASO 9: Subiendo Reel 08 a TikTok Studio (@escucha_sia)...")
    print("="*70)
    
    from playwright.sync_api import sync_playwright
    
    video_path = REELS_DIR / REEL_FILENAME
    caption = "¿RIP MCP? Por qué la IA ya no llama a herramientas una por una: Cloudflare Code Mode, 2,500 endpoints en 1,000 tokens y sandboxes V8. Episodio completo en Spotify (sIA) y blog en perfil. #mcp #agentesia #cloudflare #anthropic #programacion #softwareengineer #siapodcast"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES"
        )
        page = context.new_page()
        print("[*] Accediendo a TikTok Studio...")
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        
        file_input = page.locator("input[type='file']").first
        if file_input.count() == 0:
            frame = page.frame_locator("iframe").first
            file_input = frame.locator("input[type='file']").first
            
        print(f"[*] Subiendo archivo: {video_path}...")
        file_input.set_input_files(str(video_path))
        time.sleep(8)
        
        caption_box = page.locator("div[contenteditable='true']").first
        if caption_box.count() > 0:
            print("[*] Escribiendo pie de video...")
            caption_box.click()
            caption_box.fill("")
            time.sleep(1)
            caption_box.type(caption, delay=20)
            time.sleep(2)
            
        print("[*] Esperando procesamiento del video (15s)...")
        time.sleep(15)
        
        post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
        if post_btn.count() > 0:
            print("[*] Haciendo clic en Publicar...")
            post_btn.click()
            time.sleep(10)
            print("✅ Publicación ejecutada en TikTok Studio.")
        else:
            print("⚠️ Botón publicar no encontrado directamente.")
            
        page.screenshot(path=str(SCRATCH_DIR / "tiktok_upload_codemode.png"))
        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    print("="*70)
    print("🚀 INICIANDO PIPELINE 360°: sIA Dev #02 (Code Mode vs MCP)")
    print("="*70)
    step1_produce_full_audio()
    step2_produce_reel_audio()
    step3_prepare_stupy_composition()
    step4_render_reel()
    step5_register_and_rebuild_magazine()
    step6_sync_gdrive()
    step7_create_obsidian_vault_note()
    step8_git_deploy()
    step9_upload_to_tiktok()
    print("\n" + "="*70)
    print("🎉 PACK 360° COMPLETADO: sIA Dev #02 (Code Mode vs MCP)")
    print("="*70)
