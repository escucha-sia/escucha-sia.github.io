import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"

# The 4 defective/frozen/duplicate videos to clean up
TARGET_KEYWORDS = [
    ("6 nov, 07:02", "Jabon_Zote_La_Corona_Ecatepec"), # Zote v1 duplicate
    ("6 nov, 05:08", "500 milisegundos"),             # XZ Utils frozen teaser
    ("6 nov, 05:06", "440 millones"),                 # Knight Capital frozen teaser
    ("6 nov, 05:05", "TV Box barata"),                # TV Boxes frozen teaser
]

def clean_one_defective_video(page, date_kw, title_kw):
    print(f"\n🔍 Buscando video defectuoso con: '{title_kw}' ({date_kw})...")
    # Click 3 dots on the table matching the row
    # Let's inspect rows
    row_info = page.evaluate(f"""([date_kw, title_kw]) => {{
        const rows = Array.from(document.querySelectorAll('tr, div[class*="table-row"], div[class*="PostItem"]'));
        for (let i = 0; i < rows.length; i++) {{
            const text = rows[i].innerText;
            if (text.includes(title_kw) && text.includes(date_kw)) {{
                // Find the 3 dots button in this row
                const btn = rows[i].querySelector('button[data-tt="components_ActionCell_Clickable"]:last-child') ||
                            rows[i].querySelectorAll('button[data-tt="components_ActionCell_Clickable"]')[3];
                if (btn) {{
                    const rect = btn.getBoundingClientRect();
                    return {{ found: true, x: rect.x + rect.width / 2, y: rect.y + rect.height / 2, index: i }};
                }}
            }}
        }}
        // Fallback: look through all elements with text
        return {{ found: false }};
    }}""", [date_kw, title_kw])

    if not row_info or not row_info.get("found"):
        print(f"⚠️ No se encontró la fila para: {title_kw}")
        return False

    click_x = row_info["x"]
    click_y = row_info["y"]
    print(f"🎯 Fila localizada. Haciendo clic en 3 puntos en ({click_x:.1f}, {click_y:.1f})...")
    page.mouse.click(click_x, click_y)
    time.sleep(1.5)

    # Click Eliminar in the menu
    del_menu = page.locator("div:has-text('Eliminar'), span:has-text('Eliminar')").filter(has_text="Eliminar").last
    if del_menu.count() > 0 and del_menu.is_visible():
        print("🗑️ Menú desplegado. Clic en opción 'Eliminar'...")
        del_menu.click()
        time.sleep(1.5)

        # Modal confirmation button
        confirm_btn = page.locator("div[role='dialog'] button:has-text('Eliminar'), button:has-text('Eliminar')").last
        if confirm_btn.count() > 0 and confirm_btn.is_visible():
            print("⚠️ Confirmando modal de eliminación...")
            confirm_btn.click()
            time.sleep(4)
            print(f"✅ Video '{title_kw}' eliminado exitosamente.")
            return True
        else:
            print("❌ No se encontró el botón de confirmación.")
    else:
        print("❌ No se desplegó el menú 'Eliminar'.")

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

        deleted_count = 0
        for date_kw, title_kw in TARGET_KEYWORDS:
            success = clean_one_defective_video(page, date_kw, title_kw)
            if success:
                deleted_count += 1
                time.sleep(3)
                page.reload(wait_until="domcontentloaded")
                time.sleep(6)

        print(f"\n✨ Proceso de limpieza finalizado. Total videos defectuosos eliminados: {deleted_count}")
        page.screenshot(path=str(SCRATCH_DIR / "content_after_cleanup.png"))
        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    main()
