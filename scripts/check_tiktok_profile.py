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
    print("[*] Navegando a la página de perfil en TikTok...", flush=True)
    page.goto("https://www.tiktok.com/@sia67486", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_profile_current.png"))
    print("[+] Captura de perfil guardada en tiktok_profile_current.png", flush=True)
    
    # Check if there is an "Editar perfil" button
    edit_btn = page.locator("button:has-text('Editar perfil'), a:has-text('Editar perfil'), div:has-text('Editar perfil')").first
    print(f"[*] Botón 'Editar perfil' visible: {edit_btn.count() > 0}", flush=True)
    if edit_btn.count() > 0:
        edit_btn.click()
        time.sleep(3)
        page.screenshot(path=str(SCRATCH_DIR / "tiktok_profile_edit_modal.png"))
        print("[+] Modal de edición capturado en tiktok_profile_edit_modal.png", flush=True)

    browser.close()
