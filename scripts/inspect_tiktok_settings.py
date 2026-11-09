import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        print("Navegando a TikTok Studio Content...")
        page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        page.screenshot(path=str(SCRATCH_DIR / "tiktok_content_full.png"))

        # Inspect table rows
        rows = page.locator("tbody tr, div[data-tt*='PostItem']").all()
        print(f"Total filas encontradas: {len(rows)}")

        # Check options for the first and second videos
        # Let's inspect upload page settings for subtitles
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        page.evaluate("window.scrollTo(0, 1000)")
        time.sleep(1)
        page.screenshot(path=str(SCRATCH_DIR / "tiktok_upload_settings.png"))

        # Check text in upload page
        text_content = page.locator("body").inner_text()
        print("Opciones en Upload:")
        for line in text_content.splitlines():
            if any(k in line.lower() for k in ["subtítulo", "idioma", "traduc", "ajuste", "mostrar"]):
                print("  ->", line.strip())

        browser.close()

if __name__ == "__main__":
    main()
