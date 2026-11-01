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
    page.goto("https://www.tiktok.com/", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)
    
    # Avatar en header
    avatar = page.locator("header img, div[data-e2e='profile-icon'], div.tiktok-avatar, img[alt=''], img[data-e2e]").last
    print(f"[*] Localizando avatar: count={avatar.count()}", flush=True)
    avatar.click()
    time.sleep(2)
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_avatar_dropdown.png"))
    
    # Click en 'Ver perfil'
    view_prof = page.locator("a:has-text('Ver perfil'), span:has-text('Ver perfil')").first
    if view_prof.count() > 0:
        print("[*] Clic en 'Ver perfil'...", flush=True)
        view_prof.click()
        time.sleep(4)
        page.screenshot(path=str(SCRATCH_DIR / "tiktok_my_profile.png"))
        
        # Buscar botón editar perfil
        edit_btn = page.locator("button:has-text('Editar perfil'), div:has-text('Editar perfil')").first
        print(f"[*] Botón Editar perfil visible: {edit_btn.count() > 0}", flush=True)
        if edit_btn.count() > 0:
            edit_btn.click()
            time.sleep(2)
            page.screenshot(path=str(SCRATCH_DIR / "tiktok_edit_modal.png"))
            
            # Buscar textarea o input de descripción
            bio_input = page.locator("textarea[placeholder*='descripción'], textarea[name='bio'], textarea").first
            if bio_input.count() > 0:
                print("[*] Escribiendo biografía...", flush=True)
                bio_input.fill("🎧 Podcasts de arquitectura tech y datos.\n👇 Episodios y fuentes en:\nescucha-sia.github.io/links.html")
                time.sleep(1)
                save_btn = page.locator("button:has-text('Guardar')").first
                if save_btn.count() > 0:
                    save_btn.click()
                    time.sleep(3)
                    print("[OK] ¡Biografía guardada exitosamente!", flush=True)
                    page.screenshot(path=str(SCRATCH_DIR / "tiktok_bio_saved.png"))
                    context.storage_state(path=str(SESSION_FILE))

    browser.close()
