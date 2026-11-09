import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SESSION_FILE = Path(r"C:\Carlos\noticias_podcast\tiktok_session.json")
SCRATCH_DIR = Path(r"C:\Carlos\noticias_podcast\scratch")

def make_moe_public():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()
        print("Accediendo a TikTok Studio Content...")
        page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=45000)
        time.sleep(6)

        # Reintentar hasta 10 veces (esperando que termine 'Content under review')
        for attempt in range(1, 11):
            print(f"Intento {attempt}: Verificando estado de privacidad...")
            page.reload(wait_until="domcontentloaded")
            time.sleep(5)
            
            # Buscar el primer botón o dropdown de privacidad que esté en Only me
            btn_privacy = page.locator("button:has-text('Only me'), div:has-text('Only me'), [data-tt*='Privacy']").first
            if btn_privacy.count() > 0 and btn_privacy.is_visible():
                print("Haciendo clic en selector de privacidad...")
                btn_privacy.click()
                time.sleep(1.5)

                opt_everyone = page.locator("div[role='option']:has-text('Everyone'), div:has-text('Everyone'), li:has-text('Everyone'), div:has-text('Público')").first
                if opt_everyone.count() > 0 and opt_everyone.is_visible():
                    opt_everyone.click()
                    print("¡Privacidad cambiada exitosamente a Everyone!")
                    time.sleep(2)
                    break
            else:
                first_row = page.locator("div[role='row'], tr, div.table-row").first
                if first_row.count() > 0 and "Everyone" in first_row.inner_text():
                    print("¡El video ya está público en Everyone!")
                    break
            print("Video aún en revisión o selector no accesible, esperando 15s...")
            time.sleep(15)

        page.screenshot(path=str(SCRATCH_DIR / "moe_public_check.png"))
        print("Screenshot guardado en scratch/moe_public_check.png")
        browser.close()

if __name__ == "__main__":
    make_moe_public()
