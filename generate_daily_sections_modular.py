"""
sIA Modular Daily Generator: Un Capítulo (Episodio en Spotify) por Sección
Cada sección es un producto unitario de 5 a 6 minutos:
1. Noticia central / debate técnico en la burbuja
2. Cápsula Fuera de la Burbuja
"""

import sys
import os
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")

SECTIONS = [
    {
        "id": "34_ia_agentes",
        "title": "sIA #34: IA & Agentes — El Mito de Gemini Flash y 🌌 Redes Neuromórficas en Silicio",
        "filename": "sIA_Daily_S01_IA_Gemini_Flash_Neuromorfico_2026-10-12.mp3",
        "category": "sIA Focus: IA & Agentes",
        "badge_color": "cyan",
        "read_time": "6 min",
        "reel_video": "sIA_Reel_02_Mito_Gemini_Flash.mp4",
        "script": """
[CHAPTER: Noticia Central: El Mito de Gemini Flash y Prompt Engineering]
JORGE: ¡Muy buenos días a toda nuestra comunidad técnica! Bienvenidos a sIA Focus, tu cápsula técnica de seis minutos para el camino. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es lunes doce de octubre de dos mil veintiséis, y en este capítulo nos sumergimos de lleno en la Inteligencia Artificial y la orquestación de agentes autónomos.
JORGE: El fin de semana estalló un debate masivo en r diagonal google_antigravity con una publicación titulada: Opinión impopular: el noventa por ciento del odio hacia modelos ligeros como Gemini Flash proviene de desarrolladores que no saben usarlos o fanboys corporativos.
DALIA: Es una queja constante, Jorge. Desarrolladores que envían un prompt ambiguo y abierto a un modelo sub-doscientos milisegundos como Gemini Flash, esperando que razone diez pasos abstractos como si fuera Claude tres punto cinco Sonnet. Y cuando el modelo responde de forma concisa o falla en un caso de borde, declaran en foros que el modelo no sirve para nada.
JORGE: Hay que entender la arquitectura. Gemini Flash no es un oráculo lento de razonamiento monolítico; es una unidad de procesamiento de estado de altísima velocidad y costo microscópico. En producción, su rol es clasificar intenciones, enrutar peticiones entre microservicios y extraer datos en esquemas JSON estrictamente tipados con Pydantic o TypeSafe.
DALIA: Totalmente. Si alimentas a Flash con un prompt de sistema determinista, pocos ejemplos claros y aprovechas Context Caching para no recomputar la matriz de atención en cada llamada, el desempeño es brutal. Usa modelos pesados únicamente cuando el costo de un fallo sea inaceptable; pero para la orquestación masiva y el flujo continuo en tiempo real, dominar el prompting estructurado sobre modelos rápidos como Flash es la verdadera ventaja competitiva.

[CHAPTER: 🌌 Fuera de la Burbuja: Micro-Redes Neuromórficas en Silicio]
JORGE: Y habiendo analizado la optimización de prompts en producción, es momento de romper la burbuja del algoritmo con nuestra ventana disruptiva de hoy.
DALIA: Demos un salto cuántico hacia la computación neuromórfica en silicio. Mientras toda la industria comercial sigue compitiendo por quién construye el clúster de GPUs más gigante consumiendo megavatios en la nube, en los laboratorios de microelectrónica se perfeccionan las Spiking Neural Networks o redes neuronales por impulsos.
JORGE: El cerebro humano no procesa datos con un reloj de cuatro gigahercios transmitiendo ceros y unos continuamente. Nuestras neuronas permanecen en reposo consumiendo casi nada de energía hasta que reciben un estímulo específico; solo entonces disparan una espiga eléctrica a través de sus sinapsis.
DALIA: Chips neuromórficos como Intel Loihi o BrainChip copian exactamente ese principio físico. En lugar de multiplicar matrices de punto flotante en silicio ardiente, tienen neuronas analógicas que solo se activan cuando hay un cambio relevante en el entorno.
JORGE: ¿El resultado? Modelos de visión o detección de anomalías operando con menos de un milivatio. Sensores inteligentes que pueden funcionar durante diez años con una pila de botón en campos agrícolas remotos o implantes médicos, tomando decisiones al instante sin tocar la nube. La verdadera inteligencia artificial no siempre es más grande; muchas veces consiste en imitar la eficiencia energética de la naturaleza.

[CHAPTER: Cierre & Recursos]
DALIA: Recuerda que puedes consultar el artículo técnico completo con diagramas Mermaid y referencias APA en escucha-sia punto github punto io.
JORGE: Y en nuestras redes y canal de Spotify ya tienes disponible el Reel vertical animado de cuarenta y cinco segundos de esta entrega. ¡Nos escuchamos en el siguiente sIA Focus!
"""
    },
    {
        "id": "35_data_cloud",
        "title": "sIA #35: Data & Cloud — Contratos Semánticos en YAML y 🌌 Criptografía Homomórfica en Memoria",
        "filename": "sIA_Daily_S02_Data_Contratos_Semanticos_FHE_2026-10-12.mp3",
        "category": "sIA Focus: Datos & Cloud",
        "badge_color": "blue",
        "read_time": "6 min",
        "reel_video": None,
        "script": """
[CHAPTER: Noticia Central: Contratos de Datos y Desacoplamiento Semántico]
JORGE: ¡Bienvenidos a sIA Focus: Datos y Cloud! Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy abordamos uno de los dolores de cabeza más caros de la ingeniería de datos: la fragilidad de los pipelines analíticos ante mutaciones silenciosas de esquema.
JORGE: La tendencia arquitectónica definitiva de este año es tratar a los datos como un producto de software formal a través de Data Contracts. Durante años, los equipos vivieron bajo el terror de que un cambio en una columna transaccional rompiera todos los tableros en BigQuery o Snowflake a las tres de la mañana.
DALIA: Exacto. Un Data Contract ya no es un documento pasivo en Notion; es una especificación ejecutable en YAML que valida esquemas, restricciones de tipo, frescura de datos y métricas de negocio antes de permitir la ingesta al lago de datos. Si una columna cambia de entero a flotante, el contrato falla en el pipeline de CI/CD, exactamente como una prueba unitaria de software.
JORGE: Y a esto se suma el desacoplamiento semántico. Definir métricas como código versionado en Git mediante herramientas como d b t Semantic Layer permite que cualquier consumidor, ya sea un tablero de Looker, una consulta SQL ad-hoc o un agente autónomo de Google Antigravity, comparta exactamente la misma definición de negocio sin quedar atrapado en el vendor lock-in de un solo almacén.

[CHAPTER: 🌌 Fuera de la Burbuja: Criptografía Homomórfica Completa en Memoria]
DALIA: Y pasando de la gobernanza de esquemas a la frontera de la seguridad de datos, abramos nuestra cápsula Fuera de la Burbuja.
JORGE: Hablemos de la Criptografía Homomórfica Completa, conocida como F H E. Históricamente, si querías hacer una consulta SQL o entrenar un modelo analítico sobre datos confidenciales, como historiales médicos o transacciones bancarias, estabas obligado a descifrar los datos en la memoria RAM del servidor, dejándolos vulnerables a fugas de memoria o ataques de canal lateral.
DALIA: Con F H E, las leyes del álgebra matemática permiten realizar operaciones aritméticas directamente sobre los datos cifrados. El servidor ejecuta sumas, promedios y agrupaciones sobre texto cifrado ilegible, produciendo un resultado cifrado que solo el cliente con su clave privada puede descifrar.
JORGE: Aunque tradicionalmente era prohibitivamente lento, los nuevos aceleradores de hardware dedicados y bibliotecas de vectores lattice están reduciendo la penalización a menos de diez veces el tiempo convencional. Esto abre la puerta a un mundo donde las empresas pueden procesar información ultra-sensible en nubes públicas sin confiar ciegamente en el proveedor de infraestructura. Privacidad matemática absoluta por diseño.

[CHAPTER: Cierre & Recursos]
DALIA: Encuentra el contrato de datos de ejemplo en YAML y las referencias en formato APA en nuestro portal sIA Journal.
JORGE: ¡Acompáñanos en el siguiente episodio para adentrarnos en la soberanía del hardware y los libros electrónicos!
"""
    },
    {
        "id": "36_hardware_gadgets",
        "title": "sIA #36: Hardware & Soberanía — El Cierre de DRM en E-Readers y 🌌 Pantallas Electroquímicas a 60 fps",
        "filename": "sIA_Daily_S03_Hardware_Calibre_DRM_Electroquimica_2026-10-12.mp3",
        "category": "sIA Focus: Hardware & Gadgets",
        "badge_color": "cyan",
        "read_time": "6 min",
        "reel_video": None,
        "script": """
[CHAPTER: Noticia Central: El Cierre de DRM y la Resistencia con Calibre]
JORGE: ¡Bienvenidos a sIA Focus: Hardware, Lectura Digital y Soberanía Tecnológica! Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy analizamos el encendido debate en r diagonal Calibre y comunidades de tinta electrónica sobre el endurecimiento de formatos propietarios y DRM por parte de grandes plataformas de libros electrónicos.
JORGE: Es un tema que toca una fibra muy profunda. Muchos usuarios descubren con amargura que al comprar un cómic o libro digital no son dueños del archivo; cuando la tienda cambia sus políticas o bloquea la descarga directa por cable a la computadora, su biblioteca queda secuestrada dentro de una aplicación cerrada.
DALIA: Por eso el software libre como Calibre y los dispositivos de tinta electrónica abiertos cobran un protagonismo histórico. Calibre no es solo un organizador; es la herramienta que permite a desarrolladores e investigadores indexar, convertir y preservar sus bibliotecas en formatos abiertos como EPUB o CBZ, respaldados localmente en sus propios discos duros o servidores NAS.
JORGE: Y cuando combinas Calibre con sistemas abiertos como KOReader en lectores Android o Kobo, tienes sincronización inalámbrica de anotaciones directamente hacia tu segundo cerebro en Obsidian o Notion. La tecnología debe empoderar al usuario, no convertirlo en un rehén de licencias temporales.

[CHAPTER: 🌌 Fuera de la Burbuja: Pantallas Reflectivas por Electrohumectación a 60 fps]
DALIA: Y de la tinta electrónica bistable pasamos a la física de pantallas en nuestra cápsula Fuera de la Burbuja.
JORGE: ¿Por qué la tinta electrónica tradicional es tan lenta para reproducir video? Porque depende de partículas de pigmento físicas cargadas eléctricamente que deben viajar lentamente a través de microcápsulas de fluido viscoso.
DALIA: En contraste, la tecnología de electrohumectación o electrowetting displays rompe ese cuello de botella. En lugar de mover partículas sólidas, modula el ángulo de contacto de microgotas de aceite coloreado y agua mediante campos electrostáticos microscópicos.
JORGE: Al aplicar voltaje, la gota de aceite se retrae en microsegundos, revelando una superficie blanca reflectiva subyacente. Esto permite alcanzar tasas de refresco fluidas de sesenta cuadros por segundo a pleno sol, con color brillante y sin emitir luz dañina para los ojos ni requerir retroiluminación. Una tecnología que promete pantallas tan fluidas como un panel OLED pero tan legibles y eficientes como una hoja de papel bajo el sol del mediodía.

[CHAPTER: Cierre & Recursos]
DALIA: Si quieres ver las especificaciones ópticas y los esquemas de flujo, revisa el artículo complementario en nuestra revista técnica.
JORGE: ¡Nos vemos en el próximo bloque dedicado a la fabricación aditiva y el mundo maker!
"""
    },
    {
        "id": "37_maker_3d",
        "title": "sIA #37: Maker & 3D — Tolerancias en PETG con Bambu Lab y 🌌 Impresión 4D con Memoria Térmica",
        "filename": "sIA_Daily_S04_Maker_3D_Bambu_Polimeros4D_2026-10-12.mp3",
        "category": "sIA Focus: Maker & 3D",
        "badge_color": "emerald",
        "read_time": "6 min",
        "reel_video": None,
        "script": """
[CHAPTER: Noticia Central: Tolerancias y Flujo en PETG con Bambu Lab]
JORGE: ¡Bienvenidos a sIA Focus: Fabricación Aditiva y Cultura Maker! Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy ponemos la lupa sobre la ingeniería de impresión tres D, donde la comunidad técnica en r diagonal BambuLab y r diagonal 3Dprinting debate las claves para obtener piezas mecánicas en PETG con tolerancias dimensionales exactas.
JORGE: El filamento PETG es el caballo de batalla para piezas funcionales debido a su resistencia al impacto y tolerancia térmica. Sin embargo, su tendencia al hilo o stringing y la adhesión excesiva a placas texturizadas PEI sigue frustrando a muchos creadores.
DALIA: En el software de laminado OrcaSlicer y Bambu Studio, la clave reside en calibrar dos parámetros críticos: la compensación de flujo dinámico y la retracción fina. Activar el Pressure Advance con el sensor micro-lidar permite ecualizar la presión en la boquilla antes de los giros cerrados, evitando esquinas hinchadas y asegurando que los orificios para tornillos M tres o rodamientos encajen a la primera sin post-procesado manual.

[CHAPTER: 🌌 Fuera de la Burbuja: Impresión 4D con Polímeros de Memoria Térmica]
JORGE: Y pasando de la geometría estática tradicional, entremos en la fascinante dimensión de la Impresión cuatro D en nuestra cápsula Fuera de la Burbuja.
DALIA: ¿Qué es la impresión cuatro D? Es la fabricación aditiva donde la cuarta dimensión es el tiempo y la respuesta ambiental. La pieza impresa no mantiene una forma rígida para siempre; contiene polímeros con memoria de forma térmica programada en su microestructura.
JORGE: Imaginen imprimir una estructura plana que, al ser sumergida en agua a cuarenta grados centígrados o recibir calor ambiental, se pliega automáticamente sobre sí misma para convertirse en un mecanismo robótico o una pinza mecánica sin motores, cables ni actuadores electrónicos.
DALIA: Esta tecnología se está aplicando en stents médicos autorreplegables que se expanden dentro de vasos sanguíneos con la temperatura corporal, y en paneles aeroespaciales que se despliegan en el vacío espacial al recibir la radiación solar. No es ciencia ficción; es el poder de la física de materiales programada directamente en el código G de laminado.

[CHAPTER: Cierre & Recursos]
JORGE: Todos los parámetros de laminado y los papers de polímeros térmicos están detallados en nuestro artículo web.
DALIA: ¡Nos escuchamos en el último episodio del día con ciencia ficción y narrativa geek!
"""
    },
    {
        "id": "38_geek_scifi",
        "title": "sIA #38: Cultura Geek — La Deconstrucción del Horror Psicológico y 🌌 Neurociencia del Full-Dive VR",
        "filename": "sIA_Daily_S05_Geek_Horror_FullDive_VR_2026-10-12.mp3",
        "category": "sIA Focus: Cultura Geek & Sci-Fi",
        "badge_color": "purple",
        "read_time": "6 min",
        "reel_video": None,
        "script": """
[CHAPTER: Noticia Central: Deconstrucción del Horror y Tensión Psicológica]
JORGE: ¡Bienvenidos a sIA Focus: Cultura Geek, Narrativa y Hard Sci-Fi! Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy cerramos la jornada analizando los debates en r diagonal horrorlit sobre la obra de autores contemporáneos como Darcy Coates y la evolución del suspenso psicológico frente al terror convencional.
JORGE: Lo que hace fascinante a la literatura de horror actual no son los monstruos explícitos, sino la maestría para manejar el aislamiento espacial y la descomposición gradual de la certidumbre. Autores que deconstruyen casas embrujadas o estaciones remotas utilizan la arquitectura física como un espejo de la psique humana.
DALIA: Es la misma tensión narrativa que vemos en las grandes obras de ciencia ficción dura: obligar al protagonista y al lector a enfrentar las consecuencias existenciales de sistemas tecnológicos que escapan a su control, transformando el misterio en una experiencia inmersiva inolvidable.

[CHAPTER: 🌌 Fuera de la Burbuja: La Neurociencia Real del Full-Dive VR]
JORGE: Y hablando de inmersión total en mundos alternativos, abramos nuestra última cápsula Fuera de la Burbuja de hoy: la neurociencia real del Full-Dive VR.
DALIA: Desde novelas ligeras como Sword Art Online hasta los tratados de filosofía de la mente de Peter Watts, la fantasía del Full-Dive es desconectar los sentidos biológicos del cuerpo físico y proyectar la consciencia directamente en un entorno virtual sintético.
JORGE: ¿Qué tan cerca estamos biológicamente de esto? Los cascos de realidad virtual actuales solo engañan a la vista y al oído. Pero lograr inmersión somatosensorial completa, sentir la brisa, el peso de un objeto o la textura de una superficie sin tocarla físicamente, requiere interactuar con el tálamo y la corteza somatosensorial.
DALIA: Los experimentos de estimulación magnética transcraneal focalizada y las interfaces cerebro-computadora no invasivas demuestran que es posible inducir sensaciones táctiles artificiales con pulsos electromagnéticos de alta precisión. Sin embargo, el gran reto de seguridad biofísica no es escribir sensaciones en el cerebro, sino el motor de interrupción: bloquear de forma reversible la señal motora eferente para que el usuario no se mueva en el mundo real mientras corre en el entorno virtual.
JORGE: Un dilema fascinante donde la ingeniería de software, la ética médica y la neurología convergen para explorar qué significa realmente la experiencia de estar vivo en una era digital.

[CHAPTER: Cierre & Despedida]
DALIA: Con este viaje a la frontera de la mente cerramos nuestra serie de cinco entregas modulares de sIA Focus de hoy.
JORGE: Recuerda que cada sección tiene su propio artículo técnico y referencias académicas en sIA Journal. ¡Muchísimas gracias por acompañarnos en el camino y nos escuchamos en la próxima edición!
"""
    }
]

async def generate_all_sections():
    print("=" * 70)
    print("🚀 GENERANDO 5 CAPÍTULOS MODULARES DE sIA FOCUS (EDICIÓN 12 DE OCTUBRE)")
    print("=" * 70)

    for idx, sec in enumerate(SECTIONS, 1):
        print(f"\n[{idx}/5] Procesando capítulo: {sec['title']}...")
        mp3_out = await process_dialogue(
            script_text=sec['script'],
            episode_title=sec['title'],
            custom_filename=sec['filename']
        )
        print(f"  [OK] Audio generado: {mp3_out}")

    print("\n" + "=" * 70)
    print("✅ ¡LOS 5 CAPÍTULOS MODULARES FUERON GENERADOS EXITOSAMENTE!")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(generate_all_sections())
