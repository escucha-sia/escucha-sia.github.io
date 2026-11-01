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
    print("[*] Verificando perfil actualizado en TikTok: @escucha_sia...", flush=True)
    page.goto("https://www.tiktok.com/@escucha_sia", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    # Cerrar posibles modales
    page.keyboard.press("Escape")
    time.sleep(1)
    
    out_img = SCRATCH_DIR / "tiktok_profile_live_escucha_sia.png"
    page.screenshot(path=str(out_img))
    print(f"[+] Captura guardada en: {out_img}", flush=True)
    browser.close()
