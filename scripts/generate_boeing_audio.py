import asyncio
import os
import sys
import subprocess
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Configuración de locutores oficiales
VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

SCRIPT_SEGMENTS = [
    # ACTO 1: La Presión de Airbus y el Motor Adelantado (00:00 - 00:50)
    (VOICE_JORGE, "En diciembre de 2010, Airbus lanzó una bomba en la industria de la aviación comercial: el A320neo, un avión con motores gigantes que ahorraban un quince por ciento de combustible."),
    (VOICE_DALIA, "Boeing entró en pánico. American Airlines, su cliente más fiel durante décadas, amenazó con cancelar pedidos multimillonarios si no ofrecían una respuesta inmediata."),
    (VOICE_JORGE, "Diseñar un avión desde cero habría costado diez mil millones de dólares y casi una década de certificaciones. La solución de emergencia de la directiva fue tomar su fuselaje más vendido, el Boeing 737 diseñado en 1967, y montarle los nuevos motores CFM LEAP-1B."),
    (VOICE_DALIA, "Pero había un grave problema físico: el 737 original estaba diseñado muy pegado al suelo. Los enormes motores no cabían bajo las alas. La solución de ingeniería fue moverlos hacia adelante y elevarlos sobre el borde de ataque."),

    # ACTO 2: La Sustentación Inestable y el Nacimiento del MCAS (00:50 - 01:40)
    (VOICE_JORGE, "Ese cambio geométrico alteró radicalmente la aerodinámica del avión. En aceleración y ángulos de ascenso pronunciados, las carcasas de los motores generaban una sustentación no deseada que empujaba la nariz del avión hacia arriba."),
    (VOICE_DALIA, "Bajo las reglas de la aviación, si un avión tiende a levantar la nariz de forma descontrolada arriesga una entrada en pérdida o stall. Y para certificarlo, los pilotos de todo el mundo tendrían que pasar por costosos entrenamientos en simuladores de vuelo."),
    (VOICE_JORGE, "Para evitar que las aerolíneas pagaran millones de dólares en cursos y prometiendo que el MAX se comportaría exactamente igual al 737 anterior, los ingenieros crearon un parche por software en segundo plano: el MCAS, o Sistema de Aumento de Características de Maniobra."),
    (VOICE_DALIA, "El MCAS fue diseñado para actuar en silencio: si detectaba que el avión subía con un ángulo excesivo, tomaría el control del estabilizador horizontal de la cola para empujar la nariz hacia abajo automáticamente, sin que los pilotos tuvieran que intervenir."),

    # ACTO 3: El Fallo Fatal de Arquitectura: Un Solo Sensor (01:40 - 02:30)
    (VOICE_JORGE, "Hasta aquí parecía una solución lógica de ingeniería de control. Pero Boeing cometió un pecado mortal en el diseño de sistemas críticos: la falta de redundancia."),
    (VOICE_DALIA, "El avión contaba con dos sensores externos de ángulo de ataque en la nariz, pequeñas veletas metálicas que miden la dirección del flujo de aire. Pero el código del software del MCAS fue programado para consultar únicamente a uno de ellos a la vez."),
    (VOICE_JORGE, "Si una sola veleta fallaba por el impacto de un ave, hielo o descalibración, la computadora de vuelo recibía una lectura errónea. Creía falsamente que el morro del avión apuntaba peligrosamente hacia el cielo, aunque el vuelo fuera perfectamente nivelado."),
    (VOICE_DALIA, "Y lo peor: el software tenía autoridad casi ilimitada para mover el estabilizador de cola mucho más allá de lo que los ingenieros habían especificado en las pruebas iniciales."),

    # ACTO 4: La Batalla de los Pilotos contra el Algoritmo (02:30 - 03:20)
    (VOICE_JORGE, "En octubre de 2018 con el vuelo 610 de Lion Air y en marzo de 2019 con Ethiopian Airlines, la trampa de software se cerró en el aire."),
    (VOICE_DALIA, "Apenas el avión despegaba, el sensor dañado mandaba una alerta de entrada en pérdida falsa. Los timones vibraban con fuerza y el sistema MCAS activaba el motor eléctrico del tornillo sinfín de la cola, forzando la nariz hacia el suelo a toda velocidad."),
    (VOICE_JORGE, "Los pilotos luchaban desesperadamente, jalando la palanca de control con una fuerza de más de cuarenta kilogramos para levantar el morro."),
    (VOICE_DALIA, "Lograban nivelar el avión por unos instantes, pero el algoritmo estaba programado con un ciclo implacable: cada cinco segundos, el MCAS se reactivaba en bucle continuo, volviendo a clavar la nariz del avión en picada hasta agotar la fuerza humana de la tripulación."),

    # ACTO 5: La Omisión del Manual y la Votación Comunitaria (03:20 - 04:05)
    (VOICE_JORGE, "La revelación más indignante de las investigaciones del Congreso de Estados Unidos fue descubrir que Boeing había eliminado deliberadamente cualquier mención del MCAS del manual de vuelo para que los pilotos ni siquiera supieran que ese software existía a bordo."),
    (VOICE_DALIA, "El caso 737 MAX se convirtió en la lección más costosa de la historia aeroespacial sobre lo que ocurre cuando las presiones corporativas recortan la redundancia de sensores y subordinan el control humano a algoritmos opacos."),
    (VOICE_JORGE, "Recuerda que puedes escuchar todas nuestras crónicas completas en Spotify en tu coche, o ver las figuras técnicas animadas en YouTube y TikTok buscando escucha guion bajo s-i-a."),
    (VOICE_DALIA, "Y ahora, déjanos tu voto en los comentarios para el Capítulo número doce: ¿prefieres la batalla legal de Nintendo contra Universal que salvó a Donkey Kong, o el fraude de las máquinas de sangre de Theranos? ¡Tu comentario decide el próximo episodio!")
]

async def generate_audio():
    os.makedirs("audio", exist_ok=True)
    temp_files = []
    
    print("🎙️ Generando segmentos de audio para Boeing 737 MAX con Edge-TTS...")
    for idx, (voice, text) in enumerate(SCRIPT_SEGMENTS):
        part_filename = f"audio/temp_boeing_{idx:02d}.mp3"
        communicate = edge_tts.Communicate(text, voice, rate="+2%", volume="+0%")
        await communicate.save(part_filename)
        temp_files.append(part_filename)
        print(f"  [✓] Segmento {idx+1}/{len(SCRIPT_SEGMENTS)} generado ({voice})")
        
    # Concat list file
    concat_list_path = "audio/concat_boeing.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in temp_files:
            abs_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")
            
    raw_output = "audio/sIA_Corp_11_Boeing_737_MAX_MCAS_raw.mp3"
    master_output = "audio/sIA_Corp_11_Boeing_737_MAX_MCAS_2026-11-09.mp3"
    
    print("🎛️ Concatenando y masterizando a -16 LUFS...")
    # Concat
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        raw_output
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Master -16 LUFS
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_output,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "24000",
        "-b:a", "128k",
        master_output
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Clean up temp files
    for p in temp_files:
        try:
            os.remove(p)
        except Exception:
            pass
    try:
        os.remove(concat_list_path)
        os.remove(raw_output)
    except Exception:
        pass
        
    print(f"✅ Audio maestro generado con éxito: {master_output}")
    
    # Get duration
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", master_output
    ], capture_output=True, text=True)
    duration = float(res.stdout.strip())
    print(f"⏱️ Duración total: {duration:.2f} segundos ({duration/60:.2f} minutos)")
    return master_output, duration

if __name__ == "__main__":
    asyncio.run(generate_audio())
