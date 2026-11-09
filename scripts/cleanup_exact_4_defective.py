import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

def delete_row_2(page, index_num):
    print(f"\n[Paso {index_num}/4] Abriendo menú de fila 2 en (1178, 341)...")
    page.mouse.click(1178, 341)
    time.sleep(1.5)

    # Click the 'Eliminar' text in the popover
    del_option = page.locator("div:has-text('Eliminar'), span:has-text('Eliminar')").filter(has_text="Eliminar").last
    if del_option.count() > 0 and del_option.is_visible():
        print(f"  [Paso {index_num}/4] Clic en 'Eliminar' del menú popover...")
        del_option.click()
        time.sleep(1.5)

        # Confirm in modal
        confirm_btn = page.locator("div[role='dialog'] button:has-text('Eliminar'), button:has-text('Eliminar')").last
        if confirm_btn.count() > 0 and confirm_btn.is_visible():
            print(f"  [Paso {index_num}/4] Confirmando eliminación en modal...")
            confirm_btn.click()
            time.sleep(4)
            print(f"  ✅ [Paso {index_num}/4] Fila 2 eliminada exitosamente.")
            return True
        else:
            print("  ❌ No apareció el botón de confirmación en el modal.")
    else:
        print("  ❌ No se desplegó el menú con 'Eliminar'.")
    return False

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES"
        )
        page = context.new_page()
        page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        # Delete the 4 defective items sequentially
        for i in range(1, 5):
            success = delete_row_2(page, i)
            if not success:
                page.screenshot(path=str(SCRATCH_DIR / f"delete_fail_step_{i}.png"))
                break
            time.sleep(2)

        time.sleep(3)
        page.reload(wait_until="domcontentloaded")
        time.sleep(6)
        page.screenshot(path=str(SCRATCH_DIR / "final_clean_table.png"))
        context.storage_state(path=str(SESSION_FILE))
        browser.close()
        print("\n🎉 Limpieza de los 4 videos defectuosos completada.")

if __name__ == "__main__":
    main()
