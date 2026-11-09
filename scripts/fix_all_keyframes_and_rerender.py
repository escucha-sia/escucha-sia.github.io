import os
import sys
import math
import json
import time
import shutil
import hashlib
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
GDRIVE_REELS_DIR = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
NODE_PATH = r"C:\Carlos\nodejs"

EPISODE_FILENAME = "sIA_Corp_08_Jabon_Zote_La_Corona_Ecatepec_2026-11-06.mp3"
REEL_FILENAME = "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"

from produce_episode_jabon_zote_storybook import DIALOGUE, get_duration, get_audio_sha256

def build_css_keyframe_rule(name: str, start_s: float, end_s: float, total_dur: float, is_first: bool = False, is_last: bool = False) -> str:
    p_start = max(0.0, (start_s / total_dur) * 100.0)
    p_in = min(100.0, ((start_s + 0.35) / total_dur) * 100.0)
    p_out = max(p_in + 0.1, ((end_s - 0.35) / total_dur) * 100.0)
    p_end = min(100.0, (end_s / total_dur) * 100.0)

    if is_first:
        return f"""
      @keyframes {name} {{
        0% {{ opacity: 1; transform: scale(1); z-index: 5; }}
        {p_out:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; }}
        {p_end:.3f}% {{ opacity: 0; transform: scale(1.04); z-index: 0; }}
        100% {{ opacity: 0; transform: scale(1.04); z-index: 0; }}
      }}"""
    elif is_last:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ opacity: 0; transform: scale(0.94); z-index: 0; }}
        {p_in:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; }}
        100% {{ opacity: 1; transform: scale(1); z-index: 5; }}
      }}"""
    else:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ opacity: 0; transform: scale(0.94); z-index: 0; }}
        {p_in:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; }}
        {p_out:.3f}% {{ opacity: 1; transform: scale(1); z-index: 5; }}
        {p_end:.3f}%, 100% {{ opacity: 0; transform: scale(1.04); z-index: 0; }}
      }}"""

def build_chapter_pill_keyframe(name: str, start_s: float, end_s: float, total_dur: float, active_bg: str, active_border: str, is_first: bool = False, is_last: bool = False) -> str:
    p_start = max(0.0, (start_s / total_dur) * 100.0)
    p_in = min(100.0, ((start_s + 0.1) / total_dur) * 100.0)
    p_out = max(p_in + 0.05, ((end_s - 0.1) / total_dur) * 100.0)
    p_end = min(100.0, (end_s / total_dur) * 100.0)
    inactive = "background: rgba(255, 255, 255, 0.08); color: #94a3b8; border-color: rgba(255, 255, 255, 0.15); transform: scale(1);"
    active = f"background: {active_bg}; color: #ffffff; border-color: {active_border}; box-shadow: 0 0 18px {active_bg}; transform: scale(1.04);"

    if is_first:
        return f"""
      @keyframes {name} {{
        0%, {p_out:.3f}% {{ {active} }}
        {p_end:.3f}%, 100% {{ {inactive} }}
      }}"""
    elif is_last:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ {inactive} }}
        {p_in:.3f}%, 100% {{ {active} }}
      }}"""
    else:
        return f"""
      @keyframes {name} {{
        0%, {max(0.0, p_start - 0.05):.3f}% {{ {inactive} }}
        {p_in:.3f}%, {p_out:.3f}% {{ {active} }}
        {p_end:.3f}%, 100% {{ {inactive} }}
      }}"""

def render_zote_storybook_css():
    print("\n" + "="*75)
    print("🎬 RE-RENDERIZANDO JABÓN ZOTE STORYBOOK CON @KEYFRAMES CSS NATIVOS...")
    print("="*75)

    temp_dir = BASE_DIR / "temp_audio_stupy_14_zote"
    chunk_files = sorted(temp_dir.glob("chunk_*.mp3"))
    durations = [get_duration(c) for c in chunk_files]

    final_master = AUDIO_DIR / EPISODE_FILENAME
    total_dur = float(math.ceil(get_duration(final_master)))
    shutil.copy2(final_master, ENGINE_DIR / "assets" / "current_clip.mp3")
    shutil.copy2(final_master, ENGINE_DIR / "assets" / "audio.mp3")

    cur_t = 0.0
    scene_timings = []
    for i, (item, d) in enumerate(zip(DIALOGUE, durations)):
        st = cur_t
        et = cur_t + d if i < len(DIALOGUE) - 1 else total_dur
        scene_timings.append({
            "index": i,
            "start": st,
            "end": et,
            "speaker": item["speaker"],
            "chapter": item["chapter"],
            "img": item["img"],
            "tag": item["tag"],
            "headline": item["headline"],
            "pill": item["pill"],
            "caption": item["caption_short"]
        })
        cur_t += d

    # Group chapter start/end times
    chap_ranges = {}
    for st in scene_timings:
        ch = st["chapter"]
        if ch not in chap_ranges:
            chap_ranges[ch] = [st["start"], st["end"]]
        else:
            chap_ranges[ch][1] = st["end"]

    # Build CSS keyframes for all 9 scenes and 5 chapter pills
    keyframes_css = []
    for i, st in enumerate(scene_timings):
        kf_name = f"showStoryScene{i}"
        keyframes_css.append(build_css_keyframe_rule(
            kf_name, st["start"], st["end"], total_dur,
            is_first=(i == 0), is_last=(i == len(scene_timings) - 1)
        ))
        keyframes_css.append(f"#scene-{i} {{ animation: {kf_name} {total_dur:.1f}s linear forwards; }}")

        # Also zoom image during its active window
        p_s = (st["start"] / total_dur) * 100.0
        p_e = (st["end"] / total_dur) * 100.0
        keyframes_css.append(f"""
      @keyframes zoomImg{i} {{
        0%, {p_s:.3f}% {{ transform: scale(1.0); }}
        {p_e:.3f}%, 100% {{ transform: scale(1.10); }}
      }}
      #scene-{i} .story-img {{ animation: zoomImg{i} {total_dur:.1f}s linear forwards; }}""")

    for ch in range(1, 6):
        c_start, c_end = chap_ranges[ch]
        kf_ch = f"chapActive{ch}"
        keyframes_css.append(build_chapter_pill_keyframe(
            kf_ch, c_start, c_end, total_dur,
            active_bg="#ec4899", active_border="#f9a8d4",
            is_first=(ch == 1), is_last=(ch == 5)
        ))
        keyframes_css.append(f"#chap-{ch} {{ animation: {kf_ch} {total_dur:.1f}s linear forwards; }}")

    keyframes_joined = "\n".join(keyframes_css)

    scenes_html_parts = []
    for st in scene_timings:
        idx = st["index"]
        speaker_color = "#ec4899" if st["speaker"] == "DALIA" else "#06b6d4"
        speaker_badge = f"🎙️ {st['speaker']}"
        scenes_html_parts.append(f"""
        <div class="story-scene" id="scene-{idx}">
          <div class="top-meta-row">
            <span class="chapter-tag">{st['tag']}</span>
            <span class="speaker-pill" style="background: {speaker_color};">{speaker_badge}</span>
          </div>

          <div class="illustration-frame">
            <img src="../{st['img']}" class="story-img" alt="Ilustración escena {idx+1}" />
            <div class="floating-badge">{st['pill']}</div>
          </div>

          <div class="story-text-box">
            <div class="story-headline">{st['headline']}</div>
            <div class="story-caption">“{st['caption']}”</div>
          </div>
        </div>""")

    scenes_joined = "\n".join(scenes_html_parts)

    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>sIA Storybook #14 - Jabón Zote & La Corona</title>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0f0718; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .clip {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="sia_storybook_14_zote" data-no-timeline data-start="0" data-duration="{total_dur:.1f}" data-width="1080" data-height="1920">
      <audio id="bg-audio" class="clip" data-start="0" data-duration="{total_dur:.1f}" data-track-index="0" data-volume="1.0" src="assets/current_clip.mp3"></audio>
      <div id="main-scene" class="clip" data-composition-id="scene" data-composition-src="compositions/scene.html" data-start="0" data-duration="{total_dur:.1f}" data-track-index="1"></div>
    </div>
  </body>
</html>"""
    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    scene_html = f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>sIA Storybook 14 - Jabón Zote & Fábrica La Corona</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@800&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #0f0718;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        position: relative;
      }}

      .halftone-overlay {{
        position: absolute;
        inset: 0;
        background-image: radial-gradient(#ec4899 1.5px, transparent 1.5px);
        background-size: 26px 26px;
        opacity: 0.14;
        z-index: 1;
        pointer-events: none;
      }}

      .bg-ticker {{
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: space-around;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 76px;
        color: rgba(236, 72, 153, 0.06);
        text-transform: uppercase;
        transform: rotate(-10deg) scale(1.35);
        top: 22%;
        z-index: 0;
      }}

      .reel-wrapper {{
        position: relative;
        z-index: 10;
        width: 1080px;
        height: 1920px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 64px 52px 84px 52px;
      }}

      .header-box {{ display: flex; flex-direction: column; gap: 14px; }}
      .brand-row {{ display: flex; align-items: center; justify-content: space-between; }}
      .brand-pill {{
        background: #ec4899;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 23px;
        padding: 10px 24px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.6);
        border: 2px solid #ffffff;
      }}

      .tag-pill {{
        background: rgba(6, 182, 212, 0.18);
        color: #22d3ee;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 20px;
        padding: 8px 18px;
        border-radius: 12px;
        border: 2px solid #06b6d4;
      }}

      .chapters-bar {{ display: flex; gap: 8px; width: 100%; }}
      .chapter-pill {{
        flex: 1;
        padding: 10px 4px;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 13px;
        color: #94a3b8;
        text-transform: uppercase;
      }}

      .storybook-card {{
        background: #ffffff;
        border-radius: 36px;
        padding: 34px 36px;
        color: #0f172a;
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.85), 0 0 40px rgba(236, 72, 153, 0.3);
        border: 6px solid #ec4899;
        height: 1280px;
        position: relative;
        overflow: hidden;
      }}

      .story-scene {{
        position: absolute;
        inset: 34px 36px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 20px;
        opacity: 0;
      }}

      .top-meta-row {{ display: flex; justify-content: space-between; align-items: center; }}
      .chapter-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 20px;
        color: #be185d;
        background: #fce7f3;
        padding: 8px 18px;
        border-radius: 10px;
        border: 2px solid #f472b6;
      }}

      .speaker-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 21px;
        color: #ffffff;
        padding: 8px 20px;
        border-radius: 999px;
      }}

      .illustration-frame {{
        position: relative;
        width: 100%;
        height: 760px;
        border-radius: 26px;
        overflow: hidden;
        border: 5px solid #0f172a;
        box-shadow: 0 18px 36px rgba(15, 23, 42, 0.25);
        background: #1e293b;
      }}

      .story-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        transform-origin: center center;
      }}

      .floating-badge {{
        position: absolute;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 23, 42, 0.92);
        color: #f472b6;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 22px;
        padding: 10px 24px;
        border-radius: 14px;
        border: 2px solid #ec4899;
        white-space: nowrap;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
      }}

      .story-text-box {{
        background: #f8fafc;
        border: 3px solid #cbd5e1;
        border-radius: 24px;
        padding: 24px 28px;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }}

      .story-headline {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 38px;
        color: #0f172a;
        line-height: 1.1;
        letter-spacing: -0.5px;
      }}

      .story-caption {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 27px;
        color: #334155;
        line-height: 1.32;
      }}

      .footer-badge {{ display: flex; flex-direction: column; align-items: center; gap: 12px; }}
      .omnicanal-bar {{ display: flex; gap: 16px; justify-content: center; width: 100%; }}
      .omni-pill {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 18px;
        padding: 8px 16px;
        border-radius: 10px;
        background: rgba(255,255,255,0.08);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.2);
      }}

      .progress-bar-container {{
        width: 100%;
        height: 16px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 9999px;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }}

      @keyframes progressFillAnim {{
        0% {{ width: 0%; }}
        100% {{ width: 100%; }}
      }}

      .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #ec4899 0%, #06b6d4 100%);
        width: 0%;
        animation: progressFillAnim {total_dur:.1f}s linear forwards;
      }}

      {keyframes_joined}
    </style>
  </head>
  <body>
  <div id="scene-root" data-composition-id="scene" data-width="1080" data-height="1920" style="position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;">
    <div class="halftone-overlay"></div>
    <div class="bg-ticker">JABÓN ZOTE &bull; LA CORONA &bull; ECATEPEC &bull; 1920 &bull; MÉXICO</div>

    <div class="reel-wrapper">
      <div class="header-box">
        <div class="brand-row">
          <div class="brand-pill">🧼 sIA Crónicas #08</div>
          <div class="tag-pill">CUENTO ILUSTRADO</div>
        </div>

        <div class="chapters-bar">
          <div class="chapter-pill" id="chap-1">01 Baños 1920</div>
          <div class="chapter-pill" id="chap-2">02 Ecatepec</div>
          <div class="chapter-pill" id="chap-3">03 Química Zote</div>
          <div class="chapter-pill" id="chap-4">04 Seúl & Wall St</div>
          <div class="chapter-pill" id="chap-5">05 Coche / Video</div>
        </div>
      </div>

      <div class="storybook-card">
        {scenes_joined}
      </div>

      <div class="footer-badge">
        <div class="omnicanal-bar">
          <span class="omni-pill">🚗 Coche: Spotify (sIA)</span>
          <span class="omni-pill">📱 Video: YouTube & TikTok (@escucha_sia)</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
    </div>
  </div>
  </body>
</html>"""

    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")

    # Render with HyperFrames GPU
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    renders_dir = ENGINE_DIR / "renders"
    if renders_dir.exists():
        for old_vid in renders_dir.glob("*.mp4"):
            try:
                old_vid.unlink()
            except Exception:
                pass

    cmd = ["cmd.exe", "/c", f"set PATH={NODE_PATH};%PATH% && cd /d {ENGINE_DIR} && npx hyperframes render --gpu"]
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"HyperFrames error: {res.stderr}")

    output_mp4 = renders_dir / "video.mp4"
    if not output_mp4.exists():
        candidates = list(renders_dir.glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
    if not output_mp4.exists():
        print("HyperFrames stdout:", res.stdout)
        print("HyperFrames stderr:", res.stderr)
        raise RuntimeError("No se encontró el MP4 en renders/")
    target_reel = REELS_DIR / REEL_FILENAME
    shutil.copy2(output_mp4, target_reel)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / REEL_FILENAME)
    if GDRIVE_REELS_DIR.exists():
        shutil.copy2(output_mp4, GDRIVE_REELS_DIR / REEL_FILENAME)

    # Extract 5 verification frames across the video to prove every scene changes!
    out_audit = SCRATCH_DIR / "zote_fixed_frames"
    out_audit.mkdir(parents=True, exist_ok=True)
    for sec in [5, 40, 75, 115, 165, 200]:
        fp = out_audit / f"zote_fixed_{sec}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sec), "-i", str(target_reel),
            "-vframes", "1", "-q:v", "2", str(fp)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  📸 Frame verificado {sec}s: {fp.name} ({fp.stat().st_size} bytes)")

if __name__ == "__main__":
    render_zote_storybook_css()
