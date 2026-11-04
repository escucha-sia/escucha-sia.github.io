import json, time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
URL = "https://www.tiktok.com/@johnolven/video/7702949507830435080"
SCRATCH_DIR = Path(r"C:\Carlos\noticias_podcast\scratch")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="es-ES"
    )
    page = context.new_page()
    print(f"[*] Accediendo a {URL}...")
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)
    
    screenshot_path = SCRATCH_DIR / "tiktok_johnolven_frame1.png"
    page.screenshot(path=str(screenshot_path))
    print(f"[OK] Captura 1 guardada en: {screenshot_path}")
    
    title = page.title()
    print("Page Title:", title)
    
    body_text = page.inner_text("body")
    lines = [l.strip() for l in body_text.split("\n") if l.strip()]
    print("\n--- PRIMERAS LÍNEAS DE CONTENIDO ---")
    for l in lines[:45]:
        print("  >", l)
        
    # Salto hacia la mitad del video
    page.evaluate("""
        const v = document.querySelector('video');
        if (v) {
            v.currentTime = 15;
            v.pause();
        }
    """)
    time.sleep(2)
    screenshot_path2 = SCRATCH_DIR / "tiktok_johnolven_frame2.png"
    page.screenshot(path=str(screenshot_path2))
    print(f"[OK] Captura 2 guardada en: {screenshot_path2}")
    
    browser.close()
