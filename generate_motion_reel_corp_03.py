"""
sIA Motion Graphics Reel Generator: Corporativo #03 (Nintendo vs. Sony)
Tema: La Gran Traición de 1991 y el Nacimiento de PlayStation por Pura Venganza
Duración: 45.0 Segundos CERRADOS (Producto Terminado Completo)
- Audio propio sintetizado en 45 segundos con arco narrativo completo (Jorge + Dalia).
- Infografía animada de la evolución: CES 1991 Traición -> Puñetazo de Ohga -> Discos vs Cartuchos -> Fuga de Final Fantasy VII -> 102M Ventas.
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

TARGET_REEL = REELS_DIR / "sIA_Corp_03_Nintendo_Sony_Playstation_Reel.mp4"
DURATION = 45.0

VOICE_JORGE = "es-MX-JorgeNeural"
VOICE_DALIA = "es-MX-DaliaNeural"

REEL_DIALOGUE = [
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "¿Cómo una humillación pública en mil novecientos noventa y uno creó al verdugo que destronó a Nintendo?"
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "En el CES de Chicago, Sony anunció orgullosa su consola conjunta Play Station. Veinticuatro horas después, Nintendo subió al escenario y anunció que rompía con Sony para irse con Philips frente a toda la prensa mundial."
    },
    {
        "speaker": "JORGE",
        "voice": VOICE_JORGE,
        "text": "En Tokio, el presidente de Sony dio un golpe en la mesa y ordenó construir la consola para destruirlos. Mientras Nintendo insistía en cartuchos de treinta dólares, Sony apostó por discos CD de dos dólares y gráficos 3D."
    },
    {
        "speaker": "DALIA",
        "voice": VOICE_DALIA,
        "text": "Square abandonó a Nintendo con Final Fantasy siete, desatando una fuga masiva. PlayStation vendió más de cien millones de consolas y consumó la venganza. Conoce la historia completa en escucha guion sia punto github punto io y en sIA Podcast."
    }
]

async def generate_reel_audio():
    print("🎙️ Sintetizando audio cerrado de 45 segundos para Corporativo #03...")
    temp_dir = ENGINE_DIR / "temp_audio_corp_03"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_files = []
    for idx, item in enumerate(REEL_DIALOGUE):
        chunk_path = temp_dir / f"chunk_{idx}.mp3"
        communicate = edge_tts.Communicate(item["text"], item["voice"], rate="+2%")
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
    print("✅ Audio de Corporativo #03 sintetizado y ensamblado con éxito.")

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
    <div id="root" data-composition-id="sia_motion_reel_corp_03" data-no-timeline data-start="0" data-duration="{DURATION}" data-width="1080" data-height="1920">
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
</html>
"""
    with open(ENGINE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    scene_html = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800;900&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html, body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #080c16;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
      }
      
      .canvas-container {
        position: relative;
        width: 1080px;
        height: 1920px;
        padding: 80px 60px 100px 60px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: 
          radial-gradient(circle at 50% 15%, rgba(0, 112, 209, 0.28) 0%, transparent 60%),
          radial-gradient(circle at 80% 80%, rgba(239, 68, 68, 0.2) 0%, transparent 65%),
          linear-gradient(180deg, #080c16 0%, #111a2e 50%, #080c16 100%);
      }

      /* Grid de precisión técnica */
      .grid-overlay {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(0, 112, 209, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 112, 209, 0.06) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
      }

      /* TOP BAR */
      .header-hud {
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
      }
      .badge-series {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 10px 24px;
        background: rgba(0, 112, 209, 0.18);
        border: 1px solid rgba(0, 112, 209, 0.5);
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #60a5fa;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 25px rgba(0, 112, 209, 0.3);
      }
      .badge-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #0070d1;
        box-shadow: 0 0 14px #0070d1;
      }
      .badge-telemetry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(0, 112, 209, 0.3);
        padding: 8px 20px;
        border-radius: 8px;
        letter-spacing: 1px;
      }

      /* HOOK CARD */
      .hook-card {
        margin-top: 30px;
        padding: 34px 40px;
        background: rgba(17, 26, 46, 0.85);
        border: 1px solid rgba(0, 112, 209, 0.4);
        border-radius: 28px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        z-index: 10;
      }
      .hook-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 800;
        color: #60a5fa;
        letter-spacing: 3px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .hook-title {
        font-size: 42px;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -0.5px;
        color: #ffffff;
      }
      .hook-highlight {
        color: #0070d1;
        background: linear-gradient(135deg, #38bdf8 0%, #0070d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }

      /* INFOGRAPHIC VISUAL STAGE */
      .diagram-stage {
        position: relative;
        flex: 1;
        margin: 30px 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 10;
      }

      .svg-diagram-card {
        width: 100%;
        height: 680px;
        background: rgba(10, 16, 30, 0.85);
        border: 1px solid rgba(0, 112, 209, 0.35);
        border-radius: 32px;
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.8);
      }

      /* Live market ticker */
      .market-ticker {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(0, 112, 209, 0.12);
        border: 1px solid rgba(0, 112, 209, 0.35);
        border-radius: 16px;
        padding: 16px 24px;
        font-family: 'JetBrains Mono', monospace;
      }
      .ticker-val {
        font-size: 34px;
        font-weight: 800;
        color: #60a5fa;
      }
      .ticker-tag {
        font-size: 17px;
        color: #94a3b8;
        letter-spacing: 1px;
      }

      /* 4-Step Timeline Cards */
      .timeline-flow {
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin-top: 15px;
      }
      .timeline-item {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 18px 24px;
        background: rgba(15, 23, 42, 0.65);
        border-radius: 16px;
        border-left: 6px solid #0070d1;
      }
      .timeline-item.warning {
        border-left-color: #ef4444;
        background: rgba(239, 68, 68, 0.08);
      }
      .timeline-item.cyan {
        border-left-color: #38bdf8;
        background: rgba(56, 189, 248, 0.08);
      }
      .t-year {
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #60a5fa;
        min-width: 80px;
      }
      .t-content h4 {
        font-size: 22px;
        font-weight: 800;
        color: #f8fafc;
      }
      .t-content p {
        font-size: 18px;
        color: #94a3b8;
        margin-top: 4px;
      }

      /* Ohga Fury Callout */
      .ohga-callout {
        background: rgba(15, 23, 42, 0.85);
        border: 1px dashed rgba(239, 68, 68, 0.5);
        border-radius: 18px;
        padding: 20px 24px;
        margin-top: 15px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 19px;
        color: #fca5a5;
        line-height: 1.4;
      }
      .ohga-callout strong {
        color: #ef4444;
      }

      /* SUBTITLE & AUDIO DISPLAY */
      .subtitle-card {
        padding: 30px 40px;
        background: rgba(17, 26, 46, 0.95);
        border: 1px solid rgba(0, 112, 209, 0.5);
        border-radius: 28px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        z-index: 10;
        margin-bottom: 20px;
      }
      .speaker-pill {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 12px;
      }
      .speaker-jorge {
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
      }
      .speaker-dalia {
        background: rgba(0, 112, 209, 0.2);
        color: #60a5fa;
        border: 1px solid rgba(0, 112, 209, 0.4);
      }
      .sub-text {
        font-size: 32px;
        font-weight: 700;
        line-height: 1.35;
        color: #ffffff;
      }

      /* BOTTOM FLYWHEEL CTA */
      .flywheel-cta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(0, 112, 209, 0.4);
        border-radius: 22px;
        padding: 22px 30px;
        z-index: 10;
      }
      .cta-item {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 20px;
        font-weight: 700;
      }
      .cta-pill {
        background: #0070d1;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        padding: 6px 16px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 18px;
      }
    </style>
  </head>
  <body>
    <div id="scene-root" class="canvas-container" data-composition-id="scene" data-width="1080" data-height="1920">
      <div class="grid-overlay"></div>

      <!-- TOP HUD -->
      <div class="header-hud">
        <div class="badge-series">
          <div class="badge-dot"></div>
          sIA Corporativo #03
        </div>
        <div class="badge-telemetry">NINTENDO VS SONY // PLAYSTATION</div>
      </div>

      <!-- HOOK CARD -->
      <div class="hook-card">
        <div class="hook-label">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          CRÓNICAS DE SILICON VALLEY & JAPÓN
        </div>
        <div class="hook-title">
          La Gran Traición de 1991 y el <span class="hook-highlight">Nacimiento de PlayStation</span>
        </div>
      </div>

      <!-- INFOGRAPHIC DIAGRAM STAGE -->
      <div class="diagram-stage">
        <div class="svg-diagram-card">
          <!-- Market cap ticker -->
          <div class="market-ticker">
            <div>
              <span class="ticker-tag">CONSOLAS VENDIDAS</span>
              <div class="ticker-val" id="sales-val">PLAYSTATION: 102M</div>
            </div>
            <div style="text-align: right;">
              <span class="ticker-tag">DERROTA HISTÓRICA</span>
              <div style="font-size: 20px; font-weight: 800; color: #ef4444;" id="status-tag">NINTENDO 64: 32M</div>
            </div>
          </div>

          <!-- Timeline Evolution -->
          <div class="timeline-flow">
            <div class="timeline-item" id="step-1">
              <div class="t-year">1988</div>
              <div class="t-content">
                <h4>Ken Kutaragi & Chip SPC700</h4>
                <p>Ingeniero clandestino diseña el sonido orquestal de SNES.</p>
              </div>
            </div>

            <div class="timeline-item warning" id="step-2">
              <div class="t-year">1991</div>
              <div class="t-content">
                <h4>La Traición Pública en CES</h4>
                <p>Sony anuncia la Play Station; 24h después Nintendo los humilla con Philips.</p>
              </div>
            </div>

            <div class="timeline-item cyan" id="step-3">
              <div class="t-year">1996</div>
              <div class="t-content">
                <h4>Fuga de Final Fantasy VII</h4>
                <p>Square abandona los cartuchos de Nintendo; Sony domina el mundo.</p>
              </div>
            </div>
          </div>

          <!-- Ohga Callout -->
          <div class="ohga-callout" id="ohga-memo">
            <strong>GOLPE EN LA MESA DE NORIO OHGA (1991):</strong><br>
            "¡Jamás retrocedan! ¡Kutaragi, hazlo! Desarrolla la consola tú solo, ponle 3D y constrúyela para aplastar a Nintendo en el mercado."
          </div>
        </div>
      </div>

      <!-- SUBTITLE CARD -->
      <div class="subtitle-card">
        <div id="speaker-badge" class="speaker-pill speaker-jorge">JORGE</div>
        <div id="caption-text" class="sub-text">
          ¿Cómo una humillación pública en mil novecientos noventa y uno creó al verdugo que destronó a Nintendo?
        </div>
      </div>

      <!-- BOTTOM FLYWHEEL CTA -->
      <div class="flywheel-cta">
        <div class="cta-item">
          <span>🎧 Spotify:</span>
          <span class="cta-pill">sIA Corporativo #03</span>
        </div>
        <div class="cta-item">
          <span>🌐 Blog:</span>
          <span class="cta-pill">escucha-sia.github.io</span>
        </div>
      </div>
    </div>

    <script>
      const tl = gsap.timeline();

      // Dialogue cues:
      // 0.0s - 8.0s: Jorge (Humiliation hook)
      // 8.0s - 21.0s: Dalia (CES Chicago & Philips shock)
      // 21.0s - 34.0s: Jorge (Norio Ohga table slam, CD vs Cartridges)
      // 34.0s - 45.0s: Dalia (Square Final Fantasy VII, 102M sales & CTA)

      tl.to({}, { duration: 8.0 });
      tl.call(() => {
        document.getElementById('speaker-badge').className = 'speaker-pill speaker-dalia';
        document.getElementById('speaker-badge').textContent = 'DALIA';
        document.getElementById('caption-text').textContent = 'En el CES de Chicago, Sony anunció la Play Station. 24 horas después, Nintendo rompió el pacto frente a la prensa mundial y se fue con Philips.';
        document.getElementById('step-1').style.borderColor = '#0070d1';
      });

      tl.to({}, { duration: 13.0 });
      tl.call(() => {
        document.getElementById('speaker-badge').className = 'speaker-pill speaker-jorge';
        document.getElementById('speaker-badge').textContent = 'JORGE';
        document.getElementById('caption-text').textContent = 'En Tokio, el presidente de Sony dio un golpe en la mesa y ordenó crear PlayStation para destruirlos. Mientras Nintendo insistía en cartuchos caros, Sony apostó por CDs y 3D.';
        document.getElementById('status-tag').textContent = '💥 GUERRA DE FORMATOS';
        document.getElementById('status-tag').style.color = '#38bdf8';
        document.getElementById('sales-val').textContent = 'CD ($2) vs CART ($30)';
      });

      tl.to({}, { duration: 13.0 });
      tl.call(() => {
        document.getElementById('speaker-badge').className = 'speaker-pill speaker-dalia';
        document.getElementById('speaker-badge').textContent = 'DALIA';
        document.getElementById('caption-text').textContent = 'Square abandonó a Nintendo con Final Fantasy 7. PlayStation vendió más de 102 millones de consolas y consumó la venganza. Conoce la historia en sIA Podcast.';
        document.getElementById('status-tag').textContent = 'NINTENDO 64: 32M';
        document.getElementById('status-tag').style.color = '#ef4444';
        document.getElementById('sales-val').textContent = 'PLAYSTATION: 102M';
      });
    </script>
  </body>
</html>
"""
    comp_dir = ENGINE_DIR / "compositions"
    comp_dir.mkdir(parents=True, exist_ok=True)
    with open(comp_dir / "scene.html", "w", encoding="utf-8") as f:
        f.write(scene_html)
    print("✅ Composición HTML/CSS de Corporativo #03 generada con éxito.")

def render_reel():
    print("🎬 Renderizando Reel vertical en HyperFrames GPU...")
    REELS_DIR.mkdir(parents=True, exist_ok=True)
    SPOTIFY_REELS_DIR.mkdir(parents=True, exist_ok=True)
    
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};" + env.get("PATH", "")
    
    cmd = [
        "cmd.exe", "/c",
        f"cd /d {ENGINE_DIR} && npx hyperframes render --gpu"
    ]
    res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error en HyperFrames render:\n{res.stderr}\n{res.stdout}")
        sys.exit(1)
        
    generated_mp4 = ENGINE_DIR / "renders" / "index.mp4"
    if not generated_mp4.exists():
        potential = sorted(list((ENGINE_DIR / "renders").glob("sia_tiktok_batch_engine_*.mp4")), key=os.path.getmtime, reverse=True)
        if potential:
            generated_mp4 = potential[0]
        else:
            print("❌ No se encontró el archivo mp4 renderizado.")
            sys.exit(1)
            
    shutil.copy2(generated_mp4, TARGET_REEL)
    shutil.copy2(generated_mp4, SPOTIFY_REELS_DIR / TARGET_REEL.name)
    
    # Generate poster
    poster_path = REELS_DIR / (TARGET_REEL.stem + "_poster.jpg")
    cmd_poster = [
        "ffmpeg", "-y",
        "-ss", "20.0",
        "-i", str(TARGET_REEL),
        "-vframes", "1",
        "-q:v", "2",
        str(poster_path)
    ]
    subprocess.run(cmd_poster, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    size_mb = os.path.getsize(TARGET_REEL) / (1024 * 1024)
    print(f"✅ ¡Video Motion Graphics generado con éxito! ({size_mb:.2f} MB)")
    print(f"   -> {TARGET_REEL}")
    print(f"   -> Póster en: {poster_path}")

async def main():
    await generate_reel_audio()
    write_hyperframes_html()
    render_reel()
    print("\n🎉 ¡Reel de Corporativo #03 listo para publicación!")

if __name__ == '__main__':
    asyncio.run(main())
