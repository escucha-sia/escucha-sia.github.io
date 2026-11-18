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

MASTER_AUDIO = AUDIO_DIR / "sIA_Sec_04_CrowdStrike_BSOD_Kernel_2026-11-18.mp3"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

# Diálogo estructurado en 5 Actos (15 segmentos quirúrgicos, in-media-res, ritmo trepidante)
DIALOGUE = [
    # ACTO 1: EL VIERNES DEL FIN DEL MUNDO (SCROLL-STOPPER SHOCK)
    {
        "act": 1,
        "voice": "Jorge",
        "text": "Viernes diecinueve de julio. Cuatro de la mañana. En cuestión de minutos, las pantallas de salidas en cientos de aeropuertos, los monitores de quirófanos en hospitales y los servidores de los mayores bancos del planeta se tiñeron de azul cobalto con un reinicio infinito."
    },
    {
        "act": 1,
        "voice": "Dalia",
        "text": "Ocho millones y medio de computadoras con Windows quedaron completamente inservibles. No fue un ciberataque de estado ni un malware ruso. Fue un archivo de apenas cuarenta kilobytes enviado por la empresa de ciberseguridad más poderosa del mundo: Craud-Straik."
    },
    {
        "act": 1,
        "voice": "Jorge",
        "text": "El costo estimado superó los diez mil millones de dólares. ¿Cómo es posible que un archivo de configuración destruyera la infraestructura física global? Hoy en sIA desentrañamos la autopsia técnica de la temida Pantalla Azul y el fatídico puntero nulo."
    },

    # ACTO 2: LA MURALLA DE LA CPU: RING TRES VS RING CERO
    {
        "act": 2,
        "voice": "Dalia",
        "text": "Para entender el desastre hay que bajar a los anillos de protección del procesador x86. En el Ring Tres viven las aplicaciones normales: Chrome, Spotify o tu editor de código. Si una aplicación falla, el sistema operativo la mata y tu máquina sigue viva como si nada."
    },
    {
        "act": 2,
        "voice": "Jorge",
        "text": "Pero en el fondo absoluto de la jerarquía reside el Ring Cero: el Modo Núcleo. Aquí no existen redes de seguridad. El código tiene acceso irrestricto a toda la memoria física y a las instrucciones de la CPU. Si un controlador en Ring Cero comete un solo error, el hardware se congela en seco y la máquina colapsa."
    },
    {
        "act": 2,
        "voice": "Dalia",
        "text": "Craud-Straik Fálcon operaba en este anillo supremo mediante su controlador csagent punto sys para cazar hackers antes de que tocaran el disco. Un poder absoluto que venía con un riesgo letal."
    },

    # ACTO 3: EL ARCHIVO FANTASMA DOSCIENTOS NOVENTA Y UNO
    {
        "act": 3,
        "voice": "Jorge",
        "text": "Para actualizar sus reglas sin reiniciar servidores, Craud-Straik inventó los Channel Files. Archivos binarios que el driver de Ring Cero leía e interpretaba en caliente."
    },
    {
        "act": 3,
        "voice": "Dalia",
        "text": "A las cero cuatro horas UTC, Craud-Straik desplegó el archivo de canal doscientos noventa y uno a todo el planeta simultáneamente. Sin despliegue escalonado. Sin pruebas canario. Y violando la regla de oro de todo ingeniero: jamás actualizar producción un viernes de madrugada."
    },
    {
        "act": 3,
        "voice": "Jorge",
        "text": "Pero lo peor estaba adentro del archivo. El parser de C++ del controlador esperaba veintiún campos de entrada válidos. Pero el archivo doscientos noventa y uno solo contenía veinte. La ranura veintiuno estaba completamente vacía."
    },

    # ACTO 4: EL CHOQUE DEL PUNTERO NULO: OFFSET CERO EQUIS NOVENTA Y SEIS
    {
        "act": 4,
        "voice": "Dalia",
        "text": "Cuando el driver intentó leer el parámetro inexistente, el puntero de memoria devolvió cero. En lugar de verificar si el puntero era válido, el código le sumó un desplazamiento de memoria de noventa y seis bytes en hexadecimal: cero equis nueve ce."
    },
    {
        "act": 4,
        "voice": "Jorge",
        "text": "Resultado: el procesador intentó leer la dirección de memoria cero equis noventa y seis. Pero esa dirección no existe en el mapa de memoria del kernel. La unidad de manejo de memoria lanzó de inmediato la excepción no recuperable: Page Fault in Nonpaged Area."
    },
    {
        "act": 4,
        "voice": "Dalia",
        "text": "Al estar en Ring Cero, Windows no pudo salvar el sistema. Entró en pánico, arrojó la Pantalla Azul y, al reiniciar, volvió a cargar el driver defectuoso, atrapando a millones de máquinas en un bucle de muerte del que solo se salía borrando el archivo a mano."
    },

    # ACTO 5: LA GRAN LECCIÓN Y DEBATE COMUNITARIO
    {
        "act": 5,
        "voice": "Jorge",
        "text": "El colapso demostró que darle acceso total al kernel a software de terceros es una bomba de tiempo. Apple ya expulsó a los antivirus fuera del kernel en macOS mediante extensiones de sistema aisladas en User Space."
    },
    {
        "act": 5,
        "voice": "Dalia",
        "text": "Microsoft ahora enfrenta la misma encrucijada: ¿restringir los agentes de seguridad al Ring Tres para garantizar estabilidad, o mantener el acceso a bajo nivel para interceptar exploits sofisticados?"
    },
    {
        "act": 5,
        "voice": "Jorge",
        "text": "Mándale este video a ese colega que todavía hace despliegues en viernes. Y dinos en los comentarios: ¿Debe prohibirse por ley el acceso al kernel para empresas de seguridad? ¡Comenta tu postura y suscríbete a sIA!"
    }
]

async def generate_segment(idx: int, item: dict, temp_dir: Path) -> Path:
    voice = VOICE_JORGE if item["voice"] == "Jorge" else VOICE_DALIA
    rate = "+3%" if item["voice"] == "Jorge" else "+2%"
    pitch = "+0Hz"
    
    out_file = temp_dir / f"seg_{idx:02d}_{item['voice']}.mp3"
    communicator = edge_tts.Communicate(
        text=item["text"],
        voice=voice,
        rate=rate,
        pitch=pitch
    )
    await communicator.save(str(out_file))
    return out_file

async def main():
    print("=======================================================")
    print("🎙️ GENERANDO AUDIO MASTER: sIA Sec #04 - CrowdStrike BSOD")
    print("=======================================================")
    
    temp_dir = SCRATCH_DIR / "crowdstrike_segments"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    tasks = []
    for idx, item in enumerate(DIALOGUE):
        tasks.append(generate_segment(idx, item, temp_dir))
    
    segment_files = await asyncio.gather(*tasks)
    print(f"[+] Generados {len(segment_files)} segmentos individuales con Edge-TTS.")
    
    concat_list = temp_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segment_files:
            safe_path = str(seg).replace("\\", "/")
            f.write(f"file '{safe_path}'\n")
            
    # Concatenate & normalize with loudnorm (-16 LUFS)
    raw_concat = temp_dir / "raw_concat.mp3"
    concat_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(raw_concat)
    ]
    subprocess.run(concat_cmd, check=True, capture_output=True)
    
    # Loudnorm to EBU R128 (-16 LUFS stereo 24kHz)
    print("[*] Normalizando audio master con FFmpeg Loudnorm a -16 LUFS...")
    loudnorm_cmd = [
        "ffmpeg", "-y", "-i", str(raw_concat),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "24000", "-ac", "2", "-b:a", "128k",
        str(MASTER_AUDIO)
    ]
    subprocess.run(loudnorm_cmd, check=True, capture_output=True)
    
    # Measure final duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(MASTER_AUDIO)
    ]
    res = subprocess.run(probe_cmd, check=True, capture_output=True, text=True)
    duration = float(res.stdout.strip())
    print(f"✅ Master generado con éxito: {MASTER_AUDIO.name}")
    print(f"   Duración total: {duration:.2f}s ({int(duration//60):02d}:{int(duration%60):02d})")
    print(f"   Tamaño: {MASTER_AUDIO.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    asyncio.run(main())
