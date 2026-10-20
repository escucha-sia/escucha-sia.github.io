"""
Generador Maestro de los 4 Episodios sIA Deep Dive (Arquitectura sIA Storytelling 4.0).
1. Brújula de Sección & Vertical (00:00 - 00:25)
2. Resumen Ejecutivo & Tesis (00:25 - 00:50)
3. Despegue ("Alcanzarnos") & Debate Técnico a Fondo (00:50+)
4. Fuera de la Burbuja: Realidad implacable y límites físicos/organizacionales
5. Veredicto de Arquitectura & Flywheel Tripartito (Blog + Reel + Podcast)
"""

import sys
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# EPISODIO 1: BigQuery Gemini Cloud Assist y la Muerte de las Consultas Manuales
# ==============================================================================
SCRIPT_EP_01 = """
[CHAPTER: Apertura & Brújula: sIA Data Engineering & Cloud]
JORGE: Bienvenidos a sIA Deep Dive. Hoy abrimos nuestra vertical de Data Engineering y Cloud Analytics para poner bajo la lupa la transformación más profunda en la gestión de almacenes de datos analíticos: ¿llegó el fin definitivo de las consultas ese cu ele artesanales?
DALIA: Así es, Jorge. En esta entrega desmenuzamos la integración nativa de Gemini Cloud Assist en Google Cloud BigQuery y Dataplex. Nuestra tesis de hoy es contundente: la era en la que el analista o el ingeniero de datos dedicaba el setenta por ciento de su jornada a picar consultas ese cu ele complejas desde cero ha terminado. La analítica conversacional sobre grafos de metadatos se está consolidando como la interfaz estándar por defecto.
JORGE: En los próximos minutos vamos a analizar cómo el motor infiere la intención del usuario mediante linaje semántico, la optimización predictiva de particiones y costos, y el desplazamiento inevitable del valor profesional desde la sintaxis hacia la gobernanza de datos.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, arranquemos por las entrañas de BigQuery Studio. ¿Cómo opera realmente Gemini bajo el capó sin limitarse a un simple autocompletado superficial?

[CHAPTER: Anatomía de BigQuery Studio: Linaje, Dataplex y Planes de Ejecución]
JORGE: Bajo el capó, BigQuery Studio ya no trata al ese cu ele como texto plano. Cuando escribes o consultas en lenguaje natural, Gemini no adivina al vacío: consulta en tiempo real el grafo de conocimiento empresarial expuesto por Dataplex. Analiza el esquema relacional, los tipos de datos de las columnas, la frecuencia de actualización y el historial de consultas de toda la organización.
DALIA: Eso significa que infiere la intención semántica del analista. Si preguntas por el volumen de ventas por región, Gemini inspecciona el linaje para verificar si debe consultar la tabla de transacciones en bruto o la vista materializada previamente agregada. Puede recomendar particionamiento por fecha, sugerir clústeres óptimos para reducir el escaneo de bytes y explicar cuellos de botella en el plan de ejecución de la consulta usando sentencias expléin avanzadas.
JORGE: Y ese ahorro no es menor, Dalia. En almacenes de petabytes donde cada terabyte escaneado cuesta cinco dólares en cómputo bajo demanda, optimizar una consulta reduciendo el escaneo de cien terabytes a dos gigabytes representa cientos de miles de dólares al año para una corporación.

[CHAPTER: 🌌 Fuera de la Burbuja: Alucinaciones Silenciosas y la Trampa de las Agregaciones]
DALIA: Pero entremos a nuestra cápsula Fuera de la Burbuja, porque en analítica de datos los errores de la IA no se manifiestan con errores sintácticos, sino con catástrofes financieras silenciosas.
JORGE: Totalmente. Si le pides a Gemini ventas netas del último trimestre en una empresa de retail, ¿sabe el modelo cómo se descuentan las devoluciones de mercancía, las notas de crédito o los impuestos locales? Si la empresa no definió un contrato de datos semántico o una métrica unificada en d b t, el modelo elegirá la columna numérica que parezca más lógica. La consulta correrá en tres segundos, el resultado numérico se verá impecable en el tablero directivo, pero estará financieramente equivocado.
DALIA: Además, está la economía oculta de los tokens. Disparar llamadas a LLMs para generar consultas recurrentes que podrían resolverse con modelos estáticos compilados en d b t introduce latencia innecesaria y costos adicionales de inferencia. La IA nunca sustituye el rigor del ingeniero; lo eleva a nivel de auditoría y arquitectura semántica.

[CHAPTER: Veredicto de Arquitectura & Ecosistema sIA]
JORGE: Y para nuestra mirada geek: esto nos recuerda a los Archivos Akáshicos y a la biblioteca de Yggdrasil en la literatura fantástica. Tener acceso a toda la información del universo no te sirve de nada si no sabes formular la pregunta con los parámetros exactos y validar las fuentes.
DALIA: Veredicto de arquitectura: el valor del ingeniero de datos no murió; migró de la fontanería sintáctica a la arquitectura de contratos, calidad y linaje. Quien no domine Dataplex y d b t será reemplazado por quien sí los gobierne.
JORGE: Si eres profesional de datos y quieres consultar la arquitectura de referencia con Dataplex, las consultas de benchmark y las fuentes en formato APA, revisa el artículo técnico de hoy en escucha-sia punto github punto io.
DALIA: Y si buscas la síntesis visual de esta arquitectura con diagramas explicativos, no te pierdas nuestro Reel técnico en TikTok y YouTube Shorts. ¡Nos escuchamos en el siguiente sIA Deep Dive!
"""

# ==============================================================================
# EPISODIO 2: El Fin de la Amnesia en LLMs: Context Caching y Memoria Persistente
# ==============================================================================
SCRIPT_EP_02 = """
[CHAPTER: Apertura & Brújula: sIA Inteligencia Artificial & Modelos]
JORGE: Bienvenidos a sIA Deep Dive. Hoy abrimos nuestra vertical de Inteligencia Artificial y Arquitectura de Modelos para desarmar una de las mayores limitaciones en el despliegue de sistemas inteligentes: la amnesia crónica de los modelos de lenguaje.
DALIA: Así es, Jorge. En esta entrega analizamos el impacto revolucionario de Context Caching en Gemini y el diseño de arquitecturas de memoria persistente. Nuestra tesis de hoy es tajante: la ventana de contexto efímera y sin estado ha quedado obsoleta. Para que los agentes autónomos sean viables y rentables en entornos de producción, deben aprender de interacciones pasadas y conservar experiencia acumulada sin multiplicar exponencialmente la factura de cómputo.
JORGE: En los próximos minutos vamos a desmenuzar la mecánica interna de la memoria de claves y valores en servidores en la nube, la jerarquía entre memoria de trabajo, episódica y semántica, y cómo recortar hasta en un ochenta por ciento los costos y la latencia de inferencia.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, vayamos directo a las entrañas del silicio. ¿Cómo funciona técnicamente Context Caching para terminar de una vez por todas con el reprocesamiento redundante de millones de tokens?

[CHAPTER: Mecánica de Inferencia: KV Cache Compartido y Memoria Jerárquica]
JORGE: Tradicionalmente, cada vez que hacías una llamada a la A P I de un modelo, el sistema tenía que calcular los vectores de atención para todo el texto previo desde cero. Si le pasabas la documentación de tu empresa de quinientos mil tokens, pagabas y esperabas el procesamiento de esos quinientos mil tokens en cada interacción.
DALIA: Con Context Caching, los vectores de atención procesados se congelan en la memoria de alta velocidad de los servidores de cómputo, la famosa K V cache. El modelo genera un identificador único con un tiempo de expiración o T T L configurado. En las siguientes solicitudes, el motor salta directamente al punto donde se quedó la memoria, procesando solo los nuevos tokens de la pregunta.
JORGE: El impacto operativo es demoledor: la latencia al primer token se reduce hasta en un ochenta por ciento y el costo por token almacenado es una fracción mínima comparado con la inferencia activa.
DALIA: Pero el verdadero salto conceptual es el aprendizaje anidado o nested learning. No se trata solo de acumular texto estático, sino de estructurar la memoria en tres capas: memoria de trabajo para resolver la tarea en curso, memoria episódica para recordar incidentes y soluciones pasadas, y memoria semántica para almacenar los principios inmutables de la arquitectura empresarial.

[CHAPTER: 🌌 Fuera de la Burbuja: Envenenamiento de Contexto y Poda de Memoria]
JORGE: Entremos a nuestra cápsula Fuera de la Burbuja, porque almacenar memoria infinita sin criterio es una receta garantizada para el colapso del sistema.
DALIA: El peligro número uno se llama envenenamiento de contexto o context poisoning. Si un agente almacena en su memoria episódica persistente una deducción errónea, un código vulnerable o un supuesto falso validado accidentalmente por un usuario, ese error se convertirá en una verdad fundamental que contaminará todas las decisiones operativas futuras.
JORGE: Y está el fenómeno de degradación de atención, conocido como Lost in the Middle. Aunque la ventana de contexto soporte millones de tokens, los modelos tienden a prestar menor atención a la información atrapada en el tercio intermedio del caché. Sin políticas estrictas de recolección de basura, poda semántica y consolidación de memoria, un agente hipermnésico se vuelve lento, errático y prohibitivamente caro.

[CHAPTER: Veredicto de Arquitectura & Ecosistema sIA]
DALIA: Y aquí la conexión con la cultura geek es sencillamente fascinante. En el arco de Alicization de Sword Art Online, las almas artificiales llamadas Fluctlights tenían un límite biológico de memoria de aproximadamente ciento cincuenta años. Cuando ese límite se alcanzaba, la sobrecarga de recuerdos saturaba el núcleo y colapsaba la personalidad.
JORGE: ¡Exactamente, Dalia! En los agentes de software de dos mil veintiséis, diseñar las políticas de olvido selectivo y consolidación de memoria es tan crítico como diseñar la persistencia misma.
DALIA: Veredicto de arquitectura: los agentes sin memoria son meras calculadoras avanzadas; los agentes con memoria infinita no estructurada son bombas de tiempo cognitivas. El arte de la ingeniería de contexto radica en recordar lo esencial y podar el ruido.
JORGE: Si quieres revisar las pruebas de latencia, el código para implementar Context Caching con la A P I de Gemini y las referencias académicas en APA, visita el artículo técnico en escucha-sia punto github punto io.
DALIA: Y si prefieres explorar el diagrama visual de la jerarquía de memoria en un Reel técnico de cuarenta y cinco segundos, encuéntranos en TikTok y YouTube. ¡Hasta el próximo episodio!
"""

# ==============================================================================
# EPISODIO 3: Data Mesh en Retail Masivo: Contratos Semánticos y Streaming Continuo
# ==============================================================================
SCRIPT_EP_03 = """
[CHAPTER: Apertura & Brújula: sIA Arquitectura Empresarial & Datos]
JORGE: Bienvenidos a sIA Deep Dive. Hoy abrimos nuestra vertical de Arquitectura Empresarial y Gobernanza de Datos para examinar las fracturas del almacenamiento analítico centralizado frente al comercio omnicanal masivo.
DALIA: Totalmente, Jorge. En esta entrega desmenuzamos la implementación práctica de Data Mesh en gigantes del retail a escala global tipo Walmart. Nuestra tesis de hoy es rotunda: en organizaciones con cientos de miles de transacciones por segundo, los almacenes monolíticos centralizados no fracasan por falta de poder de cómputo en la nube, sino por la fricción sociocultural entre equipos. Data Mesh descentraliza la propiedad de los datos tratándolos como productos autónomos gobernados por contratos semánticos inmutables.
JORGE: En los próximos minutos vamos a desgranar cómo se estructuran los Data Products mediante d b t, esquemas tipados en Kafka y PubSub, la figura del Ingeniero de Plataforma de autoservicio y las claves para evitar que la descentralización se convierta en una pesadilla ingobernable.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, arranquemos por las trincheras operativas. ¿Por qué el modelo clásico de un equipo central de datos se rompe de forma inevitable en el retail moderno?

[CHAPTER: Descentralización por Dominios: Data Products y Contratos en dbt]
JORGE: En una empresa que factura millones de transacciones por minuto, pretender que un solo equipo central de datos entienda la logística de última milla, el inventario en tiendas físicas, la pasarela de pagos y los algoritmos de recomendación es absurdo. El equipo central se convierte en un cuello de botella burocrático permanente.
DALIA: En Data Mesh, cada dominio de negocio se convierte en el dueño absoluto de su producto de datos. El equipo de inventario no te da acceso a su base de datos transaccional en crudo; publica un Data Product formalizado mediante contratos de datos escritos en Y A M L y modelos testeados en d b t.
JORGE: Esos contratos definen el esquema exacto de los eventos en Kafka o PubSub, los tipos de datos, los valores nulos permitidos y los acuerdos de nivel de servicio. Si el dominio de logística cambia la estructura de sus eventos sin respetar el contrato semántico, el sistema de integración continua bloquea el despliegue antes de romper las métricas de negocio.

[CHAPTER: 🌌 Fuera de la Burbuja: La Trampa del Data Swamp y la Plataforma de Autoservicio]
DALIA: Pero entremos a nuestra cápsula Fuera de la Burbuja, porque Data Mesh mal ejecutado es una de las modas corporativas más peligrosas de la industria.
JORGE: Exacto. Si le dices a cada departamento operativo que ahora son dueños de sus datos, pero esos equipos no tienen cultura de ingeniería de software ni disciplina de pruebas, en seis meses no tienes un Data Mesh: tienes un pantano de datos fragmentado, silos aislados y una factura de almacenamiento en la nube multiplicada por diez.
DALIA: Por eso la pieza angular de Data Mesh no son los dominios, sino el equipo de Plataforma de Datos de autoservicio. La plataforma debe entregar herramientas automatizadas para que crear un pipeline, registrar metadatos en Dataplex y ejecutar validaciones de calidad con Great Expectations sea tan fácil como hacer un commit en Git. La descentralización sin plataforma es caos garantizado.

[CHAPTER: Veredicto de Arquitectura & Ecosistema sIA]
JORGE: Y para nuestra analogía geek: esto funciona exactamente igual que la economía de gremios en Log Horizon o los mundos de rol masivo en línea. Si el gremio de herreros altera unilateralmente la pureza de los lingotes de hierro sin avisar al gremio de comerciantes, toda la economía comercial del servidor colapsa de inmediato. Los contratos de datos son las leyes inmutables del mercado.
DALIA: Veredicto de arquitectura: Data Mesh no es comprar una herramienta tecnológica nueva; es una transformación organizativa radical donde los datos se construyen, empaquetan y distribuyen con la misma exigencia que el software de producción.
JORGE: Si quieres descargar la plantilla Y A M L de un Data Contract listo para producción, las métricas de gobierno y las referencias académicas en APA, visita el artículo completo en escucha-sia punto github punto io.
DALIA: Y para repasar el flujo de eventos entre dominios en un diagrama técnico de cuarenta y cinco segundos, encuéntranos en TikTok y redes sociales. ¡Nos vemos en el próximo sIA Deep Dive!
"""

# ==============================================================================
# EPISODIO 4: Inferencia en el Borde vs Nube: NPU del Galaxy S25 e Insta360 X4
# ==============================================================================
SCRIPT_EP_04 = """
[CHAPTER: Apertura & Brújula: sIA Hardware Móvil & Cómputo en el Borde]
JORGE: Bienvenidos a sIA Deep Dive. Hoy abrimos nuestra vertical de Hardware Móvil y Cómputo en el Borde para poner a prueba el silicio que llevamos en la mano y en la mochila: ¿puede la inteligencia artificial local derrotar la hegemonía de la nube?
DALIA: Así es, Jorge. En este episodio analizamos a fondo la capacidad de inferencia en dispositivo del Galaxy ese veinticinco y la captura espacial acelerada por hardware en la Insta tres sesenta X cuatro. La tesis que sostenemos hoy es clara: la asistencia contextual y la visión espacial en tiempo real no pueden depender de la latencia y los costos de red de los centros de datos remotos; la soberanía y la inmediatez exigen correr modelos reducidos directamente en la N P U del dispositivo.
JORGE: Durante los siguientes minutos exploraremos la microarquitectura de los procesadores Snapdragon y Exynos, la cuantización a cuatro bits de modelos de tres a siete mil millones de parámetros, y el procesamiento de video en ocho K a sesenta cuadros por segundo sin drenar la batería.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, vayamos directo a las especificaciones físicas. ¿Qué salto real han dado las unidades de procesamiento neuronal en los teléfonos insignia de dos mil veintiséis?

[CHAPTER: Silicio de Inferencia: Decenas de TOPS, INT4 y Visión Espacial 8K]
JORGE: Con los procesadores de última generación en la familia Galaxy ese veinticinco, contamos con decenas de T O P S de rendimiento directo en la N P U. Esto permite correr modelos de lenguaje reducidos de tres a siete mil millones de parámetros cuantizados a cuatro bits de forma completamente local, sin conexión a Internet y con consumo mínimo de energía.
DALIA: Y en movilidad, funciones del sistema operativo Uan U I nueve procesan la cámara, las llamadas y el contexto ambiental sin enviar un solo byte a servidores externos. Mientras tanto, en cámaras de acción como la Insta tres sesenta X cuatro, los chips de visión por computadora realizan el ensamblado de lentes y la estabilización FlowState de video en ocho K en tiempo real utilizando aceleración directa por hardware.
JORGE: Desacoplar la experiencia del usuario de la señal de red cambia las reglas del juego. No hay tiempo de ida y vuelta a la nube ni riesgo de filtración de datos privados.

[CHAPTER: 🌌 Fuera de la Burbuja: Estrangulamiento Térmico y la Realidad Híbrida]
DALIA: Pero entremos a nuestra cápsula Fuera de la Burbuja, porque la termodinámica en dispositivos compactos es despiadada.
JORGE: Totalmente. Un teléfono móvil carece de ventiladores activos; depende exclusivamente de la disipación pasiva a través del chasis de titanio o aluminio y pequeñas cámaras de vapor. Si pones a una N P U a inferir un modelo de siete mil millones de parámetros de forma continua durante quince minutos, la temperatura interna supera los cuarenta y cinco grados Celsius.
DALIA: Y en ese instante entra en acción el estrangulamiento térmico o thermal throttling: el sistema operativo recorta las frecuencias de reloj a la mitad para proteger la batería y evitar quemaduras al usuario, duplicando la latencia al instante. Por eso el futuro no es cien por ciento local ni cien por ciento en la nube, sino una arquitectura híbrida: inferencia local instantánea para tareas sensoriales y delegación inteligente a la nube solo cuando se requiere razonamiento profundo.

[CHAPTER: Veredicto de Arquitectura & Ecosistema sIA]
JORGE: Y como paralelismo geek: pensemos en el dispositivo Augma de Sword Art Online Ordinal Scale. La magia de su realidad aumentada radicaba en que el renderizado de combate ocurría al instante en la sien del jugador, sin esperar paquetes de red desde un servidor lejano.
DALIA: Procesar en el borde para experimentar el mundo en tiempo real; apoyarse en la nube para el análisis macroscópico.
JORGE: Veredicto de ingeniería: el silicio de borde redefine la privacidad y la inmediatez, pero el diseño térmico impone los límites del software. La maestría del arquitecto está en orquestar el equilibrio entre el bolsillo y la nube.
DALIA: Si quieres consultar las curvas de disipación térmica, los benchmarks de tokens por segundo en N P U y las referencias académicas en formato APA, revisa el artículo técnico de hoy en escucha-sia punto github punto io.
JORGE: Y si buscas la comparativa visual de rendimiento entre silicio local y centros de datos en un Reel técnico de cuarenta y cinco segundos, encuéntranos en TikTok y redes. ¡Hasta la próxima edición de sIA Deep Dive!
"""

DEEPDIVES_CONFIG = [
    {
        "title": "sIA Deep Dive: BigQuery Gemini Cloud Assist y la Muerte de las Consultas Manuales",
        "slug": "sIA_DeepDive_BigQuery_Gemini_Cloud_Assist.mp3",
        "desc": "sIA Deep Dive: Análisis exhaustivo sobre cómo Gemini Cloud Assist en BigQuery y Dataplex desplaza el valor del Data Engineer del SQL manual a la modelación semántica y gobernanza. | Leer artículo técnico y esquemas APA: https://escucha-sia.github.io/articulos/bigquery-gemini-cloud-assist-arquitectura.html",
        "script": SCRIPT_EP_01
    },
    {
        "title": "sIA Deep Dive: El Fin de la Amnesia en LLMs: Context Caching y Memoria Persistente",
        "slug": "sIA_DeepDive_Context_Caching_Memoria_Persistente.mp3",
        "desc": "sIA Deep Dive: Investigación profunda sobre Context Caching en Gemini, arquitecturas de memoria episódica jerárquica, aprendizaje anidado y el paralelismo con los Fluctlights de SAO. | Leer artículo técnico y esquemas APA: https://escucha-sia.github.io/articulos/context-caching-memoria-persistente-llms.html",
        "script": SCRIPT_EP_02
    },
    {
        "title": "sIA Deep Dive: Data Mesh en Retail Masivo: Contratos Semánticos y Streaming Continuo",
        "slug": "sIA_DeepDive_Data_Mesh_Retail_Streaming.mp3",
        "desc": "sIA Deep Dive: Descentralización de datos en retail de alta escala (estilo Walmart), Data Products con dbt y BigQuery, contratos semánticos en Kafka y economía de gremios. | Leer artículo técnico y esquemas APA: https://escucha-sia.github.io/articulos/data-mesh-retail-streaming-contratos.html",
        "script": SCRIPT_EP_03
    },
    {
        "title": "sIA Deep Dive: Inferencia en el Borde vs Nube: NPU del Galaxy S25 e Insta360 X4",
        "slug": "sIA_DeepDive_Edge_AI_Galaxy_S25_Insta360.mp3",
        "desc": "sIA Deep Dive: Silicio NPU en Galaxy S25 (Snapdragon/Exynos), inferencia de SLMs locales en One UI 9, visión computacional 8K en Insta360 X4 y el Augma de Ordinal Scale. | Leer artículo técnico y esquemas APA: https://escucha-sia.github.io/articulos/edge-ai-galaxy-s25-insta360-silicio.html",
        "script": SCRIPT_EP_04
    }
]

async def run_all():
    print("=" * 70)
    print("Iniciando regeneración de los 4 Deep Dives con sIA Storytelling 4.0...")
    print("=" * 70)
    
    for idx, cfg in enumerate(DEEPDIVES_CONFIG, 1):
        print(f"\n[{idx}/4] Sintetizando: {cfg['title']}...")
        out = await process_dialogue(
            script_text=cfg["script"],
            episode_title=cfg["title"],
            custom_filename=cfg["slug"],
            episode_description=cfg["desc"]
        )
        print(f"  [OK] Generado con éxito: {out}")
    
    print("\n" + "=" * 70)
    print("✅ ¡Los 4 episodios sIA Deep Dive fueron reconstruidos con Storytelling 4.0!")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(run_all())
