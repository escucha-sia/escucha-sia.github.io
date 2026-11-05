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
    
    # Buscar todos los elementos interactivos en la última columna de las filas
    # Busquemos los botones con clase TUXButton o similar
    buttons_info = page.evaluate("""() => {
        const rows = document.querySelectorAll('[data-tt*="RowLayout"]');
        const results = [];
        for (let r of rows) {
            const btns = r.querySelectorAll('button, div[role="button"], span[role="button"]');
            for (let b of btns) {
                const rect = b.getBoundingClientRect();
                results.push({
                    text: b.innerText,
                    ariaLabel: b.getAttribute('aria-label'),
                    rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
                    html: b.outerHTML.substring(0, 100)
                });
            }
        }
        return results;
    }""")
    
    print(f"Total action buttons in rows: {len(buttons_info)}")
    for b in buttons_info[:15]:
        print("  BTN:", b)
        
    browser.close()
