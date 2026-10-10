import sys
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EPISODE_02_SCRIPT = """
JORGE: ¡Muy buenos días a toda nuestra audiencia! Bienvenidos a una nueva entrega de sIA, tu espacio de análisis técnico y pensamiento estratégico. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy ponemos sobre la mesa un debate que está incendiando foros de arquitectura y salas de juntas técnicas: ¿estamos presenciando la muerte de la programación tradicional a manos del Vibe Coding, o estamos cayendo en una peligrosa trampa de deuda técnica?
JORGE: Y para darle contexto a quienes nos escuchan, hagamos una obligada consulta a nuestra bitácora histórica. Hace unos episodios discutíamos cómo las bases de datos vectoriales traducían el caos del mundo real para modelos como ChatGPT y Gemini. Y también vimos a Gemini tres punto cero ganar pruebas de lógica a ciegas. Pero hoy, la conversación ya no es sobre si el modelo puede escribir código... sino sobre quién tiene el criterio para auditar lo que genera.
DALIA: ¡Exactamente Jorge! Andrej Karpathy popularizó el término "Vibe Coding", esa idea seductora de programar únicamente dictando la intención o la "vibra" de lo que quieres, dejando que el modelo de lenguaje escupa cientos de líneas de código en segundos. Suena a superpoder, ¿verdad? Pues según las investigaciones recientes de Microsoft Research y el análisis de Reliable Data Engineering, estamos ante el fenómeno de la "ilusión de competencia".
JORGE: Es un concepto fascinante y a la vez aterrador, Dalia. La ilusión de competencia ocurre cuando el código generado luce elegante, tiene sangrías perfectas y pasa pruebas unitarias superficiales... pero colapsa miserablemente en casos de borde, en concurrencia masiva o en fugas de memoria silenciosas.
DALIA: Por eso la verdadera disciplina que está naciendo no es picar código por vibras, sino lo que la industria ya llama "Vibe Reviewing". Es decir, auditar holísticamente el sistema. Ya no te pagan por recordar la sintaxis de un for loop o pelearte con un punto y coma; tu valor real como ingeniero senior hoy radica en entender la arquitectura, los límites de seguridad y el comportamiento emergente del sistema.
JORGE: Y esto conecta directamente con la transformación más profunda en nuestro campo: la metamorfosis del equipo de datos. Durante una década nos llamaron "los fontaneros de datos", porque nuestro trabajo era conectar tuberías rígidas entre A P Is, bases de datos relacionales y almacenes analíticos.
DALIA: ¡Adiós al fontanero de datos, bienvenido el Arquitecto de Contexto! Con entornos como Google Antigravity y las capacidades agénticas de BigQuery y d b t con M C P, los agentes de software ya pueden generar y reparar consultas solos. Pero ojo: un agente autónomo sin contexto de negocio es una máquina de cometer errores a escala industrial.
JORGE: Así es. Si tus tablas en el almacén de datos sufren de deriva semántica, o si tus definiciones de clientes activos y ventas netas no están formalizadas en un contrato semántico claro, el agente va a alucinar métricas falsas con una seguridad pasmosa. El trabajo del ingeniero de datos moderno es curar el contexto, diseñar los esquemas de verdad, proteger la gobernanza y alimentar al agente con metadatos intachables.
DALIA: Eres el director de orquesta que le da la partitura afinada a la inteligencia artificial. Y cambiando un poco de lente hacia nuestro rincón geek favorito, ¿te has fijado, Jorge, en cómo esta arquitectura de agentes autónomos y gobernanza se parece cada vez más al Sistema Cardinal de Sword Art Online?
JORGE: ¡Totalmente! En Aincrad, Cardinal era ese motor autónomo que balanceaba misiones, ajustaba la dificultad y corregía glitches en tiempo real sin intervención humana directa. Hoy, con la orquestación multi-agente en herramientas como Antigravity, donde tienes subagentes especializados auditándose entre sí, estamos empezando a construir los primeros embriones de esos sistemas vivos.
DALIA: Fascinante paralelismo. Y antes de cerrar, un tip de movilidad para toda la comunidad: si ya tienen la actualización de Uan U I nueve en la serie Galaxy ese veinticinco, aprovechen Now Brief para que procese de forma local en la N P U sus recordatorios del día, sin enviar telemetría innecesaria a la nube.
JORGE: Excelente recomendación. Que toda nuestra audiencia tenga una jornada sumamente productiva, llena de decisiones arquitectónicas sólidas y cero ilusiones de competencia.
DALIA: ¡Nos escuchamos en el próximo episodio de sIA!
"""

async def main():
    print("Iniciando síntesis del Episodio #2 de sIA...")
    title = "sIA #2: De Plomeros a Arquitectos de Contexto: La Trampa del Vibe Coding y el Auge de Antigravity"
    filename = "sIA_Episodio_02_Arquitectos_de_Contexto.mp3"
    desc = "sIA #2: Análisis sobre Vibe Coding vs Vibe Reviewing, la ilusión de competencia técnica, la metamorfosis del ingeniero de datos a arquitecto de contexto y el paralelismo con el Sistema Cardinal de SAO."
    
    output_file = await process_dialogue(
        script_text=EPISODE_02_SCRIPT,
        episode_title=title,
        custom_filename=filename,
        episode_description=desc
    )
    print(f"\n✅ ¡Episodio #2 generado exitosamente!\nArchivo: {output_file}")

if __name__ == '__main__':
    asyncio.run(main())
