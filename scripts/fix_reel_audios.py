import subprocess, shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")

music_src = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
if not music_src.exists():
    music_src = list((BASE_DIR / "assets" / "audio_library").glob("*.mp3"))[0]

def mix_audio_and_remux(reel_id: str, temp_audio_dir: Path, output_filename: str):
    print(f"\n[*] Procesando corrección para {reel_id} ({output_filename})...")
    
    # 1. Crear concat de segmentos de voz
    segments = sorted(list(temp_audio_dir.glob("reel_seg_*.mp3")))
    print(f"  > Segmentos encontrados: {len(segments)}")
    for s in segments:
        print(f"     - {s.name} ({s.stat().st_size} bytes)")
        
    concat_list = temp_audio_dir / "concat_fixed.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"file '{s.name}'\n")
            
    mixed_audio = temp_audio_dir / "audio_mixed_r128.mp3"
    
    # Mezcla con música de fondo sutil y EBU R128 (-16 LUFS)
    cmd_mix = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-stream_loop", "-1", "-i", str(music_src),
        "-filter_complex",
        "[1:a]volume=0.034,afade=t=in:st=0:d=1.0,afade=t=out:st=43.5:d=1.5[bg];"
        "[0:a]apad=whole_dur=45.0[vox];"
        "[vox][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,"
        "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=120,"
        "loudnorm=I=-16:TP=-1.5:LRA=9[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-t", "45.0",
        str(mixed_audio)
    ]
    subprocess.run(cmd_mix, check=True)
    print(f"  [OK] Audio mezclado generado: {mixed_audio} ({mixed_audio.stat().st_size} bytes)")
    
    # 2. Re-muxar sobre el video MP4 existente sin re-renderizar video (0.5s)
    current_video = REELS_DIR / output_filename
    fixed_video = REELS_DIR / f"fixed_{output_filename}"
    
    cmd_remux = [
        "ffmpeg", "-y",
        "-i", str(current_video),
        "-i", str(mixed_audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        str(fixed_video)
    ]
    subprocess.run(cmd_remux, check=True)
    print(f"  [OK] Video remuxado con audio correcto: {fixed_video} ({fixed_video.stat().st_size} bytes)")
    
    # Reemplazar original
    shutil.move(str(fixed_video), str(current_video))
    if SPOTIFY_REELS_DIR.exists():
        shutil.copy2(str(current_video), str(SPOTIFY_REELS_DIR / output_filename))
    if GDRIVE_REELS.exists():
        shutil.copy2(str(current_video), str(GDRIVE_REELS / output_filename))
    print(f"  [DONE] Video actualizado en local, Spotify y Google Drive Hub!")

# Ejecutar para Reel 08 y Reel 09
mix_audio_and_remux("Stupy 08", ENGINE_DIR / "temp_audio_stupy_08", "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4")
mix_audio_and_remux("Stupy 09", ENGINE_DIR / "temp_audio_stupy_09", "sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4")
