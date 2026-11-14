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

APAGON_EPISODE = {
    "file": REELS_DIR / "sIA_Storybook_20_Microsoft_Apagon_Global_12Nov.mp4",
    "caption": (
        "🌐⚡ El Apagón Global: La Autopsia Técnica de las 20 Horas sin Microsoft (Dilogía Microsoft - Parte 2). "
        "¿Cómo un script de balanceo de red desató una falla en cascada de Health Checks y la estampida del Thundering Herd en 74 países? "
        "Bancos, aerolíneas y hospitales a oscuras: por qué la nube se desconectó a sí misma. "
        "💬 DEBATE: ¿Prohibir por ley el monocultivo de nube (#MultiCloud) o la culpa fue de los despidos masivos (#HumanInTheLoop)? ¡Comenta tu postura! "
        "🚗 En Spotify (sIA Podcast) | 💻 Artículos y autopsia en escucha-sia.github.io "
        "#microsoft #apagon #azure #devops #sre #thunderingherd #cloud #redes #ingenieria #software #siapodcast"
    )
}

def dismiss_modals(page):
    for _ in range(4):
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

def upload_apagon():
    video_path = APAGON_EPISODE["file"]
    caption = APAGON_EPISODE["caption"]

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

        print("[*] Navegando a TikTok Studio Upload...")
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        page.mouse.click(600, 200)
        time.sleep(1)

        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(str(video_path))

        print("[*] Subiendo video maestro a TikTok Studio (esperando 60s para carga y análisis de video de 4:18 min)...")
        time.sleep(60)
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
        time.sleep(2)

        page.screenshot(path=str(SCRATCH_DIR / "ready_to_post_apagon.png"))
        print("[*] Screenshot capturado: scratch/ready_to_post_apagon.png")

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
            time.sleep(15)
        else:
            print("[-] No se encontró el botón de publicar visible, intentando selector alternativo...")
            btn_alt = page.locator("button[data-e2e='post_video_button'], button.btn-post").first
            if btn_alt.is_visible():
                btn_alt.click(force=True)
                print("[+] ¡Clic en Publicar alternativo realizado!")
                time.sleep(15)

        page.screenshot(path=str(SCRATCH_DIR / "after_post_apagon.png"))
        print("[*] Screenshot tras publicación: scratch/after_post_apagon.png")
        browser.close()
        print("✓ Sesión de subida completada.")

if __name__ == "__main__":
    upload_apagon()
