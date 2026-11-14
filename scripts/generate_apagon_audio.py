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

MASTER_AUDIO = AUDIO_DIR / "sIA_Corp_14_Microsoft_Apagon_Global_2026-11-13.mp3"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# Diálogo estructurado en 5 Actos (19 segmentos)
DIALOGUE = [
    # ACTO 1: EL MINUTO CERO DEL COLAPSO GLOBAL (SCROLL-STOPPER)
    {
        "act": 1,
        "voice": "Jorge",
        "text": "Jueves doce de noviembre de dos mil veintiséis. Trece horas con veintiséis minutos. En una fracción de segundo, las pantallas del Banco de Inglaterra, los despachos de aerolíneas en Fráncfort y las historias clínicas en hospitales de setenta y cuatro países se fueron a negro absoluto."
    },
    {
        "act": 1,
        "voice": "Dalia",
        "text": "No fue un ciberataque de estado. No fue un malware ruso ni un corte físico de fibra transatlántica. Fue la infraestructura de Microsoft trescientos sesenta y cinco, Teams y Azure desplomándose en una reacción en cadena que duró casi veinte horas consecutivas."
    },
    {
        "act": 1,
        "voice": "Jorge",
        "text": "Bienvenidos a sIA Crónicas. Hoy abrimos la caja negra de la mayor caída en la historia del cloud computing: la autopsia técnica forense de cómo una reconfiguración rutinaria de red encendió la mecha en un sistema que ya no tenía bomberos para apagarlo."
    },

    # ACTO 2: LA CHISPA INOCENTE: LA RECONFIGURACIÓN DE RUTINA
    {
        "act": 2,
        "voice": "Dalia",
        "text": "Todo comenzó con un script automatizado de balanceo de capacidad en los clústeres Front-Door de Azure. Una actualización de topología considerada de bajo riesgo que se ejecutaba sin supervisión humana."
    },
    {
        "act": 2,
        "voice": "Jorge",
        "text": "El cambio reasignaba rutas de tráfico entre regiones. Pero el nuevo perfil de configuración contenía una anomalía sutil en la tabla de asignación de puertos, provocando que los routers de borde consumieran el cien por ciento de su memoria compartida en cuestión de segundos."
    },
    {
        "act": 2,
        "voice": "Dalia",
        "text": "En condiciones normales, una brigada de ingeniería veterana habría abortado el despliegue de inmediato. Pero con los equipos reducidos al mínimo, el pipeline automático continuó propagando la regla rota a través de los nodos de enlace global."
    },

    # ACTO 3: LA CASCADA DE LOS HEALTH CHECKS CIEGOS
    {
        "act": 3,
        "voice": "Jorge",
        "text": "Y aquí entró en juego el primer acelerador del desastre: los algoritmos de monitoreo automático. Los probes de salud estaban programados para enviar pings cada quinientos milisegundos a cada nodo."
    },
    {
        "act": 3,
        "voice": "Dalia",
        "text": "Al estar los balanceadores saturados procesando memoria, tardaban seiscientos milisegundos en responder. Para el algoritmo ciego de monitorización, una respuesta tardía equivalía a un nodo muerto."
    },
    {
        "act": 3,
        "voice": "Jorge",
        "text": "El sistema de conmutación por error retiró automáticamente los nodos saturados y desvió todo el tráfico mundial hacia los servidores restantes. ¿El resultado? Los nodos vecinos recibieron el doble de carga al instante y colapsaron exactamente igual. En menos de quince minutos, una región entera de la nube se apagó sola."
    },
    {
        "act": 3,
        "voice": "Dalia",
        "text": "El software de alta disponibilidad diseñado para prevenir caídas se convirtió en la máquina que destruía su propia infraestructura."
    },

    # ACTO 4: LA ESTAMPIDA DEL BÚFALO: THUNDERING HERD
    {
        "act": 4,
        "voice": "Jorge",
        "text": "Pero lo peor estaba por venir. Cuando los ingenieros de guardia intentaron reiniciar los servicios a mano, se toparon de frente con el monstruo más temido de los sistemas distribuidos: el Thundering Herd, la estampida masiva de clientes."
    },
    {
        "act": 4,
        "voice": "Dalia",
        "text": "Imaginen a cincuenta millones de aplicaciones de Teams, Outlook y servicios de Azure en todo el planeta perdiendo conexión. Todas estaban configuradas con reintentos agresivos sin retroceso exponencial aleatorio."
    },
    {
        "act": 4,
        "voice": "Jorge",
        "text": "Cada vez que un servidor intentaba arrancar en frío, millones de peticiones en cola se abalanzaban en el mismo milisegundo. El nodo era aniquilado antes de completar el apretón de manos TLS. Reiniciar la nube era como intentar encender una cerilla en medio de un huracán."
    },
    {
        "act": 4,
        "voice": "Dalia",
        "text": "La única forma de detener la masacre fue aplicar medidas extremas: blackholing manual, desconectar regiones enteras de internet y levantar la infraestructura a oscuras, paso por paso y a ciegas."
    },

    # ACTO 5: EL VEREDICTO FORENSE & DEBATE COMUNITARIO
    {
        "act": 5,
        "voice": "Jorge",
        "text": "Casi veinte horas después, el mundo recuperó el servicio. Pero el costo fue devastador: penalizaciones multimillonarias por acuerdos de nivel de servicio rotos, investigaciones parlamentarias y una verdad incómoda sobre la mesa."
    },
    {
        "act": 5,
        "voice": "Dalia",
        "text": "La caída del doce de noviembre no fue un accidente técnico aislado. Fue la factura cobrada por la Paradoja de Nadella que analizamos en el capítulo anterior: puedes gastar cincuenta mil millones en silicio de inteligencia artificial, pero cuando la red colapsa, ningún modelo de lenguaje puede sustituir la intuición de un ingeniero humano veterano."
    },
    {
        "act": 5,
        "voice": "Jorge",
        "text": "Abrimos el debate a la comunidad: ¿Debería prohibirse por ley que bancos y hospitales dependan de un solo monopolio de nube? Y en tus propios sistemas, ¿alguna vez has sufrido la pesadilla de un Thundering Herd?"
    },
    {
        "act": 5,
        "voice": "Dalia",
        "text": "¡Déjanos tu experiencia y tu opinión en los comentarios de TikTok o Spotify, y síguenos para más crónicas técnicas en sIA Podcast!"
    }
]

async def generate_segment(idx, seg):
    voice = VOICE_JORGE if seg["voice"] == "Jorge" else VOICE_DALIA
    out_file = SCRATCH_DIR / f"apagon_seg_{idx:02d}_{seg['voice'].lower()}.mp3"
    communicate = edge_tts.Communicate(seg["text"], voice, rate="+2%", pitch="+0Hz")
    await communicate.save(str(out_file))
    return out_file

async def main():
    print("=" * 60)
    print("🎙️ GENERANDO MASTER DE AUDIO: sIA Crónicas #14 (El Apagón Global)")
    print(f"   Voz Jorge: {VOICE_JORGE}")
    print(f"   Voz Dalia: {VOICE_DALIA}")
    print(f"   Segmentos: {len(DIALOGUE)}")
    print("=" * 60)

    seg_files = []
    for idx, seg in enumerate(DIALOGUE):
        print(f"  [{idx+1}/{len(DIALOGUE)}] Acto {seg['act']} | {seg['voice']}: {seg['text'][:50]}...")
        f = await generate_segment(idx, seg)
        seg_files.append(f)

    # Concat file
    concat_list = SCRATCH_DIR / "apagon_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as cl:
        for f in seg_files:
            # Escape path for ffmpeg
            safe_path = str(f).replace("\\", "/")
            cl.write(f"file '{safe_path}'\n")

    raw_concat = SCRATCH_DIR / "apagon_raw_concat.mp3"
    print("\n[*] Ensamblando segmentos con FFmpeg...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(raw_concat)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("[*] Normalizando a -16 LUFS estéreo profesional...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_concat),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.05",
        "-ar", "24000", "-ac", "2", "-b:a", "128k",
        str(MASTER_AUDIO)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Measure final duration
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(MASTER_AUDIO)
    ], capture_output=True, text=True, check=True)
    dur = float(res.stdout.strip())
    size_mb = MASTER_AUDIO.stat().st_size / (1024 * 1024)

    print(f"\n🎉 Master de audio generado exitosamente:")
    print(f"   Ruta: {MASTER_AUDIO}")
    print(f"   Duración: {dur:.2f} segundos ({dur/60:.2f} min)")
    print(f"   Tamaño: {size_mb:.2f} MB")

if __name__ == "__main__":
    asyncio.run(main())
