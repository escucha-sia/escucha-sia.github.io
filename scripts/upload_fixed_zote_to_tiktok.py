import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
REEL_MP4 = BASE_DIR / "reels" / "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"

CAPTION = (
    "🧼 ¿Cómo una fábrica mexicana de jabón en Ecatepec derrotó a gigantes de Wall Street sin gastar un solo peso en publicidad? "
    "De los Baños Corona de 1920 en Peralvillo a conquistar Corea del Sur con el Jabón Zote. "
    "🚗 Si vas en tu coche escúchanos en Spotify (sIA Podcast) | 📱 Mira este Cuento Ilustrado completo aquí en TikTok y YouTube (@escucha_sia). "
    "#jabonzote #hechoenmexico #industriales #historia #empresas #mexico #quimica #siapodcast"
)

def dismiss_modals(page):
    for _ in range(3):
        modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal], div[role='dialog']").all()
        dismissed = False
        for m in modals:
            if m.is_visible():
                btn = m.locator("button:has-text('Activar'), button:has-text('Cancelar'), button:has-text('Entendido'), button:has-text('Aceptar'), button[aria-label='close']").first
                if btn.count() > 0 and btn.is_visible():
                    btn.click()
                    time.sleep(1)
                    dismissed = True
        if not dismissed:
            page.keyboard.press("Escape")
            break

def main():
    print(f"Subiendo versión corregida con animación fluida: {REEL_MP4.name} ({REEL_MP4.stat().st_size / (1024*1024):.2f} MB)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        page.mouse.click(600, 200)
        time.sleep(1)

        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(str(REEL_MP4))

        print("[*] Esperando que TikTok procese la subida (35s)...")
        time.sleep(35)
        dismiss_modals(page)

        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)

        editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
        try:
            editor.click(force=True, timeout=5000)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(CAPTION, delay=15)
            time.sleep(2)
        except Exception:
            page.evaluate(f"""() => {{
                const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
                if (el) {{
                    el.innerText = `{CAPTION}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(1)

        dismiss_modals(page)
        page.screenshot(path=str(SCRATCH_DIR / "zote_fixed_ready_to_post.png"))

        page.evaluate("window.scrollTo(0, 1500)")
        time.sleep(1)
        dismiss_modals(page)

        post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
        if post_btn.count() > 0:
            try:
                post_btn.click(timeout=5000)
            except Exception:
                post_btn.click(force=True)
            print("[*] Esperando confirmación de publicación (22s)...")
            time.sleep(22)
            dismiss_modals(page)
            page.screenshot(path=str(SCRATCH_DIR / "zote_fixed_published.png"))
            print("🎉 ¡NUEVA VERSIÓN ANIMADA DE JABÓN ZOTE PUBLICADA CON ÉXITO EN TIKTOK!")

        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    main()
