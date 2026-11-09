import asyncio
import os
import sys
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

SCRIPT_SEGMENTS = [
    # ACTO 1: El Mito del Monolito Denso (00:00 - 00:50)
    (VOICE_JORGE, "En enero de 2025, Wall Street vivió el mayor colapso bursátil de una sola empresa en la historia de la tecnología: seiscientos mil millones de dólares borrados de Nvidia en veinticuatro horas."),
    (VOICE_DALIA, "El culpable no fue un gigante como Google o Microsoft, sino un laboratorio chino llamado DeepSeek, que lanzó un modelo capaz de competir con los titanes de Silicon Valley habiendo gastado menos de seis millones de dólares en entrenamiento."),
    (VOICE_JORGE, "Para entender cómo lograron semejante humillación algorítmica, hay que entender el fraude de los modelos densos tradicionales. Cuando le preguntas cualquier cosa a un modelo como GPT-4, cada uno de sus cientos de miles de millones de parámetros se enciende forzosamente en la tarjeta gráfica."),
    (VOICE_DALIA, "Es el equivalente a encender todas las luces de un rascacielos de cien pisos solo para leer un libro en la planta baja. Una brutalidad energética que exigía clústeres de cien mil chips H100 consumiendo plantas eléctricas enteras."),

    # ACTO 2: La Anatomía de Mixture of Experts (00:50 - 01:45)
    (VOICE_JORGE, "La respuesta de la arquitectura moderna se llama MoE, o Mixture of Experts: Mezcla de Expertos."),
    (VOICE_DALIA, "En lugar de un cerebro gigante homogéneo, el modelo se divide en decenas o cientos de redes neuronales especializadas, llamadas expertos. Unos son expertos en sintaxis de Python, otros en medicina forense, otros en lógica matemática y otros en gramática."),
    (VOICE_JORGE, "Al frente de la red se coloca un árbitro matemático llamado Gating Router o Enrutador. Cuando entra una palabra o token, el router calcula en milisegundos qué dos o tres expertos son los únicos capacitados para responder."),
    (VOICE_DALIA, "En DeepSeek V3, el modelo tiene un tamaño colosal de seiscientos setenta y un mil millones de parámetros en disco, pero para cada palabra individual solo se activan treinta y siete mil millones. El noventa y cinco por ciento del modelo duerme en silencio, recortando el costo de cálculo a una fracción ridícula."),

    # ACTO 3: Multi-Head Latent Attention y la Memoria Comprimida (01:45 - 02:35)
    (VOICE_JORGE, "Pero el verdadero cuello de botella de la inteligencia artificial nunca fue la velocidad del procesador, sino el hambre voraz de memoria RAM de video: la llamada caché K-V."),
    (VOICE_DALIA, "En conversaciones largas de miles de palabras, las tarjetas gráficas colapsaban porque tenían que retener matrices gigantescas en memoria de alto ancho de banda. DeepSeek resolvió esto con una técnica matemática brillante llamada Multi-Head Latent Attention o MLA."),
    (VOICE_JORGE, "En lugar de guardar todas las claves y valores en su tamaño completo, el algoritmo comprime la memoria en un vector latente de baja dimensión antes de escribirlo en la RAM. Al momento de calcular la atención, lo descomprime en el aire."),
    (VOICE_DALIA, "El resultado fue una reducción del noventa y tres por ciento en el uso de memoria. Lo que antes requería ocho servidores con refrigeración líquida ahora cabía en un puñado de tarjetas comerciales."),

    # ACTO 4: Precisión FP8 y la Rebelión del Hardware (02:35 - 03:20)
    (VOICE_JORGE, "A esto le sumaron el entrenamiento en precisión FP8, números de apenas ocho bits calculados con precisión microscópica, y un pipeline de comunicación llamado DualPipe que solapa la computación con el envío de datos entre nodos para que los chips jamás esperen ociosos."),
    (VOICE_DALIA, "El impacto geopolítico fue instantáneo: demostró que la inteligencia artificial de frontera no requiere presupuestos militares de miles de millones de dólares, sino arquitectura matemática elegante y optimización extrema a bajo nivel."),
    (VOICE_JORGE, "El monopolio del hardware se fracturó: los modelos de código abierto ya no son juguetes académicos, sino bestias de ingeniería capaces de ejecutarse de forma soberana y local."),

    # ACTO 5: Comunidad Abierta y Llamado a la Acción (03:20 - 04:05)
    (VOICE_DALIA, "DeepSeek abrió su código y sus pesos al mundo, demostrando que en el software, la inteligencia algorítmica siempre supera a la fuerza bruta del hardware."),
    (VOICE_JORGE, "Recuerda que puedes escuchar el audio completo de todas nuestras investigaciones en Spotify en tu trayecto diario, o ver los diagramas tácticos en movimiento en TikTok y YouTube buscando escucha guion bajo s-i-a."),
    (VOICE_DALIA, "Y ahora, la mesa está abierta para toda nuestra comunidad. No importa qué tan complejo, oscuro o fascinante sea: déjanos en los comentarios qué tecnología, arquitectura, algoritmo o misterio corporativo quieres que desarmemos."),
    (VOICE_JORGE, "Tú propones el tema, nosotros investigamos los datos reales y lo convertimos en código animado. ¡Escribe tu propuesta en los comentarios y construyamos el próximo capítulo juntos!")
]

async def generate_moe_audio():
    os.makedirs("audio", exist_ok=True)
    temp_files = []
    
    print("🎙️ Generando segmentos de audio para MoE & DeepSeek con Edge-TTS...")
    for idx, (voice, text) in enumerate(SCRIPT_SEGMENTS):
        part_filename = f"audio/temp_moe_{idx:02d}.mp3"
        communicate = edge_tts.Communicate(text, voice, rate="+2%", volume="+0%")
        await communicate.save(part_filename)
        temp_files.append(part_filename)
        print(f"  [✓] Segmento {idx+1}/{len(SCRIPT_SEGMENTS)} generado ({voice})")
        
    concat_list_path = "audio/concat_moe.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in temp_files:
            abs_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")
            
    raw_output = "audio/sIA_Corp_12_DeepSeek_MoE_raw.mp3"
    master_output = "audio/sIA_Corp_12_DeepSeek_MoE_2026-11-09.mp3"
    
    print("🎛️ Concatenando y masterizando a -16 LUFS estéreo...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        raw_output
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_output,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "24000",
        "-b:a", "128k",
        master_output
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for p in temp_files:
        try: os.remove(p)
        except: pass
    try:
        os.remove(concat_list_path)
        os.remove(raw_output)
    except: pass
        
    print(f"✅ Audio maestro generado con éxito: {master_output}")
    
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", master_output
    ], capture_output=True, text=True)
    duration = float(res.stdout.strip())
    print(f"⏱️ Duración total: {duration:.2f} segundos ({duration/60:.2f} minutos)")
    return master_output, duration

if __name__ == "__main__":
    asyncio.run(generate_moe_audio())
