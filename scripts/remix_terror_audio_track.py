import os
import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
REEL_FILE = BASE_DIR / "reels" / "sIA_Terror_01_Las_Escaleras_Reel.mp4"
SFX_DRONE = BASE_DIR / "assets" / "sfx" / "dark_drone.mp3"
MUSIC_TENSION = BASE_DIR / "assets" / "audio_library" / "music_isolated_tension.mp3"
SCRATCH_DIR = BASE_DIR / "scratch"

def remix_terror():
    print("[*] Remezclando audio atmosférico de Terror #01...")
    
    # 1. Extraer voz limpia del reel
    voice_track = SCRATCH_DIR / "terror_voice_raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(REEL_FILE),
        "-vn", "-ac", "2", "-ar", "48000", str(voice_track)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 2. Mezclar voz con ambient dark drone + tension music
    # loop drone para cubrir los 45s a -24dB, voz a volumen normal
    mixed_wav = SCRATCH_DIR / "terror_mixed.wav"
    filter_complex = (
        "[1:a]aloop=loop=-1:size=2e+09,volume=0.18,afade=t=in:st=0:d=1.5,afade=t=out:st=43.5:d=1.5[drone];"
        "[0:a][drone]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-16:TP=-1.5:LRA=11[norm]"
    )
    
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", str(voice_track),
        "-i", str(SFX_DRONE),
        "-filter_complex", filter_complex,
        "-map", "[norm]",
        "-ac", "2",
        "-ar", "48000",
        str(mixed_wav)
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 3. Remux en el video MP4 sin re-renderizar video (0 perdida de calidad)
    temp_mp4 = SCRATCH_DIR / "terror_remuxed.mp4"
    cmd_remux = [
        "ffmpeg", "-y",
        "-i", str(REEL_FILE),
        "-i", str(mixed_wav),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        str(temp_mp4)
    ]
    subprocess.run(cmd_remux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # 4. Reemplazar archivo final
    temp_mp4.replace(REEL_FILE)
    print(f"[OK] Terror #01 actualizado con audio inmersivo EBU R128: {REEL_FILE.name}")
    print(f"Nuevo tamaño: {REEL_FILE.stat().st_size} bytes")

if __name__ == "__main__":
    remix_terror()
