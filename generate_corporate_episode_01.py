"""
sIA Crónicas Corporativas — Episodio Especial #01
Empresa: NVIDIA: De Lavar Platos en Denny's al Imperio de 3 Billones
Formato Narrativo sIA 4.0 (Estilo Chisme Corporativo & Negocios):
1. Apertura & Brújula: sIA Crónicas Corporativas.
2. Resumen Ejecutivo & Tesis: El mito de Silicon Valley vs. el barro de Denny's y cheques rebotados.
3. Despegue ("Alcanzarnos"): El desayuno de 1993, hot cakes y servilletas manchadas.
4. La Apuesta Suicida: La confesión a Sega y el rescate milagroso con RIVA 128.
5. Sangre en la Sala de Juntas: La muerte de 3dfx y el choque con Steve Ballmer y Xbox.
6. Fuera de la Burbuja: La cultura de Jensen, el correo de 3 líneas y la solitaria apuesta de 15 años en CUDA.
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

SCRIPT_CORP_01 = """
[CHAPTER: Apertura & Brújula: sIA Crónicas Corporativas]
JORGE: Bienvenidos al estreno de sIA Crónicas Corporativas, el espacio donde abrimos las puertas traseras de Silicon Valley para contar la historia real de las empresas que cambiaron el mundo: sin el filtro de relaciones públicas, con todo el chisme de oficina, las traiciones en las salas de juntas y las apuestas suicidas del día a día.
DALIA: Así es, Jorge. Y para inaugurar esta serie, teníamos que empezar con el titán absoluto del momento: NVIDIA. Hoy vale más de tres billones de dólares y domina el noventa por ciento del silicio para inteligencia artificial en el planeta. Pero la tesis de hoy es que NVIDIA no nació en un garaje glamoroso ni con una ronda millonaria de inversionistas; nació en una mesa grasienta de un restaurante Denny's, comiendo huevos fríos, esquivando tiroteos en San José y a punto de quebrar no una, sino cuatro veces.
JORGE: En los próximos diez minutos vamos a desenterrar cómo Jensen Huang pasó de lavar platos y limpiar baños a los quince años a convertirse en el CEO más temido de la industria, la traición involuntaria a Sega que casi los destruye, la guerra a muerte con Steve Ballmer por la primera Xbox, y la despiadada cultura del correo de tres líneas a las dos de la mañana.
DALIA: Dicho esto, alcancemos el meollo del chisme: Jorge, arranquemos por ese desayuno de mil novecientos noventa y tres. ¿Quiénes eran estos tres tipos y por qué se reunían en un Denny's de mala muerte?

[CHAPTER: El Desayuno de 1993: Denny's, Café Frío y Servilletas Manchadas]
JORGE: Mil novecientos noventa y tres. East San Jose, California. Un Denny's al lado de la autopista con agujeros de bala en el letrero. Jensen Huang, que en ese momento tenía treinta años y era ingeniero en LSI Logic, se reúne con Chris Malachowsky y Curtis Priem, dos ingenieros de Sun Microsystems que estaban hartos de sus jefes.
DALIA: Y el detalle cotidiano es genial: no tenían oficina, no tenían dinero para alquilar un garaje y elegían Denny's porque el café tenía refill infinito y las meseras los dejaban quedarse cuatro horas seguidas siempre que pidieran un plato de hot cakes. Jensen ya conocía el lugar a la perfección: de adolescente en Oregon había trabajado ahí lavando platos y limpiando baños. Él mismo cuenta que aprendió a trabajar bajo presión limpiando platos grasosos lo más rápido posible.
JORGE: Entre hot cakes con miel y tazas de café aguado, dibujaban diagramas de procesadores gráficos en servilletas de papel. Los tres compartían una obsesión: la computación basada en tres dimensiones para videojuegos. En esa época el mercado de gráficos 3D para PC prácticamente no existía. Cuando Jensen le dijo a su madre que iba a fundar una empresa para hacer chips de videojuegos, su madre le respondió: '¿Por qué no mejor buscas un trabajo de verdad?'.
DALIA: Pero consiguieron dos millones de dólares de capital de riesgo y fundaron la compañía. Al principio ni siquiera tenían nombre. Llamaban a sus archivos 'NV', por 'Next Version'. Hasta que buscaron en el diccionario palabras en latín y encontraron 'invidia', que significa envidia. Querían que la competencia se muriera de envidia. Y vaya que lo lograron, pero antes estuvieron a punto de morir de hambre.

[CHAPTER: La Apuesta Suicida: La Traición Involuntaria a Sega y el RIVA 128]
JORGE: El primer chip, el NV1, lanzado en mil novecientos noventa y cinco, fue un desastre monumental. Decidieron construirlo usando superficies cuadriláteras curvas en lugar de polígonos triangulares. Y justo en ese momento, Microsoft lanza Windows noventa y cinco y Direct3D, estandarizando los triángulos para toda la industria. El chip de NVIDIA era matemáticamente incompatible con todos los juegos nuevos.
DALIA: Y aquí viene el primer gran chisme de supervivencia. NVIDIA había firmado un contrato millonario con Sega para fabricar el procesador gráfico de la consola Dreamcast. Sega ya les había adelantado millones de dólares. Jensen se dio cuenta de que la tecnología de cuadriláteros que le estaban vendiendo a Sega era un callejón sin salida. Si seguían, Sega fracasaría; si paraban, NVIDIA quebraba al instante.
JORGE: ¿Y qué hizo Jensen? Se subió a un avión a Japón, se sentó con Shoichiro Irimajiri, el mítico CEO de Sega, y le confesó en la cara: 'Nuestra arquitectura está mal. Si la usamos, tu consola perderá. Tenemos que parar el proyecto... pero si cancelas el contrato y no nos pagas los últimos cinco millones de dólares, mi empresa irá a la quiebra'.
DALIA: ¡Piénsalo por un segundo! Vas con tu cliente, le dices que tu producto no sirve, y le pides que te regale cinco millones de dólares de caridad para no quebrar. Lo increíble es que el CEO de Sega, conmovido por la brutal honestidad de Jensen y creyendo en su talento, le autorizó los cinco millones de dólares. Ese dinero le dio a NVIDIA exactamente seis meses de vida.
JORGE: Con treinta días de dinero en el banco, Jensen despidió a la mitad de la plantilla. Los ingenieros restantes dormían debajo de los escritorios. Se la jugaron a un solo tiro de dados: el chip RIVA 128. Si ese chip fallaba en el laboratorio, la empresa desaparecía en treinta días. Lanzaron el RIVA 128 en mil novecientos noventa y siete, soportaba triángulos a toda velocidad y vendieron un millón de unidades en cuatro meses. Se salvaron por un pelo de rana.

[CHAPTER: Sangre en la Sala de Juntas: La Venganza de 3dfx y la Pelea con Xbox]
DALIA: A finales de los noventa el rey indiscutible de las tarjetas gráficas no era NVIDIA; era 3dfx con sus legendarias tarjetas Voodoo. Todo el mundo quería una Voodoo para jugar Quake y Unreal. Pero a 3dfx le dio el ataque clásico de soberbia corporativa: decidieron fabricar sus propias tarjetas, pelearon con sus distribuidores y retrasaron sus lanzamientos.
JORGE: Mientras 3dfx se dormía en los laureles, Jensen impuso un ritmo despiadado: una arquitectura completamente nueva cada seis meses. Era un ritmo suicida para los ingenieros, pero en el año dos mil lanzaron la GeForce 256, acuñaron el término 'GPU', y quebraron a 3dfx. Y con una frialdad quirúrgica, NVIDIA compró todas las patentes y restos de 3dfx por una miseria.
DALIA: Pero luego llegó el choque de trenes con Microsoft. En el año dos mil uno, Bill Gates eligió a NVIDIA para fabricar el chip gráfico y de sonido de la primera consola Xbox. Parecía el contrato de ensueño, pero se convirtió en una pesadilla. Los costos de fabricación de la consola eran altísimos y Microsoft perdía dinero por cada Xbox vendida.
JORGE: Steve Ballmer llamó a Jensen exigiendo rebajar el precio de los chips a la fuerza. Jensen se negó rotundamente: 'Un contrato firmado es un contrato'. Ballmer enfureció. La pelea terminó en un arbitraje legal sangriento. NVIDIA ganó el arbitraje y cobró cada centavo, pero Microsoft juró venganza y para la Xbox 360 se fue directamente con su archirrival, ATI. Jensen aprendió a la mala que ganar una batalla legal puede costarte el negocio de consolas.

[CHAPTER: 🌌 Fuera de la Burbuja: La Tortura de Jensen, la Chaqueta de Cuero y el Correo de 3 Líneas]
DALIA: Llegamos a nuestra cápsula Fuera de la Burbuja Corporativa, porque el mito del líder carismático con chaqueta de cuero esconde una de las culturas laborales más implacables y estresantes de todo el planeta tech.
JORGE: Empecemos por la icónica chaqueta negra de cuero. Jensen la usa todo el año, haga frío en Nueva York o haya cuarenta grados de calor en Taiwán. Su esposa y su hija se la compraron hace más de una década para que no perdiera tiempo eligiendo ropa, y se convirtió en su armadura de batalla. Pero detrás de la chaqueta hay un micro-gestor legendario.
DALIA: En NVIDIA no existen las evaluaciones de desempeño privadas uno a uno. Jensen las odia. Su filosofía es: 'Si alguien comete un error, se lo digo frente a todos en la sala de juntas para que las cincuenta personas presentes aprendan la lección'. Los directores describen esas reuniones como una sala de operaciones donde te diseccionan vivo si no tienes el dato exacto de ingeniería.
JORGE: Jensen tiene más de cincuenta subordinados directos. No cree en las jerarquías intermedias. Y todo empleado debe enviarle periódicamente un correo con sus cinco cosas más importantes del momento. Jensen lee miles de correos y responde a las dos o tres de la mañana con respuestas demoledoras de exactamente tres líneas: 'Esto está mal. Corrígelo ahora. Llámame en cinco minutos'.
DALIA: Y está la mayor apuesta incomprendida de la historia: CUDA en dos mil seis. Jensen decidió meter núcleos de cómputo general en cada una de las tarjetas gráficas para que sirvieran para simulaciones científicas, encareciendo los chips un treinta por ciento. Wall Street castigó la acción, los analistas decían que Jensen estaba destruyendo los márgenes de la empresa en una locura sin mercado, y la acción se desplomó un ochenta por ciento.
JORGE: Jensen aguantó la respiración durante quince años seguidos perdiendo dinero en software que casi nadie usaba... hasta que en dos mil doce los investigadores de Deep Learning descubrieron que las redes neuronales corrían mil veces más rápido en CUDA que en CPUs tradicionales. La apuesta de quince años dio en el blanco más grande de la historia financiera.

[CHAPTER: Veredicto Corporativo & Flywheel Tripartito]
DALIA: Veredicto de sIA Crónicas Corporativas: NVIDIA no domina el mundo por suerte ni por un golpe de genialidad repentino. Domina porque su fundador sigue operando cada mañana con el terror visceral de que la empresa va a quebrar en treinta días. De lavar platos con agua hirviendo a los quince años a controlar los cerebros de silicio de la inteligencia artificial moderna.
JORGE: Si te apasiona el chisme corporativo y quieres ver la cronología completa con los balances financieros, las fotos de la servilleta de Denny's y la bibliografía en formato APA, revisa el artículo de investigación en escucha-sia punto github punto io.
DALIA: Y si quieres ver el mapa visual animado con la evolución desde la mesa de Denny's hasta el chip H100 en un Reel dinámico de cuarenta y cinco segundos, encuéntranos en TikTok y YouTube. ¡Nos vemos en el próximo episodio de sIA Crónicas Corporativas!
"""

EPISODE_INFO = {
    "title": "sIA Corporativo #01: NVIDIA: De Lavar Platos en Denny's al Imperio de 3 Billones (Chisme, Traición y el Correo de 3 Líneas)",
    "filename": "sIA_Corp_01_NVIDIA_Dennys_a_3_Billones_2026-10-20.mp3",
    "description": "sIA Crónicas Corporativas #01: La historia sin censura de NVIDIA. De lavar platos en un Denny's de San José al imperio de 3 billones. La confesión desesperada a Sega, la quiebra evitada con el RIVA 128, la guerra a muerte con Steve Ballmer por la Xbox, los 15 años de sangría con CUDA y la cultura despiadada del correo de 3 líneas de Jensen Huang. | Leer artículo y cronología financiera: https://escucha-sia.github.io/articulos/sia-corp-01-nvidia-historia-chisme-corporativo-dennys-3-billones.html"
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
            "Historia corporativa de NVIDIA desde 1993 a 2026 (Denny's diner origins)",
            "Quiebra evitada con Sega y desarrollo del RIVA 128",
            "Disputa de arbitraje legal con Steve Ballmer y Microsoft Xbox",
            "La apuesta de 15 años en CUDA y el auge de aceleración para Deep Learning",
            "Cultura interna de Jensen Huang: estructura plana de 50 directos y microgestión por correos de 3 líneas"
        ],
        "cooldown_days": 45,
        "date": "Tue, 20 Oct 2026 12:00:00 GMT"
    })
    NEWS_VAULT.write_text(json.dumps(vault_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("✅ Registro añadido al archivo de memoria corporativa (news_vault.json).")

async def run():
    print("=" * 70)
    print("🎙️ INICIANDO PRODUCCIÓN: sIA CRÓNICAS CORPORATIVAS #01 (NVIDIA)")
    print("=" * 70)
    
    out_mp3 = await process_dialogue(
        script_text=SCRIPT_CORP_01,
        episode_title=EPISODE_INFO["title"],
        custom_filename=EPISODE_INFO["filename"],
        episode_description=EPISODE_INFO["description"]
    )
    print(f"\n[OK] Episodio producido exitosamente: {out_mp3}")
    log_to_news_vault()
    print("\n✅ ¡Episodio sIA Corporativo #01 listo e integrado en el Feed RSS!")

if __name__ == '__main__':
    asyncio.run(run())
