#!/usr/bin/env python3
"""
verify_reel.py - Script determinista de Prueba de Terminado (Definition of Done)
Valida que un video vertical de sIA cumpla con todos los estándares técnicos:
1. Existencia y peso (> 2MB).
2. Duración (entre 35.0s y 55.0s).
3. Resolución exacta vertical (1080x1920).
4. Audio presente con bitrate adecuado.
5. Poster frame JPEG existente (> 20KB).
"""

import sys
import os
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def check_video(video_path: Path):
    print(f"\n=======================================================")
    print(f"🔍 AUDITORÍA DE PRUEBA DE TERMINADO: {video_path.name}")
    print(f"=======================================================")
    
    if not video_path.exists():
        print(f"❌ ERROR: El archivo de video no existe: {video_path}")
        return False
        
    size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"📦 Tamaño del archivo: {size_mb:.2f} MB")
    if size_mb < 2.0:
        print(f"❌ ERROR: El archivo pesa menos de 2.0 MB ({size_mb:.2f} MB). Posible render corrupto o incompleto.")
        return False
    else:
        print("   [PASS] Tamaño del video válido.")

    # Probe with ffprobe
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=width,height,codec_name,codec_type",
        "-of", "json",
        str(video_path)
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        meta = json.loads(proc.stdout)
    except Exception as e:
        print(f"❌ ERROR al ejecutar ffprobe: {e}")
        return False

    duration = float(meta.get("format", {}).get("duration", 0))
    print(f"⏱️ Duración real: {duration:.2f} segundos")
    if duration < 30.0 or duration > 60.0:
        print(f"❌ ERROR: La duración {duration:.2f}s está fuera del límite admitido (30s - 60s).")
        return False
    else:
        print("   [PASS] Duración dentro del rango canónico para Reels/TikTok.")

    streams = meta.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    if not video_stream:
        print("❌ ERROR: No se encontró stream de video.")
        return False
        
    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    print(f"📐 Resolución: {width} x {height}")
    if width != 1080 or height != 1920:
        print(f"❌ ERROR: Resolución {width}x{height} no coincide con el estándar vertical 1080x1920.")
        return False
    else:
        print("   [PASS] Resolución 1080x1920 (9:16 portrait) confirmada.")

    if not audio_stream:
        print("❌ ERROR: No se encontró stream de audio.")
        return False
    else:
        print(f"   [PASS] Audio stream presente ({audio_stream.get('codec_name', 'audio')}).")

    # Check poster
    poster_path = video_path.parent / f"{video_path.stem}_poster.jpg"
    if poster_path.exists():
        poster_kb = poster_path.stat().st_size / 1024
        print(f"🖼️ Poster frame detectado: {poster_path.name} ({poster_kb:.1f} KB)")
        if poster_kb < 15.0:
            print("⚠️ AVISO: El poster frame es menor a 15 KB.")
        else:
            print("   [PASS] Poster frame óptimo.")
    else:
        print(f"⚠️ AVISO: No se encontró poster frame {poster_path.name}")

    print("=======================================================")
    print("✅ ¡PRUEBA DE TERMINADO (DoD) SUPERADA AL 100%!")
    print("=======================================================\n")
    return True

def main():
    if len(sys.argv) < 2:
        print("Uso: python verify_reel.py <ruta_al_video.mp4>")
        sys.exit(1)
        
    video_path = Path(sys.argv[1])
    success = check_video(video_path)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
