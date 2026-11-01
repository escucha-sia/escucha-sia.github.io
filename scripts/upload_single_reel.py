import sys
import time
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

def upload_video(video_path: Path, caption: str, dry_run: bool = False):
    print("="*60, flush=True)
    print(f"🚀 INICIANDO SUBIDA A TIKTOK: {video_path.name}", flush=True)
    print("="*60, flush=True)
    
    if not video_path.exists():
        print(f"[-] Error: Archivo de video no existe: {video_path}", flush=True)
        return False
        
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        print("[*] Accediendo a TikTok Studio...", flush=True)
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)
        
        # Buscar input file
        file_input = page.locator("input[type='file']").first
        if not file_input:
            print("[-] No se encontró input[type='file']", flush=True)
            browser.close()
            return False
            
        print(f"[*] Cargando archivo: {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)...", flush=True)
        file_input.set_input_files(str(video_path))
        
        # Esperar a que el uploader procese el video y muestre el formulario
        print("[*] Esperando procesamiento del video (15-20 segundos)...", flush=True)
        time.sleep(15)
        
        upload_form_screen = SCRATCH_DIR / f"upload_form_{video_path.stem}.png"
        page.screenshot(path=str(upload_form_screen))
        print(f"[+] Captura del formulario guardada en: {upload_form_screen}", flush=True)
        
        # Localizar el editor de texto / caption
        # En TikTok suele ser un div contenteditable o un DraftEditor
        editor = page.locator("div[contenteditable='true'], div[class*='notranslate'][contenteditable='true'], div[class*='DraftEditor-editorContainer'] [contenteditable='true']").first
        if editor.count() > 0:
            print("[*] Editor de leyenda encontrado. Escribiendo texto y hashtags...", flush=True)
            editor.click()
            # Limpiar contenido inicial si lo hay
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(1)
            # Escribir el caption
            editor.type(caption, delay=40)
            time.sleep(2)
        else:
            print("[!] Advertencia: No se encontró div contenteditable estándar. Buscando textarea...", flush=True)
            textareas = page.locator("textarea").all()
            if textareas:
                textareas[0].fill(caption)
                time.sleep(1)
                
        after_caption_screen = SCRATCH_DIR / f"upload_caption_{video_path.stem}.png"
        page.screenshot(path=str(after_caption_screen))
        print(f"[+] Captura con texto guardada en: {after_caption_screen}", flush=True)
        
        # Buscar botón de Publicar
        # Puede ser button:has-text('Publicar') o button:has-text('Post')
        post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post'), button[data-e2e='post_video_button']").first
        
        if dry_run:
            print("[DRY-RUN] No se presiona el botón de publicar. Formulario listo para revisión.", flush=True)
            browser.close()
            return True
            
        if post_btn.count() > 0 and post_btn.is_visible():
            print("[*] Clickeando botón de 'Publicar'...", flush=True)
            post_btn.click()
            
            # Esperar confirmación de publicación (10-15s)
            print("[*] Esperando confirmación de TikTok...", flush=True)
            time.sleep(12)
            
            final_screen = SCRATCH_DIR / f"upload_success_{video_path.stem}.png"
            page.screenshot(path=str(final_screen))
            print(f"[+] Captura final guardada en: {final_screen}", flush=True)
            print(f"🎉 ¡VIDEO PUBLICADO CON ÉXITO: {video_path.name}!", flush=True)
            
            # Actualizar storage_state con las cookies más recientes
            context.storage_state(path=str(SESSION_FILE))
            browser.close()
            return True
        else:
            print("[-] No se encontró botón 'Publicar' visible. Revisa la captura.", flush=True)
            browser.close()
            return False

if __name__ == "__main__":
    reels_dir = BASE_DIR / "reels"
    r1 = reels_dir / "sIA_Reel_Stupy_01_Mito_IA_Codigo.mp4"
    cap1 = "¿Copiar código de la IA te hace 10x más rápido o 10x más bugs? Un estudio de Stanford y GitHub reveló la letra chiquita. #ia #programacion #softwareengineer #coding #aprenderaprogramar #devhumor"
    upload_video(r1, cap1, dry_run=False)
