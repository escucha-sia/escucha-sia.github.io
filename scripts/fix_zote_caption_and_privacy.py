import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

NEW_CAPTION = (
    "🧼 ¿Cómo una fábrica mexicana de jabón en Ecatepec derrotó a gigantes de Wall Street sin gastar un solo peso en publicidad? "
    "De los Baños Corona de 1920 en Peralvillo a conquistar Corea del Sur con el Jabón Zote. "
    "🚗 Si vas en tu coche escúchanos en Spotify (sIA Podcast) | 📱 Mira este Cuento Ilustrado completo aquí en TikTok y YouTube (@escucha_sia). "
    "#jabonzote #hechoenmexico #industriales #historia #empresas #mexico #quimica #siapodcast"
)

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
        page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)

        # Click the pencil icon on the first row (x=809, y=254 on 1280x950 viewport)
        page.mouse.click(809, 254)
        time.sleep(5)
        page.screenshot(path=str(SCRATCH_DIR / "edit_modal_zote.png"))

        editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
        if editor.count() > 0:
            editor.click(force=True)
            time.sleep(0.5)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(NEW_CAPTION, delay=15)
            time.sleep(2)
            page.keyboard.press("Escape")
            time.sleep(1)

            save_btn = page.locator("button:has-text('Guardar'), button:has-text('Enviar'), button:has-text('Save'), button:has-text('Continuar'), button:has-text('Publicar')").first
            if save_btn.count() > 0:
                save_btn.click(force=True)
                time.sleep(8)
                print("✅ Leyenda actualizada y guardada con éxito.")
        page.screenshot(path=str(SCRATCH_DIR / "after_edit_zote.png"))
        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    main()
