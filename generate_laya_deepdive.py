"""
sIA Deep Dive: Laya: El Centro de Comando Agéntico Open Source que Desafía a Jev
Generador autónomo de audio y artículo técnico.
"""

import sys
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT = """
JORGE: ¡Hola a toda nuestra audiencia! Bienvenidos a una nueva entrega de sIA Deep Dive. Soy Jorge.
DALIA: ¡Y yo soy Dalia! En nuestro episodio anterior desmenuzamos a fondo el impacto de Jev, el nuevo modelo de TypeSafe AI que demostró por qué usar LLMs generativos para tomar decisiones operativas es un grave error de arquitectura.
JORGE: Así es Dalia. La comunidad recibió ese análisis con entusiasmo, pero de inmediato surgió el gran debate técnico: Jev es un modelo fascinante, pero es privativo y cerrado. ¿Existe una alternativa de código abierto, local y soberana que nos permita orquestar acciones y decisiones agénticas en nuestras herramientas de trabajo diarias sin depender de APIs de terceros?
DALIA: La respuesta acaba de aterrizar en el ecosistema open source y se llama Laya, un proyecto desarrollado por Aayush Chawla que está llamando poderosamente la atención en GitHub por su enfoque local-first como centro de comando para agentes de inteligencia artificial.
JORGE: Nuestra tesis de hoy es clara: mientras Jev ataca el problema de la toma de decisiones a nivel de los pesos neuronales del modelo, Laya resuelve el desafío a nivel de la arquitectura del sistema. Transforma el diluvio de notificaciones de nuestros entornos profesionales en tarjetas de acción pre-estadiadas y listas para ejecutarse con un solo clic.
DALIA: Para entender el porqué de Laya, entremos al Acto Uno: El Infierno de las Notificaciones y la Sobrecarga Cognitiva. Cualquier ingeniero o líder técnico en dos mil veintiséis vive atrapado en una dispersión brutal: mensajes urgentes en Slack, hilos interminables en Gmail y Outlook, incidencias en Jira o Linear, pull requests en GitHub o Bitbucket y documentación en Notion.
JORGE: Es un cambio de contexto constante que destruye el estado de flujo. Y los intentos previos de resolverlo con inteligencia artificial fallaban porque te ponían un bot de chat al que tenías que copiarle y pegarle la información para recibir un resumen genérico que al final te obligaba a abrir tres pestañas más.
DALIA: ¡Exactamente! Por eso Laya plantea una premisa disruptiva en su Acto Dos: La respuesta debe estar lista antes de que abras la notificación. ¿Cómo lo logra? Interceptando los eventos en segundo plano mediante un ecosistema local de flujos en n8n.
JORGE: Y eso nos lleva al Acto Tres: La Anatomía Técnica de Laya. Aquí hay varias decisiones de ingeniería que merecen un aplauso de pie. Primero: nada de aplicaciones web pesadas basadas en Electron que consumen gigabytes de memoria RAM. Laya utiliza Tauri versión dos compilado en Rust para el shell de escritorio.
DALIA: Para la interfaz gráfica usa Svelte cinco con su nuevo sistema reactivo de Runes y Tailwind CSS, logrando una fluidez instantánea. En el backend corre un motor de Python con FastAPI sobre el puerto local ocho mil cuatrocientos veinte.
JORGE: Y la persistencia es una obra de arte híbrida: SQLite en modo WAL para los datos estructurados y búsqueda léxica BM25 sobre SQLite FTS5, combinada con búsqueda vectorial densa mediante ChromaDB embebido.
DALIA: Ambas fuentes se fusionan mediante Reciprocal Rank Fusion, lo que permite a Laya encontrar tanto palabras clave exactas como conceptos semánticos de forma ultrarrápida en tu propio disco duro.
JORGE: Pero lo más brillante es el Acto Cuatro: El Cerebro Multi-Persona y las Action Cards. Cuando llega un evento, Laya no te manda una alerta vacía. Su motor lo clasifica y lo envía a un agente especializado: Ingeniero, Comunicaciones, Operaciones, Ventas, Recursos Humanos o Finanzas.
DALIA: Este agente investiga el contexto histórico, cruza el ticket de Jira con el pull request de GitHub y el hilo de Slack gracias a su resolución de entidades cruzadas, y prepara una Action Card. Si es un bug, te presenta la explicación y el borrador del comentario; si es un correo, te deja redactada la respuesta.
JORGE: Y para tareas de programación complejas, Laya abre un Card Workspace colaborativo que se conecta directamente con agentes CLI que ya tengas instalados en tu computadora, como Claude Code, Gemini CLI o Cursor Agent, aprovechando incluso las cuotas de tus herramientas locales sin gastar tokens extra de API.
DALIA: Tú como humano en el bucle simplemente revisas la tarjeta de acción, y si estás de acuerdo, presionas un botón para que el gateway local de n8n ejecute la acción en la plataforma correspondiente.
JORGE: Y llegamos al Acto Cinco: Laya frente a Jev: Dos Filosofías que Redefinen el Futuro Agéntico. Jev es la micro-decisión de milisegundo a nivel de silicio, el Sistema Uno reflejo que no genera texto. Laya es el centro de control macroscópico que orquesta el Sistema Uno con el Sistema Dos, dándole soberanía total, privacidad absoluta y código abierto a la comunidad de desarrolladores.
DALIA: ¡Totalmente! Y para nuestra conexión geek en el Acto Seis: Laya me recuerda inmediatamente a la computadora central y la interfaz LCARS del USS Enterprise en Star Trek. Los sensores de la nave procesan la telemetría del motor de curvatura y las alertas tácticas en tiempo real, y cuando el Capitán Picard mira su consola, la maniobra ya está calculada; solo tiene que decir su famoso Make it so, o Hágase.
JORGE: ¡Qué gran analogía, Dalia! O también al sistema JARVIS y FRIDAY en la armadura de Iron Man: Tony Stark no se detiene a escribir prompts en medio de la batalla; el sistema pre-calcula las trayectorias balísticas y proyecta en su visor la acción lista para ser confirmada con un simple parpadeo. Laya lleva esa misma sensación de mando a nuestro día a día profesional.
DALIA: Dos visiones complementarias que demuestran que el futuro de la inteligencia artificial no consiste en chatear con bots, sino en orquestar acciones deterministas con criterio humano.
JORGE: Esperamos que este análisis les brinde a todos nuestros oyentes una visión clara para evaluar tanto modelos especializados como plataformas de orquestación soberana en sus propios proyectos.
DALIA: Recuerden suscribirse a sIA en Spotify para acompañarnos en cada entrega técnica, y visitar nuestra revista digital sIA Journal en escucha-sia.github.io para leer el artículo completo con las referencias en formato APA y los enlaces directos a los repositorios de Laya y Jev.
JORGE: ¡Hasta la próxima y que sus centros de comando ejecuten siempre la mejor acción!
DALIA: ¡Hasta pronto a todos!
"""

async def main():
    title = "sIA Deep Dive: Laya: El Centro de Comando Agéntico Open Source que Desafía a Jev"
    slug = "sIA_DeepDive_Laya_OpenSource_CommandCenter.mp3"
    desc = "sIA Deep Dive: Análisis exhaustivo de Laya (aayushch/laya), la alternativa open source y local-first a los modelos privativos de decisión como Jev. Arquitectura en Tauri v2, Svelte 5, FastAPI, n8n embebido, recuperación híbrida ChromaDB + SQLite FTS5 (RRF), Action Cards y agentes CLI."
    
    print(f"🚀 Iniciando síntesis de: {title}...")
    output_path = await process_dialogue(
        script_text=SCRIPT,
        episode_title=title,
        custom_filename=slug,
        episode_description=desc
    )
    print(f"\n✅ Episodio Deep Dive sobre Laya generado exitosamente: {output_path}")

if __name__ == '__main__':
    asyncio.run(main())
