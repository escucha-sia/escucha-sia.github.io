import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Re-measure the segments from SCRIPT_SEGMENTS
from generate_solarwinds_audio import SCRIPT_SEGMENTS, VOICE_JORGE, VOICE_DALIA
import edge_tts
import asyncio

async def measure():
    os.makedirs("scratch/timing", exist_ok=True)
    timestamps = []
    current_time = 0.0
    
    for idx, (voice, text) in enumerate(SCRIPT_SEGMENTS):
        p = f"scratch/timing/seg_{idx:02d}.mp3"
        comm = edge_tts.Communicate(text, voice, rate="+2%", volume="+0%")
        await comm.save(p)
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", p
        ], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        timestamps.append({
            "idx": idx,
            "voice": "Jorge" if voice == VOICE_JORGE else "Dalia",
            "start": current_time,
            "end": current_time + dur,
            "dur": dur,
            "text": text
        })
        current_time += dur
        try: os.remove(p)
        except: pass
        
    print(f"Total measured: {current_time:.2f}s")
    for t in timestamps:
        print(f"[{t['start']:.1f}s - {t['end']:.1f}s] {t['voice']}: {t['text'][:50]}...")
        
    import json
    with open("scratch/solarwinds_timestamps.json", "w", encoding="utf-8") as f:
        json.dump(timestamps, f, indent=2, ensure_ascii=False)
    print("Saved scratch/solarwinds_timestamps.json!")

asyncio.run(measure())
