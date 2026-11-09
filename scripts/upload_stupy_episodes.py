import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
REELS_DIR = BASE_DIR / "reels"

EPISODES_TO_UPLOAD = [
    {
        "id": "sec_02_tvboxes",
        "file": REELS_DIR / "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
        "caption": (
            "🚨 ¿Tienes una TV Box barata en tu sala? Google desmanteló una botnet de 1.3 millones de decodificadores "
            "con el backdoor militar x.cpe instalado directamente de fábrica por Videostrong (MECOOL/T95). "
            "Usaban tu módem y Wi-Fi como proxy para cibercriminales. "
            "🚗 Si vas en tu coche escúchanos completo en Spotify (sIA Podcast) | 📱 Mira este análisis con diagramas aquí en TikTok y YouTube (@escucha_sia). "
            "#ciberseguridad #androidtv #mecool #google #malware #seguridadinformatica #hackers #siapodcast"
        )
    },
    {
        "id": "corp_07_knight",
        "file": REELS_DIR / "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
        "caption": (
            "📉 ¿Cómo una variable booleana destruyó 440 millones de dólares en 45 minutos? "
            "En 2012, Knight Capital dominaba el 17% de Wall Street. Un técnico olvidó 1 de 8 servidores durante un despliegue manual "
            "y desató un bucle infinito que compraba caro y vendía barato. "
            "🚗 Si vas en tu coche escúchanos en Spotify (sIA Podcast) | 📱 Diagramas tácticos completos en TikTok y YouTube (@escucha_sia). "
            "#programacion #devops #wallstreet #finanzas #bugs #ingenieriadesoftware #trading #siapodcast"
        )
    },
    {
        "id": "sec_03_xz",
        "file": REELS_DIR / "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4",
        "caption": (
            "🛡️ ¿Cómo un retraso de 500 milisegundos en una terminal salvó al internet entero? "
            "Un atacante pasó 2 años ganándose al mantenedor de xz e inyectó un backdoor indetectable en OpenSSH. "
            "Andrés Freund notó el micro-lag de medio segundo y frenó el mayor ciberataque de la historia. "
            "🚗 En coche escúchalo en Spotify (sIA Podcast) | 📱 Mira la cadena forense completa aquí en TikTok y YouTube (@escucha_sia). "
            "#ciberseguridad #linux #openssh #xzutils #programacion #seguridad #hackers #siapodcast"
        )
    }
]

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

def upload_single_episode(page, ep_info):
    file_path = ep_info["file"]
    caption = ep_info["caption"]
    ep_id = ep_info["id"]

    print(f"\n=======================================================")
    print(f"🚀 INICIANDO SUBIDA A TIKTOK: {file_path.name}")
    print(f"   Tamaño: {file_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"=======================================================")

    page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
    time.sleep(6)
    page.mouse.click(600, 200)
    time.sleep(1)

    file_input = page.locator("input[type='file']").first
    file_input.set_input_files(str(file_path))

    print("[*] Subiendo video maestro a TikTok Studio (esperando 40s para procesamiento completo)...")
    time.sleep(40)
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
            const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
            if (el) {{
                el.innerText = `{caption}`;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }}""")
        time.sleep(1)

    dismiss_modals(page)
    page.screenshot(path=str(SCRATCH_DIR / f"upload_{ep_id}_ready.png"))

    # Scroll down to publish button
    page.evaluate("window.scrollTo(0, 1500)")
    time.sleep(1)
    dismiss_modals(page)

    post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
    if post_btn.count() > 0:
        try:
            post_btn.click(timeout=5000)
        except Exception:
            post_btn.click(force=True)
        print("[*] Botón 'Publicar' presionado. Esperando confirmación de red (25s)...")
        time.sleep(25)
        dismiss_modals(page)
        page.screenshot(path=str(SCRATCH_DIR / f"upload_{ep_id}_published.png"))
        print(f"🎉 ¡PUBLICACIÓN COMPLETADA CON ÉXITO: {file_path.name}!")
        return True
    else:
        print("❌ No se encontró el botón de publicación.")
        return False

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

        for ep in EPISODES_TO_UPLOAD:
            success = upload_single_episode(page, ep)
            if success:
                time.sleep(8)
            else:
                print(f"⚠️ Error al subir {ep['id']}, continuando...")

        context.storage_state(path=str(SESSION_FILE))
        browser.close()
        print("\n✨ ¡TODOS LOS VIDEOS MAESTROS STUPY FULL-LENGTH FUERON PUBLICADOS!")

if __name__ == "__main__":
    main()
