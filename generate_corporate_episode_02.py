"""
sIA Crónicas Corporativas — Episodio Especial #02
Empresa: Valve & Gabe Newell: De Millonarios en Microsoft al Trono de Steam
Formato Narrativo sIA 4.0 (Estilo Chisme Corporativo & Negocios):
1. Apertura & Brújula: sIA Crónicas Corporativas.
2. Resumen Ejecutivo & Tesis: Dejar a Bill Gates para fundar una empresa de videojuegos sin jefes ni accionistas.
3. Despegue ("Alcanzarnos"): El día que DOOM superó a Windows 95 y la renuncia millonaria.
4. El Gran Escándalo: El hacker alemán que robó el código de Half-Life 2 y la trampa del FBI.
5. Sangre en la Sala de Juntas: La demanda contra Vivendi y la imposición forzada de Steam en 2004.
6. Fuera de la Burbuja: La anarquía de los escritorios con ruedas, la rentabilidad récord por empleado y por qué jamás existirá Half-Life 3.
7. Veredicto Corporativo & Flywheel Tripartito (Blog + Reel + Spotify).
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

SCRIPT_CORP_02 = """
[CHAPTER: Apertura & Brújula: sIA Crónicas Corporativas]
JORGE: Bienvenidos a sIA Crónicas Corporativas, el espacio donde contamos la historia sin censura de las empresas que cambiaron las reglas del juego tecnológico: sus traiciones, sus obsesiones de oficina y las jugadas maestras que nadie vio venir.
DALIA: Así es, Jorge. Y hoy nos adentramos en los pasillos de la compañía más enigmática, rentable y anárquica de la industria del entretenimiento digital: Valve Corporation y su legendario líder, Gabe Newell. La tesis central de hoy es fascinante: Valve no es una empresa de videojuegos convencional; es un monopolio privado de distribución digital que genera más ganancias por empleado que Apple, Google o Goldman Sachs, operando sin jefes, con escritorios sobre ruedas y tras haber sobrevivido al robo de código fuente más humillante de la historia.
JORGE: En los próximos diez minutos vamos a revelar cómo dos millonarios de Microsoft renunciaron el mismo día de una boda para apostar su propia fortuna, la trampa con el F B I para cazar a un hacker alemán en un aeropuerto, la guerra legal contra Vivendi que casi los destruye, y la verdadera razón corporativa por la que jamás lanzarán Half-Life tres.
DALIA: Dicho esto, alcancemos el meollo del chisme: Jorge, arranquemos por mil novecientos noventa y seis en las oficinas de Microsoft en Redmond. ¿Qué vio Gabe Newell para dejar el imperio de Bill Gates?

[CHAPTER: La Fuga de Microsoft y el Desastre de Quiver]
JORGE: Principios de los noventa. Gabe Newell y Mike Harrington eran dos de los primeros empleados clave de Microsoft. Llevaban más de una década programando las primeras versiones de Windows y tenían tantas opciones sobre acciones que ya eran multimillonarios antes de cumplir los treinta y cinco años. Pero Gabe tenía una obsesión que desconcertaba a Bill Gates: los videojuegos.
DALIA: En mil novecientos noventa y cinco, Gabe analizó los datos de instalación en computadoras de todo el mundo y descubrió una estadística demoledora: el juego Doom de John Carmack estaba instalado en más computadoras personales que el flamante sistema operativo Windows noventa y cinco. Microsoft se gastaba cientos de millones de dólares en marketing y un puñado de chicos en Texas haciendo un juego de disparos los superaba en adopción.
JORGE: Gabe convenció a Bill Gates de dejarlo portar Doom a Windows noventa y cinco de forma gratuita. Pero después de ver el fenómeno de cerca, entendió que el software del futuro no eran las hojas de cálculo de Excel; era el entretenimiento interactivo. En mil novecientos noventa y seis, el mismo día en que Gabe se casó, él y Mike Harrington renunciaron a Microsoft, pusieron millones de dólares de su propio bolsillo y fundaron Valve en Kirkland, Washington.
DALIA: Querían ser cien por ciento independientes. Jamás aceptarían capital de riesgo ni presiones de inversionistas de Wall Street. Pero su primer proyecto, llamado inicialmente Quiver, era un juego mediocre, lleno de clichés espaciales. A finales de mil novecientos noventa y siete, con el juego casi listo para Navidad, Gabe tomó una decisión que cualquier editor comercial habría prohibido: canceló el lanzamiento, tiró a la basura casi todo el trabajo de un año y rediseñó el juego desde cero.
JORGE: Crearon el proceso Cabal: sentaron a escritores, animadores y programadores en una misma sala para construir una narrativa sin cortes de cámara ni pantallas de carga, donde el jugador jamás abandona los ojos de Gordon Freeman. Así nació Half-Life en mil novecientos noventa y ocho: vendió millones de copias, ganó más de cincuenta premios a juego del año y transformó la industria para siempre.

[CHAPTER: El Hacker Alemán y la Trampa del FBI]
DALIA: Pero el éxito atrajo una de las mayores catástrofes de seguridad informática en la historia corporativa. En dos mil tres, Valve llevaba cinco años desarrollando en secreto la secuela más esperada del planeta: Half-Life dos. La presión era brutal, los retrasos se acumulaban y los fanáticos estaban desesperados.
JORGE: Y en octubre de dos mil tres, el desastre golpeó. Un joven hacker alemán de veinte años llamado Axel Gembe descubrió un servidor de Valve con una contraseña en blanco y logró instalar un registrador de teclas en la máquina del propio Gabe Newell. Durante semanas espió el desarrollo interno, hasta que descargó el código fuente completo del motor Source y de Half-Life dos, y lo filtró entero en internet.
DALIA: Fue una herida de muerte. El juego que representaba una inversión de más de cuarenta millones de dólares estaba destripado en foros públicos un año antes de salir al mercado. Gabe Newell estaba tan desesperado que publicó un mensaje en los foros de la comunidad pidiendo ayuda a los propios jugadores para encontrar al responsable.
JORGE: Y aquí viene el giro digno de película de espías. El hacker, con una soberbia increíble y buscando la aprobación de su ídolo, le envió un correo electrónico al propio Gabe usando una dirección anónima. Le confesó que él había sido el atacante, pero le aseguró que amaba el juego y le pidió trabajo como consultor de seguridad en Valve.
DALIA: ¡Imagínate la escena! El tipo que te robó el trabajo de cinco años te pide empleo. Gabe le siguió la corriente con total frialdad: le hizo una entrevista técnica por teléfono, le ofreció un contrato formal y le compró un boleto de avión para volar a Seattle. Al mismo tiempo, Gabe coordinó con el F B I para que agentes federales esperaran al hacker en la puerta del avión y lo arrestaran en cuanto pisara suelo estadounidense.
JORGE: El plan era perfecto, pero las autoridades alemanas interceptaron las llamadas y arrestaron a Gembe en su casa en Alemania la madrugada previa a su vuelo, desbaratando la emboscada del F B I. El lanzamiento de Half-Life dos tuvo que retrasarse otro año entero para reescribir partes críticas del código.

[CHAPTER: La Guerra contra Vivendi y la Noche que Nació Steam]
DALIA: Pero mientras lidiaban con hackers, Gabe estaba librando una batalla mucho más peligrosa contra las distribuidoras tradicionales. En dos mil dos, Valve vio que mantener actualizados juegos como Counter-Strike era una pesadilla logística. Gabe le propuso a gigantes como Microsoft, Yahoo y Cisco crear una plataforma de distribución digital que actualizara los juegos y vendiera contenido directamente por internet.
JORGE: ¿Y sabes qué le respondieron todos? Se le rieron en la cara. Le dijeron que nadie compraría videojuegos por internet y que el ancho de banda jamás soportaría descargas masivas. Así que Valve dijo: 'Perfecto, lo haremos nosotros solos'. Desarrollaron Steam.
DALIA: En noviembre de dos mil cuatro, cuando finalmente lanzaron Half-Life dos en formato físico en tiendas de todo el mundo a través de su distribuidora Vivendi Universal, Valve ejecutó la jugada más audaz de la historia: obligó a que toda persona que comprara el disco en una tienda tuviera que instalar Steam y activar el juego por internet.
JORGE: Fue el caos absoluto. Los servidores colapsaron, millones de jugadores enfurecidos se quejaban del error de conexión y Vivendi demandó a Valve acusándolos de competencia desleal y de querer robarles el canal minorista. Pero en el juicio, los abogados de Valve descubrieron un correo interno demoledor: un ejecutivo de Vivendi ordenaba destruir intencionalmente archivos para forzar a Valve a la bancarrota.
DALIA: Vivendi perdió el juicio de forma estrepitosa. Tuvieron que cederle a Valve los derechos de propiedad intelectual absolutos sobre todas sus franquicias y abandonar el mercado. En una sola jugada maestra, Gabe Newell no solo sobrevivió: convirtió a Steam en la tienda por defecto de todos los jugadores de P C del mundo.

[CHAPTER: 🌌 Fuera de la Burbuja: La Anarquía de los Escritorios con Ruedas y la Maldición de Half-Life 3]
JORGE: Entremos a nuestra cápsula Fuera de la Burbuja Corporativa, porque el modelo interno de Valve es algo que ninguna escuela de negocios tradicional puede explicar.
DALIA: En las oficinas de Valve en Bellevue, Washington, no hay organigramas, no hay jefes de proyecto ni mandos medios. Literalmente, cada escritorio tiene ruedas industriales de trabajo pesado. El manual del empleado dice claramente: si un proyecto te parece aburrido o crees que puedes aportar más valor en otra área, desconectas tu computadora, empujas tu escritorio rodando por el pasillo y te unes a ese equipo.
JORGE: Suena utópico, pero tiene su lado oscuro: la tiranía de los pares. Las compensaciones y bonos anuales multimillonarios se deciden mediante votaciones cruzadas entre los propios compañeros. Si caes mal en el grupo o tu proyecto no genera impacto comercial inmediato, te aíslan silenciosamente.
DALIA: Y hablemos de la pregunta que todo el planeta se hace: ¿por qué nunca salió Half-Life tres? La respuesta no es creativa; es pura economía matemática. Con Steam, Valve cobra una comisión de hasta el treinta por ciento sobre cada videojuego vendido en computadoras a nivel global. Tienen apenas unos trescientos cincuenta empleados y generan miles de millones de dólares en ganancias líquidas puras cada año.
JORGE: Para qué vas a gastar cien millones de dólares y cuatro años de sufrimiento de ingenieros arriesgándote a no cumplir las expectativas colosales de Half-Life tres, cuando la economía de skins de Counter-Strike y la tienda de Steam te generan esa misma cantidad de dinero cada tres semanas en piloto automático. Gabe Newell convirtió a Valve en la máquina de imprimir dinero más eficiente de la historia.

[CHAPTER: Veredicto Corporativo & Flywheel Tripartito]
DALIA: Veredicto de sIA Crónicas Corporativas: Gabe Newell demostró que en la era digital, ser dueño del software te da un buen negocio; pero ser dueño del protocolo de distribución y de la tienda te convierte en el rey intocable del ecosistema.
JORGE: Si eres fanático de la historia del software y quieres ver la cronología completa de Valve, el manual de bienvenida original con los escritorios con ruedas y las referencias bibliográficas en formato APA, revisa el artículo de investigación en escucha-sia punto github punto io.
DALIA: Y si quieres ver la recreación visual animada con la trampa del hacker, la evolución de Steam y los escritorios sobre ruedas en un Reel dinámico de cuarenta y cinco segundos, encuéntranos en TikTok y YouTube Shorts. ¡Nos escuchamos en el próximo episodio de sIA Crónicas Corporativas!
"""

EPISODE_INFO = {
    "title": "sIA Corporativo #02: Valve & Gabe Newell: De Millonarios en Microsoft al Trono de Steam (Hackers, Traición y Escritorios con Ruedas)",
    "filename": "sIA_Corp_02_Valve_Gabe_Newell_Steam_2026-10-21.mp3",
    "description": "sIA Crónicas Corporativas #02: La historia no contada de Valve Corporation y Gabe Newell. La fuga millonaria de Microsoft, el hacker alemán que filtró Half-Life 2 y la emboscada fallida del FBI, la guerra judicial contra Vivendi que dio a luz a Steam, la anarquía interna de los escritorios sobre ruedas y la matemática fría detrás de por qué jamás existirá Half-Life 3. | Leer artículo y cronología APA: https://escucha-sia.github.io/articulos/sia-corp-02-valve-gabe-newell-steam-hackers-escritorios-ruedas.html"
}

def log_to_news_vault():
    vault_data = {"covered_items": []}
    if NEWS_VAULT.exists():
        try:
            vault_data = json.loads(NEWS_VAULT.read_text(encoding='utf-8'))
        except Exception:
            pass
    vault_data["covered_items"].append({
        "title": EPISODE_INFO["title"],
        "filename": EPISODE_INFO["filename"],
        "topics": [
            "Historia corporativa de Valve y Gabe Newell desde Microsoft a 2026",
            "La filtración del código de Half-Life 2 por Axel Gembe y la trampa del FBI",
            "Litigio contra Vivendi Universal y el nacimiento forzado de Steam en 2004",
            "Cultura organizacional ultraplana: escritorios sobre ruedas y evaluación por pares",
            "Economía de plataforma: el 30% de comisión de Steam y el análisis financiero de Half-Life 3"
        ],
        "cooldown_days": 45,
        "date": "Wed, 21 Oct 2026 12:00:00 GMT"
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro añadido al archivo de memoria corporativa (news_vault.json).")

async def run():
    print("=" * 70)
    print("🎙️ INICIANDO PRODUCCIÓN: sIA CRÓNICAS CORPORATIVAS #02 (VALVE & GABE NEWELL)")
    print("=" * 70)
    
    out_mp3 = await process_dialogue(
        script_text=SCRIPT_CORP_02,
        episode_title=EPISODE_INFO["title"],
        custom_filename=EPISODE_INFO["filename"],
        episode_description=EPISODE_INFO["description"]
    )
    print(f"\n[OK] Episodio producido exitosamente: {out_mp3}")
    log_to_news_vault()
    print("\n✅ ¡Episodio sIA Corporativo #02 listo e integrado en el Feed RSS!")

if __name__ == '__main__':
    asyncio.run(run())
