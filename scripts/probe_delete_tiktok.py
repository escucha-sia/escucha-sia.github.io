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
    print("[*] Accediendo a TikTok Studio Content...")
    page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    # Tomar captura inicial
    page.screenshot(path=str(SCRATCH_DIR / "before_delete.png"))
    
    # Buscar botones con icono de 3 puntos (...)
    # En TikTok Studio, los botones de más acciones suelen ser botones con svg o aria-label o dentro de la columna de acciones
    more_btns = page.locator("button:has(svg), div[role='button']:has(svg), span[role='button']").all()
    print(f"[*] Botones detectados: {len(more_btns)}")
    
    # Buscar específicamente el botón de 3 puntos en las primeras filas
    action_btns = page.locator("div[class*='action'], td:last-child button, div[role='row'] button").all()
    print(f"[*] Botones de acción detectados: {len(action_btns)}")
    
    # Localizar el primer botón de 3 puntos en la fila superior
    # En la captura previa vimos 4 iconos en acciones: lápiz, ojo/analíticas, globo de comentarios, y tres puntos (...)
    dots_btns = page.locator("button:has-text('···'), button:has-text('...'), svg[class*='more'], button[aria-label*='más'], button[aria-label*='More']").all()
    print(f"[*] Botones '...' detectados: {len(dots_btns)}")
    
    context.storage_state(path=str(SESSION_FILE))
    browser.close()
