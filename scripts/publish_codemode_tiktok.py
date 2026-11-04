import time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SESSION_FILE = Path(r"C:\Carlos\noticias_podcast\tiktok_session.json")
SCRATCH_DIR = Path(r"C:\Carlos\noticias_podcast\scratch")
REELS_DIR = Path(r"C:\Carlos\noticias_podcast\reels")

REEL_FILENAME = "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4"
video_path = REELS_DIR / REEL_FILENAME

caption = "¿RIP MCP? Por qué la IA ya no llama a herramientas una por una: Cloudflare Code Mode, 2,500 endpoints en 1,000 tokens y sandboxes V8. Episodio completo en Spotify (sIA) y blog en perfil. #mcp #agentesia #cloudflare #anthropic #programacion #softwareengineer #siapodcast"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_FILE),
        viewport={"width": 1280, "height": 950},
        locale="es-ES"
    )
    page = context.new_page()
    print("[*] Accediendo a TikTok Studio...")
    page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)
    
    # Manejar modales que aparezcan antes
    modal_btn = page.locator("button:has-text('Activar'), button:has-text('Ahora no'), button:has-text('Aceptar'), button:has-text('Entendido')")
    if modal_btn.count() > 0:
        print("[*] Cerrando modal previo...")
        try:
            modal_btn.first.click(timeout=3000)
            time.sleep(2)
        except Exception:
            pass
            
    file_input = page.locator("input[type='file']").first
    if file_input.count() == 0:
        frame = page.frame_locator("iframe").first
        file_input = frame.locator("input[type='file']").first
        
    print(f"[*] Subiendo archivo: {video_path}...")
    file_input.set_input_files(str(video_path))
    time.sleep(8)
    
    # Revisar si salió el modal de revisiones automáticas
    auto_check_modal = page.locator("button:has-text('Activar'), button:has-text('Ahora no'), button:has-text('Entendido'), button:has-text('Aceptar')")
    if auto_check_modal.count() > 0:
        print("[*] Modal de revisión detectado, haciendo clic...")
        try:
            auto_check_modal.first.click(timeout=3000)
            time.sleep(2)
        except Exception:
            pass
            
    caption_box = page.locator("div[contenteditable='true']").first
    if caption_box.count() > 0:
        print("[*] Escribiendo pie de video...")
        try:
            caption_box.click(force=True, timeout=5000)
        except Exception:
            pass
        caption_box.fill("")
        time.sleep(1)
        caption_box.type(caption, delay=20)
        time.sleep(2)
        
    print("[*] Esperando procesamiento del video (15s)...")
    time.sleep(15)
    
    post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
    if post_btn.count() > 0:
        print("[*] Haciendo clic en Publicar...")
        post_btn.click()
        time.sleep(10)
        print("[OK] Publicación ejecutada en TikTok Studio.")
    else:
        print("[!] Botón publicar no encontrado directamente.")
        
    page.screenshot(path=str(SCRATCH_DIR / "tiktok_upload_codemode_done.png"))
    context.storage_state(path=str(SESSION_FILE))
    browser.close()
