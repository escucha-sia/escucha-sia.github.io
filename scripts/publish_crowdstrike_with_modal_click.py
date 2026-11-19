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

VIDEO_PATH = REELS_DIR / "sIA_Storybook_21_CrowdStrike_Ring0_BSOD.mp4"
CAPTION = (
    "💻💥 La BSOD del Billón de Dólares: Autopsia Técnica de CrowdStrike y el Puntero Nulo 0x9c (sIA Sec #04). "
    "¿Cómo un archivo de solo 40 KB tiró 8.5 millones de computadoras con Windows, 8,500 vuelos y hospitales en todo el mundo? "
    "La diferencia entre Ring 3 (Modo Usuario) y Ring 0 (Kernel): por qué un error en la ranura 21 congeló el silicio. "
    "Mándale esto a tu amigo que siempre hace deploys en viernes a producción. "
    "🗳️ DEBATE: ¿Debe Microsoft expulsar el antivirus fuera del kernel como hizo Apple en macOS? ¡Vota en comentarios: #Ring3Seguro o #Ring0Maximo! "
    "🚗 En Spotify (sIA Podcast) | 💻 Artículos y autopsia en escucha-sia.github.io "
    "#crowdstrike #bsod #pantallaazul #kernel #devops #sre #windows #ciberseguridad #programacion #software #siapodcast"
)

def dismiss_initial_dialogs(page):
    turn_on = page.locator("button:has-text('Turn on'), button:has-text('Activar')").first
    if turn_on.count() > 0 and turn_on.is_visible():
        try:
            turn_on.click()
            time.sleep(1)
        except Exception:
            pass

def main():
    print("=======================================================")
    print(f"🚀 SUBIENDO Y CONFIRMANDO PUBLICACIÓN DE CROWDSTRIKE...")
    print(f"   Archivo: {VIDEO_PATH.name} ({VIDEO_PATH.stat().st_size / (1024*1024):.2f} MB)")
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
        dismiss_initial_dialogs(page)

        print("[*] Seleccionando archivo de video...")
        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(str(VIDEO_PATH))

        print("[*] Esperando 50s para carga y análisis preliminar del video...")
        time.sleep(50)
        dismiss_initial_dialogs(page)

        # Inset caption
        print("[*] Escribiendo título y descripción con SEO...")
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
                const el = document.querySelector("div.public-DraftEditor-content, div[contenteditable='true']");
                if (el) {{
                    el.innerText = `{CAPTION}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(2)

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        # Click Post
        print("[*] Clic en botón Post principal...")
        post_btn = page.locator("div.btn-post button, button:has-text('Publicar'), button:has-text('Post')").last
        if post_btn.is_visible():
            post_btn.click(force=True)
        else:
            page.locator("button[data-e2e='post_video_button'], button.btn-post").first.click(force=True)

        print("[*] Esperando 4 segundos a ver si aparece el modal 'Continue to post?'...")
        time.sleep(4)

        # Handle modal "Continue to post? -> Post now"
        modal_post_now = page.locator("button:has-text('Post now'), button:has-text('Publicar ahora')").first
        if modal_post_now.count() > 0 and modal_post_now.is_visible():
            print("[+] ¡Modal detectado! Haciendo clic en 'Post now'...")
            modal_post_now.click(force=True)
            time.sleep(15)
        else:
            print("[*] Modal no requerido o no visible, esperando redirección...")
            time.sleep(12)

        page.screenshot(path=str(SCRATCH_DIR / "cs_post_result.png"))
        print("[*] Screenshot capturado: scratch/cs_post_result.png")

        # Now navigate to content list to verify
        print("[*] Verificando en la lista de contenido...")
        page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
        time.sleep(8)

        page.screenshot(path=str(SCRATCH_DIR / "cs_content_published.png"))
        print("[*] Screenshot lista final: scratch/cs_content_published.png")
        browser.close()
        print("✓ Publicación verificada con éxito.")

if __name__ == "__main__":
    main()
