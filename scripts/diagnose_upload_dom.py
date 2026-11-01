import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
VIDEO_PATH = BASE_DIR / "reels" / "sIA_Reel_Stupy_01_Mito_IA_Codigo.mp4"

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        print("[*] Navegando a TikTok Studio Upload...", flush=True)
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        
        # Click on body to dismiss any tooltip
        page.mouse.click(600, 300)
        time.sleep(1)
        
        file_input = page.locator("input[type='file']").first
        print("[*] Seleccionando archivo...", flush=True)
        file_input.set_input_files(str(VIDEO_PATH))
        
        # Monitorear cada 5 segundos durante 25 segundos
        for i in range(1, 6):
            time.sleep(5)
            print(f"\n--- Check {i} ({i*5}s tras set_input_files) ---", flush=True)
            print("URL:", page.url, flush=True)
            
            # Buscar iframes
            for idx, fr in enumerate(page.frames):
                if fr != page.main_frame:
                    print(f"  Iframe [{idx}]: {fr.url[:80]}", flush=True)
                    
            # Buscar textos clave en la página
            texts = ["Subir", "Publicar", "Post", "Leyenda", "Caption", "Portada", "Cover", "Cancelar", "Descartar", "%", "Cargando"]
            found = []
            for t in texts:
                if page.get_by_text(t).count() > 0:
                    found.append(t)
            print("Textos encontrados:", found, flush=True)
            
            # Buscar inputs y botones
            btns = [b.text_content().strip() for b in page.locator("button").all() if b.is_visible()]
            print("Botones visibles:", btns[:10], flush=True)
            
            page.screenshot(path=str(SCRATCH_DIR / f"diag_check_{i}.png"))
            
        browser.close()

if __name__ == "__main__":
    test()
