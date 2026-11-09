import os
import sys
import math
import json
import shutil
import asyncio
import hashlib
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
ARTICULOS_DIR = BASE_DIR / "articulos"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
SPOTIFY_REELS_DIR = SPOTIFY_DIR / "Reels"
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
GDRIVE_AUDIO_DIR = Path(r"G:\Mi unidad\sIA_Hub\03_Audios_Completos")
ARTIFACT_DIR = Path(r"C:\Users\c_a_c\.gemini\antigravity\brain\3d3829e3-9423-4249-b4ec-672aaf684c20")
NODE_PATH = r"C:\Carlos\nodejs"

EPISODE_FILENAME = "sIA_Corp_09_Pascual_Boing_Cooperativa_TetraPak_2026-11-08.mp3"
REEL_FILENAME = "sIA_Storybook_15_Pascual_Boing_Cooperativa_TetraPak.mp4"
REEL_POSTER_FILENAME = "sIA_Storybook_15_Pascual_Boing_Cooperativa_TetraPak_poster.jpg"

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

STORY_IMAGES = {
    "img1": ARTIFACT_DIR / "pascual_scene1_1982_strike_1794145992905.jpg",
    "img2": ARTIFACT_DIR / "pascual_scene2_tetrapak_cutaway_1794146010306.jpg",
    "img3": ARTIFACT_DIR / "pascual_scene3_pulp_factory_1794146026806.jpg",
    "img4": ARTIFACT_DIR / "pascual_scene4_cooperative_triumph_1794146045072.jpg",
    "img5": ARTIFACT_DIR / "pascual_scene5_omnicanal_car_1794146063838.jpg",
}

DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 1,
        "img": "assets/pascual_img1.jpg",
        "tag": "CAPÍTULO 01 • LA HUELGA DE 1982",
        "headline": "EL ENFRENTAMIENTO EN SAN RAFAEL",
        "pill": "LA CRISIS DEL PATRÓN PASCUAL",
        "caption_short": "En mayo de 1982, tras la devaluación del peso, los obreros exigieron el aumento salarial por ley. La empresa cerró las puertas.",
        "text": "¿Cómo una empresa refresquera mexicana cuyos dueños amenazaron con quebrar antes de pagar un aumento salarial se convirtió en una cooperativa obrera que hoy factura miles de millones de pesos? Bienvenidos a sIA Podcast. Hoy abrimos nuestro cuento industrial en mayo de 1982, cuando el presidente López Portillo decretó un aumento salarial de emergencia por la devaluación del peso. En la fábrica de Refrescos Pascual, en la colonia San Rafael, el dueño Rafael Jiménez se negó rotundamente a pagarlo."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 1,
        "img": "assets/pascual_img1.jpg",
        "tag": "CAPÍTULO 01 • RESISTENCIA OBRERA",
        "headline": "3 AÑOS DE PLANTÓN Y SANGRE",
        "pill": "DEMETRIO VALLEJO Y EL PUEBLO",
        "caption_short": "Con el apoyo del líder ferrocarrilero Demetrio Vallejo y artistas mexicanos, los obreros resistieron 3 años de plantón.",
        "text": "Aquella negativa desató una de las huelgas más dramáticas del México moderno, Jorge. Los patrones contrataron golpeadores armados que dispararon contra las puertas de la fábrica dejando dos obreros muertos y decenas de heridos. Con la asesoría del histórico líder ferrocarrilero Demetrio Vallejo y el apoyo de intelectuales y pintores como Rufino Tamayo, los trabajadores resistieron tres años de campamento en las banquetas hasta que la Suprema Corte les dio la razón legal definitiva."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 2,
        "img": "assets/pascual_img2.jpg",
        "tag": "CAPÍTULO 02 • INGENIERÍA DEL TETRA PAK",
        "headline": "EL TRIÁNGULO INDESTRUCTIBLE",
        "pill": "TETRA CLASSIC ASEPTIC",
        "caption_short": "La geometría piramidal del triángulo de Boing distribuía el peso de manera uniforme, eliminando la necesidad de cajas rígidas.",
        "text": "En 1985, tras rematar los bienes para pagar los salarios caídos, los propios trabajadores fundaron la Sociedad Cooperativa Trabajadores de Pascual. Pero su gran milagro comercial ya venía gestándose desde los años sesenta con una genialidad de ingeniería del empaque: el triángulo de Boing. Fue el primer envase Tetra Classic Aseptic de América Latina, una pirámide geométrica perfecta inventada por el doctor Ruben Rausing en Suecia que revolucionó la conservación de líquidos."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 2,
        "img": "assets/pascual_img2.jpg",
        "tag": "CAPÍTULO 02 • ANATOMÍA DE 6 CAPAS",
        "headline": "SIN CONSERVADORES QUÍMICOS",
        "pill": "ALUMINIO + POLIETILENO QUIRÚRGICO",
        "caption_short": "Seis capas protectoras formaban una barrera estéril contra la luz y el oxígeno, permitiendo conservar pulpa natural de fruta por meses.",
        "text": "A diferencia de las botellas de vidrio que requerían costosas flotillas de retorno, este empaque se formaba a partir de un tubo continuo de papel que se llenaba con jugo y se sellaba por inducción térmica con pinzas cruzadas a noventa grados. Sus seis capas combinan cartón para rigidez estructural, aluminio como barrera impenetrable contra la luz ultravioleta y el oxígeno, y polietileno apto para alimentos. Esto permitía conservar pulpa natural de fruta mexicana por meses sin necesidad de refrigeración ni conservadores químicos."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 3,
        "img": "assets/pascual_img3.jpg",
        "tag": "CAPÍTULO 03 • INTEGRACIÓN AGROINDUSTRIAL",
        "headline": "DE LAS HUERTAS A LA PLANTA",
        "pill": "MANGO Y GUAYABA MEXICANA",
        "caption_short": "En San Juan del Río procesan directamente miles de toneladas de mango ataulfo y guayaba comprados a productores locales.",
        "text": "Y esa fue la segunda gran ventaja competitiva de Boing frente a las trasnacionales de refrescos oscuros de cola: la fruta real. Mientras las marcas extranjeras vendían jarabe de maíz con saborizantes artificiales, Pascual instaló su megaplanta de procesamiento en San Juan del Río, Querétaro, y en Tizayuca, Hidalgo, comprando cosechas directas de mango ataulfo en Chiapas y Sinaloa, guayaba en Michoacán y tamarindo nacional, integrando la cadena agrícola sin intermediarios."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 3,
        "img": "assets/pascual_img3.jpg",
        "tag": "CAPÍTULO 03 • DESPULPADO ASÉPTICO",
        "headline": "CENTRIFUGADO Y PASTEURIZACIÓN FLASH",
        "pill": "BOLSAS ASÉPTICAS DE 200 LITROS",
        "caption_short": "Centrífugas de acero inoxidable separan la piel y semillas, envasando puré estéril al vacío para abastecer la producción todo el año.",
        "text": "El proceso en planta es una coreografía térmica de alta precisión: despalilladoras y despulpadoras centrífugas separan la cáscara y el hueso; la pulpa pasa por pasteurizadores de placas de intercambio rápido a más de noventa grados centígrados para eliminar enzimas oxidativas, y se almacena en bolsas asépticas de doscientos litros. Eso garantiza que el néctar conserve el sabor del mango fresco recolectado meses atrás."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 4,
        "img": "assets/pascual_img4.jpg",
        "tag": "CAPÍTULO 04 • AUTOGESTIÓN Y SOBERANÍA",
        "headline": "EL TRIUNFO DE LA COOPERATIVA",
        "pill": "EL PATO BOING Y CERO DEUDAS",
        "caption_short": "Superaron la demanda de derechos de Disney rediseñando su mascota y hoy exportan a Centroamérica y EE.UU.",
        "text": "Hoy, la Cooperativa Pascual es un faro de autogestión obrera. Cada trabajador es socio y tiene derecho a un voto en las asambleas, eligiendo a sus propios directivos. Cuando Walt Disney Corporation los demandó en los años ochenta por el parecido de su pato con el Pato Donald, la cooperativa convocó a un certamen y rediseñó a su icónica mascota sonriente con gorra beisbolera. Con su propia red de distribución y cero pago de regalías al extranjero, Boing es el rey indiscutible de las cooperativas escolares y taquerías del país."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "chapter": 5,
        "img": "assets/pascual_img5.jpg",
        "tag": "CAPÍTULO 05 • ECOSISTEMA TRI-PLATAFORMA",
        "headline": "EN TU COCHE O EN VIDEO ILUSTRADO",
        "pill": "SPOTIFY • YOUTUBE • TIKTOK (@escucha_sia)",
        "caption_short": "🚗 En tu coche escúchanos en Spotify | 📱 Para ver el cuento ilustrado búscanos en YouTube y TikTok.",
        "text": "Recuerda que este episodio tiene el mismo formato completo en nuestras tres plataformas para acompañarte donde estés: si vas manejando en tu coche o en el transporte, escúchanos manos libres en Spotify como sIA Podcast; y si prefieres ver este cuento ilustrado con todos sus esquemas técnicos de ingeniería, encuéntranos en YouTube y en TikTok en arroba escucha guion bajo sia."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "chapter": 5,
        "img": "assets/pascual_img5.jpg",
        "tag": "CAPÍTULO 05 • sIA JOURNAL",
        "headline": "INVESTIGACIÓN Y FUENTES APA",
        "pill": "ESCUCHA-SIA.GITHUB.IO",
        "caption_short": "Lee la tesis industrial y referencias APA en escucha-sia.github.io. ¡Hasta la próxima!",
        "text": "Además, la tesis técnica sobre ingeniería de envasado aséptico y economía social con bibliografía académica está disponible en nuestra revista digital escucha guion sia punto github punto io. Soy Jorge, junto a Dalia. ¡Gracias por sintonizar sIA Podcast!"
    }
]

async def synthesize_voice_segment(text: str, voice: str, output_path: Path):
    for attempt in range(4):
        try:
            communicate = edge_tts.Communicate(text, voice, rate="+6%")
            await communicate.save(str(output_path))
            if output_path.exists() and output_path.stat().st_size > 200:
                return
        except Exception as e:
            if attempt == 3:
                raise e
            await asyncio.sleep(2)

def get_duration(file_path: Path) -> float:
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ], capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def produce_audio_track():
    print("🎙️ 1. Sintetizando locuciones neuronales con Edge-TTS...")
    temp_dir = BASE_DIR / "temp_audio_stupy_15_pascual"
    temp_dir.mkdir(parents=True, exist_ok=True)

    segment_files = []
    for idx, d in enumerate(DIALOGUE):
        seg_path = temp_dir / f"seg_{idx:02d}_{d['speaker']}.mp3"
        if not seg_path.exists() or seg_path.stat().st_size < 200:
            print(f"   [{idx+1}/{len(DIALOGUE)}] {d['speaker']} ({d['headline'][:30]}...)")
            await synthesize_voice_segment(d["text"], d["voice"], seg_path)
        segment_files.append(seg_path)

    concat_list = temp_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sf in segment_files:
            f.write(f"file '{sf.as_posix()}'\n")

    raw_voice_concat = temp_dir / "voice_raw_concat.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(raw_voice_concat)
    ], check=True, capture_output=True)

    voice_dur = get_duration(raw_voice_concat)
    print(f"   Voces concatenadas exitosamente: {voice_dur:.2f}s ({int(voice_dur//60):02d}:{int(voice_dur%60):02d})")

    # Audio Master con fondo musical ambiental normalizado
    bg_music = BASE_DIR / "assets" / "raw" / "bg_music.mp3"
    master_mp3 = AUDIO_DIR / EPISODE_FILENAME

    if bg_music.exists():
        print("🎵 2. Mezclando música de fondo con sidechain / ducking...")
        filter_complex = (
            f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{voice_dur + 2.5},"
            f"volume=0.10,afade=t=out:st={voice_dur}:d=2.5[bg];"
            f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2,"
            f"loudnorm=I=-16:TP=-1.5:LRA=11[out]"
        )
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(raw_voice_concat),
            "-i", str(bg_music),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-b:a", "192k",
            str(master_mp3)
        ], check=True, capture_output=True)
    else:
        print("⚠️ bg_music.mp3 no encontrada. Normalizando voz estéreo limpia...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(raw_voice_concat),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-b:a", "192k",
            str(master_mp3)
        ], check=True, capture_output=True)

    total_dur = get_duration(master_mp3)
    print(f"✅ Master de Audio sIA Corp #09 generado: {master_mp3} ({total_dur:.2f}s)")
    return master_mp3, total_dur, segment_files

if __name__ == "__main__":
    asyncio.run(produce_audio_track())
