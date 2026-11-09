import subprocess
import os
import sys
import json
import asyncio
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath("scripts"))
from generate_boeing_audio import SCRIPT_SEGMENTS, VOICE_JORGE, VOICE_DALIA

async def measure():
    os.makedirs("scratch/timing", exist_ok=True)
    timestamps = []
    current_time = 0.0
    
    print("📏 Midiendo duración exacta de cada segmento...")
    for idx, (voice, text) in enumerate(SCRIPT_SEGMENTS):
        p = f"scratch/timing/seg_boeing_{idx:02d}.mp3"
        comm = edge_tts.Communicate(text, voice, rate="+2%", volume="+0%")
        await comm.save(p)
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", p
        ], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        
        # Determine act based on idx
        # Act 1: 0..3 (4 segs)
        # Act 2: 4..7 (4 segs)
        # Act 3: 8..11 (4 segs)
        # Act 4: 12..15 (4 segs)
        # Act 5: 16..19 (4 segs)
        act_num = (idx // 4) + 1
        
        timestamps.append({
            "idx": idx,
            "act": act_num,
            "voice": "Jorge" if voice == VOICE_JORGE else "Dalia",
            "start": current_time,
            "end": current_time + dur,
            "dur": dur,
            "text": text
        })
        current_time += dur
        try: os.remove(p)
        except: pass
        
    print(f"Total medido: {current_time:.2f}s")
    for t in timestamps:
        print(f"Acto {t['act']} | [{t['start']:.1f}s - {t['end']:.1f}s] {t['voice']}: {t['text'][:45]}...")
        
    with open("scratch/boeing_timestamps.json", "w", encoding="utf-8") as f:
        json.dump(timestamps, f, indent=2, ensure_ascii=False)
    print("Saved scratch/boeing_timestamps.json!")

if __name__ == "__main__":
    asyncio.run(measure())
