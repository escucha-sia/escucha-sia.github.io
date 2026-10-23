"""
sIA Motion Graphics Reel Generator: Terror #02 (El Moderador del Turno Nocturno)
Tema: Anomalías en la Cola 7 de Moderación Algorítmica en Austin, Texas
Duración: 45.0 Segundos CERRADOS (Producto Terminado Completo)
- Audio propio sintetizado en 45 segundos con arco de misterio completo (Jorge + Dalia).
- Infografía animada de la evolución: Alerta 0x7ff -> Ángulo a la espalda -> Reloj en reversa -> Bloqueo de Cuarentena -> Redirección.
- Redirección omnicanal total: enlaza visual y verbalmente a Spotify y al Blog.
"""

import os
import sys
import shutil
import asyncio
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
ENGINE_DIR = BASE_DIR / "sia_tiktok_batch_engine"
AUDIO_DIR = BASE_DIR / "audio"
REELS_DIR = BASE_DIR / "reels"
SPOTIFY_REELS_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels")
NODE_PATH = r"C:\Carlos\nodejs"

TARGET_REEL = REELS_DIR / "sIA_Terror_02_El_Moderador_Nocturno_Reel.mp4"
DURATION = 45.0

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_FEMALE = "es-MX-DaliaNeural"

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "A las tres y catorce de la madrugada en Austin, Texas, un monitor solitario emitió una alerta imposible: Archivo huérfano. Confianza: cero por ciento. Topología: no humana."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_FEMALE,
        "text": "El analista nocturno reprodujo el clip de seis segundos: la toma apuntaba a su propia espalda en tiempo real, mientras el reloj en la pantalla comenzó a correr en reversa."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "Al intentar escapar, la puerta magnética se bloqueó por cuarentena. La temperatura bajó a ocho grados y la figura en el video comenzó a imitar sus movimientos."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_FEMALE,
        "text": "A la mañana siguiente solo hallaron su silla en el suelo y una terminal parpadeando. Conoce el expediente completo en escucha guion sia punto github punto io y en Sia Podcast."
    }
]

async def generate_reel_audio():
    print("🎙️ Sintetizando audio cerrado de 45 segundos para Terror #02...")
    temp_dir = ENGINE_DIR / "temp_audio_terror_02"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        communicate = edge_tts.Communicate(item["text"], item["voice"], rate="+3%")
        await communicate.save(str(chunk_path))
        chunk_files.append(chunk_path)
        
    concat_list = temp_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            p = str(cf).replace('\\', '/')
            f.write(f"file '{p}'\n")
            
    clip_audio = ENGINE_DIR / "assets" / "current_clip.mp3"
    clip_audio.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-af", f"apad=whole_dur={DURATION},afade=t=out:st=44.0:d=1.0",
        str(clip_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Audio de Terror #02 sintetizado y ensamblado con éxito.")

def write_hyperframes_html():
    index_html = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #080c16;
      }}
      #root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
      }}
      .clip {{
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="sia_motion_reel_terror_02" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
      <audio
        id="bg-audio"
        class="clip"
        data-start="0"
        data-duration="{DURATION}"
        data-track-index="0"
        data-volume="1.0"
        src="assets/current_clip.mp3"
      ></audio>

      <div
        id="main-scene"
        class="clip"
        data-composition-id="scene"
        data-composition-src="compositions/scene.html"
        data-start="0"
        data-duration="{DURATION}"
        data-track-index="1"
      ></div>
    </div>
  </body>
</html>"""

    (ENGINE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    scene_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700;800&family=Inter:wght@400;600;700;900&display=swap');

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1080px;
        height: 1920px;
        background: #04060c;
        color: #f8fafc;
        font-family: 'Space Grotesk', sans-serif;
        overflow: hidden;
      }}

      .canvas-container {{
        position: relative;
        width: 1080px;
        height: 1920px;
        background: radial-gradient(circle at 50% 25%, #180d26 0%, #080a14 55%, #020307 100%);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 90px 70px 100px 70px;
      }}

      /* Scanline / CRT overlay */
      .crt-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(rgba(18, 16, 26, 0) 50%, rgba(0, 0, 0, 0.4) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
        background-size: 100% 4px, 6px 100%;
        pointer-events: none;
        opacity: 0.7;
        z-index: 100;
      }}

      /* Header */
      .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
      }}
      .brand-badge {{
        display: flex;
        align-items: center;
        gap: 16px;
        background: rgba(239, 68, 68, 0.12);
        border: 2px solid rgba(239, 68, 68, 0.4);
        padding: 14px 28px;
        border-radius: 999px;
      }}
      .brand-dot {{
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #ef4444;
        box-shadow: 0 0 20px #ef4444;
      }}
      .brand-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #ef4444;
      }}
      .episode-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 700;
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        padding: 12px 24px;
        border-radius: 12px;
        border: 1px solid rgba(168, 85, 247, 0.3);
      }}

      /* Main Title */
      .title-section {{
        text-align: center;
        z-index: 10;
        margin-top: 10px;
      }}
      .main-title {{
        font-size: 58px;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -1.5px;
        color: #ffffff;
      }}
      .highlight-red {{
        color: #ef4444;
        text-shadow: 0 0 35px rgba(239, 68, 68, 0.6);
      }}
      .highlight-purple {{
        color: #c084fc;
        text-shadow: 0 0 35px rgba(192, 132, 252, 0.6);
      }}

      /* Center Stage Graphics */
      .stage-card {{
        position: relative;
        background: rgba(15, 23, 42, 0.75);
        border: 2px solid rgba(239, 68, 68, 0.3);
        border-radius: 36px;
        padding: 45px 40px;
        backdrop-filter: blur(25px);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
        z-index: 10;
        min-height: 720px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
      }}

      /* Timeline Stages */
      .timeline-box {{
        display: flex;
        flex-direction: column;
        gap: 22px;
      }}
      .timeline-item {{
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 22px 26px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
      }}
      .timeline-icon {{
        font-size: 38px;
        width: 65px;
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(239, 68, 68, 0.15);
        border-radius: 16px;
      }}
      .timeline-text {{
        display: flex;
        flex-direction: column;
        gap: 6px;
      }}
      .timeline-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        color: #94a3b8;
        letter-spacing: 1px;
      }}
      .timeline-val {{
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
      }}

      /* Terminal Block */
      .terminal-code {{
        background: #020617;
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 20px;
        padding: 24px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        color: #ef4444;
        line-height: 1.5;
        box-shadow: inset 0 0 30px rgba(239, 68, 68, 0.15);
      }}

      /* Live Subtitles */
      .subtitles-card {{
        background: rgba(2, 6, 23, 0.85);
        border: 2px solid rgba(168, 85, 247, 0.4);
        border-radius: 24px;
        padding: 24px 32px;
        text-align: center;
        z-index: 10;
        min-height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .subtitles-text {{
        font-size: 32px;
        font-weight: 600;
        line-height: 1.35;
        color: #f1f5f9;
      }}

      /* Omnichannel Footer */
      .footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
        gap: 20px;
      }}
      .footer-item {{
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 18px 24px;
        border-radius: 20px;
        font-size: 24px;
        font-weight: 700;
      }}
      .footer-spotify {{
        color: #1ed760;
        border-color: rgba(30, 215, 96, 0.3);
      }}
      .footer-web {{
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.3);
      }}
    </style>
  </head>
  <body>
    <div id="scene-root" class="canvas-container" data-composition-id="scene" data-width="1080" data-height="1920">
      <div class="crt-overlay"></div>

      <!-- Header -->
      <div class="header">
        <div class="brand-badge">
          <div class="brand-dot"></div>
          <span class="brand-title">sIA TERROR</span>
        </div>
        <div class="episode-badge">EXPEDIENTE #02</div>
      </div>

      <!-- Main Title -->
      <div class="title-section">
        <h1 class="main-title">EL MODERADOR DEL <span class="highlight-red">TURNO NOCTURNO</span></h1>
        <p style="font-size: 30px; color: #cbd5e1; margin-top: 12px; font-weight: 600;">
          Anomalías en la <span class="highlight-purple">Cola 7</span> en Austin, Texas
        </p>
      </div>

      <!-- Center Stage Infographic -->
      <div class="stage-card">
        <div class="terminal-code">
          > PROTOCOLO: COLA_7_MONITOR<br>
          > CLASIFICACIÓN: [TOPOLOGÍA NO HUMANA]<br>
          > CONFIANZA: 0.00% | ORIGEN: CÁMARA TRASERA<br>
          > ESTADO: BLOQUEO CUARENTENA (8°C)
        </div>

        <div class="timeline-box">
          <div class="timeline-item">
            <div class="timeline-icon">🚨</div>
            <div class="timeline-text">
              <span class="timeline-label">03:14 AM · AUSTIN TEXAS</span>
              <span class="timeline-val">Archivo Huérfano 0x7ff</span>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-icon">⏳</div>
            <div class="timeline-text">
              <span class="timeline-label">ANOMALÍA TEMPORAL</span>
              <span class="timeline-val">Reloj corriendo en reversa</span>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-icon">👥</div>
            <div class="timeline-text">
              <span class="timeline-label">EL REFLEJO</span>
              <span class="timeline-val">La sombra copia sus parpadeos</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Subtitle Box -->
      <div class="subtitles-card">
        <p class="subtitles-text">
          🎧 Escucha el expediente completo con diseño sonoro SFX inmersivo.
        </p>
      </div>

      <!-- Omnichannel Footer -->
      <div class="footer">
        <div class="footer-item footer-spotify">
          <span>🟢</span> Escúchalo en Spotify
        </div>
        <div class="footer-item footer-web">
          <span>🌐</span> escucha-sia.github.io
        </div>
      </div>
    </div>
  </body>
</html>"""

    (ENGINE_DIR / "compositions" / "scene.html").write_text(scene_html, encoding="utf-8")
    print("✅ Composición HTML/CSS de Terror #02 generada con éxito.")

def render_motion_reel():
    print("🎬 Renderizando Reel vertical en HyperFrames GPU...")
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    
    cmd = ["cmd.exe", "/c", f"cd /d {ENGINE_DIR} && npx hyperframes render --gpu"]
    res = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Buscar el archivo renderizado en .hyperframes o renders
    output_mp4 = ENGINE_DIR / "renders" / "video.mp4"
    if not output_mp4.exists():
        # Buscar en renders cualquier mp4 reciente
        candidates = list((ENGINE_DIR / "renders").glob("*.mp4"))
        if candidates:
            output_mp4 = max(candidates, key=lambda p: p.stat().st_mtime)
            
    if not output_mp4.exists():
        raise RuntimeError(f"Fallo al renderizar Reel: {res.stderr or res.stdout}")
        
    REELS_DIR.mkdir(parents=True, exist_ok=True)
    SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(output_mp4, TARGET_REEL)
    shutil.copy2(output_mp4, SPOTIFY_REELS_DIR / TARGET_REEL.name)
    
    size_mb = TARGET_REEL.stat().st_size / (1024 * 1024)
    print(f"✅ ¡Video Motion Graphics generado con éxito! ({size_mb:.2f} MB)")
    print(f"   -> {TARGET_REEL}")
    
    # Extraer póster JPG en el segundo 2
    poster_path = REELS_DIR / f"{TARGET_REEL.stem}_poster.jpg"
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "00:00:02",
        "-i", str(TARGET_REEL),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if poster_path.exists():
        shutil.copy2(poster_path, SPOTIFY_REELS_DIR / poster_path.name)
        print(f"   -> Póster en: {poster_path}")

async def run():
    await generate_reel_audio()
    write_hyperframes_html()
    render_motion_reel()
    print("\n🎉 ¡Reel de Terror #02 listo para publicación!")

if __name__ == '__main__':
    asyncio.run(run())
