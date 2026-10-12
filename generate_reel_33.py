"""
sIA Reel #02 Generator (9:16 Vertical Video) - Edición 2026-10-11
Tema: El Mito del Rendimiento en Gemini Flash y Modelos Ligeros
"""

import sys
import os
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

REEL_DATA = {
    "topic_badge": "IA & AGENTES EN PRODUCCIÓN",
    "title": "EL MITO DE GEMINI FLASH",
    "subtitle": "¿Por qué el 90% de las quejas son errores de prompting?",
    "output_filename": "sIA_Reel_02_Mito_Gemini_Flash.mp4",
    "script": [
        {
            "speaker": "JORGE",
            "voice": "es-MX-JorgeNeural",
            "text": "Dalia, ¿por qué tantos desarrolladores se quejan de que los modelos ligeros como Gemini Flash no sirven?"
        },
        {
            "speaker": "DALIA",
            "voice": "es-MX-DaliaNeural",
            "text": "Porque intentan usarlos como oráculos mágicos en lugar de micro-procesadores de estado. Le mandan un prompt ambiguo y esperan milagros."
        },
        {
            "speaker": "JORGE",
            "voice": "es-MX-JorgeNeural",
            "text": "¡Exacto! Flash está optimizado para doscientos milisegundos y esquemas tipados con Pydantic. Si le pides razonar diez pasos sin contexto, el fallo es de tu arquitectura."
        },
        {
            "speaker": "DALIA",
            "voice": "es-MX-DaliaNeural",
            "text": "Usa modelos lentos para diseñar, pero para orquestar y clasificar en tiempo real a costo cero, Flash es el rey."
        },
        {
            "speaker": "JORGE",
            "voice": "es-MX-JorgeNeural",
            "text": "Escucha el Daily Express completo en Spotify y lee el artículo con esquemas en sIA Journal."
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
    print("🎙️ Sintetizando voces de Jorge y Dalia para el Reel #02...")
    audio_segments = []
    
    for idx, item in enumerate(script_items):
        out_file = TEMP_DIR / f"reel2_chunk_{idx:02d}_{item['speaker'].lower()}.mp3"
        comm = edge_tts.Communicate(item["text"], item["voice"], rate="+3%")
        await comm.save(str(out_file))
        dur = get_audio_duration(out_file)
        audio_segments.append({
            "file": out_file,
            "speaker": item["speaker"],
            "text": item["text"],
            "duration": dur
        })

    merged_audio = TEMP_DIR / "reel2_full_audio.mp3"
    concat_txt = TEMP_DIR / "reel2_audio_concat.txt"
    
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in audio_segments:
            f_path = str(seg["file"]).replace('\\', '/')
            f.write(f"file '{f_path}'\n")
            
    cmd_merge = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_txt),
        '-c', 'copy', str(merged_audio)
    ]
    subprocess.run(cmd_merge, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    total_duration = get_audio_duration(merged_audio)
    return merged_audio, audio_segments, total_duration

def format_ass_time(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 100)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}.{millis:02d}"

def generate_ass_subtitles(audio_segments, ass_path: Path):
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
        
        words = seg["text"].split()
        if len(words) > 10:
            mid = len(words) // 2
            half_dur = seg["duration"] / 2.0
            p1 = " ".join(words[:mid])
            p2 = " ".join(words[mid:])
            t1_s, t1_e = format_ass_time(start_t), format_ass_time(start_t + half_dur)
            t2_s, t2_e = format_ass_time(start_t + half_dur), format_ass_time(end_t)
            events.append(f"Dialogue: 0,{t1_s},{t1_e},{style},,0,0,0,,{p1}")
            events.append(f"Dialogue: 0,{t2_s},{t2_e},{style},,0,0,0,,{p2}")
        else:
            events.append(f"Dialogue: 0,{format_ass_time(start_t)},{format_ass_time(end_t)},{style},,0,0,0,,{seg['text']}")

    ass_path.write_text(ass_header + "\n".join(events) + "\n", encoding='utf-8')

def generate_reel_background(bg_path: Path):
    width, height = 1080, 1920
    im = Image.new("RGBA", (width, height), (7, 11, 20, 255))
    draw = ImageDraw.Draw(im)

    for y in range(height):
        ratio = y / height
        draw.line([(0, y), (width, y)], fill=(int(7 + ratio * 8), int(11 + ratio * 12), int(20 + ratio * 25), 255))

    font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 34)
    font_host = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
    font_footer = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)

    draw.text((width // 2, 90), "sIA TECH MEDIA", fill=(148, 163, 184, 255), font=font_badge, anchor="mm")

    badge_w, badge_h = 440, 56
    badge_x, badge_y = (width - badge_w) // 2, 140
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=28, fill=(15, 23, 42, 220), outline=(0, 242, 254, 255), width=2)
    draw.ellipse([badge_x + 28, badge_y + 22, badge_x + 40, badge_y + 34], fill=(0, 242, 254, 255))
    draw.text((badge_x + 44 + (badge_w - 44) // 2 - 10, badge_y + badge_h // 2), REEL_DATA["topic_badge"], fill=(0, 242, 254, 255), font=font_badge, anchor="mm")

    draw.text((width // 2, 260), REEL_DATA["title"], fill=(255, 255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, 330), REEL_DATA["subtitle"], fill=(56, 189, 248, 255), font=font_sub, anchor="mm")

    cover_src = BASE_DIR / "cover.jpg"
    if cover_src.exists():
        cover_img = Image.open(cover_src).convert("RGBA").resize((720, 540), Image.Resampling.LANCZOS)
        card_mask = Image.new("L", (720, 540), 0)
        ImageDraw.Draw(card_mask).rounded_rectangle([0, 0, 720, 540], radius=32, fill=255)
        card_x, card_y = (width - 720) // 2, 420
        im.paste(cover_img, (card_x, card_y), card_mask)
        draw.rounded_rectangle([card_x, card_y, card_x + 720, card_y + 540], radius=32, outline=(0, 242, 254, 180), width=3)

    host_bar_y = 1000
    jorge_w, jorge_h = 240, 52
    jorge_x = 240
    draw.rounded_rectangle([jorge_x, host_bar_y, jorge_x + jorge_w, host_bar_y + jorge_h], radius=16, fill=(15, 23, 42, 240), outline=(0, 242, 254, 255), width=2)
    draw.ellipse([jorge_x + 20, host_bar_y + 19, jorge_x + 34, host_bar_y + 33], fill=(0, 242, 254, 255))
    draw.text((jorge_x + 42 + (jorge_w - 42) // 2 - 10, host_bar_y + jorge_h // 2), "Jorge Neural", fill=(0, 242, 254, 255), font=font_host, anchor="mm")

    dalia_x = width - 240 - jorge_w
    draw.rounded_rectangle([dalia_x, host_bar_y, dalia_x + jorge_w, host_bar_y + jorge_h], radius=16, fill=(15, 23, 42, 240), outline=(244, 114, 182, 255), width=2)
    draw.ellipse([dalia_x + 20, host_bar_y + 19, dalia_x + 34, host_bar_y + 33], fill=(244, 114, 182, 255))
    draw.text((dalia_x + 42 + (jorge_w - 42) // 2 - 10, host_bar_y + jorge_h // 2), "Dalia Neural", fill=(244, 114, 182, 255), font=font_host, anchor="mm")

    draw.rounded_rectangle([100, 1080, 980, 1240], radius=24, fill=(10, 15, 29, 220), outline=(30, 41, 59, 255), width=2)
    draw.rounded_rectangle([70, 1280, 1010, 1640], radius=24, fill=(15, 23, 42, 140), outline=(51, 65, 85, 120), width=1)

    draw.text((width // 2, 1760), "Escucha el Daily Express completo en Spotify", fill=(255, 255, 255, 255), font=font_footer, anchor="mm")
    draw.text((width // 2, 1805), "Lee el artículo técnico en sIA Journal (GitHub Pages)", fill=(148, 163, 184, 255), font=font_sub, anchor="mm")

    im.convert("RGB").save(bg_path, quality=95)

def render_reel_video(bg_path: Path, audio_path: Path, ass_path: Path, duration: float, out_path: Path):
    sub_rel_name = ass_path.name
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
    subprocess.run(cmd, cwd=str(BASE_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

async def generate():
    print("=" * 70)
    print("🎬 GENERANDO REEL #02: EL MITO DE GEMINI FLASH (42s)")
    print("=" * 70)
    merged_audio, segments, total_dur = await synthesize_reel_audio(REEL_DATA["script"])
    ass_path = BASE_DIR / "temp_reel2.ass"
    generate_ass_subtitles(segments, ass_path)
    bg_path = BASE_DIR / "temp_reel2_bg.jpg"
    generate_reel_background(bg_path)
    output_mp4 = REELS_DIR / REEL_DATA["output_filename"]
    render_reel_video(bg_path, merged_audio, ass_path, total_dur, output_mp4)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_DATA["output_filename"])
    
    # Extract poster
    poster_path = REELS_DIR / "sIA_Reel_02_Mito_Gemini_Flash_poster.jpg"
    subprocess.run(['ffmpeg', '-y', '-ss', '00:00:10', '-i', str(output_mp4), '-vframes', '1', str(poster_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if bg_path.exists(): bg_path.unlink()
    if ass_path.exists(): ass_path.unlink()
    print(f"✅ Reel #02 generado exitosamente: {output_mp4}")

if __name__ == '__main__':
    asyncio.run(generate())
