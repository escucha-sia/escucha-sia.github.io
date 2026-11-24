"""
sIA Master Episode Producer:
Tema: Material Jetting (PolyJet): ¿Cómo la inyección de tinta microscópica está revolucionando la medicina y la manufactura 3D?
Pipeline Soberano:
1. Audio Podcast Completo (Jorge & Dalia, Capítulos con metadatos ID3/EBU R128)
2. Síntesis Neural Edge-TTS en Español de México
3. Masterización y normalización automática a -16 LUFS
4. Exportación a Biblioteca Local de Spotify (C:\\Users\\c_a_c\\Music\\NoticIAs)
5. Sincronización automática a Google Drive (G:\\Mi unidad\\sIA_Hub\\02_Podcasts_Audio)
"""

import sys
import os
import shutil
import asyncio
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = BASE_DIR / "audio"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
GDRIVE_HUB = Path(r"G:\Mi unidad\sIA_Hub")
GDRIVE_AUDIO = GDRIVE_HUB / "02_Podcasts_Audio"

EPISODE_FILENAME = "sIA_Maker_03_Material_Jetting_Impresion3D_2026-11-23.mp3"

FULL_SCRIPT = """
[CHAPTER: Apertura: El Volcán Imposible y la Paradoja de la Impresora]
JORGE: ¡Muy buenas tardes a toda nuestra comunidad maker, ingenieros de diseño y apasionados de la tecnología en México y toda Latinoamérica! Bienvenidos a un nuevo episodio de sIA. Soy Jorge.
DALIA: ¡Y yo soy Dalia! Hoy es lunes veintitrés de noviembre de dos mil veintiséis. Y hoy vamos a derribar una frontera mental. Jorge, si le preguntas a cualquier persona en la calle cómo funciona una impresora 3D, te dirán que es una máquina derritiendo hilo de plástico o una tina con líquido pegajoso y olor químico.
JORGE: Totalmente, Dalia. El noventa y nueve por ciento del mundo piensa exclusivamente en filamento fundido tipo Bambu Lab o en resina tradicional curada con pantalla LCD. Pero esta semana se volvió viral un video en talleres de manufactura mostrando algo que parece de ciencia ficción: un diorama en miniatura donde un volcán expulsa lava incandescente transparente, mientras ríos congelados y rocas ásperas conviven en una sola pieza de plástico sin una sola gota de pintura exterior.
DALIA: No fue pintado a mano, ni ensamblado con pegamento. Salió de la bandeja en una sola corrida continua. La tecnología detrás de esa proeza se conoce como Material Jetting, comercializada históricamente bajo el nombre PolyJet. Y lo más fascinante es su origen conceptual: funciona exactamente igual que la humilde impresora de inyección de tinta que tienes en tu oficina.
JORGE: En este episodio vamos a desarmar la física de esta maravilla: cabezales piezoeléctricos disparando microgotas, curado ultravioleta en milisegundos, materiales digitales que mezclan piel de goma con hueso duro, y la forma en que los cirujanos están usando estas máquinas para salvar vidas operando réplicas exactas de tumores antes de tocar al paciente. ¡Comenzamos!

[CHAPTER: La Física Oculta: Cabezales Piezoeléctricos y Curado Ultravioleta]
DALIA: Para entender por qué el Material Jetting es radicalmente distinto al resto de la industria, tenemos que viajar al interior del cabezal de impresión.
JORGE: Imaginen los cabezales térmicos o piezoeléctricos de una impresora de papel Epson o Canon de alta definición. Esos cabezales contienen cientos de micro-boquillas microscópicas capaces de disparar picolitros de líquido. Un picolitro es la billonésima parte de un litro; estamos hablando de gotas más finas que un glóbulo rojo humano.
DALIA: Pero aquí viene la genialidad de ingeniería: en lugar de disparar tinta convencional a base de agua o solvente, el cabezal de Material Jetting eyecta microgotas de fotopolímeros líquidos.
JORGE: Y pegada al carro del cabezal, viajando a toda velocidad de lado a lado de la bandeja, viaja una lámpara ultravioleta de alta potencia. En el instante microscópico en que la gota toca la plataforma, la luz UV la bombardea, provocando una reacción de polimerización en cadena. El líquido se solidifica al milisegundo.
DALIA: Esto elimina por completo el mayor dolor de cabeza de la impresión de resina tradicional en tina: ya no tienes que sumergir una pieza en litros de químicos tóxicos, ni lidiar con fuerzas de succión que deforman capas delgadas al despegarse del fondo de la película de teflón.
JORGE: Aquí el material solo se deposita donde el modelo matemático lo exige. Y lo que es más impresionante: la resolución vertical alcanza capas de hasta dieciséis micras. Para ponerlo en perspectiva, un cabello humano mide unas setenta micras. Es una superficie tan lisa que el ojo no puede detectar las líneas de capa a simple vista.

[CHAPTER: CMYK, Transparencias y Materiales Digitales]
DALIA: Pero la verdadera magia no es solo la resolución geométrica, Jorge. Es la capacidad multimaterial simultánea.
JORGE: En una impresora de filamento tradicional con sistema multimaterial como el AMS, para cambiar de color la máquina tiene que cortar el hilo, purgar la boquilla en una torre de desperdicio y empujar el nuevo filamento. Tarda minutos y genera montañas de plástico de desecho.
DALIA: En Material Jetting, el carro lleva múltiples canales en paralelo. Tienes cabezales dedicados para cian, magenta, amarillo, negro, blanco, resina transparente cristalina y resinas elastoméricas flexibles.
JORGE: Esto permite dos cosas que ninguna otra tecnología en el planeta puede igualar. La primera es el color CMYK fotográfico real. La impresora no solo colorea la superficie: mezcla las microgotas en el aire y en la capa para generar millones de tonos con degradados continuos, emulando texturas de madera, mármol o piel humana con fidelidad milimétrica.
DALIA: Y la segunda, y para mí la más revolucionaria, es lo que Stratasys denomina Materiales Digitales. La máquina puede mezclar en proporciones calculadas una resina rígida con una resina flexible. Esto significa que puedes variar la dureza Shore en una misma pieza sin transiciones visibles.
JORGE: Imaginen esto: pueden imprimir un zapato o una prótesis donde la suela exterior sea blanda y amortiguada como hule espuma, pero la estructura interna sea rígida como el policarbonato, y la parte superior sea semitransparente como malla técnica. Todo en un solo bloque monolítico sin ensambles.

[CHAPTER: Medicina Quirúrgica de Alto Riesgo: Réplicas que Sangran]
DALIA: Y donde esta tecnología deja de ser un truco de ingeniería fascinante y se convierte en un milagro tangible es en los quirófanos pediátricos y de cardiología.
JORGE: Históricamente, cuando un cirujano se enfrentaba a un tumor complejo o a una malformación cardíaca congénita en un bebé, tenía que depender de tomografías axiales y resonancias en pantallas bidimensionales. El cirujano tenía que imaginar en su mente la profundidad espacial antes de hacer la primera incisión en un órgano del tamaño de una nuez.
DALIA: Hoy, hospitales de máxima especialidad toman la tomografía del paciente, segmentan el volumen con algoritmos de inteligencia artificial y envían el archivo a una impresora como la Stratasys J850 Digital Anatomy.
JORGE: La máquina imprime una copia uno a uno del corazón del paciente. Pero escuchen esto: el tejido muscular tiene la misma elasticidad y resistencia que el miocardio vivo. Las arterias coronarias se imprimen en resina transparente flexible para que el equipo médico pueda ver la sangre pasar o insertar catéteres.
DALIA: E incluso se imprimen patologías tumorales con diferente densidad y textura táctil. Los cirujanos pueden cortar el modelo con el bisturí real, coser suturas y practicar el procedimiento tres o cuatro veces la noche anterior a la cirugía. Se ha demostrado que reduce los tiempos de quirófano en más de dos horas y disminuye drásticamente las complicaciones postoperatorias.
JORGE: Saber exactamente dónde está anclado el vaso sanguíneo antes de abrir el pecho de una persona marca la diferencia literal entre la vida y la muerte.

[CHAPTER: El Negocio, las Patentes y la Barrera de Entrada]
DALIA: Ahora bien, Jorge, la pregunta del millón que todos nuestros radioescuchas se estarán haciendo en este momento es: ¿por qué no tenemos todos una impresora PolyJet en nuestra mesa de trabajo?
JORGE: La respuesta corta es: patentes y economía corporativa. Una impresora industrial de Material Jetting no baja de los cincuenta mil dólares, y las estaciones médicas de última generación superan los doscientos cincuenta mil dólares.
DALIA: Y el modelo de negocio es el clásico monopolio de los cartuchos de impresora llevado al extremo. Mientras un kilo de filamento PLA de excelente calidad cuesta hoy unos quince o dieciocho dólares, un cartucho de resina oficial para estas máquinas puede costar fácilmente entre trescientos y cuatrocientos dólares el kilo.
JORGE: Las resinas están fuertemente protegidas por microchips criptográficos propietarios. Si le pones una resina genérica, la máquina simplemente se niega a disparar los cabezales.
DALIA: Sin embargo, al igual que ocurrió con las patentes de FDM en dos mil nueve que detonaron la revolución RepRap, el ecosistema de patentes originales de PolyJet de finales de los noventa y principios de los dos mil ha comenzado a expirar paulatinamente.
JORGE: Ya estamos viendo pioneros en Asia y proyectos de investigación en universidades europeas adaptando cabezales piezoeléctricos piezo-inkjet estándar de gran formato con tintas fotocurables de código abierto. La democratización de la inyección de materiales líquidos es la próxima gran frontera que veremos madurar en esta década.

[CHAPTER: Cierre y Recursos en sIA Journal]
DALIA: La frontera entre imprimir una fotografía plana en una hoja de papel y construir un órgano tridimensional complejo está desapareciendo. La materia se está volviendo programable a nivel de picolitros.
JORGE: Y con esta radiografía profunda sobre el futuro de la fabricación aditiva cerramos este episodio especial de sIA Maker.
DALIA: Como siempre, las notas del programa, los esquemas técnicos del cabezal piezoeléctrico y los enlaces a los estudios clínicos están disponibles en nuestra revista digital en escucha guion sia punto github punto io diagonal articulos.
JORGE: Y si nos escuchan en Spotify, recuerden calificar el podcast con cinco estrellas y compartir este episodio con sus colegas makers e ingenieros. Soy Jorge.
DALIA: Y yo soy Dalia. ¡Hasta la próxima entrega de sIA Podcast!
"""

async def produce():
    print("="*70)
    print("🚀 PRODUCCIÓN SOBERANA DE EPISODIO: Material Jetting (PolyJet)")
    print("="*70)

    from podcast_synthesizer import process_dialogue

    ep_info = {
        "title": "sIA Maker #03: Material Jetting (PolyJet): ¿Cómo la inyección de tinta microscópica revoluciona la medicina y el 3D?",
        "filename": EPISODE_FILENAME,
        "description": "Análisis técnico y estratégico sobre la tecnología Material Jetting (PolyJet): cabezales piezoeléctricos disparando microgotas de fotopolímeros, curado UV instantáneo, materiales digitales con dureza Shore variable, réplicas quirúrgicas hiperrealistas de órganos y la batalla por la democratización de patentes por cacs."
    }

    print("\n🎙️ Sintetizando audio completo con Jorge y Dalia...")
    out_path = await process_dialogue(FULL_SCRIPT, ep_info, custom_filename=EPISODE_FILENAME)
    print(f"\n✅ Audio masterizado exitosamente: {out_path}")

    # Copy to Google Drive Hub if available
    try:
        GDRIVE_AUDIO.mkdir(parents=True, exist_ok=True)
        gdrive_target = GDRIVE_AUDIO / EPISODE_FILENAME
        shutil.copy2(str(out_path), str(gdrive_target))
        print(f"☁️ Sincronizado a Google Drive: {gdrive_target}")
    except Exception as e:
        print(f"⚠️ No se pudo copiar a Google Drive: {e}")

    # Verify Spotify Local Files
    spotify_target = SPOTIFY_DIR / EPISODE_FILENAME
    if spotify_target.exists():
        print(f"🎧 Disponible en Spotify Archivos Locales: {spotify_target}")
    else:
        try:
            shutil.copy2(str(out_path), str(spotify_target))
            print(f"🎧 Copiado a Spotify Archivos Locales: {spotify_target}")
        except Exception as e:
            print(f"⚠️ Error al copiar a Spotify: {e}")

    print("\n🎉 ¡Episodio producido y distribuido al 100%!")

if __name__ == "__main__":
    asyncio.run(produce())
