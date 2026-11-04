import time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
URL = "https://www.tiktok.com/@magical_prints/video/7700357001221524767"
SCRATCH_DIR = Path(r"C:\Carlos\noticias_podcast\scratch")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="es-ES"
    )
    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    time.sleep(2)
    
    # saltar al segundo 23 del video
    page.evaluate("""
        const v = document.querySelector('video');
        if (v) {
            v.currentTime = 22;
            v.pause();
        }
    """)
    time.sleep(2)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_magical_prints_cookie_result.png"))
    
    browser.close()
