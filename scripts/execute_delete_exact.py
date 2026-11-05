import time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
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
    page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    # 1. Eliminar primer video (Reel 09 con audio erróneo)
    print("[*] Haciendo clic en los tres puntos de la fila 1 en (x=1178, y=241)...")
    page.mouse.click(1178, 241)
    time.sleep(1.5)
    page.screenshot(path=str(SCRATCH_DIR / "menu_dots_opened.png"))
    
    # Buscar opción Eliminar en el popover
    del_btn = page.locator("div:has-text('Eliminar'), span:has-text('Eliminar'), li:has-text('Eliminar')").last
    if del_btn.count() > 0 and del_btn.is_visible():
        print("[*] Clic en 'Eliminar' del menú...")
        del_btn.click()
        time.sleep(1.5)
        
        # Confirmar en el modal de confirmación
        confirm_btn = page.locator("button:has-text('Eliminar')").last
        if confirm_btn.count() > 0 and confirm_btn.is_visible():
            print("[*] Confirmando eliminación de video 1...")
            confirm_btn.click()
            time.sleep(3)
            print("[OK] Video 1 eliminado con éxito.")
            
    # 2. Ahora el video 2 (Reel 08 con audio erróneo) pasa a ser la fila 1
    time.sleep(2)
    print("\n[*] Procediendo con el segundo video con audio erróneo...")
    print("[*] Haciendo clic en los tres puntos de la fila 1 en (x=1178, y=241)...")
    page.mouse.click(1178, 241)
    time.sleep(1.5)
    
    del_btn2 = page.locator("div:has-text('Eliminar'), span:has-text('Eliminar'), li:has-text('Eliminar')").last
    if del_btn2.count() > 0 and del_btn2.is_visible():
        print("[*] Clic en 'Eliminar' del menú...")
        del_btn2.click()
        time.sleep(1.5)
        
        confirm_btn2 = page.locator("button:has-text('Eliminar')").last
        if confirm_btn2.count() > 0 and confirm_btn2.is_visible():
            print("[*] Confirmando eliminación de video 2...")
            confirm_btn2.click()
            time.sleep(3)
            print("[OK] Video 2 eliminado con éxito.")
            
    page.screenshot(path=str(SCRATCH_DIR / "after_both_deleted.png"))
    context.storage_state(path=str(SESSION_FILE))
    browser.close()
