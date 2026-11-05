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
    
    # Buscar todos los elementos en la fila 1 (y entre 210 y 290)
    row_elements = page.evaluate("""() => {
        const all = document.querySelectorAll('*');
        const list = [];
        for (let el of all) {
            const r = el.getBoundingClientRect();
            if (r.y >= 210 && r.y <= 290 && r.x >= 950 && r.width > 10 && r.height > 10) {
                list.push({
                    tagName: el.tagName,
                    className: el.className,
                    x: Math.round(r.x),
                    y: Math.round(r.y),
                    w: Math.round(r.width),
                    h: Math.round(r.height),
                    html: el.outerHTML.substring(0, 100)
                });
            }
        }
        return list;
    }""")
    
    print("Elements in action column (x >= 950, 210 <= y <= 290):")
    for e in row_elements:
        print("  >", e)
        
    browser.close()
