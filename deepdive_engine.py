"""
sIA Deep Dive Engine
Módulo de Investigación y Generación de Podcasts Extensos (15-25 min)
Basado en las directivas del Gem 19 (sIA) y los pilares de interés de Carlos Corona.
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUDIO_DIR = Path(r"C:\Carlos\noticias_podcast\audio")

# Pilares temáticos clave de Carlos para Deep Dives
PILLARS = {
    "AI_AGENTS": [
        "Google Antigravity y Sistemas Multi-Agente con MCP",
        "Vibe Coding vs Vibe Reviewing: La trampa de la deuda técnica",
        "Arquitecturas de Memoria Persistente y Context Caching en LLMs",
        "De Prompts a Agentes Autónomos: El fin de los Chatbots"
    ],
    "DATA_ENGINEERING": [
        "Data Mesh y Contratos de Datos Semánticos en Producción",
        "Agentic BigQuery y dbt con Model Context Protocol",
        "Arquitectura Kappa vs Lambda en Streaming de Alto Volumen",
        "Deriva Semántica y SCD Tipo 2: La Máquina del Tiempo de Datos"
    ],
    "HARDWARE_MOBILITY": [
        "Inferencia en el Borde: NPU Local en Galaxy S25 vs Cloud APIs",
        "Video Espacial y Fotogrametría Computacional con Insta360 X4"
    ],
    "3D_PRINTING_BAMBULAB": [
        "Bambu Lab y la Revolución de la Impresión 3D: Visión Computacional, Micro-LiDAR y Ecosistemas Cerrados",
        "Manufactura Distribuida y Prototipado Rápido: De Modelos CAD a Piezas Funcionales",
        "El Dilema Maker: Ecosistemas Integrados (Bambu Lab) vs Filosofía Open Source (Voron, Prusa)",
        "Sistemas Multi-Material y AMS: Optimizando el Desperdicio de Purga y Materiales Compuestos"
    ],
    "DECISION_MODELS_JEPA": [
        "JEPA de Yann LeCun vs LLMs: Por qué Predecir el Mundo es Superior a Predecir Tokens",
        "Modelos de Mundo y Arquitecturas de Decisión: Del Espacio Latente a la Planificación Autónoma",
        "Decision Transformers y Reinforcement Learning en Agentes de Producción"
    ],
    "GEEK_SYSTEMS": [
        "El Sistema Cardinal de Sword Art Online y la Arquitectura de AGI",
        "Mundos Virtuales Persistentes: De The Seed a los Metaversos Agénticos"
    ]
}


def build_deepdive_script(topic: str, thesis: str, technical_points: list, debate_points: list, geek_connection: str) -> str:
    """
    Construye un guion de formato largo estructurado en 4 actos entre Jorge y Dalia.
    """
    tech_str = "\n".join([f"- {p}" for p in technical_points])
    debate_str = "\n".join([f"- {p}" for p in debate_points])
    
    # Template estructurado para Jorge y Dalia
    script = f"""
JORGE: ¡Hola a todos! Bienvenidos a una edición especial de sIA Deep Dive, nuestro espacio de análisis técnico exhaustivo diseñado para esos momentos donde necesitamos ir mucho más allá del titular de las noticias. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy nos tomamos el tiempo para desmenuzar un tema que está transformando radicalmente la industria y que está en el centro de todas las conversaciones de arquitectura: {topic}.
JORGE: Así es Dalia. A diferencia de nuestros resúmenes matutinos de noticias diarias, en estas ediciones Deep Dive nos detenemos a examinar la anatomía del sistema, los trade-offs que nadie publica en las notas de prensa, y las implicaciones reales para quienes diseñamos software y datos en producción.
DALIA: Y la tesis central con la que abrimos hoy es contundente: {thesis}. Parece una afirmación audaz, pero cuando analizamos cómo se están moviendo los estándares de la industria, las piezas empiezan a encajar con una precisión matemática.

JORGE: Para entender el contexto, entremos directo al Acto Uno: El Cambio de Paradigma. ¿Por qué estamos hablando de esto precisamente ahora en dos mil veintiséis? Durante años nos acostumbramos a resolver estos problemas con arquitecturas convencionales, pero la llegada de modelos con ventanas de contexto masivas y agentes con acceso a herramientas del sistema operativo lo cambió todo.
DALIA: Exacto Jorge. Lo que antes era un cuello de botella computacional o de ancho de banda, hoy se ha convertido en un problema de diseño semántico y gobernanza. Ya no peleamos con si el modelo es capaz de responder; peleamos con si la arquitectura puede soportar respuestas no deterministas sin romper la consistencia de los datos.

JORGE: Y eso nos lleva al Acto Dos: La Anatomía Técnica bajo el capó. Desglosemos los componentes fundamentales de este ecosistema:
DALIA: Primero, tenemos que hablar de la capa de comunicación y protocolos. Los puntos críticos que están definiendo esta arquitectura son:
JORGE: El primer pilar: {technical_points[0] if len(technical_points) > 0 else 'El diseño de interfaces estandarizadas'}.
DALIA: El segundo pilar indispensable: {technical_points[1] if len(technical_points) > 1 else 'La gestión del estado persistente'}.
JORGE: Y el tercer pilar que casi todos los equipos pasan por alto hasta que colapsa: {technical_points[2] if len(technical_points) > 2 else 'El aislamiento de contexto y la seguridad de ejecución'}.

DALIA: Ahora bien, Jorge, entremos al Acto Tres: El Debate de la Realidad y los Costos Ocultos. Porque en Twitter y en las demos de marketing todo luce instantáneo y mágico, pero cuando llevas esto a un entorno empresarial con millones de transacciones, la realidad golpea con fuerza.
JORGE: ¡Totalmente de acuerdo, Dalia! La trampa principal que estamos viendo en las auditorías de sistemas es: {debate_points[0] if len(debate_points) > 0 else 'La falsa ilusión de velocidad frente a la deuda técnica acumulada'}.
DALIA: Y no olvidemos el factor financiero: {debate_points[1] if len(debate_points) > 1 else 'El costo oculto de cómputo y consumo de tokens en ciclos de retroalimentación'}. Si no diseñas límites estrictos y mecanismos de salida, tu infraestructura puede disparar la factura de nube en cuestión de horas.
JORGE: Por eso la regla de oro para el ingeniero senior hoy no es adoptar la herramienta más nueva, sino diseñar los contratos de observabilidad y las barreras de contención antes de soltar un agente o un pipeline a producción.

DALIA: Y para conectar con nuestra perspectiva reflexiva y geek en este Acto Cuatro: {geek_connection}.
JORGE: Es fascinante ver cómo las obras de ciencia ficción que leíamos hace años anticiparon exactamente los dilemas éticos y arquitectónicos a los que nos enfrentamos hoy al construir sistemas autónomos.
DALIA: Esperamos que esta inmersión profunda les brinde a todos nuestros oyentes herramientas de pensamiento estratégico y criterio técnico sólido para sus proyectos y decisiones de arquitectura.
JORGE: Recuerden que pueden consultar la bibliografía y notas completas de este episodio en nuestra revista digital sIA Journal y escucharnos directamente en Spotify. ¡Nos escuchamos en la próxima inmersión profunda de sIA Deep Dive!
DALIA: ¡Hasta la próxima!
"""
    return script.strip()

async def produce_deepdive(topic: str, thesis: str, technical_points: list, debate_points: list, geek_connection: str, custom_slug: str = None) -> Path:
    print(f"\n🚀 Produciendo episodio sIA Deep Dive: {topic}...")
    script = build_deepdive_script(topic, thesis, technical_points, debate_points, geek_connection)
    
    slug = custom_slug or topic.lower().replace(" ", "_")[:40]
    filename = f"sIA_DeepDive_{slug}.mp3"
    full_title = f"sIA Deep Dive: {topic}"
    desc = f"Episodio Deep Dive de investigación exhaustiva: {topic}. Tesis: {thesis}."
    
    output = await process_dialogue(
        script_text=script,
        episode_title=full_title,
        custom_filename=filename,
        episode_description=desc
    )
    print(f"\n✅ ¡Deep Dive completado! Archivo: {output}")
    return output

if __name__ == '__main__':
    # Test sample
    topic_sample = "Model Context Protocol y Agentes Autónomos en Producción"
    thesis_sample = "El protocolo MCP está reemplazando a las APIs REST tradicionales como el nuevo bus de integración estándar entre modelos de IA y herramientas del mundo real."
    tech_sample = [
        "Estandarización de herramientas cliente-servidor mediante JSON-RPC sobre stdio o SSE",
        "Descubrimiento dinámico de recursos, prompts y herramientas sin recompilar el agente",
        "Aislamiento de permisos y control granular de ejecución sobre el sistema de archivos"
    ]
    deb_sample = [
        "La sobrecarga de latencia y contexto cuando un agente maneja decenas de herramientas simultáneas",
        "Los riesgos de inyección de prompts indirecta a través de fuentes de datos no confiables"
    ]
    geek_sample = "Al igual que el Protocolo Seed de Sword Art Online permitió que cualquier desarrollador interconectara mundos virtuales con una misma base, MCP está creando la capa de interoperabilidad universal para agentes."
    
    asyncio.run(produce_deepdive(topic_sample, thesis_sample, tech_sample, deb_sample, geek_sample, "MCP_Agentes_Produccion"))
