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
    print("[*] Accediendo a TikTok Studio Content...")
    page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    # En la captura antes vista:
    # Columna "Acciones" está alrededor de x=800 a 950, y las filas están en y=240, y=340, etc.
    # Usemos page.mouse para hacer click en el botón '...' de la primera fila
    # Coordenadas aproximadas según la captura:
    # Ancho 1280 x 950:
    # Fila 1 (BIQU Panda Treat): y ~ 260
    # Los 4 botones de acción están a la derecha:
    # Botón 1 (Lápiz): x ~ 810
    # Botón 2 (Flecha/Analítica): x ~ 848
    # Botón 3 (Comentario): x ~ 886
    # Botón 4 (Tres puntos ...): x ~ 924
    
    print("[*] Haciendo clic en coordenadas del botón '...' de la fila 1 (x=925, y=260)...")
    page.mouse.click(925, 260)
    time.sleep(2)
    page.screenshot(path=str(SCRATCH_DIR / "click_dots_row1.png"))
    
    # Revisar si se abrió un popover / menú
    menu_items = page.locator("div[role='menu'], div[role='tooltip'], div[class*='popover'], div[class*='menu']").all_text_contents()
    print("[*] Elementos de menú detectados:", menu_items)
    
    # Buscar si aparece 'Eliminar' o 'Delete'
    del_btn = page.locator("text='Eliminar', text='Delete', text='Borrar'")
    print(f"[*] Botones Eliminar detectados: {del_btn.count()}")
    if del_btn.count() > 0:
        print("[*] HACIENDO CLIC EN ELIMINAR...")
        del_btn.first.click()
        time.sleep(2)
        page.screenshot(path=str(SCRATCH_DIR / "delete_modal.png"))
        
        # Confirmar en el modal de confirmación
        confirm = page.locator("button:has-text('Eliminar'), button:has-text('Delete'), button:has-text('Aceptar')").last
        if confirm.count() > 0 and confirm.is_visible():
            print("[*] Confirmando eliminación de fila 1...")
            confirm.click()
            time.sleep(4)
            print("[OK] Video 1 eliminado con éxito.")
            
    page.screenshot(path=str(SCRATCH_DIR / "after_delete_1.png"))
    
    # Ahora repetir para el siguiente video que quedó en la primera fila (Code Mode con audio viejo)
    time.sleep(3)
    print("\n[*] Procediendo con el segundo video con audio erróneo...")
    print("[*] Haciendo clic en coordenadas del botón '...' de la fila 1 (x=925, y=260)...")
    page.mouse.click(925, 260)
    time.sleep(2)
    
    del_btn2 = page.locator("text='Eliminar', text='Delete', text='Borrar'")
    if del_btn2.count() > 0:
        print("[*] HACIENDO CLIC EN ELIMINAR FILA 2...")
        del_btn2.first.click()
        time.sleep(2)
        confirm2 = page.locator("button:has-text('Eliminar'), button:has-text('Delete'), button:has-text('Aceptar')").last
        if confirm2.count() > 0 and confirm2.is_visible():
            print("[*] Confirmando eliminación de fila 2...")
            confirm2.click()
            time.sleep(4)
            print("[OK] Video 2 eliminado con éxito.")
            
    page.screenshot(path=str(SCRATCH_DIR / "after_delete_2.png"))
    context.storage_state(path=str(SESSION_FILE))
    browser.close()
