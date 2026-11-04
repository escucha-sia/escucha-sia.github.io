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
    time.sleep(4)
    
    # Click en play si está pausado
    video = page.locator("video").first
    if video.count() > 0:
        src = video.get_attribute("src")
        print("Video SRC:", src[:100] if src else "None")
        
    # Extraer comentarios
    comments = page.locator("p[data-e2e='comment-level-1'], [class*='DivCommentContentContainer']").all_text_contents()
    print("\n--- COMENTARIOS ---")
    for c in comments[:20]:
        print("COM:", c.strip().replace("\n", " "))
        
    # Tomar captura más adelante en el video
    time.sleep(6)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_magical_prints_frame2.png"))
    time.sleep(6)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_magical_prints_frame3.png"))
    time.sleep(6)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_magical_prints_frame4.png"))
    
    browser.close()
