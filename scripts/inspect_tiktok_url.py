import json, time, sys
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
    print(f"[*] Accediendo a {URL}...")
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    screenshot_path = SCRATCH_DIR / "tiktok_magical_prints.png"
    page.screenshot(path=str(screenshot_path))
    print(f"[OK] Captura guardada en: {screenshot_path}")
    
    # Extraer meta tags y textos
    title = page.title()
    print("Page Title:", title)
    
    # Extraer descripción / pie de video
    desc = page.locator("h1, [data-e2e='browse-video-desc'], span[class*='SpanText']").all_text_contents()
    print("\n--- DESCRIPCIONES ENCONTRADAS ---")
    for d in desc[:10]:
        if d.strip():
            print(" -", d.strip())
            
    # Intentar buscar texto en la página
    body_text = page.inner_text("body")
    lines = [l.strip() for l in body_text.split("\n") if l.strip()]
    print("\n--- PRIMERAS LÍNEAS DE CONTENIDO ---")
    for l in lines[:40]:
        print("  >", l)
        
    browser.close()
