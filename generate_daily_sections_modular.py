"""
sIA Modular Daily Generator: Un Capítulo (Episodio en Spotify) por Sección
Formato Narrativo sIA 4.0:
1. Apertura y Brújula de Sección: Declaración explícita del show y la vertical.
2. Resumen Ejecutivo & Tesis: Problema de fondo, tesis central y hoja de ruta.
3. Despegue ("Alcanzarnos"): Inmersión directa al debate de ingeniería entre Jorge y Dalia.
4. Fuera de la Burbuja: Dosis implacable de realidad, física, matemáticas o neurociencia.
5. Veredicto Conclusivo & Embudo Multicanal (Blog técnico + Reel de 45s).
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
[CHAPTER: Apertura & Brújula: sIA IA y Agentes Autónomos]
JORGE: Bienvenidos a sIA Podcast. Hoy abrimos nuestra sección de Inteligencia Artificial y Sistemas Agénticos para desmontar uno de los mitos más extendidos entre los desarrolladores: ¿realmente los modelos ligeros de lenguaje son inservibles para tareas complejas?
DALIA: Así es, Jorge. En este episodio analizamos el fenómeno de Gemini Flash y la orquestación de agentes de alta velocidad. La tesis de hoy es contundente: el noventa por ciento de las quejas contra modelos sub-doscientos milisegundos no se deben a fallas del modelo, sino a arquitecturas de prompting deficientes que esperan razonamiento deliberativo de una unidad de procesamiento de estado.
JORGE: En los próximos minutos vamos a desarmar cómo estructurar prompts tipados con Pydantic para exprimir Flash al máximo, y en nuestra cápsula Fuera de la Burbuja exploraremos la computación neuromórfica en silicio, donde chips inspirados en el cerebro operan con menos de un milivatio de energía.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, arranquemos por esa queja recurrente en las comunidades de código. ¿Por qué tantos desarrolladores se frustran al usar modelos ultrarrápidos?

[CHAPTER: Noticia Central: El Mito de Gemini Flash y Prompt Engineering]
JORGE: Es un error básico de encuadre arquitectónico, Dalia. El fin de semana estalló un debate masivo en r diagonal google_antigravity sobre desarrolladores que envían un prompt ambiguo y abierto a un modelo sub-doscientos milisegundos como Gemini Flash, esperando que razone diez pasos abstractos como si fuera Claude tres punto cinco Sonnet. Y cuando el modelo responde de forma concisa o falla en un caso de borde, declaran en foros que no sirve para nada.
DALIA: Hay que entender la arquitectura. Gemini Flash no es un oráculo lento de razonamiento monolítico; es una unidad de procesamiento de estado de altísima velocidad y costo microscópico. En producción, su rol es clasificar intenciones, enrutar peticiones entre microservicios y extraer datos en esquemas JSON estrictamente tipados con Pydantic o TypeSafe.
JORGE: Si alimentas a Flash con un prompt de sistema determinista, pocos ejemplos claros y aprovechas Context Caching para no recomputar la matriz de atención en cada llamada, el desempeño es brutal.
DALIA: Usa modelos pesados únicamente cuando el costo de un fallo sea inaceptable; pero para la orquestación masiva y el flujo continuo en tiempo real, dominar el prompting estructurado sobre modelos rápidos como Flash es la verdadera ventaja competitiva.

[CHAPTER: 🌌 Fuera de la Burbuja: Micro-Redes Neuromórficas en Silicio]
JORGE: Y habiendo analizado la optimización de prompts en producción, es momento de romper la burbuja del algoritmo con nuestra ventana disruptiva de hoy.
DALIA: Demos un salto cuántico hacia la computación neuromórfica en silicio. Mientras toda la industria comercial sigue compitiendo por quién construye el clúster de GPUs más gigante consumiendo megavatios en la nube, en los laboratorios de microelectrónica se perfeccionan las Spiking Neural Networks o redes neuronales por impulsos.
JORGE: El cerebro humano no procesa datos con un reloj de cuatro gigahercios transmitiendo ceros y unos continuamente. Nuestras neuronas permanecen en reposo consumiendo casi nada de energía hasta que reciben un estímulo específico; solo entonces disparan una espiga eléctrica a través de sus sinapsis.
DALIA: Chips neuromórficos como Intel Loihi o BrainChip copian exactamente ese principio físico. En lugar de multiplicar matrices de punto flotante en silicio ardiente, tienen neuronas analógicas que solo se activan cuando hay un cambio relevante en el entorno.
JORGE: ¿El resultado? Modelos de visión o detección de anomalías operando con menos de un milivatio. Sensores inteligentes que pueden funcionar durante diez años con una pila de botón en campos agrícolas remotos o implantes médicos, tomando decisiones al instante sin tocar la nube. La verdadera inteligencia artificial no siempre es más grande; muchas veces consiste en imitar la eficiencia energética de la naturaleza.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
DALIA: Veredicto técnico: diseña tus enjambres desacoplando razonamiento pesado de ejecución rápida con Flash, y vigila de cerca la arquitectura neuromórfica para edge computing.
JORGE: Puedes consultar el artículo técnico completo con diagramas Mermaid y referencias APA en escucha-sia punto github punto io.
DALIA: Y en nuestras redes ya tienes disponible el Reel vertical animado de cuarenta y cinco segundos con la comparativa de latencia. ¡Nos escuchamos en el siguiente sIA Focus!
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
[CHAPTER: Apertura & Brújula: sIA Datos y Cloud Engineering]
JORGE: Bienvenidos a sIA Podcast. Hoy encendemos los motores de nuestra sección de Data Engineering y Cloud para enfrentar el mayor dolor de cabeza de los equipos analíticos: ¿por qué los pipelines de datos siguen rompiéndose a las tres de la mañana?
DALIA: Así es, Jorge. En este episodio desmenuzamos los Data Contracts semánticos. La tesis de hoy es que los datos deben tratarse como un producto de software de primera clase: si una mutación inadvertida de esquema destruye un tablero en producción, la culpa no es del almacén analítico, sino de la falta de contratos declarativos en YAML ejecutados en CI/CD.
JORGE: En los próximos minutos vamos a entender cómo blindar la ingesta en BigQuery y Snowflake mediante validaciones automáticas y desvíos a Dead Letter Queue. Y en nuestra ventana Fuera de la Burbuja entraremos a la Criptografía Homomórfica Completa, la tecnología matemática que permite consultar bases de datos en la nube sin descifrar jamás la información en memoria.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, ¿cómo pasamos de tener documentos pasivos en Notion a contratos ejecutables que frenan mutaciones silenciosas?

[CHAPTER: Noticia Central: Contratos de Datos y Desacoplamiento Semántico]
JORGE: Tratando al esquema como código en Git, Dalia. Durante años, los equipos de datos vivieron bajo el terror de que un desarrollador de backend cambiara una columna transaccional de entero a cadena de texto, rompiendo todos los modelos dbt a las tres de la mañana.
DALIA: Exacto. Un Data Contract ya no es un memorando en Notion; es una especificación ejecutable en YAML que valida esquemas, restricciones de tipo, frescura de datos y métricas de negocio antes de permitir la ingesta al lago de datos. Si una columna muta sin aviso, el contrato falla en el pipeline de CI/CD exactamente como una prueba unitaria de software.
JORGE: Y a esto se suma el desacoplamiento semántico. Definir métricas como código versionado mediante herramientas como dbt Semantic Layer permite que cualquier consumidor, ya sea un tablero de Looker, una consulta SQL ad-hoc o un agente autónomo de IA, comparta exactamente la misma definición de negocio sin quedar atrapado en el vendor lock-in de un solo almacén.

[CHAPTER: 🌌 Fuera de la Burbuja: Criptografía Homomórfica Completa en Memoria]
DALIA: Y pasando de la gobernanza de esquemas a la frontera de la seguridad de datos, abramos nuestra cápsula Fuera de la Burbuja.
JORGE: Hablemos de la Criptografía Homomórfica Completa, conocida como F H E. Históricamente, si querías hacer una consulta SQL o entrenar un modelo analítico sobre datos confidenciales, como historiales médicos o transacciones bancarias, estabas obligado a descifrar los datos en la memoria RAM del servidor, dejándolos vulnerables a fugas de memoria o ataques de canal lateral.
DALIA: Con F H E, las leyes del álgebra matemática permiten realizar operaciones aritméticas directamente sobre los datos cifrados. El servidor ejecuta sumas, promedios y agrupaciones sobre texto cifrado ilegible, produciendo un resultado cifrado que solo el cliente con su clave privada puede descifrar.
JORGE: Aunque tradicionalmente era prohibitivamente lento, los nuevos aceleradores de hardware dedicados y bibliotecas de vectores lattice están reduciendo la penalización a menos de diez veces el tiempo convencional. Esto abre la puerta a un mundo donde las empresas pueden procesar información ultra-sensible en nubes públicas sin confiar ciegamente en el proveedor de infraestructura. Privacidad matemática absoluta por diseño.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
DALIA: Veredicto técnico: no aceptes datos en tus almacenes analíticos sin un contrato YAML versionado en CI/CD que proteja a tus consumidores de negocio.
JORGE: Encuentra el contrato de datos de ejemplo en YAML y las referencias en formato APA en nuestro portal técnico en escucha-sia punto github punto io.
DALIA: Y si quieres ver la simulación animada del YAML Gate y la Dead Letter Queue, revisa el Reel vertical de cuarenta y cinco segundos en nuestras redes. ¡Nos escuchamos en el siguiente sIA Focus!
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
[CHAPTER: Apertura & Brújula: sIA Soberanía Tecnológica y Hardware]
JORGE: Bienvenidos a sIA Podcast. Hoy abrimos nuestra sección de Soberanía Tecnológica y Hardware Libre para abordar una verdad incómoda de la era digital: cuando compras un libro electrónico en plataformas corporativas, ¿realmente eres dueño de algo?
DALIA: Así es, Jorge. En este episodio analizamos el endurecimiento del DRM en los principales ecosistemas de lectura digital. La tesis de hoy es clara: depender de licencias en la nube secuestra tu biblioteca personal, y la resistencia pasa por el software libre como Calibre y dispositivos abiertos con KOReader que sincronizan directamente con Obsidian.
JORGE: En los próximos minutos desarmaremos el flujo de respaldo local en NAS y formatos abiertos como EPUB, y en nuestra cápsula Fuera de la Burbuja exploraremos la electrohumectación, una tecnología electroquímica que promete pantallas reflectivas a sesenta cuadros por segundo bajo el sol del mediodía.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, arranquemos por el susto que se llevaron miles de lectores cuando las grandes tiendas bloquearon la descarga directa por cable...

[CHAPTER: Noticia Central: El Cierre de DRM y la Resistencia con Calibre]
JORGE: Es un tema que toca una fibra muy profunda, Dalia. Muchos usuarios descubren con amargura que al comprar un cómic o libro digital no son dueños del archivo; cuando la tienda cambia sus políticas o bloquea la descarga por cable, su biblioteca queda secuestrada dentro de una aplicación cerrada que la empresa puede revocar a distancia.
DALIA: Por eso el software libre como Calibre y los dispositivos de tinta electrónica abiertos cobran un protagonismo histórico. Calibre no es solo un organizador; es la herramienta que permite a desarrolladores e investigadores indexar, convertir y preservar sus bibliotecas en formatos abiertos como EPUB o CBZ, respaldados localmente en sus propios discos duros o servidores NAS.
JORGE: Y cuando combinas Calibre con sistemas abiertos como KOReader en lectores Android o Kobo, tienes sincronización inalámbrica de anotaciones directamente hacia tu segundo cerebro en Obsidian o Notion. La tecnología debe empoderar al usuario, no convertirlo en un rehén de licencias temporales.

[CHAPTER: 🌌 Fuera de la Burbuja: Pantallas Reflectivas por Electrohumectación a 60 fps]
DALIA: Y de la tinta electrónica bistable pasamos a la física de pantallas en nuestra cápsula Fuera de la Burbuja.
JORGE: ¿Por qué la tinta electrónica tradicional es tan lenta para reproducir video? Porque depende de partículas de pigmento físicas cargadas eléctricamente que deben viajar lentamente a través de microcápsulas de fluido viscoso.
DALIA: En contraste, la tecnología de electrohumectación o electrowetting displays rompe ese cuello de botella. En lugar de mover partículas sólidas, modula el ángulo de contacto de microgotas de aceite coloreado y agua mediante campos electrostáticos microscópicos.
JORGE: Al aplicar voltaje, la gota de aceite se retrae en microsegundos, revelando una superficie blanca reflectiva subyacente. Esto permite alcanzar tasas de refresco fluidas de sesenta cuadros por segundo a pleno sol, con color brillante y sin emitir luz dañina para los ojos ni requerir retroiluminación. Una tecnología que promete pantallas tan fluidas como un panel OLED pero tan legibles y eficientes como una hoja de papel bajo el sol del mediodía.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
DALIA: Veredicto de soberanía: mantén siempre una copia local de tus libros en EPUB sin DRM y no delegues tu biblioteca intelectual a la nube de un tercero.
JORGE: Si quieres ver las especificaciones ópticas de electrohumectación y la guía de configuración de Calibre, revisa el artículo en escucha-sia punto github punto io.
DALIA: Y en nuestras redes ya tienes disponible el Reel vertical de cuarenta y cinco segundos con la animación de microcápsulas E-Ink. ¡Nos escuchamos en el siguiente sIA Focus!
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
[CHAPTER: Apertura & Brújula: sIA Fabricación Digital y Cultura Maker]
JORGE: Bienvenidos a sIA Podcast. Hoy abrimos nuestra sección de Fabricación Digital y Cultura Maker para resolver un reto crítico de ingeniería: ¿cómo lograr tolerancias dimensionales exactas en piezas mecánicas impresas a alta velocidad?
DALIA: Así es, Jorge. En este episodio ponemos bajo la lupa la impresión tres D de filamentos técnicos como PETG con fibra de carbono en impresoras de quinientos milímetros por segundo. La tesis de hoy es que imprimir rápido sin calibración activa es una receta para el desastre: esquinas deformadas, delaminación y rodamientos que jamás encajan.
JORGE: En los próximos minutos analizaremos cómo el sensor Micro-LiDAR de siete micrómetros y la compensación de Pressure Advance en OrcaSlicer resuelven la histéresis de presión del polímero. Y en Fuera de la Burbuja entraremos a la Impresión cuatro D: polímeros con memoria térmica que cambian de forma con la temperatura ambiental.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, arranquemos por la física del filamento. ¿Por qué el PETG se comporta de forma tan caprichosa frente al PLA tradicional?

[CHAPTER: Noticia Central: Tolerancias y Flujo en PETG con Bambu Lab]
JORGE: Es un tema de viscosidad y reología del polímero, Dalia. El PETG es el caballo de batalla para piezas funcionales debido a su resistencia al impacto y tolerancia térmica. Sin embargo, su tendencia al hilo y la sobreextrusión en esquinas cerradas arruina cualquier ensamblaje mecánico si no calibras con precisión.
DALIA: En el software de laminado OrcaSlicer y Bambu Studio, la clave reside en calibrar dos parámetros críticos: la compensación de flujo dinámico y la retracción fina. Activar el Pressure Advance con el sensor Micro-LiDAR permite ecualizar la presión en la boquilla antes de las aceleraciones bruscas, evitando esquinas hinchadas y asegurando que los orificios para tornillos M tres o rodamientos encajen a la primera sin post-procesado manual.

[CHAPTER: 🌌 Fuera de la Burbuja: Impresión 4D con Polímeros de Memoria Térmica]
JORGE: Y pasando de la geometría estática tradicional, entremos en la fascinante dimensión de la Impresión cuatro D en nuestra cápsula Fuera de la Burbuja.
DALIA: ¿Qué es la impresión cuatro D? Es la fabricación aditiva donde la cuarta dimensión es el tiempo y la respuesta ambiental. La pieza impresa no mantiene una forma rígida para siempre; contiene polímeros con memoria de forma térmica programada en su microestructura.
JORGE: Imaginen imprimir una estructura plana que, al ser sumergida en agua a cuarenta grados centígrados o recibir calor ambiental, se pliega automáticamente sobre sí misma para convertirse en un mecanismo robótico o una pinza mecánica sin motores, cables ni actuadores electrónicos.
DALIA: Esta tecnología se está aplicando en stents médicos autorreplegables que se expanden dentro de vasos sanguíneos con la temperatura corporal, y en paneles aeroespaciales que se despliegan en el vacío espacial al recibir la radiación solar. No es ciencia ficción; es el poder de la física de materiales programada directamente en el código G de laminado.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
JORGE: Veredicto técnico: no imprimas piezas mecánicas a ciegas; calibra el Pressure Advance con metrología activa y aprovecha los nuevos compuestos con memoria de forma.
DALIA: Todos los parámetros de laminado y los papers de polímeros térmicos están detallados en nuestro artículo web en escucha-sia punto github punto io.
JORGE: Y en nuestras redes ya tienes disponible el Reel vertical de cuarenta y cinco segundos con la animación del escaneo láser Micro-LiDAR. ¡Nos escuchamos en el siguiente sIA Focus!
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
[CHAPTER: Apertura & Brújula: sIA Cultura Geek y Hard Sci-Fi]
JORGE: Bienvenidos a sIA Podcast. Hoy cerramos nuestra serie abriendo la sección de Cultura Geek y Hard Sci-Fi para explorar los límites de la mente humana: ¿qué mecanismos narrativos hacen que una historia nos despoje de la certidumbre y qué tan lejos estamos de la inmersión cerebral total?
DALIA: Así es, Jorge. En este episodio deconstruimos la literatura de horror psicológico contemporáneo y el fenómeno del aislamiento espacial. La tesis central es que el verdadero terror no proviene de monstruos explícitos, sino del colapso gradual del control sobre el entorno, una tensión idéntica a la que enfrentan los astronautas o exploradores en sistemas cerrados.
JORGE: En los próximos minutos analizaremos esa arquitectura narrativa, y en nuestra ventana Fuera de la Burbuja desnudaremos la neurociencia del Full-Dive VR: qué se necesita a nivel de corteza somatosensorial y estimulación magnética para proyectar la consciencia en un mundo virtual sin mover un solo músculo real.
DALIA: Dicho esto, alcancemos el meollo del debate: Jorge, ¿por qué los relatos que deconstruyen espacios cotidianos nos perturban tanto más que el terror convencional?

[CHAPTER: Noticia Central: Deconstrucción del Horror y Tensión Psicológica]
JORGE: Porque juegan con la pérdida de certidumbre espacial, Dalia. Lo que hace fascinante a la literatura de horror actual en foros como horrorlit no son los sustos baratos, sino la maestría para manejar el aislamiento y la descomposición gradual de las leyes de la física cotidiana. Autores que deconstruyen casas embrujadas o estaciones remotas utilizan la arquitectura física como un espejo de la psique humana.
DALIA: Es la misma tensión narrativa que vemos en las grandes obras de ciencia ficción dura: obligar al protagonista y al lector a enfrentar las consecuencias existenciales de sistemas tecnológicos que escapan a su control, transformando el misterio en una experiencia inmersiva inolvidable.

[CHAPTER: 🌌 Fuera de la Burbuja: La Neurociencia Real del Full-Dive VR]
JORGE: Y hablando de inmersión total en mundos alternativos, abramos nuestra última cápsula Fuera de la Burbuja de hoy: la neurociencia real del Full-Dive VR.
DALIA: Desde novelas ligeras como Sword Art Online hasta los tratados de filosofía de la mente de Peter Watts, la fantasía del Full-Dive es desconectar los sentidos biológicos del cuerpo físico y proyectar la consciencia directamente en un entorno virtual sintético.
JORGE: ¿Qué tan cerca estamos biológicamente de esto? Los cascos de realidad virtual actuales solo engañan a la vista y al oído. Pero lograr inmersión somatosensorial completa, sentir la brisa, el peso de un objeto o la textura de una superficie sin tocarla físicamente, requiere interactuar con el tálamo y la corteza somatosensorial.
DALIA: Los experimentos de estimulación magnética transcraneal focalizada y las interfaces cerebro-computadora no invasivas demuestran que es posible inducir sensaciones táctiles artificiales con pulsos electromagnéticos de alta precisión. Sin embargo, el gran reto de seguridad biofísica no es escribir sensaciones en el cerebro, sino el motor de interrupción: bloquear de forma reversible la señal motora eferente para que el usuario no se mueva en el mundo real mientras corre en el entorno virtual.
JORGE: Un dilema fascinante donde la ingeniería de software, la ética médica y la neurología convergen para explorar qué significa realmente la experiencia de estar vivo en una era digital.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
DALIA: Con este viaje a la frontera de la mente cerramos nuestra entrega modular de hoy.
JORGE: Recuerda que cada sección tiene su propio artículo técnico y referencias académicas en escucha-sia punto github punto io.
DALIA: Y en nuestras redes ya tienes disponibles los Reels animados de cada episodio. ¡Muchísimas gracias por acompañarnos y nos escuchamos en la próxima edición de sIA Podcast!
"""
    }
]

async def generate_all_sections():
    print("=" * 70)
    print("🚀 RECONSTRUYENDO 5 CAPÍTULOS MODULARES CON FORMATO NARRATIVO sIA 4.0")
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
    print("✅ ¡LOS 5 CAPÍTULOS MODULARES FUERON REGENERADOS EXITOSAMENTE!")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(generate_all_sections())
