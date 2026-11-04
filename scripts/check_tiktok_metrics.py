import time
from pathlib import Path
from playwright.sync_api import sync_playwright

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
    print("[*] Accediendo a TikTok Studio / Contenido...", flush=True)
    page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
    time.sleep(6)
    
    screenshot_path = SCRATCH_DIR / "tiktok_studio_current_metrics.png"
    page.screenshot(path=str(screenshot_path))
    print(f"[OK] Captura de pantalla guardada en: {screenshot_path}", flush=True)
    
    # Intentar extraer filas de la tabla de contenido
    rows = page.locator("tr, div[data-e2e='table-row'], div[role='row']")
    count = rows.count()
    print(f"[*] Filas detectadas: {count}", flush=True)
    
    # Imprimir texto visible relevante
    text = page.inner_text("body")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    # Filtrar lineas con numeros de vistas o titulos
    print("\n--- RESUMEN TEXTO TIKTOK STUDIO ---")
    for i, line in enumerate(lines[:120]):
        if any(term in line.lower() for term in ["reproducc", "visualiz", "like", "me gusta", "todo el mundo", "público", "montes", "crowdstrike", "lakehouse", "bambu", "mullenweg", "niñera"]):
            print(f"  > {line}")
            
    context.storage_state(path=str(SESSION_FILE))
    browser.close()
