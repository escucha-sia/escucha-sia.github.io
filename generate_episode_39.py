"""
sIA Episode #39 Production Script
Topic: Modelos de Mundo JEPA (Joint Embedding Predictive Architecture) & Inteligencia de Enjambre
Formato Narrativo sIA 4.0:
1. Apertura y Brújula de Sección: Identificación del show y la vertical (sIA IA & Agentes).
2. Resumen Ejecutivo & Tesis: Por qué los LLMs no entienden física y la alternativa de JEPA.
3. Despegue ("Alcanzarnos"): Debate técnico sobre representación latente vs tokens.
4. Fuera de la Burbuja: Estigmergia digital y enjambres sin orquestador central.
5. Veredicto Conclusivo & Embudo Multicanal (Blog + Reel Vertical).
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
NEWS_VAULT = BASE_DIR / "news_vault.json"

SCRIPT_TEXT = """
[CHAPTER: Apertura & Brújula: sIA IA y Agentes Autónomos]
JORGE: Bienvenidos a sIA Podcast. Hoy abrimos nuestra sección de Inteligencia Artificial y Sistemas Agénticos para abordar un dilema que está sacudiendo a los laboratorios de investigación: ¿hemos llegado al límite de lo que las máquinas pueden aprender prediciendo la siguiente palabra?
DALIA: Así es, Jorge. En este episodio desmenuzamos la arquitectura JEPA de Yann LeCun y Meta FAIR: los Modelos de Mundo predictivos en espacios latentes, y cómo la estigmergia digital permite desplegar enjambres de agentes ultra-ligeros sin necesidad de un orquestador central que asfixie el sistema en latencia y costos.
JORGE: En los próximos minutos vamos a entender por qué predecir tokens en una dimensión es ciego ante la física de la realidad, cómo JEPA anticipa trayectorias y masas descartando el ruido visual, y cómo coordinar miles de agentes como si fueran hormigas digitales en memoria compartida.
DALIA: Dicho esto, alcancemos de lleno el centro del debate: Jorge, dime una sola razón técnica por la que deberíamos seguir creyendo que predecir la siguiente palabra en un texto va a dotar a una IA de sentido común sobre las leyes de la física.

[CHAPTER: El Callejón sin Salida del Token Autoregresivo]
JORGE: Es matemáticamente inviable, Dalia. Hasta ahora el escalado masivo de tokens nos ha dado una ilusión convincente de razonamiento. Pero Yann LeCun y el equipo de Meta FAIR tienen razón en su tesis: los modelos autorregresivos son miopes. Generan texto token por token en un espacio unidimensional. Si un agente comete un error del dos por ciento en el paso uno, ese error se propaga y amplifica exponencialmente en el paso veinte.
DALIA: Exacto. El célebre efecto bola de nieve. Si le pides a un LLM tradicional que guíe un brazo robótico o planifique una ruta de rescate, el modelo no tiene noción espacial de inercia, masa ni gravedad. Solo predice qué palabra suena más verosímil según su corpus de entrenamiento estadístico.
JORGE: Ahí es donde entra JEPA: Joint Embedding Predictive Architecture. En lugar de forzar a la red neuronal a reconstruir cada píxel o cada palabra irrelevante del fondo, JEPA predice la evolución de un estado dentro de un espacio de incrustación abstracto. Si un automóvil gira a la izquierda, a la IA no le importa si una hoja de árbol se movió en la acera; le importa la trayectoria invariante y la masa del vehículo.
DALIA: Y eso reduce el espacio de búsqueda computacional en órdenes de magnitud. Donde los LLMs colapsan por latencia en video continuo o control físico en tiempo real, JEPA aprende causalidad sin millones de tokens de relleno.

[CHAPTER: 🌌 Fuera de la Burbuja: Enjambres sin Orquestador Central]
JORGE: Y si JEPA rompe el monopolio del token autoregresivo, nuestra cápsula Fuera de la Burbuja rompe el dogma del orquestador centralizado.
DALIA: Hablemos de estigmergia digital y la inteligencia de enjambre. La arquitectura agéntica dominante hoy insiste en poner un supermodelo gigantesco como director de orquesta que manda mensajes a agentes secundarios. ¿Qué pasa en producción? Ese orquestador se convierte en un cuello de botella de latencia y un único punto de falla carísimo.
JORGE: En la naturaleza, un millón de hormigas o una colonia de termitas construyen catedrales ventiladas sin tener un rey que les diga qué hacer. Cooperan dejando rastros químicos en el entorno: si una zona tiene feromonas de peligro, todas evitan ese camino automáticamente.
DALIA: En sistemas distribuidos, esto se traduce en agentes ultra-ligeros de siete millones de parámetros que solo leen y escriben marcas criptográficas en una memoria compartida. Sin orquestador. Las soluciones complejas emergen de reglas locales simples. Un agente detecta una anomalía de red, deja un rastro de prioridad en el bus, y tres agentes de contención reaccionan en paralelo en menos de cinco milisegundos.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
JORGE: Veredicto técnico para tu arquitectura: no intentes usar LLMs de razonamiento lento para problemas de control dinámico. Usa JEPA para fundamentación sensorial y enjambres descentralizados para ejecución masiva en el borde.
DALIA: Si quieres ver la formulación matemática de la función de pérdida por energía y los esquemas de estigmergia para microservicios, entra ahora mismo a nuestro artículo técnico en escucha-sia punto github punto io.
JORGE: Y en nuestras redes sociales y canal ya tienes el Reel vertical de cuarenta y cinco segundos con la síntesis visual de esta entrega. ¡Nos escuchamos en el siguiente sIA Focus!
"""

EPISODE_INFO = {
    "title": "sIA #39: IA & Agentes — Modelos de Mundo JEPA y Enjambres sin Orquestador",
    "filename": "sIA_Daily_S01_IA_JEPA_Modelos_de_Mundo_2026-10-15.mp3",
    "description": "sIA #39 (6 min): Debate técnico sobre por qué predecir el siguiente token es un callejón sin salida para entender la física, la ventaja de JEPA (Joint Embedding Predictive Architecture) y enjambres agénticos descentralizados mediante estigmergia digital. | Leer artículo y referencias APA: https://escucha-sia.github.io/articulos/sia-39-ia-agentes-modelos-de-mundo-jepa-enjambres-descentralizados.html"
}

def log_to_news_vault():
    vault_data = {"covered_items": []}
    if NEWS_VAULT.exists():
        try:
            vault_data = json.loads(NEWS_VAULT.read_text(encoding='utf-8'))
        except Exception:
            pass
    
    new_entry = {
        "title": EPISODE_INFO["title"],
        "filename": EPISODE_INFO["filename"],
        "topics": [
            "Modelos de Mundo no autoregresivos (JEPA y arquitecturas basadas en energía)",
            "Inteligencia de Enjambre y Estigmergia digital sin orquestador central"
        ],
        "cooldown_days": 45,
        "date": "Thu, 15 Oct 2026 20:30:00 GMT"
    }
    
    vault_data["covered_items"].insert(0, new_entry)
    with open(NEWS_VAULT, "w", encoding="utf-8") as f:
        json.dump(vault_data, f, indent=2, ensure_ascii=False)
    print("📋 Registrado en news_vault.json con cooldown estricto de 45 días.")

async def main():
    print("=" * 60)
    print(f"🎙️ GENERANDO EPISODIO #39 CON NUEVO STORYTELLING: {EPISODE_INFO['title']}")
    print("=" * 60)
    await process_dialogue(
        SCRIPT_TEXT,
        episode_title=EPISODE_INFO["title"],
        custom_filename=EPISODE_INFO["filename"],
        episode_description=EPISODE_INFO["description"]
    )
    log_to_news_vault()
    print("✅ ¡Episodio #39 regenerado con éxito con formato narrativo sIA 4.0!")

if __name__ == "__main__":
    asyncio.run(main())
