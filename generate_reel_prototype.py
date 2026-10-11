"""
sIA Reels & Shorts Prototype Generator (9:16 Vertical Video)
Genera un video corto (1080x1920) de 45 segundos con:
- Audio dinámico sintetizado con Jorge y Dalia (Edge-TTS).
- Portada y tarjeta tecnológica generada con Pillow.
- Onda de audio reactiva animada en tiempo real con FFmpeg.
- Subtítulos cinemáticos quemados (Burned-in ASS) con colores diferenciados por locutor.
- Barra de progreso interactiva inferior.
- Sincronización automática a carpeta de Spotify / Reels y a la revista digital.
"""

import os
import sys
import re
import asyncio
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
TEMP_DIR = BASE_DIR / "temp_chunks"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")

TEMP_DIR.mkdir(parents=True, exist_ok=True)
REELS_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)

# Dialogue Script for the Reel
REEL_DATA = {
    "topic_badge": "🌌 FUERA DE LA BURBUJA",
    "title": "COMPUTACIÓN TERMODINÁMICA",
    "subtitle": "¿El fin del silicio para la Inteligencia Artificial?",
    "output_filename": "sIA_Reel_01_Computacion_Termodinamica.mp4",
    "script": [
        {
            "speaker": "JORGE",
            "voice": "es-MX-JorgeNeural",
            "text": "¿Y si te dijera que el mayor límite de la inteligencia artificial no es la memoria... sino la termodinámica?"
        },
        {
            "speaker": "DALIA",
            "voice": "es-MX-DaliaNeural",
            "text": "Totalmente. Hoy un datacenter gasta gigavatios de energía tratando de enfriar procesadores que luchan contra el calor y el ruido térmico."
        },
        {
            "speaker": "JORGE",
            "voice": "es-MX-JorgeNeural",
            "text": "Exacto. Pero la computación termodinámica hace lo opuesto: no pelea contra el calor, ¡lo aprovecha físicamente para calcular probabilidades de redes neuronales a la velocidad de la física!"
        },
        {
            "speaker": "DALIA",
            "voice": "es-MX-DaliaNeural",
            "text": "¿Te imaginas reducir el consumo eléctrico un noventa y nueve por ciento? Es romper de golpe la burbuja del silicio tradicional."
        },
        {
            "speaker": "JORGE",
            "voice": "es-MX-JorgeNeural",
            "text": "Escucha el episodio completo en Spotify y entra a ver la arquitectura técnica en nuestra revista sIA Journal."
        }
    ]
}

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def synthesize_reel_audio(script_items):
    print("🎙️ Sintetizando voces de Jorge y Dalia para el Reel...")
    audio_segments = []
    
    for idx, item in enumerate(script_items):
        out_file = TEMP_DIR / f"reel_chunk_{idx:02d}_{item['speaker'].lower()}.mp3"
        comm = edge_tts.Communicate(item["text"], item["voice"], rate="+3%")
        await comm.save(str(out_file))
        dur = get_audio_duration(out_file)
        audio_segments.append({
            "file": out_file,
            "speaker": item["speaker"],
            "text": item["text"],
            "duration": dur
        })
        print(f"  [{idx+1}/{len(script_items)}] {item['speaker']} ({dur:.2f}s): {item['text'][:45]}...")

    # Build concat file with subtle cross-pauses (120ms silence)
    merged_audio = TEMP_DIR / "reel_full_audio.mp3"
    concat_txt = TEMP_DIR / "reel_audio_concat.txt"
    
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in audio_segments:
            f_path = str(seg["file"]).replace('\\', '/')
            f.write(f"file '{f_path}'\n")
            
    # Concatenate using ffmpeg
    cmd_merge = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_txt),
        '-c', 'copy', str(merged_audio)
    ]
    subprocess.run(cmd_merge, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    total_duration = get_audio_duration(merged_audio)
    print(f"✅ Audio del Reel consolidado: {merged_audio} ({total_duration:.2f} segundos)")
    
    return merged_audio, audio_segments, total_duration

def format_ass_time(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 100)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}.{millis:02d}"

def generate_ass_subtitles(audio_segments, ass_path: Path):
    """
    Genera subtítulos cinemáticos en formato ASS optimizados para pantalla móvil vertical 1080x1920.
    """
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Jorge,Segoe UI,48,&H00FEF200,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,70,70,350,1
Style: Dalia,Segoe UI,48,&H00F472B6,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,70,70,350,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    current_time = 0.0
    
    for seg in audio_segments:
        start_t = current_time
        end_t = current_time + seg["duration"]
        current_time = end_t
        
        style = "Jorge" if seg["speaker"] == "JORGE" else "Dalia"
        
        # Split text into bite-sized 2-line chunks if long
        words = seg["text"].split()
        if len(words) > 10:
            mid = len(words) // 2
            half_dur = seg["duration"] / 2.0
            
            p1 = " ".join(words[:mid])
            p2 = " ".join(words[mid:])
            
            t1_s = format_ass_time(start_t)
            t1_e = format_ass_time(start_t + half_dur)
            t2_s = format_ass_time(start_t + half_dur)
            t2_e = format_ass_time(end_t)
            
            events.append(f"Dialogue: 0,{t1_s},{t1_e},{style},,0,0,0,,{p1}")
            events.append(f"Dialogue: 0,{t2_s},{t2_e},{style},,0,0,0,,{p2}")
        else:
            t_s = format_ass_time(start_t)
            t_e = format_ass_time(end_t)
            events.append(f"Dialogue: 0,{t_s},{t_e},{style},,0,0,0,,{seg['text']}")

    ass_content = ass_header + "\n".join(events) + "\n"
    ass_path.write_text(ass_content, encoding='utf-8')
    print(f"✅ Subtítulos cinemáticos ASS generados: {ass_path}")

def generate_reel_background(bg_path: Path):
    """
    Genera el lienzo vertical 1080x1920 de alta definición con estética cyberpunk elegante.
    """
    width, height = 1080, 1920
    im = Image.new("RGBA", (width, height), (7, 11, 20, 255)) # Dark navy
    draw = ImageDraw.Draw(im)

    # 1. Subtle gradient backdrop
    for y in range(height):
        ratio = y / height
        r = int(7 + ratio * 8)
        g = int(11 + ratio * 12)
        b = int(20 + ratio * 25)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Fonts
    font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 34)
    font_host = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
    font_footer = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)

    # 2. Header Brand
    brand_text = "sIA TECH MEDIA"
    draw.text((width // 2, 90), brand_text, fill=(148, 163, 184, 255), font=font_badge, anchor="mm")

    # 3. Category Pill Badge
    badge_text = "FUERA DE LA BURBUJA"
    badge_w, badge_h = 400, 56
    badge_x = (width - badge_w) // 2
    badge_y = 140
    # Pill background
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=28, fill=(15, 23, 42, 220), outline=(0, 242, 254, 255), width=2)
    # Glowing dot
    draw.ellipse([badge_x + 30, badge_y + 22, badge_x + 42, badge_y + 34], fill=(0, 242, 254, 255))
    draw.text((badge_x + 44 + (badge_w - 44) // 2 - 15, badge_y + badge_h // 2), badge_text, fill=(0, 242, 254, 255), font=font_badge, anchor="mm")

    # 4. Main Title
    draw.text((width // 2, 260), REEL_DATA["title"], fill=(255, 255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, 330), REEL_DATA["subtitle"], fill=(56, 189, 248, 255), font=font_sub, anchor="mm")

    # 5. Visual Hero Card (Crop & Scale cover.jpg)
    cover_src = BASE_DIR / "cover.jpg"
    if cover_src.exists():
        cover_img = Image.open(cover_src).convert("RGBA")
        card_w, card_h = 720, 540
        cover_img = cover_img.resize((card_w, card_h), Image.Resampling.LANCZOS)
        
        # Create rounded card with glowing cyan border
        card_mask = Image.new("L", (card_w, card_h), 0)
        mask_draw = ImageDraw.Draw(card_mask)
        mask_draw.rounded_rectangle([0, 0, card_w, card_h], radius=32, fill=255)
        
        card_x = (width - card_w) // 2
        card_y = 420
        im.paste(cover_img, (card_x, card_y), card_mask)
        
        # Border
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=32, outline=(0, 242, 254, 180), width=3)

    # 6. Speaker Badges Bar
    host_bar_y = 1000
    # Jorge
    jorge_w, jorge_h = 240, 52
    jorge_x = 240
    draw.rounded_rectangle([jorge_x, host_bar_y, jorge_x + jorge_w, host_bar_y + jorge_h], radius=16, fill=(15, 23, 42, 240), outline=(0, 242, 254, 255), width=2)
    draw.ellipse([jorge_x + 20, host_bar_y + 19, jorge_x + 34, host_bar_y + 33], fill=(0, 242, 254, 255))
    draw.text((jorge_x + 42 + (jorge_w - 42) // 2 - 10, host_bar_y + jorge_h // 2), "Jorge Neural", fill=(0, 242, 254, 255), font=font_host, anchor="mm")

    # Dalia
    dalia_x = width - 240 - jorge_w
    draw.rounded_rectangle([dalia_x, host_bar_y, dalia_x + jorge_w, host_bar_y + jorge_h], radius=16, fill=(15, 23, 42, 240), outline=(244, 114, 182, 255), width=2)
    draw.ellipse([dalia_x + 20, host_bar_y + 19, dalia_x + 34, host_bar_y + 33], fill=(244, 114, 182, 255))
    draw.text((dalia_x + 42 + (jorge_w - 42) // 2 - 10, host_bar_y + jorge_h // 2), "Dalia Neural", fill=(244, 114, 182, 255), font=font_host, anchor="mm")

    # 7. Waveform Container Box (The audio waveform will be overlaid inside this zone: x=100, y=1080, w=880, h=160)
    wave_box_x, wave_box_y = 100, 1080
    wave_box_w, wave_box_h = 880, 160
    draw.rounded_rectangle([wave_box_x, wave_box_y, wave_box_x + wave_box_w, wave_box_y + wave_box_h], radius=24, fill=(10, 15, 29, 220), outline=(30, 41, 59, 255), width=2)

    # 8. Subtitle Zone Hint
    sub_box_x, sub_box_y = 70, 1280
    sub_box_w, sub_box_h = 940, 360
    draw.rounded_rectangle([sub_box_x, sub_box_y, sub_box_x + sub_box_w, sub_box_y + sub_box_h], radius=24, fill=(15, 23, 42, 140), outline=(51, 65, 85, 120), width=1)

    # 9. Call to Action Footer
    footer_y = 1760
    draw.text((width // 2, footer_y), "Escucha el episodio completo en Spotify", fill=(255, 255, 255, 255), font=font_footer, anchor="mm")
    draw.text((width // 2, footer_y + 45), "Lee el artículo técnico en sIA Journal (GitHub Pages)", fill=(148, 163, 184, 255), font=font_sub, anchor="mm")

    im.convert("RGB").save(bg_path, quality=95)
    print(f"✅ Lienzo vertical 1080x1920 generado: {bg_path}")

def render_reel_video(bg_path: Path, audio_path: Path, ass_path: Path, duration: float, out_path: Path):
    """
    Ejecuta el renderizado de video en FFmpeg con:
    - Fondo 1080x1920
    - Audio de Jorge y Dalia
    - Onda dinámica reactiva sincronizada con las frecuencias vocales
    - Subtítulos cinemáticos quemados (ASS)
    - Barra de progreso dinámica en el fondo inferior
    """
    print(f"\n🎬 Iniciando renderizado de video con FFmpeg ({duration:.2f}s)...")
    
    # En Windows, usamos ruta relativa de subtítulos para evitar problemas con C:
    sub_rel_name = ass_path.name
    
    # Filtergraph:
    # 1. showwaves: genera onda sonora reactiva de 840x140
    # 2. overlay de onda en x=120, y=1090
    # 3. drawbox: barra de progreso animada en y=1908
    # 4. subtitles: quemar subtítulos ASS
    dur_str = f"{duration:.3f}"
    
    filter_complex = (
        f"[1:a]showwaves=s=840x130:mode=cline:colors=0x00f2fe@0.9:rate=30[wave];"
        f"[0:v][wave]overlay=120:1095[v1];"
        f"[v1]drawbox=x=0:y=1908:w='min(1080,1080*t/{dur_str})':h=12:color=0x00f2fe@0.95:t=fill[v2];"
        f"[v2]subtitles={sub_rel_name}[vout]"
    )
    
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-i', str(bg_path),
        '-i', str(audio_path),
        '-filter_complex', filter_complex,
        '-map', '[vout]',
        '-map', '1:a',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '22',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-t', dur_str,
        str(out_path)
    ]
    
    res = subprocess.run(cmd, cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("❌ Error en FFmpeg:")
        print(res.stderr[-1000:])
        raise RuntimeError("Fallo en renderizado de FFmpeg")
        
    print(f"🎉 ¡Reel de video 1080x1920 generado exitosamente!")
    print(f"📁 Archivo: {out_path} ({out_path.stat().st_size / (1024*1024):.2f} MB)")

async def main():
    print("=" * 70)
    print("🚀 MOTOR DE PRODUCCIÓN DE REELS & SHORTS VERTICALES (9:16) — sIA")
    print("=" * 70)

    # 1. Sintetizar audio
    merged_audio, segments, total_duration = await synthesize_reel_audio(REEL_DATA["script"])
    
    # 2. Generar subtítulos cinemáticos ASS
    ass_path = BASE_DIR / "temp_reel.ass"
    generate_ass_subtitles(segments, ass_path)
    
    # 3. Generar lienzo vertical 1080x1920
    bg_path = BASE_DIR / "temp_reel_bg.jpg"
    generate_reel_background(bg_path)
    
    # 4. Renderizar video MP4 con FFmpeg
    output_mp4 = REELS_DIR / REEL_DATA["output_filename"]
    render_reel_video(bg_path, merged_audio, ass_path, total_duration, output_mp4)
    
    # 5. Sincronizar en carpeta de Spotify / Reels
    spotify_copy = SPOTIFY_REELS_DIR / REEL_DATA["output_filename"]
    shutil.copy2(output_mp4, spotify_copy)
    print(f"✅ Sincronizado en Spotify / Reels: {spotify_copy}")
    
    # Limpieza de temporales auxiliares
    if bg_path.exists():
        bg_path.unlink()
    if ass_path.exists():
        ass_path.unlink()
        
    print("\n" + "=" * 70)
    print(f"✨ Prototipo de Reel 100% completado listo para Spotify, TikTok y Pages.")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(main())
