"""
sIA Deep Dive: Jev de TypeSafe AI y la Revolución del Sistema 1
Generador autónomo de audio y artículo técnico.
"""

import sys
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT = """
JORGE: ¡Hola Carlos! Bienvenidos a una entrega verdaderamente especial de sIA Deep Dive. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy nos detenemos a analizar uno de los desarrollos más fascinantes y comentados de las últimas semanas en el mundo de la inteligencia artificial: la llegada de Jev, el nuevo modelo generalista desarrollado por TypeSafe AI que acaba de desmenuzar Carlos Santana en DotCSV.
JORGE: Así es Dalia. Si has seguido la conversación reciente sobre agentes autónomos, habrás notado una queja universal: los modelos de lenguaje actuales son increíbles para redactar, resumir o filosofar, pero cuando les pides que tomen decisiones rápidas en código, son lentos, caros y peligrosamente impredecibles.
DALIA: Nuestra tesis central de hoy es contundente: Durante años, la industria cometió el grave error arquitectónico de usar LLMs generativos para tareas de decisión y clasificación. Jev inaugura formalmente la era de los modelos de Sistema 1: redes discriminativas que no conversan ni generan texto, sino que evalúan estados en milisegundos y devuelven tipos de datos nativos y matemáticamente estructurados.
JORGE: Para entender el impacto, entremos directo al Acto Uno: El Absurdo de los LLMs para Enrutar Decisiones. Imagina contratar a un laureado escritor o a un filósofo para que presione un botón de emergencia cada medio segundo. Eso es exactamente lo que hacíamos al enviar un prompt gigante a GPT o Claude simplemente para decidir si un correo es urgente o para seleccionar qué función de una API invocar.
DALIA: ¡Exacto, Jorge! Un LLM autorregresivo tiene que predecir palabra por palabra, generando tokens innecesarios como "Claro, con gusto te ayudo con tu consulta", para luego intentar escupir un JSON que la mitad de las veces viene con comas rotas o campos alucinados. Pagar cientos de miles de tokens de contexto para un simple if condicional era un desperdicio técnico insostenible.
JORGE: Y eso nos lleva al Acto Dos: La Anatomía Técnica de Jev. ¿Cómo opera este modelo de TypeSafe AI bajo el capó?
DALIA: La clave de Jev es que es un modelo discriminativo generalista. No predice el siguiente token de texto en un vocabulario de cien mil palabras. Jev recibe el estado de tu sistema y entrega directamente tres tipos de salida fuertemente tipadas:
JORGE: El primer tipo es Choice: evalúa una lista de opciones discretas predefinidas y calcula la probabilidad matemática de cada una, garantizando que el resultado siempre sea una opción válida del catálogo.
DALIA: El segundo tipo es Score: una puntuación numérica continua entre cero y uno, perfecta para medir nivel de riesgo, prioridad de atención o afinidad de un cliente.
JORGE: Y el tercer tipo es Boolean o Noul: responde con precisión matemática sí o no con su respectivo intervalo de certeza, eliminando de raíz la ambigüedad del lenguaje natural.
DALIA: Y al no tener que generar texto, la inferencia ocurre en fracciones de milisegundo y con un consumo de cómputo infinitesimal comparado con un modelo como Gemini o Claude.
JORGE: Pero entremos al Acto Tres, Dalia: La Famosa Demo de DOOM y la Dupla Sistema 1 más Sistema 2 en Producción. Porque el experimento que mostró DotCSV dejó a toda la comunidad boquiabierta.
DALIA: ¡Fue una genialidad técnica! Pusieron a Jev a jugar al legendario videojuego DOOM en tiempo real. Pero ojo: no procesando los fotogramas de video con un modelo de visión pesado, sino ingiriendo directamente el vector de estado interno del motor: puntos de vida, munición, coordenadas de demonios en pantalla.
JORGE: Y Jev tomaba decisiones a decenas de ciclos por segundo: esquivar a la izquierda, disparar la escopeta, retroceder. Una velocidad de reacción que jamás podría alcanzar un modelo generativo.
DALIA: Y esto redefine por completo cómo debemos diseñar agentes autónomos en dos mil veintiséis siguiendo la teoría de Daniel Kahneman de Pensar Rápido, Pensar Despacio:
JORGE: El Sistema 1 es Jev: el reflejo incondicional del software. Enruta peticiones, valida esquemas, filtra anomalías y toma decisiones operativas instantáneas en el borde.
DALIA: Y el Sistema 2 son los modelos de razonamiento profundo como Gemini Thinking o los modelos de cadenas de pensamiento: solo los despiertas cuando el Sistema 1 detecta una situación compleja que exige deliberación estratégica de largo plazo.
JORGE: ¡Una sinergia perfecta! Y para nuestra conexión geek en el Acto Cuatro: esto me recuerda inmediatamente al Ultra Instinto en Dragon Ball Super. El principio marcial donde el cuerpo no espera a que el cerebro reflexione; las terminaciones nerviosas evalúan el entorno y reaccionan de manera instantánea y perfecta.
DALIA: ¡Totalmente! O al Sistema Cardinal de Sword Art Online, que balancea las misiones y los monstruos de Aincrad sin entablar un diálogo con los jugadores, ejecutando rutinas deterministas sobre el estado del servidor. Jev le da a la inteligencia artificial moderna ese mismo instinto reflejo.
JORGE: Una pieza clave que faltaba en el rompecabezas de la arquitectura agéntica. Carlos, esperamos que este análisis profundo sobre Jev y los modelos de decisión te brinde una perspectiva clara para optimizar tus propios pipelines y sistemas autónomos.
DALIA: Recuerda que puedes leer el artículo completo con las referencias en formato APA y el enlace directo al análisis de DotCSV en la revista digital sIA Journal en tu nueva casa escucha-sia.github.io. ¡Nos escuchamos en el próximo episodio!
JORGE: ¡Hasta la próxima y que tus modelos tomen siempre la decisión correcta!
DALIA: ¡Hasta pronto!
"""

async def main():
    title = "sIA Deep Dive: Jev de TypeSafe AI: La Muerte del LLM para Tomar Decisiones y el Auge del Sistema 1"
    slug = "sIA_DeepDive_Jev_TypeSafe_Sistema1.mp3"
    desc = "sIA Deep Dive: Análisis del nuevo modelo Jev de TypeSafe AI (analizado por DotCSV). Por qué los LLMs no deben usarse para tomar decisiones, tipado estricto (choice, score, boolean), la demo de DOOM y la arquitectura dual Sistema 1 + Sistema 2."
    
    print(f"🚀 Iniciando síntesis de: {title}...")
    output_path = await process_dialogue(
        script_text=SCRIPT,
        episode_title=title,
        custom_filename=slug,
        episode_description=desc
    )
    print(f"\n✅ Episodio Deep Dive sobre Jev generado exitosamente: {output_path}")

if __name__ == '__main__':
    asyncio.run(main())
