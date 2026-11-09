import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
REELS_DIR = BASE_DIR / "reels"

PASCUAL_EPISODE = {
    "file": REELS_DIR / "sIA_Storybook_15_Pascual_Boing_Cooperativa_TetraPak.mp4",
    "caption": (
        "🥭 ¿Cómo una fábrica mexicana de refrescos cuyos dueños cerraron las puertas para no pagar un aumento salarial "
        "se convirtió en una cooperativa obrera que factura miles de millones? "
        "De la huelga de 1982 en San Rafael al triángulo de 6 capas de Tetra Pak y la pulpa de mango natural. "
        "🚗 En tu coche escúchanos en Spotify (sIA Podcast) | 📱 Diagramas tácticos completos en TikTok y YouTube (@escucha_sia). "
        "#pascualboing #cooperativa #historiademexico #hechoenmexico #ingenieria #empresas #tetrapak #siapodcast"
    )
}

def dismiss_modals(page):
    for _ in range(3):
        # Manejar modal de automatic content checks
        turn_on_btn = page.locator("button:has-text('Turn on'), button:has-text('Activar')").first
        if turn_on_btn.count() > 0 and turn_on_btn.is_visible():
            turn_on_btn.click()
            time.sleep(1)

        modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal], div[role='dialog']").all()
        dismissed = False
        for m in modals:
            if m.is_visible():
                btn = m.locator("button:has-text('Turn on'), button:has-text('Activar'), button:has-text('Cancel'), button:has-text('Cancelar'), button:has-text('Entendido'), button:has-text('Aceptar'), button[aria-label='close']").first
                if btn.count() > 0 and btn.is_visible():
                    btn.click()
                    time.sleep(1)
                    dismissed = True
        if not dismissed:
            page.keyboard.press("Escape")
            break

def upload_pascual():
    video_path = PASCUAL_EPISODE["file"]
    caption = PASCUAL_EPISODE["caption"]

    print("=======================================================")
    print(f"🚀 INICIANDO SUBIDA A TIKTOK STUDIO: {video_path.name}")
    print(f"   Tamaño: {video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=======================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()

        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        page.mouse.click(600, 200)
        time.sleep(1)

        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(str(video_path))

        print("[*] Subiendo video maestro a TikTok Studio (esperando 45s para carga y análisis)...")
        time.sleep(45)
        dismiss_modals(page)

        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)

        # Inset caption
        editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
        try:
            editor.click(force=True, timeout=5000)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(caption, delay=15)
            time.sleep(2)
        except Exception:
            page.evaluate(f"""() => {{
                const el = document.querySelector("div.public-DraftEditor-content, div[contenteditable='true']");
                if (el) {{
                    el.innerText = `{caption}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(2)

        dismiss_modals(page)
        time.sleep(1)

        dismiss_modals(page)
        time.sleep(2)

        page.screenshot(path=str(SCRATCH_DIR / "ready_to_post_pascual.png"))
        print("[*] Screenshot capturado: scratch/ready_to_post_pascual.png")

        # Scroll to bottom to reveal Post button
        print("[*] Haciendo scroll al final del formulario...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        dismiss_modals(page)

        # Select post button inside the upload footer
        post_btn = page.locator("div.btn-post button, button:has-text('Publicar'), button:has-text('Post')").last
        if post_btn.is_visible():
            post_btn.click(force=True)
            print("[+] ¡Clic en Publicar realizado con éxito!")
            time.sleep(12)
            dismiss_modals(page)
            time.sleep(5)
            page.screenshot(path=str(SCRATCH_DIR / "published_pascual_success.png"))
            print("[+] Publicación completada. Guardado en scratch/published_pascual_success.png")
        else:
            print("[!] No se encontró el botón Post visible.")
            page.screenshot(path=str(SCRATCH_DIR / "post_btn_not_found.png"))

        browser.close()

if __name__ == "__main__":
    upload_pascual()
