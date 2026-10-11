"""
sIA Master Subtitle & Transcript Generator
Genera subtítulos WebVTT (.vtt) y SubRip (.srt) para TODOS los episodios
del catálogo de sIA utilizando faster-whisper y los sincroniza con Spotify y el feed RSS.
"""

import os
import sys
import shutil
from pathlib import Path
from faster_whisper import WhisperModel

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = BASE_DIR / "audio"
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)

def fmt_vtt(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{millis:03d}"

def fmt_srt(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{millis:03d}"

def transcribe_all():
    print("=" * 70)
    print("🎙️ GENERADOR UNIVERSAL DE SUBTÍTULOS PARA TODOS LOS CAPÍTULOS")
    print("=" * 70)

    mp3_files = sorted(list(AUDIO_DIR.glob("*.mp3")))
    pending = []
    for f in mp3_files:
        stem = f.stem
        vtt_p = AUDIO_DIR / f"{stem}.vtt"
        srt_p = AUDIO_DIR / f"{stem}.srt"
        if not vtt_p.exists() or not srt_p.exists():
            pending.append(f)

    print(f"\nTotal episodios en audio/: {len(mp3_files)}")
    print(f"Episodios con subtítulos pendientes: {len(pending)}")

    if not pending:
        print("\n[OK] Todos los episodios ya cuentan con subtítulos WebVTT y SRT.")
        return

    print("\nInicializando modelo de transcripción rápida en español (Whisper tiny int8)...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")

    for idx, audio_path in enumerate(pending, 1):
        stem = audio_path.stem
        vtt_file = AUDIO_DIR / f"{stem}.vtt"
        srt_file = AUDIO_DIR / f"{stem}.srt"

        print(f"\n[{idx}/{len(pending)}] Transcribiendo: {audio_path.name}...")
        segments, info = model.transcribe(str(audio_path), language="es", beam_size=2)

        vtt_lines = ["WEBVTT\nKind: captions\nLanguage: es\n\n"]
        srt_lines = []
        srt_idx = 1

        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            vtt_lines.append(f"{fmt_vtt(seg.start)} --> {fmt_vtt(seg.end)}\n{text}\n\n")
            srt_lines.append(f"{srt_idx}\n{fmt_srt(seg.start)} --> {fmt_srt(seg.end)}\n{text}\n\n")
            srt_idx += 1

        # Guardar en audio/
        vtt_file.write_text("".join(vtt_lines), encoding='utf-8')
        srt_file.write_text("".join(srt_lines), encoding='utf-8')

        # Sincronizar en carpeta de Spotify
        shutil.copy2(vtt_file, SPOTIFY_DIR / f"{stem}.vtt")
        shutil.copy2(srt_file, SPOTIFY_DIR / f"{stem}.srt")
        print(f"  [OK] Generados {srt_idx - 1} segmentos de subtítulos para {stem}")

    print("\n" + "=" * 70)
    print("✅ ¡TODOS LOS EPISODIOS TIENEN SUBTÍTULOS VTT Y SRT!")
    print("Regenerando revista digital y actualizando podcast.xml...")
    print("=" * 70)

    from build_magazine import build_all_articles
    build_all_articles()

if __name__ == '__main__':
    transcribe_all()
