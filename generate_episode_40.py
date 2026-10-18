"""
sIA Episode #40 Production Script
Topic: Tesla Roadster SpaceX Package, Cold Gas Thrusters & Aerodinámica Activa Aeroespacial
Formato Narrativo sIA 4.0:
1. Apertura y Brújula de Sección: Presentación del show y la vertical (Hardware & Aeroespacial).
2. Resumen Ejecutivo & Tesis: Qué problema se analiza y por qué le importa al oyente hoy.
3. Despegue ("Alcanzarnos"): Inmersión directa al debate de ingeniería a fondo.
4. Fuera de la Burbuja: Termodinámica implacable, límites reales y riesgo regulatorio NHTSA.
5. Veredicto Conclusivo & Embudo Multicanal (Blog + Reel de TikTok).
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
[CHAPTER: Apertura & Brújula: sIA Hardware y Aeroespacial]
JORGE: Bienvenidos a sIA Podcast. Hoy abrimos nuestra sección de Hardware y Aeroespacial para poner bajo la lupa un dilema de ingeniería que tiene dividido al mundo del motor: ¿tocó techo la física del automóvil tradicional?
DALIA: Así es, Jorge. En este episodio desmenuzamos el polémico paquete SpaceX anunciado para el Tesla Roadster. La tesis de hoy es contundente: ningún superdeportivo eléctrico moderno podrá acelerar de cero a cien en menos de un segundo usando neumáticos tradicionales, porque la fricción del caucho contra el asfalto tiene un límite físico insalvable.
JORGE: Para romper esa barrera, la propuesta no es meter más caballos de fuerza en los motores eléctricos, sino acoplar diez toberas de propulsión de gas frío a setecientos bar de presión directamente en el chasis. En los próximos seis minutos vamos a analizar la termodinámica de estas toberas de Laval, la viabilidad de montar tanques espaciales de fibra de carbono en el tráfico diario y el enorme riesgo de homologación de seguridad vial ante un choque.
DALIA: Dicho esto, alcancemos el meollo del problema: Jorge, arranquemos por la física pura de las ruedas. ¿Por qué los mejores ingenieros de neumáticos admiten que el asfalto ya no da para más?

[CHAPTER: La Barrera de Fricción: Por Qué el Neumático Tocó Techo]
JORGE: Es pura física newtoniana, Dalia. Cualquier superdeportivo eléctrico moderno choca de frente contra el coeficiente de fricción del caucho contra el pavimento. Da igual que le metas dos mil caballos de fuerza o tracción vectorial independiente en cada rueda: si superas la adherencia máxima del neumático, la rueda patina y la potencia se disipa en calor y humo. No puedes bajar de uno punto seis segundos de cero a cien de manera consistente usando solo tracción mecánica.
DALIA: Exacto. El límite físico de la fuerza normal multiplicada por el coeficiente mu. Para acelerar más rápido, la única opción es aumentar el peso artificialmente o empujar otra cosa.
JORGE: Y esa otra cosa es la masa de aire alrededor del vehículo. La propuesta de SpaceX para el Roadster no es un capricho estético de marketing: es la aplicación directa de la Tercera Ley de Newton. Acción y reacción. Si dejas de empujar la carretera y empiezas a empujar el aire mediante propulsores de gas frío, desacoplas por completo el rendimiento del vehículo del agarre de los neumáticos.

[CHAPTER: Anatomía de Gas Frío: Tanques COPV a 700 Bar y Toberas de Laval]
DALIA: Pero desmenucemos la ingeniería real, porque esto no es magia ni ciencia ficción. Estamos hablando de recipientes de presión de compuesto sobreenrollado, los famosos tanques COPV de fibra de carbono que SpaceX utiliza en la etapa superior del cohete Falcon nueve.
JORGE: Esos tanques van empacados en el espacio donde normalmente estarían los asientos traseros del auto, almacenando aire ultracomprimido o nitrógeno a más de setecientos bar de presión, unas diez mil libras por pulgada cuadrada. A esa presión, una fuga microscópica corta metal como si fuera mantequilla.
DALIA: El sistema integra válvulas piezomagnéticas con tiempos de apertura de menos de dos milisegundos y toberas convergentes-divergentes de Laval. En la garganta de la tobera, el flujo de gas se acelera a la velocidad del sonido, y al expandirse en la campana alcanza velocidades supersónicas generando empuje puro instantáneo.
JORGE: Y lo fascinante no es solo la aceleración en línea recta de cero a cien en cero punto ocho segundos. El verdadero salto arquitectónico está en las diez toberas perimetrales distribuidas en el chasis. Es un sistema de control de actitud aeroespacial en tierra. Si entras a una curva a doscientos kilómetros por hora, las toberas exteriores empujan hacia abajo y hacia el centro de la curva, generando toneladas de carga aerodinámica estática sin necesidad de alerones gigantescos.

[CHAPTER: 🌌 Fuera de la Burbuja: La Termodinámica Implacable y el Choque Regulatorio]
DALIA: Entremos a nuestra cápsula Fuera de la Burbuja, porque la termodinámica no tiene departamento de relaciones públicas. El impulso específico del aire comprimido es miserable: ronda los sesenta a setenta segundos, comparado con los más de trescientos segundos de un propelente químico de cohete.
JORGE: Totalmente. Una descarga continua vacía los tanques en apenas diez a doce segundos de empuje total. El compresor eléctrico a bordo, alimentado por el paquete estructural de baterías, tarda más de quince minutos en recuperar la presión operativa de los setecientos bar. Es un sistema para pulsos de milisegundos en momentos críticos, no para volar de forma sostenida como insinúan los titulares de prensa sensacionalistas.
DALIA: Y está la gran pregunta de ingeniería civil: la homologación de seguridad de la NHTSA. En una colisión a alta velocidad, un tanque COPV cargado a diez mil PSI dentro de la celda de deformación estructural del habitáculo representa un riesgo explosivo catastrófico si no cuenta con discos de ruptura pirotécnicos que liberen la presión en microsegundos. Ninguna aseguradora civil tiene tablas actuariales para cubrir propulsores supersónicos en avenidas públicas.

[CHAPTER: Veredicto de Ingeniería & Embudo Multicanal]
JORGE: Veredicto de arquitectura: el Tesla Roadster con paquete SpaceX no es un auto comercial viable para ir al supermercado; es un laboratorio rodante que demuestra cómo la mecatrónica aeroespacial va a devorar los límites mecánicos del automóvil.
DALIA: Si eres ingeniero y quieres ver el diagrama de bloques del sistema neumático COPV, las ecuaciones de expansión isentrópica y las patentes aeroespaciales en formato APA, revisa el artículo técnico de hoy en escucha-sia punto github punto io.
JORGE: Y si prefieres ver la simulación gráfica animada en dos dimensiones con el chasis vectorial y las toberas disparándose en tiempo real, ya tienes disponible nuestro Reel completo de cuarenta y cinco segundos en TikTok y YouTube Shorts. ¡Nos escuchamos en el siguiente sIA Focus!
"""

EPISODE_INFO = {
    "title": "sIA #40: Hardware & Aeroespacial — Tesla Roadster SpaceX: Propulsión de Gas Frío y la Física de Volar en Asfalto",
    "filename": "sIA_Daily_S03_Tesla_Roadster_SpaceX_Gas_Frio_2026-10-17.mp3",
    "description": "sIA #40 (6 min): Debate técnico sobre el Tesla Roadster y el paquete SpaceX. La física del límite de fricción neumático-asfalto, tanques COPV a 700 bar, toberas de Laval supersónicas para control de actitud (ACS) y los riesgos termodinámicos y regulatorios de la propulsión de gas frío en tierra. | Leer artículo y ecuaciones APA: https://escucha-sia.github.io/articulos/sia-40-tesla-roadster-spacex-gas-frio-fisica-aeroespacial.html"
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
            "Tesla Roadster paquete SpaceX con propulsores de gas frío (Cold Gas Thrusters)",
            "Límites físicos de fricción neumático-asfalto vs propulsión newtoniana por tanques COPV a 700 bar",
            "Toberas de Laval supersónicas para control de actitud vehicular (ACS)"
        ],
        "cooldown_days": 45,
        "date": "Sat, 17 Oct 2026 12:00:00 GMT"
    }
    
    vault_data["covered_items"].insert(0, new_entry)
    with open(NEWS_VAULT, "w", encoding="utf-8") as f:
        json.dump(vault_data, f, indent=2, ensure_ascii=False)
    print("📋 Registrado en news_vault.json con cooldown estricto de 45 días.")

async def main():
    print("=" * 60)
    print(f"🎙️ GENERANDO EPISODIO #40 CON NUEVO STORYTELLING: {EPISODE_INFO['title']}")
    print("=" * 60)
    await process_dialogue(
        SCRIPT_TEXT,
        episode_title=EPISODE_INFO["title"],
        custom_filename=EPISODE_INFO["filename"],
        episode_description=EPISODE_INFO["description"]
    )
    log_to_news_vault()
    print("✅ ¡Episodio #40 regenerado con éxito con formato narrativo sIA 4.0!")

if __name__ == "__main__":
    asyncio.run(main())
