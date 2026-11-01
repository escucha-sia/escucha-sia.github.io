import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_FILE = Path(r"C:\Carlos\noticias_podcast\tiktok_session.json")
SCRATCH_DIR = Path(r"C:\Carlos\noticias_podcast\scratch")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_FILE),
        viewport={"width": 1280, "height": 950},
        locale="es-ES"
    )
    page = context.new_page()
    print("[*] Verificando página de ajustes en TikTok...", flush=True)
    page.goto("https://www.tiktok.com/setting", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_setting_page.png"))
    print("[+] Captura en tiktok_setting_page.png", flush=True)
    
    # Intentar ver si hay perfil editable
    print("[*] Buscando enlaces o botones de editar perfil...", flush=True)
    links = page.locator("a, button").all_text_contents()
    relevant = [t.strip() for t in links if any(k in t.lower() for k in ["perfil", "cuenta", "editar", "nombre", "bio", "descripción"])]
    print(f"[*] Elementos relevantes: {relevant[:15]}", flush=True)

    browser.close()
