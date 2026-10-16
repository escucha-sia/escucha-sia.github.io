"""
sIA Terror: Crónicas de Reddit — Episodio Especial #01
Historia: "Las Escaleras Perdidas en el Bosque Profundo" (r/nosleep)
Formato: Narración inmersiva, tensión atmosférica, historia cerrada con conclusión contundente.
Embudo: TikTok (Hook escalofriante) -> Spotify (Historia completa 6 min) -> Blog (Adaptación escrita protegida).
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

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
HORROR_VAULT = BASE_DIR / "horror_vault.json"

SCRIPT_HORROR_01 = """
[CHAPTER: Prólogo: La Regla de los Parques Nacionales]
JORGE: Hay una orden estricta que todo oficial de búsqueda y rescate novato aprende en su primera semana en los bosques del norte. No está en los manuales oficiales de guardabosques. Nadie la menciona frente a los turistas. Pero los veteranos te la repiten al oído antes de entrar a zonas vírgenes: si en mitad de la maleza densa, a kilómetros de cualquier camino, encuentras un tramo de escaleras de concreto o madera pulida parada sola en medio de la nada... jamás te acerques. Y bajo ninguna circunstancia subas por ellas.
DALIA: Parece una broma de bienvenida para asustar novatos. Una leyenda de fogata inventada por gente aburrida en turnos de doce horas. Pero cuando llevas tres años rastreando excursionistas desaparecidos, dejas de reírte. El bosque no es pacífico, Jorge. El bosque salvaje es una masa indiferente de kilómetros de sombras donde las leyes humanas no significan nada. Y esas estructuras no tienen cimientos. No hay ruinas alrededor. No hay clavos oxidados ni vigas podridas de una cabaña inexistente. Es simplemente una escalera solitaria, perfectamente limpia, elevándose hacia las copas de los pinos como si hubiera sido recortada de una casa suburbana y arrojada por una fuerza invisible en medio de la niebla.

[CHAPTER: El Encuentro en el Valle Profundo]
JORGE: Ocurrió a mediados de otoño, en una expedición para localizar a un joven de veinte años que se había separado de su grupo de senderismo cerca de la cuenca del río. Habían pasado cuatro días. Cuando encuentras a una persona tras cuatro días en clima de congelación, el protocolo suele cambiar de rescate a recuperación de cuerpo. Pero este chico seguía dejando huellas erráticas, caminando en círculos perfectos sobre la hojarasca seca.
DALIA: El equipo se dividió en parejas. Yo iba con un oficial veterano, un tipo con más de quince años de servicio que conocía cada risco y quebrada de esa cordillera. Hacia las tres de la tarde, la niebla bajó tan espeso que apenas podíamos ver a diez metros. Y entonces, el silencio se volvió absoluto. Si alguna vez has estado en un bosque denso, sabes que el silencio total no existe: siempre hay viento entre las ramas, crujido de insectos, el llamado distante de un cuervo. Pero en ese claro, el mundo pareció quedarse mudo, como si alguien hubiera puesto en pausa la realidad.
JORGE: Y ahí estaba. Una escalera de madera de roble barnizada, con cinco escalones y un pasamanos tallado a mano, emergiendo directamente de la tierra húmeda. Sin una sola brizna de musgo. Sin hojas caídas sobre los peldaños. Brillaba con un lustre perfecto, como si alguien la hubiera encerado cinco minutos antes. Mi compañero me tomó con fuerza del hombro y me susurró con la voz temblorosa: no la mires directo. Camina en dirección contraria y no hagas ruido.

[CHAPTER: La Tentación y el Clímax]
DALIA: Pero el novato del equipo dos, que avanzaba a trescientos metros al este por radio, no tuvo la misma disciplina. Por el transmisor escuchamos su respiración agitada. Decía que había encontrado algo raro. Una escalera de caracol de hierro forjado en una meseta rocosa. Le gritamos por el canal de emergencia que retrocediera de inmediato. Pero la curiosidad morbosa es una trampa mortal en la montaña. El novato dijo por radio: solo voy a subir al primer escalón para tener una mejor vista del valle.
JORGE: En cuanto su bota tocó el metal, la estática en la radio se convirtió en un zumbido agudo insoportable, como un chirrido de frecuencias que te perfora los tímpanos. Luego un grito seco, no de dolor, sino de puro terror primordial. Cuando llegamos al sitio diez minutos después, la escalera seguía ahí. Impecable. Pero el oficial novato estaba sentado al pie de la estructura, con la mirada completamente vacía, mirando al cielo gris sin parpadear.
DALIA: Su mano izquierda, la que había tocado el pasamanos superior, ya no estaba. No había sangre en la tierra ni signos de mordedura animal. Simplemente el corte era plano, microscópicamente perfecto, como si el tejido biológico y los huesos hubieran sido rebanados a nivel atómico en el límite exacto del último escalón. El novato nunca volvió a hablar una sola palabra coherente; pasó los siguientes seis meses en una institución psiquiátrica dibujando escaleras infinitas en las paredes de su cuarto.

[CHAPTER: Cierre: La Advertencia Final]
JORGE: Las montañas de Norteamérica y los grandes bosques del mundo guardan anomalías que la ciencia formal se niega a catalogar porque destruirían nuestra ilusión de control sobre la geografía. Quienes recorremos esos senderos lo sabemos: la naturaleza no siempre es naturaleza. A veces es una trampa con arquitectura propia.
DALIA: Si alguna vez sales a caminar lejos de los senderos marcados y entre la niebla ves una escalera de madera o concreto erguida en el vacío... no te acerques. No tomes una foto. Da media vuelta despacio, no corras, y reza para que la escalera no se mueva hacia ti.
JORGE: Este relato fue adaptado del testimonio original de guardabosques publicado en r diagonal nosleep. Puedes leer la crónica literaria completa y el análisis de anomalías espaciales en nuestra revista digital protegida en escucha-sia punto github punto io.
DALIA: Y si quieres compartir esta advertencia con alguien que ame el senderismo, ya tienes disponible el Reel vertical en nuestras redes. Nos vemos... en las sombras del siguiente sIA Terror.
"""

async def generate_horror_01():
    print("=" * 70)
    print("🎬 GENERANDO sIA TERROR #01: LAS ESCALERAS EN EL BOSQUE PROFUNDO")
    print("=" * 70)

    title = "sIA Terror #01: Las Escaleras Perdidas en el Bosque Profundo (Relatos de Reddit)"
    filename = "sIA_Terror_01_Las_Escaleras_del_Bosque_2026-10-15.mp3"
    
    # 1. Sintetizar con podcast_synthesizer
    print("\n🎙️ Sintetizando audio inmersivo con Jorge y Dalia...")
    audio_path = await process_dialogue(
        script_text=SCRIPT_HORROR_01,
        episode_title=title,
        custom_filename=filename
    )
    print(f"✅ Audio generado en: {audio_path}")

    # 2. Registrar en horror_vault.json para garantizar CERO duplicación
    if HORROR_VAULT.exists():
        with open(HORROR_VAULT, "r", encoding="utf-8") as f:
            vault = json.load(f)
        
        narrated_entry = {
            "story_id": "stairs_in_the_woods_01",
            "reddit_source": "r/nosleep",
            "reddit_author": "searchandrescuewoods",
            "title": title,
            "filename": filename,
            "date_narrated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "COMPLETED",
            "cooldown": "PERMANENT",
            "summary": "Oficial de búsqueda y rescate relata el terror inexplicable de las escaleras abandonadas en parques nacionales y la mutilación espacial de quienes las suben."
        }
        vault.setdefault("narrated_stories", []).append(narrated_entry)
        
        # Actualizar pipeline para quitarlo de READY_TO_PRODUCE
        for item in vault.get("curated_master_pipeline", []):
            if item["story_id"] == "stairs_in_the_woods_01":
                item["status"] = "COMPLETED"
                break
                
        with open(HORROR_VAULT, "w", encoding="utf-8") as f:
            json.dump(vault, f, indent=2, ensure_ascii=False)
        print("🔒 Historia registrada en horror_vault.json: COOLDOWN PERMANENTE (Cero repetición garantizado).")

    return audio_path

if __name__ == '__main__':
    asyncio.run(generate_horror_01())
