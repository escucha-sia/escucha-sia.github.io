import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Carlos\noticias_podcast")
SCENE_HTML = ROOT_DIR / "sia_tiktok_batch_engine" / "compositions" / "boeing_scene.html"
SCRATCH_DIR = ROOT_DIR / "scratch"

def verify_scenes():
    print("📸 Verificando escenas de boeing_scene.html con Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        
        # Load local HTML
        page.goto(f"file:///{str(SCENE_HTML).replace(chr(92), '/')}")
        time.sleep(2)
        
        # Capture Act 1
        page.screenshot(path=str(SCRATCH_DIR / "boeing_act1_preview.png"))
        print("  [✓] Acto 1 capturado: scratch/boeing_act1_preview.png")
        
        # Force show Card 2
        page.evaluate("""() => {
            for (let i = 1; i <= 5; i++) {
                const el = document.getElementById(`card-${i}`);
                if (el) el.style.animation = 'none';
            }
            document.getElementById('card-1').style.display = 'none';
            document.getElementById('card-2').style.opacity = '1';
            document.getElementById('card-2').style.transform = 'none';
            document.getElementById('card-2').style.zIndex = '10';
        }""")
        time.sleep(1)
        page.screenshot(path=str(SCRATCH_DIR / "boeing_act2_preview.png"))
        print("  [✓] Acto 2 capturado: scratch/boeing_act2_preview.png")

        # Force show Card 3
        page.evaluate("""() => {
            document.getElementById('card-2').style.display = 'none';
            document.getElementById('card-3').style.opacity = '1';
            document.getElementById('card-3').style.transform = 'none';
            document.getElementById('card-3').style.zIndex = '10';
        }""")
        time.sleep(1)
        page.screenshot(path=str(SCRATCH_DIR / "boeing_act3_preview.png"))
        print("  [✓] Acto 3 capturado: scratch/boeing_act3_preview.png")

        # Force show Card 4
        page.evaluate("""() => {
            document.getElementById('card-3').style.display = 'none';
            document.getElementById('card-4').style.opacity = '1';
            document.getElementById('card-4').style.transform = 'none';
            document.getElementById('card-4').style.zIndex = '10';
        }""")
        time.sleep(1)
        page.screenshot(path=str(SCRATCH_DIR / "boeing_act4_preview.png"))
        print("  [✓] Acto 4 capturado: scratch/boeing_act4_preview.png")

        # Force show Card 5
        page.evaluate("""() => {
            document.getElementById('card-4').style.display = 'none';
            document.getElementById('card-5').style.opacity = '1';
            document.getElementById('card-5').style.transform = 'none';
            document.getElementById('card-5').style.zIndex = '10';
        }""")
        time.sleep(1)
        page.screenshot(path=str(SCRATCH_DIR / "boeing_act5_preview.png"))
        print("  [✓] Acto 5 capturado: scratch/boeing_act5_preview.png")

        browser.close()
    print("✨ Todas las escenas fueron verificadas exitosamente.")

if __name__ == "__main__":
    verify_scenes()
