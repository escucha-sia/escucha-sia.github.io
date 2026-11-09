import subprocess
import os
import sys
import json
import asyncio
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath("scripts"))
from generate_moe_audio import SCRIPT_SEGMENTS, VOICE_JORGE, VOICE_DALIA

async def measure():
    os.makedirs("scratch/timing_moe", exist_ok=True)
    timestamps = []
    current_time = 0.0
    
    print("📏 Midiendo duración de segmentos para MoE DeepSeek...")
    for idx, (voice, text) in enumerate(SCRIPT_SEGMENTS):
        p = f"scratch/timing_moe/seg_moe_{idx:02d}.mp3"
        comm = edge_tts.Communicate(text, voice, rate="+2%", volume="+0%")
        await comm.save(p)
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", p
        ], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        
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
        
    with open("scratch/moe_timestamps.json", "w", encoding="utf-8") as f:
        json.dump(timestamps, f, indent=2, ensure_ascii=False)
    print("Saved scratch/moe_timestamps.json!")

if __name__ == "__main__":
    asyncio.run(measure())
