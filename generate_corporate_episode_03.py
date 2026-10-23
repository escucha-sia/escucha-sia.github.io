"""
sIA Crónicas Corporativas — Episodio Especial #03
Empresa / Conflicto: Nintendo vs. Sony: La Gran Traición de 1991 y el Nacimiento de PlayStation por Pura Venganza
Formato Narrativo sIA 4.0 (Estilo Chisme Corporativo & Negocios):
1. Apertura & Brújula: sIA Crónicas Corporativas.
2. Resumen Ejecutivo & Tesis: La mayor puñalada por la espalda de la industria tecnológica y cómo la soberbia de Nintendo creó a su peor verdugo.
3. Despegue ("Alcanzarnos"): El ingeniero clandestino Ken Kutaragi y el chip SPC700.
4. El Escándalo de CES 1991: La humillación pública en Chicago frente a la prensa mundial.
5. El Golpe en la Mesa de Norio Ohga: "¡Jamás retrocedan! Constrúyanla y aplástenlos".
6. Fuera de la Burbuja: La tiranía de Hiroshi Yamauchi, el robo de Final Fantasy VII y el costo de los cartuchos de silicio.
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

SCRIPT_CORP_03 = """
[CHAPTER: Apertura & Brújula: sIA Crónicas Corporativas]
JORGE: Bienvenidos a sIA Crónicas Corporativas, el espacio donde abrimos las bóvedas secretas de la historia tecnológica para contar las guerras corporativas, los rencores personales y las traiciones que forjaron los imperios digitales modernos.
DALIA: Así es, Jorge. Y hoy traemos una de las sagas de venganza empresarial más increíbles de todos los tiempos: el choque de titanes japoneses entre Nintendo y Sony. Nuestra tesis de hoy es demoledora: la consola PlayStation, que hoy domina el mercado global de los videojuegos, no nació como un plan estratégico brillante de Sony; nació como una respuesta de pura furia y honor herido tras la humillación pública más despiadada en la historia de la electrónica de consumo.
JORGE: En los próximos diez minutos vamos a desenterrar cómo un ingeniero rebelde programó un chip a espaldas de sus jefes, la jugada sucia de Nintendo en el Consumer Electronics Show de mil novecientos noventa y uno en Chicago, el puñetazo sobre la mesa del presidente de Sony ordenando destruir a su rival, y la fuga histórica de Final Fantasy que sepultó al Nintendo sesenta y cuatro.
DALIA: Dicho esto, alcancemos el meollo del chisme: Jorge, arranquemos por finales de los años ochenta. ¿Quién era Ken Kutaragi y por qué casi lo despiden de Sony por ayudar a Nintendo?

[CHAPTER: El Ingeniero Clandestino: Ken Kutaragi y el Chip Secreto]
JORGE: Tokio, mil novecientos ochenta y ocho. Ken Kutaragi era un joven y brillante ingeniero de hardware en los laboratorios de investigación digital de Sony. Un día vio a su pequeña hija jugando con una consola Famicom, la Nintendo original, y quedó horrorizado con el sonido: eran pitidos chillones y metálicos de ocho bits que le taladraban los oídos.
DALIA: Kutaragi, obsesionado con el audio digital, entendió que el silicio podía reproducir música orquestal real. Así que contactó en secreto a los ingenieros de Nintendo para diseñarles el procesador de sonido de su próxima consola, la Super Nintendo. Pero había un pequeño problema: en Sony estaba estrictamente prohibido trabajar para otras empresas, y la alta dirección consideraba que los videojuegos eran 'juguetes baratos para niños' indignos de la marca Sony.
JORGE: Kutaragi trabajó de noche, a escondidas, en su casa. Cuando la junta directiva de Sony descubrió que uno de sus ingenieros estrella le estaba diseñando el cerebro de audio al rival, los directores exigieron su despido inmediato por insubordinación. Pero intervino el legendario CEO de Sony, Norio Ohga, un refinado cantante de ópera convertido en líder corporativo. Ohga escuchó la muestra de audio que Kutaragi había creado, el chip ese pe ce setecientos, quedó fascinado con la fidelidad acústica y autorizó el contrato con Nintendo.
DALIA: La Super Nintendo se convirtió en un éxito colosal y su sonido aplastó a la Sega Genesis. Viendo el éxito, Kutaragi convenció a Sony y a Nintendo de dar el siguiente paso: fabricar juntos un periférico de disco compacto para la Super Nintendo y una consola híbrida llamada 'Play Station', con espacio intermedio, capaz de correr tanto cartuchos tradicionales como discos ópticos.

[CHAPTER: La Humillación Pública: El Escándalo de Chicago en CES 1991]
JORGE: Parecía el matrimonio perfecto: la creatividad de Nintendo unida al músculo manufacturero de Sony. Pero había un veneno oculto en el contrato. Kutaragi y los abogados de Sony habían introducido una cláusula letal: Sony tendría el control absoluto de las licencias y las regalías de todo el software que se publicara en formato de disco compacto en todo el mundo.
DALIA: Cuando Hiroshi Yamauchi, el temido y autoritario presidente de Nintendo en Kioto, leyó esa cláusula meses después, enfureció. Yamauchi gobernaba la industria con mano de hierro: cobraba comisiones leoninas a los desarrolladores y controlaba la fabricación de cada cartucho. Si Sony se quedaba con el formato de disco compacto, Nintendo pasaba a ser un simple peón subordinado.
JORGE: En cualquier empresa normal, te sientas a renegociar el contrato en una oficina privada. Pero Yamauchi no era normal; era un estratega feudal despiadado. En mayo de mil novecientos noventa y uno, envió a sus dos máximos ejecutivos en secreto a Europa para firmar una alianza clandestina con Philips, el archirrival holandés de Sony. Y preparó la emboscada pública más salvaje de la industria.
DALIA: Junio de mil novecientos noventa y uno. La feria electrónica C E S en Chicago. El primer día, Sony convoca a cientos de periodistas internacionales y presenta con bombos y platillos la Play Station en conjunto con Nintendo. Los ejecutivos de Sony sonreían para las fotos, celebrando su entrada triunfal a los videojuegos.
JORGE: A la mañana siguiente, a las nueve en punto, le tocaba la conferencia de prensa a Nintendo. Los reporteros esperaban que confirmaran los detalles. En su lugar, el presidente de Nintendo of America subió al escenario y soltó una bomba atómica: anunció que rompían toda relación con Sony y que su nuevo socio para tecnología de disco compacto era Philips.
DALIA: ¡Piénsalo! Fue una traición televisada a nivel global. Los ejecutivos de Sony sentados en la audiencia se quedaron mudos, pálidos de la vergüenza. En la cultura corporativa japonesa, que te humillen públicamente frente a la prensa mundial no es un desacuerdo comercial; es una ofensa mortal al honor.

[CHAPTER: El Golpe en la Mesa de Norio Ohga: Venganza de Silicio]
JORGE: Julio de mil novecientos noventa y uno. Oficinas corporativas de Sony en Tokio. Reunión de emergencia al más alto nivel. Los directores más ancianos de Sony estaban furiosos y avergonzados. Le gritaron a Kutaragi: '¡Te lo advertimos! Nos rebajamos a hacer tratos con fabricantes de juguetes y nos han escupido en la cara. ¡Cancela este proyecto de inmediato y salgamos de los videojuegos!'.
DALIA: Kutaragi, acorralado frente a todos los vicepresidentes, miró a los ojos al CEO Norio Ohga y le dijo una frase que cambió el destino tecnológico del planeta: '¿De verdad vamos a aceptar que Nintendo nos pisotee y nos humille frente al mundo sin hacer nada?'.
JORGE: La sala se quedó en silencio sepulcral. Norio Ohga, rojo de ira recordando la traición de Chicago, se levantó, dio un puñetazo sobre la mesa de caoba que hizo saltar las tazas de porcelana y gritó: '¡Jamás daremos un paso atrás! ¡Kutaragi, hazlo! Desarrolla la consola tú solo, ponle gráficos en tres dimensiones y constrúyela para aplastarlos en el mercado'.
DALIA: Ahí nació la PlayStation que todos conocemos. Kutaragi abandonó la idea de hacer un accesorio para Nintendo y diseñó una bestia de arquitectura: un procesador dedicado al cálculo geométrico de polígonos en 3D y un lector de discos ópticos. Los discos costaban apenas dos dólares en fabricarse, mientras que los cartuchos de silicio de Nintendo costaban más de treinta dólares por unidad y tardaban tres meses en manufacturarse en Japón.

[CHAPTER: 🌌 Fuera de la Burbuja: La Furia de Yamauchi y la Deserción de Final Fantasy]
JORGE: Entremos a nuestra cápsula Fuera de la Burbuja Corporativa, porque el golpe de gracia no lo dio la tecnología; lo dio la soberbia de Nintendo y el maltrato a sus propios socios.
DALIA: Yamauchi estaba convencido de que los gráficos en tres dimensiones eran una moda pasajera y que los discos compactos eran una basura porque tenían tiempos de carga. Así que para el Nintendo sesenta y cuatro decidió mantener los cartuchos de memoria. Creía que su monopolio era tan fuerte que las empresas creadoras de juegos no tendrían más remedio que aguantar sus exigencias.
JORGE: Pero en mil novecientos noventa y seis, el gigante japonés Square estaba creando Final Fantasy siete. El juego era tan ambicioso, con escenas cinematográficas y música orquestal, que simplemente no cabía en un cartucho de Nintendo. Necesitaban tres discos compactos enteros. Hironobu Sakaguchi fue a rogarle a Yamauchi que cambiara a formato de disco. Yamauchi se negó rotundamente y los trató con desprecio.
DALIA: ¿Qué hizo Square? Rompió relaciones con Nintendo, empacó sus cosas y firmó exclusividad total con la PlayStation de Sony. Cuando Yamauchi se enteró, la furia fue bíblica: juró que ningún empleado de Square volvería a pisar las oficinas de Kioto jamás, una prohibición que duró casi diez años.
JORGE: La deserción de Final Fantasy provocó un efecto dominó: Capcom con Resident Evil, Konami con Metal Gear Solid y Namco con Tekken se fueron todos a PlayStation. Nintendo se quedó aislada con sus cartuchos caros. La PlayStation vendió más de ciento dos millones de consolas, destrozando al Nintendo sesenta y cuatro, que apenas logró vender treinta y dos millones. La venganza de Norio Ohga se había consumado al cien por ciento.

[CHAPTER: Veredicto Corporativo & Flywheel Tripartito]
DALIA: Veredicto de sIA Crónicas Corporativas: La soberbia y la humillación son los peores consejeros de negocios. Nintendo intentó destruir a un socio menor en una conferencia de prensa y terminó creando al monstruo más poderoso que jamás ha enfrentado.
JORGE: Si te apasiona este chisme histórico y quieres ver el contrato original de mil novecientos noventa y uno, los diagramas del chip ese pe ce setecientos y la cronología con fuentes en formato APA, revisa el artículo de investigación en escucha-sia punto github punto io.
DALIA: Y si quieres ver el Reel vertical de cuarenta y cinco segundos con la recreación animada de la traición de Chicago y la batalla de los cartuchos contra los discos, encuéntranos en TikTok y YouTube Shorts. ¡Nos escuchamos en el próximo episodio de sIA Crónicas Corporativas!
"""

EPISODE_INFO = {
    "title": "sIA Corporativo #03: Nintendo vs. Sony: La Gran Traición de 1991 y el Nacimiento de PlayStation por Pura Venganza",
    "filename": "sIA_Corp_03_Nintendo_vs_Sony_Playstation_1991_2026-10-22.mp3",
    "description": "sIA Crónicas Corporativas #03: La guerra secreta entre Nintendo y Sony. El chip clandestino de Ken Kutaragi, la humillación pública en el CES 1991 en Chicago, el puñetazo en la mesa de Norio Ohga ordenando aplastar a Nintendo, el error de los cartuchos del N64 y la histórica fuga de Final Fantasy VII a PlayStation. | Leer artículo y cronología APA: https://escucha-sia.github.io/articulos/sia-corp-03-nintendo-vs-sony-playstation-traicion-1991.html"
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
            "Guerra corporativa Nintendo vs Sony: génesis de PlayStation de 1988 a 1996",
            "El desarrollo clandestino del chip de audio SPC700 por Ken Kutaragi",
            "La traición de CES 1991 en Chicago: ruptura con Sony y anuncio con Philips",
            "La decisión de Norio Ohga de entrar al mercado de videojuegos por venganza corporativa",
            "La fuga de Square y Final Fantasy VII a CD-ROM frente a los cartuchos del N64"
        ],
        "cooldown_days": 45,
        "date": "Thu, 22 Oct 2026 12:00:00 GMT"
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro añadido al archivo de memoria corporativa (news_vault.json).")

async def run():
    print("=" * 70)
    print("🎙️ INICIANDO PRODUCCIÓN: sIA CRÓNICAS CORPORATIVAS #03 (NINTENDO VS SONY)")
    print("=" * 70)
    
    out_mp3 = await process_dialogue(
        script_text=SCRIPT_CORP_03,
        episode_title=EPISODE_INFO["title"],
        custom_filename=EPISODE_INFO["filename"],
        episode_description=EPISODE_INFO["description"]
    )
    print(f"\n[OK] Episodio producido exitosamente: {out_mp3}")
    log_to_news_vault()
    print("\n✅ ¡Episodio sIA Corporativo #03 listo e integrado en el Feed RSS!")

if __name__ == '__main__':
    asyncio.run(run())
