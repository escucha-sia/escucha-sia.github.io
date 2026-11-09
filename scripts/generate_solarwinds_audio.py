import asyncio
import os
import sys
import subprocess
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Audio configuration
VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

SCRIPT_SEGMENTS = [
    # ACTO 1: El Caballo de Troya Perfecto (00:00 - 00:45)
    (VOICE_JORGE, "En marzo de 2020, dieciocho mil redes corporativas y gubernamentales alrededor del mundo instalaron una actualización rutinaria de software."),
    (VOICE_DALIA, "No era una descarga sospechosa de internet. Venía de SolarWinds Orion, una plataforma de monitoreo de servidores utilizada por el Pentágono, el Departamento de Estado de Estados Unidos, los laboratorios nucleares de Los Álamos y más de cuatrocientas empresas de la lista Fortune 500."),
    (VOICE_JORGE, "El paquete de actualización estaba firmado digitalmente con un certificado criptográfico legítimo y válido. Ningún antivirus del planeta alertó de una amenaza. El caballo de troya más sofisticado del siglo veintiuno acababa de entrar por la puerta principal."),

    # ACTO 2: La Inyección en el Compilador (00:45 - 01:35)
    (VOICE_DALIA, "Durante meses, los mejores equipos de ciberseguridad se hicieron la misma pregunta: ¿cómo lograron los atacantes meter cuatro mil líneas de código malicioso en el producto estrella de SolarWinds sin que ningún ingeniero se diera cuenta?"),
    (VOICE_JORGE, "La respuesta fue una obra maestra de ingeniería inversa llamada Solorigate. Los atacantes, identificados como el grupo de inteligencia rusa Cozy Bear, no tocaron el repositorio oficial de código en GitHub ni modificaron los archivos fuente en disco."),
    (VOICE_DALIA, "En su lugar, crearon un software durmiente que vigilaba el proceso de compilación em ese build punto exe. Justo en la fracción de segundo en que el compilador leía el código fuente limpio y lo transformaba en memoria RAM en un archivo ejecutable, el implante inyectaba el malware directamente en la memoria volátil."),
    (VOICE_JORGE, "Cuando el archivo punto de ele ele salía del compilador, ya contenía el backdoor llamado Sunburst. Y de inmediato, los sistemas automatizados de SolarWinds lo firmaban con su clave criptográfica oficial. El código en el repositorio estaba limpio; el producto final estaba envenenado."),

    # ACTO 3: La Hibernación de 14 Días y el DNS Fantasma (01:35 - 02:25)
    (VOICE_DALIA, "Pero la genialidad técnica de Sunburst no terminó en la compilación. Una vez instalado en los servidores de las víctimas, el malware entraba en hibernación absoluta durante catorce días continuos."),
    (VOICE_JORGE, "Esta pausa deliberada burlaba las cajas de arena o sandboxes automatizadas de los antivirus, que solo monitorean el comportamiento de un software nuevo durante unos minutos."),
    (VOICE_DALIA, "Al despertar, no abría conexiones directas a servidores rusos. Utilizaba peticiones de nombres de dominio o D-N-S codificadas en base 32 hacia un dominio aparentemente legítimo alojado en Amazon Web Services: a-v-s-v-m-cloud punto com."),
    (VOICE_JORGE, "El tráfico parecía telemetría inocente de servidores. Si la víctima no era de interés estratégico, el malware se autodestruía en silencio. Pero si detectaba que estaba dentro del Departamento del Tesoro o de Microsoft, desplegaba en memoria una segunda carga espía indetectable llamada Teardrop."),

    # ACTO 4: El Error del 2FA y la Cacería de FireEye (02:25 - 03:10)
    (VOICE_DALIA, "¿Cómo cayó este fantasma digital? No fue por un error en su código, sino por un detalle humano en diciembre de 2020."),
    (VOICE_JORGE, "El equipo de seguridad de la firma FireEye notó una alerta insólita: alguien había registrado un segundo teléfono móvil en el sistema de autenticación de dos factores para hacerse pasar por uno de sus empleados."),
    (VOICE_DALIA, "Kevin Mandia y su equipo rastrearon cada paquete de red. No encontraron brechas en sus firewalls ni contraseñas filtradas. El origen del tráfico provenía de su propio software de monitoreo: la actualización oficial de SolarWinds."),
    (VOICE_JORGE, "Cuando FireEye notificó al gobierno federal y a Microsoft, el impacto fue devastador. Los atacantes habían tenido acceso durante nueve meses a correos diplomáticos, redes de defensa y partes del código fuente de los sistemas en la nube de Azure."),

    # ACTO 5: Cierre Omnicanal y Votación Comunitaria (03:10 - 03:50)
    (VOICE_DALIA, "SolarWinds destruyó la vieja ilusión de que el software firmado es software seguro, acelerando la adopción obligatoria de arquitecturas de Confianza Cero o Zero Trust a nivel global."),
    (VOICE_JORGE, "Puedes escuchar esta crónica completa en Spotify mientras manejas, o ver los diagramas interactivos en YouTube y TikTok buscando escucha guion bajo s-i-a."),
    (VOICE_DALIA, "Y ahora, la decisión es de ustedes. Para nuestro próximo capítulo, ¿qué historia de ingeniería o drama corporativo quieren que desarmemos?"),
    (VOICE_JORGE, "Opción uno: el fallo del sensor y el algoritmo MCAS del Boeing 737 MAX. Opción dos: el juicio de Nintendo contra Universal que bautizó a Kirby. U opción tres: el fraude de la máquina Edison de Theranos."),
    (VOICE_DALIA, "Déjanos en los comentarios cuál quieres que hagamos a continuación o escribe tu caso favorito. El comentario más votado será el próximo capítulo completo.")
]

async def generate_audio():
    os.makedirs("audio", exist_ok=True)
    temp_files = []
    
    print("🎙️ Generando segmentos de audio con Edge-TTS...")
    for idx, (voice, text) in enumerate(SCRIPT_SEGMENTS):
        part_filename = f"audio/temp_sw_{idx:02d}.mp3"
        communicate = edge_tts.Communicate(text, voice, rate="+2%", volume="+0%")
        await communicate.save(part_filename)
        temp_files.append(part_filename)
        print(f"  [✓] Segmento {idx+1}/{len(SCRIPT_SEGMENTS)} generado ({voice})")
        
    # Concat list file
    concat_list_path = "audio/concat_solarwinds.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in temp_files:
            abs_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")
            
    raw_output = "audio/sIA_Corp_10_SolarWinds_SUNBURST_raw.mp3"
    master_output = "audio/sIA_Corp_10_SolarWinds_SUNBURST_2026-11-08.mp3"
    
    print("🎛️ Concatenando y masterizando a -16 LUFS...")
    # Concat
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy", raw_output
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Normalize with loudnorm to -16 LUFS
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_output,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "24000", "-b:a", "128k",
        master_output
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Clean up temp
    for p in temp_files:
        try: os.remove(p)
        except: pass
    try: os.remove(concat_list_path)
    except: pass
    try: os.remove(raw_output)
    except: pass
    
    # Get duration
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", master_output
    ], capture_output=True, text=True)
    duration = float(res.stdout.strip())
    print(f"✨ Master listo: {master_output} ({duration:.2f} segundos / {duration/60:.2f} min)")
    return master_output, duration

if __name__ == "__main__":
    asyncio.run(generate_audio())
