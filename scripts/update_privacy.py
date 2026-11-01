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
    print("[*] Navegando a Gestión de Contenido en TikTok Studio...", flush=True)
    page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    # Buscar el selector o dropdown de privacidad del primer video
    dropdown = page.locator("span:has-text('Solo yo'), div:has-text('Solo yo')").first
    if dropdown.count() > 0:
        print("[*] Click en dropdown de privacidad...", flush=True)
        dropdown.click()
        time.sleep(2)
        # Seleccionar 'Todo el mundo' o 'Público'
        option = page.locator("div[role='option']:has-text('Todo el mundo'), li:has-text('Todo el mundo'), span:has-text('Todo el mundo'), div:has-text('Todo el mundo')").last
        if option.count() > 0:
            print("[*] Cambiando a 'Todo el mundo'...", flush=True)
            option.click()
            time.sleep(2)
            # Confirmar si sale modal de confirmación
            confirm_btn = page.locator("button:has-text('Actualizar'), button:has-text('Guardar'), button:has-text('Aceptar'), button:has-text('Cambiar')").first
            if confirm_btn.count() > 0 and confirm_btn.is_visible():
                confirm_btn.click()
                time.sleep(2)
            print("[OK] Privacidad actualizada a Todo el mundo.", flush=True)
        else:
            print("[!] Opción Todo el mundo no localizada.", flush=True)
    else:
        print("[*] No se encontró dropdown con 'Solo yo' o ya es público.", flush=True)
        
    page.screenshot(path=str(SCRATCH_DIR / "content_privacy_updated.png"))
    context.storage_state(path=str(SESSION_FILE))
    browser.close()
