import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

def test():
    print("[*] Iniciando Playwright con sesión guardada...", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 850},
            locale="es-ES"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        print("[*] Navegando a TikTok Studio Upload...", flush=True)
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        
        print("URL actual:", page.url, flush=True)
        print("Título:", page.title(), flush=True)
        
        screenshot_path = SCRATCH_DIR / "tiktok_studio_upload_test.png"
        page.screenshot(path=str(screenshot_path))
        print(f"[+] Captura guardada en: {screenshot_path}", flush=True)
        
        # Detectar input file o iframe
        file_inputs = page.locator("input[type='file']").all()
        print(f"File inputs encontrados: {len(file_inputs)}", flush=True)
        
        # Detectar iframes si los hay
        frames = page.frames
        print(f"Frames en la página: {len(frames)}", flush=True)
        for idx, fr in enumerate(frames):
            print(f"  Frame [{idx}]: {fr.url[:80]}", flush=True)
            inputs_in_fr = fr.locator("input[type='file']").all()
            if inputs_in_fr:
                print(f"    -> Tiene {len(inputs_in_fr)} input[type='file']!", flush=True)
                
        browser.close()

if __name__ == "__main__":
    test()
