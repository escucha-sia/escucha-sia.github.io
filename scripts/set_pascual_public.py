import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SESSION_FILE = Path(r"C:\Carlos\noticias_podcast\tiktok_session.json")
SCRATCH_DIR = Path(r"C:\Carlos\noticias_podcast\scratch")

def make_pascual_public():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()
        print("Accediendo a TikTok Studio...")
        page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)

        # Esperar que termine el processing si aún está
        for _ in range(6):
            btn_privacy = page.locator("button:has-text('Only me'), div:has-text('Only me'), [data-tt*='Privacy']").first
            if btn_privacy.count() > 0 and btn_privacy.is_visible():
                print("Haciendo clic en selector de privacidad...")
                btn_privacy.click()
                time.sleep(1.5)

                opt_everyone = page.locator("div[role='option']:has-text('Everyone'), div:has-text('Everyone'), li:has-text('Everyone'), div:has-text('Público')").first
                if opt_everyone.count() > 0 and opt_everyone.is_visible():
                    opt_everyone.click()
                    print("¡Privacidad cambiada a Everyone!")
                    time.sleep(2)
                    break
            time.sleep(5)

        page.screenshot(path=str(SCRATCH_DIR / "pascual_public_check.png"))
        print("Screenshot guardado en scratch/pascual_public_check.png")
        browser.close()

if __name__ == "__main__":
    make_pascual_public()
