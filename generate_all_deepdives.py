"""
Generador Maestro de los 4 Episodios sIA Deep Dive.
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
JORGE: ¡Hola a toda nuestra audiencia! Bienvenidos a una nueva entrega de sIA Deep Dive. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy nos sumergimos de lleno en el corazón de los almacenes de datos analíticos modernos: Google Cloud BigQuery y el impacto transformador de Gemini Cloud Assist.
JORGE: Nuestra tesis de hoy es clara: la era en la que el analista o el ingeniero pasaba horas escribiendo consultas ese cu ele artesanales desde cero ha terminado. Con la integración de modelos de lenguaje directamente en el motor de ejecución, la analítica conversacional sobre grafos de metadatos se está convirtiendo en la interfaz por defecto.
DALIA: Pero cuidado, Jorge, esto no significa que el trabajo del ingeniero de datos desaparezca. Al contrario: el foco de valor se desplaza de la sintaxis ese cu ele hacia la modelación semántica y la arquitectura de gobernanza. Si las tablas no tienen metadatos limpios en Dataplex, Gemini simplemente generará consultas sobre supuestos falsos.
JORGE: Exacto Dalia. Bajo el capó, BigQuery Studio ahora utiliza Gemini no solo para autocompletar código, sino para inferir la intención del usuario a partir del esquema y del linaje de datos. Puede recomendar particionamiento por fecha, sugerir clústeres óptimos para reducir el escaneo de bytes y explicar cuellos de botella en el plan de ejecución de la consulta.
DALIA: Y aquí viene el debate crítico que todo líder técnico debe enfrentar: el riesgo de las alucinaciones silenciosas en agregaciones financieras o métricas de negocio. Si le pides a Gemini "ventas netas del último trimestre", ¿sabe el modelo cómo se descuentan las devoluciones, las notas de crédito o los impuestos locales?
JORGE: Si la empresa no definió un contrato de datos semántico o una métrica unificada en d b t, el modelo elegirá la columna que 'parezca' más lógica. Y el resultado numérico se verá impecable, pero estará financieramente equivocado. Por eso decimos que la IA no reemplaza el rigor del ingeniero; lo eleva a nivel de arquitectura y auditoría.
DALIA: Y para nuestra conexión geek de hoy: esto me recuerda a los Archivos Akáshicos y a la biblioteca de Yggdrasil en la literatura fantástica. Tener acceso a toda la información del universo no te sirve de nada si no sabes formular la pregunta con los parámetros exactos.
JORGE: Una analogía perfecta, Dalia. En BigQuery el poder de cómputo ya es casi infinito; el verdadero reto es la precisión del contexto semántico. ¡Nos escuchamos en el siguiente acto!
DALIA: ¡Hasta pronto!
"""

# ==============================================================================
# EPISODIO 2: El Fin de la Amnesia en LLMs: Context Caching y Memoria Persistente
# ==============================================================================
SCRIPT_EP_02 = """
JORGE: ¡Saludos a toda la comunidad tech! Bienvenidos a sIA Deep Dive. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy abordamos uno de los dolores de cabeza más grandes en la historia reciente de la inteligencia artificial: la amnesia crónica de los modelos de lenguaje y cómo finalmente la estamos superando.
JORGE: La tesis central de este episodio es que la ventana de contexto estática y sin memoria ha quedado obsoleta. Con la llegada de Context Caching en Gemini y las arquitecturas de memoria episódica jerárquica, los agentes de software finalmente pueden aprender de interacciones pasadas y conservar experiencia acumulada.
DALIA: Durante años, cada vez que abrías un chat o ejecutabas un pipeline con un LLM, el modelo sufría de amnesia total. Tenías que pagar y reenviar miles de tokens de contexto, documentación y código una y otra vez.
JORGE: Con Context Caching, la memoria de inferencia se preserva en los servidores de la nube. Puedes fijar un repositorio completo de código, las especificaciones de tu empresa o la bitácora de incidentes por una fracción mínima del costo y con una latencia de respuesta reducida hasta en un ochenta por ciento.
DALIA: Pero el verdadero salto conceptual es el aprendizaje anidado o nested learning. No se trata solo de almacenar texto, sino de estructurar la memoria en capas: memoria de trabajo para la tarea inmediata, memoria episódica para recordar errores y soluciones previas, y memoria semántica para los principios inmutables de arquitectura.
JORGE: Claro, Dalia, pero hablemos de los peligros reales: la contaminación de contexto o context poisoning. Si un agente almacena una deducción errónea en su memoria persistente y no tienes mecanismos de poda y verificación, ese error contaminará todas las decisiones futuras del sistema.
DALIA: ¡Exacto! Y aquí la conexión con la cultura geek es inevitable. En el arco de Alicization de Sword Art Online, las almas artificiales llamadas Fluctlights tenían un límite biológico de memoria de aproximadamente ciento cincuenta años; más allá de eso, la acumulación de memorias saturaba el núcleo y colapsaba la personalidad.
JORGE: ¡Qué gran referencia, Dalia! En los agentes de software de dos mil veintiséis, diseñar las políticas de olvido y consolidación de memoria es tan crítico como diseñar el almacenamiento mismo.
DALIA: Diseñar sistemas que recuerden lo esencial y descarten el ruido: esa es la verdadera maestría técnica. ¡Hasta el próximo episodio!
"""

# ==============================================================================
# EPISODIO 3: Data Mesh en Retail Masivo: Contratos Semánticos y Streaming
# ==============================================================================
SCRIPT_EP_03 = """
JORGE: ¡Hola a todos! Bienvenidos a sIA Deep Dive. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy nos adentramos en las trincheras de la alta concurrencia y el volumen masivo: Data Mesh en retail a escala global.
JORGE: La tesis que defendemos hoy es que en empresas con millones de transacciones por segundo, los almacenes monolíticos centralizados fallan no por limitaciones de hardware, sino por la fricción organizacional. Data Mesh no es un framework tecnológico; es una transformación sociocultural que trata a los datos como un producto descentralizado con contratos semánticos estrictos.
DALIA: En un gigante del retail tipo Walmart o comercio omnicanal, pretender que un solo equipo central de datos entienda la logística de almacenes, el inventario de última milla, la conciliación de pagos y los algoritmos de recomendación es una receta para el estancamiento.
JORGE: En la arquitectura Data Mesh, cada dominio de negocio es dueño de su propio producto de datos. El equipo de inventario expone un Data Product formalizado mediante contratos en d b t y esquemas estrictos de eventos en Kafka o PubSub, garantizando niveles de servicio y calidad acordados.
DALIA: Pero entremos al debate de la realidad: ¿qué pasa cuando los dominios operativos no tienen cultura de ingeniería de software? Si dejas que cada departamento cree tablas a su antojo sin un plano de control unificado, en seis meses no tienes un Data Mesh; tienes un pantano de datos fragmentado y costos de almacenamiento duplicados por diez.
JORGE: Por eso la figura del Ingeniero de Plataforma de Datos es vital. La plataforma debe ofrecer herramientas de autoservicio para que crear un pipeline, aplicar pruebas de calidad con Great Expectations y publicar métricas en BigQuery sea tan sencillo como hacer un commit en Git.
DALIA: Y para nuestra mirada geek: esto funciona idéntico a la economía de gremios en Log Horizon o los MMORPGs complejos. Si la facción de herreros cambia la aleación sin avisar al gremio de comerciantes, toda la cadena de suministro del servidor entra en caos. Los contratos de datos son las leyes inmutables del mercado.
JORGE: Sin contratos claros, no hay interoperabilidad posible. Una lección fundamental para la arquitectura moderna. ¡Nos vemos en el siguiente análisis!
DALIA: ¡Hasta la próxima!
"""

# ==============================================================================
# EPISODIO 4: Inferencia en el Borde vs Nube: NPU del Galaxy S25 e Insta360 X4
# ==============================================================================
SCRIPT_EP_04 = """
JORGE: ¡Qué tal a toda nuestra audiencia! Bienvenidos a una nueva edición de sIA Deep Dive. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy miramos hacia el hardware que llevamos en la mano y en la mochila: el silicio de inferencia local en el Galaxy ese veinticinco y la captura espacial inmersiva con la Insta tres sesenta X cuatro.
JORGE: Nuestra tesis es que la próxima frontera de la inteligencia artificial personal no se jugará en los macro centros de datos de la nube, sino en la unidad de procesamiento neuronal, la N P U, directamente en el silicio de nuestros dispositivos móviles.
DALIA: Durante años dependíamos de enviar cada instrucción, audio o imagen a través de Internet para recibir una respuesta de la IA. Pero la latencia de red, la falta de cobertura y los riesgos de privacidad hacen que ese modelo sea insostenible para la asistencia en tiempo real.
JORGE: Con los procesadores de última generación en la familia Galaxy ese veinticinco, contamos con decenas de TOPS de potencia en la N P U. Esto permite correr modelos de lenguaje reducidos y cuantizados de tres a siete mil millones de parámetros de forma completamente local, sin conexión a Internet y con consumo mínimo de energía.
DALIA: Y en movilidad, funciones como Now Brief y My FanCam en Uan U I nueve procesan la cámara y el audio localmente. Mientras tanto, en cámaras de acción como la Insta tres sesenta X cuatro, los algoritmos de visión por computadora realizan el stitching y la estabilización FlowState de video en ocho K en tiempo real utilizando aceleración por hardware.
JORGE: Pero seamos honestos en el debate técnico, Dalia: el estrangulamiento térmico o thermal throttling sigue siendo una realidad física ineludible. Si pones a un teléfono delgado a inferir modelos pesados durante veinte minutos seguidos bajo el sol, la temperatura sube y el procesador baja drásticamente su frecuencia para proteger el silicio.
DALIA: Totalmente. Por eso el futuro inmediato no es todo local ni todo en la nube, sino la arquitectura híbrida: inferencia rápida y privada en el borde para la interacción inmediata, y delegación inteligente a la nube solo cuando se requiere razonamiento ultra profundo.
JORGE: Y como paralelismo geek: pensemos en el dispositivo Augma de Sword Art Online Ordinal Scale. La magia de la realidad aumentada radicaba en que el renderizado de combate ocurría al instante en la sien del jugador, sin el retraso de esperar paquetes de red desde un servidor remoto.
DALIA: Procesar en el borde para vivir en tiempo real. Esperamos que disfruten este análisis dondequiera que nos escuchen. ¡Hasta la próxima edición de sIA Deep Dive!
JORGE: ¡Hasta la próxima y excelente jornada para todos!
"""

DEEPDIVES_CONFIG = [
    {
        "title": "sIA Deep Dive: BigQuery Gemini Cloud Assist y la Muerte de las Consultas Manuales",
        "slug": "sIA_DeepDive_BigQuery_Gemini_Cloud_Assist.mp3",
        "desc": "sIA Deep Dive: Análisis exhaustivo sobre cómo Gemini Cloud Assist en BigQuery y Dataplex desplaza el valor del Data Engineer del SQL manual a la modelación semántica y gobernanza.",
        "script": SCRIPT_EP_01
    },
    {
        "title": "sIA Deep Dive: El Fin de la Amnesia en LLMs: Context Caching y Memoria Persistente",
        "slug": "sIA_DeepDive_Context_Caching_Memoria_Persistente.mp3",
        "desc": "sIA Deep Dive: Investigación profunda sobre Context Caching en Gemini, arquitecturas de memoria episódica jerárquica, aprendizaje anidado y el paralelismo con los Fluctlights de SAO.",
        "script": SCRIPT_EP_02
    },
    {
        "title": "sIA Deep Dive: Data Mesh en Retail Masivo: Contratos Semánticos y Streaming Continuo",
        "slug": "sIA_DeepDive_Data_Mesh_Retail_Streaming.mp3",
        "desc": "sIA Deep Dive: Descentralización de datos en retail de alta escala (estilo Walmart), Data Products con dbt y BigQuery, contratos semánticos en Kafka y economía de gremios.",
        "script": SCRIPT_EP_03
    },
    {
        "title": "sIA Deep Dive: Inferencia en el Borde vs Nube: NPU del Galaxy S25 e Insta360 X4",
        "slug": "sIA_DeepDive_Edge_AI_Galaxy_S25_Insta360.mp3",
        "desc": "sIA Deep Dive: Silicio NPU en Galaxy S25 (Snapdragon/Exynos), inferencia de SLMs locales en One UI 9, visión computacional 8K en Insta360 X4 y el Augma de Ordinal Scale.",
        "script": SCRIPT_EP_04
    }
]

async def run_all():
    print("=" * 60)
    print("Iniciando generación de los 4 episodios sIA Deep Dive...")
    print("=" * 60)
    
    for idx, cfg in enumerate(DEEPDIVES_CONFIG, 1):
        print(f"\n[{idx}/4] Sintetizando: {cfg['title']}...")
        out = await process_dialogue(
            script_text=cfg["script"],
            episode_title=cfg["title"],
            custom_filename=cfg["slug"],
            episode_description=cfg["desc"]
        )
        print(f"  -> Generado con éxito: {out}")
    
    print("\n✅ ¡Los 4 episodios sIA Deep Dive fueron sintetizados y añadidos al feed RSS!")

if __name__ == '__main__':
    asyncio.run(run_all())
