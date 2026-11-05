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
    
    # Evaluar qué elemento está en (925, 260)
    info = page.evaluate("""() => {
        const el = document.elementFromPoint(925, 260);
        return {
            tagName: el ? el.tagName : null,
            className: el ? el.className : null,
            outerHTML: el ? el.outerHTML : null,
            parentHTML: el && el.parentElement ? el.parentElement.outerHTML : null
        };
    }""")
    print("Element at (925, 260):", info)
    
    # Hacer click en ese elemento directamente con JS
    page.evaluate("""() => {
        const el = document.elementFromPoint(925, 260);
        if (el) {
            el.click();
            if (el.parentElement) el.parentElement.click();
        }
    }""")
    time.sleep(2)
    page.screenshot(path=str(SCRATCH_DIR / "js_click_dots.png"))
    
    # Buscar qué aparece en el DOM después del click
    popovers = page.locator("div[role='tooltip'], div[class*='popover'], ul, div[class*='menu']").all_text_contents()
    print("Popovers detected:", popovers)
    
    browser.close()
