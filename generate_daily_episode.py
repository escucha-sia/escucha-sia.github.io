import sys
import asyncio
from pathlib import Path
from podcast_synthesizer import process_dialogue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Script for Episode 01: 03 de Octubre de 2026
EPISODE_SCRIPT = """
JORGE: ¡Muy buenos días a toda nuestra audiencia! Bienvenidos a sIA, tu espacio de análisis técnico y cultura tech diseñado para acompañarte en tu día. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es sábado tres de octubre de dos mil veintiséis, y les traemos un episodio cargado de noticias clave: cambios importantes en Google A I Studio, la evolución hacia el Agentic Data Cloud en BigQuery, la llegada de Android diecisiete a la serie Galaxy ese veinticinco y novedades muy esperadas en el mundo de Sword Art Online y Mushoku Tensei.
JORGE: Así es Dalia. Comencemos directo con el bloque de Inteligencia Artificial y herramientas para desarrolladores. Esta semana, Google implementó cuotas de uso diario dentro del playground de Google A I Studio. El objetivo principal es mantener la baja latencia y alta disponibilidad de la plataforma ante la enorme demanda de prototipado.
DALIA: Una medida lógica, Jorge, considerando que los tiers de Google A I Pro y Ultra mantienen cuotas notablemente más altas. Además, se destacó la llegada de Gemini tres punto ocho Flash, posicionado como el nuevo caballo de batalla con razonamiento avanzado y soporte para SynthID Bio, que permite marcar con marcas de agua estructuras moleculares generadas por I A.
JORGE: Pero ojo, el cambio de fondo que todos los desarrolladores debemos tener en el radar es la transición estratégica de Gemini: el paso de los clásicos Gems hacia Skills modulares y reutilizables. Este despliegue inicia en Workspace este cinco de octubre y en la aplicación general el trece de octubre. Google está empujando fuerte la integración con Google Antigravity, su entorno centrado en agentes para llevar código directamente de la prueba a producción.
DALIA: Un movimiento muy acertado para profesionalizar los flujos de agentes. Y hablando de flujos y arquitecturas robustas, Jorge, pasemos al bloque dos: Ingeniería de Datos, Cloud y Analítica Empresarial, porque el ecosistema de BigQuery, d b t y Apache Airflow está viviendo una auténtica era de automatización agéntica.
JORGE: Totalmente, Dalia. En Google Cloud, BigQuery ha consolidado Gemini Cloud Assist para generar y optimizar consultas en lenguaje natural, junto al Data Engineering Agent. Ahora es posible hacer analítica conversacional interactuando con grafos de datos y tablas consolidadas, respaldado por el nuevo BigQuery Security Center para gobernanza granular.
DALIA: Y para los ingenieros que vivimos en el código, d b t ha integrado el servidor de Model Context Protocol, o M C P, directamente en su extensión oficial de Visual Studio Code. Esto permite compilar, probar y verificar métricas sin salir del editor, reduciendo drásticamente la fricción entre la capa semántica y la transformación.
JORGE: Y la regla de oro de la industria para este dos mil veintiséis se mantiene más vigente que nunca: Airflow orquesta mediante el TaskFlow A P I, y d b t transforma. Cero scripts gigantescos y cero desorden en operadores Bash. Mantener la frontera limpia entre orquestación y transformación sigue siendo el mejor antídoto contra el código espagueti.
DALIA: Sabias palabras, colega. Ahora cambiemos de marcha hacia nuestro tercer bloque: Gadgets, Movilidad y Hardware personal. Si llevas un Galaxy en el bolsillo, hay excelentes noticias.
JORGE: ¡Y vaya que sí! Samsung comenzó el despliegue oficial y estable de Uan U I nueve punto cero, basado en Android diecisiete, para toda la familia Galaxy ese veinticinco, ese veinticinco plus y Ultra.
DALIA: Entre las novedades destacadas está My FanCam, una función de cámara que rastrea y mantiene centrada a una persona específica automáticamente mientras grabas video. También llegan Call Brief y Now Brief para resumir llamadas y notificaciones clave sin distracciones. Y en cámaras de acción, Insta tres sesenta ha reforzado la estabilidad de firmware para la X cuatro, asegurando que las tomas de trescientos sesenta grados no sufran de desorientación giroscópica.
JORGE: Ideal para documentar trayectos o rodadas. Y para cerrar con broche de oro, entremos a nuestro bloque favorito: Cultura Geek, Anime y Literatura Fantástica.
DALIA: ¡Grandes noticias para la comunidad! Reki Kawahara, el legendario creador de Sword Art Online, acaba de revelar nuevo tráiler y pósteres de combate para la adaptación al anime de Demons Crest, que estrena este seis de noviembre. Además, se confirmó oficialmente la producción de una nueva película original de la franquicia titulada Sword Art Online Integral Domain para dos mil veintiocho.
JORGE: Y en el universo de Mushoku Tensei, tras el cierre de la primera parte de la tercera temporada, la comunidad ya debate los preparativos para la continuación en dos mil veintisiete. Además, en Japón arranca la gira Road to Macross Crossover dos mil veintiséis para celebrar el décimo aniversario de Macross Delta.
DALIA: Una semana redonda para la tecnología, los datos y la cultura geek. Esperamos que este resumen les prepare con la mejor información técnica.
JORGE: Recuerda que puedes consultar todos los detalles, artículos y referencias de este episodio en nuestra revista digital sIA Journal. ¡Que tengan un excelente y productivo día, y nos escuchamos en la próxima edición de sIA!
DALIA: ¡Hasta la próxima!
"""

async def main():
    print("Iniciando generación completa del episodio sIA...")
    title = "sIA #1: Gemini 3.8, Agentic BigQuery, Android 17 y Sword Art Online"
    output_file = await process_dialogue(
        script_text=EPISODE_SCRIPT,
        episode_title=title,
        custom_filename="NoticIAs_Duo_2026-10-03.mp3"
    )
    print(f"\n✅ ¡Episodio completo generado con éxito!\nArchivo: {output_file}")

if __name__ == '__main__':
    asyncio.run(main())
