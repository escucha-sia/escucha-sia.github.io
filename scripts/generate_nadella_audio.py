import asyncio
import os
import sys
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
AUDIO_DIR = ROOT_DIR / "audio"
SCRATCH_DIR = ROOT_DIR / "scratch"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

MASTER_AUDIO = AUDIO_DIR / "sIA_Corp_13_Microsoft_Nadella_Despidos_IA_2026-11-13.mp3"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# Diálogo estructurado en 5 Actos (19 segmentos)
DIALOGUE = [
    # ACTO 1: EL ENIGMA DEL ÉXITO Y LA FACTURA DE SILICIO
    {
        "act": 1,
        "voice": "Jorge",
        "text": "Bienvenidos a sIA Crónicas. Hoy abrimos las puertas de Redmond para desarmar la mayor contradicción económica en la historia de la tecnología: cómo la empresa más valiosa del planeta despidió a más de veinte mil ingenieros mientras gastaba cincuenta mil millones de dólares en comprar silicio para inteligencia artificial."
    },
    {
        "act": 1,
        "voice": "Dalia",
        "text": "Es la llamada Paradoja de Nadella. En las llamadas trimestrales con Wall Street, Satya Nadella presumía márgenes récord y un valor bursátil rozando los cuatro billones de dólares. Pero puertas adentro, bautizó la purga laboral con una frase cínica: el enigma del éxito."
    },
    {
        "act": 1,
        "voice": "Jorge",
        "text": "El mensaje para los accionistas era implacable. Cada dólar recortado en salarios humanos se redirigía de inmediato a pagar la factura eléctrica de OpenAI, comprar chips de Nvidia y construir megacentros de datos con refrigeración líquida."
    },
    {
        "act": 1,
        "voice": "Dalia",
        "text": "La promesa corporativa sonaba seductora: la inteligencia artificial aumentará la productividad de los que se queden, y Copilot escribirá el código de los que se fueron."
    },

    # ACTO 2: LA MUERTE DEL CONTROL DE CALIDAD Y LA PURGA DE SREs
    {
        "act": 2,
        "voice": "Jorge",
        "text": "Pero la tijera no cayó al azar. El golpe más brutal no fue en marketing ni en ventas, sino en los cimientos invisibles que sostenían a la nube: las divisiones de control de calidad tradicional y los ingenieros de confiabilidad de sitios, los famosos SREs."
    },
    {
        "act": 2,
        "voice": "Dalia",
        "text": "Durante décadas, Microsoft mantuvo brigadas enteras de ingenieros veteranos dedicados exclusivamente a romper el software antes de que saliera a producción. Diseñaban pruebas de estrés destructivas, simulaban caídas de cables submarinos y testeaban el arranque en frío de Exchange."
    },
    {
        "act": 2,
        "voice": "Jorge",
        "text": "Esa disciplina fue desmantelada. La directiva impuso un dogma peligroso: el código ahora lo generan modelos de lenguaje, las pruebas unitarias las sintetizan agentes sintéticos, y los pipelines de integración continua se corrigen solos."
    },
    {
        "act": 2,
        "voice": "Dalia",
        "text": "Nadella llegó a jactarse en público de que hasta el treinta por ciento del código nuevo en Microsoft ya lo escribía la inteligencia artificial. Lo que no mencionó fue el costo colateral: la pérdida total de la memoria institucional."
    },

    # ACTO 3: EL CASTILLO DE NAIPES Y LA ANSIEDAD EN REDMOND
    {
        "act": 3,
        "voice": "Jorge",
        "text": "En foros internos y plataformas como Blind, los ingenieros que sobrevivieron a las olas de recortes comenzaron a encender las alarmas. La carga de trabajo se triplicó para los pocos humanos que quedaban en guardia."
    },
    {
        "act": 3,
        "voice": "Dalia",
        "text": "Un desarrollador veterano de Azure lo describió con crudeza en una carta abierta: estamos operando un avión supersónico con el piloto automático encendido, pero despedimos a los mecánicos que sabían cómo reparar el timón si fallaban los motores."
    },
    {
        "act": 3,
        "voice": "Jorge",
        "text": "Los modelos de IA pueden generar miles de líneas de código en segundos, pero carecen de intuición arquitectónica. Cuando un sistema distribuido entra en condiciones de carrera o colapsa por latencia de red, un asistente probabilístico no puede razonar bajo fuego."
    },
    {
        "act": 3,
        "voice": "Dalia",
        "text": "Y mientras tanto, los bancos, hospitales, escuelas y gobiernos de todo el planeta continuaban migrando a ciegas su infraestructura a Microsoft 365, asumiendo que tras la pantalla había un ejército de expertos cuidando sus datos."
    },

    # ACTO 4: LA ADVERTENCIA SILENCIADA
    {
        "act": 4,
        "voice": "Jorge",
        "text": "A principios de dos mil veintiséis, varios líderes técnicos que renunciaron voluntariamente advirtieron al comité de auditoría: la infraestructura de nube de Microsoft se ha vuelto un monocultivo hiperfrágil. Una falla menor en los chequeos automatizados provocará un efecto dominó incontrolable."
    },
    {
        "act": 4,
        "voice": "Dalia",
        "text": "Nadie quiso escuchar. El mercado premiaba a Microsoft por cada GPU instalada y castigaba cualquier gasto en redundancia operativa humana. Los presupuestos de guardia se redujeron y los procedimientos de arranque manual fueron reemplazados por scripts desatendidos."
    },
    {
        "act": 4,
        "voice": "Jorge",
        "text": "Se creó la tormenta perfecta: una red global con cientos de millones de usuarios conectados, administrada por sistemas automatizados sin amortiguadores humanos suficientes."
    },

    # ACTO 5: EL GANCHO A LA PARTE 2 Y LLAMADO A LA COMUNIDAD
    {
        "act": 5,
        "voice": "Dalia",
        "text": "La trampa estaba armada. Y el reloj comenzó a descontar los segundos hasta que el sistema finalmente estalló."
    },
    {
        "act": 5,
        "voice": "Jorge",
        "text": "El jueves doce de noviembre de dos mil veintiséis, un simple cambio de capacidad de red detonó la pesadilla: setenta y cuatro países desconectados, el Banco de Inglaterra mudo y veinte horas de caos absoluto donde ninguna inteligencia artificial pudo salvar a Microsoft."
    },
    {
        "act": 5,
        "voice": "Dalia",
        "text": "En el próximo capítulo desarmaremos minuto a minuto la autopsia técnica de ese apagón: el colapso de los health checks y el temido efecto estampida. ¿Tú crees que sustituir ingenieros por inteligencia artificial fue una genialidad financiera o una negligencia histórica? Déjanos tu opinión en los comentarios."
    },
    {
        "act": 5,
        "voice": "Jorge",
        "text": "Escúchanos en Spotify y encuentra los diagramas forenses en escucha-sia.github.io. Nos vemos en la Parte Dos."
    }
]

async def generate_audio():
    print(f"[*] Sintetizando {len(DIALOGUE)} segmentos de audio con Edge-TTS...")
    segment_files = []
    
    for idx, item in enumerate(DIALOGUE):
        seg_file = SCRATCH_DIR / f"seg_{idx:02d}_{item['voice']}.mp3"
        voice = VOICE_JORGE if item["voice"] == "Jorge" else VOICE_DALIA
        
        # Rate slightly dynamic: Jorge firm and deep, Dalia precise and analytical
        rate = "+3%" if item["voice"] == "Jorge" else "+2%"
        
        communicate = edge_tts.Communicate(item["text"], voice, rate=rate)
        await communicate.save(str(seg_file))
        segment_files.append(seg_file)
        print(f"  [✓] Segmento {idx+1}/{len(DIALOGUE)} sintetizado ({item['voice']})")

    # Concatenate segments using ffmpeg concat demuxer
    concat_list = SCRATCH_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sf in segment_files:
            f.write(f"file '{sf.resolve().as_posix()}'\n")

    raw_concat = SCRATCH_DIR / "raw_concat.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy", str(raw_concat)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Master audio processing: Normalization to -16 LUFS stereo, 24kHz
    print("[*] Masterizando audio a -16 LUFS estéreo con ecualización de radiodifusión...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_concat),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.05",
        "-ar", "24000", "-b:a", "128k", str(MASTER_AUDIO)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Measure total duration
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(MASTER_AUDIO)
    ], capture_output=True, text=True)
    dur = float(res.stdout.strip())
    size_mb = MASTER_AUDIO.stat().st_size / (1024 * 1024)

    print("=======================================================")
    print(f"🎉 AUDIO MAESTRO GENERADO EXITOSAMENTE:")
    print(f"   Archivo: {MASTER_AUDIO}")
    print(f"   Duración: {dur:.2f}s ({dur/60:.2f} min)")
    print(f"   Tamaño: {size_mb:.2f} MB")
    print("=======================================================")

if __name__ == "__main__":
    asyncio.run(generate_audio())
